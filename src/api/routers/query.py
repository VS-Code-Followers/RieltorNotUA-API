from fastapi import APIRouter
from ...db.repo.offers import OfferRepo
from ..models import Offer
from ...config import get_engine
from uuid import UUID
from typing import Optional

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

# Test router. Will be delete when account router will be working


@router.get("/")
async def root_query() -> dict[str, str]:
    return {
        "result": "there will be information about possible settings for user (maybe XD)"
    }


@router.post("/create")
async def create_model(data: Offer):
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        await repo.add_offer(data)
    await engine.dispose()
    return {"msg": "Successfully created model", "status_code": 200}


@router.delete("/delete")
async def delete_model(uuid: Optional[UUID] = None, author_id: Optional[int] = None):
    engine = get_engine()
    msg = {"msg": "Successfully deleted model", "status_code": 201}
    async with engine.connect() as session:
        repo = OfferRepo(session)
        if uuid is not None:
            await repo.delete_offers_by_uuid(uuid)
        elif author_id is not None:
            await repo.delete_offers_by_author(author_id)
        else:
            msg = {"msg": "All params is None!", "status_code": 400}
    await engine.dispose()
    return msg


@router.delete("/delete/all")
async def delete_all_models():
    engine = get_engine()
    async with engine.connect() as session:
        repo = OfferRepo(session)
        await repo.cleanup_offers()
    await engine.dispose()
    return {"msg": "Successfully deleted all models", "status_code": 201}
