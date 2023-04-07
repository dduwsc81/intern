from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from fastapi.encoders import jsonable_encoder
from .format_status import *

router = APIRouter()

MAPPING_IMAGE_VALUE = {
    1: "front_exterior_image",
    2: "side_exterior_image",
    3: "back_exterior_image",
    4: "optional_exterior_image",
    5: "repair_exterior_image",
    6: "front_interior_image",
    7: "seat_interior_image",
    8: "meter_interior_image",
    9: "option_interior_image",
    10: "repair_interior_image",
}

@router.get("", response_model=List[schemas.Car])
def get_cars(
        db: Session = Depends(deps.get_db),
        page: int = 1,
        page_size: int = 10
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve cars.
    """
    # if crud.user.is_superuser(current_user):
    #     items = crud.item.get_multi(db, skip=skip, limit=limit)
    # else:
    #     items = crud.item.get_multi_by_owner(
    #         db=db, owner_id=current_user.id, skip=skip, limit=limit
    #     )
    skip = (page - 1) * page_size
    limit = page_size
    cars, count = crud.car.get_cars(db, skip=skip, limit=limit)
    car = jsonable_encoder(cars)
    # format sales_period_start
    for item in car:
        item['sales_period_start'] = format_response_sales_period_start(item['sales_period_start'])
        item["number_of_favorites"] = crud.favourite.get_number_of_favourites_by_car_id(db, car_id=item["car_id"])
        item["number_of_likes"] = crud.like_detail.get_number_of_likes_by_car_id(db, car_id=item["car_id"])
        buy_now_total_price = crud.register_sale.get_buy_now_total_price(db, max_date=item["max_date"],
                                                                         car_id_sale=item[
                                                                             "car_id_sale"])
        item["buy_now_total_price"] = buy_now_total_price["buy_now_total_price"] if buy_now_total_price else None
    re = {'total': count, 'limit': limit, 'offset': skip, 'results': car}
    res = return_response_header(re)
    return res


@router.get("/{id}", response_model=schemas.CarFullDetail)
def get_car_by_id(
        id: int = 1,
        db: Session = Depends(deps.get_db)
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve cars by id
    """
    # car, list_cars, favourite_info, like_info = crud.car.get_list_car_with_same_chassis_number(
    #     db, id=id)
    # car = jsonable_encoder(car)
    # car['sales_period_start'] = format_response_sales_period_start(car['sales_period_start'])
    # list_cars = jsonable_encoder(list_cars)
    # favourite_info = jsonable_encoder(favourite_info)
    # like_info = jsonable_encoder(like_info)
    #
    # # add list_owner, list_favorite, number_of_favorites to result
    # car['list_owner'] = list_cars
    # car["list_favorite"] = favourite_info
    # car["number_of_favorites"] = len(favourite_info)
    # car["list_like"] = like_info
    # car["number_of_likes"] = len(like_info)

    car, list_car_life_code, car_eq_detail = crud.car.get_car_by_id(db, id=id)

    db_obj = jsonable_encoder(car)
    result = schemas.CarFullDetail(**db_obj)

    result.customer_info = schemas.CustomerInfoInCarDetail(**db_obj)
    # format response: put customer_prefectures_name into customer_info.prefectures_name
    result.customer_info.prefectures_name = db_obj['customer_prefectures_name']
    if list_car_life_code is not None and result.customer_info is not None:
        life_codes = [life_code[0] for life_code in list_car_life_code]
        result.customer_info.car_life_code = life_codes
    if car_eq_detail:
        result.car_equipment_details = schemas.CarEquipmentDetailsBase(**(jsonable_encoder(car_eq_detail)))

    return jsonable_encoder(result)


@router.post("/search", response_model=schemas.CarSearchResponse)
async def car_search(
        db: Session = Depends(deps.get_db),
        page: int = 1,
        page_size: int = 10,
        item_in: schemas.CarQuery = None
        # current_user: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Search car function to show car on screen car list
    Input query param as a request body to search
    """
    skip = (page - 1) * page_size
    limit = page_size

    car_filter, count = crud.car.filter_cars(
        db=db,
        skip=skip,
        limit=limit,
        item_in=item_in
    )
    cars = jsonable_encoder(car_filter)
    result = list()
    # convert data
    for row in cars:
        result.append(schemas.CarInfo(**row))
    return {'total': count, 'results': result}



@router.get("/{id}/photos", response_model=schemas.CarFullPhoto)
def get_car_photo_by_id(
        id: int = 1,
        db: Session = Depends(deps.get_db),
        # token: schemas.TokenPayload = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve car photo by id
    """
    result = schemas.CarFullPhoto()

    car_photo_thumbnail, list_image_car = crud.car.get_car_photos_by_id(db, id=id)

    if car_photo_thumbnail is not None:
        result = schemas.CarFullPhoto(**car_photo_thumbnail)

    if list_image_car is not None:
        for item in list_image_car:
            # Mapping return list image value to property's name of the image
            setattr(
                result,
                MAPPING_IMAGE_VALUE[item["image_value"]],
                item["bucket_name"] + item["key"],
            )
    return jsonable_encoder(result)
