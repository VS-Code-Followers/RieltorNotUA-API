from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class Auth(BaseModel):
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    client_secret: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


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
        env_nested_delimiter='__', env_file='.config/api.env'
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
