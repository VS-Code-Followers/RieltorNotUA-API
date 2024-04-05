from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from pydantic import (
    EmailStr,
)
from .base import Location


class User(BaseModel):
    email: EmailStr
    full_name: str
    account_id: Optional[int] = None
    location: Optional[Location] = None


class Author(User):
    offers: Optional[list[UUID]] = None


class AuthorInDB(Author):
    password: Optional[str] = None
