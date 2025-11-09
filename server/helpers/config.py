from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SALT_ROUNDS: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
