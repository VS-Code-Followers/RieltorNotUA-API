from pydantic import BaseModel
from uuid import UUID
from pydantic_core import PydanticCustomError
from pydantic import model_validator, BaseModel, NonNegativeInt, NonNegativeFloat, EmailStr
from pydantic_extra_types.coordinate import Coordinate
from .base import Location
from typing import Optional

    
class User(BaseModel):
    email: EmailStr
    full_name: str
    account_id: int
    location: Location

# class Author(User):
#    my_offers: list[UUID]

class Author(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class AuthorInDB(Author):
    password: str