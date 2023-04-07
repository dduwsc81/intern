from datetime import datetime

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.option_group import OptionGroup
from app.models.send_customer_option_link import SendCustomerOptionLink
from app.schemas.option_group import OptionGroupCreate, OptionGroupUpdate
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from app import crud
from app.constants import Const


class CRUDOptionGroup(CRUDBase[OptionGroup, OptionGroupCreate, OptionGroupUpdate]):

    def get_list_group(
            self,
            db: Session,
            *,
            menu_id: int
    ):
        option_group = db.query(self.model).filter(OptionGroup.menu_id == menu_id,
                                                   OptionGroup.delete_flag == Const.DEL_FLG_NORMAL).all()
        option_group = jsonable_encoder(option_group)
        menu_info = crud.menu_setting.get_menu_detail(db, menu_id)
        for item in option_group:
            item['has_option'] = crud.option_setting.check_option_of_group(db, item['id'])
        option_info = {"menu_info": menu_info, "list_group_option": option_group}
        return option_info

    def get_detail_group(
            self,
            db: Session,
            *,
            group_id: int
    ):
        option_group = db.query(self.model).filter(OptionGroup.id == group_id,
                                                   OptionGroup.delete_flag == Const.DEL_FLG_NORMAL).first()
        option_group = jsonable_encoder(option_group)
        return option_group

    def create_group(
            self,
            db: Session,
            *,
            obj_in: OptionGroupCreate
    ):
        obj_in_data = jsonable_encoder(obj_in)
        if 'menu_id' not in obj_in_data or 'group_name' not in obj_in_data \
                or 'single_option' not in obj_in_data or 'option_require' not in obj_in_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Missing parameters')
        if len(obj_in_data['group_name']) > 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Invalid length group name')
        option_group = db.query(self.model).filter(OptionGroup.menu_id == obj_in_data['menu_id'],
                                                   OptionGroup.delete_flag == Const.DEL_FLG_NORMAL)
        if len(option_group.all()) >= 3:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Maximum group')
        else:
            option_group = option_group.filter(OptionGroup.group_name == obj_in_data['group_name']).first()
        if option_group:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Group {obj_in_data["group_name"]} already exists')
        if obj_in_data["single_option"] != Const.ENABLE:
            obj_in_data["single_option"] = Const.DISABLE
        if obj_in_data["option_require"] != Const.ENABLE:
            obj_in_data["option_require"] = Const.DISABLE

        # hard code insert_id , update_id
        insert_id = 88888
        update_id = 1
        db_obj = self.model(**obj_in_data, insert_id=insert_id, insert_at=datetime.utcnow(), update_id=update_id,
                            update_at=datetime.utcnow(), delete_flag=Const.DEL_FLG_NORMAL)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_group(
            self,
            db: Session,
            *,
            obj_in: OptionGroupUpdate,
            id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = db.query(self.model).filter(OptionGroup.id == id, OptionGroup.delete_flag == Const.DEL_FLG_NORMAL).first()
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Group id {id} not found')
        if 'group_name' not in obj_in_data \
                or 'single_option' not in obj_in_data or 'option_require' not in obj_in_data or not obj_in_data['group_name'] \
                or obj_in_data['single_option'] is None or obj_in_data['option_require'] is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Bad request')
        option_group = db.query(self.model).filter(OptionGroup.id != id, OptionGroup.menu_id == obj_in_data['menu_id'],
                                                   OptionGroup.group_name == obj_in_data['group_name'],
                                                   OptionGroup.delete_flag == Const.DEL_FLG_NORMAL).first()
        if option_group:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Group {obj_in_data["group_name"]} already exists')
        if len(obj_in_data['group_name']) > 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Invalid length group name')
        if obj_in_data["single_option"] != Const.ENABLE:
            obj_in_data["single_option"] = Const.DISABLE
        if obj_in_data["option_require"] != Const.ENABLE:
            obj_in_data["option_require"] = Const.DISABLE
        list_option = crud.option_setting.get_list_option(db=db, group_id=id)
        if db_obj.single_option == Const.ENABLE and obj_in_data['single_option'] == Const.DISABLE:
            if len(list_option) > 6:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Invalid length option')
            for option in list_option:
                if len(option.option_name) > 10:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail=f'Invalid length option name')
        if 'menu_id' in obj_in_data:
            del obj_in_data['menu_id']
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

    def delete_group_by_menu_id(
            self,
            db: Session,
            menu_id: int
    ):
        group_by_id = db.query(self.model).filter(OptionGroup.menu_id == menu_id,
                                                   OptionGroup.delete_flag == Const.DEL_FLG_NORMAL).all()
        if not group_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Group in menu {menu_id} not found')
        for item in group_by_id:
            # hard code delete_id
            has_option = crud.option_setting.check_option_of_group(db, group_id=item.id)
            if has_option:
                crud.option_setting.delete_option_setting_by_group_id(db, group_id=item.id)
            item.delete_id = 88888

            # update delete_flag, delete_at
            item.delete_flag = Const.DEL_FLG_DELETE
            item.delete_at = datetime.utcnow()
            db.add(item)
            db.commit()
            db.refresh(item)

    def delete_group(
            self,
            db: Session,
            *,
            id: int
    ):
        group_by_id = db.query(self.model).filter(OptionGroup.id == id, OptionGroup.delete_flag == 0).first()
        if not group_by_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Group id {id} not found')
        has_option = crud.option_setting.check_option_of_group(db, group_id=id)
        if has_option:
            crud.option_setting.delete_option_setting_by_group_id(db, group_id=id)
        # hard code delete_id
        group_by_id.delete_id = 88888

        # update delete_flag, delete_at
        group_by_id.delete_flag = Const.DEL_FLG_DELETE
        group_by_id.delete_at = datetime.utcnow()
        db.add(group_by_id)
        db.commit()
        db.refresh(group_by_id)
        group_by_id = jsonable_encoder(group_by_id)
        return group_by_id

    def check_group_of_menu(self, db, menu_id):
        list_group = db.query(OptionGroup).filter(OptionGroup.menu_id == menu_id,
                                                  OptionGroup.delete_flag == Const.DEL_FLG_NORMAL)
        return True if list_group.all() else False


option_group = CRUDOptionGroup(OptionGroup)
