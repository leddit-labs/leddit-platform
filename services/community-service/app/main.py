from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from leddit_logging import setup_logging, RequestLoggingMiddleware

from app.config import settings
from app.router import router

logger = setup_logging("community-service")

app = FastAPI(title=settings.app_name)

Instrumentator().instrument(app).expose(app)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(router)

@app.on_event("startup")
async def startup():
    logger.info("community-service is ready")

@app.get("/health")
def health():
    return {"status": "ok"}
