from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CustomerMarketBase(BaseModel):
    id: Optional[int]
    company_code: Optional[str]
    customer_code: Optional[str]
    insurance_class: Optional[str]
    decade_age: Optional[str]
    license_color: Optional[str]


class CustomerMarketInDB(CustomerMarketBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class CustomerMarket(CustomerMarketBase):
    class Config:
        orm_mode = True


class CustomerMarketCreate(CustomerMarketBase):
    pass


class CustomerMarketUpdate(CustomerMarketInDB):
    pass
