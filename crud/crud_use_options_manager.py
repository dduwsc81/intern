from datetime import datetime
from typing import Any, Dict, Union, Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.constants import Const
from app.crud.base import CRUDBase
from app.models.use_options_manager import UseOptionsManager
from app.schemas.use_options_manager import (
    UseOptionsManagerCreate,
    UseOptionsManagerUpdate,
)
ESTIMATE_TYPE = {
    "SELLER": 1,
    "BUYER": 2
}
ASSESS_OPTION_BUYER = 4

class CRUDUseOptionsManager(CRUDBase[UseOptionsManager, UseOptionsManagerCreate, UseOptionsManagerUpdate]):
    def update_assessment_option_by_estimate_id(
        self,
        db: Session,
        user_id: int,
        assess_request_flg: int,
        estimate_id: int,
        car_id: int,
        estimate_type: Optional[int] = ESTIMATE_TYPE["SELLER"]
    ) -> Any:
        option_id = Const.ASSESSMENT_OPTION
        if estimate_type == ESTIMATE_TYPE["BUYER"]:
            option_id = ASSESS_OPTION_BUYER
        db_obj = (
            db.query(self.model)
            .filter(
                UseOptionsManager.estimate_id == estimate_id,
                UseOptionsManager.option_id == option_id,
            )
            .first()
        )
        option = crud.options.get_option_by_id(db, option_id=option_id)
        if not db_obj:
            if assess_request_flg == Const.ASSESSMENT_ENABLE:
                # insert use options manager
                db_obj = UseOptionsManager(
                    car_id=car_id,
                    estimate_id=estimate_id,
                    option_id=option_id,
                    option_name=option.option_name,
                    insert_id=user_id,
                    insert_at=datetime.utcnow(),
                    update_id=user_id,
                    update_at=datetime.utcnow(),
                    delete_flag=Const.DEL_FLG_NORMAL,
                )
                db.add(db_obj)
                db.flush()
            else:
                return None

        db_obj.update_at = datetime.utcnow()
        db_obj.update_id = user_id

        if assess_request_flg == Const.ASSESSMENT_ENABLE:
            db_obj.delete_flag = Const.DEL_FLG_NORMAL
            db_obj.delete_id = None
            db_obj.delete_at = None
        else:
            db_obj.delete_flag = Const.DEL_FLG_DELETE
            db_obj.delete_id = user_id
            db_obj.delete_at = datetime.utcnow()

        db.add(db_obj)
        db.flush()
        return db_obj

    def delete_use_option_manager_by_estimate_id(
        self,
        db: Session,
        user_id: int,
        estimate_id: int,
    ) -> Any:

        db_obj = (
            db.query(self.model)
            .filter(
                UseOptionsManager.estimate_id == estimate_id,
                UseOptionsManager.delete_flag == Const.DEL_FLG_NORMAL,
            ).update({
                        UseOptionsManager.delete_at: datetime.utcnow(),
                        UseOptionsManager.delete_id: user_id,
                        UseOptionsManager.delete_flag: Const.DEL_FLG_DELETE,
                     }
                     , synchronize_session=False)
            )

        db.flush()
        return True


use_options_manager = CRUDUseOptionsManager(UseOptionsManager)
