from datetime import date

from pydantic import BaseModel


class AccountOperationOk(BaseModel):
    id: int


class AuthData(BaseModel):
    login: str
    password: str


class AccountReplenishment(BaseModel):
    amount: float


class AccountWriteOff(AccountOperationOk, AccountReplenishment):
    pass


class AccountRefund(AccountOperationOk, AccountReplenishment):
    pass


class Account(AccountOperationOk):
    login: str
    balance: float
    balance_replenishment_date: date | None
