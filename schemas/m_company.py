from typing import Optional, List

from pydantic import BaseModel
from datetime import date, datetime
from app.schemas.store import StoreBasic

# Shared properties
class MCompanyBase(BaseModel):
    owner_staff_code: Optional[str]
    company_name: Optional[str]
    company_representative: Optional[str]
    zip_code: Optional[str]
    prefectures_code: Optional[str]
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    employee_count: Optional[int]
    shop_count: Optional[int]
    first_month_of_the_year: Optional[int]


# Properties to receive on item creation
class MCompanyCreate(MCompanyBase):
    pass


# Properties to receive on item update
class MCompanyUpdate(MCompanyBase):
    pass


# Properties shared by models stored in DB
class MCompanyInDBBase(MCompanyBase):
    id: int
    company_code: Optional[str]
    owner_staff_code: Optional[str]
    company_name: Optional[str]
    company_representative: Optional[str]
    zip_code: Optional[str]
    prefectures_code: Optional[str]
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    employee_count: Optional[int]
    shop_count: Optional[int]
    first_month_of_the_year: Optional[int]
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
class MCompany(MCompanyInDBBase):
    pass


# Properties properties stored in DB
class MCompanyInDB(MCompanyInDBBase):
    pass

class MCompanyBasic(BaseModel):
    company_code: Optional[str]
    company_name: Optional[str]
    store_info: Optional[List[StoreBasic]]
