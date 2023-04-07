from typing import Optional

from pydantic import BaseModel
from datetime import datetime


# Shared properties
class MDivisionBase(BaseModel):
    id: Optional[int]
    div: Optional[int]
    div_name: Optional[str]
    param: Optional[int]
    desc: Optional[str]
    order_index: Optional[str]
    comment: Optional[str]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class MDivisionCreate(MDivisionBase):
    pass


class MDivisionUpdate(MDivisionBase):
    pass


class MDivision(BaseModel):
    id: Optional[int]
    div: Optional[int]
    div_name: Optional[str]
    param: Optional[int]
    desc: Optional[str]
    order_index: Optional[int]
    comment: Optional[str]


# Properties shared by models stored in DB
class MDivisionInDBBase(MDivisionBase):
    pass

    class Config:
        orm_mode = True
