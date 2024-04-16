from pydantic import BaseModel
from pydantic_extra_types.coordinate import Coordinate


class Location(BaseModel):
    """
    Location pydantic model
    attrs:
        text: str
        coordinate: Coordinate
    """

    text: str
    coordinate: Coordinate


class Response(BaseModel):
    """
    Response pydantic model
    attrs:
        msg: str
        status_code: int
    """

    msg: str
    status_code: int
