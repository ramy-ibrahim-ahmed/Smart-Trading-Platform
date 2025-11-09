from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schemas.CarSchema import CarCreate, CarUpdate, Car
from ..models import CarModel


async def create_car(session: AsyncSession, car: CarCreate) -> Car:
    db_car = CarModel(**car.model_dump())
    session.add(db_car)
    await session.commit()
    await session.refresh(db_car)
    return Car.model_validate(db_car)


async def get_cars(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Car]:
    result = await session.execute(select(CarModel).offset(skip).limit(limit))
    return [Car.model_validate(car) for car in result.scalars().all()]


async def get_car(session: AsyncSession, car_id: int) -> Optional[Car]:
    result = await session.execute(select(CarModel).where(CarModel.id == car_id))
    db_car = result.scalar_one_or_none()
    if db_car:
        return Car.model_validate(db_car)
    return None


async def update_car(
    session: AsyncSession, car_id: int, car_update: CarUpdate
) -> Optional[Car]:
    result = await session.execute(select(CarModel).where(CarModel.id == car_id))
    db_car = result.scalar_one_or_none()
    if not db_car:
        return None
    update_data = car_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_car, key, value)
    await session.commit()
    await session.refresh(db_car)
    return Car.model_validate(db_car)


async def delete_car(session: AsyncSession, car_id: int) -> bool:
    result = await session.execute(select(CarModel).where(CarModel.id == car_id))
    db_car = result.scalar_one_or_none()
    if not db_car:
        return False
    await session.delete(db_car)
    await session.commit()
    return True
