from .core import Base
from uuid import UUID as ID
from sqlalchemy import UUID, Integer, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import ARRAY, JSON


class Offers(Base):
    __tablename__ = "offers"
    uuid: Mapped[ID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(100))
    location: Mapped[dict] = mapped_column(JSON)
    price: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    photos: Mapped[list[ID]] = mapped_column(ARRAY(UUID), primary_key=True)
