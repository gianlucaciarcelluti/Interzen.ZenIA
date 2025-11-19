# Sequence Diagrams Template - ZenIA

Questo documento contiene pattern e template di sequence diagrams in Mermaid che puoi utilizzare per documentare i flussi dei microservizi (MS) e sub-progetti (SP).

---

## 📋 Indice Pattern

1. [Happy Path (Main Flow)](#1-happy-path-main-flow)
2. [Alternative Paths (Cache, Optimization)](#2-alternative-paths)
3. [Error Flows](#3-error-flows)
4. [Integration Flows (Multi-service)](#4-integration-flows)
5. [Lifecycle & State Changes](#5-lifecycle--state-changes)
6. [Async Processing](#6-async-processing)

---

## 1. Happy Path (Main Flow)

### Template: Simple Request-Response
Use this for basic synchronous operations.

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as MS11<br/>Gateway
    participant Service as MSxx<br/>Service
    participant DB as PostgreSQL<br/>DB

    Client->>Gateway: Request
    Gateway->>Service: Forward<br/>(auth validated)

    Service->>Service: Process logic

    Service->>DB: Store result
    DB-->>Service: Confirmed

    Service-->>Gateway: Response
    Gateway-->>Client: 200 OK
```

### Template: With External Dependency
Use this when service depends on another MS.

```mermaid
sequenceDiagram
    participant Client
    participant ServiceA as MSxx<br/>Service A
    participant ServiceB as MSyy<br/>Service B
    participant Cache as Redis<br/>Cache

    Client->>ServiceA: Request

    ServiceA->>Cache: Check cache
    Cache-->>ServiceA: Miss

    ServiceA->>ServiceB: Call dependency
    ServiceB->>ServiceB: Process
    ServiceB-->>ServiceA: Response data

    ServiceA->>Cache: Store in cache
    ServiceA-->>Client: Response
```

---

## 2. Alternative Paths

### Template: Cache Hit (Performance Optimization)

```mermaid
sequenceDiagram
    participant Client
    participant Service as MSxx<br/>Service
    participant Cache as Redis<br/>Cache

    Client->>Service: Request

    Service->>Cache: Check cache
    Cache-->>Service: HIT!<br/>(cached result)

    Service->>Service: Update metrics
    Service-->>Client: Response<br/>(from cache)<br/>FAST ⚡

    Note over Cache: Latency: < 50ms
```

### Template: Fallback Path (Degraded Mode)

```mermaid
sequenceDiagram
    participant Client
    participant Service as MSxx<br/>Service
    participant Primary as Primary<br/>Service
    participant Fallback as Fallback<br/>Service

    Client->>Service: Request

    Service->>Primary: Try primary<br/>dependency
    Primary--xService: TIMEOUT/ERROR

    Note over Service: Primary unavailable<br/>switching to fallback

    Service->>Fallback: Try fallback<br/>dependency
    Fallback-->>Service: Response<br/>(degraded)<br/>SLOW ⚠️

    Service-->>Client: 200 OK<br/>(with fallback data)
```

### Template: Retry Logic

```mermaid
sequenceDiagram
    participant Client
    participant Service as MSxx<br/>Service
    participant External as External<br/>API

    Client->>Service: Request

    loop Retry 3x (exponential backoff)
        Service->>External: Try request
        External--xService: ERROR/TIMEOUT
        Service->>Service: Wait & retry
    end

    Service-->>Client: Either 200 OK<br/>or 503 Service Unavailable
```

---

## 3. Error Flows

### Template: Validation Error

```mermaid
sequenceDiagram
    participant Client
    participant Service as MSxx<br/>Service
    participant Validator as Validator<br/>Component

    Client->>Service: Request (invalid)

    Service->>Validator: Validate input
    Validator-->>Service: Validation errors

    Service-->>Client: 422 Unprocessable<br/>Entity<br/>(validation failures)

    Note over Service: No further processing
```

### Template: Authorization Error

```mermaid
sequenceDiagram
    participant Client
    participant Gateway as MS11<br/>Gateway
    participant Security as MS13<br/>Security

    Client->>Gateway: Request<br/>(invalid auth token)

    Gateway->>Security: Validate token
    Security-->>Gateway: INVALID/EXPIRED

    Gateway-->>Client: 401 Unauthorized<br/>or 403 Forbidden

    Note over Gateway: Request rejected at gateway<br/>Never reaches service
```

### Template: Resource Not Found

```mermaid
sequenceDiagram
    participant Client
    participant Service as MSxx<br/>Service
    participant DB as PostgreSQL<br/>DB

    Client->>Service: GET /resource/{id}

    Service->>DB: Query by id
    DB-->>Service: NOT FOUND (null)

    Service-->>Client: 404 Not Found
```

### Template: Conflict/Duplicate

```mermaid
sequenceDiagram
    participant Client
    participant Service as MSxx<br/>Service
    participant DB as PostgreSQL<br/>DB

    Client->>Service: POST /resource<br/>(duplicate key)

    Service->>Service: Validate input

    Service->>DB: Insert record
    DB-->>Service: UNIQUE CONSTRAINT<br/>VIOLATION

    Service-->>Client: 409 Conflict<br/>(resource already exists)
```

---

## 4. Integration Flows

### Template: Multi-Service Pipeline (UC-style)

```mermaid
sequenceDiagram
    participant Source as Source<br/>System
    participant ServiceA as MSxx<br/>Service A
    participant ServiceB as MSyy<br/>Service B
    participant ServiceC as MSzz<br/>Service C
    participant Destination as Destination<br/>System

    Source->>ServiceA: Data input

    ServiceA->>ServiceA: Process step 1

    ServiceA->>ServiceB: Pass to step 2
    ServiceB->>ServiceB: Process step 2

    ServiceB->>ServiceC: Pass to step 3
    ServiceC->>ServiceC: Process step 3

    ServiceC->>Destination: Final output
    Destination-->>ServiceC: Confirmed

    Note over Source,Destination: Complete pipeline execution<br/>Total time: ~50 seconds
```

### Template: Publish-Subscribe Pattern

```mermaid
sequenceDiagram
    participant EventSource as Event<br/>Source
    participant EventBus as Event Bus<br/>(RabbitMQ/Kafka)
    participant Subscriber1 as Service<br/>Subscriber 1
    participant Subscriber2 as Service<br/>Subscriber 2

    EventSource->>EventBus: Publish event

    EventBus-->>Subscriber1: Event notification
    EventBus-->>Subscriber2: Event notification

    Subscriber1->>Subscriber1: Handle event
    Subscriber2->>Subscriber2: Handle event

    Note over EventBus: Non-blocking<br/>All subscribers process<br/>independently
```

### Template: Saga Pattern (Distributed Transaction)

```mermaid
sequenceDiagram
    participant Orchestrator as Orchestrator<br/>Service
    participant ServiceA as ServiceA
    participant ServiceB as ServiceB
    participant ServiceC as ServiceC

    Orchestrator->>ServiceA: Step 1 - Execute

    ServiceA->>ServiceA: Process
    ServiceA-->>Orchestrator: Success / Failure

    alt Success
        Orchestrator->>ServiceB: Step 2 - Execute
        ServiceB->>ServiceB: Process
        ServiceB-->>Orchestrator: Success
    else Failure
        Orchestrator->>ServiceA: Step 1 - Compensate<br/>(rollback)
        ServiceA-->>Orchestrator: Rolled back
    end

    Orchestrator->>ServiceC: Step 3 - Execute
    ServiceC-->>Orchestrator: Response

    Note over Orchestrator: Ensures consistency across<br/>multiple services
```

---

## 5. Lifecycle & State Changes

### Template: Model/Version Lifecycle

```mermaid
sequenceDiagram
    participant Admin as Admin/User
    participant ConfigService as MS15<br/>Config
    participant WorkerService as MSxx<br/>Worker
    participant DB as PostgreSQL<br/>DB
    participant Monitor as MS08<br/>Monitor

    Admin->>ConfigService: Deploy new version<br/>(v2.2)

    ConfigService->>DB: Create version record<br/>(inactive)
    DB-->>ConfigService: Created

    ConfigService->>Monitor: Start monitoring<br/>v2.2 performance

    Monitor->>Monitor: A/B test for 24h

    alt Performance OK
        Monitor->>ConfigService: v2.2 is better
        ConfigService->>DB: Activate v2.2
        ConfigService->>DB: Deprecate v2.1
        ConfigService->>WorkerService: Load new version
        WorkerService->>WorkerService: Switch active version
    else Performance Bad
        Monitor->>ConfigService: v2.2 failed
        ConfigService-->>Admin: Deployment failed
    end

    Monitor-->>Admin: Completion alert
```

### Template: Data Migration/Upgrade

```mermaid
sequenceDiagram
    participant Admin as Admin
    participant MigrationService as Migration<br/>Service
    participant SourceDB as Source<br/>DB
    participant TargetDB as Target<br/>DB
    participant Monitor as Monitoring

    Admin->>MigrationService: Initiate migration

    MigrationService->>SourceDB: Read data<br/>(batch)
    SourceDB-->>MigrationService: Data chunk

    MigrationService->>MigrationService: Transform data

    MigrationService->>TargetDB: Write data
    TargetDB-->>MigrationService: Confirmed

    MigrationService->>Monitor: Report progress
    Monitor-->>Monitor: Track metrics

    loop Until all data migrated
        MigrationService->>SourceDB: Next batch
    end

    Admin-->>Admin: Verify completion
```

---

## 6. Async Processing

### Template: Background Job Queue

```mermaid
sequenceDiagram
    participant Client
    participant Service as MSxx<br/>Service
    participant Queue as Job Queue<br/>(RabbitMQ)
    participant Worker as Background<br/>Worker

    Client->>Service: Submit job<br/>POST /jobs

    Service->>Queue: Queue job<br/>(async)
    Queue-->>Service: Job ID: job-123

    Service-->>Client: 202 Accepted<br/>job_id: job-123<br/>(FAST ⚡)

    Queue->>Worker: Deliver job
    Worker->>Worker: Process job<br/>(long running)
    Worker->>Worker: Update status<br/>(PROCESSING)

    Client->>Service: Poll status<br/>GET /jobs/job-123
    Service-->>Client: Status: PROCESSING

    Worker->>Worker: Job complete
    Worker->>Service: Update status<br/>(COMPLETED)

    Client->>Service: Poll status<br/>GET /jobs/job-123
    Service-->>Client: Status: COMPLETED<br/>Results: {...}

    Note over Client,Worker: Client polls for completion<br/>or uses WebSocket for push updates
```

### Template: Event-Driven Processing

```mermaid
sequenceDiagram
    participant EventSource as Event<br/>Source
    participant EventBus as Event Bus<br/>(Kafka)
    participant Consumer as Async<br/>Consumer
    participant DB as Database

    EventSource->>EventBus: Emit event<br/>(document.classified)

    Note over EventBus: Event stored in topic<br/>Multiple consumers can<br/>process independently

    Consumer->>EventBus: Subscribe to topic<br/>(consumer group)
    EventBus->>Consumer: Deliver event<br/>(with offset)

    Consumer->>Consumer: Process event<br/>(async, non-blocking)

    Consumer->>DB: Store result
    DB-->>Consumer: Confirmed

    Consumer->>EventBus: Commit offset<br/>(mark processed)

    Note over Consumer: Next startup will<br/>resume from this offset
```

### Template: Scheduled Task (Batch Processing)

```mermaid
sequenceDiagram
    participant Scheduler as Scheduler<br/>(Cron/APScheduler)
    participant Service as MSxx<br/>Service
    participant DB as PostgreSQL<br/>DB
    participant Monitor as Monitoring

    Scheduler->>Scheduler: Time trigger<br/>(daily 2am)

    Scheduler->>Service: Execute batch job

    Service->>DB: Query data<br/>(all records)
    DB-->>Service: Large dataset

    Service->>Service: Process in batches<br/>(1000 per iteration)

    loop Process all batches
        Service->>Service: Transform batch
        Service->>DB: Update batch
        Service->>Monitor: Report progress
    end

    Service-->>Scheduler: Job completed
    Monitor-->>Scheduler: Completion alert
```

---

## 🎓 Best Practices

### 1. **Clarity**
- Use descriptive labels on arrows
- Include what data/message is passed
- Show response values (not just 200 OK)

### 2. **Error Handling**
- Show both success AND failure paths
- Use `--x` for errors/exceptions
- Include error codes (404, 500, etc.)

### 3. **Performance**
- Annotate latency where relevant
- Show caching/optimization paths
- Include alternative faster paths

### 4. **Security**
- Show authentication/authorization checks
- Indicate encryption/validation steps
- Mark sensitive data handling

### 5. **Readability**
- Keep diagrams focused (max 6-8 participants)
- Use `alt`/`loop`/`opt` for conditional logic
- Break complex flows into multiple diagrams

---

## 🚀 How to Use These Templates

### For MS (Microservice) Documentation

1. Copy the appropriate template above
2. Replace generic names with your MS/service names
3. Adapt flow to match your actual implementation
4. Add error paths and alternatives
5. Update timing/latency estimates

### For SP (Sub-Project) Documentation

1. Use integration flow templates for SP-to-SP interactions
2. Show how SP integrates with parent UC
3. Include data transformation steps
4. Add validation/quality checks

### Example: Adding to SPECIFICATION.md

```markdown
## Sequence Diagrams

### Main Flow: Feature X (Happy Path)

[paste mermaid diagram from template]

### Alternative: Cache Hit Optimization

[paste cache template]

### Error: Validation Failure

[paste validation error template]
```

---

## 📝 Mermaid Syntax Quick Reference

```mermaid
sequenceDiagram
    participant A
    participant B

    A->>B: Sync call
    A-->>B: Async response
    A-xB: Sync call with error
    B--xA: Async error

    opt Optional block
        A->>B: Message
    end

    alt Success path
        A->>B: Do this
    else Error path
        A->>B: Do that
    end

    loop Repeat
        A->>B: Message
    end

    Note over A,B: Comment/annotation
```

---

## 📚 Dove Aggiungere i Diagrammi

| Documento | Pattern | Esempio |
|-----------|---------|---------|
| SPECIFICATION.md | Main flow, alternative paths, error flows | MS01: Classification, cache hit, low confidence |
| DATABASE-SCHEMA.md | Data lifecycle, state changes | Model versioning, data migration |
| TROUBLESHOOTING.md | Error flows, recovery paths | Timeout handling, retry logic |
| API.md | Request-response flows | Simple client-server interaction |

---

**Versione**: 1.0
**Creato**: 2024-11-18
**Lingua**: Italiano/English (Mermaid syntax universal)
