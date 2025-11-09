from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from ..helpers.db_conf import ORM_BASE
from .OrderItemModel import order_items


class Order(ORM_BASE):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="orders")
    cars = relationship("Car", secondary=order_items, back_populates="orders")
