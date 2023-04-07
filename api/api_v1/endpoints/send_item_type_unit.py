from typing import Any

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/{company_code}", response_model=schemas.SendItemTypeUnit)
def get_service_units(
        company_code: str,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get the name of companies
    """
    service_units = crud.send_item_type_unit.get_service_unit_by_company(db=db, company_code=company_code)
    r = {"service_units": service_units}
    result = jsonable_encoder(r)
    return JSONResponse(result)


@router.delete("/{id}", response_model=schemas.SendItemTypeUnit)
def delete_service_unit(
        id: int,
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    service_unit = crud.send_item_type_unit.detele_service_unit_by_update_delete_flag(db=db, id=id)
    return service_unit


@router.post("", response_model=schemas.SendItemTypeUnit)
def create_service_unit(
        item_in: schemas.SendItemTypeUnitCreate,
        *,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create new service unit.
    """
    service_unit = crud.send_item_type_unit.create_service_unit(db=db, obj_in=item_in)
    return service_unit
