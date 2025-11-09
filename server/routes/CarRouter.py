from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..helpers.db_conf import get_session
from ..schemas.CarSchema import Car, CarCreate, CarUpdate
from ..services.CarService import create_car, get_cars, get_car, update_car, delete_car

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("/", response_model=Car, status_code=status.HTTP_201_CREATED)
async def create_new_car(
    car: CarCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_car(session, car)


@router.get("/", response_model=List[Car])
async def read_cars(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    return await get_cars(session, skip, limit)


@router.get("/{car_id}", response_model=Car)
async def read_car(car_id: int, session: AsyncSession = Depends(get_session)):
    car = await get_car(session, car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
    return car


@router.put("/{car_id}", response_model=Car)
async def update_existing_car(
    car_id: int,
    car: CarUpdate,
    session: AsyncSession = Depends(get_session),
):
    updated_car = await update_car(session, car_id, car)
    if not updated_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
    return updated_car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_car(
    car_id: int,
    session: AsyncSession = Depends(get_session),
):
    deleted = await delete_car(session, car_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )
