from pydantic import BaseModel
from pydantic_extra_types.coordinate import Coordinate


class Location(BaseModel):
    text: str
    coordinate: Coordinate
