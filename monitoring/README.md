# Monitoring

Metrics, Logs, Tracing

## Overview

UI's at:

- localhost:12345 : Alloy
- localhost:3000 : Grafana

## PromQL

For request rate:

```PromQL
rate(http_requests_total{service="community-service"}[5m])
```

For p95 latency:

```PromQL
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```
