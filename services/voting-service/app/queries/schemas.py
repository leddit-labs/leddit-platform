from pydantic import BaseModel
from uuid import UUID


class PostVoteSummaryOut(BaseModel):
    post_id: UUID
    upvotes: int
    downvotes: int
    score: int

    class Config:
        from_attributes = True


class CommentVoteSummaryOut(BaseModel):
    comment_id: UUID
    upvotes: int
    downvotes: int
    score: int

    class Config:
        from_attributes = True


class UserVoteOut(BaseModel):
    value: int