from datetime import date

from database.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class AccountModel(BaseModel):
    __tablename__ = "account"

    login: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    password: Mapped[str] = mapped_column(nullable=False)

    balance: Mapped[float] = mapped_column(nullable=False, default=float(0))

    balance_replenishment_date: Mapped[date] = mapped_column(nullable=True, default=None)
