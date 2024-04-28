from typing import Annotated

from database.controllers.category import CategoryController
from fastapi import APIRouter, Depends, status
from schemas.v1 import Category, CategoryCreatingData, CategoryOperationOk
from utils.auth import authenticate

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_category_list_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    owner_id: Annotated[int, Depends(authenticate)],
) -> list[Category]:
    return await controller.get_category_list(owner_id=owner_id)


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_category_by_id_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    owner_id: Annotated[int, Depends(authenticate)],
    id: int,
) -> Category | None:
    return await controller.get_category_by_id(id=id, owner_id=owner_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_category_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    owner_id: Annotated[int, Depends(authenticate)],
    category: CategoryCreatingData,
) -> Category:
    return await controller.create_category(category=category, owner_id=owner_id)


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def put_category_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    owner_id: Annotated[int, Depends(authenticate)],
    id: int,
    new_name: str,
) -> CategoryOperationOk:
    return await controller.update_category(id=id, new_name=new_name, owner_id=owner_id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_category_handler(
    controller: Annotated[CategoryController, Depends(CategoryController)],
    owner_id: Annotated[int, Depends(authenticate)],
    id: int,
) -> CategoryOperationOk:
    return await controller.delete_category(id=id, owner_id=owner_id)
