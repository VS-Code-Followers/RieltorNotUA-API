from __future__ import annotations
from typing import Any, Optional
from enum import Enum
from uuid import UUID
from pydantic_core import PydanticCustomError
from pydantic import model_validator, BaseModel, NonNegativeInt, NonNegativeFloat
from .users import Author
from .base import Location, Coordinate


class OfferType(Enum):
    """
    OfferType Enum
    attrs:
        HOUSE = 'house'
        FLAT = 'flat'
        OFFICE = 'office'
    """

    HOUSE = 'house'
    FLAT = 'flat'
    OFFICE = 'office'


class BaseOffer(BaseModel):
    """
    BaseOffer pydantic model
    attrs:
        uuid: UUID
        offer_type: str
        price: NonNegativeInt
        name: str
        location: Location
    """

    uuid: UUID
    offer_type: str
    price: NonNegativeInt
    name: str
    location: Location


class ShortOffer(BaseOffer):
    """
    ShortOffer pydantic model
    attrs:
        uuid: UUID
        offer_type: str
        price: NonNegativeInt
        name: str
        location: Location
        photo: UUID
    """

    photo: UUID


class OfferWithOutAuthor(BaseOffer):
    """
    OfferWithOutAuthor pydantic model
    attrs:
        uuid: UUID
        offer_type: str
        price: NonNegativeInt
        name: str
        location: Location
        area: NonNegativeFloat
        description: str
        floor: NonNegativeInt
        tags: Optional[dict]
        photos: list[UUID]
    """

    area: NonNegativeFloat
    description: str
    floor: NonNegativeInt
    tags: Optional[dict]
    photos: list[UUID]  # UUID of photos


class InputOffer(OfferWithOutAuthor):
    """
    InputOffer pydantic model
    attrs:
        uuid: UUID
        offer_type: str
        price: NonNegativeInt
        name: str
        location: Coordinate
        area: NonNegativeFloat
        description: str
        floor: NonNegativeInt
        tags: Optional[dict]
        photos: list[UUID]
    """

    location: Coordinate  # type: ignore


class Offer(OfferWithOutAuthor):
    """
    Offer pydantic model
    attrs:
        uuid: UUID
        offer_type: str
        price: NonNegativeInt
        name: str
        location: Location
        area: NonNegativeFloat
        description: str
        floor: NonNegativeInt
        tags: Optional[dict]
        photos: list[UUID]
    """

    author: Author


class ValueSinceToValidate(BaseModel):
    """
    ValueSinceToValidate pydantic model
    attrs:
        value: Optional[NonNegativeInt] = None
        since: Optional[NonNegativeInt] = None
        to: Optional[NonNegativeInt] = None
    """

    value: Optional[NonNegativeInt] = None
    since: Optional[NonNegativeInt] = None
    to: Optional[NonNegativeInt] = None


class SearchValidate(BaseModel):
    """
    SearchValidate pydantic model
    attrs:
        offer_type: Optional[OfferType] = None
        uuid: Optional[UUID] = None
        author_id: Optional[int] = None
        author_name: Optional[str] = None
        price: Optional[ValueSinceToValidate] = None
        area: Optional[ValueSinceToValidate] = None
        location: Optional[Coordinate] = None
    """

    offer_type: Optional[OfferType] = None
    uuid: Optional[UUID] = None
    author_id: Optional[int] = None
    author_name: Optional[str] = None
    price: Optional[ValueSinceToValidate] = None
    area: Optional[ValueSinceToValidate] = None
    location: Optional[Coordinate] = None

    @model_validator(mode='before')
    @classmethod
    def _validate(cls, value: Any) -> SearchValidate:
        if not value:
            raise PydanticCustomError(
                'search_validate_error',
                'All values cannot be None! Use /offers/all to get all offers',
            )
        return value
