from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import UserModel
from ..schemas.UserSchema import UserCreate, UserUpdate, User
from ..helpers.security import hash_password, verify_password


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = UserModel(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return User.model_validate(db_user)


async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        return User.model_validate(db_user)
    return None


async def get_user_by_username(
    session: AsyncSession, username: str
) -> Optional[UserModel]:
    result = await session.execute(
        select(UserModel).where(UserModel.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[UserModel]:
    result = await session.execute(select(UserModel).where(UserModel.email == email))
    return result.scalar_one_or_none()


async def update_user(
    session: AsyncSession, user_id: int, user_update: UserUpdate
) -> Optional[User]:
    result = await session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(db_user, key, value)
    await session.commit()
    await session.refresh(db_user)
    return User.model_validate(db_user)


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    result = await session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()
    if not db_user:
        return False
    await session.delete(db_user)
    await session.commit()
    return True


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> Optional[UserModel]:
    db_user = await get_user_by_username(session, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
