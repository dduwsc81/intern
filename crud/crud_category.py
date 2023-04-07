from typing import List, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import schemas
from app import crud
from app.crud.base import CRUDBase

from app.models.category import Category
from app.schemas.category import CategoryUpdate, CategoryCreate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):

    def create_category(
            self,
            item_in: schemas.CategoryCreate,
            db: Session
    ) -> Any:
        data = jsonable_encoder(item_in)
        item_in_db = Category(**data)
        db.add(item_in_db)
        db.commit()
        db.refresh(item_in_db)
        return item_in_db

    def get_all_category(
            self,
            db: Session
    ) -> Any:
        item_in_db = db.query(self.model).all()
        if len(item_in_db) > 0:
            result = {"Categories": item_in_db}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return result

    def get_category_by_id(
            self,
            cat_id: int,
            db: Session
    ) -> Any:
        item_in_db = db.query(self.model).filter(self.model.id == cat_id).first()
        if not item_in_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found category ID: {cat_id}")
        else:
            result = {f"CategoryID#{cat_id}": item_in_db}
        return result

    def get_book_in_category(
            self,
            cat_id: int,
            db: Session
    ) -> Any:
        data_db = db.query(self.model).filter(self.model.id == cat_id).first()
        books = crud.book.get_book_by_cat_id(cat_id, db)
        data = {"category_info": data_db, "books_in_category": books}
        data = jsonable_encoder(data)
        return data

    def update_category(
            self,
            cat_id: int,
            item_in: schemas.CategoryUpdate,
            db: Session
    ) -> Any:
        item_in_db = db.query(self.model).filter(self.model.id == cat_id).first()
        if item_in_db:
            data = jsonable_encoder(item_in_db)
            if isinstance(item_in, dict):
                update_data = item_in
            else:
                update_data = item_in.dict()

            for field in data:
                if field in update_data:
                    setattr(item_in_db, field, update_data[field])

            db.add(item_in_db)
            db.commit()
            db.refresh(item_in_db)
            return item_in_db
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found category ID: {cat_id}")

    def delete_category(
            self,
            cat_id: int,
            db: Session
    ) -> Any:
        item_in_db = db.query(self.model).filter(self.model.id == cat_id)
        if item_in_db.first():
            item_in_db.delete()
            return {"Detail": "Deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found category ID: {cat_id}")


category = CRUDCategory(Category)
