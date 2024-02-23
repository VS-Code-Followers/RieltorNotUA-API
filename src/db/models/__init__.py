from sqlalchemy.orm import DeclarativeBase
from uuid import UUID as ID
from typing import Optional
from sqlalchemy import UUID, Integer, VARCHAR, BigInteger, Float
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import ARRAY, JSON


class Base(DeclarativeBase):
    pass


class Offers(Base):
    __tablename__ = "offers"
    uuid: Mapped[ID] = mapped_column(UUID, primary_key=True)
    author_id: Mapped[int] = mapped_column(BigInteger)
    offer_type: Mapped[str] = mapped_column(VARCHAR(20))
    area: Mapped[float] = mapped_column(Float())
    name: Mapped[str] = mapped_column(VARCHAR(100))
    description: Mapped[str] = mapped_column(VARCHAR(500))
    location: Mapped[dict] = mapped_column(JSON)
    price: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    photos: Mapped[list[ID]] = mapped_column(ARRAY(UUID), primary_key=True)
    tags: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location: Mapped[dict] = mapped_column(JSON)
    offers: Mapped[list[ID]] = mapped_column(ARRAY(UUID), primary_key=True)
    active_offers: Mapped[int] = mapped_column(Integer, default=0)
