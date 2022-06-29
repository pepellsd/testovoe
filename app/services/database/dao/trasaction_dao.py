from typing import Literal

from app.services.database.models import TransactionHistory, OperationStatus
from app.services.database.dao.base_dao import BaseDAO


class TransactionDAO(BaseDAO):
    async def create_transaction(self, user_id: int, amount: int, operation: Literal['+', '-'], is_declined: bool):
        operation = OperationStatus.refill if operation == '+' else OperationStatus.withdrawal
        transaction = TransactionHistory(user_id=user_id, amount=amount, status=operation, is_declined=is_declined)
        self.db.add(transaction)
        await self.db.commit()