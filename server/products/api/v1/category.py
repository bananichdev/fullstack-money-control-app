from typing import Annotated

from fastapi import APIRouter, status, Depends

from database.controllers.category import CategoryController
from schemas.v1 import Category, CategoryOperationOk

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_category_list_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
) -> list[Category]:
    return await controller.get_category_list()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_category_by_id_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    id: int,
) -> Category:
    return await controller.get_category_by_id(id=id)


@router.post("/{name}", status_code=status.HTTP_201_CREATED)
async def post_category_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    name: str,
) -> Category:
    return await controller.create_category(name=name)


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def put_category_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    id: int,
    new_name: str,
) -> CategoryOperationOk:
    return await controller.update_category(id=id, new_name=new_name)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_category_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    id: int,
) -> CategoryOperationOk:
    return await controller.delete_category(id=id)
