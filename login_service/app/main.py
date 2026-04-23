from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql import schema
from app.db import engine, Base

app = FastAPI(title="Login Service")

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/health")
async def health():
    return {"status": "ok"}