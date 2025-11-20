# Matrice Dipendenze Sottoprogetti - UC1 Sistema di Gestione Documentale

## Overview Dipendenze

Questa matrice mostra le interdipendenze tra i sottoprogetti del Sistema di Gestione Documentale, identificando relazioni di dipendenza, flusso dati e punti di integrazione.

```mermaid
graph TD
    subgraph "Input Layer"
        SP15[SP15<br/>Orchestrator<br/>Entry Point]
    end

    subgraph "Processing Layer"
        SP02[SP02<br/>Document<br/>Extractor]
        SP07[SP07<br/>Content<br/>Classifier]
        SP13[SP13<br/>Document<br/>Summarizer]
    end

    subgraph "Storage Layer"
        SP14[SP14<br/>Metadata<br/>Indexer]
        SP12[SP12<br/>Semantic<br/>Search]
    end

    subgraph "Output Layer"
        SP10[SP10<br/>Dashboard]
        SP11[SP11<br/>Security<br/>& Audit]
    end

    SP15 --> SP02
    SP15 --> SP07
    SP15 --> SP13
    SP15 --> SP14
    SP15 --> SP12
    SP15 --> SP10
    SP15 --> SP11

    SP02 --> SP07
    SP02 --> SP14

    SP07 --> SP13
    SP07 --> SP14
    SP07 --> SP12

    SP13 --> SP14
    SP13 --> SP12

    SP14 --> SP12

    SP02 -.-> SP11
    SP07 -.-> SP11
    SP13 -.-> SP11
    SP14 -.-> SP11
    SP12 -.-> SP11

    style SP15 fill:#ffd700
```

## Matrice Dipendenze Dettagliata

| Sottoprogetto | Dipendenze In | Dipendenze Out | Tipo Dipendenza | Dati Scambiati |
|---------------|---------------|----------------|-----------------|----------------|
| **SP15** Document Workflow Orchestrator | - | SP02, SP07, SP13, SP14, SP12, SP10, SP11 | Orchestrazione | Workflow commands, status updates |
| **SP02** Document Extractor | SP15 | SP07, SP14, SP11 | Processing | Extracted text, metadata, OCR results |
| **SP07** Content Classifier | SP15, SP02 | SP13, SP14, SP12, SP11 | Classification | Document type, category, entities |
| **SP13** Document Summarizer | SP15, SP07 | SP14, SP12, SP11 | Summarization | Summaries, key points, structured data |
| **SP14** Metadata Indexer | SP15, SP02, SP07, SP13 | SP12, SP11 | Indexing | Indexed documents, search indices |
| **SP12** Semantic Search & Q&A | SP15, SP07, SP13, SP14 | SP10, SP11 | Search | Search results, Q&A responses |
| **SP10** Dashboard | SP15, SP12 | - | Presentation | UI data, metrics, visualizations |
| **SP11** Security & Audit | SP15, SP02, SP07, SP13, SP14, SP12 | - | Security | Audit logs, security events |

## Pipeline Operative

### Pipeline Principale: Document Processing

```mermaid
sequenceDiagram
    participant User
    participant SP15 as SP15 Orchestrator
    participant SP02 as SP02 Extractor
    participant SP07 as SP07 Classifier
    participant SP13 as SP13 Summarizer
    participant SP14 as SP14 Indexer
    participant SP12 as SP12 Search
    participant SP10 as SP10 Dashboard

    User->>SP15: Upload Document
    SP15->>SP02: Extract Content
    SP02-->>SP15: Text + Metadata
    SP15->>SP07: Classify Document
    SP07-->>SP15: Classification
    SP15->>SP13: Generate Summary
    SP13-->>SP15: Summary
    SP15->>SP14: Index Document
    SP14-->>SP15: Index Confirmation
    SP15->>SP12: Enable Search
    SP12-->>SP15: Search Ready
    SP15->>SP10: Update Dashboard
    SP10-->>User: Document Processed
```

### Pipeline Secondaria: Search Query

```mermaid
sequenceDiagram
    participant User
    participant SP10 as SP10 Dashboard
    participant SP12 as SP12 Search
    participant SP14 as SP14 Indexer

    User->>SP10: Search Query
    SP10->>SP12: Semantic Search
    SP12->>SP14: Query Index
    SP14-->>SP12: Results
    SP12-->>SP10: Formatted Results
    SP10-->>User: Search Results
```

## Punti di Integrazione

### API Endpoints

| Endpoint | Metodo | Produttore | Consumatore | Scopo |
|----------|--------|------------|-------------|-------|
| `/api/v1/documents/upload` | POST | SP15 | External | Upload documento |
| `/api/v1/documents/extract` | POST | SP02 | SP15 | Estrazione contenuto |
| `/api/v1/documents/classify` | POST | SP07 | SP15 | Classificazione |
| `/api/v1/documents/summarize` | POST | SP13 | SP15 | Riassunto |
| `/api/v1/documents/index` | POST | SP14 | SP15 | Indicizzazione |
| `/api/v1/search/semantic` | POST | SP12 | SP10 | Ricerca semantica |
| `/api/v1/dashboard/metrics` | GET | SP10 | External | Metriche |

### Event Stream

| Event | Produttore | Consumatore | Trigger |
|-------|------------|-------------|---------|
| `document.uploaded` | SP15 | SP02 | Upload completato |
| `document.extracted` | SP02 | SP07, SP14 | Estrazione completata |
| `document.classified` | SP07 | SP13, SP14 | Classificazione completata |
| `document.summarized` | SP13 | SP14 | Riassunto completato |
| `document.indexed` | SP14 | SP12 | Indicizzazione completata |
| `search.performed` | SP12 | SP10 | Query eseguita |

## Considerazioni Architetturali

### Accoppiamento
- **Loose Coupling**: Comunicazione via eventi/API
- **High Cohesion**: Ogni SP ha responsabilità singola
- **Fault Tolerance**: Circuit breaker per failure isolation

### Scalabilità
- **Horizontal Scaling**: SP indipendenti scalabili separatamente
- **Load Balancing**: API Gateway distribuisce load
- **Caching**: Redis per ridurre load su componenti downstream

### Monitoraggio
- **Health Checks**: Ogni SP espone endpoint health
- **Metrics**: Prometheus per performance monitoring
- **Tracing**: Distributed tracing per request flow

### Sicurezza
- **Authentication**: JWT su ogni API call
- **Authorization**: RBAC per accesso risorse
- **Encryption**: TLS per data in transit

## Testing Strategy

### Unit Testing
- Ogni SP testato isolatamente
- Mock per dipendenze esterne

### Integration Testing
- Test pipeline end-to-end
- Contract testing per API

### Performance Testing
- Load testing per scalabilità
- Stress testing per limiti

### Security Testing
- Penetration testing
- Vulnerability scanning
- Compliance auditing</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC1 - Sistema di Gestione Documentale/02 Matrice Dipendenze Sottoprogetti UC1.md
