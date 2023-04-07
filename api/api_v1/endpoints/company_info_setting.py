from typing import Any, List
import datetime
from fastapi import APIRouter, Depends, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
from app import crud, schemas
from app.api import deps
from app.models.company_info_setting import CompanyInfoSetting
from app.schemas.company_info_setting import CompanyInfoSettingCreate
from botocore.errorfactory import ClientError
import boto3
from fastapi import HTTPException, status
from app.schemas.s3_file import S3FileCreate
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

router = APIRouter()
s3 = boto3.resource("s3")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{company_code}", response_model=schemas.ResponseCompanyInfoSettingInfo)
def get_company_information(
        db_ro: Session = Depends(deps.get_db), company_code: str = ""
) -> Any:
    company_information = crud.company_info_setting.get_company_information(
        db=db_ro, company_code=company_code
    )
    return JSONResponse(company_information)


@router.get("", response_model=List[schemas.ResponseCompanyInfoSettingInfo])
def get_list_company_information(
        db: Session = Depends(deps.get_db)
) -> Any:
    domain_image = os.environ["DOMAIN_IMAGE"]
    results = crud.company_info_setting.get_list_company_information(db=db)
    list_company_info = []
    for item in results:
        list_company_info.append({
            "company_code": item.CompanyInfoSetting.company_code,
            "company_logo": str(domain_image) + str(item.key) if item.bucket_name and item.key else '',
            "company_name_display": item.CompanyInfoSetting.company_name_display,
            "company_name": item.CompanyInfoSetting.company_name,
            "sender_name": item.CompanyInfoSetting.sender_name,
            "sender_mail": item.CompanyInfoSetting.sender_mail,
            "hidden_company_name": item.CompanyInfoSetting.hidden_company_name
        })
    return JSONResponse(list_company_info)


@router.post("/{company_code}", response_model=schemas.ResponseCompanyInfoSettingInfo)
def update_company_logo(
    db: Session = Depends(deps.get_db),
    company_code: str = "",
    file: bytes = File(...),
    token: str = Depends(oauth2_scheme)
) -> Any:
    claims = jwt.get_unverified_claims(token)
    cognito_id = int(claims["cognito_id"])

    # Create key for file
    name = "logo/" + str(company_code) + "_" + str(datetime.datetime.now())
    bucket_name = os.environ["BUCKET_NAME"]
    region = os.environ["REGION_NAME"]
    domain_image = os.environ["DOMAIN_IMAGE"]

    # Upload to s3
    bucket = ''
    try:
        s3.Bucket(bucket_name).put_object(
            Key=name,
            Body=file,
            ACL="public-read",
            ContentType="image/jpg",
        )
    except ClientError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.response["Error"]["Message"])

    # Check logo
    company_logo_s3_id = crud.company_info_setting.check_company_logo(db=db, company_code=company_code)
    if company_logo_s3_id:
        old_key = crud.s3file.get_old_key(db=db, id=company_logo_s3_id)

        # Delete old logo
        crud.company_info_setting.delete_file(del_bucket=bucket_name, del_key=old_key)
        s3file = crud.s3file.update_s3_file(db=db, id=company_logo_s3_id, key=name)
    else:
        s3_obj = S3FileCreate(bucket_name=domain_image, key=name)
        s3file = crud.s3file.create_s3_file(db=db, obj_in=s3_obj, user_id=cognito_id)

    # Update company logo
    crud.company_info_setting.update_company_logo(db=db, company_code=company_code, s3_file_id=s3file.id)

    company_information = crud.company_info_setting.get_company_information(
        db=db, company_code=company_code
    )
    return JSONResponse(company_information)


@router.put("/{company_code}", response_model=schemas.ResponseCompanyInfoSettingInfo)
def update_company_name_display(
        item_in: schemas.CompanyInfoSettingUpdate,
        company_code: str,
        db: Session = Depends(deps.get_db),
) -> Any:
    company_name_display = item_in.company_name_display
    is_delete_logo = item_in.is_delete_logo
    company_information = crud.company_info_setting.update_company_name_display(
        db=db, company_code=company_code, company_name_display=company_name_display, is_delete_logo=is_delete_logo,
        sender_name=item_in.sender_name, sender_mail=item_in.sender_mail,
        hidden_company_name=item_in.hidden_company_name
    )
    company_information = crud.company_info_setting.get_company_information(
        db=db, company_code=company_code
    )
    return JSONResponse(company_information)


@router.delete("/{company_code}", response_model=schemas.ResponseCompanyInfoSettingInfo)
def delete_company_logo(
        db: Session = Depends(deps.get_db), company_code: str = ""
) -> Any:
    company_information = crud.company_info_setting.delete_company_information(
        db=db, company_code=company_code
    )
    company_information = jsonable_encoder(company_information)
    return JSONResponse(company_information)
