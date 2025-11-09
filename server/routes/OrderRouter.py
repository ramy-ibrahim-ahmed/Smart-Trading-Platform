from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..helpers.db_conf import get_session
from ..schemas.OrderSchema import Order, OrderCreate, OrderUpdate
from ..services.OrderService import *
from ..models import UserModel
from ..helpers.security import get_current_active_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_new_order(
    order: OrderCreate,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    return await create_order(session, current_user.id, order)


@router.get("/", response_model=List[Order])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    return await get_orders(session, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{order_id}", response_model=Order)
async def read_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    order = await get_order(session, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this order",
        )
    return order


@router.put("/{order_id}", response_model=Order)
async def update_existing_order(
    order_id: int,
    order: OrderUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    existing_order = await get_order(session, order_id)
    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if existing_order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this order",
        )
    updated_order = await update_order(session, order_id, order)
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    existing_order = await get_order(session, order_id)
    if not existing_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    if existing_order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this order",
        )
    await delete_order(session, order_id)
