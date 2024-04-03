from fastapi import logger, APIRouter, Depends, HTTPException, status
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

router = APIRouter(
    prefix='/account',
    tags=['account'],
)


@router.get('/')
async def root_account() -> dict[str, str]:
    return {
        'account': 'there will be information about possible settings for user (maybe 😁)'
    }


@router.post('/token')
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
