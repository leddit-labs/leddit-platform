#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# Leddit K8s Local Setup Script
# Run from the project root (where this k8s/ dir lives)
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$K8S_DIR/.." && pwd)"

echo "==> Starting minikube..."
minikube start --cpus=4 --memory=8192 --driver=docker \
  --addons=metrics-server,ingress 2>/dev/null || true

echo "==> Pointing Docker to minikube..."
eval $(minikube docker-env --shell bash)

echo "==> Building service images..."
docker build -t leddit/post-service:latest "$PROJECT_ROOT/services/post-service"
docker build -t leddit/comment-service:latest "$PROJECT_ROOT/services/comment-service"
docker build -t leddit/community-service:latest "$PROJECT_ROOT/services/community-service"
docker build -t leddit/user-service:latest "$PROJECT_ROOT/services/user-service"
docker build -t leddit/voting-service:latest "$PROJECT_ROOT/services/voting-service"
docker build -t leddit/integrity-service:latest "$PROJECT_ROOT/services/integrity-service"
docker build -t leddit/frontend:latest "$PROJECT_ROOT/frontend"

echo "==> Creating namespace..."
kubectl apply -f "$K8S_DIR/namespace/"

kubectl -n leddit delete configmap keycloak-terraform-config --ignore-not-found 2>/dev/null || true
kubectl -n leddit create configmap keycloak-terraform-config \
  --from-file=main.tf="$PROJECT_ROOT/keycloak/terraform/main.tf" \
  --from-file=variables.tf="$PROJECT_ROOT/keycloak/terraform/variables.tf" \
  --from-file=leddit-realm.tf="$PROJECT_ROOT/keycloak/terraform/leddit-realm.tf"

if ! kubectl -n leddit get configmap keycloak-terraform-config > /dev/null 2>&1; then
  echo "FATAL: Failed to create keycloak-terraform-config"
  exit 1
fi
echo "   keycloak-terraform-config created"

echo "==> Creating configmaps from source files..."
kubectl -n leddit create configmap monitoring-config \
  --from-file=loki-config.yml="$PROJECT_ROOT/monitoring/loki-config.yml" \
  --from-file=prometheus.yml="$PROJECT_ROOT/monitoring/prometheus.yml" \
  --from-file=alloy-config.alloy="$PROJECT_ROOT/monitoring/alloy-config.alloy" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n leddit create configmap grafana-datasources \
  --from-file=datasources.yml="$PROJECT_ROOT/monitoring/grafana/provisioning/datasources/datasources.yml" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n leddit create configmap apisix-config \
  --from-file=config.yaml="$PROJECT_ROOT/api-gateway/apisix/config.yaml" \
  --from-file=apisix.yaml="$PROJECT_ROOT/api-gateway/apisix/apisix.yaml" \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n leddit create configmap vote-init-sql \
  --from-file=init-db.sql="$PROJECT_ROOT/services/voting-service/app/db/init-db.sql" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Installing KEDA (for queue-based autoscaling)..."
helm repo add kedacore https://kedacore.github.io/charts 2>/dev/null || true
helm repo update
helm upgrade --install keda kedacore/keda --namespace keda --create-namespace --wait

echo "==> Deploying infrastructure..."
kubectl apply -f "$K8S_DIR/infrastructure/rabbitmq/"
kubectl apply -f "$K8S_DIR/infrastructure/keycloak/"
kubectl apply -f "$K8S_DIR/infrastructure/monitoring/"
kubectl apply -f "$K8S_DIR/infrastructure/apisix/"

echo "==> Waiting for infrastructure to be ready..."
kubectl -n leddit wait --for=condition=ready pod -l app=rabbitmq --timeout=120s || true
kubectl -n leddit wait --for=condition=ready pod -l app=keycloak-db --timeout=60s || true

echo "==> Running Keycloak Terraform job..."
kubectl -n leddit wait --for=condition=ready pod -l app=keycloak --timeout=300s || {
  echo "WARNING: Keycloak not ready after 300s, running Terraform anyway..."
}
kubectl apply -f "$K8S_DIR/infrastructure/keycloak/job-terraform.yaml"
echo "   Waiting for Terraform job to complete..."
kubectl -n leddit wait --for=condition=complete job/keycloak-terraform --timeout=300s
echo "   Terraform job completed."

echo "==> Deploying application services..."
kubectl apply -f "$K8S_DIR/services/post-service/"
kubectl apply -f "$K8S_DIR/services/comment-service/"
kubectl apply -f "$K8S_DIR/services/community-service/"
kubectl apply -f "$K8S_DIR/services/user-service/"
kubectl apply -f "$K8S_DIR/services/voting-service/"
kubectl apply -f "$K8S_DIR/services/integrity-service/"
kubectl apply -f "$K8S_DIR/services/frontend/"

echo ""
echo "==> Done! Watch pods come up with:"
echo "    kubectl -n leddit get pods -w"
echo ""
echo "==> To access services, run in a separate terminal:"
echo "    minikube tunnel"
echo ""
echo "==> Or port-forward individually:"
echo "    kubectl -n leddit port-forward svc/apisix 9080:9080"
echo "    kubectl -n leddit port-forward svc/grafana 3000:3000"
echo "    kubectl -n leddit port-forward svc/keycloak 8080:8080"
