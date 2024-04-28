from typing import Annotated

from database.controllers.account import AccountController
from fastapi import APIRouter, Depends, status
from schemas.v1.account import AccountOperationOk
from utils.auth import check_token_header

router = APIRouter()


@router.post("/check_token", status_code=status.HTTP_200_OK)
async def check_token(
    controller: Annotated[AccountController, Depends(AccountController)],
    id: Annotated[int, Depends(check_token_header)],
) -> AccountOperationOk:
    account = await controller.get_account_by_id(id=id)

    return AccountOperationOk(id=account.id)
