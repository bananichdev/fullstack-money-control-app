from datetime import date

from database.models.account import AccountModel
from database.models.base import BaseModel

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from utils.operations import OperationType


class OperationModel(BaseModel):
    __tablename__ = "operations"

    account_id: Mapped[str] = mapped_column(ForeignKey(AccountModel.id))

    type: Mapped[OperationType] = mapped_column(nullable=False)

    amount: Mapped[float] = mapped_column(nullable=False)

    operation_date: Mapped[date] = mapped_column(nullable=False, default=date.today)
