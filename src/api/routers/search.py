from fastapi import APIRouter
from ..models import Offer
from ..models import SearchValidate
from ...db.repo.offers import OfferRepo
from ...config import get_engine


router = APIRouter(
    prefix='/search',
    tags=['search'],
)


@router.post('/')
async def search(value: SearchValidate) -> list[Offer]:
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        result = await repo.get_filters_offers(value)
    await engine.dispose()
    return result
