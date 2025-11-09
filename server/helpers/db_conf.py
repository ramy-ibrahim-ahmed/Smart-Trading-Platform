from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

SETTINGS = get_settings()
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD}@{SETTINGS.POSTGRES_USER}:5432/{SETTINGS.POSTGRES_DB}"
ENGINE = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=ENGINE, class_=AsyncSession, expire_on_commit=False
)

ORM_BASE = declarative_base()


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
