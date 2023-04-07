from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class CustomerActiveStatusBase(BaseModel):
    id: Optional[int]
    company_code: Optional[str]
    customer_code: Optional[str]
    active_status: Optional[str]
    maintenance_sales_recording_date: Optional[date]
    car_sales_recording_date: Optional[date]
    recency_score: Optional[int]
    maintenance_frequency: Optional[int]
    car_sales_frequency: Optional[int]
    frequency_score: Optional[int]
    maintenance_monetary: Optional[float]
    car_sales_monetary: Optional[float]
    monetary_score: Optional[int]
    total_score: Optional[int]
    rank: Optional[int]

    class Config:
        orm_mode = True


# Properties to create customer
class CustomerActiveStatusCreate(CustomerActiveStatusBase):
    company_code: str
    customer_code: str
    active_status: str


# Properties to Insert DB
class CustomerActiveStatusInDB(CustomerActiveStatusCreate):
    insert_at: datetime
    update_at: datetime


# Properties to update customer
class CustomerActiveStatusUpdate(CustomerActiveStatusCreate):
    id: int
    insert_at: Optional[datetime]
    update_at: datetime


class CustomerActiveStatus(CustomerActiveStatusInDB):
    pass
