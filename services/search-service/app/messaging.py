import pika

from app.config import settings


EXCHANGE = "leddit_events"
DLX_EXCHANGE = "leddit_events.dlx"
DLQ_NAME = "search_events.dlq"


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


def get_consumer_channel(queue_name: str, binding_keys):
    connection = _get_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    channel.exchange_declare(exchange=DLX_EXCHANGE, exchange_type="direct", durable=True)
    channel.queue_declare(
        queue=queue_name,
        durable=True,
        arguments={
            "x-dead-letter-exchange": DLX_EXCHANGE,
            "x-dead-letter-routing-key": DLQ_NAME,
        },
    )
    channel.queue_declare(queue=DLQ_NAME, durable=True)
    channel.queue_bind(exchange=DLX_EXCHANGE, queue=DLQ_NAME, routing_key=DLQ_NAME)
    if isinstance(binding_keys, (list, tuple, set)):
        for k in binding_keys:
            channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=k)
    else:
        channel.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=binding_keys)
    channel.basic_qos(prefetch_count=1)
    return connection, channel