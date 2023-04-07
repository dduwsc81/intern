from datetime import datetime

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.option_setting import OptionSetting
from app.models.send_customer_option_link import SendCustomerOptionLink
from app.schemas.option_setting import OptionSettingCreate, OptionSettingUpdate
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from app import crud
from app.constants import Const


class CRUDOptionSetting(CRUDBase[OptionSetting, OptionSettingCreate, OptionSettingUpdate]):
    def get_list_option(
            self,
            db: Session,
            *,
            group_id: int
    ):
        option = db.query(self.model).filter(OptionSetting.group_id == group_id, OptionSetting.delete_flag == Const.DEL_FLG_NORMAL).all()
        return option

    def create_option_setting(
            self,
            db: Session,
            *,
            obj_in: OptionSettingCreate
    ):
        obj_in_data = jsonable_encoder(obj_in)
        option_group = crud.option_group.get_detail_group(db=db, group_id=obj_in_data['group_id'])
        if not option_group:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Bad request.')
        else:
            if option_group['single_option'] == Const.DISABLE and len(obj_in_data['option_name']) > 10:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Invalid length option name.')
        option = db.query(self.model).filter(OptionSetting.group_id == obj_in_data['group_id'],
                                             OptionSetting.delete_flag == Const.DEL_FLG_NORMAL)
        if len(option.all()) >= 6 and option_group['single_option'] == Const.DISABLE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Maximum option.')
        else:
            option = option.filter(OptionSetting.option_name == obj_in_data['option_name']).first()
        if option:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Option {obj_in_data["option_name"]} already exists.')

        # hard code insert_id , update_id
        insert_id = 88888
        update_id = 1
        db_obj = self.model(**obj_in_data, insert_id=insert_id, insert_at=datetime.utcnow(), update_id=update_id,
                            update_at=datetime.utcnow(), delete_flag=0)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_option_setting(
            self,
            db: Session,
            *,
            obj_in: OptionSettingUpdate,
            id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = db.query(self.model).filter(OptionSetting.id == id, OptionSetting.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Option Setting id {id} not found')
        option_group = crud.option_group.get_detail_group(db=db, group_id=obj_in_data['group_id'])
        if not option_group:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Bad request.')
        else:
            if option_group['single_option'] == Const.DISABLE and len(obj_in_data['option_name']) > 10:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Invalid length option name.')
        option = db.query(self.model).filter(OptionSetting.id != id,
                                             OptionSetting.group_id == obj_in_data['group_id'],
                                             OptionSetting.option_name == obj_in_data['option_name'],
                                             OptionSetting.delete_flag == 0).first()
        if option:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Option {obj_in_data["option_name"]} already exists.')
        if 'group_id' in obj_in_data:
            del obj_in_data['group_id']
        # hard code insert_id , update_id
        db_obj.update_id = 88888
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

    def delete_option_setting_by_group_id(
            self,
            db: Session,
            group_id: int
    ):
        option_by_id = db.query(self.model).filter(OptionSetting.group_id == group_id,
                                                   OptionSetting.delete_flag == Const.DEL_FLG_NORMAL).all()
        if not option_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Option Setting in group {group_id} not found.')
        for item in option_by_id:
            # hard code delete_id
            item.delete_id = 88888

            # update delete_flag, delete_at
            item.delete_flag = Const.DEL_FLG_DELETE
            item.delete_at = datetime.utcnow()
            db.add(item)
            db.commit()
            db.refresh(item)

    def delete_option_setting(
            self,
            db: Session,
            *,
            id: int
    ):
        option_by_id = db.query(self.model).filter(OptionSetting.id == id, OptionSetting.delete_flag == 0).first()
        if not option_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Option Setting id {id} not found.')

        # hard code delete_id
        option_by_id.delete_id = 88888

        # update delete_flag, delete_at
        option_by_id.delete_flag = Const.DEL_FLG_DELETE
        option_by_id.delete_at = datetime.utcnow()
        db.add(option_by_id)
        db.commit()
        db.refresh(option_by_id)
        return jsonable_encoder(option_by_id)

    def get_option_setting_by_id(self, db, send_customer_id):
        list_option_link = db.query(SendCustomerOptionLink).filter \
            (SendCustomerOptionLink.send_customer_id == send_customer_id)
        list_id_option_setting = []
        for option_link in list_option_link:
            list_id_option_setting.append(option_link.option_id)
        list_option_setting = db.query(OptionSetting).filter(OptionSetting.id.in_(list_id_option_setting))
        list_detail_option_setting = []
        tax_rate = crud.m_rate.get_tax_rate(db)
        for option_setting in list_option_setting:
            detail_option_setting = {
                "option_id": option_setting.id,
                "option_name": option_setting.option_name,
                "option_user_price": option_setting.option_user_price,
                "option_user_price_tax": option_setting.option_user_price + int(option_setting.option_user_price *
                                                                                tax_rate["rate"] / 100),
                "option_time_require": option_setting.option_time_require
            }
            list_detail_option_setting.append(detail_option_setting)
        return list_detail_option_setting

    def get_option_detail(self, db, send_customer_id, tax_rate):
        option_data = db.query(SendCustomerOptionLink,
                               OptionSetting.option_name,
                               OptionSetting.option_time_require,
                               OptionSetting.group_id) \
            .join(OptionSetting, OptionSetting.id == SendCustomerOptionLink.option_id) \
            .filter(SendCustomerOptionLink.send_customer_id == send_customer_id) \
            .order_by(OptionSetting.group_id, OptionSetting.id) \
            .all()

        lst_option = []
        option_data = jsonable_encoder(option_data)
        for row in option_data:
            obj_option = {}
            option_price = row["SendCustomerOptionLink"]["send_customer_option_price"]
            obj_option["group_id"] = row["group_id"]
            obj_option["option_id"] = row["SendCustomerOptionLink"]["option_id"]
            obj_option["option_name"] = row["option_name"]
            obj_option["option_time_require"] = row["option_time_require"]
            obj_option["option_user_price_tax"] = option_price + int(option_price * tax_rate / 100)
            lst_option.append(obj_option)

        return lst_option

    def check_option_of_group(self, db, group_id):
        list_option = db.query(OptionSetting).filter(OptionSetting.group_id == group_id, OptionSetting.delete_flag == Const.DEL_FLG_NORMAL)
        return True if list_option.all() else False


option_setting = CRUDOptionSetting(OptionSetting)
