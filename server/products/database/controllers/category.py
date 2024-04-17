from database.models import CategoryModel
from schemas.v1 import (
    Category,
    CategoryAlreadyExists,
    CategoryDeleteError,
    CategoryNotFound,
    CategoryOperationOk,
    DBAPICallError,
)
from sqlalchemy import delete, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError

from server.common.settings import get_db_sessionmaker


class CategoryController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_category_by_id(self, id: int) -> Category | None:
        try:
            async with self.db_sessionmaker.begin() as session:
                category_entity = await session.scalar(
                    select(CategoryModel).where(CategoryModel.id == id)
                )
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get category") from e

        if category_entity is None:
            raise CategoryNotFound()

        return Category(**category_entity.as_dict()) if category_entity else None

    async def get_category_list(self) -> list[Category]:
        try:
            async with self.db_sessionmaker.begin() as session:
                category_entity_list = await session.scalars(select(CategoryModel))
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get category list") from e

        category_list = [
            Category(**category.as_dict()) for category in category_entity_list
        ]
        if not category_list:
            raise CategoryNotFound()

        return category_list

    async def create_category(self, name: str) -> Category:
        try:
            async with self.db_sessionmaker.begin() as session:
                category_entity = CategoryModel(name=name)
                session.add(category_entity)
        except IntegrityError as e:
            await session.rollback()
            raise CategoryAlreadyExists() from e
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not create category") from e

        return Category(**category_entity.as_dict())

    async def update_category(self, id: int, new_name: str) -> CategoryOperationOk:
        category = await self.get_category_by_id(id=id)

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    update(CategoryModel)
                    .where(CategoryModel.id == category.id)
                    .values(name=new_name)
                )
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not update category") from e

        return CategoryOperationOk(id=category.id)

    async def delete_category(self, id: int) -> CategoryOperationOk:
        category = await self.get_category_by_id(id=id)

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    delete(CategoryModel).where(CategoryModel.id == category.id)
                )
        except IntegrityError as e:
            await session.rollback()
            raise CategoryDeleteError() from e
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not delete category") from e

        return CategoryOperationOk(id=category.id)
