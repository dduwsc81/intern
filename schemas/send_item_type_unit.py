from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class SendItemTypeUnitBase(BaseModel):
    company_code: Optional[str]
    send_item_type_code: Optional[str]
    unit: Optional[int]
    from_apply_at: Optional[date]
    to_apply_at: Optional[date]


# Properties to receive on item creation
class SendItemTypeUnitCreate(SendItemTypeUnitBase):
    pass


# Properties to receive on item update
class SendItemTypeUnitUpdate(SendItemTypeUnitBase):
    pass


# Properties shared by models stored in DB
class SendItemTypeUnitInDBBase(SendItemTypeUnitBase):
    id: int
    company_code: Optional[str]
    send_item_type_code: Optional[str]
    unit: Optional[int]
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
class SendItemTypeUnit(SendItemTypeUnitInDBBase):
    pass


# Properties properties stored in DB
class SendItemTypeUnitInDB(SendItemTypeUnitInDBBase):
    pass
