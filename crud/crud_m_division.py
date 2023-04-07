from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_division import MDivision
from app.schemas.m_division import MDivisionBase, MDivisionCreate, MDivisionUpdate
from datetime import datetime, timedelta
from app import crud


class CRUDMDivision(CRUDBase[MDivisionBase, MDivisionCreate, MDivisionUpdate]):
    PAID_TYPE = 'paid_type'
    DIV_PAID_TYPE = 11

    # Get status description
    def get_status_description(
            self, db: Session,
            div_name: str,
            param: int
    ) -> MDivisionBase:
        result = db.query(self.model.desc).filter(MDivision.div_name == div_name, MDivision.param == param,
                                                  MDivision.delete_flag == 0).first()
        return result if result else ("",)

    def get_paid_type(self, db: Session) -> Any:
        result = db.query(self.model.param.label("value"),
                          self.model.desc.label("text")).filter(MDivision.div == self.DIV_PAID_TYPE,
                                          MDivision.div_name == self.PAID_TYPE, MDivision.delete_flag == 0).all()
        return result

    # Get m_division by div
    def get_m_division_by_div(self, db: Session, div: int) -> Any:
        try:
            result = db.query(self.model).filter(MDivision.div == div).all()
            return result
        except Exception as err:
            raise err


m_division = CRUDMDivision(MDivision)
