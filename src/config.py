from functools import lru_cache
from os import getenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


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
        env_file=getenv("ENV_FILE", ".env"), env_nested_delimiter="_"
    )


@lru_cache
def get_config() -> Config:
    return Config()
