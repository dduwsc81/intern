from fastapi import APIRouter
from typing import Any
from fastapi.responses import JSONResponse
from app import schemas

router = APIRouter()


@router.get("", response_model=schemas.HealthCheck)
def create_health_check_page() -> Any:
    """
    Health check
    """
    result = {"status": "healthy"}
    return JSONResponse(result)
