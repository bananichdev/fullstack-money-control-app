from datetime import date

from database.models import ProductModel
from schemas.v1 import (
    CategoryNotFound,
    DBAPICallError,
    Product,
    ProductChangingData,
    ProductCreatingData,
    ProductNotFound,
    ProductOperationOk,
)
from settings import get_db_sessionmaker
from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError


class ProductController:
    def __init__(self):
        self.db_sessionmaker = get_db_sessionmaker()

    async def get_product_by_id(self, id: int) -> Product:
        try:
            async with self.db_sessionmaker.begin() as session:
                product_entity = await session.scalar(
                    select(ProductModel).where(ProductModel.id == id)
                )
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get product") from e

        return Product(**product_entity.as_dict()) if product_entity else None

    async def get_product_list(
        self, created_date: date | None, category_id: int | None, skip: int, limit: int
    ) -> list[Product]:
        try:
            async with self.db_sessionmaker.begin() as session:
                query = select(ProductModel)
                filters = []

                if created_date is not None:
                    filters.append(ProductModel.created_date == created_date)
                if category_id is not None:
                    filters.append(ProductModel.category_id == category_id)

                if filters:
                    query = query.filter(and_(*filters))

                product_entity_list = await session.scalars(
                    query.offset(skip).limit(limit)
                )
        except DBAPIError as e:
            raise DBAPICallError(msg="can not get product list") from e

        return [
            Product(**product_entity.as_dict())
            for product_entity in product_entity_list
        ]

    async def create_product(self, product: ProductCreatingData) -> Product:
        try:
            async with self.db_sessionmaker.begin() as session:
                product_entity = ProductModel(**product.model_dump())
                session.add(product_entity)
        except IntegrityError as e:
            await session.rollback()
            raise CategoryNotFound() from e
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not create product") from e

        return Product(**product_entity.as_dict())

    async def update_product(
        self, id: int, product_changes: ProductChangingData
    ) -> ProductOperationOk:
        product = await self.get_product_by_id(id=id)
        if product is None:
            raise ProductNotFound()

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    update(ProductModel)
                    .where(ProductModel.id == id)
                    .values(**product_changes.model_dump(exclude_none=True))
                )
        except IntegrityError as e:
            await session.rollback()
            raise CategoryNotFound() from e
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not update product") from e

        return ProductOperationOk(id=product.id)

    async def delete_product(self, id: int) -> ProductOperationOk:
        product = await self.get_product_by_id(id=id)
        if product is None:
            raise ProductNotFound()

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(delete(ProductModel).where(ProductModel.id == id))
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not delete product") from e

        return ProductOperationOk(id=product.id)
