from sqlalchemy.orm import Session

from app.schemas import PostCreate, PostUpdate
from app.post_repository import PostRepository


# TODO should probably be some verification in each method. check if user is logged in and all that stuff --> using other microservices
class PostService:
    def __init__(self):
        self.repo = PostRepository()

    def create_post(self, db: Session, data: PostCreate):
        post = self.repo.create(db, data)
        return post

    def get_post(self, db: Session, post_id):
        return self.repo.get(db, post_id)

    def get_posts(self, db: Session, page: int, size: int):
        skip = (page - 1) * size
        return self.repo.list_posts(db, skip, size)

    def update_post(self, db: Session, post_id, update: PostUpdate):
        post = self.repo.get(db, post_id)
        if not post:
            return None

        return self.repo.update(db, post, update.dict(exclude_unset=True))

    def delete_post(self, db: Session, post_id):
        post = self.repo.get(db, post_id)
        if not post:
            return None

        return self.repo.delete(db, post)
