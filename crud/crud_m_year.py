from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_year import MYear
from app.schemas.m_year import MYearCreate, MYearUpdate, MYearBase
from datetime import datetime, timedelta
from app import crud


class CRUDMYear(CRUDBase[MYear, MYearCreate, MYearUpdate]):

    # Get all m_year
    def get_m_year(
            self, db: Session
    ) -> MYearBase:
        result = db.query(self.model).filter(MYear.delete_flag == 0).all()
        return result


m_year = CRUDMYear(MYear)
