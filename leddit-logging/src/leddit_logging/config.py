"""
Structured JSON logging configuration.

Produces one JSON object per log line — exactly what Loki/Promtail expects.
Also works great with kubectl logs, docker logs, and any log aggregator.
"""

import logging
import sys
import json
from datetime import datetime, timezone
from typing import Any

from .context import request_id_ctx

KNOWN_EXTRA_FIELDS = frozenset({
    "user_id",
    "post_id",
    "comment_id",
    "community_id",
    "method",
    "path",
    "status_code",
    "duration_ms",
    "client_ip",
    "content_length",
})


class JSONFormatter(logging.Formatter):

    def __init__(self, service_name: str, extra_fields: frozenset[str] | None = None):
        super().__init__()
        self.service_name = service_name
        self.extra_fields = extra_fields or KNOWN_EXTRA_FIELDS

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": self.service_name,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_ctx.get("-"),
        }

        # Attach exceptions
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)
            log_entry["exception_type"] = record.exc_info[0].__name__

        # Attach extra fields passed via extra={...}
        for key in self.extra_fields:
            val = getattr(record, key, None)
            if val is not None:
                log_entry[key] = val

        return json.dumps(log_entry, default=str)


def setup_logging(
    service_name: str,
    level: str = "INFO",
    extra_fields: frozenset[str] | None = None,
    suppress: dict[str, str] | None = None,
) -> logging.Logger:
    all_fields = KNOWN_EXTRA_FIELDS | (extra_fields or frozenset())

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    root.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(service_name, extra_fields=all_fields))
    root.addHandler(handler)

    defaults = {
        "uvicorn.access": "WARNING",
        "uvicorn.error": "INFO",
        "sqlalchemy.engine": "WARNING",
        "httpcore": "WARNING",
        "httpx": "WARNING",
        "aio_pika": "WARNING",
    }
    for logger_name, logger_level in (suppress or defaults).items():
        logging.getLogger(logger_name).setLevel(
            getattr(logging, logger_level.upper(), logging.WARNING)
        )

    return root
