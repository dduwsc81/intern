from typing import Any, List
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("", response_model=List[schemas.MCompanyBasic])
def get_company_and_store(
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get list company.
    """
    list_company = crud.m_company.get_list_company(db)
    list_company = jsonable_encoder(list_company)
    results = list()
    for item in list_company:
        item["store_info"] = crud.m_company.get_list_store(db, company_code=item["company_code"])
        results.append(schemas.MCompanyBasic(**item))
    return results


@router.get("/all", response_model=schemas.MCompany)
def get_companies(
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get the name of companies
    """
    companies = crud.m_company.get_name_of_companies(db=db)
    r = {"companies": companies}
    result = jsonable_encoder(r)
    return JSONResponse(result)
