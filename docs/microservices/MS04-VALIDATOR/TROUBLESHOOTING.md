# MS04 - Validatore - Troubleshooting

**Navigazione**: [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING](TROUBLESHOOTING.md) | [docker-compose.yml →](docker-compose.yml)

## Indice

1. [Flusso Diagnostico Generale](#flusso-diagnostico-generale)
2. [Problemi Comuni](#problemi-common)
   - [Validazione Fallita](#validazione-fallita)
   - [Timeout Validazione](#timeout-validazione)
   - [Errore Schema](#errore-schema)
   - [Connessione Database](#connessione-database)
   - [Certificato Non Valido](#certificato-non-valido)
   - [Problemi Performance](#problemi-performance)
3. [Strumenti Diagnostici](#strumenti-diagnostici)
4. [Procedure Recovery](#procedure-recovery)

---

## Flusso Diagnostico Generale

```mermaid
flowchart TD
    A[Problema Rilevato] --> B{Check Status Validazione}
    B --> C{Status?}
    C -->|Failed| D[Check Error Details]
    C -->|Timeout| E[Check Performance]
    C -->|Running| F[Check Progress]

    D --> G{Error Type?}
    G -->|Schema| H[Validate Schema]
    G -->|Business| I[Check Rules]
    G -->|Compliance| J[Check Compliance]
    G -->|Integrity| K[Check Integrity]

    E --> L{Load High?}
    L -->|Yes| M[Scale Resources]
    L -->|No| N[Check Bottlenecks]

    F --> O{Stuck?}
    O -->|Yes| P[Check Dependencies]
    O -->|No| Q[Monitor Progress]

    H --> R{Schema OK?}
    R -->|No| S[Fix Schema]
    R -->|Yes| T[Check Document]

    I --> U{Rules OK?}
    U -->|No| V[Update Rules]
    U -->|Yes| W[Check Conditions]

    J --> X{Compliance OK?}
    X -->|No| Y[Update Compliance]
    X -->|Yes| Z[Check Data]

    K --> AA{Integrity OK?}
    AA -->|No| BB[Fix Integrity]
    AA -->|Yes| CC[Check Signature]

    M --> DD[Resources Scaled]
    N --> EE[Bottleneck Fixed]
    P --> FF[Dependencies OK]
    Q --> GG[Progress OK]

    S --> HH[Schema Fixed]
    T --> II[Document OK]
    V --> JJ[Rules Updated]
    W --> KK[Conditions OK]
    Y --> LL[Compliance Updated]
    Z --> MM[Data OK]
    BB --> NN[Integrity Fixed]
    CC --> OO[Signature OK]

    DD --> PP[Performance OK]
    EE --> PP
    FF --> PP
    GG --> PP
    HH --> PP
    II --> PP
    JJ --> PP
    KK --> PP
    LL --> PP
    MM --> PP
    NN --> PP
    OO --> PP
```

[↑ Torna al Indice](#indice)

---

## Problemi Comuni

### Validazione Fallita

**Sintomi**:
- Status validazione "failed"
- Errori critici nei risultati
- Documento non validato

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Validation Failed] --> B{Check Error Category}
    B --> C{Schema Error?}
    C -->|Yes| D[Validate Document Schema]
    C -->|No| E{Check Business Rules}

    D --> F{Schema Valid?}
    F -->|No| G[Fix Document Schema]
    F -->|Yes| H[Check Schema Config]

    E --> I{Rules Applied?}
    I -->|No| J[Check Rule Conditions]
    I -->|Yes| K[Check Rule Logic]

    G --> L[Document Fixed]
    H --> M[Schema Config OK]
    J --> N[Conditions Met]
    K --> O[Logic OK]

    L --> P[Validation OK]
    M --> P
    N --> P
    O --> P
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "validation_failed",
    "validation_id": "val-2024-11-18-001",
    "root_cause": "schema_violation",
    "solution": {
      "action": "fix_document_schema",
      "missing_fields": ["invoice_number", "tax_amount"],
      "invalid_fields": ["customer_id"]
    },
    "recovery_payload": {
      "validation_id": "val-2024-11-18-001",
      "action": "retry_validation",
      "skip_failed_checks": false,
      "updated_document": {
        "invoice_number": "INV-2024-001",
        "tax_amount": 704.00,
        "customer_id": "CUST-12345"
      }
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Timeout Validazione

**Sintomi**:
- Validazione non completa entro timeout
- Status rimane "running"
- Errori timeout nei log

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Validation Timeout] --> B{Check Current Step}
    B --> C{Step Type?}
    C -->|Schema| D[Check Document Size]
    C -->|Business| E[Check Rules Count]
    C -->|Compliance| F[Check Data Complexity]

    D --> G{Size > Limit?}
    G -->|Yes| H[Increase Timeout]
    G -->|No| I[Check Processing]

    E --> J{Rules > 100?}
    J -->|Yes| K[Optimize Rules]
    J -->|No| L[Check Rule Performance]

    F --> M{Complex Data?}
    M -->|Yes| N[Split Validation]
    M -->|No| O[Check Compliance Logic]

    H --> P[Timeout Extended]
    I --> Q[Processing OK]
    K --> R[Rules Optimized]
    L --> S[Performance OK]
    N --> T[Validation Split]
    O --> U[Logic OK]

    P --> V[Timeout Resolved]
    Q --> V
    R --> V
    S --> V
    T --> V
    U --> V
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "validation_timeout",
    "validation_id": "val-2024-11-18-001",
    "current_step": "compliance_validation",
    "timeout_duration_seconds": 300,
    "root_cause": "large_document_complexity",
    "solution": {
      "action": "extend_timeout_and_optimize",
      "new_timeout": 600,
      "split_validation": true,
      "parallel_processing": true
    },
    "recovery_payload": {
      "validation_id": "val-2024-11-18-001",
      "action": "resume_with_extended_timeout",
      "timeout_seconds": 600,
      "processing_mode": "parallel"
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Errore Schema

**Sintomi**:
- Errori "SCHEMA_VALIDATION_ERROR"
- Campi richiesti mancanti
- Tipi dati non validi

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Schema Error] --> B{Check Schema Type}
    B --> C{XML Schema?}
    C -->|Yes| D[Validate XSD]
    C -->|No| E{JSON Schema?}

    D --> F{XSD Valid?}
    F -->|No| G[Fix XSD]
    F -->|Yes| H[Check XML Document]

    E --> I{JSON Schema Valid?}
    I -->|No| J[Fix JSON Schema]
    I -->|Yes| K[Check JSON Document]

    G --> L[XSD Fixed]
    H --> M[XML OK]
    J --> N[JSON Schema Fixed]
    K --> O[JSON OK]

    L --> P[Schema OK]
    M --> P
    N --> P
    O --> P
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "schema_validation_error",
    "validation_id": "val-2024-11-18-001",
    "schema_type": "xml",
    "errors": [
      {
        "field": "invoice/invoice_number",
        "error": "required_field_missing",
        "expected_type": "string"
      },
      {
        "field": "invoice/total_amount",
        "error": "invalid_data_type",
        "expected_type": "decimal",
        "actual_type": "string"
      }
    ],
    "solution": {
      "action": "fix_document_fields",
      "corrections": {
        "invoice_number": "INV-2024-001",
        "total_amount": 3904.00
      }
    },
    "recovery_payload": {
      "validation_id": "val-2024-11-18-001",
      "action": "retry_with_corrections",
      "corrected_document": {
        "invoice": {
          "invoice_number": "INV-2024-001",
          "total_amount": 3904.00
        }
      }
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Connessione Database

**Sintomi**:
- Errori "CONNECTION_REFUSED"
- Validazione non può salvare risultati
- Timeout connessione database

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[DB Connection Error] --> B{Check DB Status}
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
      "host": "postgres-validator",
      "port": 5432,
      "database": "validator_db",
      "error": "CONNECTION_TIMEOUT"
    },
    "root_cause": "pool_exhausted",
    "solution": {
      "action": "scale_connection_pool",
      "max_connections": 50,
      "health_check_interval": 30
    },
    "recovery_payload": {
      "database": "validator_db",
      "action": "scale_pool",
      "max_connections": 50,
      "timeout_seconds": 30
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Certificato Non Valido

**Sintomi**:
- Errori "CERTIFICATE_EXPIRED"
- Certificati non verificabili
- Validazioni non certificate

**Flusso Diagnostico**:
```mermaid
flowchart TD
    A[Invalid Certificate] --> B{Check Certificate Status}
    B --> C{Expired?}
    C -->|Yes| D[Renew Certificate]
    C -->|No| E{Revoked?}

    D --> F[Generate New Cert]
    E -->|Yes| G[Check Revocation Reason]
    E -->|No| H{Check Signature?}

    F --> I[New Cert Generated]
    G --> J{Reason Valid?}
    J -->|Yes| K[Keep Revoked]
    J -->|No| L[Unrevoke Cert]

    H -->|No| M[Fix Signature]
    H -->|Yes| N{Check Chain?}

    I --> O[Certificate OK]
    K --> O
    L --> O
    M --> P[Signature Fixed]
    N -->|No| Q[Fix Chain]
    N -->|Yes| R{Check Issuer?}

    P --> O
    Q --> S[Chain Fixed]
    R -->|No| T[Update Issuer]
    R -->|Yes| O

    S --> O
    T --> U[Issuer Updated]
    U --> O
```

**Soluzione JSON**:
```json
{
  "diagnostic_result": {
    "issue_type": "invalid_certificate",
    "certificate_id": "cert-val-2024-11-18-001",
    "certificate_status": "expired",
    "root_cause": "certificate_expired",
    "solution": {
      "action": "renew_certificate",
      "new_validity_days": 365,
      "auto_renewal": true
    },
    "recovery_payload": {
      "certificate_id": "cert-val-2024-11-18-001",
      "action": "renew",
      "validity_period_days": 365,
      "renewal_reason": "expired_certificate"
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### Problemi Performance

**Sintomi**:
- Latenza validazione elevata
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
      "average_latency_ms": 1850,
      "throughput_docs_per_min": 15,
      "cpu_usage_percent": 85,
      "memory_usage_percent": 78
    },
    "bottleneck": "cpu_exhaustion",
    "solution": {
      "action": "scale_resources",
      "cpu_cores": 4,
      "memory_gb": 8,
      "replicas": 3
    },
    "recovery_payload": {
      "service": "ms04_validator",
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
curl -X GET "http://localhost:8004/api/v1/health" \
  -H "Authorization: Bearer {token}"
```

**Response**:
```json
{
  "status": "healthy",
  "checks": {
    "database": "up",
    "redis": "up",
    "certificate_authority": "up",
    "validation_engine": "healthy"
  },
  "timestamp": "2024-11-18T14:30:00Z"
}
```

### Validation Debug Endpoint
```bash
curl -X GET "http://localhost:8004/api/v1/debug/validation/{validation_id}" \
  -H "Authorization: Bearer {token}"
```

**Response**:
```json
{
  "validation_id": "val-2024-11-18-001",
  "debug_info": {
    "current_step": "compliance_validation",
    "step_progress": {
      "completed": 3,
      "total": 5,
      "percentage": 60
    },
    "rule_engine": {
      "active_rules": 12,
      "rules_applied": 8,
      "rules_failed": 0
    },
    "performance": {
      "total_time_ms": 1200,
      "step_times": {
        "schema_validation": 150,
        "business_rules": 450,
        "compliance_check": 600
      }
    },
    "memory_usage": {
      "current_mb": 256,
      "peak_mb": 512
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

## Procedure Recovery

### Recovery da Validazione Fallita
```json
{
  "recovery_procedure": {
    "validation_id": "val-2024-11-18-001",
    "steps": [
      {
        "step": 1,
        "action": "analyze_failure_cause",
        "error_category": "schema_violation",
        "timeout": 30
      },
      {
        "step": 2,
        "action": "generate_correction_suggestions",
        "missing_fields": ["invoice_number"],
        "invalid_fields": ["total_amount"]
      },
      {
        "step": 3,
        "action": "apply_corrections",
        "corrections": {
          "invoice_number": "INV-2024-001",
          "total_amount": 3904.00
        }
      },
      {
        "step": 4,
        "action": "retry_validation",
        "skip_previous_failures": false
      }
    ],
    "rollback_plan": {
      "preserve_original_document": true,
      "max_retry_attempts": 3,
      "notify_on_final_failure": true
    }
  }
}
```

### Recovery da Timeout
```json
{
  "recovery_procedure": {
    "validation_id": "val-2024-11-18-001",
    "steps": [
      {
        "step": 1,
        "action": "extend_timeout",
        "new_timeout_seconds": 600
      },
      {
        "step": 2,
        "action": "optimize_processing",
        "enable_parallel_processing": true,
        "split_large_documents": true
      },
      {
        "step": 3,
        "action": "resume_validation",
        "from_current_step": true
      }
    ],
    "monitoring": {
      "progress_tracking": true,
      "performance_monitoring": true,
      "alert_on_issues": true
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING](TROUBLESHOOTING.md) | [docker-compose.yml →](docker-compose.yml)
