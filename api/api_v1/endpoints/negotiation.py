from typing import Any, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.constants import Const

router = APIRouter()


@router.get("/car/{car_id}", response_model=schemas.ListNegotiation)
def get_negotiation_by_car_id(
    car_id: int,
    page_size: Optional[int] = 1,
    page: Optional[int] = 1,
    db: Session = Depends(deps.get_db),
    # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve negotiation by car id
    """
    skip = (page - 1) * page_size
    limit = page_size
    total, nego = crud.negotiation.get_negotiation_by_car_id(db=db,
                                                             limit=limit,
                                                             offset=skip,
                                                             car_id=car_id)
    result = [ne[0] for ne in nego]
    if nego:
        for index in range(len(nego)):
            result[index].company_name = nego[index][1]
            result[index].store_name = nego[index][2]
    return {"total": total, "result": result}


@router.put("/deadline", response_model=schemas.NegotiationUpdateStatus)
def update_negotiation_deadline_by_car_id(
        item_in: schemas.NegotiationUpdateDeadline,
        db: Session = Depends(deps.get_db)
        # token: schemas.TokenPayload = Depends(deps.get_current_user),        ,
) -> Any:
    """
    Update negotiation deadline and register sale deadline
    """
    # init result response default False
    result = schemas.NegotiationUpdateStatus()
    result.status = False
    # update nego deadline
    # init negotiation period_to = selected date at time 23:59:00
    nego_period_to = item_in.period_to.strftime('%Y-%m-%d %H:%M:%S')
    nego_period_to = nego_period_to.split(' ')[0] + " 23:59:00"
    nego_period_to = datetime.strptime(nego_period_to, '%Y-%m-%d %H:%M:%S')
    db_obj = schemas.NegotiationUpdate(period_to=nego_period_to)
    crud.negotiation.update_negotiation_by_car_id(db=db,
                                                  car_id=item_in.car_id,
                                                  obj_in=db_obj,
                                                  update_id=Const.ADMIN_ID)

    # plus 7 day from nego deadline for register_sale đeadline
    register_period_to = nego_period_to + timedelta(days=7)
    # update register sale deadline
    db_obj = schemas.RegisterSaleUpdate(period_to=register_period_to)
    crud.register_sale.update_register_sale_by_car_id(db=db,
                                                      car_id=item_in.car_id,
                                                      obj_in=db_obj,
                                                      update_id=Const.ADMIN_ID)
    # if everything fine change status = True
    result.status = True
    return result
