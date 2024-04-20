from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyCookie, APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext

from schemas.v1 import TokenIncorrect, TokenNotFound
from settings import ALGORITHM, HASH_ROUNDS, SECRET_KEY

AUTH_COOKIE_KEY = "authorization"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=HASH_ROUNDS)

cookie_apikey = APIKeyCookie(name=AUTH_COOKIE_KEY, auto_error=False)
header_apikey = APIKeyHeader(name=AUTH_COOKIE_KEY, auto_error=False)


async def create_token(id: int) -> str:
    to_encode = {"id": id}
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


async def check_token(access_token: Annotated[str, Depends(cookie_apikey)]) -> int:
    if access_token is None:
        raise TokenNotFound()

    try:
        return jwt.decode(access_token, SECRET_KEY, ALGORITHM).get("id")
    except JWTError as e:
        raise TokenIncorrect() from e


async def check_token_header(access_token: Annotated[str, Depends(header_apikey)]) -> int:
    if access_token is None:
        raise TokenNotFound()

    try:
        return jwt.decode(access_token, SECRET_KEY, ALGORITHM).get("id")
    except JWTError as e:
        raise TokenIncorrect() from e
