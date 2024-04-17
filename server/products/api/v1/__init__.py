from fastapi import FastAPI

from .category import router as category_router
from .product import router as product_router

app = FastAPI()

app.include_router(
    category_router,
    prefix="/category",
)

app.include_router(
    product_router,
    prefix="/product",
)


@app.get("/ping")
async def ping_handler() -> str:
    return f"Ping products"
