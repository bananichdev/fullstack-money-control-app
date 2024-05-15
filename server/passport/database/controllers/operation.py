from database.models import OperationModel
from schemas.v1 import DBAPICallError, Operation
from settings import get_db_sessionmaker
from sqlalchemy import desc, select
from sqlalchemy.exc import DBAPIError


class OperationController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_operation_list(self, account_id: int) -> list[Operation]:
        try:
            async with self.db_sessionmaker() as session:
                operation_entity_list = await session.scalars(
                    select(OperationModel)
                    .where(OperationModel.account_id == account_id)
                    .order_by(desc(OperationModel.id))
                )
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get operation list") from e

        return [
            Operation(**operation_entity.as_dict()) for operation_entity in operation_entity_list
        ]
