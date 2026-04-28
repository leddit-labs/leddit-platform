from datetime import datetime, timezone

from sqlalchemy.orm import Session
from app.models import Post
from app.schemas import PostCreate, PostUpdate


class PostRepository:
    def create(self, db: Session, data: PostCreate) -> Post:
        post = Post(**data.model_dump())
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    def get(self, db: Session, post_u_id) -> Post:
        return db.query(Post).filter(Post.u_id == post_u_id).first()

    def list_posts(self, db: Session, skip: int, limit: int):
        #TODO this can be approved alot if we want - by community and author id and so on. maybe using the voting service to rank them and so on 
        return (
            db.query(Post)
            .filter(Post.deleted_at.is_(None)) # don't return deleted posts - filter these out
            .order_by(Post.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
    )

    def update(self, db: Session, post: Post, update: PostUpdate) -> Post:
        post_update = update.model_dump(exclude_unset=True)

        #iterates over PostUpdate object fields and overwrites with new info
        for key, value in post_update.items():
            setattr(post, key, value)

        db.commit()
        db.refresh(post)
        return post

    def delete(self, db: Session, post: Post) -> Post:
        # using the same timezone for consistency if this microservice is scaled and deployed over different timezones
        post.deleted_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(post)
        return post
