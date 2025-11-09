from pydantic import BaseModel
from typing import Optional


class CarBase(BaseModel):
    brand: str
    model: str
    year: int
    body_type: str
    engine_type: str
    engine_size_liters: float
    horsepower: int
    transmission: str
    fuel_type: str
    mileage_km: int
    top_speed_kmh: int
    color: str
    features: str
    price_usd: float
    discount_percent: float
    num_in_stock: int
    description: str


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    body_type: Optional[str] = None
    engine_type: Optional[str] = None
    engine_size_liters: Optional[float] = None
    horsepower: Optional[int] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    mileage_km: Optional[int] = None
    top_speed_kmh: Optional[int] = None
    color: Optional[str] = None
    features: Optional[str] = None
    price_usd: Optional[float] = None
    discount_percent: Optional[float] = None
    num_in_stock: Optional[int] = None
    description: Optional[str] = None


class Car(CarBase):
    id: int

    class Config:
        from_attributes = True
