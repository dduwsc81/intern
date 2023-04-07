from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MServiceBase(BaseModel):
    service_cd: Optional[str]
    service_name: Optional[str]
    category: Optional[str]
    price: Optional[int]
    order_index: Optional[int]
    description: Optional[str]


class MServiceInDB(MServiceBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class MServiceCreate(MServiceInDB):
    pass


class MServiceUpdate(MServiceInDB):
    id: Optional[int]


class MServiceQuery(MServiceBase):
    pass


class MService(MServiceBase):
    id: int

    class Config:
        orm_mode = True
