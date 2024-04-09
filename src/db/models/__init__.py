from sqlalchemy.orm import DeclarativeBase
from uuid import UUID as ID
from typing import Optional
from sqlalchemy import UUID, Integer, VARCHAR, Text, BigInteger, Float
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import ARRAY, JSON


class Base(DeclarativeBase):
    """Base sqlalchemy class from declaring other tables"""

    pass


class Offers(Base):
    """View as a offers table class"""

    __tablename__ = 'offers'
    uuid: Mapped[ID] = mapped_column(UUID, primary_key=True)
    author: Mapped[dict] = mapped_column(JSON)
    offer_type: Mapped[str] = mapped_column(VARCHAR(20))
    area: Mapped[float] = mapped_column(Float())
    name: Mapped[str] = mapped_column(VARCHAR(100))
    description: Mapped[str] = mapped_column(VARCHAR(500))
    location: Mapped[dict] = mapped_column(JSON)
    price: Mapped[int] = mapped_column(BigInteger)
    floor: Mapped[int] = mapped_column(Integer)
    photos: Mapped[list[ID]] = mapped_column(ARRAY(UUID), unique=True)
    tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class Users(Base):
    """View as a users table class"""

    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(VARCHAR(50), unique=True)
    password: Mapped[str] = mapped_column(Text, unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(VARCHAR(100))
    account_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    location: Mapped[dict] = mapped_column(JSON, nullable=True)
    offers: Mapped[list[ID]] = mapped_column(ARRAY(UUID), nullable=True)
    # active_offers: Mapped[int] = mapped_column(Integer, default=0)
