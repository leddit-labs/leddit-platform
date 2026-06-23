from datetime import datetime
from uuid import UUID

import strawberry

from app.post_service import PostService
from app.db import SessionLocal

service = PostService()

@strawberry.type
class PostType:
    u_id: UUID
    title: str
    content: str | None
    community_id: UUID
    author_id: UUID
    created_at: datetime

@strawberry.type
class Query:
    @strawberry.field
    def posts(
        self,
        page: int = 1,
        size: int = 20
    ) -> list[PostType]:

        db = SessionLocal()

        try:
            posts = service.get_posts(db, page, size)

            return [
                PostType(
                    u_id=(post["u_id"]),
                    title=post["title"],
                    content=post["content"],
                    community_id=(post["community_id"]),
                    author_id=(post["author_id"]),
                    created_at=post["created_at"]
                )
                for post in posts
            ]

        finally:
            db.close()
schema = strawberry.Schema(query=Query)