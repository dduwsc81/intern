from fastapi import APIRouter

from api.api_v1.endpoints import car_training, book, author, category
# from app.api.api_v1.endpoints import items
from app.api.api_v1.endpoints import cars
# from app.api.api_v1.endpoints import car_details
from app.api.api_v1.endpoints import offers
from app.api.api_v1.endpoints import register_sales
from app.api.api_v1.endpoints import m_prefectures
from app.api.api_v1.endpoints import chat_group
from app.api.api_v1.endpoints import health_check_page
from app.api.api_v1.endpoints import m_distance_travelled
from app.api.api_v1.endpoints import m_year
from app.api.api_v1.endpoints import m_price
from app.api.api_v1.endpoints import send_customer
from app.api.api_v1.endpoints import m_company
from app.api.api_v1.endpoints import send_item_type_unit
from app.api.api_v1.endpoints import code_master
from app.api.api_v1.endpoints import menu_setting
from app.api.api_v1.endpoints import option_setting
from app.api.api_v1.endpoints import service_fee
from app.api.api_v1.endpoints import reservation
from app.api.api_v1.endpoints import negotiation
from app.api.api_v1.endpoints import car_market
from app.api.api_v1.endpoints import utilization
from app.api.api_v1.endpoints import m_rate
from app.api.api_v1.endpoints import estimate
from app.api.api_v1.endpoints import options
# from app.api.api_v1.endpoints import store
from app.api.api_v1.endpoints import car_transaction_history
from app.api.api_v1.endpoints import company_service_setting
from app.api.api_v1.endpoints import system_maintainance
from app.api.api_v1.endpoints import search_condition
from app.api.api_v1.endpoints import search_condition_detail
from app.api.api_v1.endpoints import staff
from app.api.api_v1.endpoints import m_division
from app.api.api_v1.endpoints import company_info_setting
from app.api.api_v1.endpoints import option_group
from app.api.api_v1.endpoints import customers
from app.api.api_v1.endpoints import assess
from app.api.api_v1.endpoints import activity_memo



api_router = APIRouter()
# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(cars.router, prefix="/cars", tags=["cars"])
# api_router.include_router(car_details.router, prefix="/cardetails", tags=["cardetails"])
api_router.include_router(offers.router, prefix="/offers", tags=["offers"])
api_router.include_router(register_sales.router, prefix="/register_sales", tags=["register_sales"])
api_router.include_router(m_prefectures.router, prefix="/m_prefectures", tags=["m_prefectures"])
api_router.include_router(chat_group.router, prefix="/chat_groups", tags=["chat_groups"])
api_router.include_router(health_check_page.router, prefix="/health_check", tags=["health_check"])
api_router.include_router(m_distance_travelled.router, prefix="/m-distance-travelled", tags=["m-distance-travelled"])
api_router.include_router(m_year.router, prefix="/m-year", tags=["m-year"])
api_router.include_router(m_price.router, prefix="/m-price", tags=["m-price"])
api_router.include_router(send_customer.router, prefix="/send_customer", tags=["send_customer"])
api_router.include_router(m_company.router, prefix="/m_company", tags=["m_company"])
api_router.include_router(send_item_type_unit.router, prefix="/service_unit", tags=["send_item_type_unit"])
api_router.include_router(code_master.router, prefix="/code_master", tags=["code_master"])
api_router.include_router(menu_setting.router, prefix="/menu_setting", tags=["menu_setting"])
api_router.include_router(option_setting.router, prefix="/option_setting", tags=["option_setting"])
api_router.include_router(service_fee.router, prefix="/service_fee", tags=["service_fee"])
api_router.include_router(reservation.router, prefix="/reservation", tags=["reservation"])
api_router.include_router(negotiation.router, prefix="/negotiation", tags=["negotiation"])
api_router.include_router(car_market.router, prefix="/car-market", tags=["car_market"])
api_router.include_router(utilization.router, prefix="/utilization", tags=["utilization"])
api_router.include_router(m_rate.router, prefix="/m-rate", tags=["m-rate"])
api_router.include_router(estimate.router, prefix="/estimation", tags=["estimation"])
api_router.include_router(options.router, prefix="/options", tags=["options"])
# api_router.include_router(store.router, prefix="/company", tags=["store_setting"])
api_router.include_router(car_transaction_history.router, prefix="/car-transaction-history", tags=["car-transaction-history"])
api_router.include_router(company_service_setting.router, prefix="/company", tags=["service_setting"])
api_router.include_router(system_maintainance.router, prefix="/system_maintainance", tags=["system"])
api_router.include_router(search_condition.router, prefix="/search-condition", tags=["search-condition"])
api_router.include_router(search_condition_detail.router, prefix="/search-condition-detail", tags=["search-condition-detail"],)
api_router.include_router(staff.router, prefix="/staff", tags=["staff"])
api_router.include_router(m_division.router, prefix="/m-division", tags=["m-division"])
api_router.include_router(company_info_setting.router, prefix="/company-info", tags=["company-info"])
api_router.include_router(option_group.router, prefix="/option-group", tags=["option-group"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(assess.router, prefix="/assess", tags=["assess"])
api_router.include_router(activity_memo.router, prefix="/activity_memo", tags=["activity_memo"])

api_router.include_router(car_training.router, prefix="/car_training", tags=['car_training'])
api_router.include_router(book.router, prefix="/book", tags=['Training2'])
api_router.include_router(author.router, prefix="/author", tags=['Training2'])
api_router.include_router(category.router, prefix="/category", tags=["Training2"])
