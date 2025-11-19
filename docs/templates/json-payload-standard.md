# Standard Template Payload JSON - ZenIA

**Versione**: 1.0
**Data**: 2025-11-19
**Scopo**: Definire strutture standard per request/response JSON in tutti gli SP

---

## 📋 LINEE GUIDA GENERALI

### Naming Convention
- **Preferenza**: `snake_case` per nomi campi
- **Eccezioni accettate**: `camelCase` per contesti cross-team (se standardizzato)
- **Standard globale ZenIA**: Usare `snake_case` per consistenza italiana

### Campi Obbligatori

Ogni request **DEVE** contenere:
```json
{
  "request_id": "REQ-2025-XXXXX",
  "timestamp": "2025-11-19T14:30:00Z",
  "version": "1.0"
}
```

Ogni response **DEVE** contenere:
```json
{
  "request_id": "REQ-2025-XXXXX",
  "response_id": "RES-2025-XXXXX",
  "timestamp": "2025-11-19T14:30:00Z",
  "status": "success|warning|error",
  "version": "1.0"
}
```

---

## 📤 STRUTTURA REQUEST STANDARD

```json
{
  "request_id": "REQ-2025-001234",
  "timestamp": "2025-11-19T14:30:00Z",
  "version": "1.0",
  "metadata": {
    "user_id": "USR-12345",
    "session_id": "SESS-67890",
    "source": "api|web|mobile",
    "locale": "it-IT"
  },
  "data": {
    // Payload specifico SP qui
  },
  "options": {
    "async": false,
    "timeout_ms": 30000,
    "retry_policy": "exponential"
  }
}
```

### Campi Dettaglio

| Campo | Tipo | Obbligatorio | Descrizione |
|-------|------|-------------|------------|
| `request_id` | string | ✓ | ID univoco per tracciabilità |
| `timestamp` | ISO 8601 | ✓ | Timestamp creazione request |
| `version` | string | ✓ | Versione API (es. "1.0") |
| `metadata` | object | ⚠️ | Context utente/sessione |
| `metadata.user_id` | string | ⚠️ | ID utente che fa la richiesta |
| `metadata.session_id` | string | ⚠️ | ID sessione (se applicabile) |
| `metadata.source` | enum | ⚠️ | Origine richiesta |
| `metadata.locale` | string | ⚠️ | Locale (default: "it-IT") |
| `data` | object | ✓ | Payload specifico SP |
| `options` | object | ⚠️ | Opzioni di elaborazione |
| `options.async` | boolean | ⚠️ | Se true, response asincrona |
| `options.timeout_ms` | number | ⚠️ | Timeout massimo in ms |
| `options.retry_policy` | string | ⚠️ | Politica retry |

---

## 📥 STRUTTURA RESPONSE STANDARD (Success)

```json
{
  "request_id": "REQ-2025-001234",
  "response_id": "RES-2025-005678",
  "timestamp": "2025-11-19T14:30:15Z",
  "status": "success",
  "version": "1.0",
  "data": {
    // Payload specifico SP qui
  },
  "metadata": {
    "execution_time_ms": 245,
    "records_processed": 1,
    "records_failed": 0,
    "warnings": []
  }
}
```

### Campi Dettaglio

| Campo | Tipo | Descrizione |
|-------|------|------------|
| `request_id` | string | ID request originale (per correlazione) |
| `response_id` | string | ID univoco response |
| `timestamp` | ISO 8601 | Timestamp elaborazione |
| `status` | enum | "success", "warning", "error", "partial" |
| `version` | string | Versione API |
| `data` | object | Payload risultato specifico SP |
| `metadata.execution_time_ms` | number | Tempo elaborazione in ms |
| `metadata.records_processed` | number | Record elaborati (se batch) |
| `metadata.records_failed` | number | Record falliti (se batch) |
| `metadata.warnings` | array | Warning non-blocking |

---

## ⚠️ STRUTTURA RESPONSE ERROR

### HTTP 400 - Bad Request
```json
{
  "request_id": "REQ-2025-001234",
  "response_id": "RES-2025-005678",
  "timestamp": "2025-11-19T14:30:15Z",
  "status": "error",
  "version": "1.0",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Campo 'email' è obbligatorio",
    "details": [
      {
        "field": "email",
        "reason": "required",
        "value": null
      }
    ]
  },
  "metadata": {
    "http_status": 400,
    "error_type": "CLIENT_ERROR"
  }
}
```

### HTTP 422 - Unprocessable Entity
```json
{
  "request_id": "REQ-2025-001234",
  "response_id": "RES-2025-005678",
  "timestamp": "2025-11-19T14:30:15Z",
  "status": "error",
  "version": "1.0",
  "error": {
    "code": "PROCESSING_ERROR",
    "message": "Impossibile elaborare il documento: formato non riconosciuto",
    "details": [
      {
        "step": "document_parsing",
        "reason": "unsupported_format",
        "expected": "PDF, DOCX, TXT",
        "received": "XLS"
      }
    ]
  },
  "metadata": {
    "http_status": 422,
    "error_type": "VALIDATION_ERROR"
  }
}
```

### HTTP 500 - Server Error
```json
{
  "request_id": "REQ-2025-001234",
  "response_id": "RES-2025-005678",
  "timestamp": "2025-11-19T14:30:15Z",
  "status": "error",
  "version": "1.0",
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Errore interno durante l'elaborazione",
    "details": [
      {
        "service": "SP01-EML-PARSER",
        "operation": "email_extraction",
        "error_id": "ERR-2025-67890"
      }
    ]
  },
  "metadata": {
    "http_status": 500,
    "error_type": "SERVER_ERROR",
    "support_contact": "support@zendata.local"
  }
}
```

---

## 📊 PAYLOAD SPECIFICO SP - ESEMPIO (SP01 - EML Parser)

### Request (seguendo template standard)
```json
{
  "request_id": "REQ-2025-001234",
  "timestamp": "2025-11-19T14:30:00Z",
  "version": "1.0",
  "metadata": {
    "user_id": "USR-12345",
    "session_id": "SESS-67890",
    "source": "api"
  },
  "data": {
    "eml_file_path": "s3://zenia-bucket/emails/incoming/email_001.eml",
    "workflow_id": "WF-UC5-SP01-001",
    "extract_options": {
      "validate_pec_signature": true,
      "extract_attachments": true,
      "extract_headers": true
    }
  },
  "options": {
    "timeout_ms": 60000,
    "retry_policy": "exponential"
  }
}
```

### Response Success
```json
{
  "request_id": "REQ-2025-001234",
  "response_id": "RES-2025-005678",
  "timestamp": "2025-11-19T14:30:15Z",
  "status": "success",
  "version": "1.0",
  "data": {
    "email_id": "EMAIL-2025-001",
    "workflow_id": "WF-UC5-SP01-001",
    "parsing_status": "success",
    "metadata": {
      "sender": "protocollo@comune.example.it",
      "recipients": ["protocollo@zendata.local"],
      "subject": "Richiesta protocollo - Documento allegato",
      "received_at": "2025-11-19T14:25:00Z"
    },
    "pec_validation": {
      "is_pec": true,
      "signature_valid": true,
      "certificate_issuer": "ArubaPEC"
    },
    "attachments": [
      {
        "filename": "documento_richiesta.pdf",
        "mime_type": "application/pdf",
        "size_bytes": 245678,
        "hash_sha256": "abc123def456..."
      }
    ]
  },
  "metadata": {
    "execution_time_ms": 1245,
    "records_processed": 1,
    "warnings": []
  }
}
```

---

## ✅ CHECKLIST PER SP CREATORS

Quando crei un nuovo SP, assicurati che:

- [ ] Request contiene: `request_id`, `timestamp`, `version`
- [ ] Request contiene `metadata` con almeno `user_id` (se applicabile)
- [ ] Request contiene `data` con payload specifico SP
- [ ] Request contiene `options` con timeout e retry policy (opzionale)
- [ ] Response success contiene: `request_id`, `response_id`, `timestamp`, `status`, `version`
- [ ] Response success contiene `data` con risultato specifico SP
- [ ] Response success contiene `metadata` con `execution_time_ms` e `records_processed`
- [ ] Error responses seguono template HTTP 400/422/500
- [ ] Error responses contengono `error.code`, `error.message`, `error.details`
- [ ] Tutti i campi usano `snake_case`
- [ ] ISO 8601 per tutti i timestamp
- [ ] ID univoci generati con formato standardizzato (REQ-YYYY-XXXXX, RES-YYYY-XXXXX)

---

## 📝 ESEMPI PER PATTERN COMUNI

### Pattern: Batch Processing
```json
{
  "request_id": "REQ-2025-001234",
  "data": {
    "items": [
      { "id": "ITEM-1", "data": {...} },
      { "id": "ITEM-2", "data": {...} }
    ],
    "batch_size": 100
  }
}
```

**Response**:
```json
{
  "response_id": "RES-2025-005678",
  "data": {
    "results": [
      { "id": "ITEM-1", "result": "success", "output": {...} },
      { "id": "ITEM-2", "result": "error", "error": "Invalid format" }
    ]
  },
  "metadata": {
    "records_processed": 2,
    "records_failed": 1
  }
}
```

### Pattern: Async Processing
```json
{
  "request_id": "REQ-2025-001234",
  "options": {
    "async": true
  }
}
```

**Response** (immediate):
```json
{
  "response_id": "RES-2025-005678",
  "status": "accepted",
  "data": {
    "job_id": "JOB-2025-001",
    "status_url": "https://api.zendata.local/jobs/JOB-2025-001/status"
  }
}
```

**Callback** (quando completato):
```json
{
  "job_id": "JOB-2025-001",
  "status": "completed",
  "result": {...}
}
```

---

## 🔗 RIFERIMENTI

- Vedere pagine SPECIFICATION.md nei singoli SP per dettagli implementativi
- Vedi Payload esempi nei singoli SP (SP01, SP04, SP10, SP12, etc.)
- Conformità normativa: Per normative applicate, vedi `docs/COMPLIANCE-MATRIX.md`
- Architettura MS: Per dettagli microservizi, vedi `docs/microservices/MS-ARCHITECTURE-MASTER.md`

---

**Approvato da**: Architecture Team
**Versione**: 1.0 (19 novembre 2025)
**Prossima Review**: 19 dicembre 2025

