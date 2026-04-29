from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comment:
    id: int
    u_id: str
    post_id: str
    parent_id: int | None
    author_id: str
    content: str
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None
