from fastapi import logger, APIRouter, Depends, HTTPException, status
import requests
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    oauth2_scheme,
    Token,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from ..auth.models import OAuth2Form
from ..models.users import Author
from typing import Annotated
from datetime import timedelta
from jose import jwt

router = APIRouter(
    prefix="/account",
    tags=["account"],
)

"""
fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "fakehashedsecret",
        "disabled": False,
    },
    "alice@example.com": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "password": "fakehashedsecret2",
        "disabled": True,
    },
}
"""

fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "$2b$12$DX/CgXx3.vwKSENi0mUZHeK.l94QqIPs9kWjaSu2CdfEmu2TfdrD2",
        "disabled": False,
    }
}


@router.get("/")
async def root_account() -> dict[str, str]:
    return {
        "account": "there will be information about possible settings for user (maybe 😁)"
    }


@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return user_info.json()


@router.post("/token/google")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    logger.logger.info(form_data)
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    logger.logger.info(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=Author)
async def read_users_me(
    current_user: Annotated[Author, Depends(get_current_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[Author, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.email}]
