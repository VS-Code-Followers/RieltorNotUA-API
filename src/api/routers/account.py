from fastapi import (
    Security,
    logger,
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
)
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.base import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from jose import jwt
from ..models.auth import Token
from ..models.users import Author
from ..models.offers import Offer, OfferWithOutAuthor
from ..models.base import Response
from ...db.repo.offers import OfferRepo
from ..auth.google import get_user_info, authenticate_user_from_google

from typing import Annotated
from datetime import timedelta
from src.config import get_config, get_engine
from uuid import UUID

config = get_config()
auth = config.fastapi.auth

router = APIRouter(
    prefix='/account',
    tags=['account'],
)


@router.get('/login/google')
async def login_google():
    return {
        'url': f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={auth.google_client_id}&redirect_uri={auth.google_redirect_uri}&scope=openid%20profile%20email&access_type=offline'
    }


@router.get('/auth/google')
async def auth_google(code: str, request: Request):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user =  await get_user_info(code)
    access_token = create_access_token(
        data={'sub':user.email}, expires_delta=access_token_expires
    )
    await authenticate_user_from_google(user.email, user.name)
    request.session['access_token'] = access_token
    return RedirectResponse('/')


@router.get('/google/token')
async def get_token(request: Request):
    access_token = request.session.get('access_token')
    if access_token:
        return jwt.decode(access_token, auth.secret_key, algorithms=['HS256'])
    return 'No JWT token'


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
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
        data={'sub': form_data.username, 'scopes': form_data.scopes},
        expires_delta=access_token_expires,
    )
    request.session['access_token'] = access_token
    return Token(access_token=access_token, token_type='bearer')


@router.get('/logout')
async def logout(request: Request):
    access_token = request.session.get('access_token')
    if access_token:
        request.session['access_token'] = ''
        return "Logout successful"
    return "No access token"



@router.get('/users/me/')
async def read_users_me(
    current_user: Annotated[Author, Security(get_current_user, scopes=['get_me'])],
) -> Author:
    return current_user


@router.get('/users/me/offers/all')
async def read_own_offers(
    current_user: Annotated[
        Author, Security(get_current_user, scopes=['get_my_offers'])
    ],
) -> list[OfferWithOutAuthor]:
    async with get_engine().connect() as session:
        db = OfferRepo(session)
        return await db.get_offers_by_author(current_user.account_id)


@router.post('/users/me/offers/create')
async def create_new_offer(
    current_user: Annotated[
        Author, Security(get_current_user, scopes=['create_offer'])
    ],
    data: OfferWithOutAuthor,
) -> Response:
    logger.logger.info(data)
    offer = Offer(author=current_user, **data.model_dump())
    async with get_engine().connect() as session:
        db = OfferRepo(session)
        await db.add_offer(offer)
    return Response(msg='Successfully created offer model', status_code=200)


@router.delete('/users/me/offers/delete')
async def delete_my_offer(
    current_user: Annotated[
        Author, Security(get_current_user, scopes=['delete_offer'])
    ],
    uuid: UUID,
) -> Response:
    async with get_engine().connect() as session:
        db = OfferRepo(session)
        await db.delete_offers_by_uuid(uuid)
    return Response(msg='Successfully deleted offer model', status_code=201)


@router.delete('/users/me/offers/delete/all')
async def delete_all_my_offers(
    current_user: Annotated[
        Author, Security(get_current_user, scopes=['delete_offer'])
    ],
) -> Response:
    async with get_engine().connect() as session:
        db = OfferRepo(session)
        await db.delete_offers_by_author_id(current_user.account_id)
    return Response(msg='Successfully deleted all offer models', status_code=201)
