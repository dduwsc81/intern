from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel


class CarTransactionHistoryBase(BaseModel):
    id: Optional[int]
    car_id: Optional[int]
    company_code: Optional[str]
    car_code: Optional[str]
    transaction_date: Optional[date]
    transaction_type: Optional[int]
    transaction_type_name: Optional[str]
    contents: Optional[str]

    class Config:
        orm_mode = True


class CarTransactionHistoryInDB(CarTransactionHistoryBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class CarTransactionHistoryCreate(CarTransactionHistoryInDB):
    pass


class CarTransactionHistoryUpdate(CarTransactionHistoryInDB):
    pass

class CarTransactionHistoryList(BaseModel):
    results: List[CarTransactionHistoryBase]
    total: int
