# Leddit

Keycloak authentication setup for Leddit

## Prerequisites

- Docker Desktop
- Terraform CLI

## Quick Start

make setup

or

```bash
# 1. Start Keycloak
docker compose up -d

# 2. Wait for it to be ready
curl http://localhost:9000/health/ready

# 3. Apply configuration
cd terraform
terraform init
terraform apply -auto-approve
```
