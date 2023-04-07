from datetime import date
from typing import Optional

from pydantic import BaseModel


class BookBase(BaseModel):
    book_name: str
    book_description: Optional[str]


class BookCreate(BookBase):
    created_at: date
    author_id: int
    cat_id: int


class BookUpdate(BookCreate):
    pass


class BookInDB(BookCreate):
    id: int

    class Config:
        orm_mode = True
