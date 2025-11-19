# Infrastructure

Questa directory contiene tutti i file relativi all'infrastruttura e al deployment del progetto ZenIA.

## 📚 Documentazione

- 📖 **README.md** (questo file) - Panoramica infrastruttura
- 📁 **nifi-workflows/README.md** - Workflow Apache NiFi e configurazione
- 🔧 **nifi-workflows/services/README.md** - Stato microservizi
- 🐳 **nifi-workflows/docker-compose.yml** - Configurazione Docker

## 📁 Struttura

```
infrastructure/
└── nifi-workflows/          # Orchestrazione Apache NiFi e Docker
    ├── docker-compose.yml   # Configurazione Docker Compose
    ├── services/            # Microservizi dedicati
    │   ├── sp01/           # EML Parser & Email Intelligence
    │   ├── sp02/           # Document Extractor & Attachment Classifier
    │   ├── sp03/           # Procedural Classifier Service
    │   ├── sp04/           # Knowledge Base Service (RAG)
    │   ├── sp07/           # Content Classifier Service
    │   └── hitl/           # Human-in-the-Loop Manager
    ├── nifi-templates/     # Template NiFi (.xml)
    ├── nifi-extensions/    # Custom NiFi processors
    ├── deploy.sh           # Script deployment (Linux/macOS)
    ├── deploy.ps1          # Script deployment (Windows)
    ├── test-builds.sh      # Test build Docker
    └── .env.example        # Template variabili ambiente
    
NOTA: SP05, SP06, SP08, SP09, SP11 sono implementati come Process Groups in Apache NiFi,
      non come microservizi separati. SP10 (Dashboard) è pianificato per implementazione futura.
```

## 🚀 Deployment

### Quick Start

1. **Configura le variabili d'ambiente**:
   ```bash
   cd infrastructure/nifi-workflows
   cp .env.example .env
   # Modifica .env con le tue API keys
   ```

2. **Avvia tutto (Linux/macOS)**:
   ```bash
   ./deploy.sh
   ```

3. **Avvia tutto (Windows)**:
   ```powershell
   .\deploy.ps1
   ```

### Test Build

Per testare solo i build Docker senza avviare i servizi:
```bash
cd infrastructure/nifi-workflows
./test-all-services.sh
```

## 🔧 Servizi

| Servizio | Porta | Status | Descrizione |
|----------|-------|--------|-------------|
| **Apache NiFi** | **8443/8080** | **✅** | **Orchestratore workflow (HTTPS/HTTP)** |
| PostgreSQL | 5432 | ✅ | Database principale (con pgvector) |
| Redis | 6379 | ✅ | Cache e sessioni |
| ZooKeeper | 2181 | ✅ | Coordinazione NiFi cluster |
| Neo4j | 7474/7687 | ✅ | Knowledge graph |
| MinIO | 9000/9001 | ✅ | Object storage |
| **Microservizi Dedicati** | | | |
| **SP01 EML Parser** | **5001** | **✅** | **Analisi email PEC in arrivo (Python FastAPI)** |
| **SP02 Document Extractor** | **5002** | **✅** | **Estrazione testo da allegati + OCR (Python FastAPI)** |
| **SP03 Procedural Classifier** | **5003** | **✅** | **Classificazione procedimenti (Python FastAPI)** |
| **SP04 Knowledge Base** | **5004** | **✅** | **RAG + Vector Search (Python FastAPI)** |
| **SP07 Content Classifier** | **5007** | **⚠️ Opzionale** | **Classificazione documenti (Python FastAPI)** |
| **HITL Manager** | **5009** | **✅** | **Human-in-the-Loop interface (Python FastAPI)** |
| **Process Groups NiFi** | | | |
| SP05 Template Engine | - | ✅ NiFi Process Group | Generazione template con Groq API |
| SP06 Validator | - | ✅ NiFi Process Group | Validazione semantica e conformità |
| SP08 Quality Checker | - | ✅ NiFi Process Group | Controllo qualità linguistica |
| SP09 Workflow Engine | - | ✅ Apache NiFi Core | Orchestrazione workflow completa |
| SP10 Dashboard | - | 🔵 Pianificato | Dashboard analytics e monitoring |
| SP11 Security & Audit | - | ✅ NiFi Process Group | Audit trail e sicurezza |

## ⚠️ Note Importanti

### Stato Attuale Implementazione

#### Microservizi (cartelle in `services/`)
- **SP01 EML Parser** (`services/sp01/`): Analisi email PEC e estrazione metadata
- **SP02 Document Extractor** (`services/sp02/`): Estrazione testo da PDF/immagini con OCR
- **SP03 Procedural Classifier** (`services/sp03/`): Classificazione tipo procedimento amministrativo
- **SP04 Knowledge Base** (`services/sp04/`): RAG + Vector Search + Neo4j
- **SP07 Content Classifier** (`services/sp07/`): Classificazione documenti (opzionale, commentato)
- **HITL Manager** (`services/hitl/`): Interfaccia Human-in-the-Loop

#### Process Groups Apache NiFi
- **SP05 Template Engine**: Orchestrato in NiFi (InvokeHTTP → Groq API)
- **SP06 Validator**: Orchestrato in NiFi (rule engine + validazioni)
- **SP08 Quality Checker**: Orchestrato in NiFi (LanguageTool + NLP)
- **SP09 Workflow Engine**: Apache NiFi Core (orchestrazione completa)
- **SP11 Security Audit**: Orchestrato in NiFi (JWT + audit logging)

### Container Attivi
Attualmente vengono avviati **11 containers**:
1. Apache NiFi orchestrator
2. PostgreSQL (con pgvector)
3. Redis
4. ZooKeeper (per NiFi clustering)
5. Neo4j
6. MinIO
7. SP01 EML Parser
8. SP02 Document Extractor
9. SP03 Procedural Classifier
10. SP04 Knowledge Base
11. HITL Manager

## 🎯 Vantaggi Apache NiFi

### Rispetto a n8n
- ✅ **100% Open Source** - nessun costo di licenza
- ✅ **Enterprise-grade** - audit trail automatico e data lineage
- ✅ **Scalabilità** - clustering nativo per alta disponibilità
- ✅ **Data Provenance** - tracciamento completo di ogni dato
- ✅ **Backpressure** - gestione automatica del carico
- ✅ **Conforme PA** - audit e governance integrati

### Funzionalità Chiave
- **Flow-based programming** visuale
- **Retry automatici** e circuit breaker
- **Data lineage** completo (importante per PA)
- **Versioning** dei flow integrato
- **Monitoring** real-time integrato

## 📖 Documentazione

- [Apache NiFi Documentation](https://nifi.apache.org/docs.html)
- [NiFi User Guide](https://nifi.apache.org/docs/nifi-docs/html/user-guide.html)
- [NiFi REST API](https://nifi.apache.org/docs/nifi-docs/rest-api/index.html)
