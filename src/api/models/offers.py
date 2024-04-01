from __future__ import annotations
from typing import Any, Optional
from enum import Enum
from uuid import UUID
from pydantic_core import PydanticCustomError
from pydantic import model_validator, BaseModel, NonNegativeInt, NonNegativeFloat
from .users import Author
from .base import Location


class OfferType(Enum):
    HOUSE = 'house'
    FLAT = 'flat'
    OFFICE = 'office'

class BaseOffer(BaseModel):
    uuid: UUID
    offer_type: str
    price: NonNegativeInt
    name: str
    location: Location


class ShortOffer(BaseOffer):
    photo: UUID


class Offer(BaseOffer):
    author: Author
    area: NonNegativeFloat
    description: str
    floor: NonNegativeInt
    tags: Optional[dict]
    photos: list[UUID]  # UUID of photos


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

    @model_validator(mode='before')
    @classmethod
    def _validate(cls, value: Any) -> SearchValidate:
        if not value:
            raise PydanticCustomError(
                'search_validate_error',
                'All values cannot be None! Use /offers/all to get all offers',
            )
        return value
