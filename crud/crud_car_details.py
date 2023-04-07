from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.car_details import CarDetails
from app.schemas.car_details import CarDetailsCreate, CarDetailsUpdate
from app.models.register_sale import RegisterSale
from app.models.car import Car
from datetime import datetime, timedelta


class CRUDCarDetails(CRUDBase[CarDetails, CarDetailsCreate, CarDetailsUpdate]):
    def create_car_details(
            self, db: Session, *, obj_in: CarDetailsCreate
    ) -> CarDetails:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, insert_id=1, insert_at=datetime.utcnow() + timedelta(hours=7), update_id=1,
                            update_at=datetime.utcnow() + timedelta(hours=7), delete_flag=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_by_update_deleteflag(
            self,
            db: Session,
            *,
            id: int
    ) -> CarDetails:
        db_obj = db.query(self.model).filter(CarDetails.car_code == id, CarDetails.delete_flag == 0).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Car details id {id} not found')
        db_obj.delete_flag = 1
        db_obj.delete_at = datetime.utcnow() + timedelta(hours=7)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_cardetails_by_id(
            self,
            db: Session,
            *,
            obj_in: Union[CarDetailsUpdate, Dict[str, Any]],
            id: int
    ) -> CarDetails:
        db_obj = db.query(self.model).filter(CarDetails.car_code == id, CarDetails.delete_flag == 0).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Car details id {id} not found')
        db_obj.update_at = datetime.utcnow() + timedelta(hours=7)
        db_obj.update_id += 1
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
        return db_obj

    def get_cardetails(
            self, db: Session, *, skip: int = 0, limit: int = 10
    ) -> List[CarDetails]:
        return (
            db.query(self.model)
                .filter(CarDetails.delete_flag == 0)
                .offset(skip)
                .limit(limit)
                .all()
        )

    def get_cardetails_by_id(
            self, db: Session, *, id: int = 0
    ) -> Any:
        cardetail = db.query(self.model, Car.number_of_offer, RegisterSale.period_from, RegisterSale.period_to,
                             RegisterSale.hope_sale_base_price, RegisterSale.buy_now_base_price,
                             RegisterSale.hope_sale_total_price, RegisterSale.buy_now_total_price,
                             RegisterSale.price_type) \
            .outerjoin(RegisterSale, (RegisterSale.car_code == CarDetails.car_code)) \
            .outerjoin(Car, (Car.car_code == CarDetails.car_code)) \
            .filter(CarDetails.car_code == id, CarDetails.delete_flag == 0) \
            .first()
        return cardetail

    def delete_cardetails_by_id(
            self, db: Session, *, id: int
    ) -> CarDetails:
        obj = db.query(self.model).filter(CarDetails.car_code == id, CarDetails.delete_flag == 0).first()
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Car detail id {id} not found')
        db.delete(obj)
        db.commit()
        return obj


car_details = CRUDCarDetails(CarDetails)
