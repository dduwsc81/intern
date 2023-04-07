from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class CustomerCarLifeMasterLinkBase(BaseModel):
    id: Optional[int]
    company_code: Optional[str]
    car_code: Optional[str]
    car_life_code: Optional[str]


class CustomerCarLifeMasterLinkCreate(CustomerCarLifeMasterLinkBase):
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class CustomerCarLifeMasterLinkUpdate(CustomerCarLifeMasterLinkBase):
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


# Properties shared by models stored in DB
class CustomerCarLifeMasterLinkInDBBase(CustomerCarLifeMasterLinkBase):
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True
