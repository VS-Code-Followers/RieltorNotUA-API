from fastapi.param_functions import Form
from pydantic import EmailStr, BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
    scopes: list[str] = []
