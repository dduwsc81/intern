from typing import Optional, List

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class OptionGroupBase(BaseModel):
    menu_id: Optional[int]
    group_name: Optional[str]
    single_option: Optional[int]
    option_require: Optional[int]


# Properties to receive on item creation
class OptionGroupCreate(OptionGroupBase):
    pass


# Properties to receive on item update
class OptionGroupUpdate(OptionGroupBase):
    pass


# Properties shared by models stored in DB
class OptionGroupInDBBase(OptionGroupBase):
    id: int

    menu_id: Optional[int]
    group_name: Optional[str]
    single_option: Optional[int]
    option_require: Optional[int]

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
class OptionGroup(OptionGroupInDBBase):
    pass


# Properties properties stored in DB
class OptionGroupInDB(OptionGroupInDBBase):
    pass


# Shared properties of response
class OptionGroupResponse(BaseModel):
    id: Optional[int]
    menu_id: Optional[int]
    group_name: Optional[str]
    single_option: Optional[int]
    option_require: Optional[int]
    has_option: Optional[bool]

class MenuInfo(BaseModel):
    menu_id: Optional[int]
    code_type_id: Optional[int]
    menu_name: Optional[str]
    from_store_code: Optional[str]
    from_company_code: Optional[str]
    store_name: Optional[str]
    company_name: Optional[str]
    service_name: Optional[str]

class OptionGroupFullInfo(OptionGroupInDBBase):
    has_option: Optional[bool]


class OptionGroupListResponse(BaseModel):
    menu_info: Optional[MenuInfo]
    list_group_option: Optional[List[OptionGroupFullInfo]]
