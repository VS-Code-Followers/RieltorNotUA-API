from src.config import get_config, get_engine
from ..models.users import AuthorInDB
from ..models.auth import GoogleUserInfo
from ...db.repo.users import UserRepo
from google.oauth2 import id_token
from google.auth.transport import requests

# Google auth constants

config = get_config()
auth_config = config.fastapi.auth
db_config = config.database
GOOGLE_CLIENT_ID = auth_config.google_client_id


async def get_user_info(token: str) -> GoogleUserInfo:
    """
    Getting information about user from google.
    Takes code from google and returns GoogleUserInfo model
    """
    # clock_skew_in_seconds added because without it function throws exception "Token used too early"
    user_info = id_token.verify_oauth2_token(
        token, requests.Request(), GOOGLE_CLIENT_ID, clock_skew_in_seconds=10
    )

    return GoogleUserInfo(email=user_info['email'], name=user_info['name'])


async def authenticate_user_from_google(email: str, full_name: str) -> None:
    """Creating user if not exists yet"""
    async with get_engine(db_config).connect() as session:
        db = UserRepo(session)
        if not await db.user_exists(email):
            await db.create_user(AuthorInDB(email=email, full_name=full_name))
