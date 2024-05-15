from datetime import date
from typing import Annotated

from database.controllers.product import ProductController
from fastapi import APIRouter, Depends, status
from schemas.v1 import Product, ProductChangingData, ProductCreatingData, ProductOperationOk
from utils.auth import authenticate
from utils.internal import write_off_balance

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_product_list_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    owner_id: Annotated[int, Depends(authenticate)],
    created_date: date | None = None,
    category_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[Product]:
    return await controller.get_product_list(
        created_date=created_date,
        category_id=category_id,
        skip=skip,
        limit=limit,
        owner_id=owner_id,
    )


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_by_id_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    owner_id: Annotated[int, Depends(authenticate)],
    id: int,
) -> Product | None:
    return await controller.get_product_by_id(id=id, owner_id=owner_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_products_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    owner_id: Annotated[int, Depends(authenticate)],
    product: ProductCreatingData,
) -> Product:
    await write_off_balance(owner_id=owner_id, amount=product.price)
    product = await controller.create_product(product=product, owner_id=owner_id)

    return product


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def put_product_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    owner_id: Annotated[int, Depends(authenticate)],
    id: int,
    product_changes: ProductChangingData,
) -> ProductOperationOk:
    return await controller.update_product(
        id=id, product_changes=product_changes, owner_id=owner_id
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_category_handler(
    controller: Annotated[ProductController, Depends(ProductController)],
    owner_id: Annotated[int, Depends(authenticate)],
    id: int,
) -> ProductOperationOk:
    return await controller.delete_product(id=id, owner_id=owner_id)
