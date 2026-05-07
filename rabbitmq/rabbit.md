# BunnyMQ (C)

## In code

```python
channel.exchange_declare(
  exchange=EXCHANGE_NAME,
  exchange_type="topic",
  durable=True
)
```

The first service to connect creates the events exchange, and every subsequent
call just confirms it already exists. Same thing on the consumer side with `queue_declare`

This makes it idempotent.

## GUI

See `localhsot:15672` with username `guest` and password `guest`
