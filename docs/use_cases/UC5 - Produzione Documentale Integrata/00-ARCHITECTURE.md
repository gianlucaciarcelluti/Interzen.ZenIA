# Architettura Generale Microservizi ZenShareUp

## Diagramma Architettura Generale

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Web UI Dashboard]
        API_GW[API Gateway]
        HITL_UI[HITL Interface<br/>Human in the Loop]
    end
    
    subgraph "Application Services"
        WF[SP09 - Workflow Engine<br/>Apache NiFi]
        DASH[SP10 - Explainability<br/>Dashboard]
        HITL_MGR[HITL Manager<br/>Decision Tracking]
    end
    
    subgraph "Input Processing Layer"
        EML[SP01 - EML Parser<br/>Email Intelligence]
        DOC_EXT[SP02 - Document Extractor<br/>OCR/Attachment Classifier]
    end
    
    subgraph "Core AI Services"
        PROC[SP03 - Classificatore Procedurale<br/>DistilBERT/spaCy]
        KB[SP04 - Knowledge Base<br/>RAG/Mistral]
        TPL[SP05 - Template Engine<br/>GPT-4/LangChain]
        VAL[SP06 - Validatore<br/>BERT/RoBERTa]
        CLS[SP07 - Classifier<br/>DistilBERT/spaCy]
        QC[SP08 - Quality Checker<br/>LanguageTool/spaCy]
    end
    
    subgraph "Cross-Cutting Services"
        SEC[SP11 - Security & Audit<br/>Isolation Forest/Vault]
        MON[Monitoring<br/>Grafana/Prometheus]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Metadata/Audit)]
        VDB[(Vector DB<br/>FAISS/Pinecone)]
        GRAPH[(Neo4j<br/>Knowledge Graph)]
        REDIS[(Redis<br/>Cache)]
        MINIO[(MinIO<br/>Documents/Attachments)]
        HITL_DB[(PostgreSQL<br/>HITL Tracking)]
    end
    
    subgraph "External Systems"
        PROT[Sistema Protocollo]
        FIRMA[Firma Digitale]
        PEC[Gestione PEC]
        DOC[Documentale]
    end
    
    UI --> API_GW
    HITL_UI --> API_GW
    API_GW --> WF
    API_GW --> DASH
    API_GW --> HITL_MGR
    
    PEC --> WF
    WF --> EML
    EML --> DOC_EXT
    DOC_EXT --> PROC
    
    WF --> HITL_MGR
    HITL_MGR --> HITL_UI
    
    WF --> PROC
    WF --> TPL
    WF --> VAL
    WF --> CLS
    WF --> QC
    WF --> KB
    
    PROC --> KB
    TPL --> KB
    TPL --> CLS
    VAL --> KB
    VAL --> CLS
    CLS --> QC
    
    DASH --> EML
    DASH --> DOC_EXT
    DASH --> PROC
    DASH --> TPL
    DASH --> VAL
    DASH --> CLS
    DASH --> QC
    DASH --> KB
    
    SEC -.->|Audit| EML
    SEC -.->|Audit| DOC_EXT
    SEC -.->|Audit| PROC
    SEC -.->|Audit| TPL
    SEC -.->|Audit| VAL
    SEC -.->|Audit| CLS
    SEC -.->|Audit| QC
    SEC -.->|Audit| KB
    
    MON -.->|Metrics| WF
    MON -.->|Metrics| EML
    MON -.->|Metrics| DOC_EXT
    MON -.->|Metrics| PROC
    MON -.->|Metrics| TPL
    MON -.->|Metrics| VAL
    MON -.->|Metrics| CLS
    MON -.->|Metrics| QC
    MON -.->|Metrics| KB
    
    EML --> PG
    EML --> MINIO
    DOC_EXT --> PG
    DOC_EXT --> MINIO
    PROC --> PG
    TPL --> PG
    VAL --> PG
    CLS --> PG
    KB --> VDB
    KB --> GRAPH
    PROC --> REDIS
    TPL --> REDIS
    VAL --> REDIS
    KB --> REDIS
    PROC --> MINIO
    CLS --> MINIO
    TPL --> MINIO
    SEC --> PG
    
    HITL_MGR --> HITL_DB
    HITL_MGR --> MINIO
    
    WF --> PROT
    WF --> FIRMA
    WF --> DOC
    
    style EML fill:#ffd700
    style DOC_EXT fill:#ffd700
    style PROC fill:#e1f5ff
    style TPL fill:#e1f5ff
    style VAL fill:#e1f5ff
    style KB fill:#e1f5ff
    style CLS fill:#e1f5ff
    style QC fill:#e1f5ff
    style WF fill:#fff3cd
    style SEC fill:#f8d7da
    style DASH fill:#d4edda
    style HITL_MGR fill:#ffeb3b
    style HITL_UI fill:#ffeb3b
    style HITL_DB fill:#ffeb3b
```

## Stack Tecnologico per Microservizio

| Microservizio | Linguaggio | Framework | Database | Message Queue | Container |
|--------------|-----------|-----------|----------|---------------|-----------|
| SP01 - EML Parser & Email Intelligence | Python | FastAPI | PostgreSQL + MinIO | NiFi FlowFiles | Docker |
| SP02 - Document Extractor & Classifier | Python | FastAPI | PostgreSQL + MinIO | NiFi FlowFiles | Docker |
| SP03 - Classificatore Procedurale | Python | FastAPI | PostgreSQL + MinIO | NiFi FlowFiles | Docker |
| SP04 - Legal Knowledge Base | Python | FastAPI | FAISS + Neo4j | NiFi FlowFiles | Docker |
| SP05 - Template Engine | Python | FastAPI | PostgreSQL | NiFi FlowFiles | Docker |
| SP06 - Validatore | Python | FastAPI | PostgreSQL | NiFi FlowFiles | Docker |
| SP07 - Content Classifier | Python | FastAPI | PostgreSQL + MinIO | NiFi FlowFiles | Docker |
| SP08 - Quality Checker | Python | FastAPI | Redis | NiFi FlowFiles | Docker |
| SP09 - Workflow Engine | Python | Apache NiFi | PostgreSQL | - | Docker |
| SP10 - Explainability Dashboard | Python | Streamlit | PostgreSQL | - | Docker |
| SP11 - Security & Audit | Python | FastAPI | PostgreSQL | NiFi FlowFiles | Docker |
| **HITL Manager** | **Python** | **FastAPI** | **PostgreSQL** | **NiFi FlowFiles** | **Docker** |

## Comunicazione tra Microservizi

### Pattern Architetturali

1. **Comunicazione Sincrona**: REST API via HTTP
2. **Comunicazione Asincrona**: Event-driven via Apache NiFi flow files
3. **Service Mesh**: Istio per resilienza e osservabilità  
4. **Circuit Breaker**: Pattern integrato in NiFi processors
5. **API Gateway**: Kong/Ambassador per routing e rate limiting

### Event Bus (Apache NiFi FlowFiles)

Apache NiFi gestisce il routing degli eventi tramite **FlowFiles** che vengono processati attraverso i vari Process Groups. Ogni evento mantiene gli attributi e può essere tracciato completamente tramite **Data Provenance**.

```mermaid
graph LR
    subgraph "NiFi Flow"
        T0[email.received]
        T1[email.parsed]
        T2[documents.extracted]
        T3[procedure.classified]
        T4[document.classified]
        T5[document.validated]
        T6[document.generated]
        T7[quality.checked]
        T8[workflow.completed]
        T9[security.alert]
        T10[hitl.decision.pending]
        T11[hitl.decision.submitted]
        T12[hitl.modification.applied]
    end
    
    EML -->|Publish| T1
    DOC_EXT -->|Publish| T2
    PROC -->|Publish| T3
    CLS -->|Publish| T4
    TPL -->|Publish| T6
    VAL -->|Publish| T5
    QC -->|Publish| T7
    WF -->|Publish| T8
    SEC -->|Publish| T9
    
    T0 -->|Subscribe| EML
    T1 -->|Subscribe| DOC_EXT
    T2 -->|Subscribe| PROC
    T4 -->|Subscribe| TPL
    T4 -->|Subscribe| VAL
    T6 -->|Subscribe| VAL
    T6 -->|Subscribe| QC
    T5 -->|Subscribe| WF
    T7 -->|Subscribe| WF
    
    style T0 fill:#ffd700
    style T1 fill:#ffd700
    style T2 fill:#ffd700
    style T3 fill:#e1f5ff
    style T4 fill:#e1f5ff
    style T5 fill:#e1f5ff
    style T6 fill:#e1f5ff
    style T7 fill:#e1f5ff
    style T8 fill:#d4edda
    style T9 fill:#f8d7da
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        subgraph "Namespace: ai-services"
            POD1[SP01 Pod<br/>3 replicas]
            POD2[SP02 Pod<br/>2 replicas]
            POD3[SP03 Pod<br/>2 replicas]
            POD4[SP04 Pod<br/>3 replicas]
            POD5[SP05 Pod<br/>2 replicas]
        end
        
        subgraph "Namespace: workflow"
            POD6[SP06 Pod<br/>2 replicas]
            POD7[SP07 Pod<br/>1 replica]
        end
        
        subgraph "Namespace: security"
            POD8[SP08 Pod<br/>2 replicas]
        end
        
        subgraph "Namespace: data"
            STS1[PostgreSQL StatefulSet]
            STS2[Redis StatefulSet]
            STS3[ZooKeeper StatefulSet<br/>for NiFi Clustering]
        end
    end
    
    subgraph "External Services"
        LB[Load Balancer]
        INGRESS[Ingress Controller]
    end
    
    LB --> INGRESS
    INGRESS --> POD1
    INGRESS --> POD2
    INGRESS --> POD3
    INGRESS --> POD4
    INGRESS --> POD5
    INGRESS --> POD6
    INGRESS --> POD7
    
    POD1 --> STS1
    POD2 --> STS1
    POD3 --> STS1
    POD4 --> STS1
    POD6 --> STS3
    
    POD8 -.->|Monitor| POD1
    POD8 -.->|Monitor| POD2
    POD8 -.->|Monitor| POD3
    POD8 -.->|Monitor| POD4
    POD8 -.->|Monitor| POD5
    POD8 -.->|Monitor| POD6
```

## Service Mesh Configuration (Istio)

```yaml
# Esempio configurazione Istio per retry e circuit breaker
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: template-engine-circuit-breaker
spec:
  host: sp05-template-engine
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        http2MaxRequests: 100
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 40
```

## Scalabilità e Resilienza

### Horizontal Pod Autoscaling (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sp05-template-engine-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sp05-template-engine
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
```

### Priorità di Scaling

| Servizio | Min Replicas | Max Replicas | Priorità | Motivo |
|----------|-------------|-------------|----------|---------|
| SP01 - EML Parser | 2 | 8 | Alta | Entry point email, parsing PEC |
| SP02 - Document Extractor | 3 | 12 | Alta | OCR CPU-intensive, alto traffico allegati |
| SP03 - Classificatore Procedurale | 3 | 10 | Alta | Classificazione critica |
| SP05 - Template Engine | 3 | 10 | Alta | CPU intensive (LLM) |
| SP06 - Validatore | 2 | 8 | Media | Validation critica |
| SP04 - Knowledge Base | 2 | 6 | Media | RAG queries frequenti |
| SP08 - Quality Checker | 2 | 5 | Bassa | Non bloccante |
| SP09 - Workflow Engine | 2 | 4 | Media | Orchestrazione critica |
| SP11 - Security & Audit | 2 | 4 | Alta | Always-on monitoring |

## Monitoring e Observability Stack

```mermaid
graph TB
    subgraph "Microservizi"
        SVC[Tutti i Servizi SP01-SP11]
    end
    
    subgraph "Metrics Collection"
        PROM[Prometheus]
        METRICS[Service Metrics]
    end
    
    subgraph "Logging"
        FLUENT[Fluentd]
        ES[Elasticsearch]
        KIB[Kibana]
    end
    
    subgraph "Tracing"
        JAEGER[Jaeger]
        TRACES[Distributed Traces]
    end
    
    subgraph "Visualization"
        GRAF[Grafana]
        ALERT[AlertManager]
    end
    
    SVC -->|Metrics| PROM
    SVC -->|Logs| FLUENT
    SVC -->|Traces| JAEGER
    
    PROM --> METRICS
    FLUENT --> ES
    ES --> KIB
    JAEGER --> TRACES
    
    METRICS --> GRAF
    TRACES --> GRAF
    PROM --> ALERT
    
    ALERT -->|Slack/Email| TEAM[Ops Team]
    
    style SVC fill:#e1f5ff
    style GRAF fill:#d4edda
    style ALERT fill:#f8d7da
```

## Key Metrics da Monitorare

### Service Level Indicators (SLI)

| Categoria | Metrica | Target | Alert Threshold |
|-----------|---------|--------|-----------------|
| **Latency** | P50 response time | <500ms | >1s |
| **Latency** | P95 response time | <2s | >5s |
| **Latency** | P99 response time | <5s | >10s |
| **Availability** | Uptime | >99.9% | <99.5% |
| **Throughput** | Requests/sec | >100 | <50 |
| **Errors** | Error rate | <1% | >3% |
| **Saturation** | CPU usage | <70% | >85% |
| **Saturation** | Memory usage | <80% | >90% |
| **Queue** | NiFi FlowFiles queue depth | <1000 FlowFiles | >10000 FlowFiles |

### Business Metrics

| Metrica | Descrizione | Target |
|---------|-------------|--------|
| Email Processing Rate | Email/ora processate | >500 |
| Document Extraction Success | % allegati estratti correttamente | >95% |
| OCR Accuracy | % accuratezza riconoscimento testo | >92% |
| Document Processing Rate | Documenti/ora elaborati | >1000 |
| Template Generation Success | % generazioni accettate | >90% |
| Validation Accuracy | % validazioni corrette | >95% |
| Average Processing Time | Tempo totale email→atto | <45s |
| Human Intervention Rate | % documenti richiede review | <10% |
| PEC Signature Validation | % firme digitali validate | 100% |

## Disaster Recovery e Backup

### Strategia di Backup

```mermaid
graph LR
    subgraph "Production"
        PROD_DB[(PostgreSQL<br/>Primary)]
        PROD_VDB[(Vector DB<br/>Primary)]
        PROD_GRAPH[(Neo4j<br/>Primary)]
    end
    
    subgraph "Standby (Sync Replication)"
        STAND_DB[(PostgreSQL<br/>Standby)]
        STAND_VDB[(Vector DB<br/>Standby)]
        STAND_GRAPH[(Neo4j<br/>Standby)]
    end
    
    subgraph "Backup Storage"
        S3[(S3/MinIO<br/>Backups)]
        SNAP[Volume<br/>Snapshots]
    end
    
    PROD_DB -->|Streaming Replication| STAND_DB
    PROD_VDB -->|Replication| STAND_VDB
    PROD_GRAPH -->|Replication| STAND_GRAPH
    
    PROD_DB -->|Daily Backup| S3
    PROD_VDB -->|Daily Backup| S3
    PROD_GRAPH -->|Daily Backup| S3
    
    PROD_DB -->|Hourly Snapshot| SNAP
    
    style PROD_DB fill:#d4edda
    style STAND_DB fill:#fff3cd
    style S3 fill:#e1f5ff
```

### Recovery Time Objective (RTO) e Recovery Point Objective (RPO)

| Sistema | RPO | RTO | Strategia |
|---------|-----|-----|-----------|
| PostgreSQL (transactional) | <5 min | <15 min | Streaming replication + PITR |
| Vector DB (ricreabile) | <1 ora | <2 ore | Daily backup + rebuild |
| Neo4j (knowledge graph) | <15 min | <30 min | Continuous backup |
| MinIO (documents) | <1 ora | <1 ora | Multi-region replication |
| Apache NiFi (workflow orchestrator) | <5 min | <10 min | 3-node cluster |
| ZooKeeper (NiFi coordination) | <2 min | <5 min | 3-node ensemble |

## Security Architecture

### Defense in Depth

```mermaid
graph TB
    subgraph "Layer 1: Perimeter"
        WAF[Web Application Firewall]
        DDOS[DDoS Protection]
    end
    
    subgraph "Layer 2: Network"
        FW[Network Firewall]
        VPN[VPN Gateway]
    end
    
    subgraph "Layer 3: Application"
        OAUTH[OAuth 2.0 / OIDC]
        JWT[JWT Validation]
        RBAC[Role-Based Access]
    end
    
    subgraph "Layer 4: Data"
        ENCRYPT[Encryption at Rest]
        TLS[TLS in Transit]
        MASK[Data Masking]
    end
    
    subgraph "Layer 5: Monitoring"
        SIEM[SIEM - SP08]
        IDS[Intrusion Detection]
        AUDIT[Audit Logging]
    end
    
    WAF --> FW
    DDOS --> FW
    FW --> OAUTH
    VPN --> OAUTH
    OAUTH --> JWT
    JWT --> RBAC
    RBAC --> ENCRYPT
    RBAC --> TLS
    ENCRYPT --> MASK
    
    SIEM -.->|Monitor| WAF
    SIEM -.->|Monitor| FW
    SIEM -.->|Monitor| OAUTH
    SIEM -.->|Monitor| ENCRYPT
    IDS -.->|Detect| FW
    AUDIT -.->|Log| RBAC
    
    style WAF fill:#f8d7da
    style SIEM fill:#f8d7da
    style ENCRYPT fill:#d4edda
```

### Secrets Management

```yaml
# HashiCorp Vault integration
apiVersion: v1
kind: Secret
metadata:
  name: vault-secrets
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "zenshare-ai"
    vault.hashicorp.com/agent-inject-secret-database: "database/creds/postgres"
    vault.hashicorp.com/agent-inject-secret-openai: "secret/openai/api-key"
```

## Costi Operativi Stimati (Mensili)

| Risorsa | Dimensione | Costo Mensile (€) | Note |
|---------|-----------|-------------------|------|
| **Compute (Kubernetes)** | 16 vCPU, 64GB RAM | 400 | 8 nodi worker |
| **GPU (per LLM on-premise)** | 2x RTX 4090 | 150 | Elettricità + ammortamento |
| **Database (PostgreSQL)** | 500GB SSD | 100 | Managed service |
| **Vector DB (Pinecone)** | 100M vectors | 70 | O self-hosted FAISS (€0) |
| **Redis Cache** | 16GB | 50 | Managed |
| **MinIO Storage** | 5TB | 80 | Object storage |
| **Apache NiFi** | 3-node cluster | 180 | Managed |
| **ZooKeeper** | 3-node ensemble | 30 | Managed |
| **Monitoring Stack** | Prometheus+Grafana | 60 | Self-hosted |
| **LLM API (sviluppo)** | Groq free tier | 0-50 | Free tier poi pay-as-you-go |
| **Network/Traffic** | 2TB/mese | 40 | Egress costs |
| **Backup Storage** | 10TB | 50 | S3-compatible |
| **Total** | | **1,120-1,170 €/mese** | ~14k €/anno |

### Alternative On-Premise vs Cloud

| Componente | On-Premise (1 anno) | Cloud (1 anno) | Break-even |
|-----------|---------------------|----------------|------------|
| Infrastruttura completa | 15k capex + 2k opex = **17k €** | 14k €/anno | 12-14 mesi |
| LLM inference | 0 € (self-hosted) | 2.4k €/anno (Groq) | Immediato |
| Storage | 500 € (hardware) | 1.2k €/anno (S3) | 5-6 mesi |

**Raccomandazione**: Hybrid - core services on-premise, LLM cloud durante sviluppo, poi migrazione.
