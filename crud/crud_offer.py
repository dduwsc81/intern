from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.car import Car
from app.models.car_photo import CarPhoto
from app.models.car_details import CarDetails
from app.models.register_sale import RegisterSale
from app.models.offer import Offer
from app.models.m_company import MCompany
from app.models.purchase import Purchase
from app.models.customer import Customer
from app.models.store import Store
from app.models.car_market import CarMarket
from app.models.m_prefectures import MPrefectures
from app.models.chat_group import ChatGroup
from app.schemas.offer import OfferCreate, OfferUpdate, OfferUpdateStatus
from datetime import datetime, timedelta
from sqlalchemy import or_
from app import crud
from ..api.api_v1.endpoints.format_status import *


class CRUDOffer(CRUDBase[Offer, OfferCreate, OfferUpdate]):
    OFFER_STATUS = (1, 2, 3, 4, 5)
    IMAGE_DIV = 1
    CHAT_GROUP_DIV = 1

    def update_offer_by_id(
            self,
            db: Session,
            *,
            obj_in: OfferUpdateStatus,
            id: int
    ) -> Offer:
        db_obj = db.query(self.model).filter(Offer.id == id, Offer.delete_flag == 0).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'オファーID{id}が存在しません。')
        db_obj.update_at = datetime.utcnow()

        # TODO:hardcode admin_id
        db_obj.update_id = 888888

        if obj_in.offer_status == 5:
            setattr(db_obj, 'offer_status', 5)
        elif obj_in.offer_status == 3:

            # update offer info
            setattr(db_obj, 'offer_status', 3)
            setattr(db_obj, 'offer_in_store_id', obj_in.offer_in_store_id)

            # update status car_market
            self.update_status_car_market(db, db_obj.car_id, 2)

            # create purchase record
            self.create_purchase(db, db_obj.car_id, db_obj.hope_purchase_price,
                                 db_obj.offer_out_store_id, obj_in.purchase_comment, db_obj.id)

            # get car chassis number in offer
            car = db.query(Car.chassis_number).filter(Car.id == db_obj.car_id, Car.delete_flag == 0).first()

            # get list car code same chassis_number
            list_car_same_chassis_number = db.query(Car.id). \
                filter(Car.chassis_number == car.chassis_number, Car.delete_flag == 0).all()

            # reject other offer
            update_data = []
            for car_id in list_car_same_chassis_number:
                other_offers = db.query(self.model).filter(Offer.car_id == car_id[0], Offer.delete_flag == 0).all()
                for offer in other_offers:
                    if offer.offer_status != 3 and offer.offer_status != 5:
                        setattr(offer, 'offer_status', 5)
                        setattr(offer, 'update_id', 888888)
                        setattr(offer, 'update_at', datetime.utcnow())
                        update_data.append(offer)
            db.bulk_save_objects(update_data)
            db.commit()
        elif obj_in.offer_status == 4:

            # update register sale status
            crud.register_sale.update_register_sale_status(db,
                                                           car_id=db_obj.car_id,
                                                           update_id=db_obj.update_id,
                                                           status=obj_in.offer_status,)
            setattr(db_obj, 'offer_status', obj_in.offer_status)

            # update purchase
            self.update_purchase(db, db_obj.car_id, obj_in.purchase_comment)

            # update status car market
            self.update_status_car_market(db, db_obj.car_id, 3)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # get detail offer
        offer, store_id, company_name_offer, list_car_same_chassis_number = self.get_offer_by_id(db, id=id)
        return offer, store_id, company_name_offer, list_car_same_chassis_number

    def update_status_car_market(self, db, car_id, car_status):
        car_market = db.query(CarMarket).filter(CarMarket.car_id == car_id, CarMarket.delete_flag == 0).first()
        if not car_market:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'車両マーケットが存在しません。')
        setattr(car_market, 'car_status', car_status)

        # TODO:hardcode admin_id
        setattr(car_market, 'update_id', 888888)
        setattr(car_market, 'update_at', datetime.utcnow())
        db.add(car_market)
        db.commit()
        db.refresh(car_market)
        return car_market

    def create_purchase(self, db, car_id, purchase_price,
                        purchase_store_id, purchase_comment, offer_id):
        obj_in_data = {"car_id": car_id, "status": 1, "purchase_price": purchase_price,
                       "purchase_store_id": purchase_store_id,
                       "comment": purchase_comment, "offer_id": offer_id}
        db_obj = Purchase(**obj_in_data, insert_id=888888, insert_at=datetime.utcnow(),
                          update_id=888888,
                          update_at=datetime.utcnow(), delete_flag=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_purchase(self, db, car_id, comment):
        purchase = db.query(Purchase).filter(Purchase.car_id == car_id, Purchase.delete_flag == 0).first()
        if not purchase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'購入情報が存在しません。')
        setattr(purchase, 'status', 2)
        setattr(purchase, 'comment', comment)
        setattr(purchase, 'update_id', 888888)
        setattr(purchase, 'update_at', datetime.utcnow())
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        return purchase

    def get_offers(
            self, db: Session, *, skip: int = 0, limit: int = 10
    ) -> Any:
        offers = db.query(
            self.model.id.label("offer_id"),
            self.model.offer_out_store_id,
            self.model.offer_in_store_id,
            self.model.offer_status,
            MCompany.company_name,
            self.model.insert_at.label("time_offer"),
            Car.maker,
            Car.car_type,
            Car.id.label("car_id"),
            CarDetails.sales_period_start,
            CarDetails.aggregation_wholesale_price_market,
            MPrefectures.name.label("area"),
            RegisterSale.buy_now_total_price,
            CarPhoto.url.label('thumbnail_url'),
            ChatGroup.message_total_cnt,
            ChatGroup.last_message_user_name,
            ChatGroup.last_message_datetime,
            ChatGroup.message_unread_cnt,
            ChatGroup.last_message_user_id
        ). \
            join(Car, (Offer.car_id == Car.id)). \
            outerjoin(CarPhoto, (Car.id == CarPhoto.car_id) & (CarPhoto.image_div == self.IMAGE_DIV)). \
            outerjoin(CarDetails, (Offer.car_id == CarDetails.car_id)). \
            outerjoin(RegisterSale, (Offer.register_sale_id == RegisterSale.id)). \
            outerjoin(MCompany, (MCompany.company_code == Car.company_code)). \
            outerjoin(CarMarket, (Offer.car_id == CarMarket.car_id)). \
            outerjoin(MPrefectures, (CarMarket.prefectures_cd == MPrefectures.prefectures_code)). \
            outerjoin(ChatGroup, (ChatGroup.offer_id == Offer.id) & (ChatGroup.store_id == Offer.offer_out_store_id) & (
                ChatGroup.div == self.CHAT_GROUP_DIV)). \
            filter(Offer.delete_flag == 0, Offer.offer_status.in_(self.OFFER_STATUS)).order_by(Offer.id.asc())
        total = offers.count()
        offers = offers.offset(skip).limit(limit).all()
        return offers, total

    # get store name by store id
    def get_store_name(self, db, store_id):
        store = db.query(Store.store_name, Store.id.label('store_id'), MCompany.company_name). \
            outerjoin(MCompany, (Store.company_code == MCompany.company_code)). \
            filter(Store.id == store_id,
                   Store.delete_flag == 0). \
            first()
        return store if store else ("", "", "")

    def search_offers(
            self, db: Session, *,
            skip: int = 0,
            limit: int = 10,
            maker,
            car_type,
            grade,
            sales_period_start_from,
            sales_period_start_to,
            registration_end_date_from,
            registration_end_date_to,
            car_mileage_from,
            car_mileage_to,
            offer_status,
            area,
            aggregation_wholesale_price_market_from,
            aggregation_wholesale_price_market_to,
            buy_now_total_price_from,
            buy_now_total_price_to,
            insert_at_from,
            insert_at_to,
            chassis_number,
            car_inspection_type,
            registration_first_date,
    ) -> Any:

        offers = db.query(
            self.model.id.label("offer_id"),
            self.model.offer_out_store_id,
            self.model.offer_in_store_id,
            self.model.offer_status,
            self.model.insert_at.label("time_offer"),
            MCompany.company_name,
            Car.maker,
            Car.car_type,
            Car.id.label("car_id"),
            CarDetails.sales_period_start,
            CarDetails.aggregation_wholesale_price_market,
            MPrefectures.name.label("area"),
            RegisterSale.buy_now_total_price,
            CarPhoto.url.label('thumbnail_url'),
            ChatGroup.message_total_cnt,
            ChatGroup.last_message_user_name,
            ChatGroup.last_message_datetime,
            ChatGroup.message_unread_cnt,
            ChatGroup.last_message_user_id
        ). \
            join(Car, (Offer.car_id == Car.id)). \
            outerjoin(CarPhoto, (Car.id == CarPhoto.car_id) & (CarPhoto.image_div == self.IMAGE_DIV)). \
            outerjoin(MCompany, (MCompany.company_code == Car.company_code)). \
            outerjoin(CarDetails, (Offer.car_id == CarDetails.car_id)). \
            outerjoin(RegisterSale, (Offer.register_sale_id == RegisterSale.id)). \
            outerjoin(CarMarket, (Offer.car_id == CarMarket.car_id)). \
            outerjoin(MPrefectures, (CarMarket.prefectures_cd == MPrefectures.prefectures_code)). \
            outerjoin(ChatGroup, (ChatGroup.offer_id == Offer.id) & (ChatGroup.store_id == Offer.offer_out_store_id) & (
                ChatGroup.div == self.CHAT_GROUP_DIV)). \
            filter(Offer.delete_flag == 0, Offer.offer_status.in_(self.OFFER_STATUS)).order_by(Offer.id.asc())

        # filter
        offers = offers. \
            filter(or_(Car.maker.like("%{}%".format(maker)), maker == "")). \
            filter(or_(Car.car_type.like("%{}%".format(car_type)),
                       Car.car_type.like("%{}%".format(format_ascii_to_unicode(car_type))), car_type == "")). \
            filter(
            or_(Car.grade.like("%{}%".format(grade)), Car.grade.like("%{}%".format(format_ascii_to_unicode(grade))),
                grade == "")). \
            filter(or_(Offer.offer_status.in_(offer_status), offer_status == [])). \
            filter(or_(MPrefectures.name.in_(area), area == []))
        if sales_period_start_from != '':
            offers = offers.filter(CarDetails.sales_period_start >= sales_period_start_from)
        if sales_period_start_to != '':
            offers = offers.filter(CarDetails.sales_period_start <= (sales_period_start_to + "12"))
        if registration_end_date_from != '':
            offers = offers.filter(Car.registration_end_date >= registration_end_date_from)
        if registration_end_date_to != '':
            offers = offers.filter(Car.registration_end_date <= registration_end_date_to)
        if aggregation_wholesale_price_market_from != 0:
            offers = offers.filter(
                CarDetails.aggregation_wholesale_price_market >= aggregation_wholesale_price_market_from)
        if aggregation_wholesale_price_market_to != 0:
            if aggregation_wholesale_price_market_from == 0:
                offers = offers.filter(
                    or_(CarDetails.aggregation_wholesale_price_market <= aggregation_wholesale_price_market_to,
                        CarDetails.aggregation_wholesale_price_market.is_(None)))
            else:
                offers = offers.filter(
                    CarDetails.aggregation_wholesale_price_market <= aggregation_wholesale_price_market_to)
        if buy_now_total_price_from != 0:
            offers = offers.filter(RegisterSale.buy_now_total_price >= buy_now_total_price_from)
        if buy_now_total_price_to != 0:
            if buy_now_total_price_from == 0:
                offers = offers.filter(
                    or_(RegisterSale.buy_now_total_price <= buy_now_total_price_to,
                        RegisterSale.buy_now_total_price.is_(None)))
            else:
                offers = offers.filter(RegisterSale.buy_now_total_price <= buy_now_total_price_to)
        if car_mileage_from != 0:
            offers = offers.filter(Car.car_mileage >= car_mileage_from)
        if car_mileage_to != 0:
            offers = offers.filter(Car.car_mileage <= car_mileage_to)
        if insert_at_from != '':
            offers = offers.filter(self.model.insert_at >= jst_to_utc(insert_at_from + " 00:00:00"))
        if insert_at_to != '':
            offers = offers.filter(self.model.insert_at <= jst_to_utc(insert_at_to + " 23:59:59"))
        if chassis_number != '':
            offers = offers.filter(or_(Car.chassis_number.like("%{}%".format(chassis_number)),
                                       Car.chassis_number.like(
                                           "%{}%".format(format_ascii_to_unicode(chassis_number)))))
        if car_inspection_type != '':
            offers = offers.filter(CarDetails.car_inspection_type.like("%{}%".format(car_inspection_type)))
        if registration_first_date != '':
            offers = offers.filter(Car.registration_first_date.like("{}%".format(registration_first_date)))
        total = offers.count()
        offers = offers.offset(skip).limit(limit).all()
        return offers, total

    def get_offer_by_id(
            self, db: Session, *, id: int
    ) -> Offer:
        offer = db.query(
            self.model.id.label("offer_id"),
            self.model.hope_purchase_price,
            self.model.offer_status,
            self.model.offer_out_store_id,
            self.model.offer_in_store_id,
            Car.maker,
            Car.car_type,
            CarDetails.sales_period_start,
            Car.grade,
            Car.land_transport_office,
            Car.car_registration_number_type,
            Car.car_registration_number_kana,
            Car.car_registration_number,
            Car.registration_first_date,
            Car.registration_start_date,
            Car.registration_end_date,
            Car.car_mileage,
            Car.car_decision_maker,
            Car.chassis_number,
            Car.id.label("car_id"),
            CarDetails.car_inspection_type,
            CarDetails.aggregation_wholesale_price_market,
            RegisterSale.price_type,
            RegisterSale.hope_sale_base_price,
            RegisterSale.buy_now_base_price,
            RegisterSale.hope_sale_total_price,
            RegisterSale.buy_now_total_price,
            RegisterSale.hope_sale_base_price_tax,
            RegisterSale.buy_now_base_price_tax,
            RegisterSale.hope_sale_total_price_tax,
            RegisterSale.buy_now_total_price_tax,
            Purchase.purchase_price
        ). \
            outerjoin(Car, (Offer.car_id == Car.id)). \
            outerjoin(CarDetails, (Offer.car_id == CarDetails.car_id)). \
            outerjoin(RegisterSale, (Offer.car_id == RegisterSale.car_id)). \
            outerjoin(Purchase, (Offer.id == Purchase.offer_id)). \
            filter(Offer.id == id, Offer.delete_flag == 0, Offer.offer_status.in_(self.OFFER_STATUS)).first()
        if not offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'オファーID{id}が存在しません。')

        # get_company_name_offer
        company_name_offer = db.query(MCompany.company_name, Store.store_name). \
            outerjoin(MCompany, (Store.company_code == MCompany.company_code)). \
            filter(Store.id == offer.offer_out_store_id,
                   Store.delete_flag == 0). \
            first()

        # get store id of offer by offer_out_store_id
        store_id = self.get_store_name(db, offer.offer_out_store_id)
        if not store_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'店舗が存在しません。')

        # get_list_cars_same_chassis_number
        list_car_same_chassis_number = db.query(Car.id, Car.chassis_number, Store.id.label("store_id"),
                                                Store.store_name,
                                                MCompany.company_name). \
            outerjoin(MCompany, (Car.company_code == MCompany.company_code)). \
            outerjoin(Customer,
                      (Car.car_decision_maker == Customer.customer_code) & (Car.company_code == Customer.company_code)). \
            outerjoin(Store,
                      (Store.store_code == Customer.my_store_code) & (Store.company_code == Customer.company_code)). \
            filter(Car.chassis_number == offer.chassis_number, Store.store_code != None,
                   Car.delete_flag == 0).all()
        return offer, store_id, company_name_offer, list_car_same_chassis_number

    def check_offered(
            self,
            db: Session,
            car_id: int
    ):
        list_offers, total = self.get_offers(db=db)
        list_car_id = []
        for offer in list_offers:
            list_car_id.append(offer.car_id)
        if car_id in list_car_id:
            return True
        return False

offer = CRUDOffer(Offer)
