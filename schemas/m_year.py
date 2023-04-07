from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime

# Shared properties
class MYearBase(BaseModel):
    display_text : Optional[str]
    value : Optional[str]
    order_index : Optional[int]


# Properties to receive on item creation
class MYearCreate(MYearBase):
    pass


# Properties to receive on item update
class MYearUpdate(MYearBase):
    pass


# Properties shared by models stored in DB
class MYearInDBBase(MYearBase):
    id : int

    display_text : Optional[str]
    value : Optional[str]
    order_index : Optional[int]

    insert_id : Optional[int]
    insert_at : Optional[datetime]
    update_id : Optional[int]
    update_at : Optional[datetime]
    delete_id : Optional[int]
    delete_at : Optional[datetime]
    delete_flag : Optional[int]
    class Config:
        orm_mode = True


# Properties to return to client
class MYear(MYearInDBBase):
    pass


# Properties properties stored in DB
class MYearInDB(MYearInDBBase):
    pass