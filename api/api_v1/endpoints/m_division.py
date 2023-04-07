from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/paid-type")
def get_paid_type(
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve paid type
    """
    db_obj = crud.m_division.get_paid_type(db=db)
    result = jsonable_encoder(db_obj)
    return result
