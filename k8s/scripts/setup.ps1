# ─────────────────────────────────────────────
# Leddit K8s Local Setup Script (Windows)
# Can be run from anywhere — paths resolve from the script's location
# ─────────────────────────────────────────────
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$K8sDir = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $K8sDir

Write-Host "==> Starting minikube..."
minikube start --cpus=4 --memory=8192 --driver=docker --addons=metrics-server,ingress

#Write-Host "==> Pointing Docker to minikube..."
#minikube docker-env --shell powershell | Invoke-Expression

Write-Host "==> Building service images..."
minikube image build -t leddit/post-service:latest "$ProjectRoot\services\post-service"
minikube image build -t leddit/comment-service:latest "$ProjectRoot\services\comment-service"
minikube image build -t leddit/community-service:latest "$ProjectRoot\services\community-service"
minikube image build -t leddit/user-service:latest "$ProjectRoot\services\user-service"
minikube image build -t leddit/voting-service:latest "$ProjectRoot\services\voting-service"
minikube image build -t leddit/integrity-service:latest "$ProjectRoot\services\integrity-service"
minikube image build -t leddit/frontend:latest "$ProjectRoot\frontend"

Write-Host "==> Checking minikube images..."
minikube image ls | Select-String "leddit"

Write-Host "==> Creating namespace..."
kubectl apply -f "$K8sDir\namespace"

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

Write-Host "==> Creating terraform configmap..."
kubectl -n leddit delete configmap keycloak-terraform-config --ignore-not-found 2>$null
kubectl -n leddit create configmap keycloak-terraform-config `
  --from-file=main.tf="$ProjectRoot\keycloak\terraform\main.tf" `
  --from-file=variables.tf="$ProjectRoot\keycloak\terraform\variables.tf" `
  --from-file=leddit-realm.tf="$ProjectRoot\keycloak\terraform\leddit-realm.tf"

if (-not $?) {
  Write-Host "FATAL: Failed to create keycloak-terraform-config"
  exit 1
}
Write-Host "   keycloak-terraform-config created"

Write-Host "==> Installing KEDA (for queue-based autoscaling)..."
helm repo add kedacore https://kedacore.github.io/charts 2>$null
helm repo update
helm upgrade --install keda kedacore/keda --namespace keda --create-namespace --wait

Write-Host "==> Deploying infrastructure..."
kubectl apply -f "$K8sDir\infrastructure\rabbitmq"
kubectl apply -f "$K8sDir\infrastructure\keycloak"
kubectl apply -f "$K8sDir\infrastructure\monitoring"
kubectl apply -f "$K8sDir\infrastructure\apisix"

Write-Host "==> Waiting for infrastructure..."
kubectl -n leddit wait --for=condition=ready pod -l app=rabbitmq --timeout=120s
kubectl -n leddit wait --for=condition=ready pod -l app=keycloak-db --timeout=60s

Write-Host "==> Running Keycloak Terraform job..."
kubectl -n leddit wait --for=condition=ready pod -l app=keycloak --timeout=300s
kubectl apply -f "$K8sDir\infrastructure\keycloak\job-terraform.yaml"
Write-Host "   Waiting for Terraform job to complete..."
kubectl -n leddit wait --for=condition=complete job/keycloak-terraform --timeout=300s
Write-Host "   Terraform job completed."

Write-Host "==> Deploying application services..."
kubectl apply -f "$K8sDir\services\post-service"
kubectl apply -f "$K8sDir\services\comment-service"
kubectl apply -f "$K8sDir\services\community-service"
kubectl apply -f "$K8sDir\services\user-service"
kubectl apply -f "$K8sDir\services\voting-service"
kubectl apply -f "$K8sDir\services\integrity-service"
kubectl apply -f "$K8sDir\services\frontend"

Write-Host ""
Write-Host "==> Done! Watch pods come up with:"
Write-Host "    kubectl -n leddit get pods -w"
Write-Host ""
Write-Host "==> To access services, run in a separate terminal:"
Write-Host "    minikube tunnel"
Write-Host ""
Write-Host "==> Or port-forward individually:"
Write-Host "    kubectl -n leddit port-forward svc/apisix 9080:9080"
Write-Host "    kubectl -n leddit port-forward svc/grafana 3000:3000"
Write-Host "    kubectl -n leddit port-forward svc/keycloak 8080:8080"
