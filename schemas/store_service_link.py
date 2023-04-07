from typing import List, Optional
from pydantic import BaseModel


class WorkingTime(BaseModel):
    sun: Optional[List[str]] = None
    mon: Optional[List[str]] = None
    tue: Optional[List[str]] = None
    wed: Optional[List[str]] = None
    thu: Optional[List[str]] = None
    fri: Optional[List[str]] = None
    sat: Optional[List[str]] = None


class ReservationMenu(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    acceptRequestFrom: Optional[str] = None
    acceptRequestTo: Optional[str] = None
    estimateCost: Optional[str] = None
    timeSlot: Optional[str] = None
    timeSlotAllDay: Optional[str] = None
    locationAtHome: Optional[str] = None
    locationAtStore: Optional[str] = None
    publicOnCm: Optional[str] = None
    publicOnSrExist: Optional[str] = None
    publicOnSrNew: Optional[str] = None
    maximumSlotApply: Optional[str] = None
    sortNumber: Optional[str] = None
    status: Optional[int] = None
    bookingTimeMode: Optional[int] = None
    menuDurationHidden: Optional[int] = None
    workingTime: Optional[WorkingTime] = None
    descriptionSummary: Optional[str] = None
    descriptionDetail: Optional[str] = None
    memoTemplate: Optional[str] = None
    substituteCarDisplay: Optional[int] = None
    acceptCancellation: Optional[int] = 0
    dateBeforeCancellation: Optional[int] = 0


class Data(BaseModel):
    maximumSlot: str
    textColor: str
    backgroundColor: str
    durationTime: str
    sortNumber: int
    deleteFlag: int
    reservationMenu: List[ReservationMenu]


class ServiceData(BaseModel):
    serviceCode: str
    data: Optional[Data]


# Shared properties
class StoreServiceLinkBase(BaseModel):
    serviceData: List[ServiceData]


# Properties to return to client
class StoreService(StoreServiceLinkBase):
    pass


class StoreServiceLinkRequest(StoreServiceLinkBase):
    copySetting: int
