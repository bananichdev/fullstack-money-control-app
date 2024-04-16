from datetime import date

from pydantic import BaseModel


class ProductOperationOk(BaseModel):
    id: int


class ProductChangingData(BaseModel):
    name: str | None
    category_id: int | None


class ProductCreatingData(BaseModel):
    name: str
    price: float
    category_id: int


class Product(ProductOperationOk, ProductCreatingData):
    created_date: date
    updated_date: date | None
