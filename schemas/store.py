from pydantic import BaseModel
from typing import List, Optional


class regularBusinessHours(BaseModel):
    dayOfWeek: int = 99
    openingTime: Optional[str] = None
    closingTime: Optional[str] = None
    restTimeFrom:  Optional[str] = None
    restTimeTo:  Optional[str] = None
    closedDayFlag:  Optional[int] = None


class irregularBusinessHours(BaseModel):
    idIrregularDay: Optional[int] = None
    closedAndReducedHoursDate: Optional[str] = None
    openingTime: Optional[str] = None
    closingTime: Optional[str] = None
    closedDayFlag: Optional[int] = None


# Shared properties
class StoreBase(BaseModel):
    isCopySetting: int
    irregularBusinessHoursDeleted: List[int]
    regularBusinessHours: Optional[List[regularBusinessHours]]
    irregularBusinessHours: Optional[List[irregularBusinessHours]]


# Properties to receive on item creation
class StoreCreate(StoreBase):
    pass


# Properties to receive on item update
class StoreUpdate(StoreBase):
    pass


# Properties to return to client
class StoreStatus(StoreBase):
    pass


class StoreBasic(BaseModel):
    id: Optional[int]
    store_code: Optional[str]
    store_name: Optional[str]


class DisplayStore(BaseModel):
    store_code: Optional[str]
    display_store_flag: Optional[str]

class ListDisplayStore(BaseModel):
    list_display_store_update: Optional[List[DisplayStore]]
