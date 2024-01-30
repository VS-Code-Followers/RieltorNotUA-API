from fastapi import APIRouter
from ..models.enums import Filters

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get("/")
async def root_search(filters: Filters):
    return {"result": filters}
