from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql import schema
from leddit_logging import setup_logging, RequestLoggingMiddleware

from app.db import Base, engine
from app.controller import router as post_router

Base.metadata.create_all(bind=engine)

logger = setup_logging("post-service")

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

app.add_middleware(RequestLoggingMiddleware)
app.include_router(post_router)


@app.get("/health")
def health():
    return {"status": "ok"}
