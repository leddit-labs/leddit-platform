import json
import pika

from app.config import settings


EXCHANGE_NAME = "leddit_events"


def publish_event(routing_key: str, message: dict):
    connection = pika.BlockingConnection(pika.URLParameters(settings.rabbitmq_url))
    channel = connection.channel()
    channel.exchange_declare(
        exchange=EXCHANGE_NAME, exchange_type="topic", durable=True
    )
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=json.dumps(message, default=str),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()
