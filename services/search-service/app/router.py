from fastapi import APIRouter, HTTPException, Query

from app.schemas import PostSearchResult
from app.search_index import search_posts


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/posts", response_model=list[PostSearchResult])
def search_posts_endpoint(
    q: str = Query(..., min_length=1),
    size: int = Query(20, ge=1, le=50),
):
    try:
        results = search_posts(q, size=size)
        return [PostSearchResult.model_validate(result) for result in results]
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Search backend unavailable") from exc