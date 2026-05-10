from fastapi import HTTPException

from .repository import CommentRepository
from .schemas import CommentCreate, CommentUpdate


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def create_comment(self, payload: CommentCreate):
        if payload.parent_id is not None:
            parent = self.repository.get_by_u_id(payload.parent_id)
            if parent is None:
                raise HTTPException(status_code=400, detail="Parent comment does not exist")
            if parent.post_id != payload.post_id:
                raise HTTPException(status_code=400, detail="Parent comment belongs to another post")

        return self.repository.create(
            post_id=payload.post_id,
            parent_id=payload.parent_id,
            author_id=payload.author_id,
            content=payload.content,
        )

    def get_comment(self, comment_id: int):
        comment = self.repository.get_by_id(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    def list_comments_for_post(self, post_id: str):
        return self.repository.list_by_post_id(post_id)

    def update_comment(self, comment_id: int, payload: CommentUpdate):
        comment = self.get_comment(comment_id)
        if comment.deleted_at is not None:
            raise HTTPException(status_code=409, detail="Deleted comments cannot be edited")

        return self.repository.update_content(comment, payload.content)

    def delete_comment(self, comment_id: int):
        comment = self.get_comment(comment_id)
        if comment.deleted_at is not None:
            return comment

        return self.repository.soft_delete(comment)
