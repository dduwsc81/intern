from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class LikeDetailBase(BaseModel):
    car_id: Optional[int]
    store_id: Optional[str]


# Properties to receive on item creation
class LikeDetailCreate(LikeDetailBase):
    pass


# Properties to receive on item update
class LikeDetailUpdate(LikeDetailBase):
    pass


# Properties shared by models stored in DB
class LikeDetailInDBBase(LikeDetailBase):
    id: int
    car_id: int
    store_id: Optional[str]

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
class LikeDetail(LikeDetailInDBBase):
    pass


# Properties properties stored in DB
class LikeDetailInDB(LikeDetailInDBBase):
    pass
