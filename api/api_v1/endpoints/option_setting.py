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


@router.get('/list_option/{group_id}', response_model=List[schemas.OptionSettingResponse])
def get_list_option(
        group_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_option = crud.option_setting.get_list_option(db=db, group_id=group_id)
    list_option = jsonable_encoder(list_option)
    return list_option


@router.post('/create_option', response_model=schemas.OptionSettingResponse)
def create_option_setting(
        item_in: schemas.OptionSettingCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_option = crud.option_setting.create_option_setting(db=db, obj_in=item_in)
    list_option = jsonable_encoder(list_option)
    return list_option


@router.put('/update_option/{id}', response_model=schemas.OptionSettingResponse)
def update_option_setting(
        item_in: schemas.OptionSettingUpdate,
        id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_option = crud.option_setting.update_option_setting(db=db, obj_in=item_in, id=id)
    list_option = jsonable_encoder(list_option)
    return list_option


@router.delete("/{id}", response_model=schemas.OptionSettingResponse)
def delete_option_setting(
        id: int,
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    option_setting = crud.option_setting.delete_option_setting(db=db, id=id)
    return option_setting
