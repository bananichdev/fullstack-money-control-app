from database.models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class CategoryModel(BaseModel):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
