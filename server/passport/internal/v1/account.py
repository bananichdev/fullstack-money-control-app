from typing import Annotated

from database.controllers.account import AccountController
from fastapi import APIRouter, Depends, status
from schemas.v1 import AccountOperationOk, AccountWriteOff
from utils.auth import check_token

router = APIRouter()


@router.patch("/write_off", status_code=status.HTTP_200_OK)
async def write_off_handler(
    controller: Annotated[AccountController, Depends(AccountController)],
    id: Annotated[int, Depends(check_token)],
    write_off: AccountWriteOff,
) -> AccountOperationOk:
    pass
