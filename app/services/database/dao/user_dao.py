from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import noload
from typing import Union, Literal

from app.services.database.models import User
from app.services.database.dao.base_dao import BaseDAO


class NegativeBalanceEXC(Exception):
    pass


class UserDAO(BaseDAO):
    async def get_user(self, user_id: int) -> Union[User, None]:
        try:
            stmt = select(User).options(noload(User.transactions_history)).where(User.id == user_id)
            result = await self.db.execute(stmt)
            return result.scalar()
        except NoResultFound:
            return None

    async def create_user(self, name: str, password: str, username: str) -> Union[User, None]:
        try:
            user = User(name=name, password_hash=password, username=username, balance=0)
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError:
            return None

    async def update_user_balance(self, user_id: int, operation: Literal['+', '-'], amount: int):
        try:
            await self.db.execute(
                update(
                    User
                ).where(
                    User.id == user_id
                ).values(
                    {User.balance: User.balance + amount if operation == '+' else User.balance - amount}
                ))
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise NegativeBalanceEXC

    async def authenticate_user(self, user_password: str, username: str):
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        db_user = result.scalar()
        if db_user is None:
            return False
        if db_user.password_hash != user_password:
            return False
        return db_user
