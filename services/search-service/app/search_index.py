import json
from elasticsearch import Elasticsearch

from app.config import settings


POST_INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "u_id": {"type": "keyword"},
            "title": {"type": "text"},
            "community_id": {"type": "keyword"},
            "author_id": {"type": "keyword"},
            "content": {"type": "text"},
        }
    }
}


def get_client() -> Elasticsearch:
    return Elasticsearch(settings.elasticsearch_url)


def ensure_post_index(client: Elasticsearch | None = None) -> Elasticsearch:
    es = client or get_client()
    if not es.indices.exists(index=settings.elasticsearch_index):
        es.indices.create(index=settings.elasticsearch_index, **POST_INDEX_MAPPING)
    return es


def index_post(document: dict, client: Elasticsearch | None = None) -> None:
    es = client or ensure_post_index()
    es.index(
        index=settings.elasticsearch_index,
        id=document["u_id"],
        document=document,
        refresh="wait_for",
    )


def search_posts(query: str, size: int = 20, client: Elasticsearch | None = None) -> list[dict]:
    es = client or ensure_post_index()
    response = es.search(
        index=settings.elasticsearch_index,
        size=size,
        query={"match_phrase_prefix": {"title": {"query": query}}},
    )
    hits = response.get("hits", {}).get("hits", [])
    results: list[dict] = []
    for hit in hits:
        source = hit.get("_source", {})
        source["score"] = hit.get("_score")
        results.append(source)
    return results