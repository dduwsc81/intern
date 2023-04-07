from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime

# Shared properties
class MDistanceTravelledBase(BaseModel):
    display_text : Optional[str]
    value : Optional[str]
    order_index : Optional[int]


# Properties to receive on item creation
class MDistanceTravelledCreate(MDistanceTravelledBase):
    pass


# Properties to receive on item update
class MDistanceTravelledUpdate(MDistanceTravelledBase):
    pass


# Properties shared by models stored in DB
class MDistanceTravelledInDBBase(MDistanceTravelledBase):
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
class MDistanceTravelled(MDistanceTravelledInDBBase):
    pass


# Properties properties stored in DB
class MDistanceTravelledInDB(MDistanceTravelledInDBBase):
    pass