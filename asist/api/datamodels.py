from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from asist.database.models import User, CurrencyExchangeRate, Finance, CheckIn


class CreatedModel(BaseModel):
    created_id: int


class UserCreate(BaseModel):
    id: int
    username: str
    password: Optional[str] = None
    created_at: Optional[datetime] = None

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: str
    password: Optional[str] = None

    @classmethod
    def from_orm(cls, user: User):
        return cls(
            id=user.id,
            username=user.username,
            created_at=user.created_at.isoformat(),
            password=user.password
        )

class UserUpdatePassword(BaseModel):
    id: int
    password: str

class PasswordStatus(str, Enum):
    CREATE = "create"
    UPDATE = "update"


class CurrencyCreated(BaseModel):
    USD_in: float
    USD_out: float
    EUR_in: float
    EUR_out: float
    USD_RUB_in: float
    USD_RUB_out: float
    RUB_EUR_in: float
    RUB_EUR_out: float
    RUB_in: float
    RUB_out: float

    updated_at: Optional[datetime] = datetime.utcnow()

    @classmethod
    def from_orm(cls, curr: CurrencyExchangeRate):
        return cls(
            USD_in=curr.USD_in,
            USD_out=curr.USD_out,
            EUR_in=curr.EUR_in,
            EUR_out=curr.EUR_out,
            USD_RUB_in=curr.USD_RUB_in,
            USD_RUB_out=curr.USD_RUB_out,
            RUB_EUR_in=curr.RUB_EUR_in,
            RUB_EUR_out=curr.RUB_EUR_out,
            RUB_in=curr.RUB_in,
            RUB_out=curr.RUB_out,
            updated_at=curr.updated_at
        )


class CreateCheckIn(BaseModel):
    check_in_name: str

    user_id: int

class UpdateCheckIn(BaseModel):
    check_in_name: Optional[str] = None
    dict_with_dates: Optional[str] = None

class CheckInResponse(BaseModel):
    id: int
    check_in_name: str
    dict_with_dates: Optional[str] = None

    user_id: int

    @classmethod
    def from_orm(cls, check_in: CheckIn):
        return cls(
            id=check_in.id,
            check_in_name=check_in.check_in_name,
            dict_with_dates=check_in.dict_with_dates,
        )


class CreateFinance(BaseModel):
    source_name: str
    amount: Optional[int] = None
    description: Optional[str] = None
    added_at: Optional[datetime] = None

    user_id: int

class UpdateFinance(BaseModel):
    source_name: Optional[str] = None
    amount: Optional[int] = None
    description: Optional[str] = None
    added_at: Optional[datetime] = None

class FinanceResponse(BaseModel):
    id: int
    source_name: str
    amount: Optional[int]
    description: Optional[str]
    added_at: Optional[datetime]

    user_id: int

    @classmethod
    def from_orm(cls, finance: Finance):
        return cls(
            id=finance.id,
            title=finance.title,
            amount=finance.amount,
            description=finance.description,
            added_at=finance.added_at,
            finance_id=finance.finance_id
        )