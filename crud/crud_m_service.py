from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_service import MService
from app.schemas.m_service import MServiceCreate, MServiceUpdate
from app.constants import Const


class CRUDMService(CRUDBase[MService, MServiceCreate, MServiceUpdate]):

    def get_service_by_code(self, db: Session, *, service_code) -> Any:
        result = db.query(self.model)\
                   .filter(MService.service_cd == service_code,
                           MService.delete_flag == Const.DEL_FLG_NORMAL).first()
        return result


m_service = CRUDMService(MService)
