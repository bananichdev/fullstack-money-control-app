import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()

PROXY_URL = os.environ.get("PROXY_URL")
DB_DRIVER = "postgresql"
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")
ALLOW_ORIGIN = "http://localhost"

DB_FULL_URL = f"{DB_DRIVER}+asyncpg://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}"

PROXY_INTERNAL_URL = f"{PROXY_URL}/internal"
PROXY_INTERNAL_V1_URL = f"{PROXY_INTERNAL_URL}/v1"
PROXY_INTERNAL_V1_PASSPORT_URL = f"{PROXY_INTERNAL_V1_URL}/passport"
CHECK_TOKEN_URL = f"{PROXY_INTERNAL_V1_PASSPORT_URL}/check_token"
WRITE_OFF_URL = f"{PROXY_INTERNAL_V1_PASSPORT_URL}/account/write_off"


@lru_cache
def get_db_sessionmaker() -> async_sessionmaker:
    return async_sessionmaker(
        create_async_engine(DB_FULL_URL),
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
