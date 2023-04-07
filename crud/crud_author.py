from typing import List, Any

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import models.car_training
import schemas
from app.crud.base import CRUDBase

from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):

    def create_author(
            self,
            item_in: schemas.AuthorCreate,
            db: Session
    ) -> Any:
        data = item_in.dict()
        item_in = Author(**data)
        db.add(item_in)
        db.commit()
        db.refresh(item_in)
        return item_in

    def get_all_author(
            self,
            db: Session
    ) -> Any:
        data = db.query(self.model).all()
        if data:
            result = {"Authors": data}
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    def get_author_by_id(
            self,
            author_id: int,
            db: Session
    ) -> Any:
        data = db.query(self.model).filter(self.model.id == author_id).first()
        if data:
            result = {f"Author ID#{author_id}": data}
            return result
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found Author ID {author_id}")

    def update_author(
            self,
            author_id: int,
            item_in: schemas.AuthorUpdate,
            db: Session
    ) -> Any:
        item_ib_db = db.query(self.model).filter(self.model.id == author_id).first()
        if not item_ib_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found Author ID {author_id}")
        else:
            data_db = jsonable_encoder(item_ib_db)

            if isinstance(item_in, dict):
                update_data = item_in
            else:
                update_data = item_in.dict()

            for field in data_db:
                if field in update_data:
                    setattr(item_ib_db, field, update_data[field])

            db.add(item_ib_db)
            db.commit()
            db.refresh(item_ib_db)
            return item_ib_db

    def delete_author(
            self,
            author_id: int,
            db: Session
    ) -> Any:
        item_in_db = db.query(self.model).filter(self.model.id == author_id)
        if item_in_db.first():
            item_in_db.delete()
            return {"detail": "Deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found Author ID {author_id}")


author = CRUDAuthor(Author)
