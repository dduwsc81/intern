from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime

# Shared properties
class MPriceBase(BaseModel):
    display_text : Optional[str]
    value : Optional[str]
    order_index : Optional[int]


# Properties to receive on item creation
class MPriceCreate(MPriceBase):
    pass


# Properties to receive on item update
class MPriceUpdate(MPriceBase):
    pass


# Properties shared by models stored in DB
class MPriceInDBBase(MPriceBase):
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
class MPrice(MPriceInDBBase):
    pass


# Properties properties stored in DB
class MPriceInDB(MPriceInDBBase):
    pass