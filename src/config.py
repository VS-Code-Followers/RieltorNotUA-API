from dataclasses import dataclass
from environs import Env


@dataclass
class FastAPI:
    host: str
    port: int


@dataclass
class DataBase:
    drivername: str
    username: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass
class Config:
    fastapi: FastAPI
    database: DataBase


def get_config(path: str = ".env") -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        FastAPI(env.str("FASTAPI_HOST"), env.int("FASTAPI_PORT")),
        DataBase(
            env.str("DATABASE_DRIVER"),
            env.str("DATABASE_USER"),
            env.str("DATABASE_PASSWORD"),
            env.str("DATABASE_HOST"),
            env.int("DATABASE_PORT"),
            env.str("DATABASE_NAME"),
        ),
    )
