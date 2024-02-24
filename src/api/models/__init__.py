from typing import Optional
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, PositiveInt, NonNegativeInt, EmailStr
from pydantic_extra_types.coordinate import Coordinate


class OfferType(Enum):
    HOUSE = 'house'
    FLAT = 'flat'
    OFFICE = 'office'


class Location(BaseModel):
    text: str
    coordinate: Coordinate


class Offer(BaseModel):
    uuid: UUID
    author_id: int
    offer_type: str
    area: float
    name: str
    description: str
    location: Location
    price: PositiveInt
    floor: NonNegativeInt
    photos: list[UUID]  # UUID of photos
    tags: Optional[dict]


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


class ValueSinceToValidate(BaseModel):
    value: Optional[int] = None
    since: Optional[int] = None
    to: Optional[int] = None


class SearchValidate(BaseModel):
    offer_type: Optional[OfferType] = None
    uuid: Optional[UUID] = None
    author_id: Optional[int] = None
    price: Optional[ValueSinceToValidate] = None
    area: Optional[ValueSinceToValidate] = None
    # location: Optional[Location]
