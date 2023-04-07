from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import logging

from app.crud.base import CRUDBase
from app.models.register_sale import RegisterSale
from app.schemas.register_sale import RegisterSaleCreate, RegisterSaleUpdate, RegisterSaleUpdateStatus\
                                    , RegisterSaleSearch, RegisterSaleUpdateAssess
from app.schemas.assess import AssessBase
from app.models.car import Car
from app.models.car_photo import CarPhoto
from app.models.car_details import CarDetails
from app.models.customer import Customer
from app.models.m_company import MCompany
from app.models.store import Store
from app import crud
from sqlalchemy.sql.elements import or_
from ..api.api_v1.endpoints.format_status import *
from app.constants import Const
logger = logging.getLogger(__name__)


class CRUDRegisterSale(CRUDBase[RegisterSale, RegisterSaleCreate, RegisterSaleUpdate]):
    ASSESS_STATUS = (2, 3)
    LIMIT_SHOW_ONE = 1
    OFFSET_SHOW_ONE = 0

    def update_status_register_sale_by_id(
            self,
            db: Session,
            *,
            obj_in: Union[RegisterSaleUpdateStatus, Dict[str, Any]],
            id: int
    ) -> RegisterSale:
        db_obj = db.query(self.model).filter(RegisterSale.id == id, RegisterSale.delete_flag == 0).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'出品ID{id}が存在しません。')
        db_obj.update_at = datetime.utcnow()

        # TODO: hardcode admin_id
        db_obj.update_id = 888888
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        sale_detail = self.get_register_sale_by_id(db, id=id)

        # response when after update status
        register_sale_update = {}
        if sale_detail.AI_assess_price:
            register_sale_update["AI_assess_price"] = round(float(sale_detail.AI_assess_price))
        register_sale_update["assess_status"] = db_obj.assess_status
        register_sale_update["assess_user_id"] = db_obj.assess_user_id
        register_sale_update["approve_user_id"] = db_obj.approve_user_id
        register_sale_update["assess_comment"] = db_obj.assess_comment
        register_sale_update["assess_price"] = db_obj.assess_price
        return register_sale_update

    def get_register_sales(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Any:
        register_sales = db.query(self.model.id.label("register_sale_id"),
                                  self.model.period_from,
                                  self.model.period_to,
                                  self.model.buy_now_total_price,
                                  self.model.assess_status,
                                  Store.store_name,
                                  Store.store_code,
                                  Car.car_owner,
                                  Car.maker,
                                  Car.car_type,
                                  Car.grade,
                                  Car.id.label("car_code"),
                                  CarDetails.sales_period_start,
                                  CarDetails.aggregation_wholesale_price_market.label("AI_assess_price"),
                                  MCompany.company_name,
                                  MCompany.company_code,
                                  CarPhoto.url.label('thumbnail_url')
                                  ). \
            outerjoin(Car, (RegisterSale.car_id == Car.id)). \
            outerjoin(CarPhoto, (Car.id == CarPhoto.car_id) & (CarPhoto.image_div == 1)). \
            outerjoin(CarDetails, (RegisterSale.car_id == CarDetails.car_id)). \
            outerjoin(MCompany, RegisterSale.company_code == MCompany.company_code). \
            outerjoin(Customer,
                      (Car.car_decision_maker == Customer.customer_code) & (Car.company_code == Customer.company_code)). \
            outerjoin(Store,
                      (Store.store_code == Customer.my_store_code) & (Store.company_code == Customer.company_code)). \
            filter(RegisterSale.assess_status.in_(self.ASSESS_STATUS), RegisterSale.delete_flag == 0).order_by(
            RegisterSale.id.asc())
        total = register_sales.count()
        register_sales = register_sales.offset(skip).limit(limit).all()
        return register_sales, total

    def search_register_sale(
            self, db: Session, *,
            skip: int = 0,
            limit: int = 100,
            item_in: RegisterSaleSearch,
    ) -> Any:
        register_sales = db.query(self.model.id.label("register_sale_id"),
                                  self.model.period_from,
                                  self.model.period_to,
                                  self.model.buy_now_total_price,
                                  self.model.assess_id,
                                  Store.store_name,
                                  Store.store_code,
                                  Car.car_owner,
                                  Car.maker,
                                  Car.car_type,
                                  Car.grade,
                                  Car.id.label("car_code"),
                                  CarDetails.sales_period_start,
                                  CarDetails.aggregation_wholesale_price_market.label("AI_assess_price"),
                                  MCompany.company_name,
                                  MCompany.company_code,
                                  CarPhoto.url.label('thumbnail_url')
                                  ). \
            outerjoin(Car, (RegisterSale.car_id == Car.id)). \
            outerjoin(CarPhoto, (Car.id == CarPhoto.car_id) & (CarPhoto.image_div == 1)). \
            outerjoin(CarDetails, (RegisterSale.car_id == CarDetails.car_id)). \
            outerjoin(MCompany, RegisterSale.company_code == MCompany.company_code). \
            outerjoin(Customer,
                      (Car.car_decision_maker == Customer.customer_code) &
                      (Car.company_code == Customer.company_code)). \
            outerjoin(Store,
                      (Store.store_code == Customer.my_store_code) &
                      (Store.company_code == Customer.company_code))

        # filter
        register_sales = register_sales.filter(RegisterSale.assess_id.in_(self.ASSESS_STATUS),
                                               RegisterSale.delete_flag == 0)
        if item_in.maker:
            register_sales = register_sales.filter(Car.maker.like("%{}%".format(item_in.maker)))
        if item_in.car_type:
            car_type = f"%{item_in.car_type}%"
            car_type_unicode = f"%{format_ascii_to_unicode(item_in.car_type)}%"
            register_sales = register_sales.filter(or_(Car.car_type.like(car_type),
                                                       Car.car_type.like(car_type_unicode)))
        if item_in.grade:
            grade = f"%{item_in.grade}%"
            grade_unicode = f"%{format_ascii_to_unicode(item_in.grade)}%"
            register_sales = register_sales.filter(or_(Car.grade.like(grade),
                                                       Car.grade.like(grade_unicode)))
        if item_in.assess_status:
            register_sales = register_sales.filter(RegisterSale.assess_id.in_(item_in.assess_status))
        if item_in.company_name:
            company_name = f"%{item_in.company_name}%"
            company_name_unicode = f"%{format_ascii_to_unicode(item_in.company_name)}%"
            register_sales = register_sales.filter(or_(MCompany.company_name.like(company_name),
                                                       MCompany.company_name.like(company_name_unicode)))
        if item_in.store_name:
            store_name = f"%{item_in.store_name}%"
            store_name_unicode = f"%{format_ascii_to_unicode(item_in.store_name)}%"
            register_sales = register_sales.filter(or_(Store.store_name.like(store_name),
                                                       Store.store_name.like(store_name_unicode)))
        if item_in.sales_period_start_from:
            register_sales = register_sales.filter(CarDetails.sales_period_start >= item_in.sales_period_start_from)
        if item_in.sales_period_start_to:
            register_sales = register_sales.filter(CarDetails.sales_period_start <= (item_in.sales_period_start_to + "12"))
        if item_in.period_from:
            register_sales = register_sales.filter(RegisterSale.period_from >= item_in.period_from)
        if item_in.period_to:
            period_to = item_in.period_to + Const.TIME_END_DATE
            register_sales = register_sales.filter(RegisterSale.period_to <= period_to)
        if item_in.car_inspection_type:
            register_sales = register_sales.filter(CarDetails.car_inspection_type.like(f"%{item_in.car_inspection_type}%"))
        if item_in.registration_first_date:
            register_sales = register_sales.filter(Car.registration_first_date.like(f"{item_in.registration_first_date}%"))

        # sort
        register_sales = register_sales.order_by(RegisterSale.id.asc())
        total = register_sales.count()
        register_sales = register_sales.offset(skip).limit(limit).all()
        return register_sales, total

    def get_register_sale_by_id(
            self, db: Session, *, id: int
    ) -> RegisterSale:
        register_sale = db.query(
            self.model.price_type,
            self.model.hope_sale_base_price,
            self.model.buy_now_base_price,
            self.model.hope_sale_total_price,
            self.model.buy_now_total_price,
            self.model.hope_sale_base_price_tax,
            self.model.buy_now_base_price_tax,
            self.model.hope_sale_total_price_tax,
            self.model.buy_now_total_price_tax,
            self.model.assess_status,
            self.model.assess_price,
            self.model.period_from,
            self.model.period_to,
            self.model.assess_user_id,
            self.model.approve_user_id,
            self.model.assess_comment,
            Store.store_name,
            Store.store_code,
            Car.car_owner,
            Car.maker,
            Car.car_type,
            Car.grade,
            Car.land_transport_office,
            Car.car_registration_number_type,
            Car.car_registration_number_kana,
            Car.car_registration_number,
            Car.registration_first_date,
            Car.registration_start_date,
            Car.registration_end_date,
            Car.car_mileage,
            Car.id.label("car_code"),
            CarDetails.car_inspection_type,
            CarDetails.sales_period_start,
            CarDetails.aggregation_wholesale_price_market.label("AI_assess_price"),
            MCompany.company_name,
            MCompany.company_code
        ). \
            join(Car, (RegisterSale.car_id == Car.id)). \
            join(CarDetails, (RegisterSale.car_id == CarDetails.car_id)). \
            outerjoin(MCompany, (RegisterSale.company_code == MCompany.company_code)). \
            outerjoin(Customer,
                      (Car.car_decision_maker == Customer.customer_code) & (Car.company_code == Customer.company_code)). \
            outerjoin(Store,
                      (Store.store_code == Customer.my_store_code) & (Store.company_code == Customer.company_code)). \
            filter(RegisterSale.id == id, RegisterSale.delete_flag == 0).first()
        if not register_sale:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'出品ID{id}が存在しません。')
        return register_sale

    # update register_sale_status for update offer status api
    def update_register_sale_status(self, db, car_id, status, update_id) -> RegisterSale:
        update_obj = db.query(self.model) \
            .filter(RegisterSale.car_id == car_id,
                    RegisterSale.delete_flag == Const.DEL_FLG_NORMAL, ).first()

        if not update_obj:
            return None
        update_obj.register_sale_status = status
        update_obj.update_at = datetime.utcnow()
        update_obj.update_id = update_id
        db.add(update_obj)
        db.flush()
        return update_obj

    # get buy_now_total_price
    def get_buy_now_total_price(self, db, max_date, car_id_sale):
        buy_now_total_price = db.query(self.model.buy_now_total_price).filter(RegisterSale.period_to == max_date,
                                                                              RegisterSale.car_id == car_id_sale,
                                                                              RegisterSale.delete_flag == 0).first()
        buy_now_total_price = jsonable_encoder(buy_now_total_price)
        return buy_now_total_price

    def get_register_sale_by_car_id(
        self, db: Session, *, car_id: int, limit: int, offset: int
    ) -> Any:
        result = db.query(self.model).filter(
                    RegisterSale.car_id == car_id,
                    RegisterSale.delete_flag == Const.DEL_FLG_NORMAL,
                )
        # sort
        result = result.order_by(RegisterSale.period_from.desc(), RegisterSale.id.asc())
        # get count
        total = result.count()
        # set limit offset
        result = result.limit(limit)
        result = result.offset(offset)
        # excute query
        result = result.all()
        return total, result


    def delete_by_update_deleteflag_bycarcode(self, db: Session, *, car_id: int) -> RegisterSale:
        db_obj = (
            db.query(self.model)
            .filter(
                RegisterSale.car_id == car_id,
                RegisterSale.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )
        if not db_obj:
            return None
        db_obj.delete_flag = Const.DEL_FLG_DELETE
        db_obj.delete_at = datetime.utcnow()
        db.add(db_obj)
        db.flush()
        return db_obj

    def update_register_sale_by_car_id(
            self, db: Session, car_id: int, obj_in: RegisterSaleUpdate, update_id: int
    ) -> Any:
        db_obj = db.query(self.model).filter(
                            RegisterSale.car_id == car_id,
                            RegisterSale.delete_flag == Const.DEL_FLG_NORMAL,
                        ).first()

        if not db_obj:
            return None
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_at = datetime.utcnow()
        db_obj.update_id = update_id
        db.add(db_obj)
        db.flush()
        return db_obj

    def update_assess_id_by_register_sale_id(self, db: Session, item_in: RegisterSaleUpdateAssess) -> RegisterSale:
        try:

            db_obj = db.query(self.model).filter(
                self.model.id == item_in.register_sale_id,
                self.model.delete_flag == Const.DEL_FLG_NORMAL
            ).first()

            if db_obj is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Register sale id {item_in.register_sale_id} not found")

            # Update assess
            assess = AssessBase(car_id=db_obj.car_id,
                                company_code=db_obj.company_code,
                                )
            if item_in.assess_status:
                assess.assess_status = item_in.assess_status
            if db_obj.assess_id:
                assess.id = db_obj.assess_id
            assess_obj = crud.assess.create_or_update_assess(db=db, obj_in=assess, user_id=item_in.user_id)
            db_obj.assess_id = assess_obj.id if item_in.assess_status else None
            db.add(db_obj)
            db.flush()
            return db_obj
        except Exception as err:
            logger.error("Error occurred", exc_info=True)
            raise err


register_sale = CRUDRegisterSale(RegisterSale)
