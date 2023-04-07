from typing import Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_price import MPrice
from app.schemas.m_price import MPriceCreate, MPriceUpdate, MPriceBase
from datetime import datetime, timedelta
from app import crud


class CRUDPrice(CRUDBase[MPrice, MPriceCreate, MPriceUpdate]):
    # Get all m_price
    def get_price(
            self, db: Session
    ) -> MPriceBase:
        result = db.query(self.model).filter(MPrice.delete_flag == 0).all()
        return result


m_price = CRUDPrice(MPrice)
