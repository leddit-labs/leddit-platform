from uuid import UUID

from sqlalchemy.orm import Session
from app.post_repository import PostRepository

from app.schemas import PostCreate, PostOut, PostUpdate
from app.models import Post

# TODO should probably be some verification in each method. check if user is logged in and all that stuff --> using other microservices

HAS_BEEN_DELETED_TEXT = (
    "This post has been deleted"  # this is returned instead of original content/title if the post is tombstoned
)


class PostService:
    def __init__(self):
        self.repo = PostRepository()

    def create_post(self, db: Session, data: PostCreate):
        post = self.repo.create(db, data)
        return self._to_out(post)

    def get_post(self, db: Session, post_u_id):
        post = self.repo.get(db, post_u_id)
        if not post:
            return None
        return self._to_out(post)

    def get_posts(self, db: Session, page: int, size: int) -> list:
        skip = (page - 1) * size
        posts = self.repo.list_posts(db, skip, size)
        return [self._to_out(p) for p in posts]

    def update_post(self, db: Session, post_u_id: UUID, update: PostUpdate) -> PostOut:
        # TODO should check if the logged in user requesting this update is the user that made the post
        post_to_update = self.repo.get(db, post_u_id)

        if not post_to_update:
            return None

        updated_post = self.repo.update(db, post_to_update, update)
        return self._to_out(updated_post)

    def delete_post(self, db: Session, post_u_id) -> PostOut:
        post = self.repo.get(db, post_u_id)
        if not post:
            return None

        deleted_post = self.repo.delete(db, post)

        return self._to_out(deleted_post)

    # helper functions below

    def _to_out(self, post: Post) -> PostOut:
        data = PostOut.model_validate(post).model_dump()

        if post.deleted_at is not None:
            data["title"] = HAS_BEEN_DELETED_TEXT
            data["content"] = HAS_BEEN_DELETED_TEXT

        return data

