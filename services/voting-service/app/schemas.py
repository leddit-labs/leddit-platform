from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, field_validator


class VoteCreate(BaseModel):
    user_u_id: UUID
    value: int

    @field_validator("value")
    @classmethod
    def validate_vote_value(cls, value):
        if value not in [-1, 1]:
            raise ValueError("Vote value must be -1 or 1")
        return value


class PostVoteOut(BaseModel):
    u_id: UUID

    post_u_id: UUID
    user_u_id: UUID

    value: int

    created_at: datetime

    class Config:
        from_attributes = True


class CommentVoteOut(BaseModel):
    u_id: UUID

    comment_u_id: UUID
    user_u_id: UUID

    value: int

    created_at: datetime

    class Config:
        from_attributes = True