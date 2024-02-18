from typing import Optional
from uuid import UUID
from pydantic import BaseModel, PositiveInt, NonNegativeInt, EmailStr
from pydantic_extra_types.coordinate import Coordinate
from .enums import OfferType


class Location(BaseModel):
    text: str
    coordinate: Coordinate


class Offer(BaseModel):
    uuid: UUID
    author_id: int
    name: str
    location: Location
    price: PositiveInt
    floor: NonNegativeInt
    photos: list[UUID]  # UUID of photos


class OfferHouse(Offer):
    type: OfferType = OfferType.HOUSE


class OfferFlat(Offer):
    type: OfferType = OfferType.FLAT
    rooms_num: PositiveInt
    has_balcony: bool


class OfferOffice(Offer):
    type: OfferType = OfferType.OFFICE
    has_secure: bool


class Auth(BaseModel):
    email: EmailStr
    password: str


class Realtor(BaseModel):
    id: PositiveInt
    # auth: Auth
    location: Location
    offers: list[Optional[Offer]]
    active_offers: NonNegativeInt


class Seller(BaseModel):
    id: PositiveInt
    # auth: Auth
    location: Optional[Location]
