import datetime

from sqlalchemy.orm import Session
from app.models import Post
from app.schemas import PostCreate


class PostRepository:
    def create(self, db: Session, data: PostCreate) -> Post:
        post = Post(**data)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def get(self, db: Session, post_id):
        return db.query(Post).filter(Post.id == post_id).first()

    def list_posts(self, db: Session, skip: int, limit: int):
        return (
            db.query(Post)
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, db: Session, post: Post, data: dict):
        for key, value in data.items():
            setattr(post, key, value)

        db.commit()
        db.refresh(post)
        return post

    def delete(self, db: Session, post: Post):
        post.deleted_at = datetime.now()
        db.commit()
        db.refresh(post)
        return post