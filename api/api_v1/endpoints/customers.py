from typing import Any
from fastapi import APIRouter
from fastapi import Depends
from app.api import deps
from .generate_token import get_cognito_token
import requests
from sqlalchemy.orm import Session
from app import schemas
from app.services import api_service
from app.constants import Const

router = APIRouter()
session = requests.Session()


@router.get("/{customer_code}/company/{company_code}/facePhoto")
def get_face_photo(
    company_code,
    customer_code,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + f"/v1/customers/{customer_code}/facePhoto"
    result = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url
    )
    return result
