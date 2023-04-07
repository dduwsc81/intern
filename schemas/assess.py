from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AssessBase(BaseModel):
    id: Optional[int]
    car_id: Optional[int]
    company_code: Optional[str]
    assess_status: Optional[int]
    assess_store_id: Optional[int]
    assess_store_name: Optional[str]
    assess_user_id: Optional[int]
    assess_user_name: Optional[str]
    assess_price: Optional[int]
    expiration_date: Optional[datetime]
    approve_user_id: Optional[int]
    assess_comment: Optional[str]
    assess_datetime: Optional[datetime]


class AssessCreate(AssessBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class AssessCreate(AssessBase):
    pass


class AssessInDB(AssessBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class AssessUpdate(AssessInDB):
    pass

class AssessResponse(BaseModel):
    car_id: Optional[int]
    company_code: Optional[str]
    assess_status: Optional[int]
    assess_store_id: Optional[int]
    assess_store_name: Optional[str]
    assess_user_id: Optional[int]
    assess_user_name: Optional[str]
    assess_price: Optional[int]
    expiration_date: Optional[datetime]
    approve_user_id: Optional[int]
    assess_comment: Optional[str]
    assess_datetime: Optional[datetime]

class AssessUpdateByRegisterSale(AssessResponse):
    register_sale_id: Optional[int]
    user_id: Optional[int]
