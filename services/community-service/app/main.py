from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
