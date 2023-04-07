from typing import Any

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("")
def get_m_year(
        db: Session = Depends(deps.get_db)
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve m_year
    """
    years = crud.m_year.get_m_year(db=db)
    r = {"years": years}
    result = jsonable_encoder(r)
    return JSONResponse(result)
