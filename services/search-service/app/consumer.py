import asyncio
import json
import logging
import time
from typing import Callable

from app.messaging import get_consumer_channel
from app.search_index import (
    ensure_post_index,
    index_post,
    delete_post,
    ensure_community_index,
    index_community,
    delete_community,
)


QUEUE_NAME = "search_events"
BINDING_KEYS = [
    "post_created",
    "post_updated",
    "post_deleted",
    "community_created",
    "community_updated",
    "community_deleted",
]

RETRY_DELAY = 10
MAX_MESSAGE_RETRIES = 3


logger = logging.getLogger(__name__)


async def start_consumer():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _consume_loop)


def _consume_loop():
    while True:
        connection = None
        try:
            ensure_post_index()
            ensure_community_index()
            connection, channel = get_consumer_channel(QUEUE_NAME, BINDING_KEYS)
            logger.info("Connected to RabbitMQ")

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=_on_message)
            channel.start_consuming()
        except Exception:
            logger.warning("RabbitMQ not ready, retrying in %ss", RETRY_DELAY)
            time.sleep(RETRY_DELAY)
        finally:
            if connection and not connection.is_closed:
                connection.close()


def _reject_dlq(channel, method):
    try:
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
    except Exception:
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def _process_with_retries(channel, method, handler: Callable[[dict], None], event: dict):
    for attempt in range(1, MAX_MESSAGE_RETRIES + 1):
        try:
            handler(event)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return
        except Exception:
            logger.exception("Handler attempt failed", extra={"attempt": attempt})
            if attempt < MAX_MESSAGE_RETRIES:
                time.sleep(attempt)

    logger.error("Handler failed after retries; sending to DLQ")
    _reject_dlq(channel, method)


def _on_message(channel, method, properties, body):
    routing_key = getattr(method, "routing_key", None)
    try:
        event = json.loads(body)
    except Exception:
        logger.exception("Invalid JSON in message; sending to DLQ")
        _reject_dlq(channel, method)
        return

    if routing_key in ("post_created", "post_updated"):
        _process_with_retries(channel, method, lambda ev: index_post(ev), event)
        return

    if routing_key == "post_deleted":
        def _del(ev: dict):
            u_id = ev.get("u_id")
            if not u_id:
                raise ValueError("missing u_id")
            delete_post(u_id)

        _process_with_retries(channel, method, _del, event)
        return

    if routing_key in ("community_created", "community_updated"):
        _process_with_retries(channel, method, lambda ev: index_community(ev), event)
        return

    if routing_key == "community_deleted":
        def _cdel(ev: dict):
            u_id = ev.get("u_id")
            if not u_id:
                raise ValueError("missing u_id")
            delete_community(u_id)

        _process_with_retries(channel, method, _cdel, event)
        return

    logger.warning("Unhandled routing key; acking", extra={"routing_key": routing_key})
    channel.basic_ack(delivery_tag=method.delivery_tag)