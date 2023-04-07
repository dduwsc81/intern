from pydantic import BaseModel
from typing import Optional


# Shared properties
class ReservationUrlBase(BaseModel):
    carCode: Optional[str] = ""
    mailAddress:  Optional[str] = ""
    carName: Optional[str] = ""
    serviceType: Optional[str] = ""
    lastName:  Optional[str] = ""
    firstName:  Optional[str] = ""
    externalType:  Optional[str] = ""
    storeCode:  Optional[str] = ""
    customerCode: Optional[str] = ""
    attractingType:  Optional[str] = None
    attractingId: Optional[int] = None
    attractingCustomersType: Optional[str] = ""
    catalogKey: Optional[str] = None
    catalogUrl: Optional[str] = None


# Properties to receive on item creation
class ReservationUrlCreate(ReservationUrlBase):
    pass


# Properties to receive on item update
class ReservationUrlUpdate(ReservationUrlBase):
    pass


# Properties to return to client
class ReservationUrlStatus(ReservationUrlBase):
    pass
