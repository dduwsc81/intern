from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime

# Shared properties
class StaffBase(BaseModel):
    company_code: Optional[str]
    staff_code: Optional[str]
    cognito_id: Optional[str]
    cars_manager_id: Optional[str]
    staff_photo: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    last_name_kana: Optional[str]
    first_name_kana: Optional[str]
    birthday: Optional[date]
    phone_number: Optional[str]
    email: Optional[str]

# Properties to receive on item creation
class StaffCreate(StaffBase):
    pass


# Properties to receive on item update
class StaffUpdate(StaffBase):
    pass


# Properties shared by models stored in DB
class StaffInDBBase(StaffBase):
    id: Optional[int]
    company_code: Optional[str]
    staff_code: Optional[str]
    cognito_id: Optional[str]
    cars_manager_id: Optional[str]
    staff_photo: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    last_name_kana: Optional[str]
    first_name_kana: Optional[str]
    birthday: Optional[date]
    phone_number: Optional[str]
    email: Optional[str]
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

# Properties to return to client
class Staff(StaffInDBBase):
    pass


# Properties properties stored in DB
class StaffInDB(StaffInDBBase):
    pass
