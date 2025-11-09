from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import OrderModel, CarModel
from ..schemas.OrderSchema import OrderCreate, OrderUpdate, Order


async def create_order(
    session: AsyncSession, user_id: int, order: OrderCreate
) -> Order:
    db_order = OrderModel(user_id=user_id)
    session.add(db_order)
    await session.flush()

    result = await session.execute(
        select(CarModel).where(CarModel.id.in_(order.car_ids))
    )
    cars = result.scalars().all()
    db_order.cars = cars

    await session.commit()
    await session.refresh(db_order)
    return Order.model_validate(db_order)


async def get_orders(
    session: AsyncSession, user_id: int = None, skip: int = 0, limit: int = 100
) -> List[Order]:
    query = select(OrderModel)
    if user_id is not None:
        query = query.where(OrderModel.user_id == user_id)
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return [Order.model_validate(order) for order in result.scalars().all()]


async def get_order(session: AsyncSession, order_id: int) -> Optional[Order]:
    result = await session.execute(select(OrderModel).where(OrderModel.id == order_id))
    db_order = result.scalar_one_or_none()
    if db_order:
        return Order.model_validate(db_order)
    return None


async def update_order(
    session: AsyncSession, order_id: int, order_update: OrderUpdate
) -> Optional[Order]:
    result = await session.execute(select(OrderModel).where(OrderModel.id == order_id))
    db_order = result.scalar_one_or_none()
    if not db_order:
        return None
    if order_update.car_ids is not None:
        result = await session.execute(
            select(CarModel).where(CarModel.id.in_(order_update.car_ids))
        )
        cars = result.scalars().all()
        db_order.cars = cars
    await session.commit()
    await session.refresh(db_order)
    return Order.model_validate(db_order)


async def delete_order(session: AsyncSession, order_id: int) -> bool:
    result = await session.execute(select(OrderModel).where(OrderModel.id == order_id))
    db_order = result.scalar_one_or_none()
    if not db_order:
        return False
    await session.delete(db_order)
    await session.commit()
    return True
