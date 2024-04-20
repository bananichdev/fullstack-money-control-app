from settings import get_db_sessionmaker


class AccountController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_account_by_id(self):
        pass

    async def create_account(self):
        pass
