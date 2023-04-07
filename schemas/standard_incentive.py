from typing import Optional

from pydantic import BaseModel


# Shared properties
class StandardIncentiveBase(BaseModel):
    id: Optional[int]
    code_type_id: Optional[int]
    send_incentive_standard_tax: Optional[int]
    fg_incentive_standard_tax: Optional[int]


# Properties shared by models stored in DB
class StandardIncentiveInDBBase(StandardIncentiveBase):
    pass

    class Config:
        orm_mode = True


# Properties to return to client
class StandardIncentive(StandardIncentiveInDBBase):
    pass


