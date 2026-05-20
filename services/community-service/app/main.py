from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.router import router

app = FastAPI(title=settings.app_name)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
