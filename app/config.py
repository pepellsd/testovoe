from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URI: PostgresDsn = 'postgresql+asyncpg://some_client:123@localhost/some'
    SECRET_KEY: str = 'fd8d38cde9a2c28977244b386772b418babfa0ca9c3d3106606b3e9146417f80'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_DAYS: int = 1


@lru_cache()
def get_settings():
    return Settings()
