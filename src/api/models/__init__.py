from typing import Optional
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, NonNegativeInt, NonNegativeFloat
from pydantic_extra_types.coordinate import Coordinate


class OfferType(Enum):
    HOUSE = 'house'
    FLAT = 'flat'
    OFFICE = 'office'


class Location(BaseModel):
    text: str
    coordinate: Coordinate


class Author(BaseModel):
    account_id: int
    name: str


class ShortOffer(BaseModel):
    uuid: UUID
    offer_type: str
    price: NonNegativeInt
    name: str
    location: Location
    photos: list[UUID]  # UUID of photos


class Offer(ShortOffer):
    author: Author
    area: NonNegativeFloat
    description: str
    floor: NonNegativeInt
    tags: Optional[dict]


class ValueSinceToValidate(BaseModel):
    value: Optional[NonNegativeInt] = None
    since: Optional[NonNegativeInt] = None
    to: Optional[NonNegativeInt] = None


class SearchValidate(BaseModel):
    offer_type: Optional[OfferType] = None
    uuid: Optional[UUID] = None
    author_id: Optional[int] = None
    author_name: Optional[str] = None
    price: Optional[ValueSinceToValidate] = None
    area: Optional[ValueSinceToValidate] = None
    # location: Optional[Location]
