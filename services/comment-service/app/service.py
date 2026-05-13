from .models import Comment
from .repository import CommentRepository
from .schemas import CommentCreate, CommentResponse, CommentUpdate


class CommentService:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def get_comment_raw(self, comment_id: int):
        return self.repository.get_by_id(comment_id)

    def get_comment_by_id(self, comment_id: int):
        comment = self.repository.get_by_id(comment_id)
        return self._to_out(comment)

    def create_comment(self, payload: CommentCreate):
        comment = self.repository.create(
            post_id=payload.post_id,
            parent_id=payload.parent_id,
            author_id=payload.author_id,
            content=payload.content,
        )
        return self._to_out(comment)

    def list_comments_for_post(self, post_id: str):
        comments = self.repository.list_by_post_id(post_id)
        return [self._to_out(c) for c in comments]

    def update_comment(self, comment: Comment, payload: CommentUpdate):
        updated_comment = self.repository.update_content(comment, payload.content)
        return self._to_out(updated_comment)

    def delete_comment(self, comment: Comment):
        deleted_comment = self.repository.soft_delete(comment)
        return self._to_out(deleted_comment)

    def _to_out(self, comment: Comment) -> dict:
        data = CommentResponse.model_validate(comment).model_dump()

        if comment.deleted_at is not None:
            data["content"] = "This comment has been deleted"

        return data