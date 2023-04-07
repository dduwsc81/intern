import json
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from starlette.responses import JSONResponse
from .format_status import *

router = APIRouter()


@router.get("", response_model=List[schemas.RegisterSale])
def get_register_sales(
        db: Session = Depends(deps.get_db),
        page: int = 1,
        page_size: int = 10
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve register_sale.
    """
    # if crud.user.is_superuser(current_user):
    #     items = crud.item.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.item.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    skip = (page - 1) * page_size
    limit = page_size
    register_sales, total = crud.register_sale.get_register_sales(db, skip=skip, limit=limit)
    register_sale = jsonable_encoder(register_sales)
    # format_assess_status
    for item in register_sale:
        item['sales_period_start'] = format_response_sales_period_start(item['sales_period_start'])
        offer_status_decs = crud.m_division.get_status_description(db, div_name='assess_status',
                                                                   param=item['assess_status'])
        item["assess_status_number"] = item["assess_status"]
        item["assess_status"] = offer_status_decs[0]
        if item['AI_assess_price']:
            item['AI_assess_price'] = round(item['AI_assess_price'])
    re = {'total': total, 'limit': limit, 'offset': skip, 'results': register_sale}
    r = json.dumps(re)
    return JSONResponse(content=json.loads(r))


@router.get("/{id}", response_model=schemas.Car)
def get_register_sale_by_id(
        id: int = 1,
        db: Session = Depends(deps.get_db)
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve cars by register_sale
    """
    register = crud.register_sale.get_register_sale_by_id(db, id=id)
    register = jsonable_encoder(register)
    register['sales_period_start'] = format_response_sales_period_start(register['sales_period_start'])
    if register['AI_assess_price']:
        register['AI_assess_price'] = round(register['AI_assess_price'])
    # format assess status
    offer_status_decs = crud.m_division.get_status_description(db, div_name='assess_status',
                                                               param=register['assess_status'])
    register["assess_status_number"] = register["assess_status"]
    register["assess_status"] = offer_status_decs[0]
    return JSONResponse(register)


@router.put("/{id}", response_model=schemas.RegisterSale)
def update_status_register_sale_by_id(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.RegisterSaleUpdateStatus,
        id: int
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Update register sale.
    """
    register_sale = crud.register_sale.update_status_register_sale_by_id(db=db, obj_in=item_in, id=id)
    # format assess status
    offer_status_decs = crud.m_division.get_status_description(db, div_name='assess_status',
                                                               param=register_sale['assess_status'])
    register_sale["assess_status_number"] = register_sale["assess_status"]
    register_sale["assess_status"] = offer_status_decs[0]
    return JSONResponse(register_sale)


@router.post("/search", response_model=List[schemas.RegisterSale])
def register_search(
        page: int = 1,
        page_size: int = 10,
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.RegisterSaleSearch = None,
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),

) -> Any:
    """
    Search register sale.
    """
    skip = (page - 1) * page_size
    limit = page_size
    register_sales_filter, count = crud.register_sale.search_register_sale(
                                                                            db=db,
                                                                            skip=skip,
                                                                            limit=limit,
                                                                            item_in=item_in,
                                                                        )

    register_sales = jsonable_encoder(register_sales_filter)
    # format_assess_status
    for item in register_sales:
        item['sales_period_start'] = format_response_sales_period_start(item['sales_period_start'])
        if item['AI_assess_price']:
            item['AI_assess_price'] = round(item['AI_assess_price'])
    re = {'total': count, 'limit': limit, 'offset': skip, 'results': register_sales}
    r = json.dumps(re)
    return JSONResponse(content=json.loads(r))


@router.get("/car/{car_id}", response_model=schemas.ListRegisterSale)
def get_register_sale_by_car_id(
    car_id: int,
    page_size: Optional[int] = 1,
    page: Optional[int] = 1,
    db: Session = Depends(deps.get_db),
    # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve register sale by car id
    """
    skip = (page - 1) * page_size
    limit = page_size
    total, register = crud.register_sale.get_register_sale_by_car_id(db=db,
                                                                     limit=limit,
                                                                     offset=skip,
                                                                     car_id=car_id)
    return {"total": total, "result": register}


@router.post("/assess-status", response_model=schemas.RegisterSale)
def update_inspection_mark(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.RegisterSaleUpdateAssess,
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
):
    """
    Insert or update assess_id in register sale
    """
    register_sale = crud.register_sale.update_assess_id_by_register_sale_id(db=db, item_in=item_in)
    return register_sale
