from sqlalchemy.orm import Session
from typing import Any
from app.crud.base import CRUDBase
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import ActivityLogCreate, ActivityLogUpdate
from fastapi.encoders import jsonable_encoder
from ..api.api_v1.endpoints.format_status import *


class CRUDActivityLog(CRUDBase[ActivityLog, ActivityLogCreate, ActivityLogUpdate]):
    UPDATE_STATUS = 1
    REQUEST_SENDING = (1, 2, 5)
    RECEIVE_REQUEST = (3, 4, 5)
    SIDE_ADMIN_SEND = 2
    SIDE_ADMIN_RECEIVE = 4

    def get_activity_log_status(
            self,
            db: Session,
            *,
            send_customer_id: int,
    ) -> Any:
        activity_logs = db.query(
            self.model.status,
            self.model.comment,
            self.model.update_at
        ).filter(ActivityLog.send_customer_id == send_customer_id, ActivityLog.delete_flag == 0).all()
        activity_logs = jsonable_encoder(activity_logs)
        for item in activity_logs:
            item["update_at"] = utc_to_jst(item["update_at"]) if item["update_at"] else ""
        return activity_logs

    def create_activity_log(
        self, db: Session, *, obj_in: ActivityLogCreate, cognito_id: int
    ) -> ActivityLog:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            insert_id=cognito_id,
            insert_at=datetime.utcnow(),
            update_id=cognito_id,
            update_at=datetime.utcnow(),
            delete_flag=0
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


activity_log = CRUDActivityLog(ActivityLog)
