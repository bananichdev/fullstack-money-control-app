from httpx import AsyncClient
from schemas.v1 import AccountNotEnoughMoney
from settings import WRITE_OFF_URL
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
