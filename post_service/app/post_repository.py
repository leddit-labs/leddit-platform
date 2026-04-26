from sqlalchemy.orm import Session
from app.models import Post


class PostRepository:
    def create(self, db: Session, data: dict) -> Post:
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
            .filter(Post.deleted_at == None)
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
