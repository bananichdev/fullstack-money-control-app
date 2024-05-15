from httpx import AsyncClient
from schemas.v1 import AccountNotEnoughMoney, AccountWriteOffForbidden, AccountRefundForbidden
from settings import REFUND_URL, WRITE_OFF_URL
from starlette import status


async def write_off_balance(owner_id: int, amount: float):
    async with AsyncClient() as client:
        response = await client.patch(
            url=WRITE_OFF_URL,
            json={
                "id": owner_id,
                "amount": amount,
            },
        )
        if response.status_code == status.HTTP_403_FORBIDDEN:
            raise AccountNotEnoughMoney()
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            raise AccountWriteOffForbidden()


async def refund_balance(owner_id: int, amount: float):
    async with AsyncClient() as client:
        response = await client.patch(
            url=REFUND_URL,
            json={
                "id": owner_id,
                "amount": amount,
            }
        )
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        raise AccountRefundForbidden()
