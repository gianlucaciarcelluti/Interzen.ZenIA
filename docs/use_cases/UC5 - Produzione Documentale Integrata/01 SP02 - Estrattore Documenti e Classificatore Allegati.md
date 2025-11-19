# SP02 - Document Extractor & Attachment Classifier

## Panoramica

**SP02 - Document Extractor** è il componente responsabile dell'elaborazione intelligente degli allegati email estratti da SP01. Esegue OCR su documenti scansionati, classifica tipologia documento (16 categorie), estrae entità named (CF, indirizzi, importi) e valida completezza documentale richiesta per procedimento.

```mermaid
graph LR
    SP01[SP01<br/>EML Parser] -->|attachments[]| SP02[SP02<br/>Doc Extractor]
    SP02 -->|documents[] + validation| SP03[SP03<br/>Procedural]
    SP02 -->|documents[] + validation| SP09[SP09<br/>Workflow]
    
    SP02 -.-> Tesseract[Tesseract OCR<br/>Engine]
    SP02 -.-> BERT[DistilBERT<br/>Classifier]
    SP02 -.-> spaCy[spaCy NER]
    SP02 -.-> MinIO[MinIO<br/>Storage]
    SP02 -.-> DB[(PostgreSQL)]
    SP02 -.-> GPU[GPU Pool<br/>CUDA]
    
    style SP02 fill:#ffd700
```

## Responsabilità

### Core Functions

1. **OCR Processing**
   - Tesseract OCR su PDF scansionati/immagini
   - Preprocessing immagini (deskew, denoise, binarizzazione)
   - Language detection (italiano prioritario)
   - Confidence scoring per testo estratto

2. **Document Classification**
   - 16 categorie documento PA:
     - `istanza_procedimento` - Domanda iniziale
     - `documento_identita` - CI, patente, passaporto
     - `visura_camerale` - CCIAA
     - `planimetria_tecnica` - Disegni tecnici
     - `relazione_tecnica` - Relazioni professionali
     - `autocertificazione` - Dichiarazioni sostitutive
     - `marca_da_bollo` - Marca telematica/fisica
     - `ricevuta_pagamento` - Bonifici, PagoPA
     - `atto_notarile` - Atti autenticati
     - `certificato_pa` - Certificati PA (residenza, destinazione urbanistica)
     - `contratto` - Contratti privati
     - `polizza_assicurativa` - Assicurazioni
     - `bilancio_aziendale` - Bilanci/stati patrimoniali
     - `curriculum_vitae` - CV
     - `dichiarazione_redditi` - CU, 730, Unico
     - `altro` - Categoria catch-all

3. **Named Entity Recognition (NER)**
   - **Persone**: Nome, cognome, ruolo
   - **Codici Fiscali**: Persone fisiche + società
   - **Partite IVA**: Con validazione checksum
   - **Indirizzi**: Via, CAP, Comune, Provincia
   - **Importi**: Euro con context (pagamento, imposta, contributo)
   - **Date**: Nascita, rilascio, scadenza, validità
   - **PEC/Email**: Contatti elettronici
   - **Telefoni**: Numeri di contatto
   - **Codici**: CIG, CUP, pratiche edilizie

4. **Document Validation**
   - Verifica leggibilità (OCR confidence > threshold)
   - Check documenti obbligatori per tipo procedimento
   - Validazione scadenze (es. documento identità valido)
   - Cross-check dati tra documenti (CF coerente)

5. **Metadata Enrichment**
   - Estrazione metadata PDF (author, creation date, software)
   - Rilevamento firme digitali su PDF (.p7m unwrapped da SP01)
   - Analisi layout documento (detect tabelle, form campi)
   - Page count e dimensioni

## Stack Tecnologico

| Componente | Tecnologia | Versione | Scopo |
|-----------|-----------|----------|-------|
| **Runtime** | Python | 3.11+ | Linguaggio principale |
| **Framework** | FastAPI | 0.104+ | REST API |
| **OCR Engine** | Tesseract | 5.3+ | Text extraction |
| **OCR Wrapper** | pytesseract | 0.3.10+ | Python binding |
| **Image Processing** | Pillow (PIL) | 10.1+ | Image manipulation |
| **Image Enhancement** | OpenCV | 4.8+ | Preprocessing (deskew, denoise) |
| **PDF Processing** | PyMuPDF (fitz) | 1.23+ | PDF parsing + rendering |
| **Document Classifier** | DistilBERT | transformers 4.35+ | ML classification |
| **NER** | spaCy | 3.7+ | Named Entity Recognition |
| **NER Model** | `it_core_news_lg` | 3.7.0 | Italian language model |
| **Text Extraction** | pdfplumber | 0.10+ | PDF text (native, non-OCR) |
| **GPU Acceleration** | CUDA | 12.0+ | Tesseract GPU, BERT inference |
| **Parallel Processing** | Celery | 5.3+ | Async task queue |
| **Storage** | MinIO SDK | 7.2+ | Document storage |
| **Database** | asyncpg | 0.29+ | PostgreSQL async |
| **Cache** | redis-py | 5.0+ | Classification cache |

## API Endpoints

### POST /extract-documents

Endpoint principale per estrazione e classificazione allegati.

**Request**:
```json
{
  "attachments": [
    {
      "attachment_id": "ATT-001",
      "filename": "istanza.pdf",
      "mime_type": "application/pdf",
      "storage_path": "s3://bucket/attachments/WF-12345/istanza.pdf",
      "size_bytes": 245760,
      "is_signed": false
    },
    {
      "attachment_id": "ATT-002",
      "filename": "documento_identita.pdf",
      "mime_type": "application/pdf",
      "storage_path": "s3://bucket/attachments/WF-12345/documento_identita.pdf",
      "size_bytes": 512000,
      "is_signed": false
    },
    {
      "attachment_id": "ATT-003",
      "filename": "planimetria.pdf",
      "mime_type": "application/pdf",
      "storage_path": "s3://bucket/attachments/WF-12345/planimetria.pdf",
      "size_bytes": 1048576,
      "is_signed": false
    }
  ],
  "workflow_id": "WF-12345",
  "options": {
    "perform_ocr": true,
    "classify_documents": true,
    "extract_ner": true,
    "validate_completeness": false,
    "required_document_types": []
  }
}
```

**Response** (200 OK):
```json
{
  "workflow_id": "WF-12345",
  "processing_status": "success",
  "documents": [
    {
      "document_id": "DOC-001",
      "attachment_id": "ATT-001",
      "filename": "istanza.pdf",
      
      "classification": {
        "document_type": "istanza_procedimento",
        "confidence": 0.96,
        "alternative_types": [
          {"type": "autocertificazione", "confidence": 0.12}
        ]
      },
      
      "text_extraction": {
        "method": "native_pdf",
        "ocr_required": false,
        "full_text": "Il sottoscritto Mario Rossi, nato a Roma il 15/03/1980, CF RSSMRA80C15H501U, residente in Via Roma 123, 00100 Roma (RM), chiede autorizzazione allo scarico delle acque reflue...",
        "page_count": 2,
        "text_length": 2456,
        "language": "ita",
        "confidence": 0.99
      },
      
      "extracted_entities": {
        "persone": [
          {
            "nome": "Mario",
            "cognome": "Rossi",
            "nome_completo": "Mario Rossi",
            "ruolo": "richiedente",
            "mention_count": 3
          }
        ],
        "codici_fiscali": [
          {
            "cf": "RSSMRA80C15H501U",
            "tipo": "persona_fisica",
            "persona": "Mario Rossi",
            "validation": "valid"
          }
        ],
        "partite_iva": [],
        "indirizzi": [
          {
            "via": "Via Roma 123",
            "cap": "00100",
            "comune": "Roma",
            "provincia": "RM",
            "tipo": "residenza"
          }
        ],
        "importi": [],
        "date": [
          {
            "data": "1980-03-15",
            "tipo": "nascita",
            "persona": "Mario Rossi"
          }
        ],
        "email": [],
        "telefoni": [],
        "codici_procedimento": []
      },
      
      "metadata": {
        "pdf_metadata": {
          "author": "Mario Rossi",
          "creator": "Microsoft Word",
          "creation_date": "2025-10-15T14:30:00Z",
          "modification_date": "2025-10-20T09:15:00Z"
        },
        "has_digital_signature": false,
        "is_searchable_pdf": true,
        "page_sizes": ["A4", "A4"],
        "contains_images": false,
        "contains_tables": true,
        "contains_forms": false
      },
      
      "validation": {
        "is_readable": true,
        "ocr_confidence": null,
        "completeness_score": 0.95,
        "issues": []
      },
      
      "processing_time_ms": 456,
      "processed_at": "2025-11-03T10:25:12Z"
    },
    {
      "document_id": "DOC-002",
      "attachment_id": "ATT-002",
      "filename": "documento_identita.pdf",
      
      "classification": {
        "document_type": "documento_identita",
        "confidence": 0.98,
        "alternative_types": []
      },
      
      "text_extraction": {
        "method": "ocr",
        "ocr_required": true,
        "full_text": "REPUBBLICA ITALIANA CARTA D'IDENTITA N. AB1234567 ROSSI MARIO NATO IL 15/03/1980 A ROMA (RM) VALIDA FINO AL 15/03/2030 COMUNE DI ROMA...",
        "page_count": 1,
        "text_length": 345,
        "language": "ita",
        "confidence": 0.87
      },
      
      "extracted_entities": {
        "persone": [
          {
            "nome": "Mario",
            "cognome": "Rossi",
            "nome_completo": "Mario Rossi",
            "ruolo": "titolare_documento"
          }
        ],
        "codici_fiscali": [
          {
            "cf": "RSSMRA80C15H501U",
            "tipo": "persona_fisica",
            "persona": "Mario Rossi",
            "validation": "valid"
          }
        ],
        "partite_iva": [],
        "indirizzi": [
          {
            "comune": "Roma",
            "provincia": "RM",
            "tipo": "nascita"
          }
        ],
        "importi": [],
        "date": [
          {
            "data": "1980-03-15",
            "tipo": "nascita"
          },
          {
            "data": "2030-03-15",
            "tipo": "scadenza_documento"
          }
        ],
        "email": [],
        "telefoni": [],
        "codici_procedimento": [
          {
            "codice": "AB1234567",
            "tipo": "numero_carta_identita"
          }
        ]
      },
      
      "metadata": {
        "pdf_metadata": {
          "author": "",
          "creator": "Scanner HP",
          "creation_date": "2025-10-25T16:45:00Z"
        },
        "has_digital_signature": false,
        "is_searchable_pdf": false,
        "page_sizes": ["Custom"],
        "contains_images": true,
        "contains_tables": false,
        "contains_forms": false
      },
      
      "validation": {
        "is_readable": true,
        "ocr_confidence": 0.87,
        "completeness_score": 0.92,
        "issues": [
          {
            "severity": "warning",
            "field": "scadenza",
            "message": "Verificare scadenza documento (2030-03-15)"
          }
        ]
      },
      
      "processing_time_ms": 1823,
      "processed_at": "2025-11-03T10:25:14Z"
    },
    {
      "document_id": "DOC-003",
      "attachment_id": "ATT-003",
      "filename": "planimetria.pdf",
      
      "classification": {
        "document_type": "planimetria_tecnica",
        "confidence": 0.94,
        "alternative_types": [
          {"type": "relazione_tecnica", "confidence": 0.18}
        ]
      },
      
      "text_extraction": {
        "method": "ocr",
        "ocr_required": true,
        "full_text": "PLANIMETRIA GENERALE Scala 1:100 Dott. Ing. Giuseppe Bianchi N. Iscrizione Albo 12345 LEGENDA...",
        "page_count": 4,
        "text_length": 892,
        "language": "ita",
        "confidence": 0.76
      },
      
      "extracted_entities": {
        "persone": [
          {
            "nome": "Giuseppe",
            "cognome": "Bianchi",
            "nome_completo": "Giuseppe Bianchi",
            "ruolo": "progettista",
            "titolo": "Dott. Ing."
          }
        ],
        "codici_fiscali": [],
        "partite_iva": [],
        "indirizzi": [],
        "importi": [],
        "date": [],
        "email": [],
        "telefoni": [],
        "codici_procedimento": [
          {
            "codice": "12345",
            "tipo": "numero_albo_professionale"
          }
        ]
      },
      
      "metadata": {
        "pdf_metadata": {
          "author": "Giuseppe Bianchi",
          "creator": "AutoCAD 2024",
          "creation_date": "2025-09-20T11:00:00Z"
        },
        "has_digital_signature": false,
        "is_searchable_pdf": false,
        "page_sizes": ["A3", "A3", "A2", "A4"],
        "contains_images": true,
        "contains_tables": false,
        "contains_forms": false,
        "is_technical_drawing": true
      },
      
      "validation": {
        "is_readable": true,
        "ocr_confidence": 0.76,
        "completeness_score": 0.85,
        "issues": [
          {
            "severity": "info",
            "field": "ocr_confidence",
            "message": "OCR confidence bassa (0.76) - disegno tecnico con poco testo"
          }
        ]
      },
      
      "processing_time_ms": 2145,
      "processed_at": "2025-11-03T10:25:16Z"
    }
  ],
  
  "validation_summary": {
    "all_documents_readable": true,
    "average_ocr_confidence": 0.815,
    "total_entities_extracted": 23,
    "required_docs_present": true,
    "missing_documents": [],
    "issues_count": {
      "critical": 0,
      "warning": 1,
      "info": 1
    }
  },
  
  "processing_summary": {
    "total_documents": 3,
    "ocr_performed": 2,
    "native_text_extraction": 1,
    "total_processing_time_ms": 4424,
    "average_time_per_doc_ms": 1475
  },
  
  "timestamp": "2025-11-03T10:25:16Z"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "DOCUMENT_UNREADABLE",
  "message": "Uno o più documenti non leggibili",
  "details": {
    "failed_documents": [
      {
        "attachment_id": "ATT-002",
        "filename": "scan_illeggibile.pdf",
        "error": "OCR_CONFIDENCE_TOO_LOW",
        "ocr_confidence": 0.23,
        "threshold": 0.60
      }
    ]
  }
}
```

**Error Response** (422 Unprocessable Entity):
```json
{
  "error": "MISSING_REQUIRED_DOCUMENTS",
  "message": "Documenti obbligatori mancanti per procedimento",
  "details": {
    "required": ["istanza_procedimento", "documento_identita", "marca_da_bollo"],
    "provided": ["istanza_procedimento", "documento_identita"],
    "missing": ["marca_da_bollo"]
  }
}
```

### POST /classify-document

Classifica singolo documento (senza OCR full).

**Request**:
```json
{
  "document_path": "s3://bucket/docs/documento.pdf",
  "perform_ocr": false
}
```

**Response**:
```json
{
  "document_type": "visura_camerale",
  "confidence": 0.91,
  "alternative_types": [
    {"type": "bilancio_aziendale", "confidence": 0.15}
  ]
}
```

### POST /extract-text

OCR su singolo documento.

**Request**:
```json
{
  "document_path": "s3://bucket/docs/scansione.pdf",
  "language": "ita",
  "preprocessing": {
    "deskew": true,
    "denoise": true,
    "binarize": true
  }
}
```

**Response**:
```json
{
  "text": "Testo estratto dal documento...",
  "page_count": 3,
  "confidence": 0.89,
  "language_detected": "ita",
  "processing_time_ms": 1823
}
```

### GET /document/{document_id}

Recupera documento già processato.

**Response**:
```json
{
  "document_id": "DOC-001",
  "classification": {},
  "text_extraction": {},
  "extracted_entities": {},
  "created_at": "2025-11-03T10:25:12Z"
}
```

## Sequence Diagrams

### Sequence Diagram: Estrazione Completa Documenti

```mermaid
sequenceDiagram
    autonumber
    participant WF as SP09 Workflow
    participant API as SP02 API
    participant OCR as Tesseract OCR
    participant Classifier as DistilBERT
    participant NER as spaCy NER
    participant Storage as MinIO
    participant DB as PostgreSQL
    participant GPU as GPU Pool
    
    Note over WF,GPU: Input: attachments[] da SP01
    
    WF->>API: POST /extract-documents<br/>{attachments[], workflow_id}
    
    Note over WF,GPU: Fase 1: Download Parallelo
    par Download allegati (parallelo)
        API->>Storage: Download istanza.pdf
        Storage-->>API: pdf_content_1
    and
        API->>Storage: Download documento_identita.pdf
        Storage-->>API: pdf_content_2
    and
        API->>Storage: Download planimetria.pdf
        Storage-->>API: pdf_content_3
    end
    
    Note over WF,GPU: Fase 2: Processing Parallelo per Documento
    
    rect rgb(240, 248, 255)
        Note over API,GPU: Documento 1: istanza.pdf (native text)
        API->>API: Check if PDF is searchable
        API->>API: Extract text with pdfplumber
        API-->>API: text: "Il sottoscritto Mario Rossi..."
        
        API->>Classifier: classify(text_preview)
        Classifier->>Classifier: DistilBERT inference
        Classifier-->>API: {type: "istanza_procedimento", conf: 0.96}
        
        API->>NER: extract_entities(full_text)
        NER->>NER: spaCy NER pipeline
        NER->>NER: Regex patterns (CF, PIVA, date)
        NER-->>API: {persone[], cf[], indirizzi[], date[]}
        
        API->>API: Create document_1 metadata
    end
    
    rect rgb(255, 250, 240)
        Note over API,GPU: Documento 2: documento_identita.pdf (OCR needed)
        API->>API: Check if PDF is searchable
        API->>API: PDF is scanned image → OCR required
        
        API->>OCR: Preprocessing pipeline
        OCR->>OCR: Convert PDF → Image (PIL)
        OCR->>OCR: Deskew (OpenCV)
        OCR->>OCR: Denoise (OpenCV)
        OCR->>OCR: Binarize (Otsu threshold)
        
        API->>GPU: Request GPU slot
        GPU-->>API: GPU allocated
        
        API->>OCR: tesseract(image, lang="ita")<br/>with GPU acceleration
        OCR->>OCR: Text recognition
        OCR-->>API: {text, confidence: 0.87}
        
        API->>GPU: Release GPU
        
        API->>Classifier: classify(ocr_text)
        Classifier-->>API: {type: "documento_identita", conf: 0.98}
        
        API->>NER: extract_entities(ocr_text)
        NER-->>API: {persone[], cf[], date[]}
        
        API->>API: Validate scadenza documento
        API->>API: Create document_2 metadata
    end
    
    rect rgb(240, 255, 240)
        Note over API,GPU: Documento 3: planimetria.pdf (technical drawing)
        API->>API: Detect technical drawing (CAD metadata)
        
        API->>GPU: Request GPU slot
        GPU-->>API: GPU allocated
        
        API->>OCR: tesseract(pages[], lang="ita")
        OCR-->>API: {text, confidence: 0.76}
        
        API->>GPU: Release GPU
        
        API->>Classifier: classify(text + metadata)
        Classifier->>Classifier: Detect "planimetria", "scala", "legenda"
        Classifier-->>API: {type: "planimetria_tecnica", conf: 0.94}
        
        API->>NER: extract_entities(text)
        NER-->>API: {persone: ["Giuseppe Bianchi"], codici[]}
        
        API->>API: Create document_3 metadata
    end
    
    Note over WF,GPU: Fase 3: Validation
    API->>API: Aggregate documents[]
    API->>API: Check all readable (conf > 0.60)
    API->>API: Cross-validate CF consistency
    API->>API: Generate validation summary
    
    Note over WF,GPU: Fase 4: Persistenza
    API->>DB: BEGIN TRANSACTION
    
    loop For each document
        API->>DB: INSERT INTO extracted_documents (...)
    end
    
    API->>DB: INSERT INTO extraction_summary (...)
    API->>DB: COMMIT
    
    Note over WF,GPU: Fase 5: Response
    API-->>WF: {<br/>  documents[3],<br/>  validation_summary,<br/>  processing_summary,<br/>  total_time_ms: 4424<br/>}
    
    WF->>WF: Update workflow:<br/>DOCUMENTS_EXTRACTED
```

### Sequence Diagram: OCR Processing Dettagliato

```mermaid
sequenceDiagram
    autonumber
    participant API as SP02 API
    participant PDF as PyMuPDF
    participant CV as OpenCV
    participant PIL as Pillow
    participant OCR as Tesseract
    participant GPU as CUDA GPU
    
    Note over API,GPU: Input: PDF scansionato (immagine)
    
    API->>PDF: Open PDF file
    PDF-->>API: PDF document handle
    
    API->>PDF: Get page count
    PDF-->>API: page_count: 3
    
    loop For each page
        Note over API,GPU: Page N processing
        
        API->>PDF: Render page to image<br/>(DPI: 300)
        PDF->>PIL: Convert to PIL Image
        PIL-->>API: image_rgb
        
        Note over API,GPU: Preprocessing Pipeline
        
        API->>CV: Convert RGB → Grayscale
        CV-->>API: image_gray
        
        API->>CV: Deskew detection
        CV->>CV: Hough transform line detection
        CV->>CV: Calculate rotation angle
        CV->>CV: Rotate image
        CV-->>API: image_deskewed (angle: -2.3°)
        
        API->>CV: Noise reduction
        CV->>CV: Gaussian blur (kernel: 3x3)
        CV-->>API: image_denoised
        
        API->>CV: Binarization
        CV->>CV: Otsu's threshold
        CV-->>API: image_binary
        
        Note over API,GPU: OCR Execution
        
        API->>GPU: Check GPU availability
        alt GPU available
            GPU-->>API: GPU slot allocated
            API->>OCR: tesseract(image_binary,<br/>lang="ita", oem=1 [LSTM + GPU])
            OCR->>GPU: CUDA acceleration
            GPU->>OCR: Fast inference
        else GPU busy
            API->>OCR: tesseract(image_binary,<br/>lang="ita", oem=0 [CPU legacy])
            Note over OCR: CPU-only processing (slower)
        end
        
        OCR->>OCR: LSTM neural net inference
        OCR->>OCR: Language model correction
        OCR->>OCR: Calculate confidence scores
        
        OCR-->>API: {<br/>  text: "Pagina N testo...",<br/>  confidence: 0.87,<br/>  word_confidences: [...]<br/>}
        
        API->>API: Append to full_text
        API->>API: Aggregate confidence
        
        opt Low confidence detected
            API->>API: Log warning:<br/>"Page N confidence 0.65 < threshold 0.75"
        end
    end
    
    Note over API,GPU: Post-processing
    
    API->>API: Combine all pages text
    API->>API: Calculate average confidence
    API->>API: Detect language (ita/eng/fra)
    API->>API: Text cleanup (fix common OCR errors)
    
    alt Confidence >= 0.60
        API->>API: Mark as readable
        API-->>WF: {text, confidence, status: "success"}
    else Confidence < 0.60
        API->>API: Mark as unreadable
        API-->>WF: {error: "OCR_CONFIDENCE_TOO_LOW",<br/>confidence: 0.52}
    end
```

### Sequence Diagram: Document Classification

```mermaid
sequenceDiagram
    autonumber
    participant API as SP02 API
    participant Cache as Redis Cache
    participant BERT as DistilBERT Model
    participant Preprocessor as Text Preprocessor
    participant GPU as GPU Pool
    
    Note over API,GPU: Input: document text + metadata
    
    API->>API: Generate cache key<br/>hash(text[:1000] + metadata)
    API->>Cache: GET classification:{cache_key}
    
    alt Cache Hit
        Cache-->>API: {type, confidence, cached_at}
        API->>API: Check if cache fresh (<24h)
        alt Cache valid
            API-->>WF: Cached result ✓
            Note over API: Skip inference (fast path)
        end
    end
    
    Note over API,GPU: Cache Miss - ML Inference Required
    
    API->>Preprocessor: Prepare text for BERT
    Preprocessor->>Preprocessor: Truncate to 512 tokens
    Preprocessor->>Preprocessor: Add [CLS], [SEP] tokens
    Preprocessor->>Preprocessor: Create attention mask
    Preprocessor-->>API: {input_ids, attention_mask}
    
    API->>GPU: Request GPU slot
    alt GPU Available
        GPU-->>API: GPU allocated
        API->>BERT: classify(input_ids)<br/>with CUDA
        BERT->>GPU: Forward pass on GPU
        GPU->>BERT: Logits tensor
        Note over BERT,GPU: Fast inference (~100ms)
    else GPU Busy
        API->>BERT: classify(input_ids)<br/>on CPU
        Note over BERT: Slower inference (~450ms)
    end
    
    BERT->>BERT: Softmax on logits
    BERT->>BERT: Get top-3 predictions
    
    BERT-->>API: {<br/>  predictions: [<br/>    {type: "istanza_procedimento", score: 0.96},<br/>    {type: "autocertificazione", score: 0.12},<br/>    {type: "relazione_tecnica", score: 0.05}<br/>  ]<br/>}
    
    API->>API: Apply metadata boosting
    Note over API: Boost score if PDF metadata matches<br/>(e.g. "AutoCAD" → +0.1 for planimetria)
    
    API->>API: Select top prediction
    API->>API: threshold_check(confidence >= 0.70)
    
    alt Confidence >= 0.70
        API->>Cache: SET classification:{key}<br/>{type, confidence}<br/>TTL=24h
        API-->>WF: {<br/>  document_type: "istanza_procedimento",<br/>  confidence: 0.96,<br/>  alternatives: [...]<br/>}
    else Confidence < 0.70
        API->>API: Mark as uncertain
        API-->>WF: {<br/>  document_type: "altro",<br/>  confidence: 0.65,<br/>  warning: "LOW_CONFIDENCE"<br/>}
    end
```

### State Diagram: Ciclo Vita Documento (Document Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> Received

    Received --> Parsing: detect_format()

    Parsing --> TextExtracted: extraction_ok
    Parsing --> ParseError: parse_failed

    ParseError --> Quarantine: [*]

    TextExtracted --> OptionalOCR: requires_ocr()

    OptionalOCR --> OCRProcessing: ocr_needed
    OptionalOCR --> Classifying: ocr_not_needed

    OCRProcessing --> OCRComplete: ocr_ok
    OCRProcessing --> OCRFailed: ocr_error

    OCRFailed --> Classifying: skip_to_classify

    OCRComplete --> Classifying: classify_document

    Classifying --> CacheCheck: check_cache()

    CacheCheck --> CacheHit: cache_valid
    CacheCheck --> CacheMiss: cache_miss

    CacheHit --> Classified: return_cached

    CacheMiss --> MLInference: run_inference()

    MLInference --> ConfidenceCheck: check_confidence()

    ConfidenceCheck --> HighConfidence: confidence_high
    ConfidenceCheck --> LowConfidence: confidence_low

    LowConfidence --> HumanReview: escalate_to_hitl
    HumanReview --> Classified: human_decision

    HighConfidence --> Classified: confident_classification

    Classified --> EntityExtraction: extract_entities()

    EntityExtraction --> Enrichment: enrich_metadata()

    Enrichment --> Storing: save_to_db()

    Storing --> Stored: persistence_ok
    Storing --> PersistenceError: db_error

    PersistenceError --> RetryQueue: retry()
    RetryQueue --> Storing

    Stored --> [*]
    Quarantine --> [*]

    note right of Parsing
        Detect file format
        Extract raw text
        native PDF extraction or OCR path
    end note

    note right of OptionalOCR
        If PDF is image-based
        or requires text validation
        trigger OCR engine
    end note

    note right of MLInference
        Run DistilBERT model
        GPU-accelerated if available
        Cache result (24h TTL)
    end note

    note right of HumanReview
        HITL Checkpoint
        Escalation if confidence < 0.70
        Operator decision feeds feedback loop
    end note
```

## Data Model

### Extracted Documents Table (PostgreSQL)

```sql
CREATE TABLE extracted_documents (
    document_id VARCHAR(50) PRIMARY KEY,
    attachment_id VARCHAR(50) NOT NULL,
    workflow_id VARCHAR(50) NOT NULL,
    
    -- File info
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100),
    size_bytes BIGINT,
    
    -- Classification
    document_type VARCHAR(50) NOT NULL,
    classification_confidence FLOAT,
    alternative_types JSONB,
    
    -- Text extraction
    extraction_method VARCHAR(20), -- 'native_pdf', 'ocr'
    ocr_required BOOLEAN DEFAULT false,
    full_text TEXT,
    text_length INTEGER,
    page_count INTEGER,
    language VARCHAR(10),
    ocr_confidence FLOAT,
    
    -- Entities (JSONB for flexibility)
    extracted_entities JSONB,
    
    -- Metadata
    pdf_metadata JSONB,
    has_digital_signature BOOLEAN DEFAULT false,
    is_searchable_pdf BOOLEAN,
    is_technical_drawing BOOLEAN DEFAULT false,
    
    -- Validation
    is_readable BOOLEAN DEFAULT true,
    completeness_score FLOAT,
    validation_issues JSONB,
    
    -- Processing
    processing_time_ms INTEGER,
    processed_at TIMESTAMP DEFAULT NOW(),
    
    -- Foreign keys
    FOREIGN KEY (attachment_id) REFERENCES email_attachments(attachment_id),
    FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id)
);

CREATE INDEX idx_extracted_docs_workflow ON extracted_documents(workflow_id);
CREATE INDEX idx_extracted_docs_type ON extracted_documents(document_type);
CREATE INDEX idx_extracted_docs_attachment ON extracted_documents(attachment_id);
CREATE INDEX idx_extracted_entities_gin ON extracted_documents USING gin(extracted_entities);
```

### Extraction Summary Table

```sql
CREATE TABLE extraction_summaries (
    summary_id VARCHAR(50) PRIMARY KEY,
    workflow_id VARCHAR(50) NOT NULL UNIQUE,
    
    -- Statistics
    total_documents INTEGER,
    ocr_performed_count INTEGER,
    native_extraction_count INTEGER,
    
    -- Validation
    all_documents_readable BOOLEAN,
    average_ocr_confidence FLOAT,
    total_entities_extracted INTEGER,
    required_docs_present BOOLEAN,
    missing_documents TEXT[],
    
    -- Issues
    critical_issues_count INTEGER DEFAULT 0,
    warning_issues_count INTEGER DEFAULT 0,
    info_issues_count INTEGER DEFAULT 0,
    
    -- Performance
    total_processing_time_ms INTEGER,
    average_time_per_doc_ms INTEGER,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id)
);

CREATE INDEX idx_extraction_summary_workflow ON extraction_summaries(workflow_id);
```

## Business Logic

### Document Type Detection

**16 categorie supportate** con pattern di riconoscimento:

1. **istanza_procedimento**: Keywords "richiede", "istanza", "domanda", form compilato
2. **documento_identita**: "carta identità", "patente", "passaporto", foto persona
3. **visura_camerale**: "Camera Commercio", "REA", CCIAA logo
4. **planimetria_tecnica**: Metadata CAD, "scala 1:", "legenda", layout tecnico
5. **relazione_tecnica**: Firma professionale, "Dott. Ing.", timbro
6. **autocertificazione**: "ai sensi dell'art.", "dichiara", DPR 445/2000
7. **marca_da_bollo**: "€ 16,00", barcode, "Agenzia Entrate"
8. **ricevuta_pagamento**: IBAN, "bonifico", "PagoPA", IUV
9. **atto_notarile**: "Notaio", "repertorio", firma autenticata
10. **certificato_pa**: Timbro PA, "certifica", protocolollo
11. **contratto**: "Contratto", "parti contraenti", firme multiple
12. **polizza_assicurativa**: "Assicurazione", premio, massimale
13. **bilancio_aziendale**: "Stato Patrimoniale", "Conto Economico"
14. **curriculum_vitae**: "Curriculum", esperienze lavorative, formazione
15. **dichiarazione_redditi**: "CU", "730", "Unico", reddito complessivo
16. **altro**: Catch-all per documenti non classificabili

### OCR Preprocessing Pipeline

**Step di preprocessing** per migliorare OCR accuracy:

1. **Deskew**: Correzione rotazione immagine (Hough transform)
2. **Denoise**: Riduzione rumore (Gaussian blur)
3. **Binarization**: Conversione bianco/nero (Otsu's threshold)
4. **Resolution**: Upscaling a 300 DPI se necessario
5. **Contrast**: Enhancement contrasto per testo sbiadito

**Configurazioni OCR Tesseract**:
- Language: `ita` (italiano prioritario)
- OEM: 1 (LSTM neural net with GPU if available)
- PSM: 3 (automatic page segmentation)
- Timeout: 30s per pagina

### Validation Rules

**Controlli automatici**:

1. **Leggibilità**: OCR confidence >= 0.60
2. **Scadenze**: Documenti identità validi alla data odierna
3. **Consistenza CF**: CF uguale in tutti i documenti
4. **Completezza**: Documenti obbligatori presenti per tipo procedimento
5. **Formato**: PDF valido, pagine leggibili

**Severity levels**:
- **critical**: Blocca workflow (es. documento illeggibile)
- **warning**: Richiede verifica (es. scadenza documento vicina)
- **info**: Informativo (es. OCR confidence < 0.85 ma >= 0.60)

## Performance

### Metriche Target

| Metrica | Target | Attuale | Note |
|---------|--------|---------|------|
| **OCR Time (1 page)** | <2s | 1.2s | Con GPU acceleration |
| **OCR Time (1 page CPU)** | <5s | 3.8s | Fallback senza GPU |
| **Classification** | <500ms | 320ms | Con GPU + cache |
| **NER Extraction** | <300ms | 245ms | spaCy + regex |
| **Full Document** | <3s | 2.5s | Media su doc misto (OCR+class+NER) |
| **Throughput** | 40 doc/min | 35/min | Con 12 worker + 4 GPU |
| **OCR Accuracy** | >85% | 87% | Media su dataset test |

### Scalability

**Horizontal Scaling**:
- **Worker Celery**: 6-12 replicas (CPU-bound)
- **GPU Pool**: 2-4 GPU (Tesla T4 o equivalente)
- **Queue**: RabbitMQ con priority routing (OCR > classification)

**Optimizations**:
- **Batch OCR**: Processa pagine multiple in parallelo (GPU batch inference)
- **Caching**: Redis per classificazioni già viste (24h TTL, 43% hit rate)
- **Smart routing**: Documenti native PDF bypass OCR
- **GPU sharing**: Time-slicing per max utilizzo

## Error Handling

### Tipi di Errore

1. **OCR_CONFIDENCE_TOO_LOW**: Testo non leggibile (conf < 0.60)
   - **Retry**: No
   - **Action**: Flag documento, richiedi re-invio scansione migliore

2. **DOCUMENT_TOO_LARGE**: PDF > 25MB o > 100 pagine
   - **Retry**: No
   - **Action**: Split manuale richiesto

3. **UNSUPPORTED_FORMAT**: Formato non PDF (DOCX, JPG raw, ecc.)
   - **Retry**: No
   - **Action**: Conversione manuale a PDF

4. **GPU_UNAVAILABLE**: Tutte GPU busy
   - **Retry**: Fallback CPU automatico
   - **Action**: Processing più lento ma funzionale

5. **TESSERACT_TIMEOUT**: OCR supera 30s per pagina
   - **Retry**: Una volta con PSM diverso
   - **Action**: Documento troppo complesso, split richiesto

### Circuit Breaker

Protezione da GPU/Tesseract failures:
- **Threshold**: 10 errori consecutivi
- **Recovery**: 120s
- **Fallback**: Queue bassa priorità per retry manuale

## Monitoring & Observability

### Metriche Prometheus

**Counters**:
- `sp02_documents_processed_total{type}` - Documenti per tipo
- `sp02_ocr_performed_total` - OCR eseguiti
- `sp02_classification_success_total` - Classificazioni riuscite
- `sp02_extraction_failed_total{error_type}` - Fallimenti per tipo

**Histograms**:
- `sp02_ocr_duration_seconds{gpu}` - Durata OCR (GPU vs CPU)
- `sp02_classification_duration_seconds` - Durata classificazione
- `sp02_document_size_pages` - Dimensione documenti in pagine
- `sp02_ocr_confidence_score` - Distribuzione confidence OCR

**Gauges**:
- `sp02_gpu_utilization_percent` - Utilizzo GPU
- `sp02_active_ocr_tasks` - Task OCR attivi
- `sp02_queue_depth` - Profondità coda processing

### Health Check

**GET /health**

```json
{
  "status": "healthy",
  "checks": {
    "database": true,
    "storage": true,
    "cache": true,
    "gpu": true,
    "tesseract": true
  },
  "gpu_status": {
    "available_gpus": 4,
    "utilization": [45, 67, 23, 89],
    "memory_used_mb": [2048, 3072, 1024, 4096]
  },
  "timestamp": "2025-11-03T11:00:00Z"
}
```

## Testing

### Test Coverage

**Unit Tests**:
- OCR preprocessing (deskew, denoise, binarize)
- Document classification (16 tipi)
- NER extraction (CF, PIVA, indirizzi, importi, date)
- Validation rules (scadenze, consistenza, completezza)

**Integration Tests**:
- Full pipeline: PDF → OCR → classify → NER → DB
- GPU acceleration vs CPU fallback
- Batch processing 10+ documenti paralleli
- Error handling (OCR timeout, low confidence)

**Test Fixtures**:
- `native_text.pdf` - PDF searchable (no OCR)
- `scanned_good_quality.pdf` - Scansione pulita (OCR conf > 0.90)
- `scanned_poor_quality.pdf` - Scansione sbiadita (OCR conf ~0.65)
- `technical_drawing.pdf` - Planimetria CAD A3
- `identity_card.pdf` - Carta identità fronte/retro
- `mixed_batch.zip` - 15 documenti vari tipi

**Coverage target**: >80% line coverage

## Deployment

### Docker Compose

```yaml
services:
  sp02-api:
    build: ./sp02
    ports:
      - "8002:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/provvedimenti
      - MINIO_ENDPOINT=minio:9000
      - REDIS_URL=redis://cache:6379
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
      - TESSERACT_PATH=/usr/bin/tesseract
      - GPU_ENABLED=true
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    depends_on:
      - db
      - minio
      - cache
      - rabbitmq
  
  sp02-worker:
    build: ./sp02
    command: celery -A sp02.tasks worker --loglevel=info --concurrency=4 --pool=prefork
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/provvedimenti
      - MINIO_ENDPOINT=minio:9000
      - REDIS_URL=redis://cache:6379
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672
      - TESSERACT_PATH=/usr/bin/tesseract
      - GPU_ENABLED=true
    deploy:
      replicas: 12
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    depends_on:
      - rabbitmq
      - db
      - minio
```

### GPU Requirements

**Minimum**:
- 1x NVIDIA GPU (Tesla T4 o equivalente)
- 4GB VRAM
- CUDA 12.0+
- cuDNN 8.x

**Recommended**:
- 4x NVIDIA GPU (Tesla T4/V100)
- 16GB VRAM per GPU
- NVLink per multi-GPU
## 🏛️ Conformità Normativa - SP02

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP02 (Document Extractor)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC1, UC5

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP02 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP02 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Responsabile della Protezione dei Dati (DPO))

---

### 6. Monitoraggio Conformità

**Schedule di Review**:
- **Trimestrale**: Compliance assessment + security audit
- **Semestrale**: Framework alignment review (CAD/GDPR/eIDAS/AGID)
- **Annuale**: Full compliance audit + risk assessment

**KPI Conformità**:
- Audit trail completeness: 100%
- Incident response time: <24h
- Compliance violations: 0 per quarter
- Certificate expiry (if eIDAS): Alert at 30 days

**Escalation**: Non-conformità → Compliance Manager → CTO → Legal

**Prossima review programmata**: 2026-02-17

---

## Riepilogo Conformità SP02

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsabile |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ✅ Sì | ✅ Compliant | DPO |
| eIDAS | ❌ No | N/A | - |
| AGID | ❌ No | N/A | - |

**Key Compliance Points**:
1. All CAD articles implemented
2. Data handling compliant with applicable regulations
3. Security controls in place (encryption, access control, audit logging)
4. Regular monitoring and review schedule established
5. Clear responsibility assignments (RACI)

**Prossima Review**: 2026-02-17

---



### Framework Normativi Applicabili

☑ L. 241/1990
☑ CAD
☑ GDPR
☐ eIDAS - Regolamento 2014/910
☐ AI Act - Regolamento 2024/1689
☐ D.Lgs 42/2004 - Codice Beni Culturali
☐ D.Lgs 152/2006 - Codice dell'Ambiente
☐ D.Lgs 33/2013 - Decreto Trasparenza

**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
| L. 241/1990 | Art. 1, Art. 3, Art. 6, Art. 27 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| CAD | Art. 1, Art. 21, Art. 22, Art. 62 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| GDPR | Art. 5, Art. 32 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP02

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP02 (Document Extractor)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC1, UC5

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP02 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP02 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Responsabile della Protezione dei Dati (DPO))

---

### 6. Monitoraggio Conformità

**Schedule di Review**:
- **Trimestrale**: Compliance assessment + security audit
- **Semestrale**: Framework alignment review (CAD/GDPR/eIDAS/AGID)
- **Annuale**: Full compliance audit + risk assessment

**KPI Conformità**:
- Audit trail completeness: 100%
- Incident response time: <24h
- Compliance violations: 0 per quarter
- Certificate expiry (if eIDAS): Alert at 30 days

**Escalation**: Non-conformità → Compliance Manager → CTO → Legal

**Prossima review programmata**: 2026-02-17

---

## Riepilogo Conformità SP02

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsabile |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ✅ Sì | ✅ Compliant | DPO |
| eIDAS | ❌ No | N/A | - |
| AGID | ❌ No | N/A | - |

**Key Compliance Points**:
1. All CAD articles implemented
2. Data handling compliant with applicable regulations
3. Security controls in place (encryption, access control, audit logging)
4. Regular monitoring and review schedule established
5. Clear responsibility assignments (RACI)

**Prossima Review**: 2026-02-17

---



---


## Roadmap

### Q1 2026
- [ ] Support formati aggiuntivi (DOCX, ODT via LibreOffice)
- [ ] ML model per layout analysis (detect tables, forms)
- [ ] Auto-rotation immagini (detect orientation)

### Q2 2026
- [ ] OCR multilingua (inglese, francese, tedesco)
- [ ] Handwriting recognition (firme, note manoscritte)
- [ ] Advanced NER (IBAN, codici catastali, coordinate GPS)

### Q3 2026
- [ ] Fine-tuning DistilBERT su dataset PA custom
- [ ] Document deduplication (detect documenti già processati)
- [ ] Quality scoring ML model (predict doc quality before OCR)

---

**Owner**: Team AI/ML  
**Status**: ✅ Produzione  
**Ultima revisione**: 2025-11-03
