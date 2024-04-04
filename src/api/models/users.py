from pydantic import BaseModel
from uuid import UUID
from pydantic import (
    EmailStr,
)
from .base import Location


class User(BaseModel):
    email: EmailStr
    full_name: str
    account_id: int
    location: Location


class Author(User):
    offers: list[UUID]


class AuthorInDB(Author):
    password: str
