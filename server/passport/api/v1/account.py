from typing import Annotated

from database.controllers.account import AccountController
from database.controllers.operation import OperationController
from fastapi import APIRouter, Depends, status
from schemas.v1 import Account, AccountOperationOk, AccountReplenishment, Operation
from utils.auth import check_token

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_account_by_token_handler(
    controller: Annotated[AccountController, Depends(AccountController)],
    id: Annotated[int, Depends(check_token)],
) -> Account:
    account = await controller.get_account_by_id(id=id)
    return Account(**account.as_dict(exclude=["password"]))


@router.get("/operation", status_code=status.HTTP_200_OK)
async def get_operation_list_handler(
    controller: Annotated[OperationController, Depends(OperationController)],
    account_id: Annotated[int, Depends(check_token)],
) -> list[Operation]:
    return await controller.get_operation_list(account_id=account_id)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_account_by_id_handler(
    controller: Annotated[AccountController, Depends(AccountController)],
    id: int,
) -> Account:
    account = await controller.get_account_by_id(id=id)
    return Account(**account.as_dict(exclude=["password"]))


@router.put("/replenishment", status_code=status.HTTP_200_OK)
async def replenishment_handler(
    controller: Annotated[AccountController, Depends(AccountController)],
    id: Annotated[int, Depends(check_token)],
    replenishment: AccountReplenishment,
) -> AccountOperationOk:
    return await controller.replenishment_balance(id=id, replenishment=replenishment)
