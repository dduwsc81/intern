from typing import Optional, List

from pydantic import BaseModel
from datetime import date, datetime

# Shared properties
class OfferBase(BaseModel):
    car_id : int
    # company_code : Optional[str]
    register_sale_id : Optional[int]
    # offer_out_user_id : Optional[int]
    offer_out_store_id : Optional[str]
    # offer_in_user_id : Optional[int]
    offer_in_store_id : Optional[str]
    offer_status : Optional[int]
    hope_purchase_price : Optional[int]
    # chat_channel_id : Optional[str]
    # chat_group_id : Optional[str]

# Properties to receive on item creation
class OfferCreate(OfferBase):
    pass


# Properties to receive on item update
class OfferUpdate(OfferBase):
    pass


# Properties shared by models stored in DB
class OfferInDBBase(OfferBase):
    id : int 
    car_id : int
    # company_code : Optional[str]
    register_sale_id : Optional[int]
    # offer_out_user_id : Optional[int]
    offer_out_store_id : Optional[str]
    # offer_in_user_id : Optional[int]
    offer_in_store_id : Optional[str]
    offer_status : Optional[int]
    hope_purchase_price : Optional[int]
    # chat_channel_id : Optional[str]
    # chat_group_id : Optional[str]
    insert_id : Optional[int]
    insert_at : Optional[datetime]
    update_id : Optional[int]
    update_at : Optional[datetime]
    delete_id : Optional[int]
    delete_at : Optional[datetime]
    delete_flag : Optional[int]
    class Config:
        orm_mode = True


# Properties to return to client
class Offer(OfferInDBBase):
    pass


# Properties properties stored in DB
class OfferInDB(OfferInDBBase):
    pass


# Update status
class OfferUpdateStatus(BaseModel):
    offer_status: Optional[int]
    offer_in_store_id: Optional[str]
    purchase_comment: Optional[str]


# Property to query
class OfferQuery(BaseModel):
    maker: Optional[str]
    car_type: Optional[str]
    grade: Optional[str]
    car_mileage_from: Optional[int]
    car_mileage_to: Optional[int]
    offer_status: List[Optional[int]]
    sales_period_start_from: Optional[str]
    sales_period_start_to: Optional[str]
    buy_now_total_price_from: Optional[int]
    buy_now_total_price_to: Optional[int]
    aggregation_wholesale_price_market_from: Optional[int]
    aggregation_wholesale_price_market_to: Optional[int]
    registration_end_date_from: Optional[str]
    registration_end_date_to: Optional[str]
    area: List[Optional[str]]
    insert_at_from: Optional[str]
    insert_at_to: Optional[str]
    chassis_number: Optional[str]
    car_inspection_type: Optional[str]
    registration_first_date: Optional[str]