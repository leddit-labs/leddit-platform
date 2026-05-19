import json
import pika

from app.config import settings


def publish_event(routing_key: str, message: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=settings.rabbitmq_port,
        )
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="leddit_events", exchange_type="topic", durable=True)
    channel.basic_publish(
        exchange="leddit_events",
        routing_key=routing_key,
        body=json.dumps(message, default=str),
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    connection.close()
