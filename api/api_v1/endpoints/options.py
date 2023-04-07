from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.OptionsResponseModel])
def get_options(
    db: Session = Depends(deps.get_db),
    # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve options
    """
    result = crud.options.get_options(db=db)
    return result
