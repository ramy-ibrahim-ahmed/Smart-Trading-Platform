from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .CarSchema import Car


class OrderBase(BaseModel):
    pass


class OrderCreate(BaseModel):
    car_ids: List[int]


class OrderUpdate(BaseModel):
    car_ids: Optional[List[int]] = None


class Order(OrderBase):
    id: int
    created_at: datetime
    user_id: int
    cars: List[Car]

    class Config:
        from_attributes = True
