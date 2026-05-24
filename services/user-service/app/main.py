from fastapi import FastAPI
from contextlib import asynccontextmanager

from leddit_logging import setup_logging, RequestLoggingMiddleware

from app.database import init_db
from app.routes import router

logger = setup_logging("user-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Leddit User Service", lifespan=lifespan)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
