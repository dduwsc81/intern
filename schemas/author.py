from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorBase(BaseModel):
    author_name: str
    author_age: Optional[int]


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorCreate):
    pass


class AuthorInDB(AuthorCreate):
    id: int

    class Config:
        orm_mode = True