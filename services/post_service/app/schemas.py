from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class PostCreate(BaseModel):
    # u_id: UUID # u_id is generated in service
    community_id: UUID
    author_id: UUID
    title: str
    content: Optional[str] = None
    # image: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    #image: Optional[str] = None


class PostOut(BaseModel):
    u_id: UUID
    title: str
    content: Optional[str]
    # image: Optional[str]
    created_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
