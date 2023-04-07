from typing import Optional, List, Any

from pydantic import BaseModel
from datetime import datetime, date


# Shared properties
from app.schemas.car_equipment_details import CarEquipmentDetailsBase


class CarBase(BaseModel):
    id: Optional[int]
    car_code: Optional[int]
    company_code: Optional[str]
    car_div: Optional[str]
    status: Optional[str]
    market_price: Optional[int]
    car_owner: Optional[str]
    car_decision_maker: Optional[str]
    external_system_type: Optional[str]
    external_system_key1: Optional[str]
    external_system_key2: Optional[str]
    maker: Optional[str]
    maker_origin: Optional[str]
    year: Optional[str]
    car_type: Optional[str]
    car_type_orgin: Optional[str]
    grade: Optional[str]
    grade_origin: Optional[str]
    chassis_number: Optional[str]
    sale_new_old_car_type: Optional[str]
    purchase_intention: Optional[str]
    transfer_intention_status: Optional[str]
    transfer_intention_updater: Optional[str]
    transfer_intention_updatetime: Optional[datetime]
    information_pattern: Optional[str]
    information_type: Optional[str]
    information_id: Optional[int]
    register_staff_code: Optional[str]
    register_store_code: Optional[str]
    car_mileage: Optional[int]
    car_mileage_registration_date: Optional[date]
    car_mileage_inspection_datetime: Optional[datetime]
    land_transport_office: Optional[str]
    car_registration_number_type: Optional[str]
    car_registration_number_kana: Optional[str]
    car_registration_number: Optional[str]
    registration_first_date: Optional[date]
    registration_first_date_origin: Optional[date]
    registration_start_date: Optional[date]
    registration_end_date: Optional[date]
    active_flag: Optional[int]
    guide_availability_sms: Optional[int]
    guide_availability_dm: Optional[int]
    guide_availability_call: Optional[int]
    guide_availability_line: Optional[int]
    guide_availability_email: Optional[int]
    hide_flag: Optional[int]
    repair_history_flag: Optional[int]
    number_of_offer: Optional[int]
    sales_period_start: Optional[str]


# Property to query
class CarQueryBase(BaseModel):
    store_id: Optional[str]
    price_from: Optional[int]
    price_to: Optional[int]
    mode: Optional[int]
    car_status: Optional[List[int]]
    color_name: Optional[List[str]]
    car_mileage_from: Optional[int]
    car_mileage_to: Optional[int]
    prefectures: Optional[List[str]]
    registration_first_date_from: Optional[int]
    registration_first_date_to: Optional[int]
    maker: Optional[str]
    car_type: Optional[str]
    grade: Optional[str]
    contacting: Optional[int]

class CarQuery(CarQueryBase):
    return_total: Optional[int]
    show_total_all: Optional[bool] = False
    new_arrival: Optional[int]
    new_contact: Optional[int]
    sort_header: Optional[Any]
    company_code: Optional[str]
    store_code: Optional[str]
    transfer_hope: Optional[int]
    transfer_alert: Optional[int]
    register_sale_type: Optional[List[int]]
    private_business: Optional[List[int]]

# Properties to receive on item creation
class CarCreate(CarBase):
    car_code: int
    company_code: str
    car_div: str
    status: str
    market_price: int
    car_owner: str
    car_decision_maker: str
    external_system_type: str
    external_system_key1: str
    external_system_key2: str
    maker: str
    maker_origin: str
    year: str
    car_type: str
    car_type_orgin: str
    grade: str
    grade_origin: str
    chassis_number: str
    sale_new_old_car_type: str
    purchase_intention: str
    transfer_intention_status: str
    transfer_intention_updater: str
    transfer_intention_updatetime: str
    information_pattern: str
    information_type: str
    information_id: int
    register_staff_code: str
    register_store_code: str
    car_mileage: int
    car_mileage_registration_date: date
    car_mileage_inspection_datetime: Optional[datetime]
    land_transport_office: str
    car_registration_number_type: str
    car_registration_number_kana: str
    car_registration_number: str
    registration_first_date: date
    registration_first_date_origin: date
    registration_start_date: date
    registration_end_date: date
    active_flag: int
    guide_availability_sms: int
    guide_availability_dm: int
    guide_availability_call: int
    guide_availability_line: int
    guide_availability_email: int
    hide_flag: int
    repair_history_flag: int
    sales_period_start: str


# Properties to receive on item update
class CarUpdate(CarBase):
    pass


# Properties shared by models stored in DB
class CarInDBBase(CarBase):
    id: Optional[int]
    car_code: Optional[int]
    company_code: Optional[str]
    car_div: Optional[str]
    status: Optional[str]
    market_price: Optional[int]
    car_owner: Optional[str]
    car_decision_maker: Optional[str]
    external_system_type: Optional[str]
    external_system_key1: Optional[str]
    external_system_key2: Optional[str]
    maker: Optional[str]
    maker_origin: Optional[str]
    year: Optional[str]
    car_type: Optional[str]
    car_type_orgin: Optional[str]
    grade: Optional[str]
    grade_origin: Optional[str]
    chassis_number: Optional[str]
    sale_new_old_car_type: Optional[str]
    purchase_intention: Optional[str]
    transfer_intention_status: Optional[str]
    transfer_intention_updater: Optional[str]
    transfer_intention_updatetime: Optional[datetime]
    information_pattern: Optional[str]
    information_type: Optional[str]
    information_id: Optional[int]
    register_staff_code: Optional[str]
    register_store_code: Optional[str]
    car_mileage: Optional[int]
    car_mileage_registration_date: Optional[date]
    car_mileage_inspection_datetime: Optional[datetime]
    land_transport_office: Optional[str]
    car_registration_number_type: Optional[str]
    car_registration_number_kana: Optional[str]
    car_registration_number: Optional[str]
    registration_first_date: Optional[date]
    registration_first_date_origin: Optional[date]
    registration_start_date: Optional[date]
    registration_end_date: Optional[date]
    active_flag: Optional[int]
    guide_availability_sms: Optional[int]
    guide_availability_dm: Optional[int]
    guide_availability_call: Optional[int]
    guide_availability_line: Optional[int]
    guide_availability_email: Optional[int]
    hide_flag: Optional[int]
    repair_history_flag: Optional[int]
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
class Car(CarInDBBase):
    pass


# Properties properties stored in DB
class CarInDB(CarInDBBase):
    pass

class CarResponse(BaseModel):
    id: Optional[int]
    company_code: Optional[str]
    status: Optional[str]
    maker: Optional[str]
    year: Optional[str]
    car_type: Optional[str]
    grade: Optional[str]
    purchase_intention: Optional[str]
    car_mileage: Optional[int]
    registration_first_date: Optional[date]
    registration_start_date: Optional[date]
    registration_end_date: Optional[date]
    insert_at: Optional[datetime]


# Get information of owner of the car in detail car screen
class CustomerInfoInCarDetail(BaseModel):
    face_photo: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    last_name_kana: Optional[str]
    first_name_kana: Optional[str]
    birthday: Optional[date]
    active_status: Optional[int]
    rank: Optional[int]
    sex: Optional[str]
    vip: Optional[int]
    zip_code: Optional[str]
    prefectures_code: Optional[str]
    prefectures_name: Optional[str]
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    phone_number: Optional[str]
    cellphone_number: Optional[str]
    email: Optional[str]
    optin_times_weekdays_from9: Optional[int]
    optin_times_weekdays_from12: Optional[int]
    optin_times_weekdays_from18: Optional[int]
    optin_times_holidays_from9: Optional[int]
    optin_times_holidays_from12: Optional[int]
    optin_times_holidays_from18: Optional[int]
    guide_availability_sms: Optional[int]
    guide_availability_dm: Optional[int]
    guide_availability_call: Optional[int]
    guide_availability_line: Optional[int]
    guide_availability_email: Optional[int]
    private_business: Optional[str]
    license_color: Optional[str]
    car_life_code: Optional[List[str]]


# Get information of the car in detail car screen
class CarFullDetail(BaseModel):
    customer_info: Optional[CustomerInfoInCarDetail]
    car_equipment_details: Optional[CarEquipmentDetailsBase]
    store_code: Optional[str]
    car_status: Optional[int]
    car_status_desc: Optional[str]
    car_active_status: Optional[int]
    aggregation_maker: Optional[str]
    chassis_number: Optional[str]
    grade: Optional[str]
    car_type: Optional[str]
    maker: Optional[str]
    aggregation_car_type: Optional[str]
    aggregation_grade: Optional[str]
    land_transport_office: Optional[str]
    car_registration_number: Optional[str]
    car_registration_number_kana: Optional[str]
    car_registration_number_type: Optional[str]
    registration_first_date: Optional[date]
    registration_end_date: Optional[date]
    registration_start_date: Optional[date]
    purchase_intention: Optional[str]
    color_name: Optional[str]
    prefectures_cd: Optional[str]
    car_private_business: Optional[str]
    view_cnt: Optional[int]
    car_mileage: Optional[int]
    car_mileage_inspection_datetime: Optional[datetime]
    battery_status: Optional[str]
    battery_status_inspection_datetime: Optional[datetime]
    battery_size: Optional[str]
    battery_create_date: Optional[date]
    battery_size_inspection_datetime: Optional[datetime]
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
    engine_oil_status: Optional[str]
    engine_oil_status_inspection_datetime: Optional[datetime]
    brake_fluid_status: Optional[str]
    brake_fluid_status_inspection_datetime: Optional[datetime]
    wiper_status: Optional[str]
    wiper_status_inspection_datetime: Optional[datetime]
    lamp_status: Optional[str]
    lamp_status_inspection_datetime: Optional[datetime]
    firebase_chat_id: Optional[str]
    message_unread_cnt: Optional[str]
    aggregation_wholesale_price_market: Optional[float]
    car_category: Optional[str]
    purpose: Optional[str]
    car_shape: Optional[str]
    passenger_capacity: Optional[str]
    maximum_payload: Optional[str]
    car_weight: Optional[str]
    car_total_weight: Optional[str]
    car_length: Optional[str]
    car_width: Optional[str]
    car_height: Optional[str]
    tire_grooves_front_r: Optional[str]
    tire_grooves_rear_r: Optional[str]
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
    div: Optional[int]
    hope_sale_base_price_tax: Optional[int]
    period_to: Optional[datetime]
    negotiation_status: Optional[int]
    register_sale_status: Optional[int]
    register_sale_type: Optional[int]
    negotiation_store_id: Optional[int]
    assess_status: Optional[int]
    assess_id: Optional[int]
    favorite_cnt: Optional[int]
    contact_cnt: Optional[int]
    transfer_total_amount_tax: Optional[int]
    platform_fee_tax: Optional[int]
    brokerage_fee_tax: Optional[int]
    new_car_price: Optional[float]
    engine_coolant_status: Optional[str]
    engine_coolant_status_inspection_datetime: Optional[datetime]
    at_ctv_field_status: Optional[str]
    at_ctv_field_status_inspection_datetime: Optional[datetime]
    register_sale_id: Optional[int]
    negotiation_id: Optional[int]
    negotiation_period_to: Optional[datetime]
    negotiation_period_from: Optional[datetime]
    aggregation_wholesale_price_low: Optional[float]
    aggregation_wholesale_price_high: Optional[float]
    hope_sale_base_price: Optional[int]
    aggregation_retail_price_high: Optional[float]
    aggregation_retail_price_low: Optional[float]
    aggregation_retail_price_middle: Optional[float]
    aggregation_retail_price_market: Optional[float]
    prefectures_name: Optional[str]
    one_onwer_flg: Optional[int]
    no_smoking_car_flg: Optional[int]
    garage: Optional[str]
    periodic_inspection_record_book: Optional[int]
    registered_car_flg: Optional[int]
    import_type: Optional[int]
    dealer_car_flg: Optional[int]
    body_type: Optional[str]
    drive: Optional[str]
    handle_type: Optional[int]
    shift: Optional[str]
    seats_cnt: Optional[int]
    fuel: Optional[str]
    fuel_economy: Optional[str]
    tire_type: Optional[str]
    cold_region_spec: Optional[int]
    door_number: Optional[int]
    key_cnt: Optional[int]
    check_car: Optional[str]
    decade_age: Optional[str]
    customer_market_license_color: Optional[str]
    car_market_displacement_power: Optional[str]
    company_code: Optional[str]
    car_code: Optional[str]
    hide_flag: Optional[int]
    overall_evaluation: Optional[int]
    interior_evaluation: Optional[int]
    exterior_evaluation: Optional[int]
    repair_history_flag: Optional[int]

class CarInfo(BaseModel):
    Car: CarResponse
    period_from: Optional[datetime]
    period_to: Optional[datetime]
    hope_sale_base_price: Optional[int]
    price_type: Optional[int]
    prefectures_cd: Optional[str]
    assess_status: Optional[int]
    color_name: Optional[str]
    car_status: Optional[str]
    price_by_carstatus: Optional[float]
    car_active_status: Optional[int]
    store_code: Optional[str]
    store_id: Optional[int]
    store_name: Optional[str]
    company_name: Optional[str]
    div: Optional[int]
    car_status_desc: Optional[str]
    url: Optional[str]
    hide_flag: Optional[int]

    view_detail_cnt: Optional[int]
    active_status: Optional[str]
    car_final_status: Optional[int]
    contact_cnt: Optional[int]
    total_unread_cnt: Optional[int]
    last_message_datetime: Optional[datetime]
    favorite_cnt: Optional[int]

    aggregation_retail_price_market: Optional[float]
    negotiation_status: Optional[int]
    negotiation_period_from: Optional[datetime]
    negotiation_period_to: Optional[datetime]
    register_sale_type: Optional[int]
    private_business: Optional[int]

    class Config:
        orm_mode = True


class CarSearchResponse(BaseModel):
    total: Optional[int]
    results: Optional[List[CarInfo]]
