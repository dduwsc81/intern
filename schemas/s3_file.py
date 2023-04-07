from typing import Optional

from pydantic import BaseModel
from datetime import date,datetime

# Shared properties
class S3FileBase(BaseModel):
    id : Optional[int]
    bucket_name: Optional[str]
    key:  Optional[str]


# Properties to receive on item creation
class S3FileCreate(S3FileBase):
    bucket_name: Optional[str]
    key:  Optional[str]


# Properties to receive on item update
class S3FileUpdate(S3FileBase):
    bucket_name: Optional[str]
    key:  Optional[str]


# Properties shared by models stored in DB
class S3FileInDBBase(S3FileBase):
    id : Optional[int]
    bucket_name: Optional[str]
    key:  Optional[str]
    insert_id : Optional[int]
    insert_at : Optional[datetime]
    update_id : Optional[int]
    update_at : Optional[datetime]
    delete_id : Optional[int]
    delete_at : Optional[datetime]
    delete_flag : Optional[int]
    # owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class S3File(S3FileInDBBase):
    pass


# Properties properties stored in DB
class S3FileInDB(S3FileInDBBase):
    pass