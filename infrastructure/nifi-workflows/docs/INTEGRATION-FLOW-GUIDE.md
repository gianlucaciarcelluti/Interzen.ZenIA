# Guida Completa: Flusso di Integrazione End-to-End

## 📋 Panoramica del Sistema

Questo documento descrive il **flusso completo di integrazione** tra tutti i componenti del sistema di generazione atti amministrativi, con esempi reali di payload, endpoint e sequence diagram dettagliati.

### Architettura Componenti

```
┌─────────────┐
│   Frontend  │ ◄─── User Interface (Streamlit/React)
│  (Streamlit)│
└──────┬──────┘
       │ HTTP REST
       ▼
┌─────────────┐
│  Apache NiFi│ ◄─── Workflow Orchestrator
│   Port 8080 │      (Process Groups SP01-SP11)
└──────┬──────┘
       │ HTTP POST
       ├───────────────┬──────────────┬──────────────┬
       ▼               ▼              ▼              ▼
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│   SP01   │   │   SP02   │   │   SP03   │   │   SP04   │
│Port 9091 │   │Port 9092 │   │Port 9093 │   │Port 9094 │
└────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘
     │              │              │              │
     └──────────────┴──────────────┴──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │  PostgreSQL  │ ◄─── Database Layer
            │   Port 5432  │
            └──────────────┘
```

---

## 🔄 Flusso 1: Generazione Atto da Fascicolo

### Sequence Diagram Completo

```mermaid
sequenceDiagram
    autonumber
    participant U as Utente (UI)
    participant FE as Frontend Streamlit
    participant NiFi as Apache NiFi
    participant SP01 as SP01 EML Parser
    participant SP02 as SP02 Doc Extractor
    participant SP03 as SP03 Procedural Classifier
    participant SP04 as SP04 Knowledge Base
    participant DB as PostgreSQL
    participant HITL as HITL Interface
    
    Note over U,DB: FASE 1: Upload Fascicolo e Parsing
    
    U->>FE: Upload fascicolo.zip
    FE->>FE: Estrai file .eml + allegati
    FE->>NiFi: POST /contentListener/fascicolo<br/>{fascicolo_data}
    activate NiFi
    
    NiFi->>NiFi: Genera workflow_id: WF-20251104-001
    NiFi->>DB: INSERT workflow_executions<br/>{workflow_id, status: STARTED}
    
    NiFi->>SP01: POST http://sp01:9091/parse-email<br/>{eml_content}
    activate SP01
    SP01->>SP01: Parse headers + body + attachments
    SP01->>DB: INSERT INTO emails
    SP01-->>NiFi: {email_id, sender, subject,<br/>attachments: []}
    deactivate SP01
    
    NiFi->>DB: UPDATE workflow_executions<br/>status: EMAIL_PARSED
    
    Note over U,DB: FASE 2: Estrazione Documenti
    
    NiFi->>SP02: POST http://sp02:9092/extract<br/>{attachments[]}
    activate SP02
    SP02->>SP02: Extract istanza.pdf
    SP02->>SP02: NER: richiedente, CF, oggetto
    SP02->>DB: INSERT INTO documenti
    SP02-->>NiFi: {documenti_estratti: [],<br/>metadata: {}}
    deactivate SP02
    
    NiFi->>DB: UPDATE workflow_executions<br/>status: DOCS_EXTRACTED
    
    Note over U,DB: FASE 3: Classificazione Procedimento
    
    NiFi->>SP03: POST http://sp03:9093/classify<br/>{istanza_data}
    activate SP03
    SP03->>SP03: DistilBERT inference
    SP03->>SP04: GET /retrieve-procedures
    activate SP04
    SP04->>SP04: Semantic search + Graph
    SP04-->>SP03: {procedimenti_rilevanti}
    deactivate SP04
    SP03->>DB: INSERT INTO classificazioni
    SP03-->>NiFi: {procedimento: "AUTORIZ_SCARICO",<br/>confidence: 0.94}
    deactivate SP03
    
    NiFi->>DB: UPDATE workflow_executions<br/>status: CLASSIFIED
    
    Note over U,DB: FASE 4: Human in the Loop
    
    NiFi->>HITL: POST /hitl/checkpoint-1<br/>{workflow_id, procedimento}
    activate HITL
    HITL->>FE: Mostra proposta classificazione
    FE-->>U: Review procedimento suggerito
    U->>FE: ✅ Conferma / ✏️ Modifica
    FE->>HITL: POST /decisions<br/>{decision, motivazione}
    HITL->>DB: INSERT hitl_decisions
    HITL-->>NiFi: {approved: true}
    deactivate HITL
    
    NiFi->>NiFi: Resume workflow
    NiFi->>DB: UPDATE workflow_executions<br/>status: COMPLETED
    
    NiFi-->>FE: {workflow_id, status: COMPLETED,<br/>documento_id}
    deactivate NiFi
    FE-->>U: ✅ Documento generato
```

---

### Sequence Diagram: Chiamata SP01 EML Parser

```mermaid
sequenceDiagram
    participant NiFi as Apache NiFi
    participant SP01 as SP01 EML Parser<br/>Port 9091
    participant DB as PostgreSQL
    participant MINIO as MinIO Storage

    NiFi->>SP01: POST /parse-email<br/>Headers: X-Workflow-ID, Content-Type
    activate SP01

    SP01->>SP01: Validate request payload
    SP01->>SP01: Decode base64 eml_content
    SP01->>SP01: Parse email headers (From, To, Subject, Date)

    SP01->>SP01: Extract plain text body
    SP01->>SP01: Extract HTML body (if present)
    SP01->>SP01: Detect language (Italian)

    SP01->>SP01: Extract attachments from eml
    loop For each attachment
        SP01->>SP01: Decode base64 attachment
        SP01->>SP01: Validate attachment integrity
        SP01->>MINIO: Upload attachment file
        SP01->>SP01: Generate attachment metadata
    end

    SP01->>SP01: Validate PEC signature (if present)
    SP01->>DB: INSERT INTO emails<br/>(email_id, workflow_id, metadata, attachments)

    SP01-->>NiFi: 200 OK<br/>{email_id, metadata, attachments[]}
    deactivate SP01

    Note right of SP01: Processing time: ~850ms
```

### Sequence Diagram: Chiamata SP02 Document Extractor

```mermaid
sequenceDiagram
    participant NiFi as Apache NiFi
    participant SP02 as SP02 Doc Extractor<br/>Port 9092
    participant DB as PostgreSQL
    participant MINIO as MinIO Storage

    NiFi->>SP02: POST /extract<br/>Headers: X-Workflow-ID, Content-Type
    activate SP02

    SP02->>SP02: Validate attachments array
    loop For each attachment
        SP02->>MINIO: Download attachment file
        SP02->>SP02: Detect document type (PDF, DOC, etc.)

        alt PDF Document
            SP02->>SP02: Extract text (native, no OCR)
            SP02->>SP02: Extract metadata (pages, author, creation date)
        else Image Document
            SP02->>SP02: OCR processing with Tesseract
            SP02->>SP02: Extract text from image
        end

        SP02->>SP02: Named Entity Recognition (NER)
        SP02->>SP02: Extract: PERSON, ORG, DATE, MONEY, LAW_REF

        SP02->>SP02: Classify document type<br/>(istanza, documento_identita, planimetria)
        SP02->>SP02: Calculate confidence score

        SP02->>DB: INSERT INTO documenti<br/>(doc_id, attachment_id, tipo, testo, entities, confidence)
    end

    SP02->>SP02: Validate completezza documentazione
    SP02->>SP02: Check documenti obbligatori presenti

    SP02-->>NiFi: 200 OK<br/>{documenti_estratti[], validazione_documenti}
    deactivate SP02

    Note right of SP02: Processing time: ~2.5s
```

### Sequence Diagram: Chiamata SP03 Procedural Classifier

```mermaid
sequenceDiagram
    participant NiFi as Apache NiFi
    participant SP03 as SP03 Classifier<br/>Port 9093
    participant SP04 as SP04 Knowledge Base<br/>Port 9094
    participant DB as PostgreSQL
    participant CACHE as Redis Cache

    NiFi->>SP03: POST /classify<br/>Headers: X-Workflow-ID, Content-Type
    activate SP03

    SP03->>CACHE: Check cache for similar documents
    alt Cache Hit
        SP03->>CACHE: Retrieve cached classification
    else Cache Miss
        SP03->>SP03: Preprocess document text
        SP03->>SP03: DistilBERT inference for classification
        SP03->>SP03: Extract entities and context

        SP03->>SP04: GET /retrieve-procedures<br/>{entities, context}
        activate SP04
        SP04->>SP04: Semantic search in vector DB
        SP04->>SP04: Graph traversal for relations
        SP04->>SP04: Retrieve legal precedents
        SP04-->>SP03: {procedimenti_rilevanti, normativa_refs}
        deactivate SP04

        SP03->>SP03: Ranking and confidence scoring
        SP03->>CACHE: Store result (TTL: 2h)
    end

    SP03->>DB: INSERT INTO classificazioni<br/>(workflow_id, procedimento, confidence, metadata)

    SP03-->>NiFi: 200 OK<br/>{procedimento, tipo_provvedimento, normativa_base}
    deactivate SP03

    Note right of SP03: Processing time: ~520ms
```

### Sequence Diagram: Human in the Loop Checkpoint

```mermaid
sequenceDiagram
    participant NiFi as Apache NiFi
    participant HITL as HITL Manager<br/>Port 8000
    participant FE as Frontend UI<br/>Port 8501
    participant U as Utente
    participant DB as PostgreSQL

    NiFi->>HITL: POST /hitl/checkpoint-1<br/>{workflow_id, data, ui_config}
    activate HITL

    HITL->>HITL: Generate checkpoint_id
    HITL->>DB: INSERT INTO hitl_checkpoints<br/>(checkpoint_id, workflow_id, type, data)

    HITL->>FE: WebSocket/SSE notification<br/>{checkpoint_id, workflow_id, type: "CONFERMA_PROCEDIMENTO"}
    activate FE

    FE->>FE: Render HITL interface
    FE->>U: Show classification proposal<br/>+ alternatives + confidence scores
    activate U

    U->>FE: Review and decide<br/>(Approve/Modify/Reject)
    deactivate U

    FE->>HITL: POST /decisions<br/>{checkpoint_id, decision, user_id, motivazione}
    deactivate FE

    HITL->>HITL: Validate decision
    HITL->>DB: INSERT INTO hitl_decisions<br/>(checkpoint_id, decision, user_id, timestamp)

    alt Decision = APPROVED
        HITL->>NiFi: Resume workflow<br/>{checkpoint_id, approved: true}
    else Decision = MODIFIED
        HITL->>NiFi: Resume with modifications<br/>{checkpoint_id, modifications: {...}}
    else Decision = REJECTED
        HITL->>NiFi: Stop workflow<br/>{checkpoint_id, reason: "rejected"}
    end

    deactivate HITL
```

---

## 📡 Dettaglio Endpoint e Payload

### 1️⃣ Frontend → NiFi: Inizia Workflow

**Endpoint**: `POST http://localhost:8080/contentListener/fascicolo`

**Headers**:
```http
Content-Type: application/json
X-User-ID: user_123
X-Session-ID: session_abc123
```

**Request Payload**:
```json
{
  "tipo_richiesta": "generazione_atto",
  "fascicolo": {
    "id": "FASC-2025-00123",
    "oggetto": "Autorizzazione scarico acque reflue industriali",
    "richiedente": {
      "nome": "Azienda XYZ S.r.l.",
      "cf_piva": "12345678901",
      "email": "info@aziendaxyz.it",
      "pec": "aziendaxyz@pec.it"
    }
  },
  "eml_content": "base64_encoded_eml_file...",
  "attachments": [
    {
      "filename": "istanza.pdf",
      "content": "base64_encoded_pdf...",
      "mime_type": "application/pdf",
      "size": 2048576
    },
    {
      "filename": "documento_identita.pdf.p7m",
      "content": "base64_encoded_signed_pdf...",
      "mime_type": "application/pkcs7-signature",
      "size": 512000
    }
  ],
  "metadata": {
    "data_ricezione": "2025-11-04T10:30:00Z",
    "protocollo_arrivo": "PROT-2025-12345"
  }
}
```

**Response**:
```json
{
  "success": true,
  "workflow_id": "WF-20251104-001",
  "status": "STARTED",
  "message": "Workflow avviato con successo",
  "timestamp": "2025-11-04T10:30:05Z",
  "tracking_url": "http://localhost:8080/nifi-api/provenance/events?componentId=..."
}
```

---

### 2️⃣ NiFi → SP01: Parse Email

**Endpoint**: `POST http://sp01:9091/parse-email`

**Headers**:
```http
Content-Type: application/json
X-Workflow-ID: WF-20251104-001
X-NiFi-FlowFile-UUID: abc-123-def-456
```

**Request Payload**:
```json
{
  "eml_content": "From: aziendaxyz@pec.it\nSubject: Richiesta autorizzazione scarico...",
  "eml_base64": "RnJvbTogYXppZW5kYXh5ekBwZWMuaXQK...",
  "parse_options": {
    "extract_attachments": true,
    "validate_signature": true,
    "extract_metadata": true
  }
}
```

**Response**:
```json
{
  "email_id": "EML-20251104-001",
  "metadata": {
    "from": "aziendaxyz@pec.it",
    "to": "protocollo@comune.it",
    "subject": "Richiesta autorizzazione scarico acque reflue",
    "date": "2025-11-04T09:15:00Z",
    "message_id": "<abc123@pec.it>",
    "pec_verified": true,
    "signature_valid": true
  },
  "body": {
    "plain_text": "Spett.le Comune,\nCon la presente si richiede...",
    "html": "<html>...</html>",
    "language": "it"
  },
  "attachments": [
    {
      "attachment_id": "ATT-001",
      "filename": "istanza.pdf",
      "mime_type": "application/pdf",
      "size": 2048576,
      "hash_sha256": "abc123def456...",
      "extracted_path": "/tmp/attachments/istanza.pdf"
    },
    {
      "attachment_id": "ATT-002",
      "filename": "documento_identita.pdf.p7m",
      "mime_type": "application/pkcs7-signature",
      "size": 512000,
      "hash_sha256": "def456abc789...",
      "signature_verified": true,
      "signer_cn": "CN=Mario Rossi, O=Azienda XYZ"
    }
  ],
  "processing_time_ms": 850,
  "status": "success"
}
```

**Error Response**:
```json
{
  "error": true,
  "error_code": "INVALID_EML_FORMAT",
  "message": "Il file .eml non è valido: manca header From",
  "details": {
    "line": 5,
    "expected": "From: sender@domain.com"
  },
  "status": "failed"
}
```

---

### 3️⃣ NiFi → SP02: Estrai Documenti

**Endpoint**: `POST http://sp02:9092/extract`

**Headers**:
```http
Content-Type: application/json
X-Workflow-ID: WF-20251104-001
X-Previous-Step: SP01
```

**Request Payload**:
```json
{
  "attachments": [
    {
      "attachment_id": "ATT-001",
      "file_path": "/tmp/attachments/istanza.pdf",
      "filename": "istanza.pdf",
      "mime_type": "application/pdf"
    }
  ],
  "extraction_options": {
    "ocr_enabled": true,
    "ner_enabled": true,
    "extract_tables": true,
    "language": "it"
  }
}
```

**Response**:
```json
{
  "extraction_id": "EXTR-20251104-001",
  "documenti_estratti": [
    {
      "documento_id": "DOC-001",
      "attachment_id": "ATT-001",
      "tipo": "istanza_procedimento",
      "confidence": 0.96,
      "testo_estratto": "Spett.le Comune di ...\nCon la presente si richiede...",
      "metadata": {
        "pages": 3,
        "ocr_used": false,
        "extraction_method": "native_text"
      },
      "entities": [
        {
          "tipo": "PERSONA",
          "valore": "Mario Rossi",
          "confidence": 0.98,
          "ruolo": "richiedente"
        },
        {
          "tipo": "CODICE_FISCALE",
          "valore": "RSSMRA80A01H501X",
          "confidence": 1.0
        },
        {
          "tipo": "IMPORTO",
          "valore": "€ 15.000,00",
          "confidence": 0.95
        },
        {
          "tipo": "DATA",
          "valore": "2025-12-31",
          "confidence": 0.99,
          "contesto": "data scadenza lavori"
        }
      ],
      "tabelle": [
        {
          "id": "TAB-001",
          "righe": 5,
          "colonne": 3,
          "header": ["Descrizione", "Quantità", "Importo"],
          "data_estratta": [
            ["Opere idrauliche", "1", "€ 10.000"],
            ["Impianto depurazione", "1", "€ 5.000"]
          ]
        }
      ],
      "normativa_riferimento": [
        {
          "riferimento": "D.Lgs 152/2006",
          "articolo": "Art. 124",
          "confidence": 0.92
        }
      ]
    }
  ],
  "validazione_documenti": {
    "documenti_obbligatori_presenti": true,
    "documenti_mancanti": [],
    "warning": []
  },
  "processing_time_ms": 2450,
  "status": "success"
}
```

---

### 4️⃣ NiFi → SP03: Classifica Procedimento

**Endpoint**: `POST http://sp03:9093/classify`

**Headers**:
```http
Content-Type: application/json
X-Workflow-ID: WF-20251104-001
X-Previous-Step: SP02
```

**Request Payload**:
```json
{
  "documenti": [
    {
      "documento_id": "DOC-001",
      "tipo": "istanza_procedimento",
      "testo": "Con la presente si richiede autorizzazione...",
      "entities": [
        {"tipo": "PERSONA", "valore": "Mario Rossi"},
        {"tipo": "IMPORTO", "valore": "€ 15.000,00"}
      ]
    }
  ],
  "email_metadata": {
    "subject": "Richiesta autorizzazione scarico acque reflue",
    "from": "aziendaxyz@pec.it"
  },
  "context": {
    "settore": "AMBIENTE",
    "tipo_richiedente": "AZIENDA"
  }
}
```

**Response**:
```json
{
  "classificazione_id": "CLASS-20251104-001",
  "procedimento": {
    "codice": "AUTORIZ_SCARICO_ACQUE",
    "nome": "Autorizzazione Scarico Acque Reflue Industriali",
    "categoria": "AMBIENTE",
    "sottocategoria": "TUTELA_ACQUE",
    "confidence": 0.94
  },
  "tipo_provvedimento": {
    "tipo": "DETERMINAZIONE",
    "organo_competente": "RESPONSABILE_UFFICIO_AMBIENTE",
    "confidence": 0.91
  },
  "normativa_base": [
    {
      "riferimento": "D.Lgs 152/2006",
      "titolo": "Norme in materia ambientale",
      "parte": "Parte Terza - Tutela delle acque",
      "articolo": "Art. 124",
      "rilevanza": 0.98
    },
    {
      "riferimento": "L.R. 12/2005",
      "titolo": "Legge regionale ambiente",
      "rilevanza": 0.85
    }
  ],
  "procedimenti_alternativi": [
    {
      "codice": "AUTORIZ_EMISSIONI",
      "nome": "Autorizzazione Emissioni Atmosfera",
      "similarity": 0.67,
      "motivo_scarto": "Oggetto non corrispondente"
    }
  ],
  "tempi_procedimento": {
    "termine_giorni": 90,
    "silenzio_assenso": false,
    "proroga_possibile": true
  },
  "metadata": {
    "model_used": "distilbert-base-italian-cased",
    "classification_method": "supervised_learning",
    "training_samples": 1245
  },
  "processing_time_ms": 520,
  "status": "success"
}
```

---

### 5️⃣ SP03 → SP04: Recupera Contesto Normativo

**Endpoint**: `GET http://sp04:9094/retrieve-procedures`

**Headers**:
```http
Content-Type: application/json
X-Workflow-ID: WF-20251104-001
```

**Request Payload**:
```json
{
  "query": {
    "procedimento": "AUTORIZ_SCARICO_ACQUE",
    "normativa_refs": ["D.Lgs 152/2006", "L.R. 12/2005"],
    "entities": [
      {"tipo": "IMPORTO", "valore": "€ 15.000,00"}
    ]
  },
  "retrieval_options": {
    "max_results": 5,
    "include_giurisprudenza": true,
    "include_precedenti": true,
    "semantic_search": true
  }
}
```

**Response**:
```json
{
  "retrieval_id": "RETR-20251104-001",
  "legal_context": {
    "normativa_principale": [
      {
        "riferimento": "D.Lgs 152/2006",
        "articolo": "Art. 124",
        "comma": "1",
        "testo": "Tutti gli scarichi devono essere preventivamente autorizzati...",
        "vigente": true,
        "ultima_modifica": "2023-06-15",
        "rilevanza": 0.98
      },
      {
        "riferimento": "D.Lgs 152/2006",
        "articolo": "Art. 101",
        "testo": "Tutela qualitativa e quantitativa...",
        "rilevanza": 0.87
      }
    ],
    "normativa_correlata": [
      {
        "riferimento": "L. 241/1990",
        "articolo": "Art. 5",
        "testo": "Responsabile del procedimento...",
        "rilevanza": 0.75
      }
    ],
    "giurisprudenza": [
      {
        "fonte": "Consiglio di Stato",
        "numero_sentenza": "1234/2024",
        "data": "2024-03-15",
        "massima": "L'autorizzazione allo scarico è atto vincolato...",
        "rilevanza": 0.82
      },
      {
        "fonte": "TAR Lazio",
        "numero_sentenza": "5678/2023",
        "massima": "Requisiti minimi parametri chimici...",
        "rilevanza": 0.68
      }
    ],
    "precedenti_simili": [
      {
        "doc_id": "DELIB-2024-0123",
        "data": "2024-05-20",
        "oggetto": "Autorizzazione scarico Azienda ABC",
        "esito": "APPROVATA",
        "similarity": 0.89,
        "tempo_istruttoria_giorni": 65
      },
      {
        "doc_id": "DETERM-2024-0045",
        "oggetto": "Autorizzazione scarico temporaneo",
        "esito": "APPROVATA_CON_PRESCRIZIONI",
        "similarity": 0.76
      }
    ]
  },
  "knowledge_graph_path": [
    "D.Lgs 152/2006 -> integra -> D.Lgs 3/2006",
    "D.Lgs 152/2006 -> modifica -> D.Lgs 152/1999",
    "L.R. 12/2005 -> attua -> D.Lgs 152/2006"
  ],
  "rag_synthesis": "Per l'autorizzazione allo scarico di acque reflue industriali è necessario rispettare i parametri di cui alla Tabella 3 Allegato 5 del D.Lgs 152/2006. Il procedimento ha termine di 90 giorni e richiede parere ARPA. Il responsabile del procedimento ai sensi L.241/90 deve essere nominato entro 10 giorni.",
  "confidence_score": 0.91,
  "processing_time_ms": 1200,
  "status": "success"
}
```

---

### 6️⃣ NiFi → HITL: Checkpoint Decisionale

**Endpoint**: `POST http://hitl:8000/hitl/checkpoint-1`

**Headers**:
```http
Content-Type: application/json
X-Workflow-ID: WF-20251104-001
```

**Request Payload**:
```json
{
  "checkpoint_id": "HITL-CHECKPOINT-1",
  "workflow_id": "WF-20251104-001",
  "checkpoint_type": "CONFERMA_PROCEDIMENTO",
  "data": {
    "procedimento_proposto": {
      "codice": "AUTORIZ_SCARICO_ACQUE",
      "nome": "Autorizzazione Scarico Acque Reflue Industriali",
      "confidence": 0.94
    },
    "normativa_applicabile": ["D.Lgs 152/2006", "L.R. 12/2005"],
    "tempi_previsti": "90 giorni",
    "alternatives": [
      {
        "codice": "AUTORIZ_EMISSIONI",
        "confidence": 0.67
      }
    ]
  },
  "ui_config": {
    "show_alternatives": true,
    "allow_modification": true,
    "require_motivazione": true
  },
  "timeout_seconds": 3600
}
```

**HITL UI Presenta**:
```
┌─────────────────────────────────────────────┐
│  🔍 Verifica Classificazione Procedimento   │
├─────────────────────────────────────────────┤
│                                             │
│  Procedimento Identificato:                 │
│  ✓ AUTORIZ_SCARICO_ACQUE                    │
│    Autorizzazione Scarico Acque Reflue      │
│    Confidence: 94%                          │
│                                             │
│  Normativa Applicabile:                     │
│  • D.Lgs 152/2006 Art. 124                  │
│  • L.R. 12/2005                             │
│                                             │
│  Tempi: 90 giorni (senza silenzio-assenso) │
│                                             │
│  Alternative trovate:                       │
│  ○ AUTORIZ_EMISSIONI (67%)                  │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ ✅ Conferma                          │   │
│  │ ✏️  Modifica                         │   │
│  │ 🔄 Scegli alternativa                │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Utente Conferma**:

**Response** (POST to `/hitl/decisions`):
```json
{
  "decision_id": "DEC-20251104-001",
  "checkpoint_id": "HITL-CHECKPOINT-1",
  "workflow_id": "WF-20251104-001",
  "user_id": "user_123",
  "decision": "APPROVED",
  "modifiche": null,
  "motivazione": "Classificazione corretta, normativa applicabile verificata",
  "timestamp": "2025-11-04T10:35:45Z",
  "processing_time_seconds": 45
}
```

**Se Utente Modifica**:
```json
{
  "decision_id": "DEC-20251104-002",
  "checkpoint_id": "HITL-CHECKPOINT-1",
  "workflow_id": "WF-20251104-001",
  "user_id": "user_123",
  "decision": "MODIFIED",
  "modifiche": {
    "procedimento": {
      "codice": "AUTORIZ_EMISSIONI",
      "motivo": "Richiedente ha specificato emissioni atmosfera"
    }
  },
  "motivazione": "Dalla documentazione integrativa emerge focus su emissioni",
  "timestamp": "2025-11-04T10:38:20Z"
}
```

---

## 🔄 Flusso 2: Interrogazione Stato Workflow

### Frontend → NiFi: Check Status

**Endpoint**: `GET http://localhost:8080/nifi-api/process-groups/{pg-id}/status`

**Headers**:
```http
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "processGroupStatus": {
    "id": "abc-123-def-456",
    "name": "WORKFLOW-WF-20251104-001",
    "statsLastRefreshed": "10:35:50 CET",
    "aggregateSnapshot": {
      "bytesIn": 2048576,
      "bytesOut": 1024000,
      "flowFilesIn": 5,
      "flowFilesOut": 3,
      "flowFilesQueued": 0,
      "bytesQueued": 0,
      "queuedCount": "0",
      "queuedSize": "0 bytes",
      "activeThreadCount": 2,
      "input": "5 (2.0 MB)",
      "output": "3 (1.0 MB)",
      "transferred": "8 / 3.0 MB"
    },
    "processorStatus": [
      {
        "id": "processor-sp01",
        "name": "Call_SP01_EML_Parser",
        "type": "InvokeHTTP",
        "runStatus": "Running",
        "statsLastRefreshed": "10:35:50 CET",
        "aggregateSnapshot": {
          "bytesIn": 2048576,
          "flowFilesIn": 1,
          "bytesOut": 512000,
          "flowFilesOut": 1,
          "taskCount": 1,
          "tasksDurationNanos": 850000000,
          "activeThreadCount": 0
        }
      },
      {
        "id": "processor-sp02",
        "name": "Call_SP02_Doc_Extractor",
        "type": "InvokeHTTP",
        "runStatus": "Running",
        "aggregateSnapshot": {
          "bytesIn": 512000,
          "flowFilesIn": 1,
          "bytesOut": 256000,
          "flowFilesOut": 1,
          "taskCount": 1,
          "tasksDurationNanos": 2450000000
        }
      },
      {
        "id": "processor-sp03",
        "name": "Call_SP03_Classifier",
        "type": "InvokeHTTP",
        "runStatus": "Running",
        "aggregateSnapshot": {
          "bytesIn": 256000,
          "flowFilesIn": 1,
          "bytesOut": 128000,
          "flowFilesOut": 1,
          "taskCount": 1,
          "tasksDurationNanos": 520000000
        }
      },
      {
        "id": "processor-hitl-wait",
        "name": "Wait_HITL_Decision",
        "type": "Wait",
        "runStatus": "Running",
        "aggregateSnapshot": {
          "activeThreadCount": 1,
          "flowFilesQueued": 1,
          "bytesQueued": 128000
        }
      }
    ]
  }
}
```

---

## 🔄 Flusso 3: Audit Trail Query

### Frontend → Database: Recupera Audit

**Endpoint**: Query diretta a PostgreSQL tramite backend API

**SQL Query**:
```sql
SELECT 
    workflow_id,
    step_name,
    status,
    duration_ms,
    timestamp_start,
    timestamp_end,
    input_payload,
    output_payload,
    error_message
FROM workflow_executions
WHERE workflow_id = 'WF-20251104-001'
ORDER BY timestamp_start ASC;
```

**Response**:
```json
{
  "workflow_id": "WF-20251104-001",
  "status": "IN_PROGRESS",
  "started_at": "2025-11-04T10:30:05Z",
  "current_step": "HITL_CHECKPOINT_1",
  "steps": [
    {
      "step_id": "STEP-001",
      "step_name": "SP01_PARSE_EMAIL",
      "status": "COMPLETED",
      "timestamp_start": "2025-11-04T10:30:05Z",
      "timestamp_end": "2025-11-04T10:30:06Z",
      "duration_ms": 850,
      "input_size_bytes": 2048576,
      "output_size_bytes": 512000,
      "error_message": null
    },
    {
      "step_id": "STEP-002",
      "step_name": "SP02_EXTRACT_DOCUMENTS",
      "status": "COMPLETED",
      "timestamp_start": "2025-11-04T10:30:06Z",
      "timestamp_end": "2025-11-04T10:30:09Z",
      "duration_ms": 2450,
      "input_size_bytes": 512000,
      "output_size_bytes": 256000,
      "metadata": {
        "documents_extracted": 1,
        "entities_found": 4,
        "ocr_used": false
      }
    },
    {
      "step_id": "STEP-003",
      "step_name": "SP03_CLASSIFY_PROCEDURE",
      "status": "COMPLETED",
      "timestamp_start": "2025-11-04T10:30:09Z",
      "timestamp_end": "2025-11-04T10:30:10Z",
      "duration_ms": 520,
      "metadata": {
        "confidence": 0.94,
        "procedimento": "AUTORIZ_SCARICO_ACQUE"
      }
    },
    {
      "step_id": "STEP-004",
      "step_name": "HITL_CHECKPOINT_1",
      "status": "WAITING",
      "timestamp_start": "2025-11-04T10:30:10Z",
      "timeout_at": "2025-11-04T11:30:10Z",
      "metadata": {
        "checkpoint_type": "CONFERMA_PROCEDIMENTO",
        "waiting_for_user": "user_123"
      }
    }
  ],
  "total_duration_ms": 3820,
  "progress_percentage": 40
}
```

---

## 📊 Monitoring e Metrics

### Prometheus Metrics Esposte

Ogni microservizio espone metriche su `/metrics`:

**Esempio SP01 Metrics**:
```
# HELP sp01_requests_total Total number of requests processed
# TYPE sp01_requests_total counter
sp01_requests_total{method="POST",endpoint="/parse-email",status="200"} 1234

# HELP sp01_request_duration_seconds Request duration in seconds
# TYPE sp01_request_duration_seconds histogram
sp01_request_duration_seconds_bucket{le="0.5"} 980
sp01_request_duration_seconds_bucket{le="1.0"} 1180
sp01_request_duration_seconds_bucket{le="2.0"} 1230
sp01_request_duration_seconds_sum 1050.23
sp01_request_duration_seconds_count 1234

# HELP sp01_emails_parsed_total Total emails successfully parsed
# TYPE sp01_emails_parsed_total counter
sp01_emails_parsed_total 1234

# HELP sp01_attachments_extracted_total Total attachments extracted
# TYPE sp01_attachments_extracted_total counter
sp01_attachments_extracted_total 3456

# HELP sp01_errors_total Total errors encountered
# TYPE sp01_errors_total counter
sp01_errors_total{error_type="INVALID_EML_FORMAT"} 12
sp01_errors_total{error_type="SIGNATURE_VERIFICATION_FAILED"} 3
```

---

## 🐛 Error Handling e Retry

### Strategia di Retry in NiFi

Ogni processor `InvokeHTTP` ha configurazione retry:

```yaml
Processor: Call_SP01_Microservice
Properties:
  - Remote URL: http://sp01:9091/parse-email
  - HTTP Method: POST
  - Connection Timeout: 5 sec
  - Read Timeout: 30 sec
  
Retry Configuration:
  - Retry Count: 3
  - Penalty Duration: 5 sec
  - Yield Duration: 10 sec
  - Backoff Strategy: Exponential (2^n seconds)
```

### Circuit Breaker Pattern

```mermaid
stateDiagram-v2
    [*] --> Closed: Inizialmente chiuso
    Closed --> Open: Errori > Threshold (5 in 1 min)
    Open --> HalfOpen: Dopo timeout (30 sec)
    HalfOpen --> Closed: Request OK
    HalfOpen --> Open: Request Failed
    Open --> [*]: Fallback Strategy
```

### Esempio Fallback Response

Quando SP03 non risponde dopo 3 retry:

```json
{
  "error": true,
  "error_code": "SERVICE_UNAVAILABLE",
  "service": "SP03_PROCEDURAL_CLASSIFIER",
  "message": "Servizio temporaneamente non disponibile",
  "retry_count": 3,
  "circuit_breaker_status": "OPEN",
  "fallback_applied": true,
  "fallback_data": {
    "procedimento": "MANUALE",
    "confidence": 0.0,
    "message": "Richiesta intervento manuale operatore"
  },
  "next_retry_available_at": "2025-11-04T10:35:40Z"
}
```

---

## 🔐 Security e Autenticazione

### JWT Token Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant AUTH as Auth Service
    participant NiFi as NiFi
    
    U->>FE: Login (username/password)
    FE->>AUTH: POST /auth/login
    AUTH->>AUTH: Validate credentials
    AUTH-->>FE: {access_token, refresh_token}
    FE->>FE: Store tokens in sessionStorage
    
    U->>FE: Request workflow
    FE->>NiFi: POST /contentListener<br/>Header: Authorization Bearer {token}
    NiFi->>NiFi: Validate JWT signature
    NiFi->>NiFi: Check token expiration
    NiFi->>NiFi: Extract user_id from claims
    NiFi-->>FE: {workflow_id, ...}
```

### JWT Payload Example

```json
{
  "sub": "user_123",
  "name": "Mario Rossi",
  "email": "mario.rossi@comune.it",
  "role": "RESPONSABILE_UFFICIO",
  "permissions": [
    "CREATE_WORKFLOW",
    "APPROVE_DOCUMENT",
    "VIEW_AUDIT"
  ],
  "iat": 1699099200,
  "exp": 1699102800,
  "iss": "provvedimento-assistant-auth"
}
```

---

## 📈 Performance Benchmarks

### Tempi Medi End-to-End

| Scenario | Tempo Medio | P95 | P99 | SLA Target |
|----------|-------------|-----|-----|------------|
| Email parsing (SP01) | 850ms | 1.2s | 2.1s | <2s |
| Document extraction (SP02) | 2.5s | 4.2s | 6.8s | <5s |
| Procedural classification (SP03) | 520ms | 850ms | 1.5s | <2s |
| Knowledge retrieval (SP04) | 1.2s | 2.1s | 3.5s | <3s |
| **Workflow completo** (senza HITL) | **44s** | **68s** | **89s** | **<60s** |
| **Workflow completo** (con HITL) | **~15 min** | **~25 min** | **~45 min** | **<1h** |

### Throughput

| Servizio | Requests/sec (media) | Max RPS | Bottleneck |
|----------|---------------------|---------|------------|
| SP01 | 50 | 120 | Parsing attachments |
| SP02 | 20 | 45 | OCR processing |
| SP03 | 80 | 200 | DistilBERT inference |
| SP04 | 100 | 300 | Vector search |
| NiFi Orchestrator | 100 | 500 | FlowFile queuing |

---

## 🧪 Test di Integrazione

### Script Test Completo

```bash
#!/bin/bash
# test-integration-e2e.sh

echo "🧪 Test Integrazione End-to-End"
echo "================================"

WORKFLOW_ID=""
BASE_URL="http://localhost:8080"

# 1. Avvia workflow
echo "1️⃣ Avvio workflow..."
RESPONSE=$(curl -s -X POST ${BASE_URL}/contentListener/fascicolo \
  -H "Content-Type: application/json" \
  -d @test-data/sample-fascicolo.json)

WORKFLOW_ID=$(echo $RESPONSE | jq -r '.workflow_id')
echo "   Workflow ID: ${WORKFLOW_ID}"

# 2. Monitora progresso
echo "2️⃣ Monitoraggio progresso..."
for i in {1..10}; do
  sleep 5
  STATUS=$(curl -s "${BASE_URL}/nifi-api/workflow/${WORKFLOW_ID}/status" | jq -r '.status')
  echo "   [${i}] Status: ${STATUS}"
  
  if [ "$STATUS" = "WAITING_HITL" ]; then
    echo "   ⏸️  Workflow in attesa HITL"
    break
  fi
done

# 3. Simula decisione HITL
echo "3️⃣ Simulazione decisione HITL..."
curl -s -X POST http://localhost:8000/hitl/decisions \
  -H "Content-Type: application/json" \
  -d "{
    \"checkpoint_id\": \"HITL-CHECKPOINT-1\",
    \"workflow_id\": \"${WORKFLOW_ID}\",
    \"decision\": \"APPROVED\",
    \"user_id\": \"test_user\"
  }" | jq .

# 4. Attendi completamento
echo "4️⃣ Attesa completamento workflow..."
for i in {1..20}; do
  sleep 5
  STATUS=$(curl -s "${BASE_URL}/nifi-api/workflow/${WORKFLOW_ID}/status" | jq -r '.status')
  echo "   [${i}] Status: ${STATUS}"
  
  if [ "$STATUS" = "COMPLETED" ]; then
    echo "   ✅ Workflow completato!"
    break
  fi
done

# 5. Recupera audit trail
echo "5️⃣ Recupero audit trail..."
curl -s "${BASE_URL}/api/audit/${WORKFLOW_ID}" | jq '.steps[] | {step_name, status, duration_ms}'

echo ""
echo "✅ Test completato!"
```

---

## 📚 Conclusioni

### Punti Chiave

1. **Orchestrazione Centralizzata**: Apache NiFi coordina tutti i microservizi
2. **Comunicazione HTTP REST**: Tutti i servizi espongono API REST standard
3. **Payload JSON Strutturati**: Dati ben definiti per ogni step
4. **Human in the Loop**: Checkpoints decisional integrati nel workflow
5. **Audit Trail Completo**: Tracciabilità end-to-end in PostgreSQL
6. **Error Handling Robusto**: Retry, circuit breaker, fallback
7. **Monitoring Real-time**: Prometheus metrics + NiFi provenance

### Architettura Completa

```
┌─────────────────────────────────────────────────────────┐
│                    LAYER 1: Frontend                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Streamlit  │  │  HITL UI     │  │  Dashboard   │  │
│  │   Port 8501  │  │  Port 8000   │  │  Port 8502   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼ HTTP REST
┌─────────────────────────────────────────────────────────┐
│              LAYER 2: Workflow Orchestration            │
│  ┌───────────────────────────────────────────────────┐  │
│  │            Apache NiFi (Port 8080)                │  │
│  │  ┌────────────────────────────────────────────┐   │  │
│  │  │ Process Groups: SP01-SP11 + HITL Manager  │   │  │
│  │  └────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼ HTTP POST
┌─────────────────────────────────────────────────────────┐
│                LAYER 3: Microservizi AI                 │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐     │
│  │ SP01 │  │ SP02 │  │ SP03 │  │ SP04 │  │ ...  │     │
│  │ 9091 │  │ 9092 │  │ 9093 │  │ 9094 │  │      │     │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼ SQL / Cache
┌─────────────────────────────────────────────────────────┐
│                   LAYER 4: Data Layer                   │
│  ┌────────────┐  ┌──────────┐  ┌──────────┐            │
│  │ PostgreSQL │  │  Redis   │  │  MinIO   │            │
│  │ Port 5432  │  │ Port 6379│  │ Port 9000│            │
│  └────────────┘  └──────────┘  └──────────┘            │
└─────────────────────────────────────────────────────────┘
```

---

**Documento creato**: 4 novembre 2025  
**Versione**: 1.0  
**Autore**: GitHub Copilot + Interzen Team
