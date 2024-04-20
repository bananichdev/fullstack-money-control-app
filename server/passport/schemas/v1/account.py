from datetime import date

from pydantic import BaseModel


class AccountOperationOk(BaseModel):
    id: int


class AuthData(BaseModel):
    login: str
    password: str


class Account(AccountOperationOk, AuthData):
    balance: float
    admission_date: date
