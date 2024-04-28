from typing import Annotated

from database.controllers.account import AccountController
from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import JSONResponse
from schemas.v1 import Account, AccountOperationOk, AuthData, RequestAuthDataError
from utils.auth import AUTH_COOKIE_KEY, check_token, create_token

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_handler(
    controller: Annotated[AccountController, Depends(AccountController)],
    account: AuthData | None = None,
    access_token: str | None = Cookie(default=None, alias=AUTH_COOKIE_KEY),
) -> AccountOperationOk | Account:
    if access_token is not None:
        id = await check_token(access_token=access_token)
        return AccountOperationOk(id=id)

    if account is not None:
        return await controller.authenticate(account=account)

    raise RequestAuthDataError()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_handler(
    controller: Annotated[AccountController, Depends(AccountController)],
    account: AuthData,
) -> AccountOperationOk:
    account_entity = await controller.create_account(account)
    access_token = await create_token(id=account_entity.id)

    response = JSONResponse(content={"id": account_entity.id})
    response.set_cookie(AUTH_COOKIE_KEY, access_token, httponly=True)

    return response


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_handler() -> JSONResponse:
    response = JSONResponse(content=None)
    response.delete_cookie(key=AUTH_COOKIE_KEY, httponly=True)

    return response
