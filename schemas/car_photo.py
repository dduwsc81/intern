from typing import Optional

from pydantic import BaseModel
from datetime import date,datetime

# Shared properties
class CarPhotoBase(BaseModel):
    id : Optional[int]
    car_id: Optional[int]
    image_div: Optional[int]
    display_index : Optional[int]
    s3_file_id: Optional[int]
    url: Optional[str]

# Properties to receive on item creation
class CarPhotoCreate(CarPhotoBase):
    pass


# Properties to receive on item update
class CarPhotoUpdate(CarPhotoBase):
    pass


# Properties shared by models stored in DB
class CarPhotoInDBBase(CarPhotoBase):
    id : Optional[int]
    car_id: Optional[int]
    image_div: Optional[int]
    display_index : Optional[int]
    s3_file_id: Optional[int]
    url: Optional[str]
    insert_id : Optional[int]
    insert_at : Optional[datetime]
    update_id : Optional[int]
    update_at : Optional[datetime]
    delete_id : Optional[int]
    delete_at : Optional[datetime]
    delete_flag : Optional[int]
    # owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class CarPhoto(CarPhotoInDBBase):
    pass


# Properties properties stored in DB
class CarPhotoInDB(CarPhotoInDBBase):
    pass

# Get information of full photo of the car in detail car screen
class CarFullPhoto(BaseModel):
    url: Optional[str]
    front_exterior_image: Optional[str]
    side_exterior_image: Optional[str]
    back_exterior_image: Optional[str]
    optional_exterior_image: Optional[str]
    repair_exterior_image: Optional[str]
    front_interior_image: Optional[str]
    seat_interior_image: Optional[str]
    meter_interior_image: Optional[str]
    option_interior_image: Optional[str]
    repair_interior_image: Optional[str]