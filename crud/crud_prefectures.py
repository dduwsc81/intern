from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_prefectures import MPrefectures
from app.schemas.m_prefectures import MPrefecturesCreate, MPrefecturesUpdate
from datetime import datetime, timedelta
from sqlalchemy import or_


class CRUDMPrefectures(CRUDBase[MPrefectures, MPrefecturesCreate, MPrefecturesUpdate]):
    def get_prefectures(
            self, db: Session
    ) -> Any:
        prefectures = db.query(self.model).all()
        total = len(prefectures)
        return prefectures, total



m_prefecture = CRUDMPrefectures(MPrefectures)
