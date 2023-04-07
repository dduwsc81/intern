from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class CarLicenseBase(BaseModel):
    id: Optional[int]
    company_code: Optional[str]
    customer_code: Optional[str]
    license_color: Optional[str]
    license_number: Optional[str]
    license_image_front: Optional[str]
    license_image_back: Optional[str]


class CarLicenseCreate(CarLicenseBase):
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class CarLicenseUpdate(CarLicenseBase):
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


# Properties shared by models stored in DB
class CarLicenseInDBBase(CarLicenseBase):
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True
