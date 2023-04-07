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
def create_author(
        item_in: schemas.AuthorCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    item_in_db = crud.author.create_author(item_in, db)
    result = jsonable_encoder(item_in_db)
    return result


@router.get("/all")
def get_all_author(
        db: Session = Depends(deps.get_db)
) -> Any:
    item_in_db = crud.author.get_all_author(db)
    result = jsonable_encoder(item_in_db)
    return result


@router.get("/author/{author_id}")
def get_author_by_id(
        author_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    item_in_db = crud.author.get_author_by_id(author_id, db)
    result = jsonable_encoder(item_in_db)
    return result


