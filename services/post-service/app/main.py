from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql import schema
from leddit_logging import setup_logging, RequestLoggingMiddleware

from app.db import Base, engine
from app.controller import router as post_router

from app.consumer import start_consumer
import asyncio

Base.metadata.create_all(bind=engine)

logger = setup_logging("post-service")

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(RequestLoggingMiddleware)
app.include_router(post_router)


@app.on_event("startup")
async def start_verdict_consumer():
    asyncio.create_task(start_consumer())


@app.get("/health")
def health():
    return {"status": "ok"}
