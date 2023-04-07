from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import JSONResponse
from .format_status import *

router = APIRouter()


@router.get("", response_model=List[schemas.Offer])
def get_offers_by_company(
        # company_id: str,
        db: Session = Depends(deps.get_db),
        page: int = 1,
        page_size: int = 10
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
    skip = (page - 1) * page_size
    limit = page_size
    offers_filter, count = crud.offer.get_offers(db, skip=skip, limit=limit)
    offers = jsonable_encoder(offers_filter)

    # format offer status and store name
    for item in offers:
        item['sales_period_start'] = format_response_sales_period_start(item['sales_period_start'])
        item['offer_out_store_name'] = crud.offer.get_store_name(db, item['offer_out_store_id'])[0]
        item['offer_out_company_name'] = crud.offer.get_store_name(db, item['offer_out_store_id'])[2]
        item['offer_in_store_name'] = crud.offer.get_store_name(db, item['offer_in_store_id'])[0]
        item['offer_in_company_name'] = crud.offer.get_store_name(db, item['offer_in_store_id'])[2]
        item['time_offer'] = utc_to_jst(item['time_offer'])
        item['last_message_datetime'] = utc_to_jst(item['last_message_datetime']) if item[
            'last_message_datetime'] else None
        item.pop('offer_out_store_id')
        item.pop('offer_in_store_id')
        offer_status_decs = crud.m_division.get_status_description(db, div_name='offer_status',
                                                                   param=item['offer_status'])
        item["offer_status_number"] = item["offer_status"]
        item["offer_status"] = offer_status_decs[0]
    re = {'total': count, 'limit': limit, 'offset': skip, 'results': offers}
    r = json.dumps(re)
    return JSONResponse(content=json.loads(r))


@router.get("/{id}", response_model=schemas.Offer)
def get_offer_by_id(
        id: int = 1,
        db: Session = Depends(deps.get_db)
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve offer by id
    """
    offer, store_id, store_out, list_car_same_chassis_number = crud.offer.get_offer_by_id(db, id=id)
    resp = jsonable_encoder(offer)
    list_car_same_chassis_number = jsonable_encoder(list_car_same_chassis_number)
    for item in list_car_same_chassis_number:
        item['is_offer'] = crud.offer.check_offered(db=db, car_id=item['id'])
        item.pop("id")
        item["company_name_owner"] = item.pop("company_name")
    resp.pop('car_id')
    resp['store_id'] = store_id[1]
    resp['offer_out_store_id'] = int(resp['offer_out_store_id']) if resp['offer_out_store_id'] else ""
    resp['offer_in_store_id'] = int(resp['offer_in_store_id']) if resp['offer_in_store_id'] else ""
    resp["other_store"] = list_car_same_chassis_number
    resp["company_name_offer"] = store_out[0] if store_out else ""
    resp["offer_out_store_name"] = store_out[1] if store_out else ""
    resp['sales_period_start'] = format_response_sales_period_start(resp['sales_period_start'])

    # format offer status
    offer_status_decs = crud.m_division.get_status_description(db, div_name='offer_status', param=resp['offer_status'])
    resp["offer_status_number"] = resp["offer_status"]
    resp["offer_status"] = offer_status_decs[0]
    return JSONResponse(resp)


@router.put("/{id}", response_model=schemas.Offer)
def update_offer(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        item_in: schemas.OfferUpdateStatus,

        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Update status offer.
    """
    offer, store_id, store_out, list_car_same_chassis_number = crud.offer.update_offer_by_id(db=db, obj_in=item_in,
                                                                                             id=id)
    resp = jsonable_encoder(offer)
    list_car_same_chassis_number = jsonable_encoder(list_car_same_chassis_number)
    for item in list_car_same_chassis_number:
        item.pop("id")
        item["company_name_owner"] = item.pop("company_name")
    resp['store_id'] = store_id[1]
    resp['offer_out_store_id'] = int(resp['offer_out_store_id']) if resp['offer_out_store_id'] else ""
    resp['offer_in_store_id'] = int(resp['offer_in_store_id']) if resp['offer_in_store_id'] else ""
    resp["other_store"] = list_car_same_chassis_number
    resp["company_name_offer"] = store_out[0] if store_out else ""
    resp["offer_out_store_name"] = store_out[1] if store_out else ""
    resp['sales_period_start'] = format_response_sales_period_start(resp['sales_period_start'])

    # format offer status
    offer_status_decs = crud.m_division.get_status_description(db, div_name='offer_status', param=resp['offer_status'])
    resp["offer_status_number"] = resp["offer_status"]
    resp["offer_status"] = offer_status_decs[0]
    return JSONResponse(resp)


@router.post("/search", response_model=List[schemas.Offer])
def offer_search(
        page: int = 1,
        page_size: int = 10,
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.OfferQuery = None,
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),

) -> Any:
    """
    Search offer.
    """
    skip = (page - 1) * page_size
    limit = page_size
    maker = item_in.maker
    car_type = item_in.car_type
    grade = item_in.grade
    sales_period_start_from = item_in.sales_period_start_from
    sales_period_start_to = item_in.sales_period_start_to
    registration_end_date_from = item_in.registration_end_date_from
    registration_end_date_to = item_in.registration_end_date_to
    car_mileage_from = item_in.car_mileage_from
    car_mileage_to = item_in.car_mileage_to
    offer_status = item_in.offer_status
    area = item_in.area
    aggregation_wholesale_price_market_from = item_in.aggregation_wholesale_price_market_from
    aggregation_wholesale_price_market_to = item_in.aggregation_wholesale_price_market_to
    buy_now_total_price_from = item_in.buy_now_total_price_from
    buy_now_total_price_to = item_in.buy_now_total_price_to
    insert_at_from = item_in.insert_at_from
    insert_at_to = item_in.insert_at_to
    chassis_number = item_in.chassis_number
    car_inspection_type = item_in.car_inspection_type
    registration_first_date = item_in.registration_first_date
    offer_filter, count = crud.offer.search_offers(
        db=db,
        skip=skip,
        limit=limit,
        maker=maker,
        car_type=car_type,
        grade=grade,
        sales_period_start_from=sales_period_start_from,
        sales_period_start_to=sales_period_start_to,
        registration_end_date_from=registration_end_date_from,
        registration_end_date_to=registration_end_date_to,
        car_mileage_from=car_mileage_from,
        car_mileage_to=car_mileage_to,
        offer_status=offer_status,
        area=area,
        aggregation_wholesale_price_market_from=aggregation_wholesale_price_market_from,
        aggregation_wholesale_price_market_to=aggregation_wholesale_price_market_to,
        buy_now_total_price_from=buy_now_total_price_from,
        buy_now_total_price_to=buy_now_total_price_to,
        insert_at_from=insert_at_from,
        insert_at_to=insert_at_to,
        chassis_number=chassis_number,
        car_inspection_type=car_inspection_type,
        registration_first_date=registration_first_date
    )
    offers = jsonable_encoder(offer_filter)
    # format offer status
    for item in offers:
        item['sales_period_start'] = format_response_sales_period_start(item['sales_period_start'])
        item['offer_out_store_name'] = crud.offer.get_store_name(db, item['offer_out_store_id'])[0]
        item['offer_out_company_name'] = crud.offer.get_store_name(db, item['offer_out_store_id'])[2]
        item['offer_in_store_name'] = crud.offer.get_store_name(db, item['offer_in_store_id'])[0]
        item['offer_in_company_name'] = crud.offer.get_store_name(db, item['offer_in_store_id'])[2]
        item['time_offer'] = utc_to_jst(item['time_offer'])
        item.pop('offer_out_store_id')
        item.pop('offer_in_store_id')
        offer_status_decs = crud.m_division.get_status_description(db, div_name='offer_status',
                                                                   param=item['offer_status'])
        item["offer_status_number"] = item["offer_status"]
        item["offer_status"] = offer_status_decs[0]
        item['last_message_datetime'] = utc_to_jst(item['last_message_datetime']) if item[
            'last_message_datetime'] else None
    re = {'total': count, 'limit': limit, 'offset': skip, 'results': offers}
    r = json.dumps(re)
    return JSONResponse(content=json.loads(r))
