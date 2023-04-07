from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.search_condition_detail import SearchConditionDetail


# Shared properties
class SearchConditionBase(BaseModel):
    search_name: Optional[str]
    store_id: Optional[str]
    search_tab_id: Optional[int]


# Properties to receive on item creation
class SearchConditionCreate(SearchConditionBase):
    pass


# Properties to receive on item update
class SearchConditionUpdate(SearchConditionBase):
    pass


# Properties shared by models stored in DB
class SearchConditionInDBBase(BaseModel):
    search_condition_id: int
    search_name: Optional[str]
    store_id: Optional[str]
    search_tab_id: Optional[int]
    order_index: Optional[int]
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
class SearchCondition(SearchConditionBase):
    search_condition_id: int
    order_index: Optional[int]

    class Config:
        orm_mode = True


# Properties properties stored in DB
class SearchConditionInDB(SearchConditionInDBBase):
    pass


# Full Search response
class SearchAndSearchDetail(BaseModel):
    result: List[SearchCondition]
    detail: List[SearchConditionDetail]

    class Config:
        orm_mode = True
