# SP01 - EML Parser & Email Intelligence

## 📧 Descrizione

Microservizio FastAPI per l'analisi automatica di email PEC in arrivo. Estrae metadata, classifica il tipo di richiesta e prepara i dati per l'elaborazione successiva.

## 🎯 Funzionalità

- **Parsing Email**: Analisi completa di file .eml
- **Estrazione Metadata**: Mittente, destinatario, oggetto, data
- **Classificazione**: Identifica se è una richiesta amministrativa
- **Gestione Allegati**: Lista allegati con metadata
- **Riconoscimento PEC**: Identifica email PEC certificate

## 🔌 API Endpoints

### POST /parse
Parsifica email e estrae informazioni

**Request:**
```json
{
  "eml_content": "base64_encoded_eml_or_raw_content"
}
```

**Response:**
```json
{
  "metadata": {
    "from_address": "sender@example.com",
    "to_addresses": ["recipient@comune.it"],
    "subject": "Richiesta autorizzazione",
    "date": "2025-11-03T10:00:00Z"
  },
  "body_text": "Contenuto email...",
  "attachments": [
    {
      "filename": "documento.pdf",
      "content_type": "application/pdf",
      "size_bytes": 102400
    }
  ],
  "is_pec": true,
  "confidence": 0.95,
  "classification": "RICHIESTA_AMMINISTRATIVA"
}
```

### GET /health
Health check

### GET /
Informazioni servizio

## 🚀 Utilizzo

### Locale
```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 5001
```

### Docker
```bash
docker build -t sp01-eml-parser .
docker run -p 5001:5001 sp01-eml-parser
```

### Docker Compose
Già incluso in `docker-compose.yml` principale

## 📝 Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `GROQ_API_KEY`: API key per classificazione AI (opzionale)

## 🔗 Integrazione

Utilizzato da:
- **SP09 Workflow Engine** (NiFi) - Come primo step del workflow
- **SP02 Document Extractor** - Per processare allegati

## 📊 Status

✅ **Struttura creata** - Implementazione base pronta per sviluppo

## 🔧 TODO

- [ ] Implementare parsing reale con `email.parser`
- [ ] Aggiungere supporto per attachments extraction
- [ ] Implementare classificazione AI con Groq
- [ ] Aggiungere validazione PEC signature
- [ ] Implementare caching con Redis

## 📚 Documentazione

API Docs: http://localhost:5001/docs
