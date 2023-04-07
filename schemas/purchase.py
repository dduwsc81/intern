from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PurchaseBase(BaseModel):
    car_id: Optional[int]
    negotiation_id: Optional[int]
    status: Optional[int]
    purchase_store_id: Optional[str]
    purchase_user_id: Optional[str]
    purchase_store_id: Optional[str]
    sale_approve_user_id: Optional[str]
    sale_approve_store_id: Optional[str]
    contract_datetime: Optional[datetime]
    close_datetime: Optional[datetime]
    comment: Optional[str]


class PurchaseCreate(PurchaseBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class PurchaseUpdate(PurchaseBase):
    pass


class PurchaseInDB(PurchaseBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class PurchaseApproveQueryParam(BaseModel):
    car_id: int
    store_id: int
    status: Optional[int]
    user_id: Optional[int]
    comment: Optional[str]


class Purchase(PurchaseBase):
    purchase_id: int

    class Config:
        orm_mode = True
