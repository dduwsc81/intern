from typing import Optional, Text, List, Dict

from pydantic import BaseModel
from datetime import datetime, time, date


# Shared properties
class SurveyUrlSettingBase(BaseModel):
    company_code: Optional[str]
    store_code: Optional[str]
    service_code: Optional[str]
    menu_id: Optional[str]


# Properties to receive on item creation
class SurveyUrlSettingCreate(SurveyUrlSettingBase):
    pass
