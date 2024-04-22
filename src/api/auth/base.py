from pathlib import Path
from fastapi.security import SecurityScopes
from fastapi import Request, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from ..models.users import Author
from ...db.repo.users import UserRepo
from src.config import get_config, get_engine
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from pydantic import EmailStr, ValidationError
from ..models.auth import TokenData
from fastapi import Depends, status
from typing import Optional, Annotated


# Base auth constants

config = get_config()
auth_config = config.fastapi.auth
db_config = config.database
SECRET_KEY = auth_config.secret_key
ALGORITHM = auth_config.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = auth_config.access_token_expire_minutes
HOST = config.fastapi.host
EMAIL_RESET_TOKEN_EXPIRE_HOURS = auth_config.email_reset_token_expire_hours 


conf = ConnectionConfig(
    MAIL_USERNAME = auth_config.mail,
    MAIL_PASSWORD = auth_config.password,
    MAIL_FROM = auth_config.mail,
    MAIL_PORT = auth_config.mail_port,
    MAIL_SERVER = auth_config.mail_server,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    TEMPLATE_FOLDER = Path(__file__).parent / 'email-templates'/ 'build'
)

# CryptoContext to encrypt credentials
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    """Checking if password is correct"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Creating password hash. Used when create user account"""
    return pwd_context.hash(password)


async def get_access_token(request: Request):
    token = request.session.get('access_token')
    if not bool(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return token


async def authenticate_user(email: str, password: str) -> Author | bool:
    """Getting user from DB. If user not exists or password is incorrect, returns False"""
    async with get_engine(db_config).connect() as session:
        db = UserRepo(session)
        password_from_db = await db.get_password_by_email(email)
        if not password_from_db:
            return False
        if not verify_password(password, password_from_db):
            return False
        user = await db.get_user_by_email(email)
        if not user:
            return False
        return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creating user`s access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(get_access_token)]
):
    """
    Getting current user.
    Raises HTTPException if couldn`t validate users credentials
    or user didn`t  have enough permissions
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        # Decoding token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(scopes=token_scopes, email=email)
        for scope in security_scopes.scopes:
            # Checking if user had this scopes
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Not enough permissions',
                    headers={
                        'WWW-Authenticate': f'Bearer scope="{security_scopes.scope_str}"'
                    },
                )
        async with get_engine(db_config).connect() as session:
            db = UserRepo(session)
            # returning User from DB
            return await db.get_user_by_email(email)
    # TODO: add ExpiredSignatureError handling
    except (JWTError, ValidationError, ExpiredSignatureError):
        raise credentials_exception


async def send_password_recovery_email(email: EmailStr, token: str):
	"""
	Sending email with password recovery link
	"""
	async with get_engine().connect() as session:
		db = UserRepo(session)
		user = await db.get_user_by_email(email)
		if not user:
			raise HTTPException(
				status_code=404,
				detail="The user with this email does not exist in the system.",
			)
            
	subject = f"RieltorNotUA - Password recovery for user {user.full_name}"
	link=f"{HOST}/reset-password?token={token}"

	message = MessageSchema(
		subject=subject,
		recipients=[email],
		template_body={'project_name': "RieltorNotUA", 'username': user.full_name,"valid_hours": EMAIL_RESET_TOKEN_EXPIRE_HOURS, 'link': link},
		subtype=MessageType.html)

	fm = FastMail(conf)
	await fm.send_message(message, template_name="reset_password.html")


def generate_password_reset_token(email: EmailStr) -> str:
	"""
	Generating token for resetting password with email
	"""
	expires = datetime.now(timezone.utc) + timedelta(hours=EMAIL_RESET_TOKEN_EXPIRE_HOURS)
	encoded_jwt = jwt.encode(
		{"exp": expires, "sub": email}, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    """
	Verifing token for resetting password with email
	"""
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return str(decoded_token["sub"])
    except JWTError:
        return None
    
async def change_user_password(email: EmailStr, new_password: str):
	"""
	Changing user password after resetting/recovering
	"""
	async with get_engine().connect() as session:
		db = UserRepo(session)
		if not await db.user_exists(email):
			raise HTTPException(
				status_code=404,
				detail="The user with this email does not exist in the system.",
			)
		hashed_password = get_password_hash(new_password)
		await db.change_user_password(email, hashed_password)
