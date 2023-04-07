import json
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.models.m_distance_travelled import MDistanceTravelled
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("")
def get_m_distance_travelled(
        db: Session = Depends(deps.get_db)
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve m_distance_travelled
    """
    mileage_master = crud.m_distance_travelled.get_m_distance_travelled(db=db)
    r = {"mileage_master": mileage_master}
    result = jsonable_encoder(r)
    return JSONResponse(result)
