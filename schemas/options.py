from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OptionsBase(BaseModel):
    option_id: Optional[int]
    option_name: Optional[str]
    option_fee: Optional[int]
    option_fee_tax: Optional[int]
    content: Optional[str]


class OptionsCreate(OptionsBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


# Properties shared by models stored in DB
class OptionsInDBBase(OptionsBase):
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
class Options(OptionsInDBBase):
    pass


class OptionsResponseModel(OptionsBase):
    class Config:
        orm_mode = True


class OptionsUpdate(OptionsInDBBase):
    pass


class OptionQuery(BaseModel):
    option_id: Optional[int]
    option_fee: Optional[int]


class OptionResponse(BaseModel):
    option_name: Optional[str]
    option_id: Optional[int]
    option_fee: Optional[int]


