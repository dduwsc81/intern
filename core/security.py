from typing import Optional
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def check_authenticated(
        authorization: str
) -> Optional[str]:
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return param
