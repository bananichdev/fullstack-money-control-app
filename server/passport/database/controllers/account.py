from datetime import date

from database.models import AccountModel, OperationModel
from schemas.v1 import (
    Account,
    AccountNotFound,
    AccountOperationOk,
    AccountReplenishment,
    AccountReplenishmentForbidden,
    AccountWriteOff,
    AccountWrongPassword,
    AuthData,
    DBAPICallError,
)
from settings import get_db_sessionmaker
from sqlalchemy import select, update
from sqlalchemy.exc import DBAPIError
from utils.auth import password_context


class AccountController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_account_by_id(self, id: int) -> Account:
        try:
            async with self.db_sessionmaker() as session:
                if (
                    account_entity := await session.scalar(
                        select(AccountModel).where(AccountModel.id == id)
                    )
                ) is None:
                    raise AccountNotFound()
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get account by id") from e

        return Account(**account_entity.as_dict(exclude=["password"]))

    async def get_account_by_login(self, login: str) -> Account:
        try:
            async with self.db_sessionmaker.begin() as session:
                if (
                    account_entity := await session.scalar(
                        select(AccountModel).where(AccountModel.login == login)
                    )
                ) is None:
                    raise AccountNotFound()
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get account by login") from e

        return (
            Account(**account_entity.as_dict(exclude=["password"]))
            if account_entity
            else None
        )

    async def create_account(self, account: AuthData) -> Account:
        try:
            async with self.db_sessionmaker.begin() as session:
                password = password_context.hash(account.password)
                account_entity = AccountModel(login=account.login, password=password)
                session.add(account_entity)
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not create account") from e

        return Account(**account_entity.as_dict(exclude=["password"]))

    async def authenticate(self, account: AuthData) -> AccountOperationOk:
        account_entity = await self.get_account_by_login(account.login)

        if not password_context.verify(account.password, account_entity.password):
            raise AccountWrongPassword()

        return AccountOperationOk(id=account_entity.id)

    async def replenishment_balance(
        self, id: int, replenishment: AccountReplenishment
    ) -> AccountOperationOk:
        account_entity = await self.get_account_by_id(id=id)
        if (
            account_entity.balance_replenishment_date is not None
            and account_entity.balance_replenishment.day < date.today().day
        ):
            raise AccountReplenishmentForbidden()

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    update(AccountModel)
                    .where(AccountModel.id == id)
                    .values(
                        balance=AccountModel.balance + replenishment.amount,
                    )
                )
                operation_entity = OperationModel(
                    account_id=id,
                    type="replenishment",
                    amount=replenishment.amount,
                )
                session.add(operation_entity)
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(
                msg="can not update balance and balance_replenishment_date"
            ) from e

        return AccountOperationOk(id=id)

    async def write_off_balance(
        self, id: int, write_off: AccountWriteOff
    ) -> AccountOperationOk:
        pass
