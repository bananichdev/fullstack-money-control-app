from typing import Annotated

from fastapi import Depends, status
from fastapi.security import APIKeyCookie
from httpx import AsyncClient
from schemas.v1 import TokenIncorrect, TokenNotFound
from settings import CHECK_TOKEN_URL

AUTH_COOKIE_KEY = "authorization"

cookie_apikey = APIKeyCookie(name=AUTH_COOKIE_KEY, auto_error=False)


async def authenticate(access_token: Annotated[str, Depends(cookie_apikey)]) -> int:
    if access_token is None:
        raise TokenNotFound()

    async with AsyncClient() as client:
        response = await client.post(
            url=CHECK_TOKEN_URL,
            headers={AUTH_COOKIE_KEY: access_token},
        )

    if response.status_code == status.HTTP_200_OK:
        return int(response.json()["id"])

    elif response.status_code == status.HTTP_403_FORBIDDEN:
        raise TokenIncorrect()
