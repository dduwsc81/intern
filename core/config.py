import logging
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, validator


class Settings(BaseSettings):
    COGNITO_ISS_PATTERN: str = r'^https://cognito-idp.[0-9a-zA-Z_-]+.amazonaws.com/([0-9a-zA-Z_-]+)$'
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    SQLALCHEMY_DATABASE_URI: str
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    # SENTRY_DSN: Optional[HttpUrl] = None
    #
    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v


    class Config:
        case_sensitive = True


settings = Settings()
