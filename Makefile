COMPOSE = docker compose \
		--project-directory . \
		-f api-gateway/docker-compose.yml \
		-f services/community-service/docker-compose.yml

NAMESPACE := leddit

.PHONY: build clean down network ps gateway-up kube-script kube-up kube-down kube-nuke

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

voting-up: network
	cd services/voting-service && docker compose up -d --build

keycloak-up: network
	cd keycloak && docker compose up -d

integrity-up: network
	cd services/integrity-service && docker compose up -d

monitoring-up: network
	cd monitoring && docker compose up -d

up: gateway-up community-up rabbit-up post-up comment-up user-up voting-up keycloak-up integrity-up monitoring-up

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

voting-down:
	cd services/voting-service && docker compose down

keycloak-down:
	cd keycloak && docker compose down

integrity-down:
	cd services/integrity-service && docker compose down

monitoring-down:
	cd monitoring && docker compose down

down: gateway-down community-down rabbit-down post-down comment-down user-down voting-down keycloak-down integrity-down monitoring-down

# -------------------------
# Kubernetes
# -------------------------

kube-up:
	powershell -ExecutionPolicy Bypass -File k8s\scripts\setup.ps1

kube-down:
	kubectl delete namespace $(NAMESPACE) --ignore-not-found=true

status:
	kubectl get all -n $(NAMESPACE)

pods:
	kubectl get pods -n $(NAMESPACE) -w

logs:
	kubectl logs -n $(NAMESPACE) -l app=leddit --tail=100 -f

# -------------------------
# STUFF
# -------------------------
clean:
	cd services/community-service && docker compose down --remove-orphans
	cd api-gateway && docker compose down --remove-orphans


