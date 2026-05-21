from fastapi import FastAPI

from leddit_logging import setup_logging, RequestLoggingMiddleware

from app.db import Base, engine
from app.controller import router as post_router

Base.metadata.create_all(bind=engine)

logger = setup_logging("post-service")

app = FastAPI()

app.add_middleware(RequestLoggingMiddleware)
app.include_router(post_router)
