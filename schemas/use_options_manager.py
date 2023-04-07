from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UseOptionsManagerBase(BaseModel):
    id: Optional[int]
    car_id: Optional[int]
    estimate_id: Optional[int]
    option_id: Optional[int]
    option_name: Optional[str]
    option_packet_id: Optional[int]
    option_packet_name: Optional[str]
    option_fee: Optional[int]
    option_fee_tax: Optional[int]
    option_content: Optional[str]


class UseOptionsManagerCreate(UseOptionsManagerBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


# Properties shared by models stored in DB
class UseOptionsManagerInDBBase(UseOptionsManagerBase):
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
class UseOptionsManager(UseOptionsManagerInDBBase):
    pass


class UseOptionsManagerUpdate(UseOptionsManagerInDBBase):
    pass
