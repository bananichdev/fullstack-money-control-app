import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

HOST = "0.0.0.0"
PORT = 8000

PROXY_URL = os.environ.get("PROXY_URL")
DB_DRIVER = "postgresql"
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")

DB_FULL_URL = f"{DB_DRIVER}+asyncpg://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}"
ALLOW_ORIGIN = "http://localhost"

ALGORITHM = os.environ.get("ALGORITHM")
HASH_ROUNDS = os.environ.get("HASH_ROUNDS")
SECRET_KEY = os.environ.get("SECRET_KEY")


@lru_cache
def get_db_sessionmaker() -> async_sessionmaker:
    return async_sessionmaker(
        create_async_engine(DB_FULL_URL),
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
