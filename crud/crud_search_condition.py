from datetime import date, datetime
from typing import Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas
from app.constants import Const
from app.crud.base import CRUDBase
from app.models.search_condition import SearchCondition
from app.models.search_condition_detail import SearchConditionDetail
from app.schemas.search_condition import SearchConditionCreate, SearchConditionUpdate
from app.schemas.search_condition_detail import SearchConditionDetailCreate


class CRUDSearchCondition(
    CRUDBase[SearchCondition, SearchConditionCreate, SearchConditionUpdate]
):
    def create_search_condition(
        self,
        db: Session,
        *,
        obj_in: SearchConditionCreate,
        item_in: schemas.CarQuery,
        user_id,
    ) -> Any:
        # Function recieve 2 object: search condition and search condition detail

        # Insert a new search condition record
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data,
            insert_id=user_id,
            insert_at=datetime.utcnow(),
            update_id=user_id,
            update_at=datetime.utcnow(),
            delete_flag=Const.DEL_FLG_NORMAL,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # update order index = search_condition_id
        db_obj.order_index = db_obj.search_condition_id
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        obj_data = jsonable_encoder(item_in)

        # For each search condition detail insert a record to search condition detail table have same search_condition_id
        for field, value in obj_data.items():
            setvalue = ""
            # check each type of input search condition and convert to string
            if isinstance(value, int):
                if field in [
                    "car_status_1",
                    "car_status_2",
                    "car_status_3",
                    "car_status_4",
                ]:
                    if value > -1:
                        setvalue = str(value)
                else:
                    if value >= -1:
                        setvalue = str(value)

            if isinstance(value, list):
                if value != []:
                    for item in value:
                        setvalue += str(item) + ","
                    setvalue = setvalue[0 : len(setvalue) - 1]
            if isinstance(value, date):
                if value != None:
                    value = value.__str__()
            if isinstance(value, str):
                setvalue = value
            # if condition exist , create a new search condition detail
            if setvalue != "":
                detail_obj = SearchConditionDetailCreate(
                    search_condition_id=db_obj.search_condition_id,
                    condition_name=field,
                    values=setvalue,
                )
                result = crud.search_condition_detail.create_search_condition_detail(
                    db=db, obj_in=detail_obj
                )
        return db_obj

    # get all search condition
    def get_search_condition(self, db: Session, *, search_tab_id, store_id) -> Any:
        all = db.query(self.model).filter(
            SearchCondition.delete_flag == Const.DEL_FLG_NORMAL,
            SearchCondition.search_tab_id == search_tab_id,
            SearchCondition.store_id == store_id,
        )
        result = all.all()
        return result

    # get a main condition and all detail having same seach condition id
    def get_search_condition_by_id(
        self,
        db: Session,
        *,
        id: int,
        search_tab_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Any:
        result = (
            db.query(self.model, SearchConditionDetail)
            .outerjoin(
                SearchConditionDetail,
                (
                    SearchCondition.search_condition_id
                    == SearchConditionDetail.search_condition_id
                ),
            )
            .filter(
                SearchCondition.search_condition_id == id,
                SearchCondition.delete_flag == Const.DEL_FLG_NORMAL,
                SearchCondition.search_tab_id == search_tab_id,
            )
            .all()
        )
        if not result:
            raise HTTPException(
                status_code=200, detail=f"Search condition {id} not found"
            )

        search_detail = [r[1] for r in result]
        search = [result[0][0]]
        return search, search_detail

    # update search order index swap order of id1 and id2
    def update_search_condition_order(
        self, db: Session, *, search_tab_id: int, id1: int = 1, id2: int = 1
    ) -> Any:
        db_obj1 = (
            db.query(self.model)
            .filter(
                SearchCondition.search_condition_id == id1,
                SearchCondition.search_tab_id == search_tab_id,
                SearchCondition.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )
        if not db_obj1:
            raise HTTPException(
                status_code=404, detail=f"Search condition {id1} not found"
            )

        db_obj2 = (
            db.query(self.model)
            .filter(
                SearchCondition.search_condition_id == id2,
                SearchCondition.search_tab_id == search_tab_id,
                SearchCondition.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )
        if not db_obj2:
            raise HTTPException(
                status_code=404, detail=f"Search condition {id2} not found"
            )

        order1 = db_obj1.order_index
        order2 = db_obj2.order_index

        if order1 is not None and order2 is not None:
            db_obj1.order_index = order2
            db_obj2.order_index = order1
            db.add(db_obj1)
            db.add(db_obj2)
            db.commit()
            db.refresh(db_obj1)
            db.refresh(db_obj2)
        return db_obj1, db_obj2

    # delete search_condition by updating delete_flag
    def delete_search_condition(
        self, db: Session, *, id: int, search_tab_id: int
    ) -> Any:
        db_obj = (
            db.query(self.model)
            .filter(
                SearchCondition.search_condition_id == id,
                SearchCondition.search_tab_id == search_tab_id,
                SearchCondition.delete_flag == Const.DEL_FLG_NORMAL,
            )
            .first()
        )
        if not db_obj:
            raise HTTPException(
                status_code=404, detail=f"Search condition {id} not found"
            )
        db_obj.delete_flag = Const.DEL_FLG_DELETE
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


search_condition = CRUDSearchCondition(SearchCondition)
