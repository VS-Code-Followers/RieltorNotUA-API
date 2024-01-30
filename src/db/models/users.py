from .core import Base
from uuid import UUID as ID
from sqlalchemy import BigInteger, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY, JSON


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location: Mapped[dict] = mapped_column(JSON)
    offers: Mapped[list[ID]] = mapped_column(
        ARRAY(UUID), primary_key=True, server_default=[]
    )
    active_offers: Mapped[int] = mapped_column(Integer, server_default=0)
