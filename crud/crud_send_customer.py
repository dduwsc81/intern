from sqlalchemy.orm import Session
from typing import Any
from app.crud.base import CRUDBase
from app.models.send_customer import SendCustomer
from app.models.staff import Staff
from app.models.m_company import MCompany
from app.models.store import Store
from app.models.car import Car
from app.models.car_photo import CarPhoto
from app.models.code_master import CodeMaster
from app.models.activity_log import ActivityLog
from app.schemas.send_customer import SendCustomerCreate, SendCustomerUpdate, RequestSendCustomerChatGroup
from sqlalchemy import or_, and_, text, func
from fastapi import HTTPException, status
from ..api.api_v1.endpoints.format_status import *
from fastapi.encoders import jsonable_encoder
from app import crud, schemas
from app.models.standard_incentive import StandardIncentive
from app.constants import Const
from app.models.m_mail_format import MMailFormat
from app.models.tenant_information import TenantInformation
from app.models.notification_mail_address import NotificationMailAddress
from app.models.m_system_param import MSystemParam
from app.models.send_customer_chat_group import SendCustomerChatGroup
import os
from firebase_admin import auth, credentials
from app.schemas.survey_url_setting import SurveyUrlSettingCreate
from app.models.survey_url_setting import SurveyUrlSetting
from app.utils import encode_token


class CRUDSendCustomer(CRUDBase[SendCustomer, SendCustomerCreate, SendCustomerUpdate]):
    CODE_TYPE_STATUS = "send_customer_status_new"
    CODE_TYPE_ITEM = "send_customer_type_code_new"
    STATUS_START = (0, 1)
    STATUS_IN_PROGRESS = (2, 3, 4)
    STATUS_IS_PAID = 4
    STATUS_CANCEL = 5
    STATUS_TYPE_1 = 1
    STATUS_TYPE_2 = 2

    def get_list_requests(self, db: Session, *,
                          send_customer_at_from,
                          send_customer_at_to,
                          send_item_type_code,
                          send_status,
                          maker,
                          car_type,
                          customer_last_name,
                          customer_first_name,
                          from_company_name,
                          from_store_name,
                          to_company_name,
                          to_store_name,
                          car_registration_number,
                          skip: int = 0, limit: int = 10,
                          sort: str,
                          ) -> Any:
        from_company_name_sub = db.query(MCompany.company_code, MCompany.company_name).subquery('from_company_name')
        to_company_name_sub = db.query(MCompany.company_code, MCompany.company_name).subquery('to_company_name')
        from_store_name_sub = db.query(Store.store_code, Store.company_code, Store.store_name).subquery(
            'from_store_name')
        to_store_name_sub = db.query(Store.store_code, Store.company_code, Store.store_name).subquery('to_store_name')
        list_request = db.query(
            self.model.id.label("send_customer_id"),
            self.model.send_customer_code,
            self.model.send_item_type_code,
            self.model.send_customer_at,
            self.model.customer_last_name,
            self.model.customer_first_name,
            self.model.car_maker,
            self.model.car_type,
            self.model.status_flag,
            self.model.send_incentive,
            self.model.fg_incentive,
            self.model.send_incentive_tax,
            self.model.fg_incentive_tax,
            self.model.car_land_transport_office,
            self.model.car_registration_number_type,
            self.model.car_registration_number_kana,
            self.model.car_registration_number,
            self.model.reservation_id,
            self.model.menu_user_price_tax,
            self.model.option_user_price_tax,
            from_company_name_sub.c.company_name.label("from_company_name"),
            to_company_name_sub.c.company_name.label("to_company_name"),
            to_company_name_sub.c.company_code.label('to_company_code'),
            from_store_name_sub.c.store_name.label("from_store_name"),
            to_store_name_sub.c.store_name.label("to_store_name")
        ). \
            outerjoin(from_company_name_sub,
                      from_company_name_sub.c.company_code == SendCustomer.from_company_code). \
            outerjoin(to_company_name_sub, to_company_name_sub.c.company_code == SendCustomer.to_company_code). \
            outerjoin(from_store_name_sub, and_(from_store_name_sub.c.company_code == SendCustomer.from_company_code,
                                                from_store_name_sub.c.store_code == SendCustomer.from_store_code)). \
            outerjoin(to_store_name_sub, and_(to_store_name_sub.c.company_code == SendCustomer.to_company_code,
                                              to_store_name_sub.c.store_code == SendCustomer.to_store_code)). \
            filter(SendCustomer.delete_flag == 0)
        if sort is not None:
            order = convert_sort_key(
                sort,
                {
                    "send_customer_at": ["send_customer_at"],
                    "customer_name": ["customer_last_name", "customer_first_name"],
                    "customer_car": ["car_type", "car_registration_number"],
                    "send_customer_id": ["send_customer_id"]
                },
                "- send_customer_id",
            )
        else:
            order = "- send_customer_id"
        if send_status:
            list_request = list_request.filter(SendCustomer.status_flag.in_(send_status))
        if send_item_type_code:
            list_request = list_request.filter(SendCustomer.send_item_type_code.in_(send_item_type_code))
        if send_customer_at_from:
            list_request = list_request.filter(SendCustomer.send_customer_at >= send_customer_at_from)
        if send_customer_at_to:
            list_request = list_request.filter(SendCustomer.send_customer_at <= send_customer_at_to + " 23:59:59")
        if maker:
            list_request = list_request.filter((SendCustomer.car_maker.like("%{}%".format(maker))))
        if car_type:
            list_request = list_request.filter(or_(SendCustomer.car_type.like("%{}%".format(car_type)),
                                                   SendCustomer.car_type.like(
                                                       "%{}%".format(format_ascii_to_unicode(car_type)))))
        if customer_first_name:
            list_request = list_request.filter(
                or_(
                    SendCustomer.customer_first_name.like("%{}%".format(customer_first_name)),
                    SendCustomer.customer_first_name_kana.like("%{}%".format(customer_first_name))
                )
            )
        if customer_last_name:
            list_request = list_request.filter(
                or_(
                    SendCustomer.customer_last_name.like("%{}%".format(customer_last_name)),
                    SendCustomer.customer_last_name_kana.like("%{}%".format(customer_last_name))
                )
            )
        if from_company_name:
            list_request = list_request.filter(
                or_(from_company_name_sub.c.company_name.like("%{}%".format(from_company_name)),
                    from_company_name_sub.c.company_name.like(
                        "%{}%".format(format_ascii_to_unicode(from_company_name)))))
        if to_company_name:
            list_request = list_request.filter(
                or_(to_company_name_sub.c.company_name.like("%{}%".format(to_company_name)),
                    to_company_name_sub.c.company_name.like(
                        "%{}%".format(format_ascii_to_unicode(to_company_name)))))
        if from_store_name:
            list_request = list_request.filter(
                or_(from_store_name_sub.c.store_name.like("%{}%".format(from_store_name)),
                    from_store_name_sub.c.store_name.like(
                        "%{}%".format(format_ascii_to_unicode(from_store_name)))))
        if to_store_name:
            list_request = list_request.filter(
                or_(to_store_name_sub.c.store_name.like("%{}%".format(to_store_name)),
                    to_store_name_sub.c.store_name.like(
                        "%{}%".format(format_ascii_to_unicode(to_store_name)))))
        if car_registration_number:
            list_request = list_request.filter(
                SendCustomer.car_registration_number.contains(car_registration_number))
        total = list_request.count()
        list_request = (
            list_request.order_by(text(order)).offset(skip).limit(limit).all()
        )
        list_requests = jsonable_encoder(list_request)

        # format list request
        for item in list_requests:
            item["send_customer_at"] = utc_to_jst(item["send_customer_at"]) if item["send_customer_at"] else ""
            item["status"] = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_STATUS,
                                                            code_value=item["status_flag"])
            item["service_name"] = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_ITEM,
                                                                  code_value=item[
                                                                      "send_item_type_code"])
            item['menu'] = crud.menu_setting.get_menu_setting_by_id(db, item['send_customer_id'])
            item['option'] = crud.option_setting.get_option_setting_by_id(db, item['send_customer_id'])
        return list_requests, total

    def get_send_customer(
            self, db: Session, *,
            send_customer_id: int
    ) -> Any:
        send_customer_request = db.query(
            self.model.id.label("send_customer_id"),
            self.model.send_item_type_code,
            self.model.status_flag,
            self.model.customer_last_name,
            self.model.customer_first_name,
            self.model.customer_last_name_kana,
            self.model.customer_first_name_kana,
            self.model.customer_address1,
            self.model.customer_address2,
            self.model.customer_address3,
            self.model.customer_phone_number,
            self.model.customer_cellphone_number,
            self.model.customer_email,
            self.model.customer_zip_code,
            self.model.car_code,
            self.model.car_type,
            self.model.car_maker,
            self.model.car_grade,
            self.model.car_registration_first_date,
            self.model.car_registration_end_date,
            self.model.car_mileage,
            self.model.car_mileage_registration_date,
            self.model.car_land_transport_office,
            self.model.car_registration_number_type,
            self.model.car_registration_number_kana,
            self.model.car_registration_number,
            self.model.send_customer_at,
            self.model.content,
            self.model.reservation_time,
            self.model.from_company_code,
            self.model.from_store_code,
            self.model.to_company_code,
            self.model.to_store_code,
            self.model.contact_option,
            self.model.fg_incentive,
            self.model.send_incentive,
            self.model.fg_incentive_tax,
            self.model.send_incentive_tax,
            self.model.menu_user_price_tax,
            self.model.option_user_price_tax,
            self.model.reservation_id,
            self.model.paid_type,
            self.model.reservation_classification,
            self.model.tax_rate,
            Staff.last_name.label("staff_last_name"),
            Staff.first_name.label("staff_first_name"),
            Staff.phone_number.label("staff_phone_number"),
            Staff.email.label("staff_email"),
            CarPhoto.url.label("thumbnail_url"),
        ). \
            outerjoin(Car, Car.car_code == SendCustomer.car_code). \
            outerjoin(CarPhoto, (CarPhoto.car_id == Car.id) & (CarPhoto.image_div == 1)). \
            outerjoin(Staff, (Staff.staff_code == SendCustomer.from_staff_code) & (
                Staff.company_code == SendCustomer.from_company_code)). \
            filter(SendCustomer.delete_flag == 0, SendCustomer.id == send_customer_id).first()
        if not send_customer_request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Send customer id  {send_customer_id} not found')

        # format send_customer
        send_customer = jsonable_encoder(send_customer_request)

        # get store's name and company's name
        send_customer["from_store_name"], send_customer[
            "from_company_name"] = self.get_store_and_company_name(db=db, company_code=send_customer[
            "from_company_code"], store_code=send_customer["from_store_code"])
        send_customer["to_store_name"], send_customer[
            "to_company_name"] = self.get_store_and_company_name(db=db, company_code=send_customer[
            "to_company_code"], store_code=send_customer["to_store_code"])

        # get value of status and service
        send_customer["status"] = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_STATUS,
                                                                 code_value=send_customer["status_flag"])
        send_customer["service_name"] = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_ITEM,
                                                                       code_value=send_customer["send_item_type_code"])
        send_customer['menu'] = crud.menu_setting.get_menu_setting_by_id(db, send_customer['send_customer_id'])
        send_customer['option'] = crud.option_setting.get_option_detail(db,
                                                                        send_customer['send_customer_id'],
                                                                        send_customer['tax_rate'])

        # get activity logs with status
        send_customer["activity_log"] = crud.activity_log.get_activity_log_status(db=db,
                                                                                  send_customer_id=send_customer[
                                                                                      "send_customer_id"])

        # format send_customer_at
        send_customer["send_customer_at"] = utc_to_jst(send_customer["send_customer_at"]) if send_customer[
            "send_customer_at"] else ""
        return send_customer

    def get_store_and_company_name(self, db, store_code, company_code):

        # get store by store code and company code
        store = db.query(Store.store_name).filter(Store.store_code == store_code,
                                                  Store.company_code == company_code).first()

        # get company by company code
        company = db.query(MCompany.company_name).filter(MCompany.company_code == company_code).first()
        return store.store_name if store else "", company.company_name if company else ""

    def update_send_customer_by_id(
        self,
        db: Session,
        *,
        obj_in: SendCustomerUpdate,
        id: int,
    ) -> SendCustomer:
        db_obj = (
            db.query(self.model)
            .filter(SendCustomer.id == id, SendCustomer.delete_flag == 0)
            .first()
        )
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Send customer request id {id} not found",
            )
        old_status = db_obj.status_flag
        if obj_in.status_flag is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is invalid or parameters are incorrect",
            )
        if (
                obj_in.status_flag != self.STATUS_CANCEL
                and old_status == self.STATUS_IS_PAID
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is invalid or parameters are incorrect",
            )
        if (
            old_status in self.STATUS_START or old_status in self.STATUS_IN_PROGRESS
        ) & (obj_in.status_flag != self.STATUS_CANCEL):
            if obj_in.status_flag > old_status + 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Request is invalid or parameters are incorrect",
                )
        if obj_in.status_flag == self.STATUS_CANCEL and not obj_in.comment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is invalid or parameters are incorrect",
            )
        if old_status == self.STATUS_CANCEL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Request is invalid or parameters are incorrect",
            )
        db_obj.update_at = datetime.utcnow()
        db_obj.update_id = 88888
        db_obj.status_flag = obj_in.status_flag

        # check exit log
        log = (
            db.query(ActivityLog)
            .filter(
                ActivityLog.send_customer_id == id,
                ActivityLog.status == obj_in.status_flag,
            )
            .first()
        )
        if not log:
            new_log = schemas.ActivityLogCreate()
            new_log.send_customer_id = id
            new_log.status = obj_in.status_flag
            if obj_in.comment and (obj_in.status_flag == self.STATUS_IS_PAID or obj_in.status_flag == self.STATUS_CANCEL):
                new_log.comment = obj_in.comment
            crud.activity_log.create_activity_log(
                db=db, obj_in=new_log, cognito_id=88888
            )
        else:
            log.delete_flag = 0
            log.update_at = datetime.utcnow()
            if obj_in.comment and (obj_in.status_flag == self.STATUS_IS_PAID or obj_in.status_flag == self.STATUS_CANCEL):
                log.comment = obj_in.comment
            update_data = []
            log_backs = (
                db.query(ActivityLog)
                .filter(
                    ActivityLog.send_customer_id == id,
                    ActivityLog.status > obj_in.status_flag,
                )
                .all()
            )
            for log_back in log_backs:
                log_back.delete_flag = 1
                log_back.update_at = datetime.utcnow()
                update_data.append(log_back)
            db.bulk_save_objects(update_data)
            db.commit()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_incentive_by_id(
        self,
        db: Session,
        *,
        obj_in: SendCustomerUpdate,
        id: int,
    ) -> SendCustomer:
        db_obj = (
            db.query(self.model)
            .filter(SendCustomer.id == id, SendCustomer.delete_flag == 0)
            .first()
        )
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Send customer request id {id} not found",
            )
        tax_rate = crud.m_rate.get_tax_rate(db)
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["fg_incentive"] = obj_in.fg_incentive_tax / (100 + tax_rate['rate']) * 100 if tax_rate \
            else obj_in.fg_incentive_tax
        obj_in_data["send_incentive"] = obj_in.send_incentive_tax / (100 + tax_rate['rate']) * 100 if tax_rate \
            else obj_in.send_incentive_tax

        # hard code update_id
        db_obj.update_id = 88888
        db_obj.update_at = datetime.utcnow()
        if isinstance(obj_in_data, dict):
            update_data = obj_in_data
        else:
            update_data = obj_in_data.dict(exclude_unset=True)
        for field in update_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_fg_incentive_info(
            self,
            db: Session,
            *,
            send_customer_at_from,
            send_customer_at_to
    ) -> Any:
        fg_incentive_info = db.query(
            SendCustomer.send_item_type_code,
            func.count(SendCustomer.send_item_type_code).label("count"),
            func.sum(
                SendCustomer.fg_incentive_tax
            ).label("amount"),
        ).group_by(SendCustomer.send_item_type_code)
        fg_incentive_info = fg_incentive_info.filter(
            SendCustomer.status_flag == self.STATUS_IS_PAID
        ).outerjoin(ActivityLog, (ActivityLog.send_customer_id == SendCustomer.id) & (
                ActivityLog.status == SendCustomer.status_flag) & (SendCustomer.status_flag == self.STATUS_IS_PAID))
        if send_customer_at_from != "":
            fg_incentive_info = fg_incentive_info.filter(
                ActivityLog.update_at >= send_customer_at_from
            )
        if send_customer_at_to != "":
            fg_incentive_info = fg_incentive_info.filter(
                ActivityLog.update_at <= send_customer_at_to + " 23:59:59"
            )
        fg_incentive_info = fg_incentive_info.all()
        fg_incentive_info = jsonable_encoder(fg_incentive_info)
        total_amount = 0
        send_item_type_codes = crud.code_master.get_list_service(db=db)
        send_item_type_codes = jsonable_encoder(send_item_type_codes)

        type_exist = []
        for item in fg_incentive_info:
            item["value"] = int(item["send_item_type_code"])
            item["service_name"] = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_ITEM,
                                                                  code_value=item[
                                                                      "send_item_type_code"])
            if item["amount"]:
                total_amount += item["amount"]
            else:
                item["amount"] = 0
            type_exist.append(item["value"])
            item.pop("send_item_type_code")

            # Filter send_item_type_code
            filtered_send_item_type_code = [send_item for send_item in send_item_type_codes
                                            if send_item['code_value'] == item["value"]]
            item['sort_number'] = filtered_send_item_type_code[0]['sort_number']
        else:
            for item in send_item_type_codes:
                if item['code_value'] not in type_exist:
                    service_name = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_ITEM,
                                                                  code_value=item['code_value'])
                    item = {"value": item['code_value'], "count": 0, "amount": 0, "service_name": service_name,
                            "sort_number": item['sort_number']}
                    fg_incentive_info.append(item)
        re = {"total_amount": total_amount, "fg_incentive_info": fg_incentive_info}
        return re

    def get_list_fg_info(self, db: Session, *,
                         send_customer_at_from,
                         send_customer_at_to,
                         send_item_type_code,
                         type_status,
                         from_company_code,
                         from_store_code,
                         to_company_code,
                         to_store_code,
                         skip: int = 0, limit: int = 10,
                         sort: str,
                         ) -> Any:
        list_request = db.query(
            self.model.id.label("send_customer_id"),
            self.model.send_customer_code,
            self.model.send_item_type_code,
            self.model.send_customer_at,
            self.model.from_company_code,
            self.model.from_store_code,
            self.model.to_company_code,
            self.model.to_store_code,
            self.model.status_flag,
            self.model.send_incentive,
            self.model.fg_incentive,
            self.model.send_incentive_tax,
            self.model.fg_incentive_tax,
            self.model.menu_user_price_tax,
            self.model.option_user_price_tax,
            ActivityLog.update_at
        ). \
            outerjoin(ActivityLog, (ActivityLog.send_customer_id == SendCustomer.id) & (
                ActivityLog.status == SendCustomer.status_flag) & (SendCustomer.status_flag == self.STATUS_IS_PAID)). \
            filter(SendCustomer.status_flag != self.STATUS_CANCEL)
        if sort is not None:
            order = convert_sort_key(
                sort,
                {
                    "send_customer_at": ["send_customer_at"],
                    "update_at": ["activity_log.update_at"]
                },
                "- send_customer_at",
            )
        else:
            order = "- send_customer_at"
        fg_incentive_total = db.query(
            func.sum(self.model.fg_incentive_tax).label("fg_incentive_total")
        ).filter(SendCustomer.status_flag != self.STATUS_CANCEL). \
            outerjoin(ActivityLog, (ActivityLog.send_customer_id == SendCustomer.id) & (
                ActivityLog.status == SendCustomer.status_flag) & (SendCustomer.status_flag == self.STATUS_IS_PAID))
        if send_item_type_code:
            list_request = list_request.filter(SendCustomer.send_item_type_code.in_(send_item_type_code))
            fg_incentive_total = fg_incentive_total.filter(SendCustomer.send_item_type_code.in_(send_item_type_code))
        if send_customer_at_from:
            list_request = list_request.filter(ActivityLog.update_at >= send_customer_at_from)
            fg_incentive_total = fg_incentive_total.filter(ActivityLog.update_at >= send_customer_at_from)
        if send_customer_at_to:
            list_request = list_request.filter(ActivityLog.update_at <= send_customer_at_to + " 23:59:59")
            fg_incentive_total = fg_incentive_total.\
                filter(ActivityLog.update_at <= send_customer_at_to + " 23:59:59")
        if type_status:
            if type_status == self.STATUS_TYPE_1:
                list_request = list_request.filter(SendCustomer.status_flag == self.STATUS_IS_PAID)
                fg_incentive_total = fg_incentive_total.filter(SendCustomer.status_flag == self.STATUS_IS_PAID)
            elif type_status == self.STATUS_TYPE_2:
                list_request = list_request.filter(SendCustomer.status_flag != self.STATUS_IS_PAID,
                                                   SendCustomer.status_flag != self.STATUS_CANCEL)
                fg_incentive_total = fg_incentive_total.filter(SendCustomer.status_flag != self.STATUS_IS_PAID,
                                                               SendCustomer.status_flag != self.STATUS_CANCEL)
            else:
                list_request = list_request.filter(SendCustomer.status_flag != self.STATUS_CANCEL)
                fg_incentive_total = fg_incentive_total.filter(SendCustomer.status_flag != self.STATUS_CANCEL)
        if from_company_code:
            list_request = list_request.filter(SendCustomer.from_company_code == from_company_code)
            fg_incentive_total = fg_incentive_total.filter(SendCustomer.from_company_code == from_company_code)
        if from_store_code:
            list_request = list_request.filter(SendCustomer.from_store_code == from_store_code)
            fg_incentive_total = fg_incentive_total.filter(SendCustomer.from_store_code == from_store_code)
        if to_company_code:
            list_request = list_request.filter(SendCustomer.to_company_code == to_company_code)
            fg_incentive_total = fg_incentive_total.filter(SendCustomer.to_company_code == to_company_code)
        if to_store_code:
            list_request = list_request.filter(SendCustomer.to_store_code == to_store_code)
            fg_incentive_total = fg_incentive_total.filter(SendCustomer.to_store_code == to_store_code)
        total = list_request.count()
        list_request = (
            list_request.order_by(text(order)).offset(skip).limit(limit).all()
        )
        list_requests = jsonable_encoder(list_request)
        fg_incentive_total = fg_incentive_total.first()
        fg_incentive_total = jsonable_encoder(fg_incentive_total)

        # format list request
        for item in list_requests:
            item["send_customer_at"] = utc_to_jst(item["send_customer_at"]) if item["send_customer_at"] else ""
            item["status"] = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_STATUS,
                                                            code_value=item["status_flag"])
            item["service_name"] = crud.code_master.get_code_name(db=db, code_type=self.CODE_TYPE_ITEM,
                                                                  code_value=item[
                                                                      "send_item_type_code"])

            # get store's name and company's name
            item["from_store_name"], item["from_company_name"] = \
                self.get_store_and_company_name(db=db, company_code=item["from_company_code"],
                                                store_code=item["from_store_code"])
            item["to_store_name"], item["to_company_name"] = \
                self.get_store_and_company_name(db=db, company_code=item["to_company_code"],
                                                store_code=item["to_store_code"])
            item['menu'] = crud.menu_setting.get_menu_setting_by_id(db, item['send_customer_id'])
            item['option'] = crud.option_setting.get_option_setting_by_id(db, item['send_customer_id'])
            item["finish_payment_at"] = utc_to_jst(item["update_at"]) if item["update_at"] else ""
            item.pop("update_at")
        fg_incentive_total = fg_incentive_total["fg_incentive_total"] if fg_incentive_total["fg_incentive_total"] else 0

        return list_requests, total, fg_incentive_total

    def get_list_standard_incentive(
            self,
            db: Session
    ):
        list_service = db.query(StandardIncentive).all()
        return list_service

    def get_mail_format(self, db, template_type):
        mail_format = (
            db.query(
                MMailFormat.title,
                MMailFormat.content,
            )
            .filter(MMailFormat.div == 2,
                    MMailFormat.template_type == template_type,
                    MMailFormat.delete_flag == Const.DEL_FLG_NORMAL)
            .first()
        )

        return jsonable_encoder(mail_format)

    def get_url_detail(self, db, company_code, send_customer_id, is_request):
        base_url = db.query(TenantInformation.base_url).filter(TenantInformation.company_code == company_code).first()

        if base_url:
            base_url = jsonable_encoder(base_url)["base_url"]
            url_detail = self.convert_url_base_to_detail(base_url, send_customer_id, is_request)
        else:
            url_detail = ""

        return url_detail

    def convert_url_base_to_detail(self, url_link, send_customer_id, is_request: bool = None):
        if is_request is None:
            url_content = url_link + f"/send-customer/detail?sendCustomerId={send_customer_id}"
        else:
            if is_request:
                url_content = url_link[0:-3] + f"send/detail/?isRequest=1&sendCustomerId={send_customer_id}"
            else:
                url_content = url_link[0:-3] + f"send/detail/?isRequest=0&sendCustomerId={send_customer_id}"
        return "[[" + url_content + "]]"

    def get_mail_address(self, db, div, company_code=None, store_code=None):
        mail_address = db.query(NotificationMailAddress.mail_address)\
                        .filter(NotificationMailAddress.div == div,
                                NotificationMailAddress.delete_flag == Const.DEL_FLG_NORMAL)
        if company_code:
            mail_address = mail_address.filter(NotificationMailAddress.company_code == company_code)

        if store_code:
            mail_address = mail_address.filter(NotificationMailAddress.store_code == store_code)

        mail_address = mail_address.first()

        if mail_address:
            return jsonable_encoder(mail_address)["mail_address"]
        else:
            return None

    def get_company_store_code_by_id(self, db, id):
        send_customer = db.query(self.model.from_company_code,
                                 self.model.from_store_code,
                                 self.model.to_company_code,
                                 self.model.to_store_code) \
                        .filter(SendCustomer.id == id, SendCustomer.delete_flag == Const.DEL_FLG_NORMAL) \
                        .first()

        return jsonable_encoder(send_customer)

    def get_config_mail(self, db, div, div_name):
        config_mail = (
            db.query(MSystemParam.desc1)
            .filter(MSystemParam.div == div,
                    MSystemParam.div_name == div_name,
                    MSystemParam.delete_flag == Const.DEL_FLG_NORMAL)
            .first()
        )

        if config_mail:
            return jsonable_encoder(config_mail)["desc1"]
        else:
            return None

    def create_send_customer_chat_group(
            self, db: Session, *, obj_in: RequestSendCustomerChatGroup, cognito_id: int
    ) -> Any:
        try:
            UID = "marketplace-uid"
            path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
            credentials.Certificate(path)
            custom_token = auth.create_custom_token(UID)
        except IOError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Firebase information not found")
        firebase_chat_id = str(obj_in.send_customer_id) + '_' + str(obj_in.div) + '_' + str(obj_in.company_code) + '_' + str(obj_in.store_code)

        # Check exit group
        group_chat = self.check_exist_chat_group(db, firebase_chat_id)
        if group_chat:
            return group_chat, custom_token
        else:
            obj_data = jsonable_encoder(obj_in)
            new_group_chat = SendCustomerChatGroup(
                **obj_data,
                firebase_chat_id=firebase_chat_id,
                insert_id=cognito_id,
                insert_at=datetime.utcnow(),
                update_id=cognito_id,
                update_at=datetime.utcnow(),
                delete_flag=Const.DEL_FLG_NORMAL
            )
            db.add(new_group_chat)
            db.commit()
            db.refresh(new_group_chat)
            return new_group_chat, custom_token


    def check_exist_chat_group(
            self, db, firebase_chat_id
    ):
        chat_group = db.query(SendCustomerChatGroup).\
            filter(SendCustomerChatGroup.firebase_chat_id == firebase_chat_id,
                   SendCustomerChatGroup.delete_flag == Const.DEL_FLG_NORMAL).first()
        return chat_group

    def check_exist_survey_url(
            self, db: Session, obj_in: SurveyUrlSettingCreate
    ) -> Any:
        # check exist survey url
        existed_survey_url_data = db.query(SurveyUrlSetting).filter_by(company_code=obj_in.company_code,
                                                                       store_code=obj_in.store_code,
                                                                       service_code=obj_in.service_code,
                                                                       menu_id=obj_in.menu_id).first()
        if existed_survey_url_data:
            return jsonable_encoder(existed_survey_url_data)
        else:
            return None

    def create_survey_url(
            self, db: Session, obj_in: SurveyUrlSettingCreate
    ) -> Any:
        # get survey url base
        m_system_param_data = db.query(MSystemParam.desc1).filter_by(div=12,
                                                                     div_name="survey_url_base",
                                                                     delete_flag=Const.DEL_FLG_NORMAL).first()

        if m_system_param_data:
            survey_url_base = jsonable_encoder(m_system_param_data)["desc1"]
        else:
            survey_url_base = ""

        # get company name
        m_company_data = db.query(MCompany.company_name).filter_by(company_code=obj_in.company_code,
                                                                   delete_flag=Const.DEL_FLG_NORMAL).first()

        if m_company_data:
            company_name = jsonable_encoder(m_company_data)["company_name"]
        else:
            company_name = ""

        # encode token
        encode_data = {
            "company_code": obj_in.company_code,
            "company_name": company_name,
            "store_code": obj_in.store_code,
            "service_code": obj_in.service_code,
            "menu_id": obj_in.menu_id,
            "url_setting_flag": 1,
        }

        token = encode_token(encode_data)
        survey_url = survey_url_base + "/?token=" + token + "&type=smart-survey"

        return survey_url

    def save_survey_url(
            self, db: Session, obj_in: SurveyUrlSettingCreate, survey_url_full: str, survey_url_short: str
    ) -> Any:
        # save survey url to DB
        try:
            obj_data = jsonable_encoder(obj_in)
            new_survey_url = SurveyUrlSetting(**obj_data,
                                              survey_url_full=survey_url_full,
                                              survey_url_short=survey_url_short,
                                              insert_id=9999,
                                              insert_at=datetime.utcnow()
                                              )
            db.add(new_survey_url)
            db.commit()
            db.refresh(new_survey_url)
        except Exception as err:
            raise HTTPException(status_code=500, detail=err)

        return True


send_customer = CRUDSendCustomer(SendCustomer)
