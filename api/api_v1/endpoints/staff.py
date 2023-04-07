import json
from typing import Any
from fastapi import APIRouter
from app import crud, schemas, models
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session
import requests
from app.api import deps
from .generate_token import get_cognito_token

router = APIRouter()
session = requests.Session()
REQUEST_TIMEOUT = 30


@router.get('/{id}/company/{company_code}/staff-photo')
def get_staff_photo(
        id: str,
        company_code: str,
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
       Retrieve staff photo by login internal account and call to Cm server.
    """
    cognito_token = get_cognito_token(db, company_code)
    try:
        authorization = "Bearer " + cognito_token['token']
        print('authorization>>>', authorization)
        res = session.get(
            f"{cognito_token['base_url']}/v1/staff/{id}/staffPhoto",
            headers={"authorization": authorization},
            timeout=REQUEST_TIMEOUT,
        )
        if res.status_code < 200 or res.status_code >= 300:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is invalid or parameters are incorrect",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Staff id {id} not found",
        )
    print('Print staff photo obj>>>>>>', res.text)
    result = json.loads(res.text)
    return result
