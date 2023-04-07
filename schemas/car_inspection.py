from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class CarInspectionBase(BaseModel):
    id: Optional[int]
    car_id: Optional[int]
    company_code: Optional[int]
    car_code: Optional[str]
    car_category: Optional[str]
    purpose: Optional[str]
    private_business: Optional[str]
    car_shape: Optional[str]
    passenger_capacity: Optional[str]
    maximum_payload: Optional[str]
    car_weight: Optional[str]
    car_total_weight: Optional[str]
    car_length: Optional[str]
    car_width: Optional[str]
    car_height: Optional[str]
    front_front_axle_weight: Optional[str]
    front_rear_axle_weight: Optional[str]
    rear_front_axle_weight: Optional[str]
    rear_rear_axle_weight: Optional[str]
    car_inspection_type: Optional[str]
    engine_type: Optional[str]
    displacement_power: Optional[str]
    fuel_type: Optional[str]
    type_number: Optional[str]
    category_number: Optional[str]
    registration_end_date: Optional[date]


class CarInspectionCreate(CarInspectionBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class CarInspectionCreate(CarInspectionBase):
    pass


class CarInspectionInDB(CarInspectionBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True
