from fastapi import Depends, Security, APIRouter, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from ..models.auth import OAuth2Form
from ..auth.base import (
    authenticate_user,
    change_user_password,
    create_access_token,
    generate_password_reset_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM,
    send_password_recovery_email,
    verify_password_reset_token
)
from jose import ExpiredSignatureError, jwt

from ..models.users import Author
from ..models.offers import Offer, OfferWithOutAuthor, InputOffer
from ..models.base import Response, Location
from ...db.repo.offers import OfferRepo
from ..auth.google import get_user_info, authenticate_user_from_google
from ..tools.geocoding import get_full_adress

from typing import Annotated
from datetime import timedelta
from src.config import get_engine
from uuid import UUID


router = APIRouter(
    prefix='/account',
    tags=['account'],
)


@router.post("/password-recovery")
async def recover_password(email: EmailStr) -> JSONResponse:
    """
    Generating password recovery token and sending email with recovery link
    """
    password_reset_token = generate_password_reset_token(email)
    await send_password_recovery_email(email, password_reset_token)
    
    return JSONResponse(status_code=200, content={"message": "Email has been sent"})
  
  
@router.post("/reset-password")
async def reset_password(new_password: str, token: str) -> JSONResponse:
    """
    Resetting password
    """
    email = verify_password_reset_token(token=token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    await change_user_password(email, new_password)
    return JSONResponse(status_code=200, content={"message": "Password updated successfully"})
  
        
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
    return {'sub': 'No JWT'}


@router.post('/token', status_code=status.HTTP_204_NO_CONTENT)
async def login_for_access_token(
    form_data: Annotated[OAuth2Form, Depends()], request: Request
):
    """
    Creating and saving access token to the session for base(without google) user auth
    """
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # scopes question
        data={'sub': form_data.email, 'scopes': form_data.scopes},
        expires_delta=access_token_expires,
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
    data: InputOffer,
) -> Response:
    """Creating offer by user"""
    offer = Offer(
        author=current_user,
        location=Location(
            text=await get_full_adress(data.location), coordinate=data.location
        ),
        **data.model_dump(exclude={'location'}),
    )
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
