from fastapi.param_functions import Form
from pydantic import EmailStr, BaseModel


class OAuth2Form:
    """
    OAuth2Form to authenticate user
    attrs:
        email: EmailStr = Form(),
        password: str = Form(),
        scope: list[str] = Form(default=[])
    """

    def __init__(
        self,
        email: EmailStr = Form(),
        password: str = Form(),
        scope: list[str] = Form(
            default=[],
        ),
    ):
        self.email = email
        self.password = password
        self.scopes = scope


class Token(BaseModel):
    """
    Token pydantic model.
    attrs:
        access_token: str
        token_type: str
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData pydantic model.
    attrs:
        email: EmailStr
        scopes: list[str] = []
    """

    email: EmailStr
    scopes: list[str] = []


class GoogleUserInfo(BaseModel):
    """
    GoogleUserInfo pydantic model
    attrs:
        email: EmailStr
        name: str
    """

    email: EmailStr
    name: str
