from typing import Any
import json
import os
from sqlalchemy.orm import Session
from sqlalchemy import asc, and_
from app.crud.base import CRUDBase
from app.models.menu_setting import MenuSetting
from app.models.menu_store_link import MenuStoreLink
from app.models.send_customer_menu_link import SendCustomerMenuLink
from app.schemas.menu_setting import MenuSettingCreate, MenuSettingUpdate, MenuSettingRequest

from app import crud
from fastapi.encoders import jsonable_encoder
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.constants import Const
from app.models.s3_file import S3File


class CRUDMenuSetting(CRUDBase[MenuSetting, MenuSettingCreate, MenuSettingUpdate]):
    SEND_ITEM_TYPE_CODE = "send_customer_type_code_new"
    PDF_TYPE = '2'

    def get_menu_setting(
            self,
            db: Session,
            *,
            obj_in: MenuSettingRequest
    ):
        domain_image = os.environ["DOMAIN_IMAGE"]
        company_code = obj_in.company_code if obj_in.company_code else None
        store_code = obj_in.store_code if obj_in.store_code else None
        code_type = obj_in.code_type_id if obj_in.code_type_id else None

        list_menu = db.query(self.model).filter(MenuSetting.delete_flag == Const.DEL_FLG_NORMAL)
        if company_code:
            list_menu = list_menu.filter(MenuSetting.from_company_code == company_code)
        if store_code:
            list_menu = list_menu.filter(MenuSetting.from_store_code == store_code)
        if code_type:
            list_menu = list_menu.filter(MenuSetting.code_type_id == code_type)

        if company_code is None and store_code is None and code_type is None:
            list_menu = []
        else:
            list_menu = list_menu.all()
            list_menu = jsonable_encoder(list_menu)
            for item in list_menu:

                # get list sp2 by menu_id
                company_store_info = db.query(MenuStoreLink.to_store_code,
                                              MenuStoreLink.to_company_code,
                                              MenuStoreLink.reservable_time,
                                              MenuStoreLink.transfer_flag,
                                              MenuStoreLink.vehicle_inspection_flag,
                                              MenuStoreLink.legal_inspection_flag,
                                              MenuStoreLink.periodic_inspection_flag,
                                              MenuStoreLink.oil_flag,
                                              MenuStoreLink.battery_flag,
                                              MenuStoreLink.tire_flag,
                                              MenuStoreLink.insurance_flag,
                                              MenuStoreLink.loan_lease_flag,
                                              MenuStoreLink.birthday_flag,
                                              MenuStoreLink.in_household_acquaintance_flag).\
                    filter(MenuStoreLink.menu_id == item["id"], MenuStoreLink.delete_flag == Const.DEL_FLG_NORMAL).\
                    order_by(asc(MenuStoreLink.sort_number)). \
                    all()
                company_store_info = jsonable_encoder(company_store_info)
                for i in company_store_info:
                    i["to_store_name"], i["to_company_name"] = \
                        crud.send_customer.get_store_and_company_name(db, i["to_store_code"], i["to_company_code"])
                    if i["reservable_time"]:
                        reservable_time = i["reservable_time"][1: -1].replace(' ', '').split('/')
                        list_interval = [None if i == "null" else i for i in reservable_time]
                        for key, value in enumerate(list_interval):
                            if value:
                                list_interval[key] = value.strip('[]').split(',')
                        i["reservable_time"] = list_interval
                    else:
                        i["reservable_time"] = [None for i in range(7)]
                item["company_store_info"] = company_store_info
                item["code_type_name"] = crud.code_master.get_code_name(db, self.SEND_ITEM_TYPE_CODE,
                                                                        item["code_type_id"])
                item['has_group'] = crud.option_group.check_group_of_menu(db, item['id'])
                if item['menu_candidate_time']:
                    item['menu_candidate_time'] = json.loads(item['menu_candidate_time'])
                else:
                    item['menu_candidate_time'] = []
                # check policy and terms of use
                if item["policy_type"] == self.PDF_TYPE:
                    if item["policy_content"]:
                        s3_file = db.query(S3File).filter(S3File.id == int(item["policy_content"]),
                                                          S3File.delete_flag == Const.DEL_FLG_NORMAL).first()
                        item["policy_file"] = str(domain_image) + str(s3_file.key)
                    else:
                        item["policy_content"] = None
                if item["terms_type"] == self.PDF_TYPE:
                    if item["terms_content"]:
                        s3_file = db.query(S3File).filter(S3File.id == int(item["terms_content"]),
                                                          S3File.delete_flag == Const.DEL_FLG_NORMAL).first()
                        item["terms_file"] = str(domain_image) + str(s3_file.key)
                    else:
                        item["terms_content"] = None
        return list_menu

    def create_menu_setting(
            self,
            db: Session,
            *,
            obj_in: MenuSettingCreate
    ):
        obj_in_data = jsonable_encoder(obj_in)
        company_store_info = obj_in_data["menu_link_store"]
        obj_in_data.pop("menu_link_store")

        # hard code insert_id , update_id
        insert_id = 88888
        update_id = 1
        if "menu_time_require" in obj_in_data and obj_in_data["menu_time_require"] <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Bad request.')
        if "shortest_available_day" in obj_in_data and not 0 <= obj_in_data["shortest_available_day"] <= 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Invalid shortest available day.')
        if "incentive_flag" in obj_in_data:
            if obj_in_data["incentive_flag"] != Const.ENABLE:
                obj_in_data["incentive_flag"] = Const.DISABLE
            else:
                if "menu_send_incentive" not in obj_in_data or obj_in_data["menu_send_incentive"] is None \
                        or "menu_fg_incentive" not in obj_in_data or obj_in_data["menu_fg_incentive"] is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f'Bad request.')

        db_obj = self.model(**obj_in_data, insert_id=insert_id, insert_at=datetime.utcnow(), update_id=update_id,
                            update_at=datetime.utcnow(), delete_flag=Const.DEL_FLG_NORMAL)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        new_menu_setting = jsonable_encoder(db_obj)
        menu_id = new_menu_setting["id"]
        for idx, item in enumerate(company_store_info):
            reservable_time = item["reservable_time"] if "reservable_time" in item else None
            str_list_reservable_time = None
            if reservable_time:
                list_reservable_time = ["null" if i is None else i for i in reservable_time]
                str_list_reservable_time = '[' + '/'.join(map(str, list_reservable_time)).replace("'", "") + ']'
            self.create_menu_link_store(db, menu_id, item["to_company_code"], item["to_store_code"],
                                        item["transfer_flag"], item["vehicle_inspection_flag"],
                                        item["legal_inspection_flag"],
                                        item["periodic_inspection_flag"], item["oil_flag"], item["battery_flag"],
                                        item["tire_flag"], item["insurance_flag"], item["loan_lease_flag"],
                                        item["birthday_flag"], item["in_household_acquaintance_flag"],
                                        sort_number=idx + 1, reservable_time=str_list_reservable_time
                                        )
        return new_menu_setting

    def update_menu_setting(
            self,
            db: Session,
            *,
            obj_in: MenuSettingUpdate,
            id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        company_store_info = obj_in_data["menu_link_store"]
        obj_in_data.pop("menu_link_store")
        db_obj = db.query(self.model).filter(MenuSetting.id == id, MenuSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Menu Setting id {id} not found')

        if "shortest_available_day" in obj_in_data and not 0 <= obj_in_data["shortest_available_day"] <= 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Invalid shortest available day.')

        # hard code  update_id
        if "incentive_flag" in obj_in_data:
            if obj_in_data["incentive_flag"] != Const.ENABLE:
                obj_in_data["incentive_flag"] = Const.DISABLE
            else:
                if "menu_send_incentive" not in obj_in_data or obj_in_data["menu_send_incentive"] is None \
                        or "menu_fg_incentive" not in obj_in_data or obj_in_data["menu_fg_incentive"] is None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f'Bad request.')
        # hard code insert_id , update_id
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
        update_menu = jsonable_encoder(db_obj)
        self.update_menu_link_store(db, id, company_store_info)
        return update_menu

    def delete_menu_setting(
            self,
            db: Session,
            *,
            id: int
    ):
        menu_by_id = db.query(self.model).filter(MenuSetting.id == id,
                                                 MenuSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not menu_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Menu Setting id {id} not found')

        # hard code delete_id
        menu_by_id.delete_id = 88888

        # update delete_flag, delete_at
        has_group = crud.option_group.check_group_of_menu(db, id)
        if has_group:
            crud.option_group.delete_group_by_menu_id(db, menu_id=id)
        has_link_store = self.check_menu_link_store(db, menu_id=id)
        if has_link_store:
            self.delete_menu_link_store_by_menu_id(db, menu_id=id)
        menu_by_id.delete_flag = Const.DEL_FLG_DELETE
        menu_by_id.delete_at = datetime.utcnow()
        db.add(menu_by_id)
        db.commit()
        db.refresh(menu_by_id)
        return menu_by_id

    def get_menu_setting_by_id(self, db, send_customer_id):
        menu_link = db.query(SendCustomerMenuLink).filter(
            SendCustomerMenuLink.send_customer_id == send_customer_id).first()
        list_detail_menu_setting = []
        if menu_link:
            list_menu_setting = db.query(MenuSetting).filter(MenuSetting.id == menu_link.menu_id)
            tax_rate = crud.m_rate.get_tax_rate(db)
            for menu_setting in list_menu_setting:
                detail_menu_setting = {
                    "menu_id": menu_setting.id,
                    "menu_name": menu_setting.menu_name,
                    "menu_user_price": menu_setting.menu_user_price,
                    "menu_time_require": menu_setting.menu_time_require,
                    "menu_user_price_tax": menu_setting.menu_user_price + int(menu_setting.menu_user_price
                                                                              * tax_rate["rate"] / 100),
                    "menu_paid_type": menu_setting.paid_type
                }
                list_detail_menu_setting.append(detail_menu_setting)
        return list_detail_menu_setting


    def create_menu_link_store(
        self, db: Session, menu_id: int, to_company_code: str, to_store_code: str, transfer_flag: int,
            vehicle_inspection_flag: int, legal_inspection_flag: int,
            periodic_inspection_flag: int, oil_flag: int, battery_flag: int, tire_flag: int, insurance_flag: int,
            loan_lease_flag: int, birthday_flag: int, in_household_acquaintance_flag: int, sort_number: int,
            reservable_time: str
    ) -> Any:
        obj_in_data = {"menu_id": menu_id, "to_company_code": to_company_code,
                       "to_store_code": to_store_code, "sort_number": sort_number, "reservable_time": reservable_time,\
                       "transfer_flag": transfer_flag, "vehicle_inspection_flag": vehicle_inspection_flag,\
                       "legal_inspection_flag": legal_inspection_flag, "periodic_inspection_flag": periodic_inspection_flag,\
                       "oil_flag": oil_flag, "battery_flag": battery_flag, "tire_flag": tire_flag, "insurance_flag": insurance_flag,\
                       "loan_lease_flag": loan_lease_flag, "birthday_flag": birthday_flag,\
                       "in_household_acquaintance_flag": in_household_acquaintance_flag}

        # hard code insert_id , update_id
        insert_id = 88888
        update_id = 1
        menu_store_link = MenuStoreLink(
            **obj_in_data,
            insert_id=insert_id,
            insert_at=datetime.utcnow(),
            update_id=update_id,
            update_at=datetime.utcnow(),
            delete_flag=Const.DEL_FLG_NORMAL,
        )
        db.add(menu_store_link)
        db.commit()
        db.refresh(menu_store_link)

    def update_menu_link_store(
            self, db: Session, menu_id: int, company_store_info
    ) -> Any:
        obj_in = db.query(MenuStoreLink).filter(MenuStoreLink.menu_id == menu_id,
                                                MenuStoreLink.delete_flag == Const.DEL_FLG_NORMAL).all()
        obj_data = jsonable_encoder(obj_in)
        list_dict = company_store_info + obj_data

        def subset_dict(ele, lst):
            for el in lst:
                if ele.items() < el.items():
                    return el
            return False

        list_new = []
        for idx, i in enumerate(company_store_info):
            e = subset_dict(i, list_dict) if subset_dict(i, list_dict) else i
            e["sort_number"] = idx + 1
            if e not in list_new:
                reservable_time = e["reservable_time"] if "reservable_time" in e else None
                str_list_reservable_time = None
                if reservable_time:
                    list_reservable_time = ["null" if i is None else i for i in reservable_time]
                    str_list_reservable_time = '[' + '/'.join(map(str, list_reservable_time)).replace("'", "") + ']'
                if "id" not in e:
                    self.create_menu_link_store(db, menu_id, e["to_company_code"], e["to_store_code"], e["transfer_flag"],
                    e["vehicle_inspection_flag"], e["legal_inspection_flag"], e["periodic_inspection_flag"], e["oil_flag"],
                    e["battery_flag"], e["tire_flag"], e["insurance_flag"], e["loan_lease_flag"], e["birthday_flag"],
                    e["in_household_acquaintance_flag"], e["sort_number"], str_list_reservable_time)
                else:
                    update_obj = self.get_menu_store_link_by_id(db=db, menu_store_link_id=e["id"])
                    update_obj.sort_number = e["sort_number"]
                    db.add(update_obj)
                    db.commit()
                    db.refresh(update_obj)
                list_new.append(e)
        for item in obj_data:
            if item not in list_new:
                db_obj = self.get_menu_store_link_by_id(db=db, menu_store_link_id=item["id"])
                db_obj.update_id = 88888
                db_obj.update_at = datetime.utcnow()
                db_obj.delete_flag = Const.DEL_FLG_DELETE
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)

    def get_menu_store_link_by_id(self, db: Session, menu_store_link_id: int):
        db_obj = db.query(MenuStoreLink).filter(MenuStoreLink.id == menu_store_link_id,
                                                MenuStoreLink.delete_flag == Const.DEL_FLG_NORMAL).first()
        return db_obj

    def delete_menu_link_store_by_menu_id(
            self,
            db: Session,
            menu_id: int
    ):
        menu_link_store = db.query(MenuStoreLink).filter(MenuStoreLink.menu_id == menu_id,
                                                   MenuStoreLink.delete_flag == Const.DEL_FLG_NORMAL).all()
        if not menu_link_store:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Menu Setting have {menu_id} not found')
        for item in menu_link_store:
            # hard code delete_id
            item.delete_id = 88888

            # update delete_flag, delete_at
            item.delete_flag = Const.DEL_FLG_DELETE
            item.delete_at = datetime.utcnow()
            db.add(item)
            db.commit()
            db.refresh(item)

    def check_menu_link_store(self, db, menu_id):
        menu_link_store = db.query(MenuStoreLink).filter(MenuStoreLink.menu_id == menu_id,
                                                         MenuStoreLink.delete_flag == Const.DEL_FLG_NORMAL).all()
        return True if menu_link_store else False

    def get_menu_detail(self, db, menu_id):
        menu = db.query(self.model.id.label("menu_id"),
                        self.model.code_type_id,
                        self.model.menu_name,
                        self.model.from_store_code,
                        self.model.from_company_code)\
            .filter(MenuSetting.id == menu_id, MenuSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        menu = jsonable_encoder(menu)
        menu["store_name"], menu["company_name"] = crud.send_customer.\
            get_store_and_company_name(db, menu["from_store_code"], menu["from_company_code"])
        menu["service_name"] = crud.code_master.get_code_name(db, self.SEND_ITEM_TYPE_CODE,
                                                              menu["code_type_id"])
        return menu

    def check_exit_file(self, db, menu_id, file_type):
        menu = db.query(MenuSetting).filter(
            and_(MenuSetting.delete_flag == Const.DEL_FLG_NORMAL, MenuSetting.id == menu_id)).first()

        _type = None
        if file_type == "policy_content":
            _type = "policy_type"
        elif file_type == "terms_content":
            _type = "terms_type"
        if not _type:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"File type {file_type} not valid")

        menu = jsonable_encoder(menu)
        if menu and menu[_type] == self.PDF_TYPE:
            s3_file_id = menu[file_type]
            return s3_file_id
        else:
            return None


menu_setting = CRUDMenuSetting(MenuSetting)

