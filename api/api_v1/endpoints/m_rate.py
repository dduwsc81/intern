from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import crud, schemas
from app.api import deps


router = APIRouter()


@router.get("", response_model=schemas.MRateResponse)
def get_tax_rate(
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve tax_rate
    """
    tax_rate = crud.m_rate.get_tax_rate(db=db)
    return tax_rate
