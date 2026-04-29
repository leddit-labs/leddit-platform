from datetime import datetime

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    post_id: str = Field(min_length=1, max_length=64)
    parent_id: int | None = None
    author_id: str = Field(min_length=1, max_length=64)
    content: str = Field(min_length=1, max_length=5000)


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class CommentResponse(BaseModel):
    id: int
    u_id: str
    post_id: str
    parent_id: int | None
    author_id: str
    content: str
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    model_config = {"from_attributes": True}
