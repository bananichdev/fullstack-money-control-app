import uvicorn
from api.v1 import app as api_v1
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import ALLOW_ORIGIN, HOST, PORT

app = FastAPI()
app.mount("/api/v1/products", api_v1)

app.add_middleware(
    CORSMiddleware,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=[ALLOW_ORIGIN],
    allow_credentials=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT)
