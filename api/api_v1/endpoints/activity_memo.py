from typing import Any, List, Optional
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.constants import Const


router = APIRouter()


@router.get("", response_model=Optional[schemas.ActivityMemoResponseList])
def get_activity_memo_by_car_id(
        car_id: int,
        db: Session = Depends(deps.get_db),
        sort_name: int = Const.MEMO_CREATE_AT,
        sort_type: int = Const.SORT_DESC,
        page: int = 1,
        page_size: int = 10,
) -> Any:
    """
    Retrieve activity memo by car id.
    """
    skip = (page - 1) * page_size
    limit = page_size
    activity_memo, total = crud.activity_memo.get_activity_memo_by_car_id(db=db,
                                                                   car_id=car_id,
                                                                   sort_name=sort_name,
                                                                   sort_type=sort_type,
                                                                   skip=skip,
                                                                   limit=limit,
                                                                   )
    response = schemas.ActivityMemoResponseList()
    response.total = total

    memo = jsonable_encoder(activity_memo)
    memo_list = list()
    # convert data
    for row in memo:
        memo_list.append(schemas.ActivityMemo(**row))

    response.results = memo_list
    return response


@router.put("/{activity_memo_id}", response_model=schemas.ActivityMemo)
def update_activity_memo_by_activity_memo_id(
        *,
        item_in: schemas.ActivityMemoUpdate,
        activity_memo_id: int,
        user_id: int,
        db: Session = Depends(deps.get_db),
        token: schemas.TokenPayload = Depends(deps.get_current_user_v2),
) -> Any:
    """
    Update activity memo.
    """
    staff_info = crud.staff.get_staff_by_cognito_id(db=db, cognito_id=token.cognito_id, company_code=token.company_code)
    if staff_info:
        item_in.memo_editor = staff_info.last_name + staff_info.first_name
    activity_memo = crud.activity_memo.update_activity_memo(db=db,
                                                            obj_in=item_in,
                                                            activity_memo_id=activity_memo_id,
                                                            user_id=token.cognito_id)
    activity_memo = jsonable_encoder(activity_memo)
    result = schemas.ActivityMemo(**activity_memo)
    return result


@router.post("", response_model=schemas.ActivityMemo)
def create_activity_memo(
        *,
        item_in: schemas.ActivityMemoCreate,
        user_id: int,
        db: Session = Depends(deps.get_db),
        token: schemas.TokenPayload = Depends(deps.get_current_user_v2),
) -> Any:
    """
    Create activity memo.
    """
    staff_info = crud.staff.get_staff_by_cognito_id(db=db, cognito_id=token.cognito_id, company_code=token.company_code)
    if staff_info:
        item_in.memo_editor = staff_info.last_name + staff_info.first_name
    activity_memo = crud.activity_memo.create_activity_memo(db=db, user_id=token.cognito_id, obj_in=item_in)
    activity_memo = jsonable_encoder(activity_memo)
    result = schemas.ActivityMemo(**activity_memo)
    return result


@router.delete("/{activity_memo_id}", response_model=schemas.ActivityMemo)
def delete_activity_by_activity_id(
        *,
        activity_memo_id: int,
        user_id: int,
        db: Session = Depends(deps.get_db),
        token: schemas.TokenPayload = Depends(deps.get_current_user_v2),
) -> Any:
    """
    Delete activity memo by setting delete_flag = 1
    """
    activity_memo = crud.activity_memo.delete_by_update_delete_flag(db=db,
                                                                    activity_memo_id=activity_memo_id,
                                                                    user_id=token.cognito_id)
    activity_memo = jsonable_encoder(activity_memo)
    result = schemas.ActivityMemo(**activity_memo)
    return result

