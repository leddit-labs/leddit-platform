from fastapi import APIRouter, HTTPException, Query

from app.cache import get_cached, set_cached
from app.schemas import PostSearchResult, CommunitySearchResult
from app.search_index import search_posts, search_communities


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/posts", response_model=list[PostSearchResult])
def search_posts_endpoint(
    q: str = Query(..., min_length=1),
    size: int = Query(20, ge=1, le=50),
):
    cached = get_cached("posts", q, size)
    if cached is not None:
        return [PostSearchResult.model_validate(result) for result in cached]

    try:
        results = search_posts(q, size=size)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Search backend unavailable") from exc

    set_cached("posts", q, size, results)
    return [PostSearchResult.model_validate(result) for result in results]


@router.get("/communities", response_model=list[CommunitySearchResult])
def search_communities_endpoint(
    q: str = Query(..., min_length=1),
    size: int = Query(20, ge=1, le=50),
):
    cached = get_cached("communities", q, size)
    if cached is not None:
        return [CommunitySearchResult.model_validate(result) for result in cached]

    try:
        results = search_communities(q, size=size)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Search backend unavailable") from exc

    set_cached("communities", q, size, results)
    return [CommunitySearchResult.model_validate(result) for result in results]
