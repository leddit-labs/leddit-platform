from fastapi import FastAPI
from app.db.db_write import Base, engine
from app.commands.controller import router as vote_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(vote_router)
