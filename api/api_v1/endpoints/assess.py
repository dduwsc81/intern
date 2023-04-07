import json
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.constants import Const
from starlette.responses import JSONResponse
from .format_status import *

router = APIRouter()


@router.put("", response_model=schemas.AssessResponse)
def update_inspection_mark(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.AssessUpdateByRegisterSale,
        token: schemas.TokenPayload = Depends(deps.get_current_user_v2),
):
    """
    upsert assess
    """
    item_in.assess_user_id = token.cognito_id
    item_in.user_id = token.cognito_id
    staff_info = crud.staff.get_staff_by_cognito_id(db=db, cognito_id=token.cognito_id, company_code=token.company_code)
    if staff_info:
        item_in.assess_user_name = staff_info.last_name + staff_info.first_name
        item_in.assess_user_id = staff_info.cognito_id
    assess = crud.assess.upsert_by_registersale(db,item_in, item_in.user_id)
    result = schemas.AssessResponse(**jsonable_encoder(assess))

    return result
