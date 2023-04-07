import json
from typing import Any, List
from fastapi import APIRouter
from app import crud, schemas, models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from app.api import deps
from fastapi.encoders import jsonable_encoder

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/list_service_fee')
def get_list_service_fee(
        item_in: schemas.ServiceFeeRequest,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_service_fee = crud.service_fee.get_service_fee(db=db, obj_in=item_in)
    list_service_fee = jsonable_encoder(list_service_fee)
    return list_service_fee


@router.post('/create_service_fee', response_model=schemas.ServiceFee)
def create_menu_setting(
        item_in: schemas.ServiceFeeCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    service_fee = crud.service_fee.create_service_fee(db=db, obj_in=item_in)
    service_fee = jsonable_encoder(service_fee)
    return service_fee


@router.delete('/delete_service_fee/{id}', response_model=schemas.ServiceFee)
def delete_service_fee(
        id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    service_fee = crud.service_fee.delete_service_fee(db=db, id=id)
    service_fee = jsonable_encoder(service_fee)
    return service_fee


@router.put('/update_service_fee/{id}', response_model=schemas.ServiceFee)
def update_service_fee(
        id: int,
        item_in: schemas.ServiceFeeUpdate,
        db: Session = Depends(deps.get_db)
) -> Any:
    service_fee = crud.service_fee.update_service_fee(db=db, id=id, obj_in=item_in)
    service_fee = jsonable_encoder(service_fee)
    return service_fee
