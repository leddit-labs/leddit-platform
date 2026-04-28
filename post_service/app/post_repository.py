import datetime

from sqlalchemy.orm import Session
from app.models import Post
from app.schemas import PostCreate, PostOut


class PostRepository:
    def create(self, db: Session, data: PostCreate) -> Post:
        # **means unpacking from dict. mapping it to the Post object.
        post = Post(**data)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def get(self, db: Session, post_u_id) -> PostOut:
        # todo if tombstones, then return something else? - maybe not smart to return the whole object if tombstoned
        return db.query(Post).filter(Post.u_id == post_u_id).first()

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
        post.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(post)
        return post
