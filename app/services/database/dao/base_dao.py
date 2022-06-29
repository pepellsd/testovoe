from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, db: AsyncSession):
        self.db = db
