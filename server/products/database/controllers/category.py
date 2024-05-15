from database.models import CategoryModel
from schemas.v1 import (
    Category,
    CategoryAlreadyExists,
    CategoryCreatingData,
    CategoryDeleteError,
    CategoryNotFound,
    CategoryOperationOk,
    DBAPICallError,
)
from settings import get_db_sessionmaker
from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError


class CategoryController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_category_by_id(self, id: int, owner_id: int) -> Category:
        try:
            async with self.db_sessionmaker.begin() as session:
                if (
                    category_entity := await session.scalar(
                        select(CategoryModel).where(
                            and_(
                                CategoryModel.id == id,
                                CategoryModel.owner_id == owner_id,
                            )
                        )
                    )
                ) is None:
                    raise CategoryNotFound()
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get category") from e

        return Category(**category_entity.as_dict())

    async def get_category_list(self, owner_id: int) -> list[Category]:
        try:
            async with self.db_sessionmaker.begin() as session:
                category_entity_list = await session.scalars(
                    select(CategoryModel).where(CategoryModel.owner_id == owner_id)
                )
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get category list") from e

        return [Category(**category.as_dict()) for category in category_entity_list]

    async def create_category(self, category: CategoryCreatingData, owner_id: int) -> Category:
        try:
            async with self.db_sessionmaker.begin() as session:
                category_entity = await session.scalar(
                    select(CategoryModel).where(
                        and_(
                            CategoryModel.name == category.name,
                            CategoryModel.owner_id == owner_id,
                        )
                    )
                )
                if category_entity is not None:
                    raise CategoryAlreadyExists(name=category.name)

                category_entity = CategoryModel(name=category.name, owner_id=owner_id)
                session.add(category_entity)
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not create category") from e

        return Category(**category_entity.as_dict())

    async def update_category(self, id: int, new_name: str, owner_id: int) -> CategoryOperationOk:
        category = await self.get_category_by_id(id=id, owner_id=owner_id)

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

    async def delete_category(self, id: int, owner_id: int) -> CategoryOperationOk:
        category = await self.get_category_by_id(id=id, owner_id=owner_id)

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(delete(CategoryModel).where(CategoryModel.id == category.id))
        except IntegrityError as e:
            await session.rollback()
            raise CategoryDeleteError(name=category.name) from e
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not delete category") from e

        return CategoryOperationOk(id=category.id)
