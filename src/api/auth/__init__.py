from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from fastapi import logger,HTTPException
from ..models.users import AuthorInDB
from ...db.repo.users import UserRepo
from src.config import get_config, get_engine
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, EmailStr
from .models import Token, TokenData
from fastapi import Depends, status
from typing import Optional, Annotated

config = get_config()
auth_config = config.fastapi.auth
db_config = config.database
SECRET_KEY = auth_config.secret_key
ALGORITHM = auth_config.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = auth_config.access_token_expire_minutes


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str) -> AuthorInDB:
    async with get_engine(db_config).connect() as session:
        db = UserRepo(session)
        password_from_db = await db.get_password_by_email(email)
        if not password_from_db:
            return False
        if not verify_password(password, password_from_db):
            return False
        return password_from_db

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: EmailStr = payload.get("sub")
        if email is None:
            raise credentials_exception
        async with get_engine(db_config).connect() as session:
            db = UserRepo(session)
            password = await db.get_password_by_email(email)
            user = await db.get_user_by_password(password)
            return user
    except JWTError:
        raise credentials_exception

