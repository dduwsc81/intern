from typing import Any, List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.m_company import MCompany
from app.models.store import Store
from app.schemas.m_company import MCompanyBase, MCompanyCreate, MCompanyUpdate
from datetime import datetime, timedelta
from app import crud
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


class CRUDCompany(CRUDBase[MCompany, MCompanyCreate, MCompanyUpdate]):

    # Get list company
    def get_list_company(
            self, db: Session
    ) -> MCompany:
        list_company = db.query(
            self.model.company_code,
            self.model.company_name,
        ).filter(MCompany.delete_flag == 0).all()
        return list_company

    # Get list store by company_code
    def get_list_store(
            self, db: Session,
            company_code
    ) -> List[Store]:
        list_store = db.query(Store.store_code,
                              Store.id,
                              Store.store_name). \
            filter(Store.company_code == company_code, Store.delete_flag == 0).all()
        list_store = jsonable_encoder(list_store)
        return list_store

    # Get the name of companies
    def get_name_of_companies(
            self, db: Session
    ) -> MCompany:
        companies = db.query(
            self.model.company_code,
            self.model.company_name
        ).filter(MCompany.delete_flag == 0).all()
        return companies


m_company = CRUDCompany(MCompany)
