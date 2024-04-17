from database.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class AccountModel(BaseModel):
    __tablename__ = "account"

    login: Mapped[str] = mapped_column()

    password: Mapped[str] = mapped_column()

    balance: Mapped[float] = mapped_column()
