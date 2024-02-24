from fastapi import APIRouter

router = APIRouter(
    prefix='/account',
    tags=['account'],
)


@router.get('/')
async def root_account() -> dict[str, str]:
    return {
        'account': 'there will be information about possible settings for user (maybe 😁)'
    }
