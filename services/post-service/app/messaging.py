import json
import pika

from app.config import settings


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


def publish_event(routing_key: str, message: dict):
    connection = _get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange="leddit_events", exchange_type="topic", durable=True)
    channel.basic_publish(
        exchange="leddit_events",
        routing_key=routing_key,
        body=json.dumps(message, default=str),
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    connection.close()


def get_consumer_channel(queue_name: str, binding_keys):
    connection = _get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange="leddit_events", exchange_type="topic", durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    if isinstance(binding_keys, (list, tuple, set)):
        for binding_key in binding_keys:
            channel.queue_bind(exchange="leddit_events", queue=queue_name, routing_key=binding_key)
    else:
        channel.queue_bind(exchange="leddit_events", queue=queue_name, routing_key=binding_keys)
    channel.basic_qos(prefetch_count=1)
    return connection, channel
