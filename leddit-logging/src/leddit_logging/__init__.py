"""
leddit-logging: Shared structured logging for Leddit microservices.

Usage:
    from leddit_logging import setup_logging, RequestLoggingMiddleware

    logger = setup_logging("my-service")

    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)
"""

from .config import setup_logging, request_id_ctx
from .middleware import RequestLoggingMiddleware
from .context import get_request_id, set_request_id

__all__ = [
    "setup_logging",
    "RequestLoggingMiddleware",
    "request_id_ctx",
    "get_request_id",
    "set_request_id",
]
