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

## Horizontal Pod Scaling

Two strategies for horizontal pod scaling are used in this project:

1. KEDA (Kubernetes Event-driven Autoscaling)
2. HPA (Horizontal Pod Autoscaler)

Event-driven scaling looks for depth of queue in rabbitmq.
HPA looks at pod metrics like CPU usage or memory usage.

## TODO

1. Make / fix all the manifest yml's.
2. Test it
3. Update Makefile to build service images inside minikube
4. Update Makefile to apply the manifests

## Users guide

Remove everything in namespace:
```bash
kubectl delete namespace leddit
```