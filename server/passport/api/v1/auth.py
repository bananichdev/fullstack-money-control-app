from fastapi import APIRouter, status

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_handler():
    pass


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_handler():
    pass
