from typing import List, Any

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
import models.car_training
import schemas
from app.crud.base import CRUDBase

from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):

    def create_book(
            self,
            item_in: schemas.BookCreate,
            db: Session
    ) -> Any:

        if crud.author.get_author_by_id(item_in.author_id, db) and crud.category.get_category_by_id(item_in.cat_id, db):
            data = item_in.dict()
            item_in_db = Book(**data)
            db.add(item_in_db)
            db.commit()
            db.refresh(item_in_db)
            return item_in_db
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found ForeignKey")

    def get_all_book(
            self,
            db: Session
    ) -> Any:
        data_db = db.query(self.model).all()
        if data_db:
            result = {"Books": data_db}
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    def get_book_by_id(
            self,
            book_id: int,
            db: Session
    ) -> Any:
        data_db = db.query(self.model).filter(self.model.id == book_id).first()
        if data_db:
            return data_db
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def get_book_by_cat_id(
            self,
            cat_id: int,
            db: Session
    ) -> Any:
        data_db = db.query(self.model).filter(self.model.cat_id == cat_id).all()
        return data_db


book = CRUDBook(Book)
