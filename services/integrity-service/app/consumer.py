import asyncio
import json
import time

from app.messaging import get_consumer_channel, publish_event
from app.moderation import moderate_post


QUEUE_NAME = "integrity_post_created"
BINDING_KEY = "post_created"

MAX_RETRIES = 5
RETRY_DELAY = 5 # seconds

async def start_consumer():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _consume_loop)

def _consume_loop():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            connection, channel = get_consumer_channel(QUEUE_NAME, BINDING_KEY)
            print(f"Connected to RabbitMQ (attempt {attempt}). Waiting for messages...")

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=_on_message)

            channel.start_consuming()
        except Exception:
            print(f"RabbitMQ connection failed (attempt {attempt}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                print("Max retries reached. Consumer exiting")
                raise


def _on_message(channel, method, properties, body):
    try:
        event = json.loads(body)
        post_id = event.get("u_id")
        title = event.get("title", "")
        content = event.get("content")
 
        print(f"Received post_created for post {post_id}")
 
        is_accepted = moderate_post(title, content)
 
        result_event = {
            "u_id": post_id,
            "community_id": event.get("community_id"),
            "author_id": event.get("author_id"),
            "title": title,
        }
 
        if is_accepted:
            publish_event("post_accepted", result_event)
            print(f"Post {post_id} ACCEPTED")
        else:
            publish_event("post_denied", result_event)
            print(f"Post {post_id} DENIED")
 
        channel.basic_ack(delivery_tag=method.delivery_tag)
 
    except Exception:
        print("Error processing message")
        # nack and requeue so we don't lose the message
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

