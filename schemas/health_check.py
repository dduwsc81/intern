from typing import Optional
from pydantic import BaseModel


# Properties to return to client
class HealthCheck(BaseModel):
    status: Optional[str]