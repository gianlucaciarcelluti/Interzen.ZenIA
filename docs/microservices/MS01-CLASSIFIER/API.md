# MS01 - Riferimento API Classificatore

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)

## Indice

1. [URL Base](#url-base)
2. [Autenticazione](#autenticazione)
3. [Endpoint](#endpoint)
4. [Limitazione del Tasso](#limitazione-del-tasso)
5. [Gestione Errori](#gestione-errori)
6. [Esempi di Richiesta/Risposta](#esempi-di-richiestaris posta)

---

## URL Base
```
http://localhost:8001/api/v1
```

## Autenticazione
Tutti gli endpoint richiedono un token Bearer nell'intestazione Authorization:
```
Authorization: Bearer <jwt-token>
```

[↑ Torna al Indice](#indice)

---

## Endpoint

### 1. Classifica Documento
**POST** `/classify`

Classifica un singolo documento in base al contenuto e ai metadati.

#### Richiesta
```json
{
  "document_id": "doc-2024-11-18-001",
  "filename": "invoice_20241115.pdf",
  "file_content": "JVBERi0xLjQK...",
  "file_size": 245632,
  "mime_type": "application/pdf",
  "metadata": {
    "source": "email",
    "sender": "vendor@example.com",
    "received_date": "2024-11-18T10:30:00Z",
    "department": "procurement"
  },
  "classification_hints": ["invoice"]
}
```

#### Response (Success 200)
```json
{
  "document_id": "doc-2024-11-18-001",
  "classification": {
    "type": "invoice",
    "confidence": 0.97,
    "category": "financial",
    "requires_review": false
  },
  "routing": {
    "next_step": "SP03-PROCEDURAL-CLASSIFIER",
    "workflow_id": "UC5-INVOICE"
  },
  "processing_time_ms": 342
}
```

#### Risposta (Errori)
- **400 Bad Request**: Input non valido (campi obbligatori mancanti)
- **413 Payload Too Large**: File supera la dimensione massima
- **422 Unprocessable Entity**: Formato file non supportato
- **500 Internal Server Error**: Errore motore di classificazione
- **503 Service Unavailable**: Errore caricamento modello

---

### 2. Classifica in Batch
**POST** `/classify/batch`

Classifica più documenti in una singola richiesta.

#### Richiesta
```json
{
  "batch_id": "batch-2024-11-18-001",
  "documents": [
    {
      "document_id": "doc-1",
      "filename": "invoice_1.pdf",
      "file_content": "base64-content",
      "mime_type": "application/pdf"
    },
    {
      "document_id": "doc-2",
      "filename": "contract_2.docx",
      "file_content": "base64-content",
      "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
  ]
}
```

#### Response (Success 200)
```json
{
  "batch_id": "batch-2024-11-18-001",
  "total_documents": 2,
  "successful": 2,
  "failed": 0,
  "results": [
    {
      "document_id": "doc-1",
      "classification": {
        "type": "invoice",
        "confidence": 0.97
      }
    },
    {
      "document_id": "doc-2",
      "classification": {
        "type": "contract",
        "confidence": 0.88
      }
    }
  ],
  "processing_time_ms": 1245
}
```

---

### 3. Ottieni Cache di Classificazione
**GET** `/classify/{document_id}`

Recupera il risultato di classificazione memorizzato in cache (se disponibile).

#### Risposta (Successo 200)
```json
{
  "document_id": "doc-2024-11-18-001",
  "classification": {
    "type": "invoice",
    "confidence": 0.97
  },
  "cached": true,
  "cache_age_hours": 2,
  "timestamp": "2024-11-18T08:30:00Z"
}
```

#### Risposta (Non Trovato 404)
```json
{
  "error": "Classification not found in cache",
  "document_id": "doc-2024-11-18-001"
}
```

---

### 4. Aggiorna Classificazione (Sovrascrittura Manuale)
**PUT** `/classify/{document_id}`

Sovrascrivi la classificazione automatizzata con correzione manuale.

#### Richiesta
```json
{
  "classification_type": "invoice",
  "confidence": 1.0,
  "reviewer_comment": "Manual review: confirmed as invoice",
  "reviewed_by": "user@company.com"
}
```

#### Response (Success 200)
```json
{
  "document_id": "doc-2024-11-18-001",
  "classification": {
    "type": "invoice",
    "confidence": 1.0,
    "override": true
  },
  "audit_log": "manual-override-logged"
}
```

---

### 5. Ottieni Stato del Modello
**GET** `/models/status`

Recupera la versione del modello ML attivo e le metriche di prestazione.

#### Risposta (Successo 200)
```json
{
  "models": [
    {
      "name": "document-classifier-v2.1",
      "active": true,
      "version": "2.1",
      "training_date": "2024-10-15",
      "accuracy": 0.945,
      "f1_score": 0.932,
      "last_updated": "2024-11-15T14:30:00Z"
    },
    {
      "name": "document-classifier-v2.0",
      "active": false,
      "version": "2.0",
      "accuracy": 0.928
    }
  ],
  "cache_stats": {
    "total_cached": 15432,
    "cache_hit_rate": 0.78,
    "cache_size_mb": 245
  }
}
```

---

### 6. Controllo Salute
**GET** `/health`

Controllo della salute e prontezza del servizio.

#### Risposta (Successo 200)
```json
{
  "status": "healthy",
  "service": "MS01-CLASSIFIER",
  "uptime_seconds": 86400,
  "model_loaded": true,
  "database_connected": true,
  "last_classification": "2024-11-18T10:50:30Z",
  "requests_processed": 45230
}
```

#### Risposta (Degradato 503)
```json
{
  "status": "degraded",
  "service": "MS01-CLASSIFIER",
  "issues": ["ML model loading", "cache connection timeout"],
  "retry_after_seconds": 30
}
```

[↑ Torna al Indice](#indice)

---

## Limitazione del Tasso

### Limiti per Tenant
- 1000 richieste/minuto per tier standard
- 5000 richieste/minuto per tier premium
- 50 richieste concorrenti per tenant

### Intestazioni di Risposta
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1700318400
```

[↑ Torna al Indice](#indice)

---

## Gestione Errori

### Risposte di Errore Comuni

#### 400 Richiesta Non Valida
```json
{
  "error_code": "INVALID_REQUEST",
  "message": "Missing required field: filename",
  "details": {
    "field": "filename",
    "reason": "required"
  }
}
```

#### 413 Payload Troppo Grande
```json
{
  "error_code": "FILE_TOO_LARGE",
  "message": "File size 150MB exceeds maximum 100MB",
  "max_size_mb": 100,
  "provided_size_mb": 150
}
```

#### 422 Entità Non Elaborabile
```json
{
  "error_code": "UNSUPPORTED_FORMAT",
  "message": "MIME type application/x-custom not supported",
  "supported_types": ["application/pdf", "application/msword", "text/plain"]
}
```

[↑ Torna al Indice](#indice)

---

## Caso d'Uso: Workflow Completo End-to-End

### Scenario: Fattura da Email (UC5 - Produzione Documentale)

Questo scenario mostra il flusso completo di una fattura ricevuta via email che viene classificata e inoltrata al pipeline di generazione documentale.

#### Step 1: Client invia richiesta di classificazione

```bash
curl -X POST http://localhost:8001/api/v1/classify \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d @payload_invoice.json
```

**Payload: `payload_invoice.json`**
```json
{
  "document_id": "doc-2024-11-18-vendor-001",
  "filename": "FATTURA-2024-11-15-ACME.pdf",
  "file_content": "JVBERi0xLjQK%JFxEU1RhcnQgcmVmCjEwIDAgb2JqCjw8L1R5cGUvQ2F0YWxvZy9QYWdlcyAyIDAgUj4+CmVuZG9iag...",
  "file_size": 245632,
  "mime_type": "application/pdf",
  "metadata": {
    "source": "email",
    "sender": "fatture@acme-corp.com",
    "received_date": "2024-11-18T10:15:00Z",
    "subject": "FATTURA 2024-11-15",
    "department": "procurement",
    "user_role": "document-processor"
  },
  "classification_hints": ["invoice", "procurement"],
  "force_reprocessing": false
}
```

#### Step 2: MS01 valida e processa

**Operazioni interne**:
1. Document Intake Handler: valida input ✓
2. Cache Layer: verifica Redis (MISS)
3. Feature Extractor: estrae features
4. Quality Validator: controlli di sicurezza ✓
5. Classification Engine: esegue modello ML
6. Router: determina routing
7. Metrics Collector: registra metriche

#### Step 3: MS01 risponde con classificazione

**Response: 200 OK**
```json
{
  "document_id": "doc-2024-11-18-vendor-001",
  "classification_result": {
    "primary_type": "invoice",
    "primary_confidence": 0.97,
    "secondary_types": [
      {
        "type": "procurement_document",
        "confidence": 0.88
      },
      {
        "type": "financial_document",
        "confidence": 0.82
      }
    ],
    "category": "financial",
    "urgency": "normal",
    "requires_manual_review": false
  },
  "metadata_extracted": {
    "document_language": "it",
    "key_entities": {
      "vendor_name": "ACME Corp SRL",
      "vendor_id": "IT12345678901",
      "invoice_number": "FATTURA-2024-11-15",
      "invoice_date": "2024-11-15",
      "document_date": "2024-11-15",
      "due_date": "2024-12-15",
      "total_amount": "2.450,00",
      "currency": "EUR",
      "tax_amount": "538,00",
      "vat_rate": 0.22
    },
    "extracted_keywords": ["invoice", "payment", "procurement", "tax", "vendor"]
  },
  "quality_checks": {
    "file_integrity": {
      "status": "PASS",
      "checksum_algorithm": "SHA256",
      "checksum_value": "a1b2c3d4e5f6..."
    },
    "format_compliance": {
      "status": "PASS",
      "standard": "ISO/IEC 32000 (PDF)",
      "warnings": []
    },
    "malware_scan": {
      "status": "CLEAN",
      "engine": "ClamAV",
      "scan_timestamp": "2024-11-18T10:15:15Z"
    },
    "size_check": {
      "status": "PASS",
      "size_bytes": 245632
    },
    "overall_status": "PASS"
  },
  "routing": {
    "next_pipeline": "SP03-PROCEDURAL-CLASSIFIER",
    "workflow_id": "UC5-INVOICE-PROCESSING-ACME",
    "priority": "normal",
    "sla_minutes": 15,
    "routing_rules_applied": [
      "document_type:invoice → UC5-pipeline",
      "confidence:0.97 → fast_track",
      "vendor:ACME → standard_processing"
    ]
  },
  "processing_time_ms": 342,
  "timestamp": "2024-11-18T10:15:45.123Z",
  "request_id": "req-2024-11-18-001"
}
```

#### Step 4: Downstream processing (SP03 → SP05 → SP06)

Il routing indica che il documento deve andare a **SP03-PROCEDURAL-CLASSIFIER**:

```
MS01 Response → Message Queue (RabbitMQ)
   ↓
SP03 consuma messaggio
   ├─ Applica regole procedurali
   ├─ Arricchisce con template mapping
   └─ → SP05 (Template Engine)
        ├─ Genera documento output
        └─ → SP06 (Validator)
             ├─ Validazione finale
             └─ → Dashboard (SP10) - Notifica completamento
```

---

### Scenario 2: Hit Cache (Fast Path)

Se lo stesso documento viene inviato di nuovo entro 24 ore:

```bash
curl -X POST http://localhost:8001/api/v1/classify \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d @payload_invoice_same.json
```

**Response: 200 OK (da cache, ~50ms)**
```json
{
  "document_id": "doc-2024-11-18-vendor-001",
  "classification_result": {
    "primary_type": "invoice",
    "primary_confidence": 0.97,
    "category": "financial",
    "urgency": "normal",
    "requires_manual_review": false
  },
  "cached": true,
  "cache_age_ms": 12453,
  "routing": {
    "next_pipeline": "SP03-PROCEDURAL-CLASSIFIER",
    "workflow_id": "UC5-INVOICE-PROCESSING-ACME"
  },
  "processing_time_ms": 48,
  "timestamp": "2024-11-18T10:27:38.576Z"
}
```

**Vantaggio**: Riduzione latenza da 342ms a 48ms (7x più veloce)

---

### Scenario 3: Classificazione Ambigua (Low Confidence)

Se il documento è difficile da classificare:

**Payload**: Documento scansionato di bassa qualità
```json
{
  "document_id": "doc-2024-11-18-unknown-001",
  "filename": "scanned_document_bad_quality.pdf",
  "file_content": "...",
  "mime_type": "application/pdf",
  "metadata": {
    "source": "scanner",
    "quality": "low"
  }
}
```

**Response: 202 Accepted (Richiede Revisione)**
```json
{
  "document_id": "doc-2024-11-18-unknown-001",
  "classification_result": {
    "primary_type": "contract",
    "primary_confidence": 0.58,
    "secondary_types": [
      {
        "type": "agreement",
        "confidence": 0.52
      },
      {
        "type": "report",
        "confidence": 0.41
      }
    ],
    "requires_manual_review": true,
    "review_reason": "Primary confidence 0.58 below threshold 0.70 (low document quality)"
  },
  "status": "PENDING_REVIEW",
  "review_id": "review-2024-11-18-low-confidence-001",
  "review_queue": "MANUAL_CLASSIFICATION_QUEUE",
  "estimated_review_time_minutes": 15,
  "message": "Document queued for manual review by human classifier. Awaiting reviewer attention.",
  "processing_time_ms": 285,
  "timestamp": "2024-11-18T10:30:22.456Z"
}
```

**Human Reviewer Flow**:
```
Review Queue
   ↓ (Reviewer opens dashboard)
Decision: Contract
   ↓
PUT /api/v1/classify/doc-2024-11-18-unknown-001
   {
     "classification_type": "contract",
     "confidence": 1.0,
     "reviewer_comment": "Manual review: Confirmed as Supplier Agreement",
     "reviewed_by": "reviewer@company.com"
   }
   ↓
Response: Classification Updated
   └─ Sent to routing pipeline with manual override flag
```

---

### Scenario 4: Batch Processing

Classificazione di 100 fatture in una singola richiesta:

```bash
curl -X POST http://localhost:8001/api/v1/classify/batch \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d @batch_invoices.json
```

**Payload: `batch_invoices.json`** (estratto)
```json
{
  "batch_id": "batch-2024-11-18-acme-monthly",
  "documents": [
    {
      "document_id": "doc-invoice-001",
      "filename": "invoice_001.pdf",
      "file_content": "..",
      "mime_type": "application/pdf"
    },
    {
      "document_id": "doc-invoice-002",
      "filename": "invoice_002.pdf",
      "file_content": "..",
      "mime_type": "application/pdf"
    }
  ]
}
```

**Response: 200 OK**
```json
{
  "batch_id": "batch-2024-11-18-acme-monthly",
  "total_documents": 100,
  "successful": 98,
  "failed": 2,
  "processing_time_ms": 18542,
  "results": [
    {
      "document_id": "doc-invoice-001",
      "status": "SUCCESS",
      "classification": {
        "type": "invoice",
        "confidence": 0.96
      },
      "processing_time_ms": 185
    },
    {
      "document_id": "doc-invoice-002",
      "status": "SUCCESS",
      "classification": {
        "type": "invoice",
        "confidence": 0.94
      },
      "processing_time_ms": 192
    },
    {
      "document_id": "doc-invoice-050",
      "status": "FAILED",
      "error": {
        "code": "FILE_CORRUPTED",
        "message": "PDF file header corrupted"
      }
    }
  ],
  "batch_statistics": {
    "average_confidence": 0.948,
    "cache_hits": 45,
    "cache_misses": 53,
    "hit_rate": 0.459,
    "average_processing_time_ms": 185
  }
}
```

---

## Esempi di Richiesta/Risposta

Vedi la cartella [examples/](../examples/) per campioni dettagliati:
- `request.json`: Richiesta di classificazione completa
- `response.json`: Risposta di classificazione completa
- `batch_request.json`: Esempio di elaborazione batch
- `error_response.json`: Esempi di risposta di errore
- `end_to_end_workflow.md`: Workflow completo per UC5

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)
