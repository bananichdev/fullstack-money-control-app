from api.v1 import app as api_v1
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from internal.v1 import app as internal_v1
from settings import ALLOW_ORIGIN

app = FastAPI()
app.mount("/api/v1/passport", api_v1)
app.mount("/internal/v1/passport", internal_v1)

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=[ALLOW_ORIGIN],
    allow_credentials=True,
)
