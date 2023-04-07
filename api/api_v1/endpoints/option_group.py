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


@router.get('/list-group/{menu_id}', response_model=schemas.OptionGroupListResponse)
def get_list_group(
        menu_id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_group = crud.option_group.get_list_group(db=db, menu_id=menu_id)
    return list_group


@router.post('/create-group', response_model=schemas.OptionGroupResponse)
def create_group(
        item_in: schemas.OptionGroupCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    option_group = crud.option_group.create_group(db=db, obj_in=item_in)
    option_group = jsonable_encoder(option_group)
    return option_group


@router.put('/update-group/{id}', response_model=schemas.OptionGroupResponse)
def update_group(
        item_in: schemas.OptionGroupUpdate,
        id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    option_group = crud.option_group.update_group(db=db, obj_in=item_in, id=id)
    option_group = jsonable_encoder(option_group)
    return option_group


@router.delete("/{id}", response_model=schemas.OptionGroupResponse)
def delete_group(
        id: int,
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    option_group = crud.option_group.delete_group(db=db, id=id)
    return option_group
