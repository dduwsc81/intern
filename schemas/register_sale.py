from typing import Optional, List

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class RegisterSaleBase(BaseModel):
    car_id: Optional[int]
    company_code: Optional[str]
    register_sale_type: Optional[int]
    period_from: Optional[datetime]
    period_to: Optional[datetime]

    hope_sale_base_price: Optional[int]
    hope_sale_total_price: Optional[int]
    buy_now_base_price: Optional[int]
    buy_now_total_price: Optional[int]

    hope_sale_base_price_tax: Optional[int]
    hope_sale_total_price_tax: Optional[int]
    buy_now_base_price_tax: Optional[int]
    buy_now_total_price_tax: Optional[int]

    price_type: Optional[int]
    cust_agree_flg: Optional[int]
    register_sale_status: Optional[int]
    assess_request_flg: Optional[int]
    assess_id: Optional[int]
    assess_status: Optional[int]
    assess_user_id: Optional[int]
    assess_price: Optional[int]
    approve_user_id: Optional[int]
    assess_comment: Optional[str]
    assess_datetime: Optional[datetime]


# Properties to receive on item creation
class RegisterSaleCreate(RegisterSaleBase):
    pass


# Properties to receive on item update
class RegisterSaleUpdate(RegisterSaleBase):
    pass


# Properties shared by models stored in DB
class RegisterSaleInDBBase(RegisterSaleBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    # owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class RegisterSale(RegisterSaleBase):
    id: int

    class Config:
        orm_mode = True


# Properties properties stored in DB
class RegisterSaleInDB(RegisterSaleInDBBase):
    pass


# Search register sale
class RegisterSaleSearch(BaseModel):
    company_name: Optional[str]
    store_name: Optional[str]
    maker: Optional[str]
    car_type: Optional[str]
    grade: Optional[str]
    sales_period_start_from: Optional[str]
    sales_period_start_to: Optional[str]
    period_from: Optional[str]
    period_to: Optional[str]
    assess_status: Optional[List[int]]
    car_inspection_type: Optional[str]
    registration_first_date: Optional[str]
    show_total_all: Optional[int]
    car_id: Optional[int]
    company_code: Optional[str]


# update status registersale
class RegisterSaleUpdateStatus(BaseModel):
    assess_status: Optional[int]
    assess_comment: Optional[str]


# Return list register sale
class ListRegisterSale(BaseModel):
    total: Optional[int] = 0
    result: Optional[List[RegisterSale]]

    class Config:
        orm_mode = True


class RegisterSaleUpdateAssess(BaseModel):
    register_sale_id: Optional[int]
    assess_status: Optional[int]
    user_id: Optional[int]
