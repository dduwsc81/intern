from datetime import datetime
from typing import Any
import logging

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from app.constants import Const
from app.crud.base import CRUDBase
from app.models.assess import Assess
from app.models.register_sale import RegisterSale
from app.schemas.assess import (
    AssessCreate,
    AssessUpdate,
    AssessBase,
    AssessUpdateByRegisterSale,
)

logger = logging.getLogger(__name__)


class CRUDAsess(CRUDBase[Assess, AssessCreate, AssessUpdate]):

    def delete_assess_by_id(
        self,
        db: Session,
        user_id: int,
        id: int,
    ) -> Any:

        db_obj = (
            db.query(self.model)
            .filter(
                Assess.id == id,
                Assess.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )

        if not db_obj:
            return None

        db_obj.update_at = datetime.utcnow()
        db_obj.update_id = user_id
        db_obj.delete_at = datetime.utcnow()
        db_obj.delete_id = user_id
        db_obj.delete_flag = Const.DEL_FLG_DELETE

        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def upsert_by_registersale(self, db: Session, item_in:AssessUpdateByRegisterSale, user_id: int) -> Assess:
        try:
            db_obj = db.query(RegisterSale).filter(
                RegisterSale.id == item_in.register_sale_id,
                RegisterSale.delete_flag == Const.DEL_FLG_NORMAL
            ).first()

            if db_obj is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Register sale id {item_in.register_sale_id} not found")
            assess_obj = self.upsert(db=db, item_in=item_in, user_id=user_id)
            db_obj.assess_id = assess_obj.id if item_in.assess_status else None
            db.add(db_obj)
            db.flush()
            return assess_obj
        except Exception as err:
            logger.error("Error occurred", exc_info=True)
            raise err

    def upsert(self, db: Session, item_in, user_id: int) -> Assess:
        try:
            # get assess if exist
            db_obj = (
                db.query(self.model)
                    .filter(self.model.car_id == item_in.car_id)
                    .first()
            )

            # convert obj_in to dict
            if isinstance(item_in, dict):
                upsert_data = item_in
            else:
                upsert_data = item_in.dict(exclude_unset=True, exclude={'register_sale_id', 'user_id'})

            # update when exist
            if db_obj:
                # update attributes have in obj_in
                for field in upsert_data.keys():
                    setattr(db_obj, field, upsert_data[field])
                db_obj.update_at = datetime.utcnow()
                db_obj.update_id = user_id
            else:
                # insert new record assess
                db_obj = Assess(
                    **upsert_data,
                    insert_id=user_id,
                    insert_at=datetime.utcnow(),
                    update_id=user_id,
                    update_at=datetime.utcnow(),
                )
                db_obj.delete_flag = Const.DEL_FLG_NORMAL
            db.add(db_obj)
            db.flush()
            return db_obj
        except Exception as err:
            logger.error("Error occurred", exc_info=True)
            raise err

    def create_or_update_assess(self,
                                db: Session,
                                user_id: int,
                                obj_in: AssessBase) -> Assess:
        try:
            # get assess if exist
            db_obj = (
                db.query(self.model)
                    .filter(self.model.car_id == obj_in.car_id)
                    .first()
            )

            # assign value of delete_flag
            del_flag = Const.DEL_FLG_NORMAL if obj_in.assess_status else Const.DEL_FLG_DELETE

            # update when exist
            if db_obj:
                # convert obj_in to dict
                if isinstance(obj_in, dict):
                    update_data = obj_in
                else:
                    update_data = obj_in.dict(exclude_unset=True)

                # update attributes have in obj_in
                for field in update_data.keys():
                    setattr(db_obj, field, update_data[field])
                db_obj.update_at = datetime.utcnow()
                db_obj.update_id = user_id
                db_obj.delete_flag = del_flag
            else:
                # insert new record assess
                obj_in_data = obj_in.dict()
                db_obj = Assess(
                    **obj_in_data,
                    insert_id=user_id,
                    insert_at=datetime.utcnow(),
                    update_id=user_id,
                    update_at=datetime.utcnow(),
                    delete_flag=del_flag
                )
            # update delete_flag
            if del_flag == Const.DEL_FLG_DELETE:
                db_obj.delete_id = user_id
                db_obj.delete_at = datetime.utcnow()
            else:
                db_obj.delete_id = None
                db_obj.delete_at = None
            db.add(db_obj)
            db.flush()
            return db_obj
        except Exception as err:
            logger.error("Error occurred", exc_info=True)
            raise err


assess = CRUDAsess(Assess)
