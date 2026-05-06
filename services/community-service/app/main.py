import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import get_settings
from app.grpc.server import create_grpc_server

from app.messaging.publisher import create_publisher
from app.messaging.consumer import create_consumer
from app.rest.router import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──────────────────────────────────────────────────────────────
    print("Stating community service")

    # RabbitMQ publisher
    app.state.publisher = await create_publisher(settings.rabbitmq_url)

    # RabbitMQ consumer (inbound events from other services)
    app.state.consumer = await create_consumer(settings.rabbitmq_url)
    await app.state.consumer.start()

    # gRPC server (runs alongside FastAPI in the same process)
    app.state.grpc_server = await create_grpc_server(
        port=settings.grpc_port,
        publisher=app.state.publisher,
    )

    yield

    # ── Shutdown ─────────────────────────────────────────────────────────────
    await app.state.grpc_server.stop(grace=5)
    await app.state.publisher.close()


app = FastAPI(
    title="Leddit — Community Service",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "service": settings.app_name}
