from datetime import datetime
from typing import Any, Dict, Union

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.constants import Const
from app.crud.base import CRUDBase
from app.models.car_transaction_history import CarTransactionHistory
from app.models.m_division import MDivision
from app.schemas.car_transaction_history import (
    CarTransactionHistoryCreate,
    CarTransactionHistoryUpdate,
)

from sqlalchemy import and_

TRANSACTION_TYPE_DIV = 12

class CRUDCarTransactionHistory(CRUDBase[CarTransactionHistory, CarTransactionHistoryCreate, CarTransactionHistoryUpdate]):

    def get_car_transaction_by_car_id(self, db: Session, id: int, skip: int, limit: int) -> Any:
        result = (db.query(CarTransactionHistory.id,
                           CarTransactionHistory.car_id,
                           CarTransactionHistory.car_code,
                           CarTransactionHistory.company_code,
                           CarTransactionHistory.transaction_date,
                           CarTransactionHistory.transaction_type,
                           CarTransactionHistory.contents,
                           MDivision.desc.label("transaction_type_name"))
                  .outerjoin(MDivision, and_(CarTransactionHistory.transaction_type == MDivision.param,
                                             MDivision.div == TRANSACTION_TYPE_DIV,
                                             MDivision.delete_flag == Const.DEL_FLG_NORMAL))
                  .filter(and_(CarTransactionHistory.delete_flag == Const.DEL_FLG_NORMAL,
                               CarTransactionHistory.car_id == id))
                  .order_by(CarTransactionHistory.transaction_date.desc()))

        total = result.count()
        result = result.offset(skip).limit(limit).all()

        return result, total

car_transaction_history = CRUDCarTransactionHistory(CarTransactionHistory)
