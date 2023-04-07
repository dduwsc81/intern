from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.code_master import CodeMaster
from app.schemas.code_master import CodeMasterCreate, CodeMasterUpdate
from app.models.menu_setting import MenuSetting
from typing import Any

from sqlalchemy import func


class CRUDCodeMaster(CRUDBase[CodeMaster, CodeMasterCreate, CodeMasterUpdate]):
    SEND_ITEM_TYPE_CODE = "send_customer_type_code_new"

    def get_code_name(
            self,
            db: Session,
            code_type: str,
            code_value: int
    ):
        code = db.query(self.model.code_name).filter(CodeMaster.code_type == code_type,
                                                     CodeMaster.code_value == code_value).first()
        return code.code_name if code else ""

    def get_list_service(
            self,
            db: Session
    ):
        list_service = db.query(self.model).filter(CodeMaster.code_type == self.SEND_ITEM_TYPE_CODE).all()
        return list_service


    def get_service_types_by_company(
        self, company_code: str, store_code: str, db: Session
    ) -> Any:
        list_menu = (
            db.query(MenuSetting.code_type_id, func.count(MenuSetting.code_type_id))
            .filter(
                MenuSetting.from_company_code == company_code,
                MenuSetting.from_store_code == store_code,
                MenuSetting.delete_flag == 0,
            )
            .group_by(MenuSetting.code_type_id)
            .subquery("list_menu")
        )
        service_types = (
            db.query(
                self.model.code_name.label("text"),
                self.model.code_value.label("value"),
                self.model.sort_number.label("sort"),
            )
            .filter(CodeMaster.code_type == self.SEND_ITEM_TYPE_CODE)
            .join(list_menu, (list_menu.c.code_type_id == CodeMaster.code_value))
            .all()
        )
        return service_types


code_master = CRUDCodeMaster(CodeMaster)
