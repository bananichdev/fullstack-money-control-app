from datetime import date

from database.models import AccountModel, OperationModel
from schemas.v1 import (
    Account,
    AccountAlreadyExists,
    AccountNotEnoughMoney,
    AccountNotFound,
    AccountOperationOk,
    AccountReplenishment,
    AccountReplenishmentForbidden,
    AccountWriteOff,
    AccountWrongPassword,
    AuthData,
    DBAPICallError, AccountWriteOffForbidden, AccountRefund, AccountRefundForbidden,
)
from settings import get_db_sessionmaker
from sqlalchemy import select, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from utils.auth import password_context


class AccountController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_account_by_id(self, id: int) -> AccountModel:
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

        return account_entity

    async def get_account_by_login(self, login: str) -> AccountModel:
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

        return account_entity

    async def create_account(self, account: AuthData) -> Account:
        try:
            async with self.db_sessionmaker.begin() as session:
                password = password_context.hash(account.password)
                account_entity = AccountModel(login=account.login, password=password)
                session.add(account_entity)
        except IntegrityError as e:
            raise AccountAlreadyExists() from e
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not create account") from e

        return Account(**account_entity.as_dict(exclude=["password"]))

    async def authenticate(self, account: AuthData) -> (AccountOperationOk, str):
        account_entity = await self.get_account_by_login(account.login)

        if not password_context.verify(account.password, account_entity.password):
            raise AccountWrongPassword()

        return AccountOperationOk(id=account_entity.id)

    async def replenishment_balance(
        self, id: int, replenishment: AccountReplenishment
    ) -> AccountOperationOk:
        account_entity = await self.get_account_by_id(id=id)
        if account_entity.balance_replenishment_date is not None:
            if (
                account_entity.balance_replenishment_date.day < date.today().day
                or account_entity.balance_replenishment_date.month == date.today().month
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
            raise DBAPICallError(msg="can not update balance and balance_replenishment_date") from e

        return AccountOperationOk(id=id)

    async def write_off_balance(self, write_off: AccountWriteOff) -> AccountOperationOk:
        account_entity = await self.get_account_by_id(id=write_off.id)
        if account_entity.balance_replenishment_date is None:
            raise AccountWriteOffForbidden()
        if account_entity.balance - write_off.amount < 0:
            raise AccountNotEnoughMoney()

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    update(AccountModel)
                    .where(AccountModel.id == write_off.id)
                    .values(
                        balance=AccountModel.balance - write_off.amount,
                    )
                )
                operation_entity = OperationModel(
                    account_id=write_off.id,
                    type="write_off",
                    amount=write_off.amount,
                )
                session.add(operation_entity)
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not update balance") from e

        return AccountOperationOk(id=write_off.id)

    async def refund_balance(self, refund: AccountRefund) -> AccountOperationOk:
        account_entity = await self.get_account_by_id(id=refund.id)
        if account_entity.balance_replenishment_date is None:
            raise AccountRefundForbidden()

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    update(AccountModel)
                    .where(AccountModel.id == refund.id)
                    .values(
                        balance=AccountModel.balance + refund.amount,
                    )
                )
                operation_entity = OperationModel(
                    account_id=refund.id,
                    type="refund",
                    amount=refund.amount,
                )
                session.add(operation_entity)
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not update balance") from e

        return AccountOperationOk(id=refund.id)
