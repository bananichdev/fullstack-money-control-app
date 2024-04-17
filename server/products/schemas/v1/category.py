from datetime import date

from pydantic import BaseModel


class CategoryOperationOk(BaseModel):
    id: int


class Category(CategoryOperationOk):
    name: str
    created_date: date
    updated_date: date | None
