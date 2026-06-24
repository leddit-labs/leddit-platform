import asyncio
import json
import time
from uuid import UUID
from datetime import datetime, timezone

from app.db import SessionLocal
from app.messaging import publish_event
from app.messaging import get_consumer_channel
from app.models import Post


QUEUE_NAME = "post_service_verdicts"
ROUTING_KEYS = ["post_accepted", "post_denied"]

RETRY_DELAY = 5
 

async def start_consumer():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _consume_loop)


def _consume_loop():
    attempt = 1
    while True:
        try:
            connection, channel = get_consumer_channel(QUEUE_NAME, ROUTING_KEYS)

            print(f"Connected to RabbitMQ (attempt {attempt}). Waiting for verdict messages...")
            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=_on_message)
            channel.start_consuming()
        except Exception as exc:
            print(f"RabbitMQ connection failed (attempt {attempt}): {exc}")
            print(f"Retrying verdict consumer in {RETRY_DELAY} seconds")
            time.sleep(RETRY_DELAY)
            attempt += 1


def _on_message(channel, method, properties, body):
    db = SessionLocal()
    try:
        event = json.loads(body)
        post_u_id = UUID(event.get("u_id"))
        post = db.query(Post).filter(Post.u_id == post_u_id).first()

        if not post:
            print(f"Post {post_u_id} not found")
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return

        if method.routing_key == "post_accepted":
            post.status = "accepted"
            db.commit()
            db.refresh(post)
            print(f"Post {post_u_id} ACCEPTED")
        elif method.routing_key == "post_denied":
            post.status = "denied"
            post.deleted_at = post.deleted_at or datetime.now(timezone.utc)
            db.commit()
            db.refresh(post)
            publish_event(
                "post_deleted",
                {
                    "u_id": str(post.u_id),
                },
            )
            print(f"Post {post_u_id} DENIED")

        channel.basic_ack(delivery_tag=method.delivery_tag)
    except Exception:
        db.rollback()
        print("Error processing verdict message")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    finally:
        db.close()