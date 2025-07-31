from datetime import datetime

from typing import Optional

import enum

from sqlalchemy import ForeignKey, String, Integer, Float, Boolean, Enum, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .core import Base


class PriorityStatus(str, enum.Enum):
    LOW = "low"
    AVERAGE = "average"
    HIGH = "high"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


class CheckIn(Base):
    __tablename__ = "check_in"
    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)

    check_in_name: Mapped[str] = mapped_column(String(20), nullable=False)
    dict_with_dates: Mapped[str] = mapped_column(String(), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class FinanceGroup(Base):
    __tablename__ = "finances_group"

    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)
    source_name: Mapped[str] = mapped_column(String(60), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class Finance(Base):
    __tablename__ = "finances"

    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(60), nullable=True)
    amount: Mapped[int] = mapped_column(Integer(), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    added_at: Mapped[datetime] = mapped_column(nullable=True)

    finance_id: Mapped[int] = mapped_column(ForeignKey('finances_group.id'), nullable=False)


class CurrencyExchangeRate(Base):
    __tablename__ = "currency_exchange_rates"

    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)

    USD_in: Mapped[float] = mapped_column(Float(), nullable=False)
    USD_out: Mapped[float] = mapped_column(Float(), nullable=False)
    EUR_in: Mapped[float] = mapped_column(Float(), nullable=False)
    EUR_out: Mapped[float] = mapped_column(Float(), nullable=False)
    USD_RUB_in: Mapped[float] = mapped_column(Float(), nullable=False)
    USD_RUB_out: Mapped[float] = mapped_column(Float(), nullable=False)
    RUB_EUR_in: Mapped[float] = mapped_column(Float(), nullable=False)
    RUB_EUR_out: Mapped[float] = mapped_column(Float(), nullable=False)
    RUB_in: Mapped[float] = mapped_column(Float(), nullable=False)
    RUB_out: Mapped[float] = mapped_column(Float(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow())



class House(Base):
    __tablename__ = "house"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    task_name: Mapped[str] = mapped_column(String(100), nullable=False)
    frequency: Mapped[str] = mapped_column(String(100), nullable=False)  # можно enum
    repeat: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    interval_days: Mapped[int] = mapped_column(Integer(), nullable=True)  # если repeat = True
    weekdays: Mapped[list[str]] = mapped_column(JSON(), nullable=True)  # ['monday', 'wednesday']
    next_run_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    mileage: Mapped[int] = mapped_column(Integer(), nullable=False)
    price: Mapped[int] = mapped_column(Integer(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class Debts(Base):
    __tablename__ = "debts"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(String(50), nullable=False)
    paid: Mapped[int] = mapped_column(Integer(), default=0, nullable=False)
    priority: Mapped[PriorityStatus] = mapped_column(Enum(PriorityStatus), default=PriorityStatus.LOW, nullable=False)
    due_date: Mapped[datetime] = mapped_column(String(50), default='', nullable=False)
    is_closed: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
    notes: Mapped[str] = mapped_column(String(300), default='', nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)



__all__ = ["User", "CheckIn", "FinanceGroup", "Finance", "CurrencyExchangeRate",
           "House", "Car", "Debts",
           "PriorityStatus"
           ]