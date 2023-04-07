from typing import Any, Dict, Union, List

from sqlalchemy.orm import Session

from app.constants import Const
from app.crud.base import CRUDBase
from app.models.estimate import Estimate
from app.models.car_market import CarMarket
from app.models.use_options_manager import UseOptionsManager
from app.schemas.estimate import EstimateCreate, EstimateUpdate
from datetime import datetime
from app.utils import round_decimal, round_number
from app import crud

ESTIMATE_TYPE = {
    "SELLER": 1,
    "BUYER": 2
}

REGISTER_SALE_TYPE = {
    "DIRECT": 1,
    "BROKERAGE": 2
}

DIV_BUYER = 1
CONSIST_TAX_RATE = 1.1
TAX_RATE = 0.1

INIT_VALUE = 0


class CRUDEstimation(CRUDBase[Estimate, EstimateCreate, EstimateUpdate]):

    # get estimate
    def get_estimation(self, db: Session, *, car_id: int, store_id: int) -> Any:
        # Check current store is buyer or seller
        car_market_store_id = db.query(CarMarket.store_code) \
            .filter(CarMarket.car_id == car_id,
                    CarMarket.delete_flag == 0) \
            .first()

        estimate = None
        list_option_manager = None

        if car_market_store_id is not None:
            car_market_store_id = int(car_market_store_id[0])

            # return estimate type depends on seller or buyer
            if car_market_store_id == store_id:
                estimate_type = ESTIMATE_TYPE["SELLER"]
            else:
                estimate_type = ESTIMATE_TYPE["BUYER"]

            estimate = db.query(Estimate) \
                .filter(Estimate.car_id == car_id,
                        Estimate.estimate_type == estimate_type,
                        Estimate.delete_flag == Const.DEL_FLG_NORMAL) \
                .first()

            if estimate is not None:
                list_option_manager = db.query(UseOptionsManager) \
                    .filter(UseOptionsManager.car_id == car_id,
                            UseOptionsManager.estimate_id == estimate.id,
                            UseOptionsManager.delete_flag == Const.DEL_FLG_NORMAL) \
                    .all()

        return estimate, list_option_manager

    def update_estimate(self, db: Session, item_in: Union[EstimateUpdate, Dict], update_id: int) -> Any:
        # get Tax rate from m_division
        tax_rate_obj = crud.m_division.get_m_division_by_div(db=db, div=Const.TAX_RATE_DIV)
        tax_rate = tax_rate_obj[0].param / 100

        # get estimate
        obj_update = db.query(Estimate)\
                        .filter(Estimate.id == item_in.id, Estimate.delete_flag == Const.DEL_FLG_NORMAL)\
                        .first()
        # convert obj_in to dict
        if isinstance(item_in, dict):
            update_data = item_in
        else:
            update_data = item_in.dict(exclude_unset=True)
        # update attributes have in obj_in
        for field in update_data.keys():
            setattr(obj_update, field, update_data[field])
        obj_update.update_at = datetime.utcnow()
        obj_update.update_id = update_id

        # get option
        option_obj = db.query(UseOptionsManager)\
                        .filter(UseOptionsManager.estimate_id == item_in.id,
                                UseOptionsManager.option_id == item_in.option_id,
                                UseOptionsManager.delete_flag == Const.DEL_FLG_NORMAL)\
                        .first()

        option_obj.option_fee = item_in.option_fee
        option_obj.option_fee_tax = item_in.option_fee * (1 + tax_rate) if item_in.option_fee is not None else None
        option_obj.update_at = datetime.utcnow()
        option_obj.update_id = update_id

        # calculate estimate
        obj_update = self.calculate_estimate(db=db, item_in=obj_update,
                                             register_sale_type=item_in.register_sale_type)

        # update db
        db.add(obj_update)
        db.flush()
        return obj_update

    def calculate_estimate(self, db: Session, item_in: Union[EstimateCreate, Estimate], register_sale_type: int):
        # get Tax rate from m_division
        tax_rate_obj = crud.m_division.get_m_division_by_div(db=db, div=Const.TAX_RATE_DIV)
        tax_rate = tax_rate_obj[0].param / 100
        consist_tax_rate = 1 + tax_rate
        # Get all options
        option_obj = (
            db.query(UseOptionsManager)
                .filter(UseOptionsManager.estimate_id == item_in.id,
                        UseOptionsManager.delete_flag == Const.DEL_FLG_NORMAL)
                .all()
        )

        # Calculate total option fee
        total_option_fee = 0

        if option_obj is not None:
            for option in option_obj:
                if option.option_fee is not None:
                    total_option_fee += option.option_fee

        # check value of option_fee
        if item_in.options_fee is None:
            item_in.option_fee_tax = None
        else:
            item_in.options_fee = total_option_fee
            item_in.option_fee_tax = round_decimal(total_option_fee * consist_tax_rate)

        # Get market fee from m_service
        market_fee_obj = crud.m_service.get_service_by_code(db=db, service_code=Const.ServiceCode.MARKET_FEE)
        market_fee = market_fee_obj.price

        item_in.market_fee = market_fee
        item_in.market_fee_tax = round_decimal(market_fee * consist_tax_rate)
        item_in.hope_sale_base_price = round_number(item_in.hope_sale_base_price)
        item_in.hope_sale_base_price_tax = round_decimal(item_in.hope_sale_base_price * consist_tax_rate)

        # calculate estimate if
        # professional mode (register_sale_type = DIRECT) or
        # CtoC mode (register_sale_type != DIRECT)
        if register_sale_type == REGISTER_SALE_TYPE["DIRECT"]:
            margin_fee = None
            if item_in.margin_rate is not None:
                margin_fee = round_decimal(item_in.hope_sale_base_price * item_in.margin_rate / 100)
            if item_in.margin_fee is not None:
                margin_fee = item_in.margin_fee
            item_in.business_amount_tax = \
                round_decimal((item_in.hope_sale_base_price + item_in.market_fee + total_option_fee) * consist_tax_rate)
            item_in.business_amount = \
                round_decimal(item_in.business_amount_tax - item_in.business_amount_tax * tax_rate)
            item_in.customer_amount_tax = \
                round_decimal((item_in.hope_sale_base_price + margin_fee + total_option_fee) * consist_tax_rate)
            item_in.customer_amount = \
                round_decimal(item_in.customer_amount_tax - item_in.customer_amount_tax * tax_rate)
        else:
            brokerage_fee = None
            if item_in.brokerage_rate is not None:
                brokerage_fee = round_decimal(item_in.hope_sale_base_price * item_in.brokerage_rate / 100)
            if item_in.brokerage_fee is not None:
                brokerage_fee = item_in.brokerage_fee
            item_in.business_amount_tax = round_decimal((brokerage_fee - item_in.market_fee) * consist_tax_rate)
            item_in.business_amount = \
                round_decimal(item_in.business_amount_tax - item_in.business_amount_tax * tax_rate)
            item_in.customer_amount_tax = \
                round_decimal(item_in.hope_sale_base_price + (brokerage_fee + total_option_fee) * consist_tax_rate)
            item_in.customer_amount = \
                round_decimal(item_in.customer_amount_tax - item_in.customer_amount_tax * tax_rate)

        return item_in

    def delete_estimate_by_id(self, db: Session, *, user_id: int, id: int,) -> Any:
        db_obj = (
            db.query(self.model)
            .filter(
                Estimate.id == id,
                Estimate.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )
        if not db_obj:
           return None
        db_obj.delete_at = datetime.utcnow()
        db_obj.delete_id = user_id
        db_obj.delete_flag = Const.DEL_FLG_DELETE
        db.add(db_obj)
        db.flush()
        return db_obj

estimation = CRUDEstimation(Estimate)
