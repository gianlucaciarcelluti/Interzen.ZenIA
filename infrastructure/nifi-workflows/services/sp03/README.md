# SP03 - Procedural Classifier Service

## Descrizione

Servizio di classificazione iniziale del procedimento amministrativo a partire dall'istanza di parte (richiesta utente).

## Funzionalità

- **Classificazione procedimento**: Identifica il procedimento amministrativo applicabile
- **Determinazione provvedimento**: Individua il tipo di provvedimento da generare
- **Recupero normativa**: Fornisce la normativa di base applicabile
- **Metadata richiesti**: Specifica i metadata obbligatori e opzionali
- **Enti coinvolti**: Identifica gli enti che devono essere coinvolti nel procedimento

## Tecnologie

- **FastAPI**: Framework web
- **Pydantic**: Validazione dati
- **DistilBERT**: Classificazione semantica (in produzione)
- **spaCy**: Named Entity Recognition (in produzione)
- **PostgreSQL**: Storage procedimenti e classificazioni
- **Redis**: Cache risultati

## API Endpoints

### POST /classify-procedure

Classifica il procedimento amministrativo.

**Request:**
```json
{
  "workflow_id": "WF-12345",
  "istanza_metadata": {
    "oggetto": "Richiesta autorizzazione scarico acque reflue industriali",
    "richiedente": {
      "tipo": "PERSONA_GIURIDICA",
      "denominazione": "Industria Tessile Rossi S.p.A.",
      "partita_iva": "IT12345678901"
    },
    "descrizione_istanza": "L'azienda richiede autorizzazione...",
    "data_presentazione": "2025-10-10",
    "urgenza": "NORMALE"
  },
  "allegati_info": {
    "count": 3,
    "types": ["PLANIMETRIA", "RELAZIONE_TECNICA"],
    "total_size_mb": 4.5
  }
}
```

**Response:**
```json
{
  "classification": {
    "procedimento": {
      "codice": "PROC_AMB_001",
      "denominazione": "AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE",
      "categoria": "AMBIENTE",
      "confidence": 0.96
    },
    "tipo_provvedimento": {
      "codice": "PROV_DET_DIR",
      "denominazione": "DETERMINAZIONE_DIRIGENZIALE",
      "autorita_competente": "DIRIGENTE_SETTORE_AMBIENTE",
      "confidence": 0.94
    },
    "normativa_base": [...],
    "termini_procedimento": {...},
    "metadata_required": {...}
  },
  "processing_time_ms": 520
}
```

### GET /health

Health check del servizio.

## Build & Run

### Docker

```bash
docker build -t sp03-procedural-classifier .
docker run -p 5003:5003 sp03-procedural-classifier
```

### Local

```bash
pip install -r requirements.txt
python app.py
```

## Environment Variables

- `PORT`: Porta del servizio (default: 5003)
- `DATABASE_URL`: Connection string PostgreSQL
- `REDIS_URL`: Connection string Redis

## Integration

Questo servizio è invocato dal Workflow Engine (SP09) come primo step dopo l'autenticazione utente.

Flusso:
1. Utente invia istanza
2. SP09 chiama SP03 per classificare procedimento
3. SP03 restituisce procedimento + tipo provvedimento
4. SP09 procede con gli altri sottoprogetti usando le info da SP03
