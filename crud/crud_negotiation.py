from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.negotiation import Negotiation
from app.models.m_company import MCompany
from app.models.store import Store
from app.schemas.negotiation import (
    NegotiationBase,
    NegotiationQuery,
    NegotiationInDB,
    NegotiationCreate,
    NegotiationUpdate,
)
from app.constants import Const
from datetime import datetime
from fastapi.encoders import jsonable_encoder


class CRUDNegotiation(CRUDBase[Negotiation, NegotiationCreate, NegotiationUpdate]):

    def get_negotiation_by_car_id(
        self, db: Session, *, car_id: int, limit: int, offset: int
    ) -> Any:
        result = db.query(self.model, MCompany.company_name, Store.store_name)\
            .outerjoin(Store, Store.id == Negotiation.negotiation_store_id)\
            .outerjoin(MCompany, MCompany.company_code == Store.company_code)\
            .filter(
                    Negotiation.car_id == car_id,
                    Negotiation.delete_flag == Const.DEL_FLG_NORMAL,
                )
        result = result.order_by(Negotiation.period_from.desc())

        # get count
        total = result.count()
        # set limit offset
        result = result.limit(limit)
        result = result.offset(offset)
        # excute query
        result = result.all()
        return total, result

    def update_negotiation_status_by_car_id(
            self, db: Session, *, car_id: int, update_id: int, negotiation_status: int
    ) -> Any:
        update_obj = db.query(self.model).filter(
                            Negotiation.car_id == car_id,
                            Negotiation.delete_flag == Const.DEL_FLG_NORMAL,
                        ).first()

        if not update_obj:
            return None
        update_obj.negotiation_status = negotiation_status
        update_obj.update_at = datetime.utcnow()
        update_obj.update_id = update_id
        db.add(update_obj)
        db.flush()
        return update_obj

    def update_negotiation_by_car_id(
            self, db: Session, car_id: int, obj_in: NegotiationUpdate, update_id: int
    ) -> Any:
        db_obj = db.query(self.model).filter(
                            Negotiation.car_id == car_id,
                            Negotiation.delete_flag == Const.DEL_FLG_NORMAL,
                        ).first()

        if not db_obj:
            return None
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.update_at = datetime.utcnow()
        db_obj.update_id = update_id
        db.add(db_obj)
        db.flush()
        return db_obj

    def delete_by_car_id(self, db: Session, *, car_id: int, delete_id: int) -> Negotiation:
        db_obj = (
            db.query(self.model)
            .filter(
                Negotiation.car_id == car_id,
                Negotiation.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )
        if not db_obj:
            return None
        db_obj.delete_flag = Const.DEL_FLG_DELETE
        db_obj.delete_at = datetime.utcnow()
        db_obj.delete_id = delete_id
        db.add(db_obj)
        db.flush()
        return db_obj

negotiation = CRUDNegotiation(Negotiation)
