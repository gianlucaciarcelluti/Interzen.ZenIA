# SP07 - Content Classifier: Sequence Diagram (Adattato per UC1)

## Classificazione e Analisi Contesto Documentale

Questo diagramma mostra tutte le interazioni del **Content Classifier (SP07)** nel processo di classificazione dei documenti nel Sistema di Gestione Documentale.

```mermaid
sequenceDiagram
    autonumber
    participant WF as SP15 Document Workflow Orchestrator
    participant CLS as SP07 Content Classifier
    participant CACHE as Redis Cache
    participant DB as PostgreSQL
    participant STORAGE as MinIO Storage
    participant NIFI_PROV as NiFi Provenance (Data Lineage)
    participant DASH as SP10 Dashboard
    
    Note over WF,DASH: Fase 2: Classificazione Documenti
    
    WF->>CLS: POST /classify<br/>{document_text, metadata}
    
    CLS->>CACHE: Check cached classification
    
    alt Cache Miss
        CLS->>CLS: DistilBERT inference<br/>+ NER extraction
        
        CLS->>DB: Retrieve similar documents
        
        CLS->>STORAGE: Fetch historical classifications
        
        CLS->>CACHE: Store classification result<br/>(TTL: 1h)
    end
    
    CLS-->>WF: {doc_type: "DELIBERA",<br/>category: "URBANISTICA",<br/>metadata_extracted: {...},<br/>confidence: 0.94}
    
    WF->>NIFI_PROV: Log provenance event<br/>DOCUMENT_CLASSIFIED
    
    WF->>DB: Update document<br/>status: CLASSIFIED
    
    WF->>DASH: Update dashboard<br/>{document_id, status: "CLASSIFIED",<br/>classification_data}
    
    DASH->>DASH: Store metrics<br/>Update real-time view
    
    rect rgb(200, 255, 200)
        Note over CLS: Classifier<br/>Tempo medio: 450ms<br/>SLA: 95% < 1s<br/>Cache TTL: 1 ora<br/>DistilBERT + NER
    end
```

## Payload Example: Classification Request

```json
{
  "document_id": "DOC-2025-001234",
  "text": "DELIBERA DELLA GIUNTA COMUNALE N. 123/2025 ...",
  "metadata": {
    "filename": "delibera_urbanistica.pdf",
    "upload_date": "2025-11-15T10:00:00Z",
    "user_id": "user-456"
  },
  "context": {
    "department": "Urbanistica",
    "priority": "normal"
  }
}
```

## Response Example

```json
{
  "document_id": "DOC-2025-001234",
  "classification": {
    "type": "DELIBERA",
    "category": "URBANISTICA",
    "subcategory": "PIANI_REGOLATORI",
    "confidence": 0.94
  },
  "extracted_metadata": {
    "title": "Approvazione Piano Urbanistico Zona Industriale",
    "date": "2025-11-15",
    "authority": "Giunta Comunale",
    "number": "123/2025",
    "amount": 150000.00,
    "cig": "Z1234567890"
  },
  "entities": [
    {
      "text": "Giunta Comunale",
      "label": "ORG",
      "confidence": 0.98
    },
    {
      "text": "Piano Urbanistico",
      "label": "LAW",
      "confidence": 0.92
    }
  ],
  "processing_time_ms": 450,
  "cached": false
}
```

## Error Handling

```json
{
  "error": "CLASSIFICATION_FAILED",
  "message": "Confidence too low for reliable classification",
  "confidence": 0.45,
  "suggestions": [
    "Review document manually",
    "Provide additional context",
    "Split document if too complex"
  ]
}
```

## Performance Metrics

- **Accuracy**: >90% per categorie principali
- **Precision**: >92% entità estratte
- **Recall**: >88% documenti classificati
- **Latency**: <500ms media
- **Throughput**: 120 documenti/minuto
## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

☑ CAD
☑ AI Act
☑ GDPR
☐ L. 241/1990 - Procedimento Amministrativo
☐ eIDAS - Regolamento 2014/910
☐ D.Lgs 42/2004 - Codice Beni Culturali
☐ D.Lgs 152/2006 - Codice dell'Ambiente
☐ D.Lgs 33/2013 - Decreto Trasparenza

**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
| CAD | Art. 1, Art. 21, Art. 22, Art. 62 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| AI Act | Art. 6, Art. 13, Art. 22 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| GDPR | Art. 5, Art. 32 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa" del template standard.

---


## Integration Points

- **Input**: Da SP02 (testo estratto), SP14 (metadati esistenti)
- **Output**: A SP12 (per ricerca), SP13 (per riassunto), SP14 (per indicizzazione)
- **Monitoring**: Metriche inviate a SP10 Dashboard</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC1 - Sistema di Gestione Documentale/01 SP07 - Content Classifier.md