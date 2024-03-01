from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from os import getenv


class FastAPI(BaseModel):
    host: str
    port: int


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
        env_nested_delimiter='_', env_file=getenv('ENV_FILE', None)
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
