from datetime import datetime
from typing import Any, Optional
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.constants import Const
from app.crud.base import CRUDBase
from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseCreate, PurchaseUpdate


class CRUDPurchase(CRUDBase[Purchase, PurchaseCreate, PurchaseUpdate]):

    def update_status_purchase_by_negotiation_id(
            self,
            db: Session,
            update_id: int,
            obj_in: PurchaseUpdate,
    ) -> Purchase:
        db_obj = db.query(self.model)\
                       .filter(Purchase.negotiation_id == obj_in.negotiation_id,
                               Purchase.delete_flag == Const.DEL_FLG_NORMAL,)\
                       .first()
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

        db_obj.update_at = datetime.utcnow(),
        db_obj.update_id = update_id,
        db.add(db_obj)
        db.flush()
        return db_obj


purchase = CRUDPurchase(Purchase)
