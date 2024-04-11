from fastapi import (
    Form,
    Security,
    logger,
    APIRouter,
    HTTPException,
    status,
    Request
)
from ..auth.base import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM
)
from jose import ExpiredSignatureError, jwt

from ..models.users import Author
from ..models.offers import Offer, OfferWithOutAuthor
from ..models.base import Response
from ...db.repo.offers import OfferRepo
from ..auth.google import get_user_info, authenticate_user_from_google

from typing import Annotated
from datetime import timedelta
from src.config import get_engine
from uuid import UUID


router = APIRouter(
    prefix='/account',
    tags=['account'],
)


@router.get('/auth/google')
async def auth_google(token: str, request: Request):
    """Creating access_token for user"""
    user = await get_user_info(token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    await authenticate_user_from_google(user.email, user.name)
    # Saving accsess token to the session
    request.session['access_token'] = access_token

# TODO: think about refresh token
@router.get('/token', status_code=status.HTTP_200_OK)
async def get_token(request: Request):
    """Getting data from access token"""
    access_token = request.session.get('access_token')
    if access_token:
        try:
            return jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
        except ExpiredSignatureError:
            return {'sub': 'Session expired'}
    return {'sub':'No JWT'}


@router.post('/token', status_code=status.HTTP_204_NO_CONTENT)
async def login_for_access_token(email: Annotated[str, Form()], password: Annotated[str, Form()], request: Request):
    """
    Creating and saving access token to the session for base(without google) user auth
    """
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # scopes question
        data={'sub': email, 'scopes': 'some scopes idk'},
        expires_delta=access_token_expires
    )
    request.session['access_token'] = access_token


@router.get('/logout')
async def logout(request: Request):
    """Logout user (deleting user`s access token)"""
    access_token = request.session.get('access_token')
    if access_token:
        request.session['access_token'] = ''
        return 'Logout successful'
    return 'No access token'

@router.get('/users/me/')
async def read_users_me(
    current_user: Annotated[Author, Security(get_current_user, scopes=['get_me'])],
) -> Author:
    """Getting user"""
    return current_user


@router.get('/users/me/offers/all')
async def read_own_offers(
    current_user: Annotated[
        Author, Security(get_current_user, scopes=['get_my_offers'])
    ],
) -> list[OfferWithOutAuthor]:
    """Getting user`s offers"""
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
    """Creating offer by user"""
    logger.logger.info(data)
    offer = Offer(author=current_user, **data.model_dump())
    async with get_engine().connect() as session:
        db = OfferRepo(session)
        await db.add_offer(offer)
    return Response(
        msg='Successfully created offer model', status_code=status.HTTP_201_CREATED
    )


@router.delete('/users/me/offers/delete')
async def delete_my_offer(
    current_user: Annotated[
        Author, Security(get_current_user, scopes=['delete_offer'])
    ],
    uuid: UUID,
) -> Response:
    """Deleting offer by user"""
    async with get_engine().connect() as session:
        db = OfferRepo(session)
        await db.delete_offers_by_uuid(uuid)
    return Response(
        msg='Successfully deleted offer model', status_code=status.HTTP_200_OK
    )


@router.delete('/users/me/offers/delete/all')
async def delete_all_my_offers(
    current_user: Annotated[
        Author, Security(get_current_user, scopes=['delete_offer'])
    ],
) -> Response:
    """Deleting all user offers"""
    async with get_engine().connect() as session:
        db = OfferRepo(session)
        await db.delete_offers_by_author_id(current_user.account_id)  # type: ignore
    return Response(
        msg='Successfully deleted all offer models', status_code=status.HTTP_200_OK
    )
