import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from leddit_logging import setup_logging, RequestLoggingMiddleware

from app.consumer import start_consumer
from app.config import settings
from app.router import router

logger = setup_logging("search-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting search consumer")
    consumer_task = asyncio.create_task(start_consumer())
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        logger.warning("consumer task cancelled")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
