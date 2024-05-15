from datetime import date

from sqlalchemy import Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    __table_args__ = {"schema": "products"}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    created_date: Mapped[date] = mapped_column(Date(), nullable=False, default=func.current_date())

    updated_date: Mapped[date] = mapped_column(Date(), nullable=True, onupdate=func.current_date())

    owner_id: Mapped[int] = mapped_column(nullable=False, index=True)

    def as_dict(self, exclude: list[str] | None = None) -> dict:
        res_dict = {}

        for column in self.__table__.columns:
            if not exclude or column.name not in exclude:
                if column.name in ["created_date", "updated_date"]:
                    res_dict[column.name] = (
                        str(getattr(self, column.name)) if getattr(self, column.name) else None
                    )
                else:
                    res_dict[column.name] = getattr(self, column.name)

        return res_dict
