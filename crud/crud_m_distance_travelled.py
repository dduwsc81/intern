from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_distance_travelled import MDistanceTravelled

from app.schemas.m_distance_travelled import MDistanceTravelledCreate, MDistanceTravelledUpdate, MDistanceTravelledBase
from datetime import datetime, timedelta
from app import crud


class CRUDMDistanceTravelled(CRUDBase[MDistanceTravelled, MDistanceTravelledCreate, MDistanceTravelledUpdate]):
    def get_m_distance_travelled(
        self, db: Session
    ) -> MDistanceTravelledBase:
        result = db.query(self.model).filter(MDistanceTravelled.delete_flag == 0).all()
        return result


m_distance_travelled = CRUDMDistanceTravelled(MDistanceTravelled)
