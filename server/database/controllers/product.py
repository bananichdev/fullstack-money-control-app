from sqlalchemy import select, delete, update
from sqlalchemy.exc import DBAPIError, IntegrityError

from database.connection import get_db_sessionmaker
from database.models import ProductModel
from schemas.v1 import Product, ProductCreatingData, DBAPICallError, ProductOperationOk, ProductNotFound, \
    ProductChangingData, CategoryNotFound


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

        if product_entity is None:
            raise ProductNotFound()

        return Product(**product_entity.as_dict())

    async def get_product_list(self) -> list[Product]:
        pass

    async def create_product(self, product: ProductCreatingData) -> Product:
        try:
            async with self.db_sessionmaker.begin() as session:
                product_entity = ProductModel(**product.model_dump())
                session.add(product_entity)
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not create product") from e

        return Product(**product_entity.as_dict())

    async def update_product(self, id: int, product_changes: ProductChangingData) -> ProductOperationOk:
        product = await self.get_product_by_id(id=id)

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    update(ProductModel)
                    .where(ProductModel.id == product.id)
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

        try:
            async with self.db_sessionmaker.begin() as session:
                await session.execute(
                    delete(ProductModel).where(ProductModel.id == product.id)
                )
        except DBAPIError as e:
            await session.rollback()
            raise DBAPICallError(msg="can not delete product") from e

        return ProductOperationOk(id=product.id)
