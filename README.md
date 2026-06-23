# Leddit Platform

Leddit is a Reddit-inspired microservice platform. The project is split into multiple services, with an API gateway in front and a Python seeder that can create demo data across the running services.

## Requirements

Make sure you have the following installed:

- Docker
- Docker Compose
- Make
- Python 3.12, (only if you want to run the seeder locally instead of in Docker)
- Minikube and kubectl, (only if you want to run the Kubernetes setup)

## Services

The local Docker setup expects the services to communicate on the shared Docker network `leddit-network`.

The seeder uses these internal service URLs:

| Service     | Internal URL                    |
| ----------- | ------------------------------- |
| Users       | `http://user-service:8001`      |
| Communities | `http://community-service:8000` |
| Posts       | `http://post-service:8000`      |
| Comments    | `http://comment-service:8003`   |
| Votes       | `http://vote-write-api:8004`    |
| Keycloak    | `http://keycloak:8080`          |

The API gateway is exposed locally on port `9080`.

## Quick start with Docker Compose

From the repository root, create the shared Docker network:

```bash
make network
```

Or create it manually:

```bash
docker network create leddit-network
```

Start all services:

```bash
make up
```

This starts the gateway, community service, RabbitMQ, post service, comment service, user service, voting service, Keycloak, integrity service, and monitoring stack.

Check that the containers are running:

```bash
docker ps
```

Test the API gateway:

```bash
curl http://localhost:9080/api/v1/communities
```

Useful local URLs:

| App                 | URL                      |
| ------------------- | ------------------------ |
| API Gateway         | `http://localhost:9080`  |
| Keycloak            | `http://localhost:8080`  |
| Grafana             | `http://localhost:3000`  |
| RabbitMQ Management | `http://localhost:15672` |

## Keycloak setup

Start Keycloak with the rest of the stack:

```bash
make keycloak-up
```

Then initialize or repair the Keycloak realm/client/user setup:

```bash
make fix-keycloak
```

The current seeder authenticates against the `leddit` realm using:

```text
username: nademtis
password: nademtis
client: leddit-frontend
```

If you change the seed user, Keycloak realm, or frontend client, update the seeder auth configuration before running the seed step.

## Seed the database

The seeder is a Python 3.12 app that waits for all dependent services to become healthy before creating data.

It currently does the following:

1. Waits for users, communities, posts, comments, votes, and Keycloak to respond successfully.
2. Logs in through Keycloak.
3. Fetches the current authenticated user from `/users/me`.
4. Creates one community.
5. Creates one post in that community for the authenticated user.

Comments and votes are present in the seeder code, but currently commented out. Enable those sections in `app/main.py` when you want to seed comments and votes too.

### Run the seeder with Docker

Make sure the main platform services are already running:

```bash
make up
make fix-keycloak
```

Then run the seeder:

```bash
docker compose -f docker-compose.yml up --build seeder
```

To run it once and remove the seeder container afterward:

```bash
docker compose -f docker-compose.yml run --rm seeder
```

If your seeder compose file has another name, point Docker Compose at that file instead. For example:

```bash
docker compose -f docker-compose.seeder.yml run --rm seeder
```

## Common commands

| Command              | Description                                                   |
| -------------------- | ------------------------------------------------------------- |
| `make network`       | Create the shared Docker network if it does not already exist |
| `make up`            | Start all Docker Compose services                             |
| `make down`          | Stop all Docker Compose services                              |
| `make gateway-up`    | Start only the API gateway                                    |
| `make community-up`  | Start only the community service                              |
| `make user-up`       | Start only the user service                                   |
| `make post-up`       | Start only the post service                                   |
| `make comment-up`    | Start only the comment service                                |
| `make voting-up`     | Start only the voting service                                 |
| `make keycloak-up`   | Start Keycloak                                                |
| `make fix-keycloak`  | Run the Keycloak init script                                  |
| `make monitoring-up` | Start monitoring services                                     |
| `make clean`         | Stop selected services and remove orphan containers           |

## Kubernetes setup

Create or configure the Kubernetes environment:

```bash
make kube-setup
```

Start Minikube:

```bash
make start
```

Check pod status:

```bash
make status
```

Watch pods:

```bash
make watch
```

Forward the main app ports:

```bash
make forward-app
```

This exposes:

| App      | URL                     |
| -------- | ----------------------- |
| Frontend | `http://localhost:5173` |
| API      | `http://localhost:9080` |

Forward the full development stack:

```bash
make forward
```

This exposes frontend, API, Grafana, Keycloak, RabbitMQ, and Alloy.

Stop Minikube:

```bash
make stop
```

Delete the Minikube cluster and all local cluster data:

```bash
make destroy
```

## Troubleshooting

### `network leddit-network declared as external, but could not be found`

Create the network:

```bash
make network
```

### Seeder fails while waiting for services

The seeder waits for service health endpoints. Make sure all required services are running and connected to `leddit-network`:

```bash
docker ps
```

Then check the logs for the failing service:

```bash
docker logs <container-name>
```

### Seeder cannot get a Keycloak token

Run the Keycloak initialization script:

```bash
make fix-keycloak
```

Then verify that Keycloak is reachable:

```bash
curl http://localhost:8080/realms/leddit
```

### API gateway returns connection errors

Make sure the target service is running and that the gateway is on the same Docker network:

```bash
docker network inspect leddit-network
```

## Development notes

The seeder depends on:

- `httpx` for HTTP requests
- `faker` for generated demo data
- `pydantic`
- `asyncio`

Generated seed data includes fake users, communities, posts, comments, and votes. The current active seed flow only creates communities and posts for the authenticated user.
