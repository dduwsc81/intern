from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class OptionSettingBase(BaseModel):
    group_id: Optional[int]
    option_name: Optional[str]
    option_user_price: Optional[int]
    option_content: Optional[str]
    option_time_require: Optional[int]


# Properties to receive on item creation
class OptionSettingCreate(OptionSettingBase):
    pass


# Properties to receive on item update
class OptionSettingUpdate(OptionSettingBase):
    pass


# Properties shared by models stored in DB
class OptionSettingInDBBase(OptionSettingBase):
    id: int

    group_id: Optional[int]
    option_name: Optional[str]
    option_user_price: Optional[int]
    option_content: Optional[str]
    option_time_require: Optional[int]

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
class OptionSetting(OptionSettingInDBBase):
    pass


# Properties properties stored in DB
class OptionSettingInDB(OptionSettingInDBBase):
    pass


# Shared properties of response
class OptionSettingResponse(BaseModel):
    id: Optional[int]
    group_id: Optional[int]
    option_name: Optional[str]
    option_user_price: Optional[int]
    option_content: Optional[str]
    option_time_require: Optional[int]
