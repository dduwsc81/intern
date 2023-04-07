from datetime import datetime
from typing import Optional
from typing import List

from pydantic import BaseModel
from app.schemas.options import OptionQuery, OptionResponse

class EstimateBase(BaseModel):
    id: Optional[int]
    car_id: Optional[int]
    estimate_type: Optional[int]
    purchase_type: Optional[int]
    purchase_store_id: Optional[int]
    hope_sale_base_price: Optional[int]
    market_fee: Optional[int]
    land_transportation_fee: Optional[int]
    name_change_fee: Optional[int]
    brokerage_rate: Optional[int]
    brokerage_fee: Optional[int]
    margin_rate: Optional[int]
    margin_fee: Optional[int]
    options_fee: Optional[int]
    business_amount_type: Optional[int]
    business_amount: Optional[int]
    customer_amount_type: Optional[int]
    customer_amount: Optional[int]
    tax_rate: Optional[int]
    hope_sale_base_price_tax: Optional[int]
    market_fee_tax: Optional[int]
    land_transportation_fee_tax: Optional[int]
    name_change_fee_tax: Optional[int]
    option_fee_tax: Optional[int]
    business_amount_tax: Optional[int]
    customer_amount_tax: Optional[int]
    class Config:
        orm_mode = True


class EstimateCreate(EstimateBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class EstimateUpdate(EstimateBase):
    id: int
    option_id: Optional[int]
    option_fee: Optional[int]
    register_sale_type: Optional[int]


# Properties shared by models stored in DB
class EstimateInDBBase(EstimateBase):
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
class Estimate(EstimateBase):
    id: int

    class Config:
        orm_mode = True


class EstimateResponseModel(EstimateBase):
    list_options: Optional[List[OptionResponse]]


class EstimateForBuyer(BaseModel):
    car_id: int
    margin_rate: int
    purchase_type: int
    purchase_store_id: int
    business_amount_type: int
    customer_amount_type: int
    list_options: Optional[List[int]]
    options_fee: Optional[int]
    user_id: int
    chassis_number: Optional[str]
    register_sale_id: int


class EstimateUpdateQueryParam(BaseModel):
    assess_request_flg: Optional[int]
    estimate_id: int
    car_id: int
    options_fee: int
    margin_rate: Optional[int]
    user_id: int

