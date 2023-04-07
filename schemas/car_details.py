from typing import Optional

from pydantic import BaseModel
from datetime import datetime, date


# Shared properties
class CarDetailsBase(BaseModel):
    car_id: Optional[int]
    car_code: Optional[int]
    company_code: Optional[str]
    car_inspection_type: Optional[str]
    engine_type: Optional[str]
    engine_maximum_output: Optional[str]
    engine_torque: Optional[str]
    tire_status: Optional[str]
    tire_status_inspection_datetime: Optional[datetime]
    tire_size_rear: Optional[str]
    tire_size_front: Optional[str]
    tire_size_inspection_datetime: Optional[datetime]
    tire_create_year: Optional[str]
    tire_create_week: Optional[str]
    tire_create_year_week_inspection_datetime: Optional[datetime]
    tire_grooves_front: Optional[str]
    tire_grooves_rear: Optional[str]
    tire_grooves_inspection_datetime: Optional[datetime]
    fuel_tank_size: Optional[str]
    battery_status: Optional[str]
    battery_status_inspection_datetime: Optional[datetime]
    battery_size: Optional[str]
    battery_create_date: Optional[date]
    battery_size_inspection_datetime: Optional[datetime]
    color_code_type: Optional[str]
    color_trim_code_type: Optional[str]
    model: Optional[str]
    sales_period_start: Optional[str]
    warranty_period_end: Optional[str]
    fuel_economy_jc08: Optional[str]
    car_weight: Optional[str]
    car_full_length: Optional[str]
    car_full_width: Optional[str]
    car_total_height: Optional[str]
    engine_oil_status: Optional[str]
    engine_oil_status_inspection_datetime: Optional[datetime]
    brake_fluid_status: Optional[str]
    brake_fluid_status_inspection_datetime: Optional[datetime]
    engine_coolant_status: Optional[str]
    engine_coolant_status_inspection_datetime: Optional[datetime]
    at_ctv_field_status: Optional[str]
    at_ctv_field_status_inspection_datetime: Optional[datetime]
    wiper_status: Optional[str]
    wiper_status_inspection_datetime: Optional[datetime]
    lamp_status: Optional[str]
    lamp_status_inspection_datetime: Optional[datetime]
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
    area: Optional[str]
    color_name: Optional[str]
    common_name: Optional[str]
    has_kawa: Optional[int]
    has_DH: Optional[int]
    handle_type: Optional[int]
    change_mode: Optional[str]


# Properties to receive on item creation
class CarDetailsCreate(CarDetailsBase):
    pass


# Properties to receive on item update
class CarDetailsUpdate(CarDetailsBase):
    pass


# Properties shared by models stored in DB
class CarDetailsInDBBase(CarDetailsBase):
    id: int
    car_id: Optional[int]
    car_code: Optional[int]
    company_code: Optional[str]
    car_inspection_type: Optional[str]
    engine_type: Optional[str]
    engine_maximum_output: Optional[str]
    engine_torque: Optional[str]
    tire_status: Optional[str]
    tire_status_inspection_datetime: Optional[datetime]
    tire_size_rear: Optional[str]
    tire_size_front: Optional[str]
    tire_size_inspection_datetime: Optional[datetime]
    tire_create_year: Optional[str]
    tire_create_week: Optional[str]
    tire_create_year_week_inspection_datetime: Optional[datetime]
    tire_grooves_front: Optional[str]
    tire_grooves_rear: Optional[str]
    tire_grooves_inspection_datetime: Optional[datetime]
    fuel_tank_size: Optional[str]
    battery_status: Optional[str]
    battery_status_inspection_datetime: Optional[datetime]
    battery_size: Optional[str]
    battery_create_date: Optional[date]
    battery_size_inspection_datetime: Optional[datetime]
    color_code_type: Optional[str]
    color_trim_code_type: Optional[str]
    model: Optional[str]
    sales_period_start: Optional[str]
    warranty_period_end: Optional[str]
    fuel_economy_jc08: Optional[str]
    car_weight: Optional[str]
    car_full_length: Optional[str]
    car_full_width: Optional[str]
    car_total_height: Optional[str]
    engine_oil_status: Optional[str]
    engine_oil_status_inspection_datetime: Optional[datetime]
    brake_fluid_status: Optional[str]
    brake_fluid_status_inspection_datetime: Optional[datetime]
    engine_coolant_status: Optional[str]
    engine_coolant_status_inspection_datetime: Optional[datetime]
    at_ctv_field_status: Optional[str]
    at_ctv_field_status_inspection_datetime: Optional[datetime]
    wiper_status: Optional[str]
    wiper_status_inspection_datetime: Optional[datetime]
    lamp_status: Optional[str]
    lamp_status_inspection_datetime: Optional[datetime]
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
    area: Optional[str]
    color_name: Optional[str]
    common_name: Optional[str]

    has_kawa: Optional[int]
    has_DH: Optional[int]
    handle_type: Optional[int]
    change_mode: Optional[str]

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
class CarDetails(CarDetailsInDBBase):
    pass


# Properties properties stored in DB
class CarDetailsInDB(CarDetailsInDBBase):
    pass