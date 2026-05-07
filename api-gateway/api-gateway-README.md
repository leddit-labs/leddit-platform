# API-Gateway

Uses open source tool; `Apache APISIX`

## API GateWHY?

### Single Point of Entry

Frontend only needs to know one address: `http://localhost:9080`

This is easier than:

- localhost:8081 for posts
- localhost:8082 for comments
- localhost:8083 for communities

### Single source of truth

[apisix.yaml](apisix/apisix.yaml) is the single source of truth for all routes,
plugins, and upstreams.

### Auth in one place

With the `openid-connect` plugin, APISIX can validate the Keycloak JWT on every
request before it reaches our services.

Therefore, our individual services don't need token validation implemented.

### Other good points

- request logging in one place
  - and metrics for Prometheus
- Load balancing (if KEDA doesn't already do this for us)
- rate limiting

## HOW TO USE

```yaml
- uri: /community-service/*
  upstream:
    type: roundrobin
    nodes:
      "community-service:8000": 1
  plugins:
    proxy-rewrite:
      regex_uri: ["^/community-service(.*)$", "$1"]
```

## Architecture Decisions

Running in Standalone mode: routes are declared in apisix.yaml, **no etcd needed.**

## Improvements

This can be added to apisix/config.yaml to expose an endpoint on 9091 for  
Prometheus metrics

```yaml
plugin_attr:
  prometheus:
    export_addr:
      ip: 0.0.0.0
      port: 9091
```
