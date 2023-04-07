from typing import List, Union, Dict, Any

from sqlalchemy.sql.expression import update
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.models.m_company import MCompany
from app.models.store import Store
from app.crud.base import CRUDBase
from app.models.favourite import Favourite
from app.schemas.favourite import FavouriteCreate, FavouriteUpdate


class CRUDFavourite(CRUDBase[Favourite, FavouriteCreate, FavouriteUpdate]):

    # Get favourite by car id
    def get_number_of_favourites_by_car_id(
            self, db: Session, *, car_id: int
    ) -> Any:
        try:
            favourite = db.query(self.model).filter(Favourite.car_id == car_id, Favourite.delete_flag == 0).count()
            return favourite
        except Exception as e:
            return {"Message:": repr(e)}

    # Get favourite by store id
    def get_favourite_by_store_id(
            self, db: Session, *, store_id: str
    ) -> Any:
        try:
            favourite = db.query(self.model).filter(Favourite.store_id == store_id, Favourite.delete_flag == 0).all()
            if not favourite:
                return None
            return favourite
        except Exception as e:
            return {"Message:": repr(e)}

    # get total and info favorite
    def get_favorite_info(self, db, car_id):
        favourite_info = db.query(self.model.id.label("favorite_id"), Store.store_name.label("store_favorite"),
                                  MCompany.company_name.label("company_favorite")). \
            outerjoin(Store, (Favourite.store_id == Store.id)). \
            outerjoin(MCompany, (Store.company_code == MCompany.company_code)). \
            filter(Favourite.car_id == car_id, Favourite.delete_flag == 0).all()
        return favourite_info


favourite = CRUDFavourite(Favourite)
