from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.chat_group import ChatGroup
from app.models.offer import Offer
from app.models.chat_group_member import ChatGroupMember
from app.models.store import Store
from app.models.m_company import MCompany
from app.models.negotiation import Negotiation
from app.models.car_market import CarMarket
from app.models.staff import Staff
from app.schemas.chat_group import ChatGroupCreate, ChatGroupUpdate
from datetime import datetime, timedelta
from ..api.api_v1.endpoints.format_status import *
from app.constants import Const
from sqlalchemy import and_, Integer
from sqlalchemy.sql.expression import cast
import firebase_admin
from firebase_admin import db

DIV_CHAT_GROUP = {
    "BUYER": 1,
    "SELLER": 2
}
ADMIN_USER_ID = 888888


class CRUDChatGroup(CRUDBase[ChatGroup, ChatGroupCreate, ChatGroupUpdate]):
    ADMIN_NAME = "FG管理者"

    def create_chat_group(
            self, db: Session, *, obj_in: ChatGroupCreate
    ) -> Any:
        firebase_chat_id = str(obj_in.car_id) + '_' + str(obj_in.div) + '_' + str(obj_in.store_id)

        # check exist group
        group_chat = self.check_exist_chat_group(db, firebase_chat_id)

        if obj_in.div == DIV_CHAT_GROUP["SELLER"]:
            # Check if store is owner store of car
            car_market = (
                db.query(CarMarket.store_code)
                    .filter(
                    CarMarket.car_id == obj_in.car_id,
                    CarMarket.delete_flag == Const.DEL_FLG_NORMAL,
                )
                    .first()
            )
            if car_market is not None:
                if int(car_market[0]) != int(obj_in.store_id):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Store_id {obj_in.store_id} is not the owner store of car_id {obj_in.car_id}",
                    )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Car market id {obj_in.car_id} not found",
                )

            if group_chat is None:
                group_chat = ChatGroup(
                    car_id=obj_in.car_id,
                    chassis_number=obj_in.chassis_number,
                    div=obj_in.div,
                    store_id=obj_in.store_id,
                    insert_id=ADMIN_USER_ID,
                    firebase_chat_id=firebase_chat_id,
                    insert_at=datetime.utcnow(),
                    update_id=ADMIN_USER_ID,
                    update_at=datetime.utcnow(),
                    delete_flag=Const.DEL_FLG_NORMAL,
                )
                db.add(group_chat)
                db.commit()
                db.refresh(group_chat)
                group_id = group_chat.id
            else:
                group_id = group_chat.id
        elif obj_in.div == DIV_CHAT_GROUP["BUYER"]:
            if group_chat is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Group chat of car id {obj_in.car_id} and store id {obj_in.store_id} not found"
                )
            group_id = group_chat.id

        self.add_admin_to_chat_group(db, user_id=ADMIN_USER_ID, group_id=group_id)

        # Get store name. company name of car
        store_company_name = db.query(Store.store_name,
                                      MCompany.company_name,
                                      Store.store_code,
                                      Store.company_code) \
            .join(CarMarket, and_(cast(CarMarket.store_code, Integer) == Store.id,
                                  CarMarket.car_id == obj_in.car_id,
                                  CarMarket.delete_flag == Const.DEL_FLG_NORMAL, )) \
            .join(MCompany, and_(MCompany.company_code == Store.company_code,
                                 MCompany.delete_flag == Const.DEL_FLG_NORMAL))\
            .first()

        # Get store name. company name of store input
        store_company_name_store = db.query(Store.store_name.label("store_name_store"),
                                            MCompany.company_name.label("company_name_store"),
                                            Store.store_code.label("store_code_store"),
                                            Store.company_code.label("company_code_store")) \
            .join(MCompany, and_(MCompany.company_code == Store.company_code,
                                 MCompany.delete_flag == Const.DEL_FLG_NORMAL)) \
            .filter(Store.id == int(obj_in.store_id))\
            .first()

        return group_chat, store_company_name, store_company_name_store

    def check_exist_chat_group(self, db: Session, firebase_chat_id: str) -> Any:
        chat_group = db.query(self.model). \
            filter(ChatGroup.firebase_chat_id == firebase_chat_id, ChatGroup.delete_flag == 0).first()
        return chat_group

    def add_admin_to_chat_group(
            self,
            db: Session,
            *,
            user_id: int,
            group_id: int
    ) -> Any:
        obj_in_data = db.query(ChatGroupMember).filter(ChatGroupMember.group_id == group_id,
                                                       ChatGroupMember.user_id == user_id,
                                                       ChatGroupMember.delete_flag == 0).first()
        if obj_in_data:
            return obj_in_data
        else:
            obj_in_data = {"user_id": user_id, "store_id": "", "group_id": group_id}
            db_obj = ChatGroupMember(**obj_in_data, insert_id=888888, insert_at=datetime.utcnow(),
                                     update_id=888888,
                                     update_at=datetime.utcnow(), delete_flag=0)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def get_chat_with_notification(self, db: Session) -> Any:
        chat_group_info = db.query(self.model).filter(self.model.delete_flag == 0,
                                                      self.model.message_unread_cnt != 0,
                                                      self.model.last_message_user_name != self.ADMIN_NAME).all()
        return chat_group_info

    def update_chat_group(
            self,
            db: Session,
            *,
            store_id: int,
            status_chat: int = Const.CHATTING_FLG,
            obj_in: Union[ChatGroupUpdate, Dict[str, Any]],
            group_id: int
    ) -> Any:
        chat_group_info = db.query(ChatGroup).filter(ChatGroup.id == group_id,
                                                     ChatGroup.delete_flag == 0).first()
        if not chat_group_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'チャットグループID{group_id}が存在しません。')
        chat_group_info.update_at = datetime.utcnow()
        if chat_group_info.message_unread_cnt is None:
            chat_group_info.message_unread_cnt = 0
        if chat_group_info.message_total_cnt is None:
            chat_group_info.message_total_cnt = 0
        if chat_group_info.last_message_store_id is None:
            chat_group_info.last_message_store_id = store_id

        # update unread message
        if store_id == chat_group_info.last_message_store_id and status_chat == Const.CHATTING_FLG:
            chat_group_info.message_unread_cnt += 1
        elif store_id != chat_group_info.last_message_store_id and status_chat == Const.RESET_CHAT_FLG:
            chat_group_info.message_unread_cnt = 0
        elif store_id != chat_group_info.last_message_store_id and status_chat == Const.CHATTING_FLG:
            chat_group_info.message_unread_cnt = 1
            chat_group_info.last_message_store_id = store_id

        if status_chat == Const.CHATTING_FLG:
            # update total message
            chat_group_info.message_total_cnt += 1

        # TODO: hardcode admin_id
        chat_group_info.update_id = 888888
        chat_group_data = jsonable_encoder(chat_group_info)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in chat_group_data:
            if field in update_data:
                setattr(chat_group_info, field, update_data[field])
        db.add(chat_group_info)
        db.commit()
        db.refresh(chat_group_info)
        return chat_group_info

    def get_chat_group_buyer(self, db: Session, *, car_id: int) -> Any:
        db_obj = db.query(ChatGroup.id,
                          ChatGroup.div,
                          ChatGroup.firebase_chat_id,
                          ChatGroup.car_id,
                          ChatGroup.store_id,
                          ChatGroup.chassis_number,
                          ChatGroup.message_unread_cnt,
                          ChatGroup.last_message_user_id,
                          ChatGroup.last_message_user_name,
                          ChatGroup.last_message_datetime,
                          ChatGroup.last_message,
                          ChatGroup.chassis_number,
                          Negotiation.id.label("negotiation_id"),
                          CarMarket.store_code,
                          Store.store_name,
                          MCompany.company_name
                          ) \
            .outerjoin(Negotiation, and_(Negotiation.car_id == car_id,
                                         Negotiation.contact_id == ChatGroup.id,
                                         Negotiation.delete_flag == Const.DEL_FLG_NORMAL
                                         )) \
            .join(CarMarket, and_(CarMarket.car_id == car_id,
                                  CarMarket.delete_flag == Const.DEL_FLG_NORMAL, )) \
            .join(Store, and_(Store.id == cast(ChatGroup.store_id, Integer),
                              Store.delete_flag == Const.DEL_FLG_NORMAL)) \
            .join(MCompany, and_(MCompany.company_code == Store.company_code,
                                 MCompany.delete_flag == Const.DEL_FLG_NORMAL)) \
            .filter(ChatGroup.car_id == car_id,
                    ChatGroup.div == DIV_CHAT_GROUP["BUYER"],
                    ChatGroup.delete_flag == Const.DEL_FLG_NORMAL) \
            .order_by(cast(ChatGroup.store_id, Integer).asc()) \
            .all()
        return db_obj

    def get_chat_group_memebers(self, db: Session, *, group_id: int) -> Any:
        db_obj = (
            db.query(ChatGroupMember.user_id, Staff.staff_code)
            .outerjoin(Staff, and_(ChatGroupMember.user_id == Staff.id,
                                   Staff.delete_flag == Const.DEL_FLG_NORMAL))
            .filter(and_(ChatGroupMember.group_id == group_id,
                         ChatGroupMember.delete_flag == Const.DEL_FLG_NORMAL))
            .all()
        )

        if not db_obj:
            return None

        return db_obj

chat_group = CRUDChatGroup(ChatGroup)
