import asyncio
import json
import logging
import time

from app.messaging import get_consumer_channel
from app.search_index import ensure_post_index, index_post


QUEUE_NAME = "search_post_created"
BINDING_KEY = "post_created"

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
            connection, channel = get_consumer_channel(QUEUE_NAME, BINDING_KEY)
            logger.info("Connected to RabbitMQ")

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=_on_message)
            channel.start_consuming()
        except Exception:
            logger.warning("RabbitMQ not ready, retrying in %ss", RETRY_DELAY)
            time.sleep(RETRY_DELAY)
        finally:
            if connection and not connection.is_closed:
                connection.close()


def _on_message(channel, method, properties, body):
    try:
        event = json.loads(body)
        post_id = event.get("u_id")

        if not post_id:
            raise ValueError("Missing post id")

        for attempt in range(1, MAX_MESSAGE_RETRIES + 1):
            try:
                index_post(event)
                logger.info("Indexed post_created", extra={"post_id": post_id})
                channel.basic_ack(delivery_tag=method.delivery_tag) #tells rabbitmq it was success = remove message from queue
                return
            except Exception:
                logger.exception("Processing attempt failed", extra={"attempt": attempt})
                if attempt < MAX_MESSAGE_RETRIES:
                    time.sleep(attempt)

        logger.error("Failed to process message after retries; sending to DLQ", extra={"post_id": post_id})
        try:
            channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception:
        logger.exception("Failed to process message; sending to DLQ")
        try:
            channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        except Exception:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)