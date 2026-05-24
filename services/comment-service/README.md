# comment-service

This is the microservice responsible for comments

## How to run

```bash
docker-compose up --build -d
```

## How to run unit tests

```bash
docker compose -f docker-compose.test.yml run --rm unit-tests
```

## How to run integration tests

```bash
docker compose -f docker-compose.test.yml run --rm integration-tests
```