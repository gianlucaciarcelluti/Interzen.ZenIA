# ZenShareUp ↔ ZenIA: Architettura di Integrazione

**Documento**: Mappatura completa dei flussi di integrazione tra ZenShareUp e ZenIA
**Data**: 20 novembre 2025
**Status**: DEFINITIVA
**Versione**: 1.0

---

## Indice

1. [Visione d'Insieme](#visione-dinsieme)
2. [Architettura di Integrazione](#architettura-di-integrazione)
3. [Flussi Documentali Principali](#flussi-documentali-principali)
4. [Mapping Microservizi ZenIA](#mapping-microservizi-zenia)
5. [Input/Output per Microservizio](#inputoutput-per-microservizio)
6. [Protocolli di Comunicazione](#protocolli-di-comunicazione)
7. [Workflow End-to-End](#workflow-end-to-end)
8. [Dati Scambiati](#dati-scambiati)
9. [Gestione Errori e Fallback](#gestione-errori-e-fallback)
10. [Performance e SLA](#performance-e-sla)

---

## Visione d'Insieme

### Ruoli Funzionali

```mermaid
graph LR
    ZS["🗄️ ZenShareUp<br/>(Document Storage & Management)"]
    ZIA["🧠 ZenIA<br/>(Intelligent Processing)"]

    ZS -->|📤 Invia Documenti<br/>per Elaborazione| ZIA
    ZIA -->|📥 Ritorna Risultati<br/>Arricchiti| ZS

    style ZS fill:#e3f2fd,stroke:#1976d2,stroke-width:3px
    style ZIA fill:#f3e5f5,stroke:#7b1fa2,stroke-width:3px
```

**ZenShareUp** è il **repository centralized** di gestione documentale:
- Archiviazione persistente dei documenti
- Gestione del ciclo di vita (creazione, modifica, archivio)
- Multi-tenancy e isolamento dei dati
- Audit trail e compliance

**ZenIA** è il **motore intelligente** di elaborazione:
- Classificazione automatica dei documenti
- Validazione e trasformazione contenuti
- Estrazione intelligente di metadati
- Ottimizzazione e arricchimento dati
- Orchestrazione di processi complessi

### Relazione Fondamentale

ZenShareUp fornisce i **dati grezzi** (raw documents), ZenIA li **processa intelligentemente** e ritorna i **risultati arricchiti** (enriched metadata, classifications, transformations) a ZenShareUp per la memorizzazione e l'utilizzo nei workflow successivi.

---

## Architettura di Integrazione

### Topologia Generale

```mermaid
graph TB
    subgraph ZenShareUp["📦 ZenShareUp (Document Hub)"]
        ZS_API["REST API Gateway"]
        ZS_DB["Document Storage<br/>PostgreSQL"]
        ZS_CACHE["Cache Layer<br/>Redis"]
        ZS_QUEUE["Task Queue<br/>RabbitMQ"]
    end

    subgraph ZenIA["🧠 ZenIA (Intelligent Processing)"]
        MS01["MS01 Classifier"]
        MS02["MS02 Analyzer"]
        MS03["MS03 Orchestrator"]
        MS04["MS04 Validator"]
        MS05["MS05 Transformer"]
        MS06["MS06 Aggregator"]
        MS07["MS07 Distributor"]
        MS11["MS11 Gateway"]
        MS13["MS13 Security"]
    end

    subgraph Infrastructure["🔧 Infrastruttura Condivisa"]
        BROKER["Message Broker<br/>RabbitMQ"]
        CACHE["Distributed Cache<br/>Redis"]
        DB["Database Layer<br/>PostgreSQL"]
    end

    ZS_API -->|Document Stream| MS11
    ZS_QUEUE -->|Async Tasks| BROKER

    MS11 -->|Orchestrate| MS03
    MS03 -->|Classify| MS01
    MS03 -->|Validate| MS04
    MS03 -->|Transform| MS05

    MS01 & MS04 & MS05 -->|Store Results| CACHE
    MS01 & MS04 & MS05 -->|Persist| DB

    MS06 -->|Aggregate| MS05
    MS07 -->|Distribute| DB
    MS13 -->|Security| BROKER

    CACHE -->|Return to| ZS_API
    DB -->|Store| ZS_DB

    style ZenShareUp fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style ZenIA fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style Infrastructure fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
```

### Punti di Integrazione Critici

| Componente | Ruolo | Protocollo | Frequenza |
|-----------|-------|-----------|-----------|
| **MS11-GATEWAY** | Porta d'ingresso | REST/gRPC | Sincrono |
| **Message Broker** | Async communication | RabbitMQ AMQP | Asincrono |
| **Cache Layer** | Result sharing | Redis Pub/Sub | Real-time |
| **Database Layer** | Data persistence | PostgreSQL | Transazionale |

---

## Flussi Documentali Principali

### 1. Flusso di Classificazione Automatica

Quando ZenShareUp riceve un nuovo documento, lo invia a ZenIA per classificazione intelligente.

```mermaid
sequenceDiagram
    participant ZS as ZenShareUp<br/>API
    participant MS01 as MS01<br/>Classifier
    participant MS02 as MS02<br/>Analyzer
    participant CACHE as Redis<br/>Cache
    participant ZS_DB as ZenShareUp<br/>DB

    ZS->>MS01: POST /classify<br/>{ documentId, fileHash, metadata }
    activate MS01

    MS01->>MS01: 1. Extract features
    MS01->>MS01: 2. Run ML models
    MS01->>MS02: GET metadata & context
    activate MS02
    MS02-->>MS01: Return analysis
    deactivate MS02

    MS01->>CACHE: Cache classification
    MS01-->>ZS: { classificationId, type,<br/>confidence, labels }
    deactivate MS01

    ZS->>ZS_DB: Store classification<br/>in document metadata

    Note over ZS,ZS_DB: Document ora contiene:<br/>originalMetadata + classification
```

**Input da ZenShareUp:**
- `documentId`: Identificatore univoco
- `fileHash`: SHA-256 per integrità
- `metadata`: Nome, dimensione, tipo MIME, data caricamento
- `tenantId`: Identificatore tenant per isolamento

**Output da ZenIA:**
- `classificationId`: UUID della classificazione
- `documentType`: Tipo riconosciuto (Fattura, Contratto, etc.)
- `confidence`: Score 0.0-1.0
- `labels`: Array di categorie
- `processingTime`: Millisecondi impiegati

---

### 2. Flusso di Validazione e Trasformazione

```mermaid
sequenceDiagram
    participant ZS as ZenShareUp
    participant MS04 as MS04<br/>Validator
    participant MS05 as MS05<br/>Transformer
    participant MS06 as MS06<br/>Aggregator
    participant DB as Database

    ZS->>MS04: POST /validate<br/>{ documentId, format, rules }
    activate MS04

    MS04->>MS04: 1. Validate structure
    MS04->>MS04: 2. Check compliance
    MS04->>MS04: 3. Verify signatures

    alt Validation Passed
        MS04->>MS05: Send to transform
        activate MS05
        MS05->>MS05: 1. Convert format
        MS05->>MS05: 2. Normalize content
        MS05->>MS06: Aggregate results
        activate MS06
        MS06->>DB: Store transformed
        MS06-->>MS05: Acknowledge
        deactivate MS06
        MS05-->>MS04: Return transformed
        deactivate MS05
        MS04-->>ZS: { status: valid, documentId,<br/>transformedFileId, metadata }
    else Validation Failed
        MS04->>DB: Log errors
        MS04-->>ZS: { status: invalid, errors,<br/>suggestions }
    end
    deactivate MS04

    ZS->>ZS: Update document status
```

**Input da ZenShareUp:**
- `documentId`: Identificatore del documento
- `format`: Formato attuale (PDF, DOCX, etc.)
- `rules`: Set di regole di validazione
- `targetFormat`: Formato di destinazione desiderato

**Output da ZenIA:**
- `validationStatus`: VALID / INVALID
- `errors`: Array dettagliato di errori
- `transformedFileId`: ID del file trasformato
- `enrichedMetadata`: Metadati estratti e normalizzati

---

### 3. Flusso di Orchestrazione Completa

```mermaid
graph TB
    subgraph Phase1["Fase 1: Ricezione"]
        A["ZenShareUp invia<br/>documento grezzo"]
        B["MS11 Gateway<br/>autenticazione e routing"]
    end

    subgraph Phase2["Fase 2: Elaborazione"]
        C["MS03 Orchestrator<br/>decide workflow"]
        D["MS01 Classifier<br/>identifica tipo"]
        E["MS04 Validator<br/>verifica struttura"]
        F["MS05 Transformer<br/>normalizza formato"]
    end

    subgraph Phase3["Fase 3: Arricchimento"]
        G["MS02 Analyzer<br/>estrae metadati"]
        H["MS06 Aggregator<br/>unisce risultati"]
        I["MS13 Security<br/>applica encryption"]
    end

    subgraph Phase4["Fase 4: Restituzione"]
        J["MS07 Distributor<br/>ritorna a ZenShareUp"]
        K["ZenShareUp archivia<br/>documento arricchito"]
    end

    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
    D --> G
    E --> G
    F --> H
    G --> H
    H --> I
    I --> J
    J --> K

    style A fill:#fff9c4
    style K fill:#c8e6c9
    style Phase1 fill:#e3f2fd
    style Phase2 fill:#f3e5f5
    style Phase3 fill:#ffe0b2
    style Phase4 fill:#e1f5fe
```

---

## Mapping Microservizi ZenIA

### Tabella Riepilogativa

| MS | Nome | Ruolo | Input da | Output a |
|----|------|-------|----------|----------|
| **MS01** | Classifier | Classificazione documenti | ZenShareUp | MS03, CACHE |
| **MS02** | Analyzer | Analisi e estrazione | MS03 | MS06 |
| **MS03** | Orchestrator | Coordinamento workflow | MS11 | MS01-02, MS04-07 |
| **MS04** | Validator | Validazione struttura | MS03 | MS05, CACHE |
| **MS05** | Transformer | Trasformazione formato | MS04 | MS06, CACHE |
| **MS06** | Aggregator | Aggregazione risultati | MS05, MS02 | MS07, DB |
| **MS07** | Distributor | Distribuzione output | MS06 | ZenShareUp |
| **MS08** | Monitor | Monitoraggio esecuzione | Tutti | Logging, Alerts |
| **MS09** | Manager | Gestione risorse | Tutti | Resource allocation |
| **MS10** | Logger | Logging centralizzato | Tutti | Audit trail |
| **MS11** | Gateway | Ingresso richieste | ZenShareUp | MS03 |
| **MS12** | Cache | Caching distribuito | Tutti | Tutti |
| **MS13** | Security | Sicurezza e encryption | Tutti | Tutti |
| **MS14** | Audit | Audit trail | Tutti | Database |
| **MS15** | Config | Gestione configurazioni | Tutti | Tutti |
| **MS16** | Registry | Service registry | Tutti | Tutti |

---

## Input/Output per Microservizio

### MS01 - Classifier

**Input da ZenShareUp:**
```json
{
  "documentId": "doc_uuid_12345",
  "tenantId": "tenant_001",
  "fileHash": "sha256_value",
  "fileName": "fattura_2025_001.pdf",
  "fileMimeType": "application/pdf",
  "fileSize": 245000,
  "uploadedAt": "2025-11-20T10:30:00Z",
  "metadata": {
    "source": "email_gateway",
    "sender": "cliente@azienda.it"
  }
}
```

**Output a ZenShareUp:**
```json
{
  "classificationId": "cls_uuid_67890",
  "documentId": "doc_uuid_12345",
  "classification": {
    "primaryType": "INVOICE",
    "secondaryTypes": ["FINANCIAL_DOCUMENT"],
    "confidence": 0.98,
    "model": "ml_classifier_v2.3",
    "processingTime": 245
  },
  "metadata": {
    "language": "it-IT",
    "keyTerms": ["fattura", "importo", "cliente"],
    "entities": {
      "amount": "1,500.00€",
      "currency": "EUR",
      "invoiceNumber": "2025-001"
    }
  },
  "routing": {
    "nextService": "MS04-VALIDATOR",
    "priority": "NORMAL",
    "workflowId": "wf_invoice_processing"
  }
}
```

### MS02 - Analyzer

**Input da MS03 Orchestrator:**
```json
{
  "documentId": "doc_uuid_12345",
  "classificationId": "cls_uuid_67890",
  "analysisType": "FULL_EXTRACTION",
  "options": {
    "extractText": true,
    "extractTables": true,
    "extractImages": true,
    "performOCR": false,
    "identifyEntities": true
  }
}
```

**Output a MS06:**
```json
{
  "analysisId": "ana_uuid_11111",
  "documentId": "doc_uuid_12345",
  "extractedContent": {
    "text": "Full text content...",
    "tables": [{ "id": "tbl_001", "rows": 5, "columns": 3 }],
    "images": [{ "id": "img_001", "format": "png", "size": 5000 }]
  },
  "entities": {
    "person": ["Mario Rossi"],
    "organization": ["Azienda SPA"],
    "location": ["Milano"],
    "amounts": [{ "value": 1500, "currency": "EUR" }]
  },
  "summary": "Document analysis complete with 98% accuracy",
  "processingTime": 1250
}
```

### MS03 - Orchestrator

**Input da MS11:**
```json
{
  "requestId": "req_uuid_22222",
  "documentId": "doc_uuid_12345",
  "classificationId": "cls_uuid_67890",
  "workflowType": "STANDARD_DOCUMENT_PROCESSING",
  "priority": "NORMAL",
  "options": {
    "parallelProcessing": true,
    "validateStructure": true,
    "transformFormat": true,
    "enrichMetadata": true
  }
}
```

**Output:**
- Coordina l'esecuzione di MS01, MS02, MS04-05
- Gestisce la sequenza logica basata su regole di business
- Ritorna a MS11 lo stato dell'orchestrazione

### MS04 - Validator

**Input da MS03:**
```json
{
  "documentId": "doc_uuid_12345",
  "classificationId": "cls_uuid_67890",
  "validationRules": [
    { "rule": "PDF_STRUCTURE", "severity": "CRITICAL" },
    { "rule": "SIGNATURE_INTEGRITY", "severity": "HIGH" },
    { "rule": "COMPLIANCE_CAD", "severity": "HIGH" }
  ],
  "documentType": "INVOICE"
}
```

**Output a MS05:**
```json
{
  "validationId": "val_uuid_33333",
  "documentId": "doc_uuid_12345",
  "validationStatus": "VALID",
  "results": [
    {
      "rule": "PDF_STRUCTURE",
      "passed": true,
      "message": "PDF structure is valid"
    },
    {
      "rule": "SIGNATURE_INTEGRITY",
      "passed": true,
      "certificateId": "cert_xyz"
    },
    {
      "rule": "COMPLIANCE_CAD",
      "passed": true,
      "complianceLevel": "FULL"
    }
  ],
  "processingTime": 530
}
```

### MS05 - Transformer

**Input da MS04:**
```json
{
  "documentId": "doc_uuid_12345",
  "validationId": "val_uuid_33333",
  "transformationRules": {
    "sourceFormat": "PDF",
    "targetFormat": "PDF_OPTIMIZED",
    "actions": [
      "COMPRESS_IMAGES",
      "NORMALIZE_FONTS",
      "REMOVE_METADATA_ARTIFACTS"
    ]
  }
}
```

**Output a MS06:**
```json
{
  "transformationId": "tra_uuid_44444",
  "documentId": "doc_uuid_12345",
  "originalFormat": "PDF",
  "transformedFormat": "PDF_OPTIMIZED",
  "transformedFileId": "file_uuid_transformed",
  "metadata": {
    "originalSize": 245000,
    "transformedSize": 156000,
    "compressionRatio": 0.636,
    "processingTime": 875
  },
  "status": "SUCCESS"
}
```

### MS06 - Aggregator

**Input da MS05 e MS02:**
```json
{
  "documentId": "doc_uuid_12345",
  "transformationId": "tra_uuid_44444",
  "analysisId": "ana_uuid_11111",
  "classificationId": "cls_uuid_67890",
  "validationId": "val_uuid_33333"
}
```

**Output a MS07:**
```json
{
  "aggregationId": "agg_uuid_55555",
  "documentId": "doc_uuid_12345",
  "enrichedDocument": {
    "classification": { "primaryType": "INVOICE", "confidence": 0.98 },
    "analysis": { "entities": [...], "summary": "..." },
    "validation": { "status": "VALID", "complianceLevel": "FULL" },
    "transformation": { "format": "PDF_OPTIMIZED", "size": 156000 },
    "metadata": {
      "processedAt": "2025-11-20T10:32:15Z",
      "totalProcessingTime": 3820,
      "servicesInvolved": 5
    }
  }
}
```

### MS07 - Distributor

**Input da MS06:**
```json
{
  "aggregationId": "agg_uuid_55555",
  "documentId": "doc_uuid_12345",
  "enrichedDocument": { ... },
  "targetRepository": "zenshareup_documents"
}
```

**Output a ZenShareUp:**
```json
{
  "distributionId": "dis_uuid_66666",
  "documentId": "doc_uuid_12345",
  "status": "READY_FOR_STORAGE",
  "enrichedData": {
    "classification": { ... },
    "analysis": { ... },
    "validation": { ... },
    "transformation": { ... }
  },
  "storageInstructions": {
    "location": "s3://zenshareup/documents/doc_uuid_12345",
    "metadata": "postgresql://documents_metadata",
    "ttl": null
  }
}
```

---

## Protocolli di Comunicazione

### REST/HTTP (Sincrono)

Utilizzato per le integrazioni critiche e request/response immediati.

**Header comuni:**
```
Authorization: Bearer {JWT_TOKEN}
X-Tenant-ID: {tenant_001}
X-Request-ID: {uuid}
X-Correlation-ID: {uuid}
Content-Type: application/json
```

**Endpoint MS11 Gateway:**
```
POST /api/v1/documents/classify
POST /api/v1/documents/validate
POST /api/v1/documents/transform
POST /api/v1/workflows/orchestrate
GET  /api/v1/documents/{id}/status
```

### RabbitMQ (Asincrono)

Per l'elaborazione batch e le operazioni non critiche.

**Exchange principali:**
- `zenaia.documents.topic` - Topic exchange per distribuzione documenti
- `zenaia.tasks.work` - Work queue per task asincroni
- `zenaia.results.fanout` - Fanout per broadcast risultati

**Binding:**
```
documents.created → MS01, MS03
validation.completed → MS05, MS06
transformation.ready → MS07
processing.error → MS08, MS10
```

### Redis Pub/Sub (Real-time)

Per cache distribuita e notifiche real-time.

**Canali:**
- `zenshareup:document:{id}:classification` - Notifiche classificazione
- `zenshareup:document:{id}:status` - Aggiornamenti stato
- `zenaia:cache:invalidate` - Invalidamento cache

---

## Workflow End-to-End

### Scenario: Ricezione email con allegato documento

```mermaid
sequenceDiagram
    participant EMAIL as Email Gateway
    participant ZS as ZenShareUp
    participant MS11 as MS11 Gateway
    participant MS03 as MS03 Orchestrator
    participant MS01 as MS01 Classifier
    participant MS04 as MS04 Validator
    participant MS05 as MS05 Transformer
    participant DB as Database

    EMAIL->>ZS: Ricevi email<br/>con allegato PDF
    ZS->>ZS: 1. Estrai allegato
    ZS->>ZS: 2. Calcola file hash
    ZS->>ZS: 3. Memorizzi in storage

    ZS->>MS11: POST /classify<br/>{ documentId, fileHash, metadata }
    activate MS11
    MS11->>MS11: Autenticazione JWT
    MS11->>MS03: Invia a orchestrator
    activate MS03

    MS03->>MS01: Classifica documento
    activate MS01
    MS01->>MS01: Estrai features
    MS01->>MS01: Esegui ML models
    MS01-->>MS03: { type: INVOICE, confidence: 0.98 }
    deactivate MS01

    MS03->>MS04: Valida struttura
    activate MS04
    MS04->>MS04: Check PDF structure
    MS04->>MS04: Verify signatures
    MS04-->>MS03: { status: VALID }
    deactivate MS04

    MS03->>MS05: Trasforma formato
    activate MS05
    MS05->>MS05: Comprimi immagini
    MS05->>MS05: Normalizza font
    MS05-->>MS03: { transformedFileId: ... }
    deactivate MS05

    MS03-->>MS11: Workflow completato
    deactivate MS03

    MS11->>DB: Store enriched metadata
    MS11-->>ZS: { status: SUCCESS, enrichedData: ... }
    deactivate MS11

    ZS->>ZS: Aggiorna documento<br/>con classificazione e validazione
    ZS->>DB: Salva metadata arricchiti

    Note over ZS,DB: Documento ora contiene:<br/>originalContent + classification<br/>+ validation + transformation
```

---

## Dati Scambiati

### Struttura Documento Arricchito

Quando un documento torna da ZenIA a ZenShareUp, contiene:

```json
{
  "documentId": "doc_uuid_12345",
  "tenantId": "tenant_001",
  "originalMetadata": {
    "fileName": "fattura_2025_001.pdf",
    "fileSize": 245000,
    "uploadedAt": "2025-11-20T10:30:00Z"
  },
  "enrichedMetadata": {
    "classification": {
      "primaryType": "INVOICE",
      "confidence": 0.98,
      "processingTime": 245
    },
    "validation": {
      "status": "VALID",
      "complianceLevel": "CAD_COMPLIANT",
      "signatureVerified": true
    },
    "analysis": {
      "extractedEntities": {
        "invoiceNumber": "2025-001",
        "amount": "1,500.00€",
        "customer": "Mario Rossi"
      },
      "keyTerms": ["fattura", "importo", "cliente"]
    },
    "transformation": {
      "originalFormat": "PDF",
      "transformedFormat": "PDF_OPTIMIZED",
      "compressionRatio": 0.636,
      "transformedFileId": "file_uuid_transformed"
    }
  },
  "processingMetadata": {
    "workflowId": "wf_invoice_processing",
    "totalProcessingTime": 3820,
    "servicesInvolved": 5,
    "completedAt": "2025-11-20T10:32:15Z"
  }
}
```

### Volumi di Dati

| Operazione | Dimensione Media | Throughput |
|-----------|------------------|-----------|
| Documento (raw) | 250 KB | 1200 doc/sec |
| Metadati classificazione | 2 KB | Inline |
| Analisi completa | 50 KB | 200 ana/sec |
| Risultati aggregati | 75 KB | 150 agg/sec |

---

## Gestione Errori e Fallback

### Strategie di Resilienza

```mermaid
graph TD
    A["Ricevi Documento<br/>da ZenShareUp"]

    A -->|Classificazione| B{"Riuscita?"}
    B -->|Sì| C["Procedi validazione"]
    B -->|No| D["Retry con backoff"]

    D -->|Retry 1-3| E{"Riuscita?"}
    E -->|Sì| C
    E -->|No| F["Log errore"]

    C -->|Validazione| G{"Riuscita?"}
    G -->|Sì| H["Procedi trasformazione"]
    G -->|No| I["Ritorna errore<br/>a ZenShareUp"]

    H -->|Trasformazione| J{"Riuscita?"}
    J -->|Sì| K["Aggregazione risultati"]
    J -->|No| L["Fallback: documenta<br/>come error"]

    K --> M["Ritorna a ZenShareUp<br/>arricchito"]
    I --> N["Documento rimane<br/>nello stato originale"]
    L --> N

    style A fill:#fff9c4
    style M fill:#c8e6c9
    style N fill:#ffccbc
```

### Circuit Breaker Pattern

```
Service Health: MS01 Classifier
├─ Success Rate: 99.2%
├─ Latency p95: 245ms
├─ Timeout Rate: 0.8%
└─ Circuit Status: CLOSED ✅

If:
  - Success Rate < 95% OR
  - Error Count > 100 in 1 minute OR
  - Latency p95 > 5000ms
Then:
  → OPEN circuit (reject requests)
  → Alert ops team
  → Route to fallback service
```

### Timeout e Retry

```json
{
  "classification": {
    "timeout": 5000,
    "retries": 2,
    "backoff": "exponential",
    "fallback": "manual_review_queue"
  },
  "validation": {
    "timeout": 10000,
    "retries": 1,
    "backoff": "linear",
    "fallback": "return_error"
  },
  "transformation": {
    "timeout": 15000,
    "retries": 3,
    "backoff": "exponential",
    "fallback": "keep_original_format"
  }
}
```

---

## Performance e SLA

### Service Level Agreement (SLA)

```mermaid
graph LR
    A["Latenza<br/>< 500ms"] ---|p95| B["99.95%<br/>Uptime"]
    C["Throughput<br/>1200 doc/sec"] ---|Sustained| D["99.9%<br/>Availability"]
    E["End-to-End<br/>Processing"] ---|Avg 4 sec| F["95th percentile<br/>< 10 sec"]

    style A fill:#c8e6c9
    style B fill:#c8e6c9
    style C fill:#c8e6c9
    style D fill:#c8e6c9
    style E fill:#c8e6c9
    style F fill:#c8e6c9
```

### Metriche per Microservizio

| Microservizio | Latenza p95 | Throughput | Availability | SLA |
|---------------|-------------|-----------|--------------|-----|
| MS01 Classifier | 245ms | 1200/sec | 99.97% | ✅ |
| MS02 Analyzer | 1250ms | 200/sec | 99.95% | ✅ |
| MS03 Orchestrator | 100ms | 2000/sec | 99.99% | ✅ |
| MS04 Validator | 530ms | 800/sec | 99.96% | ✅ |
| MS05 Transformer | 875ms | 500/sec | 99.94% | ✅ |
| MS06 Aggregator | 250ms | 1500/sec | 99.97% | ✅ |
| MS07 Distributor | 150ms | 2000/sec | 99.98% | ✅ |

### Monitoraggio e Alerting

**Metriche chiave monitorate:**
- 📊 Request latency distribution (p50, p95, p99)
- 📊 Error rate per service (% of failed requests)
- 📊 Queue depth (pending documents in processing)
- 📊 Resource utilization (CPU, Memory, Network)
- 📊 Cache hit ratio (% of cached responses)
- 📊 End-to-end processing time per document

**Alert triggers:**
```yaml
Alerts:
  - name: HighErrorRate
    condition: error_rate > 5%
    duration: 5m
    severity: CRITICAL

  - name: HighLatency
    condition: latency_p95 > 2000ms
    duration: 10m
    severity: WARNING

  - name: QueueBacklog
    condition: queue_depth > 10000
    duration: 5m
    severity: WARNING

  - name: ServiceDown
    condition: health_check_failed
    duration: 1m
    severity: CRITICAL
```

---

## Conclusioni

L'integrazione ZenShareUp ↔ ZenIA crea un ecosistema documentale completo:

1. **ZenShareUp** fornisce il **repository centralizzato** e la **gestione del ciclo di vita**
2. **ZenIA** fornisce l'**intelligenza artificiale** per l'elaborazione automatica
3. **Infrastruttura condivisa** garantisce **sicurezza, performance e scalabilità**

Questa architettura consente:
- ✅ Elaborazione automatica dei documenti
- ✅ Classificazione intelligente con ML
- ✅ Validazione e trasformazione standardizzate
- ✅ Arricchimento semantico dei dati
- ✅ Compliance garantito (CAD, GDPR, eIDAS)
- ✅ Performance enterprise (99.95% SLA)

L'aggiornamento graduale della documentazione permetterà di evidenziare ulteriormente questi collegamenti e facilitare l'adozione congiunta delle due piattaforme.

---

**Documento generato**: 20 novembre 2025
**Versione**: 1.0 - DEFINITIVA
**Prossimo aggiornamento**: Quando nuovi microservizi saranno integrati
