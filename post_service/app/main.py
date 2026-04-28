from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.schemas import PostCreate, PostUpdate, PostOut
from app.post_service import PostService

Base.metadata.create_all(bind=engine)

app = FastAPI()
service = PostService()

#todo find a way to define the /posts a global space

@app.post("/posts", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    #TODO should notify the integrity service to check this new post via rabbitMQ
    return service.create_post(db, post)


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: str, db: Session = Depends(get_db)):
    post = service.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404)
    return post


@app.get("/posts", response_model=list[PostOut])
def get_posts(page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    return service.get_posts(db, page, size)


@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: str, update: PostUpdate, db: Session = Depends(get_db)):
    post = service.update_post(db, post_id, update)
    if not post:
        raise HTTPException(status_code=404)
    return post


@app.delete("/posts/{post_u_id}", response_model=PostOut)
def delete_post(post_u_id: UUID, db: Session = Depends(get_db)):
    post = service.delete_post(db, post_u_id)
    if not post:
        raise HTTPException(status_code=404)
    return post
