from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from pydantic import (
    EmailStr,
)
from .base import Location


class User(BaseModel):
    """
    User pydantic model
    attrs:
        email: EmailStr
        full_name: str
        account_id: Optional[int] = None
        location: Optional[Location] = None
    """

    email: EmailStr
    full_name: str
    account_id: Optional[int] = None
    location: Optional[Location] = None


class Author(User):
    """
    Author pydantic model
    attrs:
        email: EmailStr
        full_name: str
        account_id: Optional[int] = None
        location: Optional[Location] = None
        offers: Optional[list[UUID]] = None
    """

    offers: Optional[list[UUID]] = None


class AuthorInDB(Author):
    """
    AuthorInDB pydantic model
    attrs:
        email: EmailStr
        full_name: str
        account_id: Optional[int] = None
        location: Optional[Location] = None
        offers: Optional[list[UUID]] = None
        password: Optional[str] = None
    """

    password: Optional[str] = None
