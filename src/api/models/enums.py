from enum import Enum


class Filters(Enum):
    BY_TYPE = "type"
    BY_REALTOR = "realtor"
    BY_AREA = "area"
    BY_LOCATION = "location"
    BY_PRICE = "price"


class OfferType(Enum):
    HOUSE = "house"
    FLAT = "flat"
    OFFICE = "office"
