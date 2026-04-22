workspace "Leddit Platform" "Architecture choices: REST for external CRUD, GraphQL for client-shaped reads, gRPC for internal sync, RabbitMQ for async. SOAP intentionally omitted. See notes for details." {

    configuration {
        scope softwareSystem
    }

     model {
        user = person "User" "End user who reads, posts, comments, and votes."
        moderator = person "Moderator" "Community moderator with elevated permissions."
        admin = person "Admin" "Platform administrator."

        platform = softwareSystem "Leddit Platform" {

            description "A Reddit-like platform"
            !docs .

            // ---------- Frontend ----------
            frontend = container "Frontend" "Web UI for the platform." "React (probably)" "Frontend"

            // ---------- API Gateway ----------
            //gateway = container "API Gateway" "Routes external traffic, terminates JWT, exposes REST + GraphQL to clients." "Traefik / Kong" "Gateway"
            gateway = container "API Gateway" "Routes external traffic, validates JWT signature locally (via Identity public key), injects trusted user claims into downstream headers. Exposes REST + GraphQL to clients." "Traefik / Kong / (maybe NGINX ?)" "Gateway"

            // ---------- Core services ----------
            identity = container "Identity Service" "Registration, login, JWT issuance, OAuth, profiles, roles." "GraphQL (external) + gRPC (internal)" "Service" {
                tags "GraphQL"
            }
            identityDb = container "Identity DB" "Users, credentials, roles, OAuth links." "PostgreSQL" "Database"

            community = container "Community Service" "Create/join/leave communities, moderator actions." "REST" "Service"
            communityDb = container "Community DB" "Communities, memberships, bans, rules." "PostgreSQL" "Database"

            posts = container "Posts Service" "Create/edit/delete posts with tombstone semantics, feeds." "FastAPI (REST)" "Service"
            postsDb = container "Posts DB" "Posts, tombstones, feed materializations." "PostgreSQL" "Database"

            comments = container "Comment Service" "Nested comments, edit/delete, threading." "REST" "Service"
            commentsDb = container "Comments DB" "Comments and reply trees." "PostgreSQL" "Database"

            voting = container "Voting Service" "CQRS; idempotent, commutative vote handling; score projection." "REST (write) + gRPC (hot reads)" "Service" {
                tags "CQRS"
            }
            votingWriteDb = container "Voting Write Store" "Append-only vote events (commutative)." "PostgreSQL" "Database"
            votingReadDb = container "Voting Read Store" "Aggregated scores and per-user vote state." "Redis / PostgreSQL" "Database"

            search = container "Search Service" "Search posts by title and communities by name." "REST" "Service"
            searchIndex = container "Search Index" "Full-text index of posts and communities." "Elasticsearch" "SearchIndex"

            notifications = container "Notification Service" "Reply and mention notifications, in-app list." "REST" "Service"
            notificationsDb = container "Notifications DB" "Per-user notification inbox." "PostgreSQL" "Database"

            moderation = container "Admin & Moderation Service" "Reports, moderation queue, user bans (Saga)." "REST" "Service" {
                tags "Saga"
            }
            moderationDb = container "Moderation DB" "Reports, queues, saga state, ban records." "PostgreSQL" "Database"

            integrity = container "Post Integrity Service" "LLM-based content moderation of new posts." "gRPC (internal) + REST (LLM)" "Service"
            llm = container "LLM Provider" "External LLM API (e.g. Anthropic / OpenAI)." "External REST API" "External"

            logging = container "Logging & Monitoring Service" "Collects logs and traces from all services." "Consumer" "Service"
            observabilityStore = container "Observability Store" "Logs, metrics, traces." "Loki / Tempo / Prometheus" "Database"

            // ---------- Messaging backbone ----------
            broker = container "RabbitMQ" "Async messaging backbone: events, commands, saga steps." "RabbitMQ (AMQP)" "Broker"

            // ============================================================
            // Users and Frontend
            // ============================================================
            user -> frontend "Uses" "HTTPS"
            moderator -> frontend "Uses" "HTTPS"
            admin -> frontend "Uses" "HTTPS"
            frontend -> gateway "API calls" "HTTPS"

            // ============================================================
            // External edge: REST and GraphQL through the gateway
            // ============================================================
            gateway -> identity "Profile & user queries" "GraphQL / HTTPS" "GraphQL"
            gateway -> community "Community CRUD" "REST / HTTPS" "REST"
            gateway -> posts "Post CRUD & feeds" "REST / HTTPS" "REST"
            gateway -> comments "Comment CRUD" "REST / HTTPS" "REST"
            gateway -> voting "Cast votes" "REST / HTTPS" "REST"
            gateway -> search "Search queries" "REST / HTTPS" "REST"
            gateway -> notifications "Inbox & read state" "REST / HTTPS" "REST"
            gateway -> moderation "Reports & queue" "REST / HTTPS" "REST"

            // ============================================================
            // Internal service-to-service: gRPC
            // ============================================================
            posts -> identity ", GetUser" "gRPC" "gRPC"
            comments -> identity "GetUser" "gRPC" "gRPC"
            moderation -> identity "Lookup users" "gRPC" "gRPC"
            posts -> voting "GetScores(postIds)" "gRPC" "gRPC"
            comments -> voting "GetScores(commentIds)" "gRPC" "gRPC"
            posts -> integrity "CheckPost (sync preview)" "gRPC" "gRPC"
            // NOTE: Not now
            // search -> posts "Hydrate post summaries" "gRPC" "gRPC"
            // search -> community "Hydrate community summaries" "gRPC" "gRPC"

            // ============================================================
            // Service -> own datastore
            // ============================================================
            identity -> identityDb "Reads/Writes"
            community -> communityDb "Reads/Writes"
            posts -> postsDb "Reads/Writes"
            comments -> commentsDb "Reads/Writes"
            voting -> votingWriteDb "Appends vote events"
            voting -> votingReadDb "Reads/Writes projections"
            search -> searchIndex "Indexes/Queries"
            notifications -> notificationsDb "Reads/Writes"
            moderation -> moderationDb "Reads/Writes"
            logging -> observabilityStore "Writes"

            // ============================================================
            // Async: publishers -> RabbitMQ
            // ============================================================
            identity -> broker "Publishes UserRegistered, UserBanned" "AMQP" "Async"
            community -> broker "Publishes CommunityCreated, UserBannedFromCommunity" "AMQP" "Async"
            posts -> broker "Publishes PostCreated, PostEdited, PostDeleted" "AMQP" "Async"
            comments -> broker "Publishes CommentCreated, UserMentioned" "AMQP" "Async"
            voting -> broker "Publishes VoteCast (commutative, idempotent)" "AMQP" "Async"
            moderation -> broker "Publishes/consumes saga steps (BanUserSaga)" "AMQP" "Async"
            integrity -> broker "Publishes PostApproved/PostRejected" "AMQP" "Async"

            // ============================================================
            // Async: RabbitMQ -> consumers
            // ============================================================
            broker -> search "Indexes new/edited posts and communities" "AMQP" "Async"
            broker -> notifications "Fans out reply/mention events" "AMQP" "Async"
            broker -> voting "Consumes vote commands" "AMQP" "Async"
            broker -> integrity "Consumes PostCreated for moderation" "AMQP" "Async"
            broker -> moderation "Consumes reports and saga replies" "AMQP" "Async"
            broker -> posts "Consumes integrity verdicts, ban-cascade commands" "AMQP" "Async"
            broker -> comments "Consumes ban-cascade commands" "AMQP" "Async"
            broker -> logging "Streams logs/traces from all services" "AMQP" "Async"

            // ============================================================
            // External
            // ============================================================
            integrity -> llm "Classifies post content" "HTTPS / REST" "REST"
        }
    }

    views {
        container platform "Containers" {
            include *
            autolayout lr
            description "Full view: REST + GraphQL edge, gRPC internal, RabbitMQ async."
        }
        container platform "Less-fluff" {
            include gateway
            include identity
            include community
            include posts
            include comments
            include voting
            include search
            include notifications
            include moderation
            include integrity
            include frontend
            include broker
            autolayout lr
            description "Something something. Describing something doing something."
        }
        container platform "Less-fluff-Noautolayout" {
            include gateway
            include identity
            include community
            include posts
            include comments
            include voting
            include search
            include notifications
            include moderation
            include integrity
            include frontend
            include broker
            description "An amazing description goes here."
        }
        container platform "services-and-datastores" "Services and DBs" {
            include identity
            include identityDb

            include community
            include communityDb

            include posts
            include postsDb

            include comments
            include commentsDb

            include voting
            include votingWriteDb
            include votingReadDb

            include search
            include searchIndex

            include notifications
            include notificationsDb

            include moderation
            include moderationDb

            include integrity

            include logging
            include observabilityStore

            description "Only services and their datastores."
        }
        container platform "services-and-broker" "Services and Broker" {
            include "element.tag==Service"
            include broker
            autolayout lr
            description "All backend services and their connections to RabbitMQ."
        }

        styles {
            element "Person" {
                shape person
                background #08427b
                color #ffffff
            }
            element "Frontend" {
                background #1168bd
                color #ffffff
            }
            element "Gateway" {
                background #2d6a4f
                color #ffffff
            }
            element "Service" {
                background #438dd5
                color #ffffff
            }
            element "Database" {
                shape cylinder
                background #f4a261
                color #000000
            }
            element "SearchIndex" {
                shape cylinder
                background #e76f51
                color #ffffff
            }
            element "Broker" {
                shape pipe
                background #c9184a
                color #ffffff
            }
            element "External" {
                background #6c757d
                color #ffffff
            }
            element "CQRS" {
                background #7209b7
                color #ffffff
            }
            element "Saga" {
                background #560bad
                color #ffffff
            }
            element "GraphQL" {
                background #e535ab
                color #ffffff
            }

            // Relationship styles
            // one color per protocol
            relationship "GraphQL" {
                color #e535ab
                thickness 3
            }
            relationship "REST" {
                color #1168bd
                thickness 2
            }
            relationship "gRPC" {
                color #7209b7
                thickness 2
                style dashed
            }
            relationship "Async" {
                color #c9184a
                thickness 2
                style dotted
            }
        }
    }
}
