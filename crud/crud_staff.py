from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate
from datetime import datetime, timedelta
from sqlalchemy import or_


class CRUDMStaff(CRUDBase[Staff, StaffCreate, StaffUpdate]):
    def get_staff_by_id(
            self, db: Session, *, id: int
    ) -> Any:
        staff = db.query(self.model). \
            filter(Staff.id == id, Staff.delete_flag == 0).first()
        if not staff:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Staff if {id} not found')
        return staff

    def get_staff_by_cognito_id(
            self, db: Session, *, cognito_id: int, company_code: str
    ) -> Staff:
        staff = db.query(self.model). \
            filter(Staff.cognito_id == cognito_id,
                   # Staff.company_code == company_code,
                   Staff.delete_flag == 0).first()
        # if not staff:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Staff if {id} not found')
        return staff


staff: CRUDMStaff = CRUDMStaff(Staff)
