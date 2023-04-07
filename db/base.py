# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.item import Item  # noqa
from app.models.cars_authority import CarsAuthority # noqa
from app.models.cars_role import CarsRole # noqa
from app.models.cars_api import CarsApi # noqa

from app.models.car import Car # noqa
from app.models.car_details import CarDetails
from app.models.offer import Offer
from app.models.register_sale import RegisterSale
from app.models.purchase import Purchase
from app.models.car_market import CarMarket