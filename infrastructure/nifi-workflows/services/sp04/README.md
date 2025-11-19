# SP04 - Classifier Service

Servizio di classificazione multi-dimensionale per documenti amministrativi.

## 🚀 Quick Start

### Build & Run
```bash
cd infrastructure/nifi-workflows

# Build (usando il build context)
docker build -f services/sp04/Dockerfile -t sp04-classifier ../..

# Run
docker run -p 5004:5004 sp04-classifier
```

### Accesso API
- **Base URL**: http://localhost:5004
- **Documentazione Swagger**: http://localhost:5004/docs
- **Documentazione ReDoc**: http://localhost:5004/redoc
- **Health Check**: http://localhost:5004/health

## 📡 Endpoints Disponibili

### GET /
Info sul servizio

### GET /health
Health check del servizio

### POST /api/v1/classify
Classifica un documento su più dimensioni

**Request Body**:
```json
{
  "testo": "Richiesta di autorizzazione scarico acque reflue industriali"
}
```

**Response**:
```json
{
  "status": "success",
  "testo": "Richiesta di autorizzazione...",
  "risultati": [
    {
      "dimensione": "Tipologia Documento",
      "categoria_predetta": "Autorizzazione",
      "categoria_id": 1,
      "probabilita": 0.85,
      "tutte_probabilita": [...]
    }
  ],
  "metadata": {
    "model_version": "1.0.0",
    "processing_time_ms": 150
  }
}
```

### POST /api/v1/classify-batch
Classifica multipli documenti in batch

### GET /api/v1/model-info
Informazioni sul modello di classificazione

### GET /api/v1/categories
Lista tutte le categorie disponibili

## 🔧 Configurazione

### Variabili d'Ambiente
- `PORT`: Porta del servizio (default: 5004)
- `HOST`: Host di binding (default: 0.0.0.0)

## 📊 Struttura

```
services/sp04/
├── Dockerfile          # Configurazione Docker
├── app.py             # FastAPI application
├── requirements.txt   # Dipendenze Python
├── main.py           # Entry point alternativo (deprecated)
└── README.md         # Questa documentazione
```

## 🔄 Versioni

### Versione Attuale (Allineata)
- ✅ Stessa struttura degli altri servizi
- ✅ FastAPI standalone app
- ✅ Build context semplificato
- ✅ Dipendenze minimali di base

### Versione Completa (Opzionale)
Per abilitare la versione completa con ML:
1. Decommenta le dipendenze in `requirements.txt`
2. Decommenta la copia di `src/SP04/` nel Dockerfile
3. Modifica `app.py` per importare il classificatore reale

## 🎯 Implementazione

### Stato Attuale
- ✅ API REST completa
- ✅ Swagger UI documentazione
- ✅ Endpoints funzionanti
- 🟡 Classificatore con dati mock

### Per Implementazione Completa
1. Decommenta dipendenze ML in `requirements.txt`
2. Implementa logica in `app.py` usando `src/SP04/classifier/`
3. Aggiungi training del modello
4. Configura database per persistenza

## 📝 Note

Questo servizio è ora allineato con la struttura degli altri servizi placeholder (SP01, SP02, SP03, SP05, SP08) ma mantiene funzionalità più avanzate.