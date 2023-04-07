from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.register_sale import RegisterSale


# Shared properties
class CarMarketBase(BaseModel):
    car_id: Optional[int]
    car_status: Optional[str]
    store_code: Optional[str]
    car_status_active: Optional[int]
    offer_cnt: Optional[int]
    market_price: Optional[int]
    prefectures_cd: Optional[str]
    hide_flag: Optional[int]
    repair_history_flag: Optional[int]
    duplication_flg: Optional[int]
    displacement_power: Optional[str]
    car_shape: Optional[str]
    door_number: Optional[int]
    has_sr: Optional[int]
    has_navi: Optional[int]
    maintenance: Optional[str]
    rating_score: Optional[str]
    interior: Optional[str]
    drive: Optional[str]
    shift: Optional[str]
    body_type: Optional[str]
    color_name: Optional[str]
    new_car_price: Optional[float]


# Properties to receive on item creation
class CarMarketCreate(CarMarketBase):
    pass


# Properties to query
class CarMarketQuery(CarMarketBase):
    pass


# Properties to receive on item update
class CarMarketUpdate(CarMarketBase):
    handle_type: Optional[int]
    has_kawa: Optional[int]
    common_dh: Optional[int]
    change_mode: Optional[str]
    view_detail_cnt: Optional[int]
    like_cnt: Optional[int]


# Properties shared by models stored in DB
class CarMarketInDBBase(CarMarketBase):
    handle_type: Optional[str]
    has_kawa: Optional[int]
    common_dh: Optional[str]
    change_mode: Optional[str]
    color_code: Optional[str]
    view_detail_cnt: Optional[int]
    like_cnt: Optional[int]
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
class CarMarket(CarMarketBase):
    id: Optional[int]
    handle_type: Optional[str]
    has_kawa: Optional[int]
    common_dh: Optional[str]
    color_code: Optional[str]
    view_detail_cnt: Optional[int]
    like_cnt: Optional[int]

    class Config:
        orm_mode = True


# Properties properties stored in DB
class CarMarketInDB(CarMarketInDBBase):
    pass


class UpdateCarStatus(BaseModel):
    car_id: int
    car_status: Optional[int] = None
    register_sale_status: Optional[int] = None
    negotiation_status: Optional[int] = None
    purchase_status: Optional[int] = None



