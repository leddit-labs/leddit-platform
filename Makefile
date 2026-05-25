COMPOSE = docker compose \
		--project-directory . \
		-f api-gateway/docker-compose.yml \
		-f services/community-service/docker-compose.yml

NAMESPACE := leddit

.PHONY: build clean down network ps gateway-up kube-script kube-up kube-down kube-nuke start stop destroy forward forward-app

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

kube-setup:
	powershell -ExecutionPolicy Bypass -File k8s\scripts\setup.ps1

start:
	minikube start
	@echo "Cluster is running. Use 'make status' to check pods."

stop:
	minikube stop

destroy:
	@echo "This will delete the minikube cluster and ALL data."
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	minikube delete

status: ## Show all pods in the leddit namespace
	kubectl -n $(NAMESPACE) get pods
 
watch: ## Watch pods in real time
	kubectl -n $(NAMESPACE) get pods -w

forward: ## Port-forward the good stuff (frontend, apisix, grafana, keycloak, rabbitmq, alloy)
	@echo "Starting port-forwards... (Ctrl+C to stop all)"
	@kubectl -n $(NAMESPACE) port-forward svc/frontend 5173:80 &
	@kubectl -n $(NAMESPACE) port-forward svc/apisix 9080:9080 &
	@kubectl -n $(NAMESPACE) port-forward svc/grafana 3000:3000 &
	@kubectl -n $(NAMESPACE) port-forward svc/keycloak 8080:8080 &
	@kubectl -n $(NAMESPACE) port-forward svc/rabbitmq 15672:15672 &
	@kubectl -n $(NAMESPACE) port-forward svc/alloy 12345:12345 &
	@echo ""
	@echo "  Frontend:  http://localhost:5173"
	@echo "  API:       http://localhost:9080"
	@echo "  Grafana:   http://localhost:3000"
	@echo "  Keycloak:  http://localhost:8080"
	@echo "  RabbitMQ:  http://localhost:15672"
	@echo "  Alloy:     http://localhost:12345"
	@echo ""
	@wait

forward-app: ## Port-forward only frontend + APISIX
	@echo "Starting app port-forwards... (Ctrl+C to stop)"
	@kubectl -n $(NAMESPACE) port-forward svc/frontend 5173:80 &
	@kubectl -n $(NAMESPACE) port-forward svc/apisix 9080:9080 &
	@echo ""
	@echo "  Frontend:  http://localhost:5173"
	@echo "  API:       http://localhost:9080"
	@echo ""
	@wait

# -------------------------
# STUFF
# -------------------------
clean:
	cd services/community-service && docker compose down --remove-orphans
	cd api-gateway && docker compose down --remove-orphans


