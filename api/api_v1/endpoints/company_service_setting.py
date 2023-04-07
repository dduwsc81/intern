from typing import Any, Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from app.api import deps
from .generate_token import get_cognito_token
import requests
from sqlalchemy.orm import Session
from app import schemas
from app.services import api_service
from app.models.m_system_param import MSystemParam
from app.constants import Const

router = APIRouter()
session = requests.Session()
REQUEST_TIMEOUT = 30


@router.get("/{company_code}/store/{store_code}/working_time_setting")
def get_setting_working_time(
    company_code,
    store_code,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + f"/v1/store/{store_code}/workingTimeSetting"
    result = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url
    )
    return result


@router.post("/{company_code}/store/{store_code}/working_time_setting")
def update_setting_working_time(
    *,
    company_code,
    store_code,
    item_in: schemas.StoreUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + f"/v1/store/{store_code}/workingTimeSetting"
    data = jsonable_encoder(item_in)
    result = api_service.call_api(
        http_type=Const.HttpMethod.POST,
        token=token,
        url=url,
        data=data
    )
    return result


@router.get("/{company_code}/store/{store_code}/store_service_link")
def get_store_service_link(
    company_code,
    store_code,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + f"/v1/store/{store_code}/configService"
    result = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url
    )
    return result


@router.post("/{company_code}/store/{store_code}/store_service_link")
def update_store_service_link(
    *,
    company_code,
    store_code,
    item_in: schemas.StoreServiceLinkRequest,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + f"/v1/store/{store_code}/configService"
    data = jsonable_encoder(item_in)
    result = api_service.call_api(
        http_type=Const.HttpMethod.POST,
        token=token,
        url=url,
        data=data
    )
    return result


@router.get("/{company_code}/company_policy")
def get_company_policy(
    company_code,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + "/v1/company/companyPolicy"
    result = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url
    )
    return result


@router.put("/{company_code}/company_policy")
def update_company_policy(
    *,
    company_code,
    db: Session = Depends(deps.get_db),
    item_in: schemas.CompanyPolicyUpdate
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + "/v1/company/companyPolicy"
    data = jsonable_encoder(item_in)
    result = api_service.call_api(
        http_type=Const.HttpMethod.PUT,
        token=token,
        url=url,
        data=data
    )
    return result


@router.get("/company_list")
def get_company_list(
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, '90000017')
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + "/v1/getAllListCompany?limit=300"
    result = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url
    )
    return result


@router.get("/{company_code}/general_info/{store_code}")
def get_company_general_info(
    company_code,
    store_code,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + f"/v1/generalInfo/{store_code}"
    result = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url
    )
    return result


@router.put("/{company_code}/general_info/{store_code}")
def update_company_general_info(
    *,
    company_code,
    store_code,
    db: Session = Depends(deps.get_db),
    item_in: schemas.CompanyInfoUpdate
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + f"/v1/generalInfo/{store_code}"
    data = jsonable_encoder(item_in)
    result = api_service.call_api(
        http_type=Const.HttpMethod.PUT,
        token=token,
        url=url,
        data=data
    )
    return result


@router.get("/stores/{company_code}")
def get_all_store(
    company_code,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + "/v1/companyStores"
    params = {
        'companyCode': company_code
    }
    result = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url,
        params=params
    )
    return result


@router.get("/company_service_info/{company_code}")
def get_company_service_info(
    company_code,
    db: Session = Depends(deps.get_db)
) -> Any:
    result = {}
    cognito_token = get_cognito_token(db, company_code)
    base_url = cognito_token['base_url']
    url_prefecture = base_url + "/v1/prefectures"
    url_area = base_url + "/v1/area"
    url_service = base_url + "/v1/getAllListService"
    token = "Bearer " + cognito_token['token']
    result_area = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url_area
        )
    result_prefecture = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url_prefecture
        )
    result_service = api_service.call_api(
        http_type=Const.HttpMethod.GET,
        token=token,
        url=url_service
        )
    result["area_code"] = result_area
    result["perfecture_code"] = result_prefecture
    result["services_code"] = result_service
    return result


@router.get("/reservation_url/{company_code}")
def get_reservation_url(
    *,
    company_code,
    db: Session = Depends(deps.get_db),
    storeCode: Optional[str] = None
) -> Any:
    data = schemas.ReservationUrlStatus()
    url_survey = (db.query(MSystemParam.desc1)
                  .filter(
                      MSystemParam.div == Const.CONFIG_RESERVE_URL["DIV_RESERVE"])
                  .first())
    catalog_authen = (db.query(MSystemParam.desc1,
                               MSystemParam.desc2)
                      .filter(
                          MSystemParam.div == Const.CONFIG_RESERVE_URL["DIV_CATALOG"])
                      .first())

    data.catalogUrl, data.catalogKey = catalog_authen
    data.storeCode = storeCode if storeCode else ""
    data = data.json()
    data = f"[{data}]"
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']

    url = cognito_token['base_url'] + "/v1/messages/reservation-url"
    reservation_token = api_service.call_api(
        http_type=Const.HttpMethod.POST,
        token=token,
        url=url,
        list_data=data
    )

    url_token = api_service.encode_btoa(reservation_token['results'][0]['code'])
    suffix_url = api_service.encode_btoa(company_code)
    base_url = f"{url_survey[0]}/new-booking/?token={url_token}&companyCode={suffix_url}"
    short_url = cognito_token['base_url'] + "/v1/line/shortUrls"

    json = {}
    json["total"] = 1
    json["urls"] = [base_url]

    data = jsonable_encoder(json)

    short_url = api_service.call_api(
        http_type=Const.HttpMethod.POST,
        token=token,
        url=short_url,
        data=data
    )

    return short_url

@router.put("/{company_code}/display_store_update")
def update_display_store(
    *,
    company_code,
    item_in: schemas.ListDisplayStore,
    db: Session = Depends(deps.get_db)
) -> Any:
    cognito_token = get_cognito_token(db, company_code)
    token = "Bearer " + cognito_token['token']
    url = cognito_token['base_url'] + "/v1/updateDisplayStore"
    json = {
        "companyCode": company_code,
        "listDisplayStoreUpdate": item_in.list_display_store_update
    }
    data = jsonable_encoder(json)
    result = api_service.call_api(
        http_type=Const.HttpMethod.PUT,
        token=token,
        url=url,
        data=data
    )
    return result
