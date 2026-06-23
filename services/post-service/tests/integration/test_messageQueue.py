import json
import time
import pika
import pytest
from uuid import uuid4


@pytest.mark.integration
def test_create_post_publishes_event(client, rabbitmq_container):
    # Set up a temporary test queue to listen for the post_created event
    queue_name = f"test-{uuid4()}"
    connection = pika.BlockingConnection(rabbitmq_container.get_connection_params())
    channel = connection.channel()

    try:
        channel.queue_declare(queue=queue_name, durable=False, auto_delete=True)
        channel.exchange_declare(exchange="leddit_events", exchange_type="topic", durable=True)
        channel.queue_bind(
            exchange="leddit_events",
            queue=queue_name,
            routing_key="post_created",
        )

        # Create a post via the API (real service logic, but the DB is mocked)
        community_id = uuid4()
        author_id = uuid4()
        response = client.post(
            "/posts",
            json={
                "community_id": str(community_id),
                "author_id": str(author_id),
                "title": "Integration test post",
                "content": "This post should trigger an event",
            },
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        post_id = response.json()["u_id"]

        # Wait for and consume the message from the test queue
        message_body = None
        for _ in range(15):
            _, _, body = channel.basic_get(queue=queue_name, auto_ack=True)
            if body:
                message_body = body
                break
            time.sleep(0.5)

        assert message_body is not None, "No message received on the queue"

        # Check that the consumed event matches the post created
        payload = json.loads(message_body)
        assert payload["u_id"] == post_id
        assert payload["title"] == "Integration test post"
        assert payload["community_id"] == str(community_id)
        assert payload["author_id"] == str(author_id)
        assert payload["content"] == "This post should trigger an event"

    finally:
        # Clean up the connection
        channel.close()
        connection.close()