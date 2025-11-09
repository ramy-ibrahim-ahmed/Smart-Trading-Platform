from sqlalchemy import Integer, Table, ForeignKey, Column
from ..helpers.db_conf import ORM_BASE

order_items = Table(
    "order_items",
    ORM_BASE.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("car_id", Integer, ForeignKey("cars.id"), primary_key=True),
)
