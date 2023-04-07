from typing import Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.base import CRUDBase
from app.models.like_detail import LikeDetail
from app.schemas.like_detail import LikeDetailCreate, LikeDetailUpdate
from fastapi.encoders import jsonable_encoder
from app.models.m_company import MCompany
from app.models.store import Store


class CRUDLikeDetail(CRUDBase[LikeDetail, LikeDetailCreate, LikeDetailUpdate]):
    # Get like detail by car id
    def get_number_of_likes_by_car_id(
            self, db: Session, *, car_id: int
    ) -> Any:
        try:
            like_detail = db.query(self.model).filter(LikeDetail.car_id == car_id, LikeDetail.delete_flag == 0).count()
            return like_detail
        except Exception as e:
            return {"Message:": repr(e)}

    # get total and info like
    def get_like_info(self, db, car_id):
        like_info = db.query(LikeDetail.id.label("like_id"), Store.store_name.label("store_like"),
                             MCompany.company_name.label("company_like")). \
            outerjoin(Store, (LikeDetail.store_id == Store.id)). \
            outerjoin(MCompany, (Store.company_code == MCompany.company_code)). \
            filter(LikeDetail.car_id == car_id, LikeDetail.delete_flag == 0).all()
        return like_info


like_detail = CRUDLikeDetail(LikeDetail)
