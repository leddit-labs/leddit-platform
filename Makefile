COMPOSE = docker compose \
		--project-directory . \
		-f api-gateway/docker-compose.yml \
		-f services/community-service/docker-compose.yml


.PHONY: build clean down network ps gateway-up

network:
	docker network inspect leddit-network >/dev/null 2>&1 || docker network create leddit-network

gateway-up: network
	cd api-gateway && docker compose up -d

community-up: network
	cd services/community-service && docker compose up --build

up: gateway-up community-up

down:
	cd services/community-service && docker compose down
	cd api-gateway && docker compose down

clean:
	cd services/community-service && docker compose down --remove-orphans
	cd api-gateway && docker compose down --remove-orphans
