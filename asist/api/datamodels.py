import enum
from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

from asist.database.models import User, CurrencyExchangeRate, Finance, CheckIn, House, Debts, Car


class CreatedModel(BaseModel):
    created_id: int


# User models
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
# /User models


# Currency models
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
# /Currency models


# CheckIn models
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
# /CheckIn models


# Finance models
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
# /Finance models


# House models
class HouseCreate(BaseModel):
    task_name: str
    frequency: str
    repeat: bool
    interval_days: Optional[int] = None
    weekdays: Optional[list] = None
    next_run_at: Optional[datetime] = None
    is_active: bool = True

    user_id: int

class HouseResponse(BaseModel):
    id: int
    task_name: str
    frequency: str
    repeat: bool
    interval_days: Optional[int]
    weekdays: Optional[list]
    next_run_at: Optional[datetime]
    is_active: bool
    created_at: str

    user_id: int

    @classmethod
    def from_orm(cls, house: House):
        return cls(
            id=house.id,
            task_name=house.task_name,
            frequency=house.frequency,
            repeat=house.repeat,
            interval_days=house.interval_days,
            weekdays=house.weekdays,
            next_run_at=house.next_run_at,
            is_active=house.is_active,
            created_at=house.created_at.isoformat(),
            user_id=house.user_id
        )
# /House models


# Debts models
class PriorityStatus(str, enum.Enum):
    LOW = "low"
    AVERAGE = "average"
    HIGH = "high"

class DebtsCreate(BaseModel):
    title: str
    amount: str
    paid: Optional[int] = None
    priority: Optional[PriorityStatus] = PriorityStatus.LOW
    due_date: Optional[str] = ''
    is_closed: Optional[bool] = False
    notes: Optional[str] = ''
    created_at: Optional[datetime] = None

    user_id: int

class DebtsUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[str] = None
    paid: Optional[int] = None
    priority: Optional[PriorityStatus] = None
    due_date: Optional[str] = 'None'
    notes: Optional[str] = None

class DebtsResponse(DebtsCreate):
    id: int
    paid: int
    priority: PriorityStatus
    due_date: str
    is_closed: bool
    notes: str
    created_at: str

    @classmethod
    def from_orm(cls, debts: Debts):
        return cls(
            id=debts.id,
            title=debts.title,
            amount=debts.amount,
            paid=debts.paid,
            priority=debts.priority,
            due_date=debts.due_date,
            is_closed=debts.is_closed,
            notes=debts.notes,
            created_at=debts.created_at.isoformat(),
            user_id=debts.user_id
        )
# /Debts models


# Car models
# /Car modelsds