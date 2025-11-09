from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import DECIMAL
from ..helpers.db_conf import ORM_BASE
from .OrderItemModel import order_items


class Car(ORM_BASE):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    body_type = Column(String, nullable=False)
    engine_type = Column(String, nullable=False)
    engine_size_liters = Column(Float, nullable=False)
    horsepower = Column(Integer, nullable=False)
    transmission = Column(String, nullable=False)
    fuel_type = Column(String, nullable=False)
    mileage_km = Column(Integer, nullable=False)
    top_speed_kmh = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    features = Column(Text, nullable=False)
    price_usd = Column(DECIMAL(10, 2), nullable=False)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)
    num_in_stock = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

    orders = relationship("Order", secondary=order_items, back_populates="cars")
