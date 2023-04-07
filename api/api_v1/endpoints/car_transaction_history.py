from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.CarTransactionHistoryList)
def get_car_transaction(
        id: int,
        page: int = 0,
        page_size: int = 10,
        *,
        db: Session = Depends(deps.get_db),
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve car_transaction_history
    """
    skip = (page - 1) * page_size
    limit = page_size

    result, total = crud.car_transaction_history.get_car_transaction_by_car_id(db=db, id=id,
                                                                        skip=skip, limit=limit)

    return {
        "results": result,
        "total": total
    }
