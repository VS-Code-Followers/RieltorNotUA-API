from fastapi import APIRouter
from ...db.repo.offers import OfferRepo
from ...db.repo.users import UserRepo
from ..models.offers import Offer
from ..models.users import AuthorInDB, Author
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


@router.get('/')
async def root_query() -> dict[str, str]:
    return {
        'result': 'there will be information about possible settings for user (maybe XD)'
    }


@router.post('/offers/create')
async def create_model(data: Offer) -> dict[str, str | int]:
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        await repo.add_offer(data)
    await engine.dispose()
    return {'msg': 'Successfully created offer model', 'status_code': 200}


@router.delete('/offers/delete')
async def delete_model(
    uuid: Optional[UUID] = None, author_id: Optional[int] = None
) -> dict[str, str | int]:
    engine = get_engine()
    msg = {'msg': 'Successfully deleted offer model', 'status_code': 201}
    async with engine.connect() as session:
        repo = OfferRepo(session)
        if uuid is not None:
            await repo.delete_offers_by_uuid(uuid)
        elif author_id is not None:
            await repo.delete_offers_by_author_id(author_id)
        else:
            msg = {'msg': 'All params is None!', 'status_code': 400}
    await engine.dispose()
    return msg


@router.delete('/offers/delete/all')
async def delete_all_models() -> dict[str, str | int]:
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        await repo.cleanup_offers()
    await engine.dispose()
    return {'msg': 'Successfully deleted all offer models', 'status_code': 201}


@router.post('/users/create')
async def create_user(data: AuthorInDB) -> dict[str, str | int]:
    engine = get_engine()
    async with engine.connect() as session:
        repo = UserRepo(session)
        data.password = get_password_hash(data.password)
        await repo.create_user(data)
    await engine.dispose()
    return {'msg': 'Successfully create user model', 'status_code': 201}


@router.get('/users/get/all')
async def get_all_user() -> list[Author]:
    engine = get_engine()
    async with engine.connect() as session:
        repo = UserRepo(session)
        result = await repo.get_all_users()
    await engine.dispose()
    return result


@router.post('/users/get')
async def get_user_by_email(email: EmailStr) -> Author:
    engine = get_engine()
    async with engine.connect() as session:
        repo = UserRepo(session)
        result = await repo.get_password_by_email(email)
    await engine.dispose()
    return result
