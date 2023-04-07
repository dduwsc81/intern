from typing import List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models.car_training
from app.crud.base import CRUDBase
from app.models.car_training import CarTraining
from app.schemas.car_training import CarTrainingCreate, CarTrainingUpdate


class CRUDCarTraining(CRUDBase[CarTraining, CarTrainingCreate, CarTrainingUpdate]):
    def create_car_training(
            self,
            db: Session,
            item_in: CarTrainingCreate
    ) -> Any:
        db_in = jsonable_encoder(item_in)
        obj_in_db = CarTraining(**db_in)
        db.add(obj_in_db)
        db.commit()
        db.refresh(obj_in_db)
        return obj_in_db

    def get_all_car_training(
            self,
            db: Session
    ) -> List[CarTraining]:
        item_in_db = db.query(self.model).filter(CarTraining.delete_flag == 0).all()
        return item_in_db

    def get_car_training_by_id(
            self,
            id: int,
            db: Session
    ) -> Any:
        item_in_id = db.query(self.model).filter(CarTraining.id == id).first()
        return item_in_id

    def get_car_by_page(
            self,
            page: int,
            row_per_page: int,
            db: Session
    ) -> Any:
        start = (page - 1) * row_per_page
        item_in_db = db.query(self.model).offset(start).limit(start + row_per_page).all()
        return item_in_db

    def update_car_training(
            self,
            id: int,
            item_in: CarTrainingUpdate,
            db: Session
    ) -> Any:
        item_in_db = db.query(self.model).filter(CarTraining.id == id).first()
        item_data = jsonable_encoder(item_in_db)
        if isinstance(item_in, dict):
            update_data = item_in
        else:
            update_data = item_in.dict(exclude_unset=True)

        for field in item_data:
            if field in update_data:
                setattr(item_in_db, field, update_data[field])
        db.add(item_in_db)
        db.commit()
        db.refresh(item_in_db)
        return item_in_db

    def delete_car_training(
            self,
            id: int,
            db: Session
    ) -> Any:
        item_in_db = db.query(self.model).filter(CarTraining.id == id).first()
        setattr(item_in_db, "delete_flag", 1)
        db.add(item_in_db)
        db.commit()
        return "Deleted"


cartraining = CRUDCarTraining(CarTraining)
