from fastapi import FastAPI

from .account import router as account_router
from .auth import router as auth_router

app = FastAPI()

app.include_router(
    account_router,
    prefix="/account",
)

app.include_router(
    auth_router,
)


@app.get("/ping")
async def ping_handler() -> str:
    return f"Ping passport"
