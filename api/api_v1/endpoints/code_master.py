from typing import Any, List
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from .generate_token import get_cognito_token
import requests
from fastapi import HTTPException, status
import json
from .format_status import convert_camel_to_snake_case


router = APIRouter()
session = requests.Session()
REQUEST_TIMEOUT = 30


@router.get("", response_model=List[schemas.CodeMaster])
def get_list_service(
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get list service.
    """
    list_service = crud.code_master.get_list_service(db)
    return list_service


@router.get("/{company_code}/get_list_reservation_type", response_model=List[schemas.CodeMaster])
def get_list_reservation_type(
        company_code: str,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get list service.
    """
    cognito_token = get_cognito_token(db, company_code)
    try:
        authorization = "Bearer " + cognito_token['token']
        res = session.get(
            f"{cognito_token['base_url']}/v1/code/reservation_data_type",
            headers={"authorization": authorization},
            timeout=REQUEST_TIMEOUT,
        )
        if res.status_code < 200 or res.status_code >= 300:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is invalid or parameters are incorrect",
            )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation list not found",
        )
    list_service = json.loads(res.text)["results"]
    list_service = [{convert_camel_to_snake_case(j): i[j] for j in i} for i in list_service]
    for reservation_type in list_service:
        reservation_type["id"] = 0
    return list_service


@router.get("/service_type_by_company", response_model=List[schemas.CodeMaster])
def get_service_types(
        company_code: str,
        store_code: str,
        db: Session = Depends(deps.get_db)) -> Any:
    service_types = crud.code_master.get_service_types_by_company(db=db,
                                                                  company_code=company_code, store_code=store_code)
    re = {"service_types": service_types}
    r = jsonable_encoder(re)
    return JSONResponse(r)
