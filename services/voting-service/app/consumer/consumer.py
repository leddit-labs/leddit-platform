import asyncio
import json
import time

from app.db.db_read import SessionLocal
from app.consumer.consumer_util import get_consumer_channel


from app.consumer.consumer_service import (
    ConsumerService,
)


QUEUE_NAME = "vote_projection"

BINDING_KEYS = [
    "vote.post.changed",
    "vote.comment.changed",
]

MAX_RETRIES = 5
RETRY_DELAY = 5

service = ConsumerService()


async def start_consumer():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _consume_loop)


def _consume_loop():

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            connection, channel = get_consumer_channel(
                QUEUE_NAME,
                "vote.#",
            )

            print(f"Connected to RabbitMQ (attempt {attempt})")

            channel.basic_qos(prefetch_count=1)

            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=_on_message,
            )

            print("Waiting for vote events...")

            channel.start_consuming()

        except Exception as e:
            print(f"RabbitMQ connection failed (attempt {attempt}/{MAX_RETRIES})")

            print(e)

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

            else:
                raise


def _on_message(channel, method, properties, body):

    db = SessionLocal()

    try:
        event = json.loads(body)

        routing_key = method.routing_key

        print(f"Received: {routing_key}")

        if routing_key == "vote.post.changed":
            service.apply_post_vote(
                db=db,
                post_id=event["post_id"],
                user_id=event["user_id"],
                #old_value=event["old_value"],
                new_value=event["new_value"],
            )

        elif routing_key == "vote.comment.changed":
            service.apply_comment_vote(
                db=db,
                comment_id=event["comment_id"],
                user_id=event["user_id"],
                #old_value=event["old_value"],
                new_value=event["new_value"],
            )

        channel.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("Error processing message")
        print(e)

        channel.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True,
        )

    finally:
        db.close()
