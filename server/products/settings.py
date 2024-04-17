import os

from dotenv import load_dotenv

load_dotenv()

NAME = "server"
HOST = "0.0.0.0"
PORT = 8000

PROXY_URL = os.environ.get("PROXY_URL")
DB_DRIVER = "postgresql"
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_URL = os.environ.get("DB_URL")
DB_NAME = os.environ.get("DB_NAME")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")

DB_FULL_URL = f"{DB_DRIVER}+asyncpg://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}"
TEST_DB_FULL_URL = f"{DB_DRIVER}+asyncpg://{DB_USER}:{DB_PASS}@{DB_URL}/{TEST_DB_NAME}"
ALLOW_ORIGIN = "http://localhost"
