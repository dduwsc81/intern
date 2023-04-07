from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime

# Shared properties
class MPrefecturesBase(BaseModel):
    prefectures_code: Optional[str]
    name: Optional[str]
    name_kana: Optional[str]
    sort_number: Optional[str]

# Properties to receive on item creation
class MPrefecturesCreate(MPrefecturesBase):
    pass


# Properties to receive on item update
class MPrefecturesUpdate(MPrefecturesBase):
    pass


# Properties shared by models stored in DB
class MPrefecturesInDBBase(MPrefecturesBase):
    id: int
    prefectures_code: Optional[str]
    name: Optional[str]
    name_kana: Optional[str]
    sort_number: Optional[str]
    province_id: Optional[int]

# Properties to return to client
class MPrefectures(MPrefecturesInDBBase):
    pass


# Properties properties stored in DB
class MPrefecturesInDB(MPrefecturesInDBBase):
    pass
