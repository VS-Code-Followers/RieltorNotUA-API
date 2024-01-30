from fastapi import APIRouter

router = APIRouter(
    prefix="/account",
    tags=["account"],
)


@router.get("/")
async def root_account():
    return {"root": 5}
