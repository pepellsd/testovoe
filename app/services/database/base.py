from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Callable, Type
from fastapi import Depends

from app.services.database.dao.base_dao import BaseDAO
from app.config import get_settings


settings = get_settings()

engine = create_async_engine(settings.DATABASE_URI, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False)
Base = declarative_base()


async def get_session() -> Callable[[], AsyncSession]:
    async with async_session() as session:
        yield session


async def get_session_stub():
    raise NotImplementedError


def get_dao(Dao_type: Type[BaseDAO]) -> Callable:
    def _get_dao(db: AsyncSession = Depends(get_session)) -> BaseDAO:
        return Dao_type(db)
    return _get_dao
