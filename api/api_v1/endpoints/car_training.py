from typing import Any, Optional

import requests
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/create", response_model=schemas.CarTrainingBase)
def create_car_training(
        item_in: schemas.CarTrainingCreate,
        db: Session = Depends(deps.get_db),

) -> Any:
    item = crud.cartraining.create_car_training(db=db, item_in=item_in)
    # car_training = jsonable_encoder(car_training)
    car_training = jsonable_encoder(item)
    return car_training


@router.get("/all")
def get_all_car_training(
        db: Session = Depends(deps.get_db)
) -> Any:
    car_trainings = crud.cartraining.get_all_car_training(db=db)
    list = {"car_training": car_trainings}
    result = jsonable_encoder(list)
    return result


@router.get("/all/page/{page}")
def get_car_in_page(
        page: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    row_per_page = 5
    item_in_db = crud.cartraining.get_car_by_page(page=page, row_per_page=row_per_page, db=db)
    if len(item_in_db) == 0:
        result = "No data available"
    else:
        list = {f"Page {page}": item_in_db}
        result = jsonable_encoder(list)
    return result


@router.get("/all/{id}", response_model=schemas.CarTrainingInDB)
def get_car_training_by_id(
        id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    car_training = crud.cartraining.get_car_training_by_id(id=id, db=db)
    result = jsonable_encoder(car_training)
    return result


@router.put("/update/{id}", response_model=schemas.CarTrainingInDB)
def update_car_training(
        id: int,
        item_in: schemas.CarTrainingUpdate,
        db: Session = Depends(deps.get_db)
) -> Any:
    item = crud.cartraining.update_car_training(id, item_in, db)
    result = jsonable_encoder(item)
    return result


@router.delete("/delete/{id}")
def delete_car_training(
        id: int,
        db: Session = Depends(deps.get_db)
) -> Any:
    return crud.cartraining.delete_car_training(id=id, db=db)
