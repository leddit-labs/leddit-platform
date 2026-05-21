import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from leddit_logging import setup_logging, RequestLoggingMiddleware

from app.consumer import start_consumer

logger = setup_logging("integrity-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting integrity consumer")
    consumer_task = asyncio.create_task(start_consumer())
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        logger.warning("consumer task cancelled")


app = FastAPI(title="Integrity Service", lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)

@app.get("/health")
def health():
    return {"status": "ok"}
