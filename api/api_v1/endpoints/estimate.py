from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.constants import Const

router = APIRouter()


@router.get("", response_model=schemas.EstimateResponseModel)
def get_estimation(
        store_id: int,
        car_id: int,
        db: Session = Depends(deps.get_db),
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve estimation info
    """
    result = schemas.EstimateResponseModel()
    estimate, list_option_manager = \
        crud.estimation.get_estimation(db=db, car_id=car_id, store_id=store_id)
    list_options = []
    if list_option_manager is not None:
        for option in list_option_manager:
            option_obj = schemas.options.OptionResponse(option_id=option.option_id,
                                                        option_fee=option.option_fee,
                                                        option_name=option.option_name)
            list_options.append(option_obj)
    if estimate is not None:
        estimate_dict = jsonable_encoder(estimate)
        result = schemas.EstimateResponseModel(**estimate_dict)
        result.list_options = list_options
    return result


@router.put("", response_model=schemas.Estimate)
def put_estimation(
        obj_in: schemas.EstimateUpdate,
        db: Session = Depends(deps.get_db),
        # token: schemas.TokenPayload 6= Depends(deps.get_current_user),
) -> Any:
    """
    Update estimation info
    """
    estimate = crud.estimation.update_estimate(db=db, item_in=obj_in, update_id=Const.ADMIN_ID)
    return estimate
