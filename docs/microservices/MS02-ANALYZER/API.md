# MS02 - Riferimento API Analizzatore

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)

## Indice

1. [URL Base](#url-base)
2. [Autenticazione](#autenticazione)
3. [Endpoint](#endpoint)
4. [Limitazione del Tasso](#limitazione-del-tasso)
5. [Gestione Errori](#gestione-errori)
6. [Esempi di Richiesta/Risposta](#esempi-di-richiestarisposta)

---

## URL Base
```
http://localhost:8002/api/v1
```

## Autenticazione
Tutti gli endpoint richiedono un token Bearer nell'intestazione Authorization:
```
Authorization: Bearer <jwt-token>
```

[↑ Torna al Indice](#indice)

---

## Endpoint

### 1. Analisi Semantica
**POST** `/analyze/semantic`

Esegue analisi semantica avanzata su testo.

#### Richiesta
```json
{
  "analysis_id": "semantic-2024-11-18-001",
  "content": {
    "text": "Il contratto prevede consegna entro 30 giorni dalla firma.",
    "language": "it",
    "domain": "legal"
  },
  "parameters": {
    "extract_entities": true,
    "extract_concepts": true,
    "sentiment_analysis": true
  }
}
```

#### Response (Success 200)
```json
{
  "analysis_id": "semantic-2024-11-18-001",
  "results": {
    "entities": [
      {
        "text": "contratto",
        "type": "LEGAL_DOCUMENT",
        "confidence": 0.95
      }
    ],
    "concepts": ["contratto commerciale", "termini consegna"],
    "sentiment": "neutral"
  },
  "processing_time_ms": 245
}
```

### 2. Rilevamento Anomalie
**POST** `/analyze/anomaly`

Rileva anomalie nei dati forniti.

#### Richiesta
```json
{
  "analysis_id": "anomaly-2024-11-18-001",
  "data_points": [
    {
      "timestamp": "2024-11-18T10:00:00Z",
      "features": {
        "amount": 1500.00,
        "location": "Rome"
      }
    }
  ],
  "context": {
    "baseline_period_days": 30,
    "sensitivity": "medium"
  }
}
```

#### Response (Success 200)
```json
{
  "analysis_id": "anomaly-2024-11-18-001",
  "results": {
    "is_anomaly": true,
    "score": 0.92,
    "confidence": 0.89
  },
  "processing_time_ms": 156
}
```

### 3. Analisi Predittiva
**POST** `/analyze/predictive`

Esegue previsioni basate sui dati storici.

#### Richiesta
```json
{
  "analysis_id": "predict-2024-11-18-001",
  "model_type": "time_series",
  "data": {
    "time_series": [
      {"timestamp": "2024-10-01", "value": 1200},
      {"timestamp": "2024-10-02", "value": 1350}
    ],
    "forecast_horizon": 7
  }
}
```

#### Response (Success 200)
```json
{
  "analysis_id": "predict-2024-11-18-001",
  "results": {
    "forecast": [
      {"timestamp": "2024-11-19", "value": 1420.50}
    ],
    "model_quality": {"mae": 45.23}
  },
  "processing_time_ms": 890
}
```

### 4. Stato Modelli
**GET** `/models/status`

Recupera stato dei modelli di analisi.

#### Response (Success 200)
```json
{
  "models": [
    {
      "name": "semantic-analyzer-v3.2",
      "active": true,
      "accuracy": 0.94
    }
  ],
  "cache_stats": {
    "hit_rate": 0.82,
    "size_mb": 1245
  }
}
```

### 5. Health Check
**GET** `/health`

Controllo salute del servizio.

#### Response (Success 200)
```json
{
  "status": "healthy",
  "service": "MS02-ANALYZER",
  "models_loaded": true,
  "last_analysis": "2024-11-18T10:45:30Z"
}
```

[↑ Torna al Indice](#indice)

---

## Limitazione del Tasso

### Limiti per Tenant
- 100 richieste/minuto per analisi semantica
- 200 richieste/minuto per rilevamento anomalie
- 50 richieste/minuto per analisi predittiva

### Intestazioni di Risposta
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
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
  "message": "Missing required field: content",
  "details": {
    "field": "content",
    "reason": "required"
  }
}
```

#### 422 Entità Non Elaborabile
```json
{
  "error_code": "UNSUPPORTED_FORMAT",
  "message": "Analysis type not supported",
  "supported_types": ["semantic", "anomaly", "predictive"]
}
```

[↑ Torna al Indice](#indice)

---

## Esempi di Richiesta/Risposta

Vedi la cartella [examples/](../examples/) per campioni dettagliati.

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)
