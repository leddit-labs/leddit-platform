import json

import pika

from app.config import settings


EXCHANGE = "leddit_events"


def _get_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(settings.rabbitmq_user, settings.rabbitmq_pass)
    params = pika.ConnectionParameters(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )
    return pika.BlockingConnection(params)


def publish_event(routing_key: str, body: dict):
    connection = _get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=routing_key,
        body=json.dumps(body),
        properties=pika.BasicProperties(
            delivery_mode=2,  # persistent
            content_type="application/json",
        ),
    )
    connection.close()


def get_consumer_channel(queue_name: str, binding_key: str):
    """Return a blocking channel bound to the given queue/routing key."""
    connection = _get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=binding_key)
    channel.basic_qos(prefetch_count=1)
    return connection, channel
