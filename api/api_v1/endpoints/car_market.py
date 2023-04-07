import logging
from typing import Any, Optional
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

from app.constants import Const

DIV_SELLER = 2
DIV_BUYER = 1
DELETE_REGISTER = (2, 3)  # SALE_EXPIRED, STOP_SALE
DELETE_NEGO = [4]

logger = logging.getLogger()

router = APIRouter()


@router.put("/car-status")
def update_car_status(
        item_in: schemas.UpdateCarStatus,
        db: Session = Depends(deps.get_db),
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Update status relate car.
    """
    car_id = item_in.car_id
    update_id = Const.ADMIN_ID
    car_market = handler_car_status(item_in, db, update_id, car_id)
    register_sale = handler_register(item_in, db, update_id, car_id)
    assess = handler_assess(item_in, db, update_id, register_sale=register_sale)
    negotiation = handler_negotiation(item_in, db, update_id, car_id)
    estimate_id = handler_estimate(item_in, db, update_id, negotiation=negotiation, register_sale=register_sale)
    handler_use_options_manager(item_in, db, update_id)
    purchase = handler_purchase(item_in, db, update_id, negotiation=negotiation, register_sale=register_sale)
    handler_utilization_service(item_in, db, update_id, car_id,
                                register_sale=register_sale,
                                negotiation=negotiation,
                                purchase=purchase)
    return JSONResponse(content=True, status_code=200)



def handler_car_status(item_in, db, update_id, car_id, **kwargs):
    if item_in.car_status is not None:
        car_market = crud.car_market.update_car_status_by_car_id(db=db,
                                                                 car_id=car_id,
                                                                 car_status=item_in.car_status,
                                                                 update_id=update_id)
        return car_market


def handler_register(item_in, db, update_id, car_id, **kwargs):
    if item_in.register_sale_status is not None:
        register_sale = crud.register_sale.update_register_sale_status(db=db,
                                                                       car_id=car_id,
                                                                       status=item_in.register_sale_status,
                                                                       update_id=update_id, )
        if item_in.register_sale_status in DELETE_REGISTER:
            crud.register_sale.delete_by_update_deleteflag_bycarcode(db=db, car_id=car_id)

        return register_sale


def handler_assess(item_in, db, update_id, **kwargs):
    # delete assess when delete register sale
    register_sale =  kwargs.get("register_sale", None)
    if (item_in.register_sale_status == Const.SaleStatus.SALE_EXPIRED
            and register_sale
            and register_sale.assess_id is not None):
        assess = crud.assess.delete_assess_by_id(db=db, id=register_sale.assess_id, user_id=update_id)
        return assess


def handler_negotiation(item_in, db, update_id, car_id, **kwargs):
    if item_in.negotiation_status is not None:
        negotiation = crud.negotiation.update_negotiation_status_by_car_id(db=db,
                                                                           car_id=car_id,
                                                                           negotiation_status=item_in.negotiation_status,
                                                                           update_id=update_id)
        if item_in.negotiation_status in DELETE_NEGO:
            crud.negotiation.delete_by_car_id(db=db, car_id=car_id, delete_id=update_id)
        return negotiation


def handler_estimate(item_in, db, update_id, **kwargs):
    register_sale = kwargs.get("register_sale", None)
    negotiation = kwargs.get("negotiation", None)
    estimate_id = None
    if item_in.negotiation_status in DELETE_NEGO and negotiation is not None:
        estimate_id = negotiation.estimate_id
    else:
        # else get estimate_id from table register_sale
        # check None before get
        if item_in.register_sale_status in DELETE_REGISTER and register_sale is not None:
            estimate_id = register_sale.estimate_id

    # delete estimate of car if have
    if estimate_id is not None:
        estimate = crud.estimation.delete_estimate_by_id(db=db, id=estimate_id, user_id=update_id)
        return estimate


def handler_use_options_manager(item_in, db, update_id, **kwargs):
    estimate = kwargs.get("estimate", None)
    if item_in.negotiation_status in DELETE_NEGO and estimate:
        use_options_manager = crud.use_options_manager.delete_use_option_manager_by_estimate_id(
            db=db,
            user_id=update_id,
            estimate_id=estimate.id)
        return use_options_manager


def handler_purchase(item_in, db, update_id, **kwargs):
    # purchase
    negotiation = kwargs.get("negotiation", None)
    if negotiation is not None:
        purchase = schemas.PurchaseUpdate(negotiation_id=negotiation.id,
                                          status=item_in.purchase_status)
        if item_in.purchase_status == Const.PURCHASE_CLOSE:
            purchase.close_datetime = datetime.utcnow()
        purchase = crud.purchase.update_status_purchase_by_negotiation_id(db=db,
                                                                          update_id=update_id,
                                                                          obj_in=purchase)
        return purchase


def handler_utilization_service(item_in, db,update_id, car_id, **kwargs):
    register_sale = kwargs.get("register_sale", None)
    negotiation = kwargs.get("negotiation", None)
    purchase = kwargs.get("purchase", None)
    if item_in.purchase_status == Const.PURCHASE_CLOSE:
        if register_sale and negotiation:
            service = crud.m_service.get_service_by_code(db=db,
                                                         service_code=Const.ServiceCode.MARKET_FEE)
            us = schemas.UtilizationServiceCreate(
                car_id=car_id,
                register_sale_id=register_sale.id,
                negotiation_id=negotiation.id,
                service_cd=service.service_cd,
                service_name=service.service_name,
                payment_amount=service.price,
                utilization_datetime=purchase.close_datetime,
            )

            # create utilization_service for seller
            cg_id_seller = f"{car_id}_{DIV_SELLER}_{negotiation.owner_store_id}"
            cg_seller = crud.chat_group.check_exist_chat_group(db=db,
                                                               firebase_chat_id=cg_id_seller)
            us.contact_id = cg_seller.id
            us.business_store_id = purchase.sale_approve_store_id
            us.business_user_id = purchase.sale_approve_user_id
            us.div = Const.SELL
            us_seller = crud.utilization_service.create_utilization_service(db=db,
                                                                            user_id=update_id,
                                                                            obj_in=us)

            # create utilization_service for buyer
            cg_id_buyer = f"{car_id}_{DIV_BUYER}_{negotiation.negotiation_store_id}"
            cg_buyer = crud.chat_group.check_exist_chat_group(db=db,
                                                              firebase_chat_id=cg_id_buyer)
            us.contact_id = cg_buyer.id
            us.business_store_id = purchase.purchase_store_id
            us.business_user_id = purchase.purchase_user_id
            us.div = Const.BUY
            us_buyer = crud.utilization_service.create_utilization_service(db=db,
                                                                           user_id=update_id,
                                                                           obj_in=us)
