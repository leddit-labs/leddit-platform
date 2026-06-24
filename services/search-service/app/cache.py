import json
import logging
from functools import lru_cache

import redis

from app.config import settings


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_redis() -> redis.Redis:
    return redis.Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=1,
        socket_timeout=1,
    )


def _gen_key(kind: str) -> str:
    return f"search:{kind}:gen"


def _current_gen(client: redis.Redis, kind: str) -> int:
    gen = client.get(_gen_key(kind))
    return int(gen) if gen is not None else 0


def _result_key(kind: str, gen: int, query: str, size: int) -> str:
    normalized = query.strip().lower()
    return f"search:{kind}:v{gen}:s{size}:{normalized}"


def get_cached(
    kind: str,
    query: str,
    size: int,
    client: redis.Redis | None = None,
) -> list[dict] | None:
    if not settings.cache_enabled:
        return None
    try:
        r = client or get_redis()
        gen = _current_gen(r, kind)
        raw = r.get(_result_key(kind, gen, query, size))
        return json.loads(raw) if raw is not None else None
    except Exception:
        logger.warning("cache read failed; bypassing cache", exc_info=True)
        return None


def set_cached(
    kind: str,
    query: str,
    size: int,
    results: list[dict],
    client: redis.Redis | None = None,
) -> None:
    if not settings.cache_enabled:
        return
    try:
        r = client or get_redis()
        gen = _current_gen(r, kind)
        r.set(
            _result_key(kind, gen, query, size),
            json.dumps(results),
            ex=settings.cache_ttl_seconds,
        )
    except Exception:
        logger.warning("cache write failed; continuing", exc_info=True)


def invalidate(kind: str, client: redis.Redis | None = None) -> None:
    if not settings.cache_enabled:
        return
    try:
        r = client or get_redis()
        r.incr(_gen_key(kind))
    except Exception:
        logger.warning(
            "cache invalidation failed; stale results may persist until TTL",
            exc_info=True,
        )
