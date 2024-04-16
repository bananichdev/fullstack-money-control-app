from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseModel
from database.models.category import CategoryModel


class ProductModel(BaseModel):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey(CategoryModel.id)
    )
