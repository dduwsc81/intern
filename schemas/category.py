from typing import Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    cat_name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDB(CategoryCreate):
    id: int

    class Config:
        orm_mode = True
