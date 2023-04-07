from datetime import datetime
from typing import Optional
from fastapi import File
from pydantic import BaseModel


# Shared properties
class CompanyInfoSettingBase(BaseModel):
    company_code: Optional[str]
    s3_file_id: Optional[int]
    sender_name: Optional[str]
    sender_mail: Optional[str]
    hidden_company_name: Optional[int]

# Properties to receive on item creation
class CompanyInfoSettingCreate(CompanyInfoSettingBase):
    pass


# Properties to receive on item update
class CompanyInfoSettingUpdate(BaseModel):
    sender_name: Optional[str]
    sender_mail: Optional[str]
    company_name_display: Optional[str]
    is_delete_logo: Optional[int] = None
    hidden_company_name: Optional[int]


# Properties shared by models stored in DB
class CompanyInfoSettingInDBBase(CompanyInfoSettingBase):
    id: Optional[int]
    company_name: Optional[str]
    company_name_display: Optional[str]
    sender_name: Optional[str]
    sender_mail: Optional[str]
    hidden_company_name: Optional[int]
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
class CompanyInfoSetting(CompanyInfoSettingInDBBase):
    pass


# Properties properties stored in DB
class CompanyInfoSettingInDB(CompanyInfoSettingInDBBase):
    pass


# Properties response company information
class ResponseCompanyInfoSettingInfo(BaseModel):
    company_code: Optional[str]
    company_name: Optional[str]
    company_name_display: Optional[str]
    company_logo: Optional[str]
    sender_name: Optional[str]
    sender_mail: Optional[str]
    hidden_company_name: Optional[int]
