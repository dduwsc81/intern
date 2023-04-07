from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.encoders import jsonable_encoder
import json
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("", response_model=List[schemas.Car])
def get_areas(
        # company_id: str,
        db: Session = Depends(deps.get_db)
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve offers.
    """
    # if crud.user.is_superuser(current_user):
    #     items = crud.item.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.item.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    areas_filter, count = crud.m_prefecture.get_prefectures(db)
    areas = jsonable_encoder(areas_filter)
    re = {'total': count, 'results': areas}
    r = json.dumps(re)
    return JSONResponse(content=json.loads(r))


# @router.get("/{id}", response_model=schemas.Car)
# def get_offer_by_id(
#         id: int = 1,
#         db: Session = Depends(deps.get_db)
#         # token: schemas.TokenPayload = Depends(deps.get_current_user),
# ) -> Any:
#     """
#     Retrieve offer by id
#     """
#     offer, store_out, list_car_same_chassis_number = crud.offer.get_offer_by_id(db, id=id)
#     resp = jsonable_encoder(offer)
#     list_car_same_chassis_number = jsonable_encoder(list_car_same_chassis_number)
#     for item in list_car_same_chassis_number:
#         item.pop("id")
#         item["company_name_owner"] = item.pop("company_name")
#     resp["other_store"] = list_car_same_chassis_number
#     resp["company_name_offer"] = store_out[0]
#     resp["offer_out_store_name"] = store_out[1]
#     re = {"response": resp}
#     r = json.dumps(re)
#     return JSONResponse(content=json.loads(r))

