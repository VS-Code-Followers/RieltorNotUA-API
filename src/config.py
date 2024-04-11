from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class Auth(BaseModel):
    """Auth Config Model"""

    google_client_id: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class FastAPI(BaseModel):
    """FastAPI Config Model"""

    host: str
    port: int
    auth: Auth


class DataBase(BaseModel):
    """DataBase Config Model"""

    driver: str
    user: str
    password: str
    host: str
    port: int
    name: str


class Config(BaseSettings):
    """Base Config Model"""

    fastapi: FastAPI
    database: DataBase
    model_config = SettingsConfigDict(
        env_nested_delimiter='__', env_file='.config/api.env'
    )


@lru_cache
def get_config() -> Config:
    """Get Base Config Model from ENV"""
    return Config()  # type: ignore


def get_engine(config: DataBase = get_config().database) -> AsyncEngine:
    """Get sqlalchemy engine from Base Config Model"""
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
