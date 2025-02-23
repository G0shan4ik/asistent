from datetime import datetime

from typing import Optional

from sqlalchemy import ForeignKey, String, Integer, Float, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .core import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)

    note_name: Mapped[str] = mapped_column(String(60), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    image: Mapped[str] = mapped_column(String(560), nullable=True)
    copy_teg: Mapped[bool] = mapped_column(Boolean(), default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


class Finance(Base):
    __tablename__ = "finances"

    id: Mapped[int] = mapped_column(Integer(), autoincrement=True, primary_key=True)
    source_name: Mapped[str] = mapped_column(String(60), nullable=True)
    amount: Mapped[int] = mapped_column(Integer(), nullable=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    added_at: Mapped[datetime] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)


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

