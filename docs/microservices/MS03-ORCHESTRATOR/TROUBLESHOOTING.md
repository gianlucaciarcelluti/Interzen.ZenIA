# MS03 - Orchestratore - Troubleshooting

**Navigazione**: [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING](TROUBLESHOOTING.md) | [docker-compose.yml →](./docker-compose.yml)

## Indice

1. [Flusso Diagnostico Generale](#flusso-diagnostico-generale)
2. [Problemi Comuni](#problemi-comuni)
   - [Workflow Bloccato](#workflow-bloccato)
   - [Timeout Servizio](#timeout-servizio)
   - [Errore Valutazione Regole](#errore-valutazione-regole)
   - [Connessione Database](#connessione-database)
   - [Errore Coordinamento](#errore-coordinamento)
   - [Problemi Performance](#problemi-performance)
3. [Strumenti Diagnostici](#strumenti-diagnostici)
4. [Procedure Recovery](#procedure-recovery)

---

## Flusso Diagnostico Generale

```mermaid
flowchart TD
    A[Problema Rilevato] --> B{Check Status Workflow}
    B --> C{Workflow Status?}
    C -->|Running| D[Check Current Step]
    C -->|Failed| E[Check Error Logs]
    C -->|Stuck| F[Check Service Health]

    D --> G{Step Status?}
    G -->|Pending| H[Check Queue]
    G -->|Running| I[Check Service Response]
    G -->|Failed| J[Check Step Error]

    E --> K[Analyze Error Pattern]
    F --> L[Check Dependencies]

    H --> M{Queue Size?}
    M -->|Normal| N[Check Resource Limits]
    M -->|High| O[Scale Resources]

    I --> P{Response Time?}
    P -->|Normal| Q[Check Network]
    P -->|Slow| R[Check Service Load]

    J --> S[Retry Logic]
    K --> T[Error Classification]
    L --> U[Dependency Check]

    N --> V[Resource Allocation]
    O --> W[Auto-scaling]
    Q --> X[Network Diagnostics]
    R --> Y[Load Balancing]

    S --> Z{Retry Success?}
    Z -->|Yes| AA[Continue Workflow]
    Z -->|No| BB[Manual Intervention]

    T --> CC[Error Pattern Analysis]
    U --> DD[Dependency Resolution]

    V --> EE[Monitor Resources]
    W --> FF[Scale Complete]
    X --> GG[Network Fix]
    Y --> HH[Load Distribution]

    AA --> II[Workflow Recovery]
    BB --> JJ[Escalation]
    CC --> KK[Fix Implementation]
    DD --> LL[Dependency Fix]

    EE --> MM[Performance OK]
    FF --> NN[Capacity OK]
    GG --> OO[Connectivity OK]
    HH --> PP[Load OK]

    II --> QQ[Success]
    JJ --> RR[Manual Resolution]
    KK --> SS[Error Fixed]
    LL --> TT[Dependency OK]

    MM --> QQ
    NN --> QQ
    OO --> QQ
    PP --> QQ
    RR --> QQ
    SS --> QQ
    TT --> QQ
```

[↑ Torna al Indice](#indice)

---

## Problemi Comuni

### Workflow Bloccato

**Sintomi**:
- Workflow status rimane "running" per più di 30 minuti
- Nessun progresso nei passi successivi
- Metriche mostrano step corrente bloccato

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Workflow Stuck] --> B{Check Current Step}
    B --> C{Step Status?}
    C -->|Running| D[Check Service Health]
    C -->|Pending| E[Check Queue Depth]

    D --> F{Service Healthy?}
    F -->|No| G[Restart Service]
    F -->|Yes| H[Check Service Logs]

    E --> I{Queue > Threshold?}
    I -->|Yes| J[Scale Orchestrator]
    I -->|No| K[Check Dependencies]

    G --> L[Test Service]
    H --> M[Analyze Logs]
    J --> N[Monitor Queue]
    K --> O[Check Downstream]

    L --> P{Service OK?}
    P -->|Yes| Q[Resume Workflow]
    P -->|No| R[Escalate]

    M --> S{Error Found?}
    S -->|Yes| T[Fix Error]
    S -->|No| U[Deep Diagnostics]

    N --> V{Queue Normal?}
    V -->|Yes| Q
    V -->|No| W[Scale More]

    O --> X{Dependencies OK?}
    X -->|Yes| Q
    X -->|No| Y[Fix Dependencies]

    Q --> Z[Workflow Resumed]
    R --> AA[Incident Created]
    T --> Q
    U --> BB[Expert Analysis]
    W --> Z
    Y --> Z
    AA --> CC[Resolution]
    BB --> CC
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "workflow_stuck",
    "workflow_id": "wf-2024-11-18-001",
    "current_step": {
      "step_number": 2,
      "service": "ms05_transformer",
      "status": "running",
      "stuck_duration_minutes": 45
    },
    "root_cause": "service_timeout",
    "solution": {
      "action": "restart_service",
      "service": "ms05_transformer",
      "fallback": "route_to_backup_service"
    },
    "recovery_payload": {
      "workflow_id": "wf-2024-11-18-001",
      "action": "resume",
      "from_step": 2,
      "retry_count": 1
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Timeout Servizio

**Sintomi**:
- Errori "408 Request Timeout"
- Workflow fallisce dopo timeout configurato
- Metriche mostrano latenza elevata

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Service Timeout] --> B{Check Service Health}
    B --> C{Service Responding?}
    C -->|No| D[Check Service Status]
    C -->|Yes| E[Check Load]

    D --> F{Service Up?}
    F -->|No| G[Start Service]
    F -->|Yes| H[Check Configuration]

    E --> I{Load > Threshold?}
    I -->|Yes| J[Scale Service]
    I -->|No| K[Check Network]

    G --> L[Test Connectivity]
    H --> M[Validate Config]
    J --> N[Monitor Load]
    K --> O[Network Diagnostics]

    L --> P{Connection OK?}
    P -->|Yes| Q[Resume Operations]
    P -->|No| R[Network Fix]

    M --> S{Config Valid?}
    S -->|Yes| Q
    S -->|No| T[Fix Configuration]

    N --> U{Load Balanced?}
    U -->|Yes| Q
    U -->|No| V[Rebalance]

    O --> W{Network OK?}
    W -->|Yes| Q
    W -->|No| X[Fix Network]

    Q --> Y[Timeout Resolved]
    R --> Z[Connectivity Fixed]
    T --> AA[Config Updated]
    V --> BB[Load Balanced]
    X --> CC[Network Fixed]

    Y --> DD[Success]
    Z --> DD
    AA --> DD
    BB --> DD
    CC --> DD
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "service_timeout",
    "service": "ms05_transformer",
    "timeout_duration_seconds": 300,
    "root_cause": "high_load",
    "solution": {
      "action": "scale_service",
      "replicas": 3,
      "timeout_extension": 600
    },
    "recovery_payload": {
      "service": "ms05_transformer",
      "action": "scale",
      "target_replicas": 3,
      "health_check_timeout": 30
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Errore Valutazione Regole

**Sintomi**:
- Workflow fallisce durante rule evaluation
- Errori "RULE_VALIDATION_ERROR"
- Regole non applicate correttamente

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Rule Evaluation Error] --> B{Check Rule Definition}
    B --> C{Rule Exists?}
    C -->|No| D[Create Rule]
    C -->|Yes| E[Validate Rule Syntax]

    D --> F[Test Rule]
    E --> G{Syntax Valid?}
    G -->|No| H[Fix Syntax]
    G -->|Yes| I[Check Conditions]

    F --> J{Rule Works?}
    J -->|Yes| K[Deploy Rule]
    J -->|No| L[Debug Rule]

    H --> M[Validate Fix]
    I --> N{Conditions Match?}
    N -->|No| O[Update Conditions]
    N -->|Yes| P[Check Actions]

    K --> Q[Rule Active]
    L --> R[Rule Fixed]
    M --> S{Syntax OK?}
    S -->|Yes| K
    S -->|No| H

    O --> T[Test Conditions]
    P --> U{Actions Valid?}
    U -->|No| V[Fix Actions]
    U -->|Yes| W[Check Permissions]

    Q --> X[Error Resolved]
    R --> X
    T --> Y{Conditions OK?}
    Y -->|Yes| P
    Y -->|No| O

    V --> AA[Test Actions]
    W --> BB{Permissions OK?}
    BB -->|No| CC[Grant Permissions]
    BB -->|Yes| X

    AA --> DD{Actions OK?}
    DD -->|Yes| W
    DD -->|No| V

    CC --> EE[Permissions Set]
    EE --> X
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "rule_evaluation_error",
    "rule_id": "rule_compliance_check",
    "error_details": {
      "error_type": "INVALID_CONDITION",
      "condition": "total_amount > 1000",
      "actual_value": "amount",
      "expected_value": "total_amount"
    },
    "solution": {
      "action": "fix_rule_condition",
      "field_name": "total_amount",
      "operator": ">",
      "value": 1000
    },
    "recovery_payload": {
      "rule_id": "rule_compliance_check",
      "action": "update",
      "conditions": {
        "total_amount": {
          "operator": ">",
          "value": 1000
        }
      },
      "version": "2.2"
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Connessione Database

**Sintomi**:
- Errori "CONNECTION_REFUSED"
- Workflow non può salvare stato
- Timeout connessione database

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Database Connection Error] --> B{Check DB Status}
    B --> C{DB Running?}
    C -->|No| D[Start Database]
    C -->|Yes| E[Check Connection Pool]

    D --> F[Test Connection]
    E --> G{Pool Available?}
    G -->|No| H[Scale Pool]
    G -->|Yes| I[Check Network]

    F --> J{Connection OK?}
    J -->|Yes| K[Resume Operations]
    J -->|No| L[Check Credentials]

    H --> M[Monitor Pool]
    I --> N{Network OK?}
    N -->|No| O[Fix Network]
    N -->|Yes| P[Check Firewall]

    K --> Q[Connection Restored]
    L --> R{Credentials Valid?}
    R -->|No| S[Update Credentials]
    R -->|Yes| T[Check Permissions]

    M --> U{Pool OK?}
    U -->|Yes| K
    U -->|No| V[Scale More]

    O --> W{Network Fixed?}
    W -->|Yes| K
    W -->|No| X[Network Expert]

    P --> Y{Firewall OK?}
    Y -->|Yes| K
    Y -->|No| Z[Update Rules]

    S --> AA[Test Auth]
    T --> BB{Permissions OK?}
    BB -->|No| CC[Grant Permissions]
    BB -->|Yes| K

    V --> Q
    X --> Q
    Z --> Q
    AA --> DD{Auth OK?}
    DD -->|Yes| T
    DD -->|No| S

    CC --> EE[Permissions OK]
    EE --> Q
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "database_connection",
    "connection_details": {
      "host": "postgres-orchestrator",
      "port": 5432,
      "database": "orchestrator_db",
      "error": "CONNECTION_TIMEOUT"
    },
    "root_cause": "pool_exhausted",
    "solution": {
      "action": "scale_connection_pool",
      "max_connections": 50,
      "health_check_interval": 30
    },
    "recovery_payload": {
      "database": "orchestrator_db",
      "action": "scale_pool",
      "max_connections": 50,
      "timeout_seconds": 30
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Errore Coordinamento

**Sintomi**:
- Workflow perde sincronizzazione tra passi
- Errori "COORDINATION_FAILED"
- Passi eseguiti fuori ordine

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Coordination Error] --> B{Check State Consistency}
    B --> C{State Valid?}
    C -->|No| D[Rebuild State]
    C -->|Yes| E[Check Step Order]

    D --> F[Validate State]
    E --> G{Order Correct?}
    G -->|No| H[Reorder Steps]
    G -->|Yes| I[Check Dependencies]

    F --> J{State OK?}
    J -->|Yes| K[Resume Coordination]
    J -->|No| L[Manual State Fix]

    H --> M[Test Order]
    I --> N{Dependencies OK?}
    N -->|No| O[Fix Dependencies]
    N -->|Yes| P[Check Concurrency]

    K --> Q[Coordination OK]
    L --> R[State Fixed]
    M --> S{Order OK?}
    S -->|Yes| I
    S -->|No| H

    O --> T[Test Dependencies]
    P --> U{Concurrency OK?}
    U -->|No| V[Fix Concurrency]
    U -->|Yes| K

    Q --> W[Success]
    R --> W
    T --> X{Dependencies OK?}
    X -->|Yes| P
    X -->|No| O

    V --> Y[Test Concurrency]
    Y --> Z{Concurrency OK?}
    Z -->|Yes| K
    Z -->|No| V
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "coordination_error",
    "workflow_id": "wf-2024-11-18-001",
    "error_details": {
      "expected_step": 3,
      "actual_step": 2,
      "coordination_failure": "step_out_of_order"
    },
    "solution": {
      "action": "resync_workflow",
      "correct_step": 3,
      "rollback_to_step": 2
    },
    "recovery_payload": {
      "workflow_id": "wf-2024-11-18-001",
      "action": "resync",
      "target_step": 3,
      "force_sync": true
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Problemi Performance

**Sintomi**:
- Latenza workflow elevata
- Throughput ridotto
- CPU/Memory usage alto

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Performance Issue] --> B{Check Metrics}
    B --> C{Metrics OK?}
    C -->|No| D[Identify Bottleneck]
    C -->|Yes| E[Check Configuration]

    D --> F{Bottleneck Type?}
    F -->|CPU| G[Scale CPU]
    F -->|Memory| H[Scale Memory]
    F -->|IO| I[Optimize IO]
    F -->|Network| J[Scale Network]

    E --> K{Config Optimal?}
    K -->|No| L[Tune Config]
    K -->|Yes| M[Check Load]

    G --> N[Monitor CPU]
    H --> O[Monitor Memory]
    I --> P[Monitor IO]
    J --> Q[Monitor Network]

    L --> R[Test Config]
    M --> S{Load Balanced?}
    S -->|No| T[Balance Load]
    S -->|Yes| U[Check Code]

    N --> V{CPU OK?}
    V -->|Yes| W[Performance OK]
    V -->|No| X[Scale More CPU]

    O --> Y{Memory OK?}
    Y -->|Yes| W
    Y -->|No| Z[Scale More Memory]

    P --> AA{IO OK?}
    AA -->|Yes| W
    AA -->|No| BB[Optimize More]

    Q --> CC{Network OK?}
    CC -->|Yes| W
    CC -->|No| DD[Scale Network]

    R --> EE{Config OK?}
    EE -->|Yes| M
    EE -->|No| L

    T --> FF[Test Balance]
    U --> GG{Code Efficient?}
    GG -->|No| HH[Optimize Code]
    GG -->|Yes| W

    X --> W
    Z --> W
    BB --> W
    DD --> W
    FF --> II{Balanced?}
    II -->|Yes| U
    II -->|No| T

    HH --> JJ[Test Optimization]
    JJ --> KK{Optimized?}
    KK -->|Yes| W
    KK -->|No| HH
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "performance_degradation",
    "metrics": {
      "average_latency_ms": 850,
      "throughput_wf_per_min": 8,
      "cpu_usage_percent": 78,
      "memory_usage_percent": 82
    },
    "bottleneck": "memory_exhaustion",
    "solution": {
      "action": "scale_resources",
      "cpu_cores": 4,
      "memory_gb": 8,
      "replicas": 3
    },
    "recovery_payload": {
      "service": "ms03_orchestrator",
      "action": "scale",
      "resources": {
        "cpu": "2",
        "memory": "4Gi"
      },
      "replicas": 3
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

## Strumenti Diagnostici

### Health Check Endpoint
```bash
curl -X GET "http://localhost:8003/api/v1/health" \
  -H "Authorization: Bearer {token}"
```

**Response**:
```json
{
  "status": "healthy",
  "checks": {
    "database": "up",
    "redis": "up",
    "services": {
      "ms01": "healthy",
      "ms05": "degraded",
      "ms06": "healthy"
    }
  },
  "timestamp": "2024-11-18T14:30:00Z"
}
```

### Workflow Debug Endpoint
```bash
curl -X GET "http://localhost:8003/api/v1/debug/workflow/{workflow_id}" \
  -H "Authorization: Bearer {token}"
```

**Response**:
```json
{
  "workflow_id": "wf-2024-11-18-001",
  "debug_info": {
    "state_machine": {
      "current_state": "step_2_running",
      "transitions": [
        {
          "from": "step_1_completed",
          "to": "step_2_running",
          "timestamp": "2024-11-18T10:32:00Z"
        }
      ]
    },
    "rule_engine": {
      "applied_rules": ["rule_compliance"],
      "rule_evaluation_time_ms": 45
    },
    "performance": {
      "total_time_ms": 120000,
      "step_times": {
        "ms01": 25000,
        "ms05": 95000
      }
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

## Procedure Recovery

### Recovery da Workflow Stuck
```json
{
  "recovery_procedure": {
    "workflow_id": "wf-2024-11-18-001",
    "steps": [
      {
        "step": 1,
        "action": "check_service_health",
        "service": "ms05_transformer",
        "timeout": 30
      },
      {
        "step": 2,
        "action": "restart_service",
        "service": "ms05_transformer",
        "condition": "health_check_failed"
      },
      {
        "step": 3,
        "action": "resume_workflow",
        "from_step": 2,
        "retry_count": 1
      }
    ],
    "rollback_plan": {
      "rollback_to_step": 1,
      "preserve_state": true,
      "notify_stakeholders": true
    }
  }
}
```

### Recovery da Database Failure
```json
{
  "recovery_procedure": {
    "database": "orchestrator_db",
    "steps": [
      {
        "step": 1,
        "action": "check_connection",
        "timeout": 60
      },
      {
        "step": 2,
        "action": "failover_to_replica",
        "condition": "primary_down"
      },
      {
        "step": 3,
        "action": "sync_pending_workflows",
        "batch_size": 10
      }
    ],
    "data_integrity_check": {
      "check_type": "checksum_validation",
      "affected_workflows": "last_24h"
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING](TROUBLESHOOTING.md) | [docker-compose.yml →](./docker-compose.yml)
