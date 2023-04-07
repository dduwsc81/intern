from typing import Any

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("", response_model=schemas.UtilizationServiceList)
async def get_utilization(
        page: int = 0,
        page_size: int = 10,
        db: Session = Depends(deps.get_db),
        *,
        item_in: schemas.UtilizationQueryParam,
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve utilization
    """
    skip = (page - 1) * page_size
    limit = page_size

    number_of_negotiation_cars, negotiation_amount, \
    number_of_platform_buy_car, platform_buy_amount, \
    number_of_platform_sell_car, platform_sell_amount, \
    total, all_utilization_service = crud.utilization_service \
        .get_utilization(db=db, limit=limit, skip=skip, item_in=item_in)

    result = schemas.UtilizationServiceList(
        total=total,
        number_of_negotiation_cars=number_of_negotiation_cars,
        negotiation_amount=negotiation_amount,
        number_of_platform_buy_car=number_of_platform_buy_car,
        platform_buy_amount=platform_buy_amount,
        number_of_platform_sell_car=number_of_platform_sell_car,
        platform_sell_amount=platform_sell_amount
    )

    if all_utilization_service is not None:
        all_utilization_service = jsonable_encoder(all_utilization_service)
        result.list_utilization_service = all_utilization_service

    return result
