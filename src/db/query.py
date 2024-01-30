"""
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from .models.core import Base
from ..config import get_config

config = get_config().database
url = URL.create(
    config.drivername,
    config.username,
    config.password,
    config.host,
    config.port,
    config.db_name
)

engine = create_engine(url, echo=True)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
"""
