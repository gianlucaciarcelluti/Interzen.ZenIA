# Sequence Diagram - Document Processing Completo (UC1)

## Flusso Completo di Processamento Documenti

Questo diagramma mostra l'intero flusso di processamento di un documento nel Sistema di Gestione Documentale, dall'upload alla ricerca abilitata.

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant API as API Gateway
    participant SP15 as SP15 Orchestrator
    participant SP02 as SP02 Extractor
    participant SP07 as SP07 Classifier
    participant SP13 as SP13 Summarizer
    participant SP14 as SP14 Indexer
    participant SP12 as SP12 Search Engine
    participant SP10 as SP10 Dashboard
    participant SP11 as SP11 Security
    participant DB as PostgreSQL
    participant ES as Elasticsearch
    participant CACHE as Redis Cache
    participant STORAGE as MinIO Storage

    Note over User,STORAGE: Flusso Completo Document Processing

    User->>API: POST /api/v1/documents/upload<br/>(file + metadata)
    API->>SP11: Authenticate & Authorize
    SP11-->>API: OK

    API->>SP15: Start Workflow<br/>{document_id, pipeline: "full"}
    SP15->>DB: Create workflow record
    SP15->>SP10: Update dashboard<br/>status: "STARTED"

    SP15->>SP02: Extract Document<br/>{document_id, file_path}
    SP02->>STORAGE: Retrieve document
    STORAGE-->>SP02: Document binary
    SP02->>SP02: OCR Processing<br/>(if needed)
    SP02->>SP02: Text extraction<br/>PDF/Word parsing
    SP02->>SP02: Entity extraction<br/>NER + regex
    SP02->>DB: Store extracted metadata
    SP02->>CACHE: Cache extraction results
    SP02-->>SP15: Extraction complete<br/>{text, metadata, confidence}

    SP15->>SP07: Classify Document<br/>{text, metadata}
    SP07->>CACHE: Check classification cache
    CACHE-->>SP07: Cache miss
    SP07->>SP07: DistilBERT inference
    SP07->>DB: Get similar documents
    DB-->>SP07: Historical classifications
    SP07->>SP07: Entity recognition
    SP07->>CACHE: Store classification<br/>(TTL: 1h)
    SP07->>DB: Update document classification
    SP07-->>SP15: Classification complete<br/>{type, category, entities}

    SP15->>SP13: Generate Summary<br/>{text, classification}
    SP13->>CACHE: Check summary cache
    CACHE-->>SP13: Cache miss
    SP13->>SP13: Extractive summarization
    SP13->>SP13: Abstractive refinement
    SP13->>SP13: Template formatting
    SP13->>CACHE: Store summary<br/>(TTL: 24h)
    SP13->>DB: Store summary
    SP13-->>SP15: Summary complete<br/>{summary, key_points}

    SP15->>SP14: Index Document<br/>{text, metadata, classification, summary}
    SP14->>ES: Create document index
    ES-->>SP14: Index created
    SP14->>ES: Index full-text content
    SP14->>ES: Index metadata fields
    SP14->>ES: Index semantic vectors
    SP14->>DB: Update index status
    SP14-->>SP15: Indexing complete

    SP15->>SP12: Enable Search<br/>{document_id}
    SP12->>ES: Verify index availability
    ES-->>SP12: Index ready
    SP12->>CACHE: Update search cache
    SP12-->>SP15: Search enabled

    SP15->>SP10: Update dashboard<br/>status: "COMPLETED"
    SP10->>SP10: Calculate metrics
    SP10->>DB: Store performance data

    SP15->>SP11: Log audit trail
    SP11->>DB: Store security events

    SP15-->>API: Workflow complete<br/>{status: "success", document_id}
    API-->>User: 201 Created<br/>{document_url, search_enabled: true}

    Note over SP02,SP12: Processing Time: ~15-45 seconds<br/>Human Review: Optional for low confidence
```

## Dettagli del Flusso

### Fase 1: Upload e Autenticazione
- **API Gateway**: Riceve upload, valida autenticazione
- **SP11 Security**: Verifica permessi utente
- **SP15 Orchestrator**: Inizializza workflow nel DB

### Fase 2: Estrazione Contenuto
- **SP02 Extractor**: OCR + parsing testo
- **Entity Recognition**: Estrae metadati strutturati
- **Caching**: Risultati temporaneamente in Redis

### Fase 3: Classificazione
- **SP07 Classifier**: AI per tipo/categoria documento
- **Similarity Search**: Confronta con documenti storici
- **Confidence Scoring**: Valuta affidabilità classificazione

### Fase 4: Riassunto
- **SP13 Summarizer**: Genera abstract e punti chiave
- **Template-based**: Formattazione per tipo documento
- **Quality Check**: Valutazione leggibilità

### Fase 5: Indicizzazione
- **SP14 Indexer**: Crea indici Elasticsearch
- **Full-text**: Ricerca tradizionale
- **Semantic**: Vettori per ricerca AI
- **Metadata**: Campi strutturati

### Fase 6: Abilitazione Ricerca
- **SP12 Search**: Verifica disponibilità indici
- **Cache Warming**: Prepara risultati frequenti

### Fase 7: Completamento
- **SP10 Dashboard**: Aggiorna UI e metriche
- **SP11 Audit**: Traccia operazioni per compliance
- **Notifica**: Utente riceve conferma processamento

## Metriche di Performance

| Fase | Tempo Medio | SLA | Note |
|------|-------------|-----|------|
| Upload | <2s | 95% <5s | Include autenticazione |
| Estrazione | 3-8s | 95% <15s | Dipende da dimensione/complessità |
| Classificazione | 0.4-1s | 95% <2s | Cache hit: <0.1s |
| Riassunto | 2-5s | 95% <10s | LLM inference time |
| Indicizzazione | 1-3s | 95% <5s | Elasticsearch bulk |
| Totale | 15-45s | 95% <60s | End-to-end |

## Error Handling

### Error Scenarios
- **OCR Failure**: Fallback a text extraction manuale
- **Classification Low Confidence**: Flag per review umana
- **Indexing Timeout**: Retry con backoff
- **Storage Unavailable**: Queue per retry

### Recovery Mechanisms
- **Circuit Breaker**: Isolamento failure tra componenti
- **Dead Letter Queue**: Documenti falliti per analisi
- **Manual Override**: Possibilità intervento operatore

## Integration Points

### External Systems
- **Identity Provider**: Autenticazione utenti
- **File Storage**: MinIO/S3 per documenti
- **Search Frontend**: UI per query utente
- **Monitoring**: Prometheus per alerting

### Internal APIs
- **Workflow API**: Gestione stato processamento
- **Search API**: Query semantiche
- **Admin API**: Configurazione e manutenzione</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC1 - Sistema di Gestione Documentale/01 Sequence - Document Processing Completo.md