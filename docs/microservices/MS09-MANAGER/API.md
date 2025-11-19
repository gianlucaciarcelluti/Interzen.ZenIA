# API Reference - MS09-MANAGER

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [← API.md](API.md) | [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOUTING.md](TROUBLESHOUTING.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms09--manager)

## 1. Panoramica API

MS09-MANAGER espone API RESTful per la gestione completa del ciclo di vita dei workflow. L'API supporta sia operazioni sincrone che asincrone, con pattern di comunicazione event-driven per workflow complessi.

**Base URL**: `https://api.zenia.local/ms09-manager/v1`
**Protocollo**: HTTPS obbligatorio
**Autenticazione**: OAuth 2.0 + JWT
**Rate Limiting**: 1000 richieste/minuto per tenant

## 2. Autenticazione

### 2.1 OAuth 2.0 Flow

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=ms09-client&client_secret=secret&scope=workflow:read workflow:write
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "workflow:read workflow:write"
}
```

### 2.2 JWT Token Usage

```http
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
X-Tenant-ID: tenant-pa-roma
X-Correlation-ID: corr-123-abc-456-def
```

## 3. Workflow Management API

### 3.1 Creazione Workflow

**Endpoint**: `POST /workflows`
**Descrizione**: Crea una nuova istanza di workflow

```http
POST /workflows
Content-Type: application/json
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma

{
  "workflow_definition_id": "document-processing-workflow",
  "variables": {
    "document_id": "doc-2024-001-abc",
    "priority": "high",
    "callback_url": "https://callback.zenia.local/webhook"
  },
  "metadata": {
    "created_by": "api-user",
    "tags": ["document-processing", "urgent"]
  }
}
```

**Response (201 Created)**:
```json
{
  "workflow_instance_id": "wf-instance-123456789",
  "status": "pending",
  "estimated_completion": "2024-01-15T10:05:00Z",
  "created_at": "2024-01-15T10:00:00Z",
  "links": {
    "self": "/workflows/wf-instance-123456789",
    "status": "/workflows/wf-instance-123456789/status",
    "cancel": "/workflows/wf-instance-123456789/cancel"
  }
}
```

**Error Responses**:

400 Bad Request - Workflow definition not found:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Workflow definition 'invalid-workflow-id' not found",
  "details": {
    "field": "workflow_definition_id",
    "value": "invalid-workflow-id"
  }
}
```

429 Too Many Requests - Rate limit exceeded:
```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded. Try again in 60 seconds",
  "retry_after": 60
}
```

### 3.2 Recupero Stato Workflow

**Endpoint**: `GET /workflows/{workflow_instance_id}`
**Descrizione**: Recupera lo stato dettagliato di un workflow

```http
GET /workflows/wf-instance-123456789
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma
```

**Response (200 OK)**:
```json
{
  "id": "wf-instance-123456789",
  "workflow_definition_id": "document-processing-workflow",
  "status": "running",
  "progress": {
    "percentage": 65,
    "current_step": "parallel_processing",
    "completed_steps": 3,
    "total_steps": 8
  },
  "context": {
    "document_id": "doc-2024-001-abc",
    "tenant_id": "tenant-pa-roma",
    "correlation_id": "corr-789-abc-123-def"
  },
  "variables": {
    "start_time": "2024-01-15T10:00:00Z",
    "estimated_completion": "2024-01-15T10:05:00Z",
    "priority": "high"
  },
  "steps": {
    "initial_validation": {
      "status": "completed",
      "started_at": "2024-01-15T10:00:00Z",
      "completed_at": "2024-01-15T10:00:30Z",
      "duration_ms": 30000,
      "result": {
        "valid": true,
        "format": "pdf",
        "size_bytes": 2048576
      }
    },
    "parallel_processing": {
      "status": "running",
      "started_at": "2024-01-15T10:00:30Z",
      "branches": {
        "classification_branch": {
          "status": "running",
          "current_step": "classification",
          "progress": 80
        },
        "analysis_branch": {
          "status": "completed",
          "completed_at": "2024-01-15T10:02:00Z",
          "result": {
            "confidence": 0.92,
            "categories": ["provvedimento", "autorizzazione"]
          }
        }
      }
    }
  },
  "events": [
    {
      "id": "event-001",
      "type": "WorkflowStarted",
      "timestamp": "2024-01-15T10:00:00Z",
      "message": "Workflow avviato"
    },
    {
      "id": "event-002",
      "type": "StepCompleted",
      "timestamp": "2024-01-15T10:00:30Z",
      "message": "Validazione iniziale completata"
    }
  ],
  "metadata": {
    "created_at": "2024-01-15T10:00:00Z",
    "created_by": "api-user",
    "updated_at": "2024-01-15T10:02:15Z",
    "version": 5
  },
  "links": {
    "self": "/workflows/wf-instance-123456789",
    "cancel": "/workflows/wf-instance-123456789/cancel",
    "retry": "/workflows/wf-instance-123456789/retry"
  }
}
```

### 3.3 Cancellazione Workflow

**Endpoint**: `POST /workflows/{workflow_instance_id}/cancel`
**Descrizione**: Cancella un workflow in esecuzione

```http
POST /workflows/wf-instance-123456789/cancel
Content-Type: application/json
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma

{
  "reason": "User requested cancellation",
  "force": false
}
```

**Response (200 OK)**:
```json
{
  "workflow_instance_id": "wf-instance-123456789",
  "status": "cancelled",
  "cancelled_at": "2024-01-15T10:05:00Z",
  "compensation_status": "completed"
}
```

### 3.4 Retry Workflow

**Endpoint**: `POST /workflows/{workflow_instance_id}/retry`
**Descrizione**: Ritenta un workflow fallito

```http
POST /workflows/wf-instance-123456789/retry
Content-Type: application/json
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma

{
  "from_step": "failed_step_id",
  "reset_variables": true,
  "max_attempts": 3
}
```

## 4. Workflow Definition API

### 4.1 Creazione Definizione Workflow

**Endpoint**: `POST /workflow-definitions`
**Descrizione**: Crea una nuova definizione di workflow

```http
POST /workflow-definitions
Content-Type: application/json
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma

{
  "id": "document-processing-workflow",
  "version": "1.0.0",
  "name": "Workflow Elaborazione Documenti",
  "description": "Workflow completo per elaborazione documenti PA",
  "definition": {
    "variables": {
      "document_id": {"type": "string", "required": true},
      "priority": {"type": "enum", "values": ["low", "normal", "high"], "default": "normal"}
    },
    "steps": [
      {
        "id": "validation",
        "name": "Validazione Documento",
        "type": "service_call",
        "service": "ms04-validator",
        "action": "validate",
        "parameters": {
          "document_id": "${variables.document_id}"
        }
      }
    ]
  },
  "metadata": {
    "author": "DevOps Team",
    "tags": ["documenti", "pa"],
    "category": "business-process"
  }
}
```

### 4.2 Lista Definizioni Workflow

**Endpoint**: `GET /workflow-definitions`
**Descrizione**: Lista tutte le definizioni workflow disponibili

```http
GET /workflow-definitions?page=1&size=20&category=business-process
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma
```

**Response (200 OK)**:
```json
{
  "definitions": [
    {
      "id": "document-processing-workflow",
      "version": "1.0.0",
      "name": "Workflow Elaborazione Documenti",
      "description": "Workflow completo per elaborazione documenti PA",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z",
      "metadata": {
        "author": "DevOps Team",
        "tags": ["documenti", "pa"],
        "category": "business-process"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "size": 20,
    "total": 1,
    "total_pages": 1
  }
}
```

## 5. Monitoring API

### 5.1 Metriche Workflow

**Endpoint**: `GET /metrics/workflows`
**Descrizione**: Recupera metriche aggregate sui workflow

```http
GET /metrics/workflows?period=1h&group_by=status
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma
```

**Response (200 OK)**:
```json
{
  "period": "1h",
  "metrics": {
    "total_workflows": 1250,
    "by_status": {
      "completed": 1100,
      "running": 120,
      "failed": 25,
      "cancelled": 5
    },
    "by_type": {
      "document-processing": 800,
      "data-analysis": 350,
      "notification": 100
    },
    "performance": {
      "avg_duration_seconds": 245.5,
      "p95_duration_seconds": 890.2,
      "success_rate_percent": 96.8,
      "throughput_per_minute": 20.8
    }
  },
  "timestamp": "2024-01-15T11:00:00Z"
}
```

### 5.2 Health Check

**Endpoint**: `GET /health`
**Descrizione**: Verifica lo stato di salute del servizio

```http
GET /health
Authorization: Bearer {token}
```

**Response (200 OK)**:
```json
{
  "status": "UP",
  "checks": {
    "database": {
      "status": "UP",
      "details": {
        "connection_time_ms": 15,
        "active_connections": 12
      }
    },
    "message_broker": {
      "status": "UP",
      "details": {
        "connections": 5,
        "channels": 23
      }
    },
    "cache": {
      "status": "UP",
      "details": {
        "hit_rate_percent": 94.5,
        "memory_usage_mb": 256
      }
    },
    "workflow_engine": {
      "status": "UP",
      "details": {
        "active_workflows": 1250,
        "threads": 8,
        "queue_size": 45
      }
    }
  },
  "version": "1.0.0",
  "timestamp": "2024-01-15T11:00:00Z"
}
```

## 6. Bulk Operations API

### 6.1 Bulk Status Check

**Endpoint**: `POST /workflows/bulk/status`
**Descrizione**: Verifica lo stato di multiple workflow

```http
POST /workflows/bulk/status
Content-Type: application/json
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma

{
  "workflow_instance_ids": [
    "wf-instance-123456789",
    "wf-instance-987654321",
    "wf-instance-abcdef123"
  ]
}
```

**Response (200 OK)**:
```json
{
  "results": [
    {
      "workflow_instance_id": "wf-instance-123456789",
      "status": "completed",
      "completed_at": "2024-01-15T10:30:00Z"
    },
    {
      "workflow_instance_id": "wf-instance-987654321",
      "status": "running",
      "progress_percentage": 75
    },
    {
      "workflow_instance_id": "wf-instance-abcdef123",
      "status": "failed",
      "error": "Step timeout exceeded",
      "failed_at": "2024-01-15T10:15:00Z"
    }
  ]
}
```

### 6.2 Bulk Cancellation

**Endpoint**: `POST /workflows/bulk/cancel`
**Descrizione**: Cancella multiple workflow

```http
POST /workflows/bulk/cancel
Content-Type: application/json
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma

{
  "workflow_instance_ids": [
    "wf-instance-123456789",
    "wf-instance-987654321"
  ],
  "reason": "Bulk maintenance operation",
  "force": false
}
```

## 7. Webhook API

### 7.1 Configurazione Webhook

**Endpoint**: `POST /webhooks`
**Descrizione**: Registra un webhook per notifiche workflow

```http
POST /webhooks
Content-Type: application/json
Authorization: Bearer {token}
X-Tenant-ID: tenant-pa-roma

{
  "url": "https://callback.zenia.local/workflow-events",
  "events": [
    "workflow.completed",
    "workflow.failed",
    "step.completed",
    "step.failed"
  ],
  "secret": "webhook-secret-123",
  "retry_policy": {
    "max_attempts": 5,
    "backoff": {
      "type": "exponential",
      "initial_delay": "1s",
      "max_delay": "5m"
    }
  },
  "filters": {
    "workflow_types": ["document-processing"],
    "tags": ["urgent"]
  }
}
```

### 7.2 Payload Webhook

```json
{
  "event_id": "event-123456789",
  "event_type": "workflow.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "webhook_id": "wh-456789",
  "data": {
    "workflow_instance_id": "wf-instance-123456789",
    "workflow_definition_id": "document-processing-workflow",
    "status": "completed",
    "result": {
      "document_id": "doc-2024-001-abc",
      "processing_time_seconds": 1800,
      "steps_completed": 8
    },
    "metadata": {
      "tenant_id": "tenant-pa-roma",
      "correlation_id": "corr-789-abc-123-def"
    }
  },
  "signature": "sha256=abc123def456..."
}
```

## 8. Administrative API

### 8.1 Workflow Cleanup

**Endpoint**: `POST /admin/workflows/cleanup`
**Descrizione**: Pulisce workflow completati vecchi (solo admin)

```http
POST /admin/workflows/cleanup
Content-Type: application/json
Authorization: Bearer {admin_token}
X-Tenant-ID: tenant-pa-roma

{
  "older_than_days": 90,
  "status_filter": ["completed", "failed"],
  "dry_run": true
}
```

### 8.2 System Statistics

**Endpoint**: `GET /admin/statistics`
**Descrizione**: Statistiche di sistema dettagliate

```http
GET /admin/statistics?period=24h
Authorization: Bearer {admin_token}
```

**Response (200 OK)**:
```json
{
  "period": "24h",
  "system": {
    "uptime_seconds": 86400,
    "version": "1.0.0",
    "environment": "production"
  },
  "workflows": {
    "total_created": 12500,
    "total_completed": 11800,
    "total_failed": 650,
    "avg_completion_time_seconds": 245.5,
    "success_rate_percent": 94.4
  },
  "performance": {
    "cpu_usage_percent": 65.2,
    "memory_usage_mb": 2048,
    "disk_usage_gb": 45.2,
    "network_io_mbps": 125.8
  },
  "queues": {
    "pending_workflows": 45,
    "active_workflows": 1250,
    "failed_workflows": 25
  }
}
```

## 9. Error Handling

### 9.1 Error Response Format

```json
{
  "error": {
    "code": "WORKFLOW_EXECUTION_FAILED",
    "message": "Workflow execution failed at step 'data_processing'",
    "details": {
      "workflow_instance_id": "wf-instance-123456789",
      "failed_step": "data_processing",
      "error_type": "SERVICE_UNAVAILABLE",
      "retryable": true,
      "retry_after_seconds": 300
    },
    "timestamp": "2024-01-15T10:15:00Z",
    "correlation_id": "corr-789-abc-123-def",
    "request_id": "req-456-def-789-abc"
  }
}
```

### 9.2 Common Error Codes

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `WORKFLOW_NOT_FOUND` | 404 | Workflow instance not found |
| `WORKFLOW_DEFINITION_INVALID` | 400 | Invalid workflow definition |
| `STEP_EXECUTION_FAILED` | 500 | Step execution failed |
| `SERVICE_UNAVAILABLE` | 503 | External service unavailable |
| `RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded |
| `AUTHENTICATION_FAILED` | 401 | Authentication failed |
| `AUTHORIZATION_FAILED` | 403 | Insufficient permissions |
| `VALIDATION_ERROR` | 400 | Request validation failed |

## 10. SDK Examples

### 10.1 JavaScript SDK

```javascript
import { ZenIABPM } from '@zenia/bpm-sdk';

const client = new ZenIABPM({
  baseUrl: 'https://api.zenia.local/ms09-manager/v1',
  tenantId: 'tenant-pa-roma',
  credentials: {
    clientId: 'my-client',
    clientSecret: 'my-secret'
  }
});

// Create workflow
const workflow = await client.workflows.create({
  workflowDefinitionId: 'document-processing-workflow',
  variables: {
    documentId: 'doc-2024-001-abc',
    priority: 'high'
  }
});

console.log(`Workflow created: ${workflow.id}`);

// Monitor progress
const status = await client.workflows.getStatus(workflow.id);
console.log(`Progress: ${status.progress.percentage}%`);

// Handle completion
client.on('workflow.completed', (event) => {
  console.log(`Workflow ${event.workflowId} completed`);
});
```

### 10.2 Python SDK

```python
from zenia_bpm import ZenIABPMClient

client = ZenIABPMClient(
    base_url='https://api.zenia.local/ms09-manager/v1',
    tenant_id='tenant-pa-roma',
    client_id='my-client',
    client_secret='my-secret'
)

# Create workflow
workflow = client.workflows.create(
    workflow_definition_id='document-processing-workflow',
    variables={
        'document_id': 'doc-2024-001-abc',
        'priority': 'high'
    }
)

print(f"Workflow created: {workflow.id}")

# Monitor with polling
import time

while True:
    status = client.workflows.get_status(workflow.id)
    print(f"Status: {status.status}, Progress: {status.progress.percentage}%")

    if status.status in ['completed', 'failed', 'cancelled']:
        break

    time.sleep(5)

print(f"Workflow finished with status: {status.status}")
```

## 11. Rate Limiting

### 11.1 Limits per Tenant

| Operation | Limit | Window |
|-----------|-------|--------|
| Create Workflow | 100/min | 1 minute |
| Get Workflow Status | 1000/min | 1 minute |
| List Workflows | 500/min | 1 minute |
| Bulk Operations | 50/min | 1 minute |
| Admin Operations | 10/min | 1 minute |

### 11.2 Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642156800
X-RateLimit-Retry-After: 60
```

## 12. Versioning

### 12.1 API Versioning

L'API utilizza versioning nell'URL path:
- `v1`: Versione corrente (stable)
- `v2`: In sviluppo (breaking changes)

### 12.2 Workflow Definition Versioning

```json
{
  "id": "document-processing-workflow",
  "version": "1.2.0",
  "compatibility": {
    "minimum_version": "1.0.0",
    "breaking_changes": false
  }
}
```

## 13. Best Practices

### 13.1 Workflow Design

1. **Idempotency**: Usa correlation IDs per evitare duplicati
2. **Timeout Management**: Configura timeout appropriati per ogni step
3. **Error Handling**: Implementa compensazione per operazioni critiche
4. **Monitoring**: Monitora metriche chiave per ottimizzazione

### 13.2 API Usage

1. **Connection Pooling**: Riutilizza connessioni HTTP
2. **Exponential Backoff**: Implementa retry con backoff esponenziale
3. **Correlation IDs**: Usa correlation IDs per tracing end-to-end
4. **Pagination**: Usa pagination per liste grandi
5. **Compression**: Abilita gzip per payload grandi

### 13.3 Security

1. **Token Rotation**: Ruota token regolarmente
2. **Least Privilege**: Usa ruoli con minimi privilegi necessari
3. **Input Validation**: Valida sempre input utente
4. **Audit Logging**: Logga operazioni sensibili