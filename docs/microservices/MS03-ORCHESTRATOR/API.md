# MS03 - Orchestratore - API Reference

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)

## Indice

1. [Panoramica API](#panoramica-api)
2. [Endpoint Workflow](#endpoint-workflow)
   - [POST /workflow/start](#post-workflowstart)
   - [GET /workflow/{id}/status](#get-workflowidstatus)
   - [PUT /workflow/{id}/pause](#put-workflowidpause)
   - [PUT /workflow/{id}/resume](#put-workflowidresume)
   - [DELETE /workflow/{id}](#delete-workflowid)
3. [Endpoint Rules](#endpoint-rules)
   - [GET /rules](#get-rules)
   - [POST /rules](#post-rules)
   - [PUT /rules/{id}](#put-rulesid)
4. [Endpoint Metrics](#endpoint-metrics)
   - [GET /metrics/workflow](#get-metricsworkflow)
   - [GET /metrics/performance](#get-metricsperformance)
5. [Codici di Errore](#codici-di-errore)

---

## Panoramica API

MS03 espone un'API RESTful per la gestione dei workflow. Tutti gli endpoint utilizzano JSON per request/response e richiedono autenticazione tramite Bearer token.

**Base URL**: `http://localhost:8003/api/v1`

**Autenticazione**: `Authorization: Bearer {token}`

**Content-Type**: `application/json`

[↑ Torna al Indice](#indice)

---

## Endpoint Workflow

```
POST /workflow/start
```

Avvia un nuovo workflow di orchestrazione.

**Request Body**:
```json
{
  "workflow_type": "document_generation",
  "parameters": {
    "input_data": {
      "document_type": "invoice",
      "template_id": "inv-001",
      "customer_id": "cust-123"
    },
    "options": {
      "priority": "high",
      "deadline": "2024-11-18T12:00:00Z",
      "callback_url": "https://client.example.com/callback"
    }
  },
  "rules": {
    "business_rules": ["rule_compliance", "rule_validation"],
    "routing_rules": ["route_to_ms05", "parallel_execution"]
  },
  "metadata": {
    "requester": "system_a",
    "correlation_id": "req-2024-11-18-001"
  }
}
```

**Response Success (201)**:
```json
{
  "workflow_id": "wf-2024-11-18-001",
  "status": "started",
  "estimated_completion": "2024-11-18T11:15:00Z",
  "workflow_path": [
    {
      "step": 1,
      "service": "ms01_classifier",
      "estimated_time": "2 minutes"
    },
    {
      "step": 2,
      "service": "ms05_transformer",
      "estimated_time": "5 minutes"
    },
    {
      "step": 3,
      "service": "ms06_validator",
      "estimated_time": "3 minutes"
    }
  ],
  "created_at": "2024-11-18T10:30:00Z"
}
```

**Response Error (400)**:
```json
{
  "error": "INVALID_WORKFLOW_TYPE",
  "message": "Workflow type 'invalid_type' is not supported",
  "details": {
    "supported_types": ["document_generation", "signature_workflow", "archival_process"]
  }
}
```

[↑ Torna al Indice](#indice)

---

### GET /workflow/{id}/status

Recupera lo stato corrente di un workflow.

**Path Parameters**:
- `id`: ID del workflow (string)

**Response Success (200)**:
```json
{
  "workflow_id": "wf-2024-11-18-001",
  "status": "running",
  "current_step": {
    "step_number": 2,
    "service": "ms05_transformer",
    "started_at": "2024-11-18T10:32:00Z",
    "estimated_completion": "2024-11-18T10:37:00Z"
  },
  "progress": {
    "completed_steps": 1,
    "total_steps": 4,
    "percentage": 25,
    "elapsed_time": "00:05:30"
  },
  "next_steps": [
    {
      "step": 3,
      "service": "ms06_validator",
      "estimated_time": "3 minutes"
    },
    {
      "step": 4,
      "service": "ms07_signer",
      "estimated_time": "2 minutes"
    }
  ],
  "metrics": {
    "total_execution_time": "00:05:30",
    "average_step_time": "00:01:45"
  },
  "updated_at": "2024-11-18T10:35:30Z"
}
```

**Response Error (404)**:
```json
{
  "error": "WORKFLOW_NOT_FOUND",
  "message": "Workflow with ID 'wf-invalid' not found"
}
```

[↑ Torna al Indice](#indice)

---

### PUT /workflow/{id}/pause

Mette in pausa un workflow in esecuzione.

**Path Parameters**:
- `id`: ID del workflow (string)

**Request Body**:
```json
{
  "reason": "manual_pause",
  "resume_at": "2024-11-18T14:00:00Z"
}
```

**Response Success (200)**:
```json
{
  "workflow_id": "wf-2024-11-18-001",
  "status": "paused",
  "pause_reason": "manual_pause",
  "resume_at": "2024-11-18T14:00:00Z",
  "current_state": {
    "step": 2,
    "service": "ms05_transformer",
    "progress": 60
  },
  "updated_at": "2024-11-18T11:00:00Z"
}
```

[↑ Torna al Indice](#indice)

---

### PUT /workflow/{id}/resume

Riprende un workflow in pausa.

**Path Parameters**:
- `id`: ID del workflow (string)

**Response Success (200)**:
```json
{
  "workflow_id": "wf-2024-11-18-001",
  "status": "running",
  "resumed_at": "2024-11-18T14:00:00Z",
  "current_step": {
    "step_number": 2,
    "service": "ms05_transformer",
    "remaining_time": "00:02:00"
  }
}
```

[↑ Torna al Indice](#indice)

---

### DELETE /workflow/{id}

Cancella un workflow (solo se non completato).

**Path Parameters**:
- `id`: ID del workflow (string)

**Request Body**:
```json
{
  "reason": "user_cancelled",
  "force": false
}
```

**Response Success (204)**:
```json
{
  "workflow_id": "wf-2024-11-18-001",
  "status": "cancelled",
  "cancelled_at": "2024-11-18T11:15:00Z",
  "reason": "user_cancelled"
}
```

[↑ Torna al Indice](#indice)

---

## Endpoint Rules

### GET /rules

Recupera la lista delle regole business configurate.

**Query Parameters**:
- `type`: Tipo regola (business, routing, validation)
- `active`: Solo regole attive (true/false)

**Response Success (200)**:
```json
{
  "rules": [
    {
      "id": "rule_compliance",
      "type": "business",
      "name": "Compliance Check",
      "description": "Verifica conformità documento",
      "conditions": {
        "document_type": "invoice",
        "amount": "> 1000"
      },
      "actions": ["add_validation_step"],
      "active": true,
      "version": "1.2",
      "created_at": "2024-01-15T09:00:00Z"
    },
    {
      "id": "rule_routing",
      "type": "routing",
      "name": "High Priority Route",
      "conditions": {
        "priority": "high"
      },
      "actions": ["route_to_fast_lane"],
      "active": true
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 50
}
```

[↑ Torna al Indice](#indice)

---

### POST /rules

Crea una nuova regola business.

**Request Body**:
```json
{
  "type": "business",
  "name": "New Compliance Rule",
  "description": "Regola per documenti ad alto rischio",
  "conditions": {
    "risk_level": "high",
    "amount": "> 50000"
  },
  "actions": [
    "add_audit_step",
    "notify_compliance_team"
  ],
  "priority": 10
}
```

**Response Success (201)**:
```json
{
  "rule_id": "rule_new_compliance",
  "status": "created",
  "version": "1.0",
  "created_at": "2024-11-18T12:00:00Z"
}
```

[↑ Torna al Indice](#indice)

---

### PUT /rules/{id}

Aggiorna una regola esistente.

**Path Parameters**:
- `id`: ID della regola (string)

**Request Body**:
```json
{
  "active": false,
  "conditions": {
    "risk_level": "critical",
    "amount": "> 100000"
  }
}
```

**Response Success (200)**:
```json
{
  "rule_id": "rule_compliance",
  "status": "updated",
  "version": "1.3",
  "updated_at": "2024-11-18T12:30:00Z"
}
```

[↑ Torna al Indice](#indice)

---

## Endpoint Metrics

### GET /metrics/workflow

Recupera metriche aggregate sui workflow.

**Query Parameters**:
- `period`: Periodo (hour, day, week, month)
- `workflow_type`: Tipo workflow

**Response Success (200)**:
```json
{
  "period": "day",
  "workflow_type": "all",
  "metrics": {
    "total_workflows": 145,
    "completed_workflows": 138,
    "failed_workflows": 7,
    "success_rate": 0.952,
    "average_completion_time": "00:12:30",
    "peak_concurrent_workflows": 23,
    "average_queue_time": "00:01:15"
  },
  "breakdown_by_type": {
    "document_generation": {
      "count": 89,
      "success_rate": 0.966,
      "avg_time": "00:08:45"
    },
    "signature_workflow": {
      "count": 34,
      "success_rate": 0.941,
      "avg_time": "00:15:20"
    },
    "archival_process": {
      "count": 22,
      "success_rate": 0.909,
      "avg_time": "00:22:10"
    }
  }
}
```

[↑ Torna al Indice](#indice)

---

### GET /metrics/performance

Recupera metriche di performance del sistema.

**Response Success (200)**:
```json
{
  "timestamp": "2024-11-18T13:00:00Z",
  "system_metrics": {
    "cpu_usage_percent": 45.2,
    "memory_usage_percent": 62.8,
    "disk_usage_percent": 34.1,
    "network_io_mbps": 12.5
  },
  "orchestrator_metrics": {
    "active_workflows": 12,
    "queued_workflows": 3,
    "completed_last_hour": 28,
    "average_response_time_ms": 125,
    "error_rate_percent": 2.1
  },
  "service_health": {
    "ms01_classifier": "healthy",
    "ms05_transformer": "healthy",
    "ms06_validator": "degraded",
    "ms07_signer": "healthy"
  }
}
```

[↑ Torna al Indice](#indice)

---

## Codici di Errore

| Codice | Descrizione | HTTP Status |
|--------|-------------|-------------|
| `INVALID_WORKFLOW_TYPE` | Tipo workflow non supportato | 400 |
| `WORKFLOW_NOT_FOUND` | Workflow non trovato | 404 |
| `WORKFLOW_ALREADY_COMPLETED` | Workflow già completato | 409 |
| `RULE_VALIDATION_ERROR` | Errore validazione regola | 400 |
| `SERVICE_UNAVAILABLE` | Servizio downstream non disponibile | 503 |
| `TIMEOUT_ERROR` | Timeout esecuzione | 504 |
| `AUTHENTICATION_FAILED` | Autenticazione fallita | 401 |
| `AUTHORIZATION_FAILED` | Autorizzazione negata | 403 |

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)
