from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class NegotiationBase(BaseModel):
    car_id: Optional[int]
    register_sale_id: Optional[int]
    contact_id: Optional[int]
    estimate_id: Optional[int]
    negotiation_store_id: Optional[int]
    owner_store_id: Optional[int]
    negotiation_status: Optional[int]
    period_from: Optional[datetime]
    period_to: Optional[datetime]


class NegotiationInDB(NegotiationBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class NegotiationCreate(NegotiationInDB):
    pass


class NegotiationUpdate(NegotiationCreate):
    pass


class NegotiationQuery(NegotiationBase):
    show_total_all: Optional[int]


class Negotiation(NegotiationBase):
    id: Optional[int]
    store_name: Optional[str]
    company_name: Optional[str]

    class Config:
        orm_mode = True


class ListNegotiation(BaseModel):
    total: Optional[int] = 0
    result: Optional[List[Negotiation]]

    class Config:
        orm_mode = True


class NegotiationOfferByBuyer(BaseModel):
    user_id: int
    car_id: int


class NegotiationUpdateDeadline(BaseModel):
    car_id: int
    period_to: Optional[datetime]


class NegotiationUpdateStatus(BaseModel):
    status: Optional[bool]
