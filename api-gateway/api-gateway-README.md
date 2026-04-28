# API-Gateway

Uses open source tool; `Apache APISIX`

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
