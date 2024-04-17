from typing import Annotated

from datetime import date

from fastapi import APIRouter, status, Depends

from database.controllers.product import ProductController
from schemas.v1 import ProductCreatingData, Product, ProductOperationOk, ProductChangingData

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_product_list_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    created_date: date | None,
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Product]:
    pass


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_by_id_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    id: int,
) -> Product:
    return await controller.get_product_by_id(id=id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_products_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    product: ProductCreatingData,
) -> Product:
    return await controller.create_product(product=product)


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def put_product_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    id: int,
    product_changes: ProductChangingData,
) -> ProductOperationOk:
    return await controller.update_product(id=id, product_changes=product_changes)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_category_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    id: int,
) -> ProductOperationOk:
    return await controller.delete_product(id=id)
