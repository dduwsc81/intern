import json
from typing import Any, List
from fastapi import APIRouter
from app import crud, schemas, models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, File
from sqlalchemy.orm import Session
from app.api import deps
import datetime
from jose import jwt
import os
import boto3
from botocore.errorfactory import ClientError
from fastapi import HTTPException, status
from app.schemas.s3_file import S3FileCreate


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post('/list_menu', response_model=List[schemas.MenuSettingResponse])
def get_list_menu(
        item_in: schemas.MenuSettingRequest,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_menu = crud.menu_setting.get_menu_setting(db=db, obj_in=item_in)
    return list_menu


@router.post('/create_menu', response_model=schemas.MenuSetting)
def create_menu_setting(
        item_in: schemas.MenuSettingCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_menu = crud.menu_setting.create_menu_setting(db=db, obj_in=item_in)
    return list_menu


@router.put('/update_menu/{id}', response_model=schemas.MenuSetting)
def update_menu_setting(
        item_in: schemas.MenuSettingUpdate,
        id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    list_menu = crud.menu_setting.update_menu_setting(db=db, obj_in=item_in, id=id)
    return list_menu


@router.delete("/{id}", response_model=schemas.MenuSetting)
def delete_menu_setting(
        id: int,
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    menu_setting = crud.menu_setting.delete_menu_setting(db=db, id=id)
    # check exit policy and terms
    for i in ("policy_content", "terms_content"):
        s3file_id = crud.menu_setting.check_exit_file(db=db, menu_id=id, file_type=i)
        if s3file_id:
            old_key = crud.s3file.get_old_key(db=db, id=s3file_id)
            crud.company_info_setting.delete_file(del_bucket=os.environ["BUCKET_NAME"], del_key=old_key)
    return menu_setting


@router.post("/upload_file/{file_type}")
def upload_file(
    menu_id: str = '',
    db: Session = Depends(deps.get_db),
    file_type: str = "",
    file: bytes = File(...),
    token: str = Depends(oauth2_scheme)
) -> Any:
    claims = jwt.get_unverified_claims(token)
    cognito_id = int(claims["cognito_id"])

    # Create key for file
    name = file_type + "/pdf/" + str(datetime.datetime.now())
    bucket_name = os.environ["BUCKET_NAME"]
    region = os.environ["REGION_NAME"]
    domain_image = os.environ["DOMAIN_IMAGE"]

    # Upload to s3
    try:
        s3 = boto3.resource("s3")
        s3.Bucket(bucket_name).put_object(
            Key=name,
            Body=file,
            ACL="public-read",
            ContentType="application/pdf",
        )
    except ClientError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.response["Error"]["Message"])

    # Check policy/terms file
    if menu_id:
        s3file_id = crud.menu_setting.check_exit_file(db=db, menu_id=int(menu_id), file_type=file_type)
        if s3file_id:
            old_key = crud.s3file.get_old_key(db=db, id=s3file_id)
            # Delete old file
            crud.company_info_setting.delete_file(del_bucket=bucket_name, del_key=old_key)
            s3file = crud.s3file.update_s3_file(db=db, id=s3file_id, key=name)
        else:
            s3_obj = S3FileCreate(bucket_name=domain_image, key=name)
            s3file = crud.s3file.create_s3_file(db=db, obj_in=s3_obj, user_id=cognito_id)
    else:
        s3_obj = S3FileCreate(bucket_name=domain_image, key=name)
        s3file = crud.s3file.create_s3_file(db=db, obj_in=s3_obj, user_id=cognito_id)

    return {
        "s3_file_id": s3file.id
    }
