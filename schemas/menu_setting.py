from typing import Optional, List

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class MenuSettingBase(BaseModel):
    code_type_id: Optional[int]
    menu_name: Optional[str]
    from_store_code: Optional[str]
    from_company_code: Optional[str]
    menu_user_price: Optional[int]
    menu_send_incentive: Optional[int]
    menu_fg_incentive: Optional[int]
    incentive_flag: Optional[int]
    menu_content: Optional[str]
    menu_time_require: Optional[int]
    reservation_data_type: Optional[int]
    paid_type: Optional[int]
    specify_location: Optional[int]
    send_email_flag: Optional[int]
    schedule_consult_flag: Optional[int]
    policy_type: Optional[str]
    policy_content: Optional[str]
    terms_type: Optional[str]
    terms_content: Optional[str]
    policy_pdf_file_name: Optional[str]
    term_pdf_file_name: Optional[str]
    menu_candidate_time: Optional[str]
    email_optional_flag: Optional[int]
    hide_checkout_language: Optional[int]
    hide_store_information: Optional[int]
    calendar_selection_detail: Optional[str]
    schedule_consultation_detail: Optional[str]


# Properties to receive on item creation
class MenuSettingCreate(MenuSettingBase):
    menu_link_store: Optional[list]
    shortest_available_day: Optional[int]
    customer_guide_flag: Optional[int] = 0
    send_email_flag: Optional[int]
    schedule_consult_flag: Optional[int]

# Properties to receive on item update
class MenuSettingUpdate(MenuSettingBase):
    menu_link_store: Optional[list]
    shortest_available_day: Optional[int]
    customer_guide_flag: Optional[int] = 0
    send_email_flag: Optional[int]
    schedule_consult_flag: Optional[int]

# Properties shared by models stored in DB
class MenuSettingInDBBase(MenuSettingBase):
    id: Optional[int]

    code_type_id: Optional[int]
    reservation_data_type: Optional[int]
    paid_type: Optional[int]

    menu_name: Optional[str]
    menu_content: Optional[str]
    menu_user_price: Optional[int]
    menu_send_incentive: Optional[int]
    menu_fg_incentive: Optional[int]
    incentive_flag: Optional[int]
    menu_time_require: Optional[int]
    specify_location: Optional[int]
    shortest_available_day: Optional[int]

    from_store_code: Optional[str]
    from_company_code: Optional[str]
    customer_guide_flag: Optional[int]

    send_email_flag: Optional[int]
    schedule_consult_flag: Optional[int]
    hide_checkout_language: Optional[int]
    hide_store_information: Optional[int]
    calendar_selection_detail: Optional[str]
    schedule_consultation_detail: Optional[str]

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
class MenuSetting(MenuSettingInDBBase):
    pass


# Properties properties stored in DB
class MenuSettingInDB(MenuSettingInDBBase):
    pass


# Shared properties
class MenuSettingRequest(BaseModel):
    code_type_id: Optional[int] = None
    store_code: Optional[str] = None
    company_code: Optional[str] = None


# properties Response
class MenuSettingResponse(BaseModel):
    id: int

    code_type_id: Optional[int]
    reservation_data_type: Optional[int]

    code_type_name: Optional[str]
    menu_name: Optional[str]
    menu_content: Optional[str]
    menu_user_price: Optional[int]
    menu_send_incentive: Optional[int]
    menu_fg_incentive: Optional[int]
    incentive_flag: Optional[int]
    menu_time_require: Optional[int]
    specify_location: Optional[int]
    shortest_available_day: Optional[int]
    paid_type: Optional[int]

    has_group: Optional[bool]
    company_store_info: List[Optional[dict]]
    customer_guide_flag: Optional[int]
    send_email_flag: Optional[int]
    schedule_consult_flag: Optional[int]
    policy_type: Optional[str]
    policy_content: Optional[str]
    terms_type: Optional[str]
    terms_content: Optional[str]
    policy_file: Optional[str]
    terms_file: Optional[str]
    policy_pdf_file_name: Optional[str]
    term_pdf_file_name: Optional[str]
    menu_candidate_time: List[Optional[int]]
    email_optional_flag: Optional[int]
    hide_checkout_language: Optional[int]
    hide_store_information: Optional[int]
    calendar_selection_detail: Optional[str]
    schedule_consultation_detail: Optional[str]
