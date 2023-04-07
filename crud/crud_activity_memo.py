import logging
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.constants import Const
from app.models.activity_memo import ActivityMemo
from app.schemas.activity_memo import ActivityMemoCreate, ActivityMemoUpdate
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class CRUDActivityMemo(CRUDBase[ActivityMemo, ActivityMemoCreate, ActivityMemoUpdate]):

    def create_activity_memo(
            self, db: Session, *, obj_in: ActivityMemoCreate, user_id
    ) -> ActivityMemo:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = ActivityMemo(
                **obj_in_data,
                memo_create_at=datetime.utcnow() + timedelta(hours=9),
                insert_id=user_id,
                insert_at=datetime.utcnow(),
                update_id=user_id,
                update_at=datetime.utcnow(),
                delete_flag=Const.DEL_FLG_NORMAL
            )
            db.add(db_obj)
            db.flush()
            return db_obj
        except Exception as err:
            logger.error("Error occurred " + str(err))
            raise err

    def get_activity_memo_by_car_id(
            self, db: Session, *, car_id: int, skip: int = 0, limit: int = 100, sort_name: str, sort_type: int
    ) -> ActivityMemo:
        try:
            # default data
            activity_memo = (
                db.query(self.model)
                .filter(ActivityMemo.car_id == car_id,
                        ActivityMemo.delete_flag == Const.DEL_FLG_NORMAL,
                        )
            )
            total = activity_memo.count()
            # Sort data
            if sort_name == Const.MEMO_CREATE_AT:
                activity_memo = activity_memo.order_by(
                    ActivityMemo.memo_create_at.asc()
                    if sort_type == Const.SORT_ASC
                    else ActivityMemo.memo_create_at.desc()
                )
            if sort_name == Const.MEMO_EDITOR:
                activity_memo = activity_memo.order_by(
                    ActivityMemo.memo_editor.asc()
                    if sort_type == Const.SORT_ASC
                    else ActivityMemo.memo_editor.desc()
                )
            else:
                activity_memo = activity_memo.order_by(
                    ActivityMemo.memo_create_at.desc(),
                )
            # limit offset
            activity_memo = activity_memo.offset(skip).limit(limit)
            activity_memo = activity_memo.all()

            return activity_memo, total
        except Exception as err:
            logger.error("Error occurred " + str(err))
            raise err

    def update_activity_memo(
            self, db: Session, obj_in: ActivityMemoUpdate, user_id: int, activity_memo_id: int
    ) -> ActivityMemo:
        try:
            obj_update = (
                db.query(ActivityMemo)
                .filter(
                    ActivityMemo.id == activity_memo_id,
                    ActivityMemo.delete_flag == Const.DEL_FLG_NORMAL
                )
                .first()
            )
            if not obj_update:
                logging.error("Error occurred: " + f"Item not found: ActivityMemo.id: {activity_memo_id}")
                raise HTTPException(
                    status_code=404,
                    detail=f"Item not found: ActivityMemo.id: {activity_memo_id}",
                )
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in update_data.keys():
                setattr(obj_update, field, update_data[field])
            obj_update.update_at = datetime.utcnow()
            obj_update.update_id = user_id
            db.add(obj_update)
            db.flush()
            return obj_update
        except Exception as err:
            logger.error("Error occurred " + str(err))
            raise err

    def delete_by_update_delete_flag(self, db:Session, *, activity_memo_id: int, user_id) -> ActivityMemo:
        try:
            db_obj = (
                db.query(self.model)
                .filter(
                    ActivityMemo.id == activity_memo_id, ActivityMemo.delete_flag == Const.DEL_FLG_NORMAL
                )
                .first()
            )
            if not db_obj:
                logging.error("Error occurred: " + f"Item not found: ActivityMemo.id: {activity_memo_id}")
                raise HTTPException(
                    status_code=404,
                    detail=f"Item not found: ActivityMemo.id: {activity_memo_id}",
                )
            db_obj.delete_flag = Const.DEL_FLG_DELETE
            db_obj.delete_at = datetime.utcnow()
            db_obj.delete_id = user_id
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as err:
            logger.error("Error occurred " + str(err))
            raise err


activity_memo = CRUDActivityMemo(ActivityMemo)
