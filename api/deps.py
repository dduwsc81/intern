import re
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.token import TokenPayload
from starlette.requests import Request
import logging

Authorization = APIKeyHeader(name='Authorization')
logger = logging.getLogger(__name__)

def get_db(request: Request) -> Generator:
    # print(request.url.path)
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        logger.exception('Session rollback because of exception')
        db.rollback()
        raise
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), authorization: str = Depends(Authorization)) -> TokenPayload:
    try:
        token = security.check_authenticated(authorization)
        payload = jwt.get_unverified_claims(token)

        pattern = re.compile(settings.COGNITO_ISS_PATTERN)
        matchCognito = pattern.match(payload.get('iss'))

        if matchCognito:
            userPoolId = matchCognito.group(1)
        payload['userpoolId'] = userPoolId

        # token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    crud.authorized.check_authority(db,
                                    auth_company_code=payload['company_code'],
                                    role_name=payload['role_name'],
                                    userpool_id=payload['userpoolId'],
                                    operationid='getSender',
                                    api_type='carsMANAGER',
                                    company_code=payload['company_code']
                                    )

    return TokenPayload(**payload)


def get_current_user_v2(db: Session = Depends(get_db), authorization: str = Depends(Authorization)) -> TokenPayload:
    try:
        token = security.check_authenticated(authorization)
        payload = jwt.get_unverified_claims(token)

        pattern = re.compile(settings.COGNITO_ISS_PATTERN)
        matchCognito = pattern.match(payload.get('iss'))

        if matchCognito:
            userPoolId = matchCognito.group(1)
        payload['userpoolId'] = userPoolId

        # token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return TokenPayload(**payload)
