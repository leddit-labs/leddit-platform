from fastapi import FastAPI
from app.db.db_read import Base, engine
from app.queries.controller import router as vote_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vote_router)
