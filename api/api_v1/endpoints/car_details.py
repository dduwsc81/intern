from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.CarDetails])
def get_car_details(
        db: Session = Depends(deps.get_db),
        page: int = 1,
        page_size: int = 10,
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve car details.
    """
    # if crud.user.is_superuser(current_user):
    #     items = crud.item.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.item.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    skip = (page - 1) * page_size
    limit = page_size
    cardetails = crud.car_details.get_cardetails(db, skip=skip, limit=limit)
    return cardetails


@router.get("/{id}")
def get_cardetail_by_id(
        id: int = 1,
        db: Session = Depends(deps.get_db),
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve cars by id
    """
    car = crud.car_details.get_cardetails_by_id(db, id=id)
    return car


@router.post("/", response_model=schemas.CarDetails)
def create_cardetail(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.CarDetailsCreate,
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Create new car detail.
    """
    cardetail = crud.car_details.create_car_details(db=db, obj_in=item_in)
    return cardetail


@router.put("/{id}", response_model=schemas.CarDetails)
def update_cardetail(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.CarDetailsUpdate,
        id: int
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Update car detail.
    """
    cardetail = crud.car.update_cardetails_by_id(db=db, obj_in=item_in, id=id)
    return cardetail


@router.delete("/{id}", response_model=schemas.CarDetails)
def delete_cardetail(
        *,
        db: Session = Depends(deps.get_db),
        id: int
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Delete  cardetail by setting delete_flag = 1
    """
    cardetail = crud.car_details.delete_by_update_deleteflag(db=db, id=id)
    # car = crud.car.delete_car_by_id(db=db, id=id)
    return cardetail
