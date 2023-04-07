from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.SearchConditionDetail)
def get_search_conditiondetail_by_id(
    id: int = 1,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve search condition by id
    """
    result = crud.search_condition_detail.get_search_conditiondetail_by_id(
        db, skip=skip, limit=limit, id=id
    )
    return result


@router.post("", response_model=schemas.SearchConditionDetail)
def create_search_condition_detail(
    *,
    item_in: schemas.SearchConditionDetailCreate,
    db: Session = Depends(deps.get_db),
    # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Create new search condition.
    """
    result = crud.search_condition_detail.create_search_condition_detail(
        db=db, obj_in=item_in
    )
    return result
