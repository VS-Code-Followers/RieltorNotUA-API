from sqlalchemy.orm import DeclarativeBase
from uuid import UUID as ID
from sqlalchemy import UUID, Integer, VARCHAR, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import ARRAY, JSON


class Base(DeclarativeBase):
    pass


class Offers(Base):
    __tablename__ = "offers"
    uuid: Mapped[ID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100))
    location: Mapped[dict] = mapped_column(JSON)
    price: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    photos: Mapped[list[ID]] = mapped_column(ARRAY(UUID), primary_key=True)


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location: Mapped[dict] = mapped_column(JSON)
    offers: Mapped[list[ID]] = mapped_column(ARRAY(UUID), primary_key=True)
    active_offers: Mapped[int] = mapped_column(Integer, default=0)
