from typing import Optional, Text, List, Dict

from pydantic import BaseModel
from datetime import datetime, time, date


# Shared properties
class SendCustomerBase(BaseModel):
    # send_customer_code: Optional[str]
    from_company_code: Optional[str]
    from_store_code: Optional[str]
    from_staff_code: Optional[str]

    customer_code: Optional[str]
    face_photo: Optional[str]
    send_item_type_code: Optional[str]

    customer_last_name: Optional[str]
    customer_first_name: Optional[str]
    customer_last_name_kana: Optional[str]
    customer_first_name_kana: Optional[str]

    customer_phone_number: Optional[str]
    customer_cellphone_number: Optional[str]
    customer_email: Optional[str]
    customer_zip_code: Optional[str]

    customer_prefectures_code: Optional[str]
    car_code: Optional[str]
    car_mileage: Optional[int]

    customer_address1: Optional[str]
    customer_address2: Optional[str]
    customer_address3: Optional[str]

    car_maker: Optional[str]
    car_type: Optional[str]
    car_grade: Optional[str]
    car_registration_number_type: Optional[str]
    car_registration_number_kana: Optional[str]
    car_registration_number: Optional[str]

    car_registration_first_date: Optional[date]
    car_registration_end_date: Optional[date]

    # send_customer_at: Optional[datetime]

    content: Optional[Text]
    reservation_id: Optional[int]


# Properties to receive on item creation
class SendCustomerCreate(SendCustomerBase):
    pass


# Properties to receive on item update
class SendCustomerUpdate(BaseModel):
    status_flag: Optional[int]
    comment: Optional[Text] = None


# Properties to receive on item update
class SendCustomerIncentive(BaseModel):
    fg_incentive_tax: Optional[int]
    send_incentive_tax: Optional[int]


# Properties shared by models stored in DB
class SendCustomerInDBBase(BaseModel):
    id: int
    send_customer_code: Optional[str]
    from_company_code: Optional[str]
    from_store_code: Optional[str]
    from_staff_code: Optional[str]
    to_company_code: Optional[str]
    to_store_code: Optional[str]
    customer_code: Optional[str]
    face_photo: Optional[str]
    send_item_type_code: Optional[str]

    customer_last_name: Optional[str]
    customer_first_name: Optional[str]
    customer_last_name_kana: Optional[str]
    customer_first_name_kana: Optional[str]

    customer_phone_number: Optional[str]
    customer_cellphone_number: Optional[str]
    customer_email: Optional[str]
    customer_zip_code: Optional[str]

    customer_prefectures_code: Optional[str]
    car_code: Optional[str]
    car_mileage: Optional[int]

    customer_address1: Optional[str]
    customer_address2: Optional[str]
    customer_address3: Optional[str]

    car_maker: Optional[str]
    car_type: Optional[str]
    car_grade: Optional[str]
    car_land_transport_office: Optional[str]
    car_registration_number_type: Optional[str]
    car_registration_number_kana: Optional[str]
    car_registration_number: Optional[str]

    car_mileage_registration_date: Optional[date]
    car_registration_first_date: Optional[date]
    car_registration_end_date: Optional[date]

    send_customer_at: Optional[datetime]

    content: Optional[Text]
    send_incentive: Optional[int]
    fg_incentive: Optional[int]
    send_incentive_tax: Optional[int]
    fg_incentive_tax: Optional[int]
    menu_user_price: Optional[int]
    menu_user_price_tax: Optional[int]
    option_user_price: Optional[int]
    option_user_price_tax: Optional[int]
    tax_rate: Optional[int]
    status_flag: Optional[int]
    reservation_id: Optional[int]
    paid_type: Optional[int]
    reservation_time: Optional[str]
    reservation_classification: Optional[str]

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
class SendCustomer(SendCustomerInDBBase):
    send_mail_status: Dict = None
    pass


# Properties properties stored in DB
class SendCustomerInDB(SendCustomerInDBBase):
    pass


# Properties to get list sending request
class SendCustomerSendingRequest(BaseModel):
    send_customer_at_from: Optional[str] = None
    send_customer_at_to: Optional[str] = None
    send_item_type_code: List[Optional[str]] = None
    send_status: List[Optional[int]] = None
    maker: Optional[str] = None
    car_type: Optional[str] = None
    customer_last_name: Optional[str] = None
    customer_first_name: Optional[str] = None
    from_company_name: Optional[str] = None
    from_store_name: Optional[str] = None
    to_company_name: Optional[str] = None
    to_store_name: Optional[str] = None
    car_registration_number: Optional[str] = None


# Properties to  send customer info
class SendCustomerInfo(BaseModel):
    send_customer_at_from: Optional[str]
    send_customer_at_to: Optional[str]


# Properties to get list fg
class SendCustomerFG(BaseModel):
    send_item_type_code: List[Optional[str]] = None
    send_customer_at_from: Optional[str] = None
    send_customer_at_to: Optional[str] = None
    type_status: Optional[int] = None
    from_company_code: Optional[str] = None
    from_store_code: Optional[str] = None
    to_company_code: Optional[str] = None
    to_store_code: Optional[str] = None


# Properties to create send customer chat group
class RequestSendCustomerChatGroup(BaseModel):
    send_customer_id: Optional[int]
    div: Optional[int]
    store_code: Optional[str]
    company_code: Optional[str]


# Properties to response send customer chat group
class ResponseSendCustomerChatGroup(BaseModel):
    firebase_chat_id: Optional[str]
    token_firebase: Optional[str]
