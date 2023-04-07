from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


class CarTrainingBase(BaseModel):
    reservation_id: Optional[int]
    company_code: Optional[str]
    store_code: Optional[str]
    customer_code: Optional[str]
    car_code: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    last_name_kana: Optional[str]
    first_name_kana: Optional[str]
    birthday: Optional[date]
    phone_number: Optional[str]
    cellphone_number: Optional[str]
    car_maker: Optional[str]
    car_type: Optional[str]
    car_number: Optional[str]
    car_registration_end_date: Optional[date]
    reservation_data_type: Optional[str]
    reservation_menu: Optional[str]
    reservation_datetime: Optional[datetime]
    reservation_datetime_to: Optional[datetime]
    reservation_classification: Optional[str]
    store_name: Optional[str]
    reservation_memo: Optional[str]
    reservation_substitute_car_hope: Optional[str]
    attracting_status: Optional[str]
    attracting_type: Optional[str]
    attracting_registration_end_date: Optional[date]
    customer_staff_main_name: Optional[str]
    staff_code_in_charge: Optional[str]
    registered_source_type: Optional[str]
    remarks_1: Optional[str]
    remarks_2: Optional[str]
    remarks_3: Optional[str]
    remarks_4: Optional[str]
    remarks_5: Optional[str]
    vip: Optional[int]
    rank: Optional[int]
    work_request_form_no: Optional[str]
    work_request_form_name: Optional[str]
    release_date: Optional[date]
    input_date: Optional[date]
    output_date: Optional[date]
    car_mileage: Optional[int]
    car_mileage_inspection_datetime: Optional[datetime]
    chassis_number: Optional[str]
    store_manager: Optional[str]
    update_staff: Optional[str]
    insert_staff: Optional[str]
    representative_fax_number: Optional[str]
    insert_id: int
    insert_at: datetime
    update_id: int
    update_at: datetime
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: int


class CarTrainingCreate(CarTrainingBase):
    pass


class CarTrainingUpdate(CarTrainingBase):
    pass


class CarTrainingInDB(CarTrainingBase):
    id: int

    class Config:
        orm_mode: True
