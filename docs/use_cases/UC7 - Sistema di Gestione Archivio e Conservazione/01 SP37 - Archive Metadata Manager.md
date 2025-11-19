# SP37 - Archive Metadata Manager

## Descrizione Componente

Il **SP37 Archive Metadata Manager** è il gestore centralizzato di metadati per il sistema di conservazione digitale. Implementa la gestione completa del ciclo di vita dei metadati, incluso tracking, validazione, evoluzione e conformità normativa secondo gli standard CAD/eIDAS.

## Responsabilità

- **Metadata Extraction**: Estrazione automatica e manuale di metadati da documenti
- **Metadata Validation**: Validazione conformità a schemi standard (Dublin Core, MIAOU, XAdES)
- **Lifecycle Management**: Gestione dell'evoluzione metadati nel tempo
- **Audit Trail**: Tracciamento completo modifiche metadati
- **Compliance Reporting**: Verificazione conformità normativa
- **Search Indexing**: Indicizzazione per ricerca semantica

## Architettura Interna

```
┌─────────────────────────────────────────────────────────────┐
│               METADATA MANAGEMENT LAYER                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Extraction Engine    Validation Engine    Schema Mgr    ││
│  │ ┌──────────────────┐  ┌──────────────────┐ ┌──────────┐││
│  │ │ - Auto Extract   │  │ - Dublin Core    │ │ - Evolv. ││
│  │ │ - Manual Input   │  │ - MIAOU          │ │ - Version││
│  │ │ - ML Inference   │  │ - XAdES          │ │ - Archiv.││
│  │ │ - OCR Metadata   │  │ - Custom         │ │ - Rollbk.││
│  │ └──────────────────┘  └──────────────────┘ └──────────┘││
└─────────────────────────────────────────────────────────────┘
│               ANALYSIS & GOVERNANCE LAYER                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Compliance Checker   Audit Trail Manager   Indexing    ││
│  │ ┌──────────────────┐  ┌──────────────────┐ ┌──────────┐││
│  │ │ - CAD Check      │  │ - Change Track   │ │ - Sematic││
│  │ │ - eIDAS Check    │  │ - Immutable Log  │ │ - Full  ││
│  │ │ - AgID Check     │  │ - Event Stream   │ │ - Real   ││
│  │ │ - Custom Rules   │  │ - Versioning     │ │ - Algol. ││
│  │ └──────────────────┘  └──────────────────┘ └──────────┘││
└─────────────────────────────────────────────────────────────┘
│                    DATA LAYER                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  PostgreSQL         Elasticsearch         Redis         ││
│  │  ┌──────────────┐   ┌──────────────────┐  ┌──────────┐ ││
│  │  │ - Meta Store │   │ - Full Text      │  │ - Cache  │ ││
│  │  │ - History    │   │ - Semantic Index │  │ - Session│ ││
│  │  │ - Audit      │   │ - Faceted Search │  │ - Queue  │ ││
│  │  └──────────────┘   └──────────────────┘  └──────────┘ ││
└─────────────────────────────────────────────────────────────┘
```

## Input/Output

### Input
- **Documents**: Documenti da UC1/UC5 con payload iniziale
- **Metadata Schemas**: Definizioni standard (Dublin Core, MIAOU)
- **Validation Rules**: Regole conformità CAD/eIDAS/AgID
- **Custom Fields**: Metadati personalizzati da business logic

### Output
- **Extracted Metadata**: Metadati strutturati in JSON/XML
- **Validation Results**: Report conformità
- **Audit Trail**: Traccia immutabile di modifiche
- **Search Index**: Documenti indicizzati per ricerca
- **Compliance Report**: Certificato conformità

## Dipendenze

### Upstream
```
SP36 (Archive Storage) → SP37
  Data: Stored documents, storage location, retention info
  Timing: Event-driven (on archive write)
  SLA: Metadata extraction < 5 sec per document
```

### Downstream
```
SP37 → SP10 (Dashboard)
  Data: Metadata for visualization, search results
  Timing: Real-time query response
  SLA: Search latency < 1 sec

SP37 → Compliance Reports
  Data: Validation results, audit trails
  Timing: Daily/on-demand
  SLA: Report generation < 30 sec
```

## Stack Tecnologico

| Componente | Tecnologia | Versione | Scopo |
|------------|-----------|----------|-------|
| Language | Python | 3.11 | Core implementation |
| API | FastAPI | 0.104+ | REST endpoints |
| Database | PostgreSQL | 15+ | Metadata storage + audit |
| Search | Elasticsearch | 8.10+ | Full-text indexing |
| Cache | Redis | 7.2+ | Session, caching |
| Validation | jsonschema | 4.20+ | Schema validation |
| ORM | SQLAlchemy | 2.0+ | Database ORM |
| Async | asyncio/ASGI | Latest | High concurrency |

## API Endpoints

**POST /api/v1/metadata/extract**

Request:
```json
{
  "document_id": "doc_123",
  "content": "base64_document_content",
  "schema": "dublin_core",
  "auto_extract": true
}
```

Response:
```json
{
  "document_id": "doc_123",
  "metadata": {
    "title": "...",
    "creator": "...",
    "subject": "...",
    "description": "...",
    "publisher": "...",
    "date_created": "2025-11-17T...",
    "format": "application/pdf",
    "language": "it",
    "rights": "..."
  },
  "extraction_confidence": 0.95,
  "schema_version": "1.2"
}
```

**POST /api/v1/metadata/validate**

Request:
```json
{
  "document_id": "doc_123",
  "metadata": {},
  "schemas": ["dublin_core", "miaou", "cad"]
}
```

Response:
```json
{
  "valid": true,
  "compliance": {
    "dublin_core": "compliant",
    "miaou": "compliant",
    "cad": "compliant",
    "eidas": "compliant"
  },
  "warnings": [],
  "timestamp": "2025-11-17T..."
}
```

**GET /api/v1/metadata/search**
```
?q=<query>&schema=<schema>&limit=50

Response:
{
  "results": [...],
  "total": 1234,
  "facets": {
    "creator": {...},
    "subject": {...},
    "date_range": {...}
  }
}
```

## Database Schema

```sql
CREATE TABLE metadata_records (
  id SERIAL PRIMARY KEY,
  document_id VARCHAR(255) UNIQUE,
  schema_type VARCHAR(50),  -- dublin_core, miaou, custom
  schema_version VARCHAR(10),
  metadata JSONB,
  extracted_at TIMESTAMPTZ,
  extraction_confidence DECIMAL(3,2),
  last_modified_at TIMESTAMPTZ,
  modified_by VARCHAR(255),
  audit_trail JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  INDEX idx_document_id (document_id),
  INDEX idx_schema_type (schema_type),
  INDEX idx_created_at (created_at DESC)
);

CREATE TABLE metadata_audit_log (
  id SERIAL PRIMARY KEY,
  document_id VARCHAR(255),
  old_metadata JSONB,
  new_metadata JSONB,
  change_description TEXT,
  changed_by VARCHAR(255),
  change_timestamp TIMESTAMPTZ DEFAULT NOW(),
  change_reason VARCHAR(255),
  INDEX idx_document_id (document_id),
  INDEX idx_timestamp (change_timestamp DESC)
);

CREATE TABLE metadata_validation_rules (
  id SERIAL PRIMARY KEY,
  schema_type VARCHAR(50),
  rule_name VARCHAR(255),
  rule_json JSONB,
  compliance_level VARCHAR(20),  -- mandatory, recommended, optional
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(schema_type, rule_name)
);
```

## Configurazione (YAML)

```yaml
sp37:
  extraction:
    auto_extract: true
    ml_model: "distilbert-base-multilingual"
    confidence_threshold: 0.80
    language_detection: true

  schemas:
    supported:
      - dublin_core:
          version: "1.1"
          required_fields: [title, creator, subject]
      - miaou:
          version: "2.0"
          required_fields: [doctype, responsabile]
      - cad:
          version: "3.0"
          compliance_level: "mandatory"

  validation:
    check_mandatory_fields: true
    check_compliance: true
    enforce_standards: [cad, eidas, agid]

  search:
    engine: "elasticsearch"
    index_strategy: "full_text + semantic"
    language_analyzers: ["italian", "english"]

  audit:
    track_changes: true
    immutable_log: true
    retention_days: 3650
    event_stream: "kafka"
```

## Performance & KPIs

| Metrica | Target |
|---------|--------|
| **Extraction Latency** | < 5 sec per document |
| **Validation Latency** | < 2 sec per document |
| **Search Latency (p50)** | < 500ms |
| **Search Latency (p99)** | < 2 sec |
| **Indexing Throughput** | 1000 docs/min |
| **Validation Accuracy** | > 95% |
| **Audit Trail Completeness** | 100% |

## Security & Compliance

- **Data Protection**: Encrypted at-rest (AES-256) and in-transit (TLS 1.3)
- **Access Control**: RBAC with audit logging
- **Audit Trail**: Immutable, tamper-proof, complete event log
- **Compliance**: CAD, eIDAS, AgID, GDPR ready
- **Retention**: Configurable retention policies per document type

## Testing Strategy

- **Unit**: Metadata extraction, validation functions (> 85% coverage)
- **Integration**: Full extraction → validation → indexing pipeline
- **E2E**: Complete metadata lifecycle (document → extract → validate → search)
- **Performance**: Load testing with 10,000+ concurrent documents
- **Compliance**: Validation against CAD, eIDAS, AgID rules

## Implementazione Timeline

1. **Phase 1**: Core extraction (ML-based + manual)
2. **Phase 2**: Validation engines (Dublin Core, MIAOU, CAD)
3. **Phase 3**: Audit trail & compliance reporting
4. **Phase 4**: Elasticsearch indexing & semantic search

---

**Associato a**: UC7 - Conservazione Digitale
**MS Primario**: MS06 Generic Knowledge Base
**MS Supporto**: MS04 Validator Engine, MS14 Audit Engine
**Status**: In Design
**Created**: 2025-11-17
