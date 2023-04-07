from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.cars_api import CarsApi
from app.models.cars_authority import CarsAuthority
from app.models.cars_role import CarsRole
from starlette.status import HTTP_401_UNAUTHORIZED


class CRUDAuthorized(CRUDBase[CarsRole, None, None]):
    """ Check Authorized """

    def check_authority(self, db: Session, *, auth_company_code: str, company_code: str, role_name: str,
                        userpool_id: str, api_type: str,
                        operationid: str) -> Optional:
        # Authority existence check (exact match pattern)
        count = db.query(func.count(self.model.id)) \
            .join(CarsAuthority, self.model.id == CarsAuthority.role_id) \
            .join(CarsApi, CarsAuthority.api_id == CarsApi.id) \
            .filter(self.model.company_code == auth_company_code, self.model.role == role_name,
                    self.model.userpool_id == userpool_id, CarsApi.company_code == company_code,
                    CarsApi.api_type == api_type, CarsApi.operationid == operationid) \
            .scalar()

        if count > 0:
            return

        # Authority exists check (role wildcard pattern)
        count = db.query(func.count(self.model.id)) \
            .join(CarsAuthority, self.model.id == CarsAuthority.role_id) \
            .join(CarsApi, CarsAuthority.api_id == CarsApi.id) \
            .filter(self.model.company_code == auth_company_code, self.model.role == '*',
                    self.model.userpool_id == userpool_id, CarsApi.company_code == company_code,
                    CarsApi.api_type == api_type, CarsApi.operationid == operationid) \
            .scalar()

        if count > 0:
            return

        # Authority exists check (wildcard pattern company ID is)
        count = db.query(func.count(self.model.id)) \
            .join(CarsAuthority, self.model.id == CarsAuthority.role_id) \
            .join(CarsApi, CarsAuthority.api_id == CarsApi.id) \
            .filter(self.model.role == '*',
                    self.model.userpool_id == userpool_id, CarsApi.company_code == company_code,
                    CarsApi.api_type == api_type, CarsApi.operationid == operationid) \
            .scalar()

        if count > 0:
            return

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


authorized = CRUDAuthorized(CarsRole)
