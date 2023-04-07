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
def create_category(
        item_in: schemas.CategoryCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    cat = crud.category.create_category(item_in=item_in, db=db)
    result = jsonable_encoder(cat)
    return result


@router.get("/all")
def get_all_categories(
        db: Session = Depends(deps.get_db)
) -> Any:
    item_in_db = crud.category.get_all_category(db=db)
    result = jsonable_encoder(item_in_db)
    return result


@router.get("/category/book/{cat_id}")
def get_book_in_category(
        cat_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    item_in_db = crud.category.get_book_in_category(cat_id, db)
    result = jsonable_encoder(item_in_db)
    return result


@router.get("/category/{cat_id}")
def get_category_by_id(
        cat_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    item_in_db = crud.category.get_category_by_id(cat_id=cat_id, db=db)
    result = jsonable_encoder(item_in_db)
    return result


@router.put("/update/{cat_id}")
def update_category(
        cat_id: int,
        item_in: schemas.CategoryUpdate,
        db: Session = Depends(deps.get_db)
) -> Any:
    item_in_db = crud.category.update_category(cat_id=cat_id, item_in=item_in, db=db)
    result = jsonable_encoder(item_in_db)
    return result


@router.delete("/delete/{cat_id}")
def delete_category(
        cat_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    result = crud.category.delete_category(cat_id=cat_id, db=db)
    result = jsonable_encoder(result)
    return result
