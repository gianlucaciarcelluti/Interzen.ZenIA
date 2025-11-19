# SP02 - Document Extractor & Attachment Classifier

## 📎 Descrizione

Microservizio FastAPI per l'estrazione automatica di testo da documenti allegati e classificazione intelligente. Supporta PDF, immagini (con OCR), DOC/DOCX.

## 🎯 Funzionalità

- **Estrazione Testo**: Da PDF, DOC, immagini con OCR Tesseract
- **Classificazione Documenti**: Identifica tipo documento (planimetria, relazione, ecc.)
- **Estrazione Dati Strutturati**: Date, importi, nomi, codici, riferimenti normativi
- **OCR Multilingua**: Italiano + altre lingue con Tesseract
- **Storage Integration**: Salvataggio automatico su MinIO

## 🔌 API Endpoints

### POST /extract
Estrae testo completo e metadata da documento

**Request:**
```bash
curl -X POST "http://localhost:5002/extract" \
  -F "file=@documento.pdf"
```

**Response:**
```json
{
  "filename": "planimetria.pdf",
  "content_type": "application/pdf",
  "text_content": "Testo estratto...",
  "classification": {
    "document_type": "PLANIMETRIA_TECNICA",
    "confidence": 0.88,
    "category": "TECNICO"
  },
  "extracted_data": {
    "dates": ["2025-11-03"],
    "amounts": [150000.00],
    "names": ["Ing. Mario Rossi"],
    "codes": ["CIG123456"],
    "references": ["L. 241/1990"]
  },
  "page_count": 5,
  "word_count": 1234,
  "ocr_applied": false
}
```

### POST /classify
Classificazione rapida senza estrazione completa

### GET /health
Health check

### GET /
Informazioni servizio

## 📦 Formati Supportati

- **PDF**: Nativi e scansionati (con OCR)
- **Immagini**: JPG, PNG, TIFF (con OCR)
- **Documenti Office**: DOC, DOCX

## 🚀 Utilizzo

### Locale
```bash
# Install Tesseract OCR first
sudo apt-get install tesseract-ocr tesseract-ocr-ita

pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 5002
```

### Docker
```bash
docker build -t sp02-document-extractor .
docker run -p 5002:5002 sp02-document-extractor
```

### Docker Compose
Già incluso in `docker-compose.yml` principale

## 📝 Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string  
- `MINIO_ENDPOINT`: MinIO storage endpoint
- `MINIO_ACCESS_KEY`: MinIO access key
- `MINIO_SECRET_KEY`: MinIO secret key
- `GROQ_API_KEY`: API key per classificazione AI

## 🔗 Integrazione

Utilizzato da:
- **SP01 EML Parser** - Processa allegati email
- **SP09 Workflow Engine** (NiFi) - Step estrazione documenti
- **SP07 Content Classifier** - Per classificazione avanzata

## 📊 Status

✅ **Struttura creata** - Implementazione base pronta per sviluppo

## 🔧 TODO

- [ ] Implementare estrazione PDF con PyPDF2/pdfplumber
- [ ] Implementare OCR con Tesseract per immagini
- [ ] Implementare estrazione DOC/DOCX con python-docx
- [ ] Aggiungere NER (Named Entity Recognition) con spaCy
- [ ] Implementare integrazione MinIO per storage
- [ ] Aggiungere caching risultati con Redis
- [ ] Implementare classificazione AI con Groq

## 📚 Documentazione

API Docs: http://localhost:5002/docs
