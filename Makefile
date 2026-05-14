COMPOSE = docker compose \
		--project-directory . \
		-f api-gateway/docker-compose.yml \
		-f services/community-service/docker-compose.yml


.PHONY: build clean down network ps gateway-up

# -------------------------
# HELPERS
# -------------------------
network:
	docker network inspect leddit-network >/dev/null 2>&1 || docker network create leddit-network

fix-keycloak:
	@bash keycloak/scripts/init-keycloak.sh

# -------------------------
# UP
# -------------------------
gateway-up: network
	cd api-gateway && docker compose up -d

community-up: network
	cd services/community-service && docker compose up -d --build

rabbit-up: network
	cd rabbitmq && docker compose up -d

post-up: network
	cd services/post-service && docker compose up -d --build

comment-up: network
	cd services/comment-service && docker compose up -d --build

user-up: network
	cd services/user-service && docker compose up -d --build

keycloak-up: network
	cd keycloak && docker compose up -d

integrity-up: network
	cd services/integrity-service && docker compose up -d

up: gateway-up community-up rabbit-up post-up comment-up user-up keycloak-up integrity-up

# -------------------------
# DOWN
# -------------------------
gateway-down:
	cd api-gateway && docker compose down

community-down:
	cd services/community-service && docker compose down

rabbit-down:
	cd rabbitmq && docker compose down

post-down:
	cd services/post-service && docker compose down

comment-down:
	cd services/comment-service && docker compose down

user-down:
	cd services/user-service && docker compose down

keycloak-down:
	cd keycloak && docker compose down

integrity-down:
	cd services/integrity-service && docker compose down

down: gateway-down community-down rabbit-down post-down comment-down user-down keycloak-down integrity-down

# -------------------------
# STUFF
# -------------------------
clean:
	cd services/community-service && docker compose down --remove-orphans
	cd api-gateway && docker compose down --remove-orphans
