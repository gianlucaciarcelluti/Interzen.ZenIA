# 01 Sequence diagrams - UC7 Sistema di Gestione Archivio e Conservazione

## Diagramma Completo Workflow Archiviazione

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant AM as SP33 Archive Manager
    participant PE as SP34 Preservation Engine
    participant IV as SP35 Integrity Validator
    participant SO as SP36 Storage Optimizer
    participant DB as PostgreSQL
    participant ES as Elasticsearch
    participant MINIO as MinIO Storage
    participant REDIS as Redis Cache

    Note over U,REDIS: Document Archival Workflow

    U->>FE: Submit document for archival
    FE->>AM: POST /api/v1/documents/archive

    AM->>DB: Validate document metadata
    DB-->>AM: Metadata validation result

    AM->>IV: Request integrity validation
    IV->>IV: Calculate SHA-256 hash
    IV->>DB: Store fixity information
    IV-->>AM: Integrity validation complete

    AM->>SO: Request storage optimization
    SO->>SO: Analyze content for compression
    SO->>SO: Apply deduplication if beneficial
    SO->>SO: Determine optimal storage tier
    SO-->>AM: Optimization recommendations

    AM->>PE: Request preservation metadata enrichment
    PE->>PE: Extract document features
    PE->>PE: Classify content type
    PE->>PE: Generate preservation metadata
    PE-->>AM: Enriched metadata

    AM->>MINIO: Store optimized document
    MINIO-->>AM: Storage confirmation

    AM->>ES: Index document for search
    ES-->>AM: Indexing confirmation

    AM->>DB: Update document status
    AM->>REDIS: Cache document metadata

    AM-->>FE: Archival complete response
    FE-->>U: Success notification
```

## Diagramma Preservation Monitoring

```mermaid
sequenceDiagram
    participant SCH as Scheduler
    participant PE as SP34 Preservation Engine
    participant IV as SP35 Integrity Validator
    participant DB as PostgreSQL
    participant MINIO as MinIO Storage
    participant ALERT as Alert Engine

    Note over SCH,ALERT: Preservation Monitoring Workflow

    SCH->>PE: Trigger preservation check
    PE->>DB: Get documents due for check
    DB-->>PE: Document list

    loop For each document
        PE->>PE: Assess preservation risk
        PE->>IV: Request integrity validation
        IV->>MINIO: Retrieve document content
        MINIO-->>IV: Document content

        IV->>IV: Verify fixity (hash comparison)
        IV-->>PE: Integrity result

        alt Integrity violation detected
            PE->>ALERT: Send integrity alert
            ALERT->>ALERT: Escalate based on severity
        end

        PE->>PE: Check format obsolescence
        alt Format needs migration
            PE->>PE: Select migration strategy
            PE->>MINIO: Retrieve original document
            MINIO-->>PE: Document content

            PE->>PE: Convert to new format
            PE->>PE: Validate conversion quality
            PE->>MINIO: Store migrated document
            PE->>DB: Update preservation metadata
        end

        PE->>DB: Update preservation status
    end

    PE-->>SCH: Preservation cycle complete
```

## Diagramma Retrieval Ottimizzato

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant AM as SP33 Archive Manager
    participant SO as SP36 Storage Optimizer
    participant DB as PostgreSQL
    participant REDIS as Redis Cache
    participant MINIO as MinIO Storage
    participant ES as Elasticsearch

    Note over U,ES: Document Retrieval Workflow

    U->>FE: Request document retrieval
    FE->>AM: GET /api/v1/documents/{id}

    AM->>REDIS: Check metadata cache
    alt Cache hit
        REDIS-->>AM: Cached metadata
    else Cache miss
        AM->>DB: Retrieve document metadata
        DB-->>AM: Document metadata
        AM->>REDIS: Cache metadata
    end

    AM->>AM: Check access permissions
    alt Access granted
        AM->>SO: Get storage location & tier
        SO-->>AM: Storage information

        AM->>MINIO: Retrieve document from tier
        MINIO-->>AM: Document content

        alt Document compressed
            AM->>SO: Request decompression
            SO->>SO: Decompress content
            SO-->>AM: Decompressed content
        end

        alt Document deduplicated
            AM->>SO: Request reconstruction
            SO->>SO: Reconstruct from chunks
            SO-->>AM: Reconstructed content
        end

        AM->>AM: Log access event
        AM->>DB: Update access statistics

        AM-->>FE: Document content
        FE-->>U: Document download
    else Access denied
        AM-->>FE: Access denied error
        FE-->>U: Permission error
    end
```

## Diagramma Storage Tiering Automatico

```mermaid
sequenceDiagram
    participant SCH as Scheduler
    participant SO as SP36 Storage Optimizer
    participant DB as PostgreSQL
    participant ANALYTICS as Access Analytics
    participant HOT as Hot Storage (NVMe)
    participant WARM as Warm Storage (SSD)
    participant COLD as Cold Storage (HDD)
    participant ARCHIVE as Archive Storage (Tape)

    Note over SCH,ARCHIVE: Automatic Storage Tiering

    SCH->>SO: Trigger tiering analysis
    SO->>DB: Get documents for tiering evaluation
    DB-->>SO: Document list with metadata

    loop For each document
        SO->>ANALYTICS: Analyze access patterns
        ANALYTICS-->>SO: Access pattern analysis

        SO->>SO: Determine optimal tier
        Note right of SO: Based on access frequency,<br/>retention policy, content type

        alt Needs tier migration
            SO->>SO: Create migration task
            SO->>DB: Update migration status

            alt From Hot to Warm
                SO->>HOT: Retrieve document
                HOT-->>SO: Document content
                SO->>WARM: Store in warm tier
                WARM-->>SO: Storage confirmation
                SO->>HOT: Mark for deletion
            else From Warm to Cold
                SO->>WARM: Retrieve document
                WARM-->>SO: Document content
                SO->>COLD: Store in cold tier
                COLD-->>SO: Storage confirmation
                SO->>WARM: Mark for deletion
            else From Cold to Archive
                SO->>COLD: Retrieve document
                COLD-->>SO: Document content
                SO->>ARCHIVE: Store in archive tier
                ARCHIVE-->>SO: Storage confirmation
                SO->>COLD: Mark for deletion
            end

            SO->>DB: Update document tier
            SO->>DB: Log migration event
        end
    end

    SO-->>SCH: Tiering cycle complete
```

## Diagramma Capacity Planning

```mermaid
sequenceDiagram
    participant SCH as Scheduler
    participant SO as SP36 Storage Optimizer
    participant MONITOR as Storage Monitor
    participant FORECAST as Forecasting Engine
    participant DB as PostgreSQL
    participant ALERT as Alert Engine

    Note over SCH,ALERT: Capacity Planning Workflow

    SCH->>SO: Trigger capacity analysis
    SO->>MONITOR: Get current storage metrics
    MONITOR-->>SO: Current usage statistics

    SO->>DB: Retrieve historical growth data
    DB-->>SO: Historical usage data

    SO->>FORECAST: Generate capacity forecast
    FORECAST->>FORECAST: Apply forecasting model
    FORECAST-->>SO: Capacity predictions

    SO->>SO: Analyze forecast vs thresholds
    alt Capacity alert needed
        SO->>ALERT: Generate capacity alert
        ALERT->>ALERT: Route to appropriate channels
    end

    SO->>SO: Generate capacity recommendations
    Note right of SO: Expansion, optimization,<br/>cleanup strategies

    SO->>DB: Store forecast results
    SO->>DB: Update capacity metrics

    SO-->>SCH: Capacity planning complete
```

## Diagramma Integrity Validation Completo

```mermaid
sequenceDiagram
    participant SCH as Scheduler
    participant IV as SP35 Integrity Validator
    participant DB as PostgreSQL
    participant MINIO as MinIO Storage
    participant DSS as DSS Framework
    participant OCSP as OCSP Responder
    participant TSA as Timestamp Authority
    participant ALERT as Alert Engine

    Note over SCH,ALERT: Complete Integrity Validation

    SCH->>IV: Trigger integrity validation
    IV->>DB: Get documents for validation
    DB-->>IV: Document batch

    loop For each document
        IV->>MINIO: Retrieve document content
        MINIO-->>IV: Document content

        IV->>IV: Calculate current hash
        IV->>DB: Compare with stored hash

        alt Hash mismatch
            IV->>ALERT: Integrity violation alert
            ALERT->>ALERT: Critical alert escalation
        end

        alt Document has signatures
            IV->>DSS: Validate digital signatures
            DSS->>OCSP: Check certificate revocation
            OCSP-->>DSS: Revocation status
            DSS-->>IV: Signature validation result

            alt Signature invalid
                IV->>ALERT: Signature violation alert
            end
        end

        alt Document has timestamp
            IV->>TSA: Validate RFC 3161 timestamp
            TSA-->>IV: Timestamp validation result

            alt Timestamp invalid
                IV->>ALERT: Timestamp violation alert
            end
        end

        IV->>IV: Update chain of custody
        IV->>DB: Store validation results
    end

    IV-->>SCH: Validation cycle complete
```

## Diagramma Ultra-Semplificato Archiviazione

```mermaid
sequenceDiagram
    participant User
    participant ArchiveManager
    participant Storage
    participant Database

    User->>ArchiveManager: Archive Document
    ArchiveManager->>ArchiveManager: Validate & Optimize
    ArchiveManager->>Storage: Store Document
    ArchiveManager->>Database: Save Metadata
    ArchiveManager-->>User: Success
```

## Workflow di Emergenza e Recovery

```mermaid
sequenceDiagram
    participant MONITOR as Storage Monitor
    participant ALERT as Alert Engine
    participant RECOVERY as Recovery Manager
    participant BACKUP as Backup System
    participant REPLICATION as Replication Service

    Note over MONITOR,REPLICATION: Disaster Recovery Workflow

    MONITOR->>MONITOR: Detect storage failure
    MONITOR->>ALERT: Trigger disaster alert

    ALERT->>RECOVERY: Initiate recovery procedures
    RECOVERY->>BACKUP: Identify latest backup
    BACKUP-->>RECOVERY: Backup information

    RECOVERY->>REPLICATION: Check replica status
    REPLICATION-->>RECOVERY: Replica health

    alt Replica available
        RECOVERY->>REPLICATION: Failover to replica
        REPLICATION-->>RECOVERY: Failover complete
    else Replica unavailable
        RECOVERY->>BACKUP: Initiate restore
        BACKUP->>BACKUP: Restore from backup
        BACKUP-->>RECOVERY: Restore complete
    end

    RECOVERY->>RECOVERY: Validate data integrity
    RECOVERY->>ALERT: Send recovery notification

    RECOVERY-->>MONITOR: Recovery complete
```

## Metriche e Monitoraggio

### Performance Metrics Flow
```mermaid
graph TD
    A[Document Archived] --> B[Measure Archive Time]
    B --> C[Update Performance Metrics]
    C --> D{Check Thresholds}
    D -->|Exceeded| E[Generate Alert]
    D -->|OK| F[Continue Monitoring]

    G[Integrity Check] --> H[Measure Check Time]
    H --> I[Update Integrity Metrics]
    I --> J{Analysis Needed}
    J -->|Yes| K[Trigger Deep Analysis]
    J -->|No| L[Continue Checks]

    M[Storage Operation] --> N[Measure I/O Performance]
    N --> O[Update Storage Metrics]
    O --> P{Optimization Needed}
    P -->|Yes| Q[Trigger Optimization]
    P -->|No| R[Continue Operations]
```

### Alert Escalation Flow
```mermaid
graph TD
    A[Alert Detected] --> B{Determine Severity}
    B -->|Critical| C[Immediate Escalation]
    B -->|High| D[Management Alert]
    B -->|Medium| E[Team Notification]
    B -->|Low| F[Log Only]

    C --> G[Pager Alert]
    D --> H[Email + Slack]
    E --> I[Slack Notification]
    F --> J[Central Logging]

    G --> K[Incident Response]
    H --> L[Review Meeting]
    I --> M[Daily Report]
    J --> N[Weekly Review]
```</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC7 - Sistema di Gestione Archivio e Conservazione/01 Sequence diagrams.md
