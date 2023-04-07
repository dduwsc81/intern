from typing import Any, Optional

import requests
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/add")
def create_book(
        item_in: schemas.BookCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    data = crud.book.create_book(item_in, db)
    result = jsonable_encoder(data)
    return result


@router.get("/all")
def get_all_book(
        db: Session = Depends(deps.get_db)
) -> Any:
    data = crud.book.get_all_book(db)
    result = jsonable_encoder(data)
    return result


@router.get("/book/{book_id}")
def get_book_by_id(
        book_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    data = crud.book.get_book_by_id(book_id, db)
    result = jsonable_encoder(data)

    return result
