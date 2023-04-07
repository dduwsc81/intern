from typing import Optional

from pydantic import BaseModel
from datetime import date,datetime


# Shared properties
class ChatGroupBase(BaseModel):
    offer_id: Optional[int]
    chassis_number: Optional[str]
    div: Optional[int]
    store_id: Optional[str]
    car_id: Optional[int]

# Properties to receive on item creation
class ChatGroupCreate(ChatGroupBase):
    user_id: Optional[int]


# Properties to receive on item update
class ChatGroupUpdate(BaseModel):
    last_message_user_id: Optional[int]
    last_message_user_name: Optional[str]
    last_message_datetime: Optional[datetime]
    last_message: Optional[str]
    last_message_store_id: Optional[int]


# Properties shared by models stored in DB
class ChatGroupInDBBase(ChatGroupBase):
    id: Optional[int]
    # group_id: Optional[str]
    firebase_chat_id: Optional[str]
    insert_id : Optional[int]
    insert_at : Optional[datetime]
    update_id : Optional[int]
    update_at : Optional[datetime]
    delete_id : Optional[int]
    delete_at : Optional[datetime]
    delete_flag : Optional[int]
    message_total_cnt: Optional[int]
    message_unread_cnt: Optional[int]
    last_message_user_id: Optional[int]
    last_message_user_name: Optional[str]
    last_message_datetime: Optional[datetime]
    last_message: Optional[str]
    last_message_store_id: Optional[int]
    class Config:
        orm_mode = True


# Properties to return to client
class ChatGroup(ChatGroupInDBBase):
    store_name: Optional[str]
    company_name: Optional[str]
    token: Optional[str]
    store_code: Optional[str]
    company_code: Optional[str]
    store_code_store: Optional[str]
    company_code_store: Optional[str]
    store_name_store: Optional[str]
    company_name_store: Optional[str]


# Properties properties stored in DB
class ChatGroupForBuyer(ChatGroupBase):
    id: Optional[int]
    negotiation_id: Optional[int]
    message_total_cnt: Optional[int]
    message_unread_cnt: Optional[int]
    last_message_user_id: Optional[int]
    last_message_user_name: Optional[str]
    last_message_datetime: Optional[datetime]
    last_message: Optional[str]
    last_message_store_id: Optional[int]
    firebase_chat_id: Optional[str]
    store_name: Optional[str]
    company_name: Optional[str]

class ChatGroupMemeber(BaseModel):
    staff_code: Optional[str]
    user_id: Optional[int]
