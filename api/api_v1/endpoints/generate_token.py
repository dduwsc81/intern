import os
import requests
import boto3
from app.models.tenant_information import TenantInformation
from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)
REGION_NAME = os.environ['REGION_NAME']


def get_cognito_info(db, company_code):
    client_id = os.environ['CARS_MANAGER_CLIENT_ID'] if 'CARS_MANAGER_CLIENT_ID' in os.environ else None
    user_info = db.query(TenantInformation).filter(TenantInformation.company_code == company_code).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User information company_code {company_code} not found')
    user_info = jsonable_encoder(user_info)
    user_info['client_id'] = client_id
    return user_info


def get_cognito_token(db, company_code):
    user_info = get_cognito_info(db, company_code)
    cognito_token = {}
    try:
        cognito = boto3.client('cognito-idp', region_name=REGION_NAME)
        res = cognito.initiate_auth(
            ClientId=user_info["client_id"],
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': user_info["user_email"],
                'PASSWORD': user_info["user_password"],
            }
        )
        cognito_token = {
            "token": res['AuthenticationResult']['IdToken'],
            "base_url": user_info['base_url']
        }
        logger.info(cognito)
        logger.info(res)
    except ClientError as e:
        print(e.args)
        return None
    return cognito_token
