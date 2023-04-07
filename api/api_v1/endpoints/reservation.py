from typing import Any
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from app.api import deps
from .generate_token import get_cognito_token
import requests
from sqlalchemy.orm import Session
import json

router = APIRouter()
session = requests.Session()
REQUEST_TIMEOUT = 30


@router.delete("/{id}/company/{company_code}")
def delete_reservation(
        id,
        company_code,
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    status_code = 0
    try:
        authorization = "Bearer " + cognito_token['token']
        res = session.delete(
            f"{cognito_token['base_url']}/v1/reservationDetail/{id}",
            headers={"authorization": authorization},
            timeout=REQUEST_TIMEOUT,
        )
        if res.status_code < 200 or res.status_code >= 300:
            print(res)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is invalid or parameters are incorrect",
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation reservation id {id} not found",
        )
    return "Deleted reservation successfuls"


@router.get("/menu/{company_code}/{store_code}/{service_code}")
def get_reservation_menu(
    company_code,
    store_code,
    service_code,
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    try:
        authorization = "Bearer " + cognito_token['token']
        res = session.get(
            f"{cognito_token['base_url']}/v1/"
            f"reservationMenu/{store_code}/{service_code}",
            headers={"authorization": authorization},
            timeout=REQUEST_TIMEOUT,
        )
        if res.status_code < 200 or res.status_code >= 300:
            status_code = res.status_code
            if status_code == 401:
                raise HTTPException(
                    status_code=status_code,
                    detail="token Unauthorized")
            raise HTTPException(
                status_code=status_code,
                detail="Request is invalid or parameters are incorrect",
            )
    except Exception as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    result = json.loads(res.text)
    return result
