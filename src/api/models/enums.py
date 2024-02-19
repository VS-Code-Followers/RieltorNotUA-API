from enum import Enum


class Filters(Enum):
    ALL = "all"
    BY_TYPE = "type"
    BY_REALTOR = "author_id"
    BY_ID = "uuid"
    BY_AREA = "area"
    BY_LOCATION = "location"
    BY_PRICE = "price"


class OfferType(Enum):
    HOUSE = "house"
    FLAT = "flat"
    OFFICE = "office"

    def __repr__(self) -> str:
        return self.value
