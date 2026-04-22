# Protocol choices

GraphQL:
external edge for aggregated/nested reads (profile pages, feeds with nested  
data).  
Used at the Identity service (spec'd that way) and could front the frontend.

REST:
external edge for resource-oriented CRUD (posts, comments, communities,  
notifications, moderation). Boring, cacheable, correct default.

gRPC:
internal service-to-service sync calls where we want strong typing, low  
latency, and generated clients (token validation, score reads, integrity checks).

RabbitMQ:
everything async — events, fanout, saga steps, indexing, notifications, logs.

SOAP:
NOT used. SOAP fits enterprise/legacy integrations (banking, insurance, HL7).  
Nothing in this platform — a social content app with web/mobile clients and

## How to run it?

Run the structurizr server app in docker:

```bash
docker run -it --rm -p 8080:8080 \
    -v ~/app/structurizr:/usr/local/structurizr \
    structurizr/structurizr local
```
