from fastapi import APIRouter
from ..models.offers import Offer, SearchValidate, ShortOffer
from ...db.repo.offers import OfferRepo
from ...config import get_engine


router = APIRouter(
    prefix='/offers',
    tags=['offers'],
)


@router.post('/')
async def search_offers(value: SearchValidate) -> list[Offer]:
    """Searching offers in the DB"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        result = await repo.get_filters_offers(value)
    await engine.dispose()
    return result


@router.get('/all')
async def get_all_offers() -> list[Offer]:
    """Getting ALL offers in the DB"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        result = await repo.get_all_offers()
    await engine.dispose()
    return result


@router.get('/short/all')
async def get_all_short_offers() -> list[ShortOffer]:
    """Getting ALL a brief view of the offers in the DB"""
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        result = await repo.get_all_short_offfers()
    await engine.dispose()
    return result
