from pydantic import BaseModel
from typing import Optional, List


class ServiceInfo(BaseModel):
    serviceCode: str
    deleteFlag: int
    sortNumber: int

# Shared properties
class CompanyInfoBase(BaseModel):
    companyCode: str
    companyName: str
    companyReservationUrl: Optional[str] = None
    storeCode: str
    storeName: str
    displayName: Optional[str] = None
    areaCode: str
    zipCode: Optional[str] = None
    prefecturesCode: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    address3: Optional[str] = None
    phoneNumber: Optional[str] = None
    email: Optional[str] = None
    email2: Optional[str] = None
    email3: Optional[str] = None
    storeReservationUrl: Optional[str] = None
    storeReservationSupplementary: Optional[str] = None
    storeReservationSupplementaryFlag: Optional[int] = None
    activeServices: Optional[List] = None
    serviceList: List[ServiceInfo]


# Properties to receive on item creation
class CompanyInfoCreate(CompanyInfoBase):
    pass


# Properties to receive on item update
class CompanyInfoUpdate(CompanyInfoBase):
    pass


# Properties to return to client
class CompanyInfoStatus(CompanyInfoBase):
    pass
