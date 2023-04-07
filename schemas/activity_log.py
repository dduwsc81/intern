from typing import Optional

from pydantic import BaseModel
from datetime import datetime


# Shared properties
class ActivityLogBase(BaseModel):
    send_customer_id: Optional[int]
    status: Optional[int]
    comment: Optional[str]


# Properties to receive on item creation
class ActivityLogCreate(ActivityLogBase):
    pass


# Properties to receive on item update
class ActivityLogUpdate(ActivityLogBase):
    pass


# Properties shared by models stored in DB
class ActivityLogInDBBase(ActivityLogBase):
    id: int
    send_customer_id: Optional[int]
    status: Optional[int]
    comment: Optional[str]
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class ActivityLog(ActivityLogInDBBase):
    pass


# Properties properties stored in DB
class ActivityLogInDB(ActivityLogInDBBase):
    pass