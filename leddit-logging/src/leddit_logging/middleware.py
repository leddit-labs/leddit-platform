"""
FastAPI middleware that:
- Forwards X-Request-ID from the API gateway
- Logs every request with method, path, status code, and duration
- Sets the request ID in the response headers for client-side correlation
"""

import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .context import request_id_ctx

logger = logging.getLogger("leddit_logging.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: set[str] | None = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or {"/health", "/ready"}

    async def dispatch(self, request: Request, call_next) -> Response:
        # Bye bye noisy crap from /health
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request_id_ctx.set(req_id)

        start = time.perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Request-ID"] = req_id
            return response

        except Exception as exc:
            logger.error(
                f"Unhandled exception on {request.method} {request.url.path}",
                extra={
                    "method": request.method,
                    "path": str(request.url.path),
                    "client_ip": request.client.host if request.client else None,
                },
                exc_info=exc,
            )
            raise

        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                f"{request.method} {request.url.path} → {status_code} ({duration_ms}ms)",
                extra={
                    "method": request.method,
                    "path": str(request.url.path),
                    "status_code": status_code,
                    "duration_ms": duration_ms,
                    "client_ip": request.client.host if request.client else None,
                },
            )
