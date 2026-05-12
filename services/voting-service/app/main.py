from fastapi import FastAPI
from app.db import Base, engine
from app.controller import router as vote_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vote_router)
