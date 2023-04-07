from pydantic import BaseModel
from typing import Optional


# Shared properties
class CompanyPolicyBase(BaseModel):
    companyCode: Optional[str] = None
    privacyPolicyType: Optional[str] = None
    privacyPolicyContent: Optional[str] = None
    displayNameCompany: Optional[str] = None


# Properties to receive on item creation
class CompanyPolicyCreate(CompanyPolicyBase):
    pass


# Properties to receive on item update
class CompanyPolicyUpdate(CompanyPolicyBase):
    pass


# Properties to return to client
class CompanyPolicyStatus(CompanyPolicyBase):
    pass
