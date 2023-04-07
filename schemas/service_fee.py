from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class ServiceFeeBase(BaseModel):
    code_type_id: Optional[int]
    store_code: Optional[str]
    company_code: Optional[str]
    send_incentive: Optional[int]
    fg_incentive: Optional[int]
    from_apply_at: Optional[date]
    to_apply_at: Optional[date] = None


# Properties to receive on item creation
class ServiceFeeCreate(ServiceFeeBase):
    pass


# Properties to receive on item update
class ServiceFeeUpdate(ServiceFeeBase):
    pass


# Properties shared by models stored in DB
class ServiceFeeInDBBase(ServiceFeeBase):
    id: int

    code_type_id: Optional[int]
    store_code: Optional[str]
    company_code: Optional[str]
    send_incentive: Optional[int]
    fg_incentive: Optional[int]

    from_apply_at: Optional[date]
    to_apply_at: Optional[date]

    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class ServiceFee(ServiceFeeInDBBase):
    pass


# Properties properties stored in DB
class ServiceFeeInDB(ServiceFeeInDBBase):
    pass


# Shared properties
class ServiceFeeRequest(BaseModel):
    store_code: Optional[str] = None
    company_code: Optional[str] = None
