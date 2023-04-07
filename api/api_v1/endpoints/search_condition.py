from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.SearchCondition])
def get_search_condition(
    store_id: str,
    search_tab_id: int = 1,
    db: Session = Depends(deps.get_db),
    # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve offers.
    """
    # if crud.user.is_superuser(current_user):
    #     items = crud.item.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.item.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )

    result = crud.search_condition.get_search_condition(
        db, search_tab_id=search_tab_id, store_id=store_id
    )
    return result


@router.get("/change", response_model=List[schemas.SearchCondition])
def change_order_index(
    *,
    id1: int,
    id2: int,
    search_tab_id: int = 1,
    db: Session = Depends(deps.get_db),
    # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    change order index of search condition.
    """
    result1, result2 = crud.search_condition.update_search_condition_order(
        db=db, id1=id1, id2=id2, search_tab_id=search_tab_id
    )
    return [result1, result2]


@router.get("/{id}", response_model=schemas.SearchAndSearchDetail)
def get_search_condition_by_id(
    id: int = 1,
    search_tab_id: int = 1,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve offer by id
    """
    result, detail = crud.search_condition.get_search_condition_by_id(
        db, skip=skip, limit=limit, id=id, search_tab_id=search_tab_id
    )
    return {"result": result, "detail": detail}


# update search order index
@router.post("", response_model=schemas.SearchCondition)
def create_search_condition(
    *,
    obj_in: schemas.SearchConditionCreate,
    search_in: schemas.CarQuery,
    user_id: int,
    db: Session = Depends(deps.get_db),
    # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Create new search condition.
    """
    result = crud.search_condition.create_search_condition(
        db=db, obj_in=obj_in, item_in=search_in, user_id=user_id
    )
    return result


# delete by updating delflag = 1
@router.delete("", response_model=schemas.SearchCondition)
def delete_search_condition(
    *,
    id: int,
    search_tab_id: int = 1,
    db: Session = Depends(deps.get_db),
    # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    delete search condition.
    """
    result = crud.search_condition.delete_search_condition(
        db=db, id=id, search_tab_id=search_tab_id
    )
    return result


# change order index of 2 search id
