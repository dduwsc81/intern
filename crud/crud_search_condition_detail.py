from datetime import datetime
from typing import Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.constants import Const
from app.crud.base import CRUDBase
from app.models.search_condition_detail import SearchConditionDetail
from app.schemas.search_condition_detail import (
    SearchConditionDetailCreate,
    SearchConditionDetailUpdate,
)


class CRUDSearchConditionDetail(
    CRUDBase[
        SearchConditionDetail, SearchConditionDetailCreate, SearchConditionDetailUpdate
    ]
):
    def create_search_condition_detail(
        self, db: Session, *, obj_in: SearchConditionDetailCreate
    ) -> SearchConditionDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            insert_id=1,
            insert_at=datetime.utcnow(),
            update_id=1,
            update_at=datetime.utcnow(),
            delete_flag=Const.DEL_FLG_NORMAL,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_search_condition_detail(
        self, db: Session, *, skip: int = 0, limit: int = 10
    ) -> Any:
        all = (
            db.query(self.model)
            .filter(SearchConditionDetail.delete_flag == Const.DEL_FLG_NORMAL)
            .all()
        )
        all.count()
        result = all.offset(skip).limit(limit).all()
        return cars, result

    def get_search_conditiondetail_by_id(
        self, db: Session, *, id: int, skip: int = 0, limit: int = 100
    ) -> Any:
        result = (
            db.query(self.model)
            .filter(
                SearchConditionDetail.search_condition_id == id,
                SearchConditionDetail.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )
        if not result:
            raise HTTPException(
                status_code=200, detail=f"Search condition detail {id} not found"
            )
        return result


search_condition_detail = CRUDSearchConditionDetail(SearchConditionDetail)
