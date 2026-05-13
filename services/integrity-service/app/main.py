import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.consumer import start_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("starting integrity consumer")
    consumer_task = asyncio.create_task(start_consumer())
    yield
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        print("consumer task cancelled")


app = FastAPI(title="Integrity Service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}
