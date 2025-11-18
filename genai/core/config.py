from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    GEMINI_API_KEY: str
    CHROMADB_PATH: str
    CARS_COLLECTION: str
    EMBEDDING_SIZE: int

    class Config:
        env_file = r"ai\.env"


@lru_cache
def get_settings():
    return Settings()
