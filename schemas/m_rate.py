from typing import Optional

from pydantic import BaseModel
from datetime import datetime, date


# Shared properties
class MRateBase(BaseModel):
    id: Optional[int]
    div: Optional[int]
    rate: Optional[int]
    from_apply_at: Optional[datetime]
    to_apply_at: Optional[datetime]
    apply_company_cd: Optional[str]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class MRateResponse(BaseModel):
    id: Optional[int]
    div: Optional[int]
    rate: Optional[int]
    from_apply_at: Optional[date]
    to_apply_at: Optional[date]
    apply_company_cd: Optional[str]
