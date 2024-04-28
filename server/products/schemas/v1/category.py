from datetime import date

from pydantic import BaseModel


class CategoryOperationOk(BaseModel):
    id: int


class CategoryCreatingData(BaseModel):
    name: str


class Category(CategoryOperationOk, CategoryCreatingData):
    owner_id: int
    created_date: date
    updated_date: date | None
