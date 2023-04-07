from datetime import datetime
from typing import Any, Dict, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.constants import Const
from app.crud.base import CRUDBase
from app.models.car_market import CarMarket
from app.schemas.car_market import CarMarketCreate, CarMarketUpdate


class CRUDCarMarket(CRUDBase[CarMarket, CarMarketCreate, CarMarketUpdate]):

    # update carmarket status by carid and delete register sale of this carid
    def update_car_status_by_car_id(
        self, db: Session, *, car_status, car_id, update_id
    ) -> Any:
        db_obj = db.query(self.model)\
                   .filter(CarMarket.car_id == car_id,
                           CarMarket.delete_flag == Const.DEL_FLG_NORMAL,).first()
        if not db_obj:
            return None
        db_obj.update_at = datetime.utcnow()
        db_obj.update_id = update_id
        db_obj.car_status = car_status
        db.add(db_obj)
        db.flush()
        return db_obj


car_market = CRUDCarMarket(CarMarket)
