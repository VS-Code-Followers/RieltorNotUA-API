from fastapi.param_functions import Form
from pydantic import EmailStr, BaseModel


class OAuth2Form:
    def __init__(
        self,
        email: EmailStr = Form(),
        password: str = Form(),
        scope: list[str] = Form(default=[]),
    ):
        self.email = email
        self.password = password
        self.scopes = scope


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
    scopes: list[str] = []
    

class GoogleUserInfo:
    email: EmailStr
    name: str
