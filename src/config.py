from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from os import getenv


class Auth(BaseModel):
    client_id: int
    client_secret: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str


class FastAPI(BaseModel):
    host: str
    port: int
    auth: Auth


class DataBase(BaseModel):
    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str

class Config(BaseSettings):
    fastapi: FastAPI
    database: DataBase
    model_config = SettingsConfigDict(
        env_nested_delimiter='__', env_file=getenv('ENV_FILE', None)
    )


@lru_cache
def get_config() -> Config:
    return Config()


def get_engine(config: DataBase = get_config().database) -> AsyncEngine:
    return create_async_engine(
        URL.create(
            config.driver,
            config.user,
            config.password,
            config.host,
            config.port,
            config.name,
        )
    )
