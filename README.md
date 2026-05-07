# Leddit Platform

## Setup Instructions

1. Create docker network

```bash
docker network create leddit-network
```

Now, you can hit services through the gateway on port 9080 (and not 8000)

If you have API Gateway and Community-Service running - Test it like this:

```bash
curl http://localhost:9080/communities
```
