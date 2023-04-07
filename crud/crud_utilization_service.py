from typing import Any, Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.utilization_service import UtilizationService
from app.models.car import Car
from app.models.store import Store
from app.schemas.utilization_service import UtilizationServiceCreate, \
    UtilizationServiceUpdate, UtilizationServiceInDB, UtilizationQueryParam
from app.constants import Const
from sqlalchemy import func, and_, extract
from datetime import datetime

UTILIZATION_BUY = 1
UTILIZATION_SELL = 2
SERVICE_NEGOTIATION = "P001"
SERVICE_PLATFORM = "P002"


class CRUDUtilizationService(CRUDBase[UtilizationService, UtilizationServiceCreate, UtilizationServiceUpdate]):

    def create_utilization_service(self, db: Session, *, user_id: int, obj_in: UtilizationServiceInDB) -> Any:
        obj_in.insert_id = user_id
        obj_in.update_id = user_id

        obj_in.insert_at = datetime.utcnow()
        obj_in.update_at = datetime.utcnow()
        obj_in.utilization_datetime = datetime.utcnow()

        obj_in.delete_flag = Const.DEL_FLG_NORMAL

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        return db_obj


    def get_utilization(self, db: Session, *, limit: int, skip: int, item_in: UtilizationQueryParam) -> Any:
        number_of_negotiation_cars, negotiation_amount \
            = db.query(func.count(UtilizationService.id).label("number_of_negotiation_cars"),
                       func.sum(UtilizationService.payment_amount).label("negotiation_amount")) \
            .filter(and_(UtilizationService.store_id.in_(item_in.list_store),
                         extract('year', UtilizationService.utilization_datetime) == datetime.utcnow().year,
                         extract('month', UtilizationService.utilization_datetime) == datetime.utcnow().month,
                         UtilizationService.div == UTILIZATION_BUY,
                         UtilizationService.service_cd == SERVICE_NEGOTIATION,
                         UtilizationService.delete_flag == Const.DEL_FLG_NORMAL)) \
            .first()

utilization_service = CRUDUtilizationService(UtilizationService)
