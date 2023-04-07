from typing import Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.options import Options
from app.schemas.options import OptionsCreate, OptionsUpdate
from app.constants import Const


class CRUDOptions(CRUDBase[Options, OptionsCreate, OptionsUpdate]):
    # Get all options
    def get_options(self, db: Session) -> Any:
        result = (
            db.query(self.model)
                .filter(self.model.delete_flag == Const.DEL_FLG_NORMAL)
                .all()
        )
        return result


options = CRUDOptions(Options)
