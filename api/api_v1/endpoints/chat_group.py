from base64 import decode
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, FastAPI, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import JSONResponse
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials
import os
from .format_status import *
from app.constants import Const
router = APIRouter()


@router.post("", response_model=schemas.ChatGroup)
def create_chat_group(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.ChatGroupCreate,
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Create new chat group.
    """
    chat_group, store_company_name, store_company_name_store =\
        crud.chat_group.create_chat_group(db=db, obj_in=item_in)
    result = schemas.ChatGroup(
        id=chat_group.id,
        firebase_chat_id=chat_group.firebase_chat_id,
        insert_id=chat_group.insert_id,
        insert_at=chat_group.insert_at,
        update_id=chat_group.update_id,
        update_at=chat_group.update_at,
        delete_id=chat_group.delete_id,
        delete_at=chat_group.delete_at,
        delete_flag=chat_group.delete_flag,
        message_total_cnt=chat_group.message_total_cnt,
        message_unread_cnt=chat_group.message_unread_cnt,
        last_message_user_id=chat_group.last_message_user_id,
        last_message_user_name=chat_group.last_message_user_name,
        last_message_datetime=chat_group.last_message_datetime,
        last_message=chat_group.last_message,
        offer_id=chat_group.offer_id,
        chassis_number=chat_group.chassis_number,
        div=chat_group.div,
        store_id=chat_group.store_id,
        car_id=chat_group.car_id,
    )

    if store_company_name is not None:
        result.store_name = store_company_name["store_name"]
        result.company_name = store_company_name["company_name"]
        result.store_code = store_company_name["store_code"]
        result.company_code = store_company_name["company_code"]

    if store_company_name_store is not None:
        result.store_name_store = store_company_name_store["store_name_store"]
        result.company_name_store = store_company_name_store["company_name_store"]
        result.store_code_store = store_company_name_store["store_code_store"]
        result.company_code_store = store_company_name_store["company_code_store"]

    # Get token firebase
    credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    uid = 'marketplace-uid'
    custom_token = auth.create_custom_token(uid)
    result.token = custom_token
    return result


# Update chat group
@router.put("/update/{id}", response_model=schemas.ChatGroup)
def update_chat_group(
        store_id: int,
        status: int = Const.CHATTING_FLG,
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.ChatGroupUpdate,
        id: int
) -> Any:
    chat_group_info = crud.chat_group.update_chat_group(db=db, store_id=store_id, status_chat=status, obj_in=item_in, group_id=id)
    chat_group_info = jsonable_encoder(chat_group_info)
    chat_group_info["last_message_datetime"] = utc_to_jst(chat_group_info["last_message_datetime"]) if chat_group_info[
        "last_message_datetime"] else None
    chat_group_info["update_at"] = utc_to_jst(chat_group_info["update_at"]) if chat_group_info["update_at"] else None
    chat_group_info["insert_at"] = utc_to_jst(chat_group_info["insert_at"]) if chat_group_info["insert_at"] else None
    return JSONResponse(chat_group_info)


# get record have message_unread_cnt != 0 and last_message_user_name != admin
@router.get("/notification", response_model=List[schemas.ChatGroup])
def get_chat_with_notification(
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_chat_group = crud.chat_group.get_chat_with_notification(db=db)
    list_chat_group = jsonable_encoder(list_chat_group)
    for item in list_chat_group:
        item["last_message_datetime"] = utc_to_jst(item["last_message_datetime"]) if item[
            "last_message_datetime"] else None
        item["update_at"] = utc_to_jst(item["update_at"]) if item["update_at"] else None
        item["insert_at"] = utc_to_jst(item["insert_at"]) if item["update_at"] else None
    return JSONResponse(list_chat_group)

@router.get("/buyers", response_model= Optional[List[schemas.ChatGroupForBuyer]])
def get_chat_group_buyer(
        car_id: int,
        *,
        db: Session = Depends(deps.get_db),
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Get chat group buyer
    """
    chat_group = crud.chat_group.get_chat_group_buyer(db=db, car_id=car_id)
    if chat_group is not None:
        chat_group = jsonable_encoder(chat_group)
    return chat_group

@router.get("/{id}/members", response_model=List[schemas.ChatGroupMemeber])
def get_chat_group_memebers(
    id: int,
    db: Session = Depends(deps.get_db),
    # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Get list member in chat group
    """
    result = crud.chat_group.get_chat_group_memebers(db=db,group_id=id)
    return jsonable_encoder(result)