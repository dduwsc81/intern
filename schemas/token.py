from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    role_name: str
    company_code: str
    user_code: str
    cognito_id: str
