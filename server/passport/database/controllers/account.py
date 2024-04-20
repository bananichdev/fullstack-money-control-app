from sqlalchemy.exc import DBAPIError

from database.models import AccountModel
from schemas.v1 import DBAPICallError, AuthData, Account

from settings import get_db_sessionmaker


class AccountController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_account_by_id(self):
        pass

    async def create_account(self, account: AuthData) -> Account:
        try:
            async with self.db_sessionmaker.begin() as session:
                account_entity = AccountModel(**account.model_dump())
                session.add(account_entity)
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not create account") from e

        return Account(**account_entity.as_dict())
