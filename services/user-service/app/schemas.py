from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserProfile(BaseModel):
    id: str
    username: str
    display_name: Optional[str]
    bio: Optional[str]
    avatar_url: Optional[str]
    post_karma: int
    comment_karma: int
    total_karma: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None