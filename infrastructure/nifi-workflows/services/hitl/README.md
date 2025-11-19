# HITL Manager Service - Human in the Loop

Servizio dedicato alla gestione dei checkpoint di intervento umano nel workflow di generazione atti amministrativi.

## Funzionalità

- **Gestione Checkpoint**: Crea e gestisce i punti di decisione umana
- **Tracking Decisioni**: Registra tutte le decisioni degli utenti
- **Versioning Documenti**: Traccia tutte le versioni dei documenti con diff
- **Analytics**: Fornisce metriche su tempo decisionale e pattern di modifica

## Checkpoint HITL

### 1. PROCEDURAL_CLASSIFICATION
Dopo SP00 - Procedural Classifier
- Conferma/modifica tipo procedimento identificato

### 2. DOCUMENT_CLASSIFICATION  
Dopo SP04 - Classifier
- Conferma/modifica tipo documento e template

### 3. DRAFT_REVIEW
Dopo SP01 - Template Engine
- Review completo draft con possibilità di modifiche inline

### 4. FINAL_APPROVAL
Dopo SP05 - Quality Checker
- Approvazione finale prima della pubblicazione

## API Endpoints

### Create Checkpoint
```http
POST /api/v1/hitl/checkpoint/create
Content-Type: application/json

{
  "workflow_id": "WF-12345",
  "checkpoint_name": "DRAFT_REVIEW",
  "ai_suggestion": {...},
  "ai_confidence": 0.96,
  "timeout_minutes": 30
}
```

### Get Checkpoint
```http
GET /api/v1/hitl/checkpoint/{workflow_id}/{checkpoint_name}
```

### Submit Decision
```http
POST /api/v1/hitl/checkpoint/{checkpoint_id}/decision
Content-Type: application/json
X-User-ID: user_uuid

{
  "action": "MODIFIED",
  "user_changes": {...},
  "modification_reason": "Aggiornamento normativa",
  "session_id": "session-123"
}
```

### Get Modifications History
```http
GET /api/v1/hitl/workflow/{workflow_id}/modifications
```

### Get Document Versions
```http
GET /api/v1/hitl/workflow/{workflow_id}/versions
```

### Save Document Version
```http
POST /api/v1/hitl/document/version
Content-Type: application/json

{
  "workflow_id": "WF-12345",
  "content": "...",
  "created_by": "user@example.com",
  "is_ai_generated": false,
  "hitl_interaction_id": 42
}
```

## Database Schema

### hitl_interactions
Traccia ogni interazione umana con un checkpoint

### document_versions  
Versioning completo dei documenti con diff

### hitl_checkpoints
Stato dei checkpoint in attesa di decisione

## Metriche Tracciate

- Tempo medio di decisione per checkpoint
- Percentuale di conferme vs modifiche vs rifiuti
- Pattern di modifica più comuni
- Correlazione tra confidence AI e azione utente
- Percentuale contenuto AI vs umano nei documenti finali

## Build & Run

### Locale
```bash
pip install -r requirements.txt
python app.py
```

### Docker
```bash
docker build -t hitl-manager .
docker run -p 5009:5009 \
  -e POSTGRES_HOST=postgres \
  -e POSTGRES_DB=provvedimenti \
  hitl-manager
```

## Environment Variables

- `POSTGRES_HOST`: Host del database PostgreSQL (default: postgres)
- `POSTGRES_DB`: Nome database (default: provvedimenti)
- `POSTGRES_USER`: Username database (default: postgres)
- `POSTGRES_PASSWORD`: Password database (default: postgres)
- `POSTGRES_PORT`: Porta database (default: 5432)

## Integration

Il servizio si integra con:
- **SP06 - Workflow Engine**: Riceve notifiche quando creare checkpoint
- **SP08 - Security & Audit**: Audit log di tutte le decisioni
- **Frontend**: UI per visualizzare e interagire con checkpoint
- **NiFi Provenance**: Eventi tracciati per notifiche async con data lineage completo

## Testing

```bash
# Health check
curl http://localhost:5009/health

# Crea checkpoint
curl -X POST http://localhost:5009/api/v1/hitl/checkpoint/create \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "WF-TEST-001",
    "checkpoint_name": "DRAFT_REVIEW",
    "ai_suggestion": {"document": "Test..."},
    "ai_confidence": 0.95
  }'
```
