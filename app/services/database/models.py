import pytz
import enum
from datetime import datetime

from sqlalchemy import String, BigInteger, DateTime, Integer, Enum, Boolean, Numeric
from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import PasswordType

from app.services.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(PasswordType(max_length=128, schemes=['bcrypt']))
    name = Column(String)
    transactions_history = relationship('TransactionHistory', cascade='all,delete', passive_deletes=True)
    balance = Column(Numeric(20, 2))

    __table_args__ = (CheckConstraint(balance >= 0, name='check_balance_positive'),)

    def __str__(self):
        return self.name


class OperationStatus(enum.Enum):
    refill = 'пополнение'
    withdrawal = 'вывод'


class TransactionHistory(Base):
    __tablename__ = "transactions_history"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    time_stamp = Column(DateTime, default=datetime.utcnow())
    amount = Column(Integer)
    is_declined = Column(Boolean)
    status = Column(Enum(OperationStatus, name='operation_status'))

    def __str__(self):
        return f"{self.user_id} тип:{self.status} сумма:{self.amount}"
