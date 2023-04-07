from typing import Any
from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from app.api import deps
from .generate_token import get_cognito_token
import requests
from sqlalchemy.orm import Session
from app import schemas
from app.services import api_service

router = APIRouter()
session = requests.Session()
REQUEST_TIMEOUT = 30


@router.get("")
def get_maintainance_mode(
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, '90000017')
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + "/v1/systemMaintenanceStatus"
    result = api_service.call_api(
        http_type="get",
        token=token,
        url=url
    )
    return result


@router.post("")
def update_maintainance_mode(
    item_in: schemas.MaintainanceModeUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, '90000017')
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + "/v1/systemMaintenanceStatus"
    data = jsonable_encoder(item_in)
    result = api_service.call_api(
        http_type="post",
        token=token,
        url=url,
        data=data
    )
    return result
