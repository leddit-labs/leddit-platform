from pydantic import BaseModel


class PostSearchResult(BaseModel):
    u_id: str
    title: str
    community_id: str | None = None
    author_id: str | None = None
    content: str | None = None
    score: float | None = None


class CommunitySearchResult(BaseModel):
    u_id: str
    name: str
    description: str | None = None
    created_by: str | None = None
    score: float | None = None