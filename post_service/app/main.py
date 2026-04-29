from fastapi import FastAPI
from app.db import Base, engine
from app.controller import router as post_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post_router)
