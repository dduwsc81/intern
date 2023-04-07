from typing import List, Union, Dict, Any
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, contains_eager, aliased

from dateutil import tz
from dateutil.relativedelta import relativedelta

from app.crud.base import CRUDBase
from app.constants import Constants

from app.models.car_details import CarDetails
from app.models.car import Car
from app.models.register_sale import RegisterSale
from app.models.offer import Offer
from app.models.m_company import MCompany
from app.models.car_photo import CarPhoto
from app.models.store import Store
from app.models.s3_file import S3File
from app.models.customer import Customer
from app.models.m_prefectures import MPrefectures
from app.models.car_market import CarMarket
from app.models.negotiation import Negotiation
from app.models.m_division import MDivision
from app.models.assess import Assess
from app.models.favourite import Favourite
from app.models.car_inspection import CarInspection
from app.models.customer_active_status import CustomerActiveStatus
from app.models.car_license import CarLicense
from app.models.customer_car_life_master_link import CustomerCarLifeMasterLink
from app.models.car_equipment_details import CarEquipmentDetails
from app.models.customer_market import CustomerMarket
from app.models.chat_group import ChatGroup
from app.schemas.car import CarCreate, CarUpdate, CarQuery
from sqlalchemy import or_, union_all, literal_column, func, and_, case, cast, DECIMAL
from ..api.api_v1.endpoints.format_status import *
from app import crud
from app.constants import Const

CAR_PHOTO = {"CAR_PHOTO_THUMBNAIL": 1, "CAR_PHOTO_DETAIL": 2}

NO_LIMIT_PRICE = -1
ACTIVE_STATUS = 1
THUMBNAIL_IMG = 1
NOT_HIDE_CAR = 0
BUYER_CHAT = 1
HOPE_PRICE = 2
MARKET_PRICE = 3
STATUS_MARKET_PRICE = 0
ALL_PRICE = 1
TRUE = 1
FALSE = 0
NEW_DURATION = 2
MILE_ALERT = 70000


class CRUDCar(CRUDBase[Car, CarCreate, CarUpdate]):
    def get_cars(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> Any:
        squery = db.query(RegisterSale.car_id.label("car_id_sale"),
                          func.max(RegisterSale.period_to).label("max_date")).group_by(RegisterSale.car_id).subquery(
            'register_sale')
        squery_price = db.query(RegisterSale.car_id, RegisterSale.period_to,
                                RegisterSale.hope_sale_base_price.label("hope_sale_base_price")).filter(
            RegisterSale.delete_flag == 0).subquery("register_sale_price")
        all_cars = db.query(self.model.company_code,
                            self.model.id.label("car_id"),
                            self.model.maker,
                            self.model.car_type,
                            self.model.grade,
                            self.model.car_mileage,
                            self.model.registration_end_date,
                            CarDetails.sales_period_start,
                            CarDetails.aggregation_wholesale_price_market,
                            CarDetails.aggregation_retail_price_market,
                            squery.c.max_date,
                            squery.c.car_id_sale,
                            MPrefectures.name.label("area"),
                            MCompany.company_name,
                            Store.store_name,
                            Store.store_code,
                            CarPhoto.url.label("thumbnail_url"),
                            Favourite.id.label("favourite_id"),
                            squery_price.c.hope_sale_base_price
                            ). \
            outerjoin(CarDetails, (Car.id == CarDetails.car_id)). \
            outerjoin(CarMarket, (Car.id == CarMarket.car_id)). \
            outerjoin(MPrefectures, (CarMarket.prefectures_cd == MPrefectures.prefectures_code)). \
            outerjoin(CarPhoto, (Car.id == CarPhoto.car_id) & (CarPhoto.image_div == 1)). \
            outerjoin(MCompany, (Car.company_code == MCompany.company_code)). \
            outerjoin(squery, and_(Car.id == squery.c.car_id_sale)). \
            outerjoin(squery_price, and_(squery_price.c.car_id == squery.c.car_id_sale,
                                         squery_price.c.period_to == squery.c.max_date)). \
            outerjoin(Customer,
                      (Car.car_decision_maker == Customer.customer_code) & (Car.company_code == Customer.company_code)). \
            outerjoin(Store,
                      (Store.store_code == Customer.my_store_code) & (Store.company_code == Customer.company_code)). \
            outerjoin(Favourite,
                      and_(Car.id == Favourite.car_id,
                           Favourite.delete_flag == Constants.DEL_FLG_NORMAL)). \
            filter(Car.delete_flag == 0, CarDetails.delete_flag == 0, CarMarket.delete_flag == 0,
                   CarMarket.hide_flag == 0).order_by(Car.id.asc()). \
            offset(skip).limit(limit).all()
        total = db.query(self.model). \
            outerjoin(CarDetails, (Car.id == CarDetails.car_id)). \
            outerjoin(CarMarket, (Car.id == CarMarket.car_id)). \
            filter(Car.delete_flag == 0, CarDetails.delete_flag == 0, CarMarket.delete_flag == 0,
                   CarMarket.hide_flag == 0).count()
        return all_cars, total

    # Get details of vehicles with the same chassis number
    def get_list_car_with_same_chassis_number(
            self, db: Session, *, id: int
    ) -> Any:
        # car, list_offers = self.get_car_by_id(db, id=id)
        # car = jsonable_encoder(car)
        # car['offer_info'] = list_offers
        # list_car_same_chassis_number = db.query(Car.id). \
        #     filter(Car.chassis_number == car['chassis_number'], Car.id != car['car_id'], Car.delete_flag == 0).all()
        # list_cars = []
        # for item in list_car_same_chassis_number:
        #     car_detail = self.get_other_info_car_by_id(db, id=item[0])
        #     car_detail = jsonable_encoder(car_detail)
        #     list_cars.append(car_detail)
        # favourite_info = crud.favourite.get_favorite_info(db, car_id=id)
        # like_info = crud.like_detail.get_like_info(db, car_id=id)
        # car.pop('car_id')
        # car.pop('chassis_number')
        # return car, list_cars, favourite_info, like_info
        pass

    def get_car_by_id(
            self, db: Session, *, id: int
    ) -> Car:
        car = (
            db.query(
                Car.company_code,
                Car.car_code,
                Car.car_decision_maker,
                Car.company_code,
                Car.aggregation_maker,
                Car.chassis_number,
                Car.aggregation_car_type,
                Car.aggregation_grade,
                Car.land_transport_office,
                Car.car_registration_number,
                Car.car_registration_number_kana,
                Car.car_registration_number_type,
                Car.registration_first_date,
                Car.registration_end_date,
                Car.registration_start_date,
                Car.purchase_intention,
                Car.car_mileage,
                Car.grade,
                Car.car_type,
                Car.maker,
                Car.car_mileage_inspection_datetime,
                MDivision.desc.label("car_status_desc"),
                MPrefectures.name.label("prefectures_name"),
                CarMarket.car_status,
                CarMarket.car_active_status,
                CarMarket.store_code,
                CarMarket.new_car_price,
                CarMarket.color_name,
                CarMarket.prefectures_cd,
                CarMarket.view_detail_cnt.label("view_cnt"),
                CarMarket.one_onwer_flg,
                CarMarket.no_smoking_car_flg,
                CarMarket.garage,
                CarMarket.periodic_inspection_record_book,
                CarMarket.registered_car_flg,
                CarMarket.import_type,
                CarMarket.dealer_car_flg,
                CarMarket.body_type,
                CarMarket.drive,
                CarMarket.handle_type,
                CarMarket.shift,
                CarMarket.displacement_power.label("car_market_displacement_power"),
                CarMarket.seats_cnt,
                CarMarket.fuel,
                CarMarket.fuel_economy,
                CarMarket.tire_type,
                CarMarket.cold_region_spec,
                CarMarket.door_number,
                CarMarket.key_cnt,
                CarMarket.check_car,
                CarMarket.hide_flag,
                CarMarket.overall_evaluation,
                CarMarket.interior_evaluation,
                CarMarket.exterior_evaluation,
                CarMarket.repair_history_flag,
            )
                .join(
                CarMarket,
                and_(
                    Car.id == CarMarket.car_id,  # noqa: E501
                    CarMarket.delete_flag == Const.DEL_FLG_NORMAL,
                ),
            )
                .outerjoin(
                MDivision,
                and_(
                    MDivision.param == CarMarket.car_status,
                    MDivision.div == 1,
                    MDivision.delete_flag == Const.DEL_FLG_NORMAL,
                ),
            )
                .outerjoin(
                MPrefectures,
                and_(
                    CarMarket.prefectures_cd == MPrefectures.prefectures_code,
                )
            )
                .filter(and_(Car.id == id, Car.delete_flag == Const.DEL_FLG_NORMAL))
        )

        # Get car price , sales status, negotiation status
        car = (
            car.add_columns(
                CarDetails.tire_size_inspection_datetime,
                CarDetails.aggregation_wholesale_price_market,
                CarDetails.battery_status,
                CarDetails.battery_status_inspection_datetime,
                CarDetails.battery_size,
                CarDetails.battery_size_inspection_datetime,
                CarDetails.battery_create_date,
                CarDetails.tire_status,
                CarDetails.tire_status_inspection_datetime,
                CarDetails.tire_size_front,
                CarDetails.tire_size_rear,
                CarDetails.tire_create_year,
                CarDetails.tire_create_week,
                CarDetails.tire_create_year_week_inspection_datetime,
                CarDetails.tire_grooves_front,
                CarDetails.tire_grooves_front_r,
                CarDetails.tire_grooves_rear,
                CarDetails.tire_grooves_rear_r,
                CarDetails.tire_grooves_inspection_datetime,
                CarDetails.engine_oil_status,
                CarDetails.engine_oil_status_inspection_datetime,
                CarDetails.brake_fluid_status,
                CarDetails.brake_fluid_status_inspection_datetime,
                CarDetails.engine_coolant_status,
                CarDetails.engine_coolant_status_inspection_datetime,
                CarDetails.at_ctv_field_status,
                CarDetails.at_ctv_field_status_inspection_datetime,
                CarDetails.wiper_status,
                CarDetails.wiper_status_inspection_datetime,
                CarDetails.lamp_status,
                CarDetails.lamp_status_inspection_datetime,
                CarDetails.front_exterior_image,
                CarDetails.side_exterior_image,
                CarDetails.back_exterior_image,
                CarDetails.optional_exterior_image,
                CarDetails.repair_exterior_image,
                CarDetails.front_interior_image,
                CarDetails.seat_interior_image,
                CarDetails.meter_interior_image,
                CarDetails.option_interior_image,
                CarDetails.repair_interior_image,
                RegisterSale.id.label("register_sale_id"),
                RegisterSale.register_sale_type,
                RegisterSale.hope_sale_base_price_tax,
                RegisterSale.period_to,
                RegisterSale.register_sale_status,
                RegisterSale.assess_id,
                RegisterSale.transfer_total_amount_tax,
                RegisterSale.platform_fee_tax,
                RegisterSale.brokerage_fee_tax,
                Assess.assess_status,
                Negotiation.id.label("negotiation_id"),
                Negotiation.negotiation_status,
                Negotiation.negotiation_store_id,
                Negotiation.period_to.label("negotiation_period_to"),
                Negotiation.period_from.label("negotiation_period_from"),
                CarDetails.aggregation_wholesale_price_low,
                CarDetails.aggregation_wholesale_price_high,
                RegisterSale.hope_sale_base_price,
                CarDetails.aggregation_retail_price_high,
                CarDetails.aggregation_retail_price_low,
                CarDetails.aggregation_retail_price_middle,
                CarDetails.aggregation_retail_price_market,
            ).join(
                CarDetails,
                and_(
                    Car.id == CarDetails.car_id,
                    CarDetails.delete_flag == Const.DEL_FLG_NORMAL,
                ),
            )
                .outerjoin(
                RegisterSale,
                and_(
                    Car.id == RegisterSale.car_id,
                    RegisterSale.delete_flag == Const.DEL_FLG_NORMAL,
                ),
            ).outerjoin(
                Assess,
                and_(
                    Car.id == Assess.car_id,
                    Car.company_code == Assess.company_code,
                    Assess.delete_flag == Const.DEL_FLG_NORMAL,
                ),
            ).outerjoin(
                Negotiation,
                and_(
                    Car.id == Negotiation.car_id,
                    Negotiation.delete_flag == Const.DEL_FLG_NORMAL,
                    Negotiation.register_sale_id == RegisterSale.id,
                ),
            )
        )

        # Get number of favorite
        sub_cnt_favorite = db.query(
                                Favourite.car_id.label("car_id"),
                                func.count(Favourite.car_id).label("favorite_cnt"),
                            ).filter(
                                Favourite.car_id == id, Favourite.delete_flag == Const.DEL_FLG_NORMAL
                            ).group_by(Favourite.car_id).subquery("sub_cnt_favorite")

        car = car.add_columns(
            sub_cnt_favorite.c.favorite_cnt.label("favorite_cnt")
        ).outerjoin(sub_cnt_favorite, and_(Car.id == sub_cnt_favorite.c.car_id))

        # Get car inspection info
        car = car.add_columns(
            CarInspection.car_category,
            CarInspection.purpose,
            CarInspection.private_business.label("car_private_business"),
            CarInspection.car_shape,
            CarInspection.passenger_capacity,
            CarInspection.maximum_payload,
            CarInspection.car_weight,
            CarInspection.car_total_weight,
            CarInspection.car_length,
            CarInspection.car_width,
            CarInspection.car_height,
            CarInspection.car_inspection_type,
            CarInspection.engine_type,
            CarInspection.displacement_power,
            CarInspection.fuel_type,
            CarInspection.type_number,
            CarInspection.category_number,
            CarInspection.front_front_axle_weight,
            CarInspection.front_rear_axle_weight,
            CarInspection.rear_rear_axle_weight,
            CarInspection.rear_front_axle_weight,
        ).outerjoin(
            CarInspection,
            and_(
                CarInspection.car_id == id,
                CarInspection.car_code == Car.car_code,
                CarInspection.company_code == Car.company_code,
                CarInspection.delete_flag == Const.DEL_FLG_NORMAL,
            ),
        )

        MPref = aliased(MPrefectures)

        # Get customer information
        car = car.add_columns(Car.guide_availability_call,
                              Car.guide_availability_dm,
                              Car.guide_availability_line,
                              Car.guide_availability_email,
                              Car.guide_availability_sms,
                              Customer.face_photo,
                              Customer.last_name,
                              Customer.first_name,
                              Customer.last_name_kana,
                              Customer.first_name_kana,
                              Customer.birthday,
                              Customer.vip,
                              Customer.zip_code,
                              Customer.prefectures_code,
                              Customer.address1,
                              Customer.address2,
                              Customer.address3,
                              Customer.phone_number,
                              Customer.cellphone_number,
                              Customer.email,
                              Customer.private_business,
                              Customer.optin_times_weekdays_from9,
                              Customer.optin_times_weekdays_from12,
                              Customer.optin_times_weekdays_from18,
                              Customer.optin_times_holidays_from9,
                              Customer.optin_times_holidays_from12,
                              Customer.optin_times_holidays_from18,
                              CustomerActiveStatus.rank,
                              Customer.sex,
                              CustomerActiveStatus.active_status,
                              Customer.birthday,
                              Customer.private_business,
                              Customer.sex,
                              CustomerMarket.decade_age,
                              CustomerMarket.license_color.label('customer_market_license_color'),
                              MPref.name.label('customer_prefectures_name'),
                              ).outerjoin(
                                    Customer,
                                    and_(
                                        Car.car_decision_maker == Customer.customer_code,
                                        Customer.company_code == Car.company_code,
                                        Customer.delete_flag == Const.DEL_FLG_NORMAL,
                                    ),
                            ).outerjoin(
                                    CustomerActiveStatus,
                                    and_(
                                        CustomerActiveStatus.customer_code == Customer.customer_code,
                                        CustomerActiveStatus.company_code == Car.company_code,
                                    ),
                            ).outerjoin(
                                    CustomerMarket,
                                    and_(
                                        CustomerMarket.customer_code == Customer.customer_code,
                                        CustomerMarket.company_code == Car.company_code,
                                        CustomerMarket.delete_flag == Const.DEL_FLG_NORMAL,
                                    ),
                            ).outerjoin(
                                    MPref,
                                    and_(
                                        Customer.prefectures_code == MPref.prefectures_code,
                                    ),
                            )

        car = car.add_columns(CarLicense.license_color)\
                 .outerjoin(
                        CarLicense,
                        and_(
                            CarLicense.company_code == Car.company_code,
                            CarLicense.customer_code == Car.car_decision_maker,
                            CarLicense.delete_flag == Const.DEL_FLG_NORMAL,
                        ),
                    )

        # create subquery for get count number of contact
        sub_cnt_contact = (
            db.query(
                ChatGroup.car_id.label("car_id"),
                func.count(ChatGroup.car_id).label("contact_cnt"), )
                .filter(ChatGroup.div == BUYER_CHAT, ChatGroup.delete_flag == Const.DEL_FLG_NORMAL)
                .group_by(ChatGroup.car_id)
                .subquery("sub_cnt_contact"))

        car = car.add_columns(
            sub_cnt_contact.c.contact_cnt.label("contact_cnt")
        ).outerjoin(sub_cnt_contact, and_(Car.id == sub_cnt_contact.c.car_id))


        car = car.first()

        car_obj = jsonable_encoder(car)

        list_car_life_code = (
            db.query(CustomerCarLifeMasterLink.car_life_code)
                .filter(CustomerCarLifeMasterLink.customer_code == car_obj["car_decision_maker"],
                        CustomerCarLifeMasterLink.company_code == car_obj["company_code"],
                        CustomerCarLifeMasterLink.delete_flag == Const.DEL_FLG_NORMAL,
                        )
                .all()
        )

        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'車両ID{id}が存在しません。')

        # get car equipment details
        car_eq_detail = db.query(CarEquipmentDetails) \
            .filter(CarEquipmentDetails.car_id == id,
                    CarEquipmentDetails.delete_flag == Const.DEL_FLG_NORMAL) \
            .first()

        return car, list_car_life_code, car_eq_detail

    def get_other_info_car_by_id(
            self, db: Session, *, id: int
    ) -> Car:
        car = db.query(self.model.maker,
                       self.model.car_type,
                       self.model.grade,
                       self.model.land_transport_office,
                       self.model.car_registration_number_type,
                       self.model.car_registration_number_kana,
                       self.model.car_registration_number,
                       self.model.registration_first_date,
                       self.model.registration_start_date,
                       self.model.registration_end_date,
                       self.model.car_mileage,
                       CarDetails.aggregation_car_inspection_type,
                       CarDetails.engine_maximum_output,
                       CarDetails.car_inspection_type,
                       CarDetails.sales_period_start,
                       CarDetails.engine_torque,
                       CarDetails.fuel_tank_size,
                       CarDetails.color_trim_code_type,
                       CarDetails.color_code_type,
                       Store.store_name). \
            outerjoin(CarDetails, (Car.id == CarDetails.car_id)). \
            outerjoin(Customer, (Car.car_decision_maker == Customer.customer_code)). \
            outerjoin(Store, (Store.store_code == Customer.my_store_code)). \
            filter(Car.id == id, Car.delete_flag == 0). \
            first()
        if not car:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'車両ID{id}が存在しません。')
        return car

    # get offer info by car id
    def get_list_offer_info_by_car_id(self, db, car_id):
        list_offer_info = db.query(Offer.offer_out_store_id,
                                   Offer.offer_in_store_id,
                                   Offer.offer_status,
                                   Offer.hope_purchase_price,
                                   Offer.car_id,
                                   Offer.id.label("offer_id")). \
            filter(Offer.car_id == car_id, Offer.delete_flag == 0).all()
        return list_offer_info

    # Seach car function to filter car, recieve query param as body from endpoint cars/seach-cars
    def filter_cars(
            self,
            db: Session,
            *,
            item_in: CarQuery,
            skip: int = 0,
            limit: int = 10,
    ) -> Any:
        # Get 7 year ago
        _7years_ago = (datetime.now(tz.gettz()) + relativedelta(years=-7)).date()
        MD1 = aliased(MDivision)
        price_by_carstatus = case(
            (
                CarMarket.car_status == 0,
                CarDetails.aggregation_retail_price_market
            ),
            else_=RegisterSale.hope_sale_base_price,
        ).label("price_by_carstatus")

        # create column for order by status
        order_by_car_status = case([(CarMarket.car_status == Const.CarStatus.UNDER_EXHIBITION, 1),
                                    (CarMarket.car_status == Const.CarStatus.APPLYING, 2),
                                    (CarMarket.car_status == Const.CarStatus.UNDER_NEGOTIATION, 3),
                                    (and_(CarMarket.car_status == Const.CarStatus.HYPEN,
                                          Car.purchase_intention == TRUE), 4),
                                    (and_(CarMarket.car_status == Const.CarStatus.HYPEN,
                                          Car.car_mileage >= MILE_ALERT,
                                          Car.registration_first_date <= _7years_ago), 5),
                                    (CarMarket.car_status == Const.CarStatus.HYPEN, 6),
                                    (CarMarket.car_status == Const.CarStatus.CONTRACTED, 7),
                                    (CarMarket.car_status == Const.CarStatus.CLOSE, 8),
                                    ]).label("sort_status")

        transfer_alert = func.IF(and_(Car.car_mileage >= MILE_ALERT,
                                      Car.registration_first_date <= _7years_ago), 1, 0).label("transfer_alert")
        transfer_hope = func.IF(Car.purchase_intention == 1, 1, 0).label("transfer_hope")

        # create subquery for get count number of contact
        # base on chat_group of car_id have div = 1 and not delete
        sub_cnt_contact = (
            db.query(
                ChatGroup.car_id.label("car_id"),
                func.count(ChatGroup.car_id).label("contact_cnt"),
            )
                .filter(ChatGroup.delete_flag == Const.DEL_FLG_NORMAL)
                .group_by(ChatGroup.car_id)
                .subquery("sub_cnt_contact")
        )

        sub_chat_group = (db.query(func.sum(func.IF(ChatGroup.last_message_store_id != Const.ADMIN_ID,
                                                    ChatGroup.message_unread_cnt,
                                                    0)).label("total_unread_cnt"),
                                   func.max(ChatGroup.last_message_datetime).label("last_message_datetime"),
                                   ChatGroup.car_id.label("car_id"))
                          .filter(ChatGroup.delete_flag == Const.DEL_FLG_NORMAL)
                          .group_by(ChatGroup.car_id).subquery("sub_chat_group"))

        sub_cnt_favorite = (
            db.query(
                Favourite.car_id.label("car_id"),
                func.count(Favourite.car_id).label("favorite_cnt"),
            )
                .filter(Car.id == Favourite.car_id, Favourite.delete_flag == Const.DEL_FLG_NORMAL)
                .group_by(Favourite.car_id)
                .subquery("sub_cnt_favorite")
        )

        cars = (
            db.query(
                Car,
                Car.aggregation_image_url.label("url"),
                CarMarket.color_name,
                CarMarket.car_status,
                CarMarket.hide_flag,
                CarMarket.offer_cnt,
                CarMarket.car_active_status,
                CarMarket.prefectures_cd,
                CarMarket.store_code,
                CarMarket.insert_at.label("carmarket_insert_at"),
                CarDetails.aggregation_wholesale_price_market,
                CarDetails.aggregation_retail_price_market,
                CarMarket.view_detail_cnt,
                order_by_car_status,
                transfer_hope,
                transfer_alert,
            )
                .join(CarDetails,
                      and_(
                          CarDetails.car_id == Car.id,
                          CarDetails.delete_flag == Const.DEL_FLG_NORMAL,
                      ),
                      )
                .join(CarMarket,
                      and_(
                          CarMarket.car_id == Car.id,
                          CarMarket.delete_flag == Const.DEL_FLG_NORMAL,
                      ),
                      )
                .filter(Car.delete_flag == Const.DEL_FLG_NORMAL,
                        Car.active_flag == ACTIVE_STATUS,
                        # CarMarket.hide_flag == 0,
                        # Car.car_decision_maker.isnot(None),
                        # Car.maker.isnot(None),
                        # Car.car_type.isnot(None),
                        )
        )

        # filter cars are contacting
        if item_in.contacting == TRUE:
            cars = (cars.add_columns(
                sub_chat_group.c.total_unread_cnt.label("total_unread_cnt"),
                sub_chat_group.c.last_message_datetime.label("last_message_datetime"), )
                    .join(sub_chat_group, and_(sub_chat_group.c.car_id == Car.id)))
        else:
            cars = (cars.add_columns(sub_chat_group.c.total_unread_cnt.label("total_unread_cnt"),
                                     sub_chat_group.c.last_message_datetime.label("last_message_datetime"), )
                    .outerjoin(sub_chat_group,
                               and_(sub_chat_group.c.car_id == Car.id)))

        # join when filter
        filter_register_sale = False
        if (item_in.mode or item_in.price_to or item_in.price_from
                or item_in.new_arrival == TRUE
                or (item_in.sort_header
                    and item_in.sort_header["header"] == Const.Sort.CAR_STATUS)
                or item_in.register_sale_type):
            filter_register_sale = True
            cars = cars.add_columns(RegisterSale.id,
                                    RegisterSale.period_from,
                                    RegisterSale.period_to,
                                    RegisterSale.hope_sale_base_price_tax,
                                    RegisterSale.hope_sale_total_price_tax,
                                    RegisterSale.price_type,
                                    price_by_carstatus,
                                    RegisterSale.hope_sale_base_price,
                                    RegisterSale.register_sale_type,
                                    RegisterSale.assess_id,
                                    )
            cars = cars.outerjoin(RegisterSale,
                                  and_(
                                      RegisterSale.car_id == Car.id,
                                      RegisterSale.delete_flag == Const.DEL_FLG_NORMAL))

            # filter by PRO/C2C
            cars = cars.filter(
                and_(
                    CarMarket.car_status.in_(Const.CAR_STATUS_REGISTERED),
                    RegisterSale.register_sale_type.in_(item_in.register_sale_type)
                )
            )

        filter_customer = False
        if item_in.private_business and len(item_in.private_business) == Const.HAS_SINGLE_VALUE:
            filter_customer = True
            cars = (cars.add_columns(Customer.last_name.label("last_name"),
                                     Customer.first_name.label("first_name"),
                                     Customer.vip,
                                     Customer.customer_code,
                                     Customer.private_business,)
            .outerjoin(
                Customer,
                and_(Customer.customer_code == Car.car_decision_maker,
                     Customer.company_code == Car.company_code,
                     Customer.delete_flag == Const.DEL_FLG_NORMAL)))
            # filter by private_business
            if Const.INDIVIDUAL in item_in.private_business:
                cars = cars.filter(or_(Customer.private_business == Const.INDIVIDUAL,
                                       Customer.private_business.is_(None)))
            else:
                cars = cars.filter(Customer.private_business.in_(Const.CORPORATE))

        # filter
        if item_in.color_name:
            cars = cars.filter(CarMarket.color_name.in_(item_in.color_name))
        # car_status
        if item_in.car_status and len(item_in.car_status) > 0:
            cars = cars.filter(CarMarket.car_status.in_(item_in.car_status))
        # alert
        if item_in.transfer_alert == TRUE:
            cars = cars.filter(and_(Car.car_mileage >= MILE_ALERT,
                                    Car.registration_first_date <= _7years_ago))
        elif item_in.transfer_alert == FALSE:
            cars = cars.filter(or_(Car.car_mileage < MILE_ALERT,
                                   Car.registration_first_date > _7years_ago))
        # hope
        if item_in.transfer_hope == TRUE:
            cars = cars.filter(Car.purchase_intention == item_in.transfer_hope)
        elif item_in.transfer_hope == FALSE:
            cars = cars.filter(transfer_hope == FALSE)

        if item_in.car_mileage_from and item_in.car_mileage_from >= 0:
            cars = cars.filter(Car.car_mileage >= item_in.car_mileage_from)
        if item_in.car_mileage_to and item_in.car_mileage_to >= 0:
            cars = cars.filter(Car.car_mileage <= item_in.car_mileage_to)
        if item_in.maker:
            cars = cars.filter(Car.aggregation_maker == item_in.maker)
        if item_in.car_type:
            cars = cars.filter(Car.aggregation_car_type == item_in.car_type)
        if item_in.grade:
            cars = cars.filter(Car.aggregation_grade == item_in.grade)
        if item_in.registration_first_date_from and item_in.registration_first_date_from >= 0:
            cars = cars.filter(
                func.YEAR(Car.registration_first_date) >= item_in.registration_first_date_from)
        if item_in.registration_first_date_to and item_in.registration_first_date_to >= 0:
            cars = cars.filter(
                func.YEAR(Car.registration_first_date) <= item_in.registration_first_date_to)
        if item_in.prefectures and len(item_in.prefectures) > 0:
            cars = cars.filter(CarMarket.prefectures_cd.in_(item_in.prefectures))
        # filter by mode ( Tab Purchase, Tab Sale)
        if item_in.mode == HOPE_PRICE:
            cars = cars.filter(
                RegisterSale.hope_sale_base_price.isnot(None)
            )
        elif item_in.mode == MARKET_PRICE:
            cars = cars.filter(
                and_(
                    CarDetails.aggregation_retail_price_market.isnot(None),
                    CarMarket.car_status == STATUS_MARKET_PRICE,
                )
            )
        elif item_in.mode == ALL_PRICE:
            cars = cars.filter(
                price_by_carstatus.isnot(None)
            )

        # filter by price ( Tab Purchase, Tab Sale)
        if item_in.price_from is not None or item_in.price_to is not None:
            if item_in.price_from != NO_LIMIT_PRICE and item_in.price_to != NO_LIMIT_PRICE \
                    and item_in.price_from is not None and item_in.price_to is not None:
                if item_in.price_from <= item_in.price_to:
                    if item_in.mode == HOPE_PRICE:
                        cars = cars.filter(
                            RegisterSale.hope_sale_base_price.between(
                                item_in.price_from, item_in.price_to
                            )
                        )
                    elif item_in.mode == MARKET_PRICE:
                        cars = cars.filter(
                            and_(
                                CarDetails.aggregation_retail_price_market.between(
                                    item_in.price_from, item_in.price_to
                                ),
                                CarMarket.car_status == STATUS_MARKET_PRICE,
                            )
                        )
                    elif item_in.mode == ALL_PRICE:
                        cars = cars.filter(
                            price_by_carstatus.between(
                                item_in.price_from, item_in.price_to
                            )
                        )
            elif item_in.price_from != NO_LIMIT_PRICE and item_in.price_from is not None:
                if item_in.mode == HOPE_PRICE:
                    cars = cars.filter(
                        RegisterSale.hope_sale_base_price >= item_in.price_from
                    )
                elif item_in.mode == MARKET_PRICE:
                    cars = cars.filter(
                        and_(
                            CarDetails.aggregation_retail_price_market >= item_in.price_from,
                            CarMarket.car_status == STATUS_MARKET_PRICE,
                        )
                    )
                elif item_in.mode == ALL_PRICE:
                    cars = cars.filter(
                        price_by_carstatus >= item_in.price_from
                    )
            elif item_in.price_to != NO_LIMIT_PRICE and item_in.price_to is not None:
                if item_in.mode == HOPE_PRICE:
                    cars = cars.filter(
                        RegisterSale.hope_sale_base_price <= item_in.price_to
                    )
                elif item_in.mode == MARKET_PRICE:
                    cars = cars.filter(
                        and_(
                            CarDetails.aggregation_retail_price_market <= item_in.price_to,
                            CarMarket.car_status == STATUS_MARKET_PRICE,
                        )
                    )
                elif item_in.mode == ALL_PRICE:
                    cars = cars.filter(
                        price_by_carstatus <= item_in.price_to
                    )

        if item_in.new_contact == TRUE:
            # if chat_group have message unread that mean this car have new contact
            cars = cars.filter(sub_chat_group.c.total_unread_cnt > 0)
        if item_in.new_arrival == TRUE:
            cars = (cars.filter(or_(
                func.datediff(datetime.utcnow(), Car.insert_at) <= NEW_DURATION,
                func.datediff(datetime.utcnow(), RegisterSale.period_from) <= NEW_DURATION),
            ))

        if item_in.company_code or item_in.store_id:
            if item_in.store_id:
                cars = cars.filter(CarMarket.store_code == item_in.store_id)
            else:
                stores = crud.m_company.get_list_store(db=db, company_code=item_in.company_code)
                list_stores_id = [str(store["id"]) for store in stores]
                cars = cars.filter(CarMarket.store_code.in_(list_stores_id))

        total = -1
        if item_in.return_total == TRUE:
            total = cars.with_entities(func.count(Car.id)).scalar()

        # Sort data
        if item_in.sort_header:
            sort_header_name = item_in.sort_header.get("header").strip()
            sort_header_type = item_in.sort_header.get("type")
            if sort_header_name == "registration_first_date":
                cars = cars.order_by(
                    Car.registration_first_date.asc()
                    if sort_header_type == 1
                    else Car.registration_first_date.desc()
                )
            if sort_header_name == "car_mileage":
                cars = cars.order_by(
                    Car.car_mileage.asc()
                    if sort_header_type == 1
                    else Car.car_mileage.desc()
                )
            if sort_header_name == "registration_end_date":
                cars = cars.order_by(
                    Car.registration_end_date.asc()
                    if sort_header_type == 1
                    else Car.registration_end_date.desc()
                )
            if sort_header_name == "sort_number":
                cars = cars.order_by(
                    Car.sort_number.asc()
                    if sort_header_type == 1
                    else Car.sort_number.desc()
                )
            if sort_header_name == "car_status":
                cars = cars.order_by(
                    price_by_carstatus.asc()
                    if sort_header_type == 1
                    else price_by_carstatus.desc()
                )
            if sort_header_name == "area":
                cars = cars.order_by(
                    cast(CarMarket.prefectures_cd, DECIMAL).asc()
                    if sort_header_type == 1
                    else cast(CarMarket.prefectures_cd, DECIMAL).desc()
                )
            if sort_header_name == "color_name":
                cars = cars.order_by(
                    CarMarket.color_name.asc()
                    if sort_header_type == 1
                    else CarMarket.color_name.desc()
                )
        else:
            cars = cars.order_by(
                sub_chat_group.c.last_message_datetime.desc(),
            )

        cars = cars.offset(skip).limit(limit)
        cars = cars.from_self()
        if not filter_register_sale:
            cars = cars.add_columns(RegisterSale.id,
                                    RegisterSale.period_from,
                                    RegisterSale.period_to,
                                    RegisterSale.hope_sale_base_price_tax,
                                    RegisterSale.hope_sale_total_price_tax,
                                    RegisterSale.price_type,
                                    RegisterSale.hope_sale_base_price,
                                    price_by_carstatus,
                                    RegisterSale.register_sale_type,
                                    )
            cars = cars.outerjoin(RegisterSale,
                                  and_(RegisterSale.car_id == Car.id,
                                       RegisterSale.delete_flag == Const.DEL_FLG_NORMAL))

        if not filter_customer:
            cars = (cars.add_columns(Customer.last_name.label("last_name"),
                                     Customer.first_name.label("first_name"),
                                     Customer.vip,
                                     Customer.customer_code,
                                     Customer.private_business,
            )
            .outerjoin(
                Customer,
                and_(Customer.customer_code == Car.car_decision_maker,
                     Customer.company_code == Car.company_code,
                     Customer.delete_flag == Const.DEL_FLG_NORMAL,)))

        cars = (cars.add_columns(
                         Assess.assess_status,
                         CustomerActiveStatus.active_status,
                         CustomerActiveStatus.rank,
                         MD1.div,
                         MD1.desc.label("car_status_desc"),
                         Negotiation.negotiation_status,
                         Negotiation.period_from.label("negotiation_period_from"),
                         Negotiation.period_to.label("negotiation_period_to"),
                         Store.store_name,
                         Store.id.label("store_id"),
                         MCompany.company_name,
                         )
            .outerjoin(Assess,
                       and_(Assess.id == RegisterSale.assess_id,
                            Assess.delete_flag == Const.DEL_FLG_NORMAL, ))
            .outerjoin(MD1,
                       and_(
                            MD1.param == CarMarket.car_status,
                            MD1.div == 1,
                            MD1.delete_flag == Const.DEL_FLG_NORMAL,))
            .outerjoin(CustomerActiveStatus,
                       and_(
                            CustomerActiveStatus.customer_code == Customer.customer_code,
                            CustomerActiveStatus.customer_code == Car.car_decision_maker,
                            CustomerActiveStatus.company_code == Car.company_code,))
            .outerjoin(Negotiation,
                       and_(
                            Negotiation.car_id == Car.id,
                            Negotiation.delete_flag == Const.DEL_FLG_NORMAL,
                            Negotiation.register_sale_id == RegisterSale.id,))
            .outerjoin(Store,
                       and_(
                            Store.id == CarMarket.store_code,
                            Store.delete_flag == Const.DEL_FLG_NORMAL))
            .outerjoin(MCompany,
                       and_(
                            MCompany.company_code == Store.company_code,
                            MCompany.delete_flag == Const.DEL_FLG_NORMAL)))

        cars = (
            cars.add_columns(
                sub_cnt_contact.c.contact_cnt.label("contact_cnt"),
                sub_cnt_favorite.c.favorite_cnt.label("favorite_cnt"),
            )
            .outerjoin(sub_cnt_contact, and_(
                sub_cnt_contact.c.car_id == Car.id
            ))
            .outerjoin(sub_cnt_favorite, and_(
                sub_cnt_favorite.c.car_id == Car.id
            ))
        )

        # Sort data
        if item_in.sort_header:
            sort_header_name = item_in.sort_header.get("header").strip()
            sort_header_type = item_in.sort_header.get("type")
            if sort_header_name == "registration_first_date":
                cars = cars.order_by(
                    Car.registration_first_date.asc()
                    if sort_header_type == 1
                    else Car.registration_first_date.desc()
                )
            if sort_header_name == "car_mileage":
                cars = cars.order_by(
                    Car.car_mileage.asc()
                    if sort_header_type == 1
                    else Car.car_mileage.desc()
                )
            if sort_header_name == "registration_end_date":
                cars = cars.order_by(
                    Car.registration_end_date.asc()
                    if sort_header_type == 1
                    else Car.registration_end_date.desc()
                )
            if sort_header_name == "sort_number":
                cars = cars.order_by(
                    Car.sort_number.asc()
                    if sort_header_type == 1
                    else Car.sort_number.desc()
                )
            if sort_header_name == "car_status":
                cars = cars.order_by(
                    price_by_carstatus.asc()
                    if sort_header_type == 1
                    else price_by_carstatus.desc()
                )
            if sort_header_name == "area":
                cars = cars.order_by(
                    cast(CarMarket.prefectures_cd, DECIMAL).asc()
                    if sort_header_type == 1
                    else cast(CarMarket.prefectures_cd, DECIMAL).desc()
                )
            if sort_header_name == "color_name":
                cars = cars.order_by(
                    CarMarket.color_name.asc()
                    if sort_header_type == 1
                    else CarMarket.color_name.desc()
                )
        else:
            cars = cars.order_by(
                sub_chat_group.c.last_message_datetime.desc(),
            )

        # print(cars.statement.compile(compile_kwargs={"literal_binds": True}))
        cars = cars.all()

        return cars, total


    # get all image by car id
    def get_car_photos_by_id(self, db: Session, *, id: int) -> Any:

        # Get car photo url
        car_photo_thumbnail = (
            db.query(CarPhoto.url)
                .filter(
                CarPhoto.car_id == id,
                CarPhoto.delete_flag == Const.DEL_FLG_NORMAL,
                CarPhoto.image_div == CAR_PHOTO.get("CAR_PHOTO_THUMBNAIL"),
            )
                .first()
        )
        list_image_car = (
            db.query(
                S3File.bucket_name,
                S3File.key,
                case(
                    [
                        (CarDetails.front_exterior_image == CarPhoto.id, 1),
                        (CarDetails.side_exterior_image == CarPhoto.id, 2),
                        (CarDetails.back_exterior_image == CarPhoto.id, 3),
                        (CarDetails.optional_exterior_image == CarPhoto.id, 4),
                        (CarDetails.repair_exterior_image == CarPhoto.id, 5),
                        (CarDetails.front_interior_image == CarPhoto.id, 6),
                        (CarDetails.seat_interior_image == CarPhoto.id, 7),
                        (CarDetails.meter_interior_image == CarPhoto.id, 8),
                        (CarDetails.option_interior_image == CarPhoto.id, 9),
                        (CarDetails.repair_interior_image == CarPhoto.id, 10),
                    ]
                ).label("image_value"),
            )
                .join(
                    CarDetails,
                    and_(CarDetails.car_id == id,
                         CarDetails.delete_flag == Const.DEL_FLG_NORMAL))
                .join(
                    CarPhoto,
                    and_(
                        or_(
                            CarDetails.front_exterior_image == CarPhoto.id,
                            CarDetails.side_exterior_image == CarPhoto.id,
                            CarDetails.back_exterior_image == CarPhoto.id,
                            CarDetails.optional_exterior_image == CarPhoto.id,
                            CarDetails.repair_exterior_image == CarPhoto.id,
                            CarDetails.front_interior_image == CarPhoto.id,
                            CarDetails.seat_interior_image == CarPhoto.id,
                            CarDetails.meter_interior_image == CarPhoto.id,
                            CarDetails.option_interior_image == CarPhoto.id,
                            CarDetails.repair_interior_image == CarPhoto.id,
                        ),
                        S3File.id == CarPhoto.s3_file_id,
                        CarPhoto.delete_flag == Const.DEL_FLG_NORMAL,
                        S3File.delete_flag == Const.DEL_FLG_NORMAL,
                    ),
            )
                .all()
        )

        return car_photo_thumbnail, list_image_car

car = CRUDCar(Car)
