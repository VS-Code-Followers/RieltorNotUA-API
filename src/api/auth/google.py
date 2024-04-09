from src.config import get_config, get_engine
from ..models.users import AuthorInDB
from ..models.auth import GoogleUserInfo
from ...db.repo.users import UserRepo
from httpx import AsyncClient

# Google auth constants

config = get_config()
auth_config = config.fastapi.auth
db_config = config.database
GOOGLE_CLIENT_ID = auth_config.google_client_id
GOOGLE_CLIENT_SECRET = auth_config.google_client_secret
GOOGLE_REDIRECT_URI = auth_config.google_redirect_uri
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_LOGIN_URL = f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'


async def get_user_info(code: str) -> GoogleUserInfo:
    """
    Getting information about user from google.
    Takes code from google and returns GoogleUserInfo model
    """
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    async with AsyncClient() as client:
        response = await client.post(TOKEN_URL, data=data)
        # Posting to google token URL to get access at user info
        google_access_token = response.json().get('access_token')

        user_info_req = await client.get(
            'https://www.googleapis.com/oauth2/v1/userinfo',
            headers={'Authorization': f'Bearer {google_access_token}'},
        )
        user_info = user_info_req.json()

    return GoogleUserInfo(email=user_info['email'], name=user_info['name'])


async def authenticate_user_from_google(email: str, full_name: str) -> AuthorInDB:
    """Creating user if not exists yet"""
    async with get_engine(db_config).connect() as session:
        db = UserRepo(session)
        if not await db.user_exists(email):
            await db.create_user(AuthorInDB(email=email, full_name=full_name))
