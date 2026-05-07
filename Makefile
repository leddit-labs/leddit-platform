COMPOSE = docker compose \
		--project-directory . \
		-f api-gateway/docker-compose.yml \
		-f services/community-service/docker-compose.yml


.PHONY: build clean down network ps gateway-up

network:
	docker network inspect leddit-network >/dev/null 2>&1 || docker network create leddit-network

# -------------------------
# UP
# -------------------------
gateway-up: network
	cd api-gateway && docker compose up -d

community-up: network
	cd services/community-service && docker compose up --build

rabbit-up: network
	cd rabbitmq && docker compose up -d

up: gateway-up community-up

# -------------------------
# DOWN
# -------------------------
gateway-down:
	cd api-gateway && docker compose down

community-down:
	cd services/community-service && docker compose down

rabbit-down:
	cd rabbitmq && docker compose down

down: gateway-down community-down rabbit-down

# -------------------------
# STUFF
# -------------------------
clean:
	cd services/community-service && docker compose down --remove-orphans
	cd api-gateway && docker compose down --remove-orphans
