# Leddit — Kubernetes Local Setup

## Prerequisites - minikube, kubectl, helm

Install on arch linux

```bash
pacman -S minikube kubectl helm
```

Install on windows using chocolatey

```powershell
choco install minikube kubectl kubernetes-helm
```

Install on windows using Winget

```powershell
winget install Kubernetes.minikube
winget install Kubernetes.kubectl
winget install Helm.Helm
```

## Usage Guidelines

### STARTING AND STOPPING THE CLUSTER

The minikube node can be started with

```bash
make start # (or minikube start)
make stop # (or minikube stop)
```

After starting the node, give it a few minutes and then check with:

```bash
make status # See all pods
make watch # Watch all pods in real time
```

### PORT-FORWARDING

Needs port-forwarding for app to work:

- Frontend - Port: 5173
- APISIX - Port: 9080

The other port-forwards are only for admin/debug access:

- Grafana for dashboards
- Keycloak admin console
- RabbitMQ management UI
- Alloy UI

| Name                   | Port  | Description                                  |
| ---------------------- | ----- | -------------------------------------------- |
| Frontend               | 5173  | The React frontend application               |
| APISIX                 | 9080  | The API Gateway                              |
| Grafana                | 3000  | For monitoring and dashboards                |
| Keycloak Admin Console | 8080  | For managing Keycloak users and realms       |
| RabbitMQ Management UI | 15672 | For monitoring RabbitMQ queues and exchanges |
| Alloy UI               | 12345 | For monitoring KEDA and HPA metrics          |

Use our Makefile scripts to forward ports:

```bash
make forward # All the good stuff from above
make forward-app # ONLY Frontend and APISIX
```

## Horizontal Pod Scaling

Two strategies for horizontal pod scaling are used in this project:

1. KEDA (Kubernetes Event-driven Autoscaling)
2. HPA (Horizontal Pod Autoscaler)

Event-driven scaling looks for depth of queue in rabbitmq.
HPA looks at pod metrics like CPU usage or memory usage.

## Users guide

Remove everything in namespace:

```bash
kubectl delete namespace leddit
```
