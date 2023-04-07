from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel


class UtilizationServiceBase(BaseModel):
    car_id: Optional[int]
    register_sale_id: Optional[int]
    contact_id: Optional[int]
    negotiation_id: Optional[int]
    utilization_datetime: Optional[datetime]
    business_store_id: Optional[int]
    business_user_id: Optional[int]
    service_cd: Optional[str]
    service_name: Optional[str]
    receipt_amount: Optional[int]
    payment_amount: Optional[int]
    div: Optional[int]


class UtilizationServiceInDB(UtilizationServiceBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class UtilizationServiceCreate(UtilizationServiceInDB):
    pass


class UtilizationServiceUpdate(UtilizationServiceInDB):
    id: Optional[int]


class UtilizationServiceQuery(UtilizationServiceBase):
    show_total_all: Optional[int]


class UtilizationService(UtilizationServiceBase):
    id: int

    class Config:
        orm_mode = True


class UtilizationQueryParam(BaseModel):
    list_store: List[int]
    billing_datetime: date

class UtilizationObject(UtilizationServiceBase):
    negotiation_id: int
    maker: Optional[str]
    car_type: Optional[str]
    store_name: Optional[str]

class UtilizationServiceList(BaseModel):
    number_of_negotiation_cars: Optional[int]
    negotiation_amount: Optional[int]
    number_of_platform_buy_car: Optional[int]
    platform_buy_amount: Optional[int]
    number_of_platform_sell_car: Optional[int]
    platform_sell_amount: Optional[int]
    total: Optional[int]
    list_utilization_service: Optional[List[UtilizationObject]]

