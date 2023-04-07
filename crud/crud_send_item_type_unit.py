from typing import Any
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.send_item_type_unit import SendItemTypeUnit
from app.models.code_master import CodeMaster
from app.schemas.send_item_type_unit import SendItemTypeUnitCreate, SendItemTypeUnitUpdate
from datetime import datetime, timedelta
from app import crud
from fastapi.encoders import jsonable_encoder
from itertools import groupby
from fastapi import HTTPException, status
from dateutil import parser


class CRUDSendItemTypeUnit(CRUDBase[SendItemTypeUnit, SendItemTypeUnitCreate, SendItemTypeUnitUpdate]):
    ITEM_TYPE_CODE = 'send_item_type_code'

    def get_key(self, k):
        return k['send_item_type_code']

    def get_key_from_apply_at(self, k):
        return k['from_apply_at']

        # Get service unit

    def get_service_unit_by_company(
            self, db: Session,
            company_code: str
    ) -> SendItemTypeUnit:
        list_service_units = db.query(
            self.model.id,
            self.model.send_item_type_code,
            self.model.unit,
            self.model.from_apply_at,
            self.model.to_apply_at,
            CodeMaster.code_name
        ).filter(SendItemTypeUnit.delete_flag == 0, SendItemTypeUnit.company_code == company_code). \
            join(CodeMaster, (CodeMaster.code_type == self.ITEM_TYPE_CODE) & (
                CodeMaster.code_value == SendItemTypeUnit.send_item_type_code)).all()
        return list_service_units

    def detele_service_unit_by_update_delete_flag(
            self,
            db: Session,
            *,
            id: int
    ) -> SendItemTypeUnit:
        service_unit = db.query(self.model).filter(SendItemTypeUnit.id == id, SendItemTypeUnit.delete_flag == 0).first()
        if not service_unit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Service unit id {id} not found')
        service_unit.delete_flag = 1
        service_unit.delete_at = datetime.utcnow()
        db.add(service_unit)
        db.commit()
        db.refresh(service_unit)
        return service_unit

    def create_service_unit(
            self,
            db: Session,
            *,
            obj_in: SendItemTypeUnitCreate
    ) -> SendItemTypeUnit:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, insert_id=88888, insert_at=datetime.utcnow(), update_id=1,
                            update_at=datetime.utcnow(), delete_flag=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


send_item_type_unit = CRUDSendItemTypeUnit(SendItemTypeUnit)
