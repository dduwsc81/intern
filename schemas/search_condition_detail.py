from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class SearchConditionDetailBase(BaseModel):
    search_condition_id: int
    condition_name: Optional[str]
    condition_type: Optional[str]
    values: Optional[str]


# Properties to receive on item creation
class SearchConditionDetailCreate(SearchConditionDetailBase):
    pass


# Properties to receive on item update
class SearchConditionDetailUpdate(SearchConditionDetailBase):
    pass


# Properties shared by models stored in DB
class SearchConditionDetailInDBBase(BaseModel):
    id: int
    search_condition_id: int
    condition_name: Optional[str]
    condition_type: Optional[str]
    values: Optional[str]
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
class SearchConditionDetail(SearchConditionDetailBase):
    id: int

    class Config:
        orm_mode = True


# Properties properties stored in DB
class SearchConditionDetailInDB(SearchConditionDetailInDBBase):
    pass
