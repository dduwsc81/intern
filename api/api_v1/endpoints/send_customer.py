from typing import Any, List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app import crud, schemas, models
from fastapi.responses import JSONResponse
from app.api import deps
from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from jose import jwt
from starlette.requests import Request
import json
from app.schemas.standard_incentive import StandardIncentive
from app.services import mail
from app.constants import Const
from app.utils import create_request_send_mail, check_lotas_tech
from fastapi.security import OAuth2PasswordBearer
from .generate_token import get_cognito_token
from app.services import api_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/{id}", response_model=schemas.SendCustomer)
def get_send_customer(
        id: int,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get detail request send customer.
    """
    send_customer = crud.send_customer.get_send_customer(db=db, send_customer_id=id)
    return JSONResponse(send_customer)


@router.post("/list_send_request", response_model=List[schemas.SendCustomer])
def get_send_customer_list(
        item_in: schemas.SendCustomerSendingRequest,
        *,
        db: Session = Depends(deps.get_db),
        page: int = 1,
        page_size: int = 10,
        requests: Request
) -> Any:
    """
    Get list request send customer.
    """
    skip = (page - 1) * page_size
    limit = page_size
    sort = requests.query_params.get("sort") if "sort" in requests.query_params.keys() else None
    send_customer_at_from = item_in.send_customer_at_from if item_in.send_customer_at_from else None
    send_customer_at_to = item_in.send_customer_at_to if item_in.send_customer_at_to else None
    send_item_type_code = item_in.send_item_type_code if item_in.send_item_type_code else None
    send_status = item_in.send_status if item_in.send_status else None
    maker = item_in.maker if item_in.maker else None
    car_type = item_in.car_type if item_in.car_type else None
    customer_last_name = item_in.customer_last_name if item_in.customer_last_name else None
    customer_first_name = item_in.customer_first_name if item_in.customer_first_name else None
    from_company_name = item_in.from_company_name if item_in.from_company_name else None
    from_store_name = item_in.from_store_name if item_in.from_store_name else None
    to_company_name = item_in.to_company_name if item_in.to_company_name else None
    to_store_name = item_in.to_store_name if item_in.to_store_name else None
    car_registration_number = item_in.car_registration_number if item_in.car_registration_number else None
    list_requests, total = crud.send_customer.get_list_requests(db=db, skip=skip, limit=limit, sort=sort,
                                                                send_customer_at_from=send_customer_at_from,
                                                                send_customer_at_to=send_customer_at_to,
                                                                send_item_type_code=send_item_type_code,
                                                                send_status=send_status, maker=maker, car_type=car_type,
                                                                customer_last_name=customer_last_name,
                                                                customer_first_name=customer_first_name,
                                                                from_company_name=from_company_name,
                                                                from_store_name=from_store_name,
                                                                to_company_name=to_company_name,
                                                                to_store_name=to_store_name,
                                                                car_registration_number=car_registration_number)
    re = {'total': total, 'limit': limit, 'offset': skip, 'results': list_requests}
    r = json.dumps(re)
    return JSONResponse(content=json.loads(r))


@router.put("/{id}", response_model=schemas.SendCustomer)
def update_send_customer(
        id: int,
        item_in: schemas.SendCustomerUpdate,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update request send customer.
    """
    send_customer = crud.send_customer.update_send_customer_by_id(
        db=db, obj_in=item_in, id=id
    )

    """
    Send email
    """
    send_mail_status = dict()

    # get company code, store code from send_customer table
    company_store_code = crud.send_customer.get_company_store_code_by_id(db, id)
    from_company_code = company_store_code["from_company_code"]
    from_store_code = company_store_code["from_store_code"]
    to_company_code = company_store_code["to_company_code"]
    to_store_code = company_store_code["to_store_code"]

    sender_sp1, sender_mail_sp1 = get_sender_mail(db, from_company_code)
    sender_sp2, sender_mail_sp2 = get_sender_mail(db, to_company_code)

    # get email address of SP1
    mail_address_sp1 = crud.send_customer.get_mail_address(db, 2, from_company_code, from_store_code)

    # get email address of SP2
    mail_address_sp2 = crud.send_customer.get_mail_address(db, 2, to_company_code, to_store_code)

    # Send mail to SP1
    if sender_mail_sp1 and mail_address_sp1:
        # get company name, store name
        store_name_sp1, company_name_sp1 = crud.send_customer.get_store_and_company_name(db,
                                                                                         from_store_code,
                                                                                         from_company_code
                                                                                         )

        # get url detail of sp1
        url_detail_sp1 = crud.send_customer.get_url_detail(db, from_company_code, id, True)
        params_sp1 = {
            "companyName": company_name_sp1,
            "storeName": store_name_sp1,
            "contentUrl": url_detail_sp1
        }

        # get title and content mail of SP1
        mail_format_sp1 = crud.send_customer.get_mail_format(db=db, template_type=7)

        request_sp1 = create_request_send_mail(params_sp1, mail_address_sp1, sender_sp1, sender_mail_sp1, mail_format_sp1)
        if mail_format_sp1 and url_detail_sp1:
            try:
                send_mail_status["send_to_sp1"] = mail.send_mail(request_sp1)
            except Exception as err:
                send_mail_status["send_to_sp1"] = f"FAIL - {err}"

    # Send mail to SP2
    if sender_mail_sp2 and mail_address_sp2:
        # get company name, store name
        store_name_sp2, company_name_sp2 = crud.send_customer.get_store_and_company_name(db,
                                                                                         to_store_code,
                                                                                         to_company_code
                                                                                         )

        # get url detail of sp2
        url_detail_sp2 = crud.send_customer.get_url_detail(db, to_company_code, id, False)

        params_sp2 = {
            "companyName": company_name_sp2,
            "storeName": store_name_sp2,
            "contentUrl": url_detail_sp2
        }

        # get title and content mail of SP2
        mail_format_sp2 = crud.send_customer.get_mail_format(db=db, template_type=8)

        request_sp2 = create_request_send_mail(params_sp2, mail_address_sp2, sender_sp2, sender_mail_sp2, mail_format_sp2)
        if mail_format_sp2 and url_detail_sp2:
            try:
                send_mail_status["send_to_sp2"] = mail.send_mail(request_sp2)
            except Exception as err:
                send_mail_status["send_to_sp2"] = f"FAIL - {err}"

    send_customer.send_mail_status = send_mail_status
    return send_customer


@router.put("/incentive/{id}", response_model=schemas.SendCustomer)
def update_send_customer(
        id: int,
        item_in: schemas.SendCustomerIncentive,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update request send customer.
    """
    send_customer = crud.send_customer.update_incentive_by_id(
        db=db, obj_in=item_in, id=id
    )
    return send_customer

@router.post("/fg_incentive_info")
def get_fg_incentive_info(
        item_in: schemas.SendCustomerInfo,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get fg_incentive_info.
    """
    send_customer_at_from = item_in.send_customer_at_from
    send_customer_at_to = item_in.send_customer_at_to
    fg_incentive_info = crud.send_customer.get_fg_incentive_info(
        db=db,
        send_customer_at_from=send_customer_at_from,
        send_customer_at_to=send_customer_at_to
    )
    return fg_incentive_info


@router.post("/list_fg_incentive")
def get_list_fg_info(
        item_in: schemas.SendCustomerFG,
        *,
        db: Session = Depends(deps.get_db),
        page: int = 1,
        page_size: int = 10,
        requests: Request
) -> Any:
    """
    Get list fg_incentive.
    """
    skip = (page - 1) * page_size
    limit = page_size
    sort = requests.query_params.get("sort") if "sort" in requests.query_params.keys() else None
    send_customer_at_from = item_in.send_customer_at_from if item_in.send_customer_at_from else None
    send_customer_at_to = item_in.send_customer_at_to if item_in.send_customer_at_to else None
    send_item_type_code = item_in.send_item_type_code if item_in.send_item_type_code else None
    type_status = item_in.type_status if item_in.type_status else None
    from_company_code = item_in.from_company_code if item_in.from_company_code else None
    from_store_code = item_in.from_store_code if item_in.from_store_code else None
    to_company_code = item_in.to_company_code if item_in.to_company_code else None
    to_store_code = item_in.to_store_code if item_in.to_store_code else None
    list_requests, total, fg_incentive_total = crud.send_customer.get_list_fg_info(
         db=db, skip=skip, limit=limit,
         sort=sort,
         send_customer_at_from=send_customer_at_from,
         send_customer_at_to=send_customer_at_to,
         send_item_type_code=send_item_type_code,
         type_status=type_status,
         from_company_code=from_company_code,
         from_store_code=from_store_code,
         to_company_code=to_company_code,
         to_store_code=to_store_code)
    re = {'total': total, 'limit': limit, 'offset': skip, 'fg_incentive_total': fg_incentive_total,
          'results': list_requests}
    r = json.dumps(re)
    return JSONResponse(content=json.loads(r))


@router.post("/get_list_standard_incentive", response_model=List[StandardIncentive])
def get_list_standard_incentive(
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get list standard incentive.
    """
    list_standard_incentive = crud.send_customer.get_list_standard_incentive(db)
    return list_standard_incentive


@router.post("/send_customer_chat_group", response_model=schemas.ResponseSendCustomerChatGroup)
def create_send_customer_chat_group(
    item_in: schemas.RequestSendCustomerChatGroup,
    *,
    db: Session = Depends(deps.get_db),
    token: str = Depends(oauth2_scheme)
) -> Any:
    """
    Create new send customer.
    """
    claims = jwt.get_unverified_claims(token)
    cognito_id = claims["cognito_id"]
    chat_group_info, custom_token = crud.send_customer.create_send_customer_chat_group(
        db=db, obj_in=item_in, cognito_id=cognito_id
    )
    chat_group_info = jsonable_encoder(chat_group_info)
    chat_group_info["token_firebase"] = custom_token
    return chat_group_info


@router.post("/create_survey_url")
def create_survey_url(
        item_in: schemas.SurveyUrlSettingCreate,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Create survey url
    """
    # check exist survey url
    exist_survey_url_data = crud.send_customer.check_exist_survey_url(db=db, obj_in=item_in)
    if exist_survey_url_data:
        survey_url_short = exist_survey_url_data["survey_url_short"]
    else:
        survey_url_full = crud.send_customer.create_survey_url(db=db, obj_in=item_in)

        # create short url
        cognito_token = get_cognito_token(db, item_in.company_code)
        token = "Bearer " + cognito_token['token']
        url = cognito_token['base_url'] + "/v1/line/shortUrls"
        data = {
            "total": 1,
            "urls": [survey_url_full]
        }

        result = api_service.call_api(
            http_type="post",
            token=token,
            url=url,
            data=data
        )

        survey_url_short = result["urls"][0]

        # save survey url to db
        crud.send_customer.save_survey_url(db, item_in, survey_url_full, survey_url_short)

    return survey_url_short


def get_sender_mail(db, company_code):
    sender = crud.send_customer.get_config_mail(db, Const.CONFIG_MAIL["DIV_MAIL"], Const.CONFIG_MAIL["SENDER"])

    sender_mail = crud.send_customer.get_config_mail(db, Const.CONFIG_MAIL["DIV_MAIL"],
                                                     Const.CONFIG_MAIL["SENDER_EMAIL"])

    # check lotas tech
    is_lotas = check_lotas_tech(db, company_code)
    if is_lotas:
        sender = crud.send_customer.get_config_mail(db, Const.CONFIG_MAIL["DIV_MAIL"],
                                                    Const.CONFIG_MAIL["SENDER_LOTAS"])
        sender_mail = crud.send_customer.get_config_mail(db, Const.CONFIG_MAIL["DIV_MAIL"],
                                                         Const.CONFIG_MAIL["SENDER_EMAIL_LOTAS"])

    return sender, sender_mail
