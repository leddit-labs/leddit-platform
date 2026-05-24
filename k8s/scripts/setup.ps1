# ─────────────────────────────────────────────
# Leddit K8s Local Setup Script (Windows)
# Run from the project root (where the k8s/ dir lives)
# ─────────────────────────────────────────────
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "==> Starting minikube..."
minikube start --cpus=4 --memory=8192 --driver=docker --addons=metrics-server,ingress

Write-Host "==> Pointing Docker to minikube..."
minikube docker-env | Invoke-Expression

Write-Host "==> Building service images..."
docker build -t leddit/post-service:latest      "$ProjectRoot\services\post-service"
docker build -t leddit/comment-service:latest   "$ProjectRoot\services\comment-service"
docker build -t leddit/community-service:latest "$ProjectRoot\services\community-service"
docker build -t leddit/user-service:latest      "$ProjectRoot\services\user-service"
docker build -t leddit/voting-service:latest    "$ProjectRoot\services\voting-service"
docker build -t leddit/integrity-service:latest "$ProjectRoot\services\integrity-service"
docker build -t leddit/frontend:latest          "$ProjectRoot\frontend"

Write-Host "==> Creating namespace..."
kubectl apply -f "$ScriptDir\namespace\"

Write-Host "==> Creating configmaps from source files..."
kubectl -n leddit create configmap monitoring-config `
  --from-file=loki-config.yml="$ProjectRoot\monitoring\loki-config.yml" `
  --from-file=prometheus.yml="$ProjectRoot\monitoring\prometheus.yml" `
  --from-file=alloy-config.alloy="$ProjectRoot\monitoring\alloy-config.alloy" `
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n leddit create configmap grafana-datasources `
  --from-file=datasources.yml="$ProjectRoot\monitoring\grafana\provisioning\datasources\datasources.yml" `
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n leddit create configmap apisix-config `
  --from-file=config.yaml="$ProjectRoot\api-gateway\apisix\config.yaml" `
  --from-file=apisix.yaml="$ProjectRoot\api-gateway\apisix\apisix.yaml" `
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n leddit create configmap vote-init-sql `
  --from-file=init-db.sql="$ProjectRoot\services\voting-service\app\db\init-db.sql" `
  --dry-run=client -o yaml | kubectl apply -f -

Write-Host "==> Installing KEDA (for queue-based autoscaling)..."
helm repo add kedacore https://kedacore.github.io/charts 2>$null
helm repo update
helm upgrade --install keda kedacore/keda --namespace keda --create-namespace --wait

Write-Host "==> Deploying infrastructure..."
kubectl apply -f "$ScriptDir\infrastructure\rabbitmq\"
kubectl apply -f "$ScriptDir\infrastructure\keycloak\"
kubectl apply -f "$ScriptDir\infrastructure\monitoring\"
kubectl apply -f "$ScriptDir\infrastructure\apisix\"

Write-Host "==> Waiting for infrastructure..."
kubectl -n leddit wait --for=condition=ready pod -l app=rabbitmq --timeout=120s
kubectl -n leddit wait --for=condition=ready pod -l app=keycloak-db --timeout=60s

Write-Host "==> Deploying application services..."
kubectl apply -f "$ScriptDir\services\post-service\"
kubectl apply -f "$ScriptDir\services\comment-service\"
kubectl apply -f "$ScriptDir\services\community-service\"
kubectl apply -f "$ScriptDir\services\user-service\"
kubectl apply -f "$ScriptDir\services\voting-service\"
kubectl apply -f "$ScriptDir\services\integrity-service\"
kubectl apply -f "$ScriptDir\services\frontend\"

Write-Host ""
Write-Host "==> Done! Watch pods come up with:"
Write-Host "    kubectl -n leddit get pods -w"
Write-Host ""
Write-Host "==> To access services, run in a separate terminal:"
Write-Host "    minikube tunnel"
