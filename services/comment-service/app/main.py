from fastapi import FastAPI
from neo4j.exceptions import Neo4jError

from .controller import router as comment_router
from .database import check_db_connection, init_db

app = FastAPI(title="Leddit Comment Service", version="0.1.0")
app.include_router(comment_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def health_db() -> dict[str, str]:
    try:
        connected = check_db_connection()
    except Neo4jError:
        return {"status": "error"}

    return {"status": "ok" if connected else "error"}
