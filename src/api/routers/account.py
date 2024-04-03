from fastapi import logger, APIRouter, Depends, HTTPException, status
import requests
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import (
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
from src.config import get_config

config = get_config()
auth = config.fastapi.auth
router = APIRouter(
    prefix="/account",
    tags=["account"],
)


@router.get("/")
async def root_account() -> dict[str, str]:
    return {
        'account': 'there will be information about possible settings for user (maybe 😁)'
    }

@router.get("/login/google")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={auth.GOOGLE_CLIENT_ID}&redirect_uri={auth.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": auth.GOOGLE_CLIENT_ID,
        "client_secret": auth.GOOGLE_CLIENT_SECRET,
        "redirect_uri": auth.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return user_info.json()


@router.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, auth.GOOGLE_CLIENT_SECRET, algorithms=["HS256"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me/', response_model=Author)
async def read_users_me(
    current_user: Annotated[Author, Depends(get_current_user)],
):
    return current_user


@router.get('/users/me/items/')
async def read_own_items(
    current_user: Annotated[Author, Depends(get_current_user)],
):
    return [{'item_id': 'Foo', 'owner': current_user.email}]
