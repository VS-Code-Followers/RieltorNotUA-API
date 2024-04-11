from fastapi import APIRouter, status
from ...db.repo.offers import OfferRepo
from ...db.repo.users import UserRepo
from ..models.offers import Offer
from ..models.users import AuthorInDB, Author
from ..models.base import Response
from ...config import get_engine
from ..auth.base import get_password_hash
from uuid import UUID
from typing import Optional
from pydantic import EmailStr

router = APIRouter(
    prefix='/query',
    tags=['query'],
)

# Test router. Will be delete when account router will be working


@router.post('/offers/create')
async def create_model(data: Offer) -> Response:
    """Creating new offer"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        await repo.add_offer(data)
    await engine.dispose()
    return Response(
        msg='Successfully created offer model', status_code=status.HTTP_200_OK
    )


@router.delete('/offers/delete')
async def delete_model(
    uuid: Optional[UUID] = None, author_id: Optional[int] = None
) -> Response:
    """Deleting offer"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        if uuid is not None:
            await repo.delete_offers_by_uuid(uuid)
        elif author_id is not None:
            await repo.delete_offers_by_author_id(author_id)
        else:
            return Response(msg='All params is None!', status_code=status.HTTP_200_OK)
    await engine.dispose()
    return Response(
        msg='Successfully deleted offer model', status_code=status.HTTP_200_OK
    )


@router.delete('/offers/delete/all')
async def delete_all_models() -> Response:
    """Deleting all offers in the DB"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        await repo.cleanup_offers()
    await engine.dispose()
    return Response(
        msg='Successfully deleted all offers model', status_code=status.HTTP_200_OK
    )


@router.post('/users/create')
async def create_user(data: AuthorInDB) -> Response:
    """Creating new user"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = UserRepo(session)
        data.password = get_password_hash(data.password)
        await repo.create_user(data)
    await engine.dispose()
    return Response(
        msg='Successfully created user model', status_code=status.HTTP_200_OK
    )


@router.get('/users/get/all')
async def get_all_user() -> list[Author]:
    """Get all users in the DB"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = UserRepo(session)
        result = await repo.get_all_users()
    await engine.dispose()
    return result


@router.post('/users/get')
async def get_user_by_email(email: EmailStr) -> Optional[Author]:
    """Get user by email"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = UserRepo(session)
        result = await repo.get_user_by_email(email)
    await engine.dispose()
    return result
