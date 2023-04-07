from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CarEquipmentDetailsBase(BaseModel):
    id: Optional[int]
    car_id: Optional[int]
    etc: Optional[int]
    navi: Optional[int]
    apple_carplay: Optional[int]
    audroid_auto: Optional[int]
    bluetooth_connect: Optional[int]
    usb_input_device: Optional[int]
    v_power_100: Optional[int]
    drive_recorder: Optional[int]
    rear_seat_monitor: Optional[int]
    back_camera: Optional[int]
    camera_360: Optional[int]
    slide_door_left: Optional[int]
    slide_door_right: Optional[int]
    electric_rear_gate: Optional[int]
    airbag: Optional[int]
    idling_stop: Optional[int]
    anti_theft_device: Optional[int]
    sunroof: Optional[int]
    roof_carrier: Optional[int]
    roof_box: Optional[int]
    leather_seat: Optional[int]
    row_seat_3: Optional[int]
    seat_heater: Optional[int]
    seat_cooler: Optional[int]
    full_flat_sheet: Optional[int]
    cruise_control: Optional[int]
    cruise_control_following: Optional[int]
    autopilot: Optional[int]
    lane_keep_assist: Optional[int]
    parking_assist: Optional[int]
    obstacle_sensor: Optional[int]
    lane_departure_warning: Optional[int]
    electronic_stability_control: Optional[int]
    collision_damage_mitigation_brake: Optional[int]
    prevention_false_start: Optional[int]
    auto_light: Optional[int]
    car_rental: Optional[int]
    test_drive: Optional[int]

class CarEquipmentDetailsCreate(CarEquipmentDetailsBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]


class CarEquipmentDetailsInDB(CarEquipmentDetailsBase):
    insert_id: Optional[int]
    insert_at: Optional[datetime]
    update_id: Optional[int]
    update_at: Optional[datetime]
    delete_id: Optional[int]
    delete_at: Optional[datetime]
    delete_flag: Optional[int]

    class Config:
        orm_mode = True


class CarEquipmentDetailsUpdate(CarEquipmentDetailsInDB):
    pass

