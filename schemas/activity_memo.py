from typing import Optional, Any, List

from pydantic import BaseModel
from datetime import datetime


# Shared properties
class ActivityMemoBase(BaseModel):
    car_id: Optional[int]
    memo_editor: Optional[str]
    comment: Optional[str]
    memo_create_at: Optional[datetime]


class ActivityMemoBaseCreate(BaseModel):
    car_id: int
    memo_editor: Optional[str]
    comment: str


class ActivityMemoBaseUpdate(BaseModel):
    comment: str
    memo_editor: Optional[str]


class ActivityMemoCreate(ActivityMemoBaseCreate):
    pass


# Properties to receive on item update
class ActivityMemoUpdate(ActivityMemoBaseUpdate):
    pass


# Properties shared by models stored in DB
class ActivityMemoInDBBase(ActivityMemoBase):
    insert_id: Optional[int]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class ActivityMemo(ActivityMemoBase):
    id: int

    class Config:
        orm_mode = True

class ActivityMemoResponseList(BaseModel):
    total: Optional[int]
    results: Optional[List[ActivityMemo]]

# Properties properties stored in DB
class ActivityMemoInDB(ActivityMemoInDBBase):
    pass


