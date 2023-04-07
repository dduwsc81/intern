from typing import Optional

from pydantic import BaseModel
from datetime import date, datetime


# Shared properties
class CodeMasterBase(BaseModel):
    code_type: Optional[str]
    code_value: Optional[int]
    code_name: Optional[str]
    sort_number: Optional[int]


# Properties to receive on item creation
class CodeMasterCreate(CodeMasterBase):
    insert_id: int


# Properties to receive on item update
class CodeMasterUpdate(CodeMasterBase):
    update_id: int


# Properties shared by models stored in DB
class CodeMasterInDBBase(BaseModel):
    id: int
    code_type: Optional[str]
    code_value: Optional[int]
    code_name: Optional[str]
    sort_number: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class CodeMaster(CodeMasterInDBBase):
    pass


# Properties properties stored in DB
class CodeMasterInDB(CodeMasterInDBBase):
    pass