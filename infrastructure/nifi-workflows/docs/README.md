# Apache NiFi Workflows - Generazione Atti Amministrativi

## 📋 Panoramica

Questa cartella contiene l'infrastruttura Apache NiFi per l'intero sistema di generazione automatica di atti amministrativi, composta da:

- **Process Groups per i sottoprogetti** (SP00-SP08)
- **Controller Services** per connessioni esterne
- **Template NiFi** riutilizzabili
- **Custom Processors** (opzionale)

## 📁 Struttura

```
nifi-workflows/
├── docker-compose.yml          # Configurazione Docker
├── .env.example                # Template variabili ambiente
├── deploy.sh                   # Script deployment Unix
├── deploy.ps1                  # Script deployment Windows
├── setup-nifi-workflows.sh     # Configurazione automatica workflow
├── test-sp01-endpoint.sh       # Test automatico SP01
├── nifi-templates/             # Template NiFi (.xml)
│   ├── SP03-Procedural-Classifier.xml
│   ├── SP05-Template-Engine.xml
│   ├── SP06-Validator.xml
│   ├── SP07-Content-Classifier.xml
│   ├── SP08-Quality-Checker.xml
│   ├── SP11-Security-Audit.xml
│   └── WORKFLOW-GLOBALE-Orchestrator.xml
├── nifi-extensions/            # Custom processors (NAR files)
└── services/                   # Microservizi esterni
    ├── sp01/                   # EML Parser & Email Intelligence
    ├── sp02/                   # Document Extractor & Attachment Classifier
    ├── sp03/                   # Procedural Classifier
    ├── sp04/                   # Knowledge Base (RAG)
    ├── sp07/                   # Content Classifier (opzionale)
    └── hitl/                   # Human-in-the-Loop
```

## 🔧 Script di Automazione

### `deploy.sh` - Deployment Completo
Script principale che automatizza l'intero deployment:

1. **Verifica prerequisiti** (Docker, Docker Compose)
2. **Configurazione ambiente** (.env file)
3. **Avvio infrastruttura** (PostgreSQL, Redis, ZooKeeper, Neo4j, MinIO)
4. **Setup database** (tabelle e dati iniziali, incluso versioning registry)
5. **Avvio NiFi** con driver JDBC PostgreSQL
6. **Configurazione automatica workflow** (`setup-nifi-workflows.sh`)
7. **Avvio microservizi** (SP01-SP04, HITL, Gotenberg)

### `setup-nifi-workflows.sh` - Configurazione Workflow
Script che configura automaticamente i workflow NiFi:

- **Importa templates** dal NiFi Registry con versioning
- **Istanzia process groups** nel canvas
- **Crea controller services** (PostgreSQL + Redis)
- **Abilita controller services**
- **Avvia processors** in tutti i process groups

### `test-sp01-endpoint.sh` - Test SP01
Script di test per l'endpoint SP01 EML Parser:

- **Test JSON semplice**
- **Test contenuto EML-like**
- **Report risultati** con codici HTTP

### Script di Build Individuali
- `build-sp01-via-api.py` - Costruisce SP01 via API (Infrastructure as Code)
- `build-sp02-via-api.py` - Costruisce SP02 via API
- `build-sp03-via-api.py` - Costruisce SP03 via API
- `build-sp04-via-api.py` - Costruisce SP04 via API
- `build-sp05-via-api.py` - Costruisce SP05 via API
- `build-sp06-via-api.py` - Costruisce SP06 via API
- `build-sp07-via-api.py` - Costruisce SP07 via API
- `build-sp08-via-api.py` - Costruisce SP08 via API
- `build-sp11-via-api.py` - Costruisce SP11 via API

## 📊 Workflow Configurati Automaticamente

Dopo il deploy, questi workflow sono attivi:

### SP01 - EML Parser
- **Endpoint**: `http://localhost:9091/`
- **Funzione**: Parsing email EML per provvedimenti
- **Controller Services**: PostgreSQL + Redis
- **Output**: Success/Failure ports

### Controller Services
- **PostgreSQL Connection Pool**: Connessione database provvedimenti
- **Redis Cache Pool**: Cache distribuita per sessioni utente

## 📝 Versioning del NiFi Registry

Il sistema è configurato con **versioning abilitato** per il NiFi Registry:

### Funzionalità Abilitate
- ✅ **Tracciamento versioni** dei flow templates
- ✅ **Rollback** a versioni precedenti
- ✅ **Audit trail** delle modifiche
- ✅ **Confronto** tra versioni
- ✅ **Metadata versioning** (parametri, contesti, encoding)

### Database Versioning
- **Database separato**: `nifi_registry_versioning`
- **Tabelle dedicate**: flow_snapshot_metadata, flow_snapshot_content
- **Storage persistente**: Versioni salvate automaticamente

### Utilizzo Versioning
```bash
# Accedi al NiFi Registry UI
open http://localhost:18080/nifi-registry

# Nella UI puoi:
# - Visualizzare cronologia versioni per ogni flow
# - Confrontare versioni differenti
# - Rollback a versioni precedenti
# - Vedere chi ha fatto modifiche e quando
```

### Configurazione Tecnica
```yaml
# Nel docker-compose.yml
nifi-registry:
  environment:
    - NIFI_REGISTRY_VERSIONING_ENABLED=true
    - NIFI_REGISTRY_VERSIONING_DB_URL=jdbc:postgresql://postgres:5432/nifi_registry_versioning
```

## 🔍 Monitoraggio e Debug

```bash
# Logs NiFi
docker-compose logs -f nifi

# Logs SP01 microservizio
docker-compose logs -f sp01-eml-parser

# Test endpoint SP01
./test-sp01-endpoint.sh

# Accesso shell NiFi
docker exec -it nifi-orchestrator bash

# Accesso NiFi UI
open http://localhost:8080/nifi
```

## 🚀 Quick Start

### 1. Prerequisiti

- Docker Desktop installato
- Almeno 8GB RAM disponibile
- Groq API Key (gratuita su https://console.groq.com)

### 2. Configurazione

```bash
# Copia template variabili
cp .env.example .env

# Modifica .env con la tua Groq API Key
nano .env
```

### 3. Deploy Automatico

```bash
# Deploy completo con configurazione automatica
./deploy.sh

# Questo script fa automaticamente:
# ✅ Verifica prerequisiti
# ✅ Avvia tutti i servizi (PostgreSQL, Redis, NiFi, etc.)
# ✅ Importa templates dal NiFi Registry
# ✅ Istanzia i process groups
# ✅ Configura controller services (PostgreSQL + Redis)
# ✅ Abilita controller services
# ✅ Avvia tutti i processors
# ✅ SP01 EML Parser attivo su porta 9091
```

### 4. Test Immediato

```bash
# Test automatico SP01 endpoint
./test-sp01-endpoint.sh

# Test manuale
curl -X POST http://localhost:9091/ \
     -H "Content-Type: application/json" \
     -d '{"test": "Hello SP01"}'
```

### 4. Accesso NiFi

Dopo circa 2 minuti, accedi a:
- **URL**: https://localhost:8443/nifi
- **Username**: admin
- **Password**: (da file .env)

⚠️ **Nota**: Il certificato SSL è self-signed, accetta l'eccezione nel browser.

## 🎯 Architettura Process Groups

### Process Groups Principali

| Process Group | Descrizione | Input | Output |
|--------------|-------------|-------|--------|
| **SP03 - Procedural Classifier** | Classifica procedimento amministrativo | Istanza utente | Tipo procedimento + normativa |
| **SP05 - Template Engine** | Genera documento con Groq AI | Metadati + contesto | Bozza documento |
| **SP06 - Validator** | Valida semantica e conformità | Documento bozza | Report validazione |
| **SP07 - Content Classifier** | Classifica tipo documento | Testo documento | Categoria + metadata |
| **SP08 - Quality Checker** | Controllo qualità linguistica | Documento finale | Report qualità |
| **SP11 - Security Audit** | Audit trail e sicurezza | Ogni evento | Log immutabile |
| **WORKFLOW-GLOBALE** | Orchestratore completo | Richiesta utente | Documento pubblicato |

### Flusso Orchestratore Globale

```
┌─────────────────────────────────────────────────┐
│         WORKFLOW GLOBALE ORCHESTRATOR            │
│  ┌───────────────────────────────────────────┐  │
│  │  1. InvokeHTTP → SP11 Auth                │  │
│  │  2. RouteOnAttribute → Check JWT          │  │
│  │  3. InvokeHTTP → SP01 Parse Email         │  │
│  │  4. InvokeHTTP → SP02 Extract Attachments │  │
│  │  5. InvokeHTTP → SP03 Classify Procedure  │  │
│  │  6. InvokeHTTP → SP07 Classify Document   │  │
│  │  7. InvokeHTTP → SP04 Retrieve Context    │  │
│  │  8. ExecuteScript → HITL Checkpoint #1    │  │
│  │  9. InvokeHTTP → SP05 Generate Template   │  │
│  │ 10. ExecuteScript → HITL Checkpoint #2    │  │
│  │ 11. InvokeHTTP → SP06 Validate            │  │
│  │ 12. RouteOnAttribute → Check Errors       │  │
│  │ 13. InvokeHTTP → SP08 Quality Check       │  │
│  │ 14. ExecuteScript → HITL Checkpoint #3    │  │
│  │ 15. InvokeHTTP → Sistema Protocollo       │  │
│  │ 16. InvokeHTTP → Firma Digitale           │  │
│  │ 17. UpdateAttribute → Log Provenance      │  │
│  │ 18. InvokeHTTP → SP11 Audit Log           │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 🔧 Configurazione Controller Services

Dopo l'importazione dei template, configura i Controller Services:

### 1. DBCPConnectionPool (PostgreSQL)

```
Name: PostgreSQL-Connection-Pool
Database Connection URL: jdbc:postgresql://postgres:5432/provvedimenti
Database Driver Class: org.postgresql.Driver
Database User: postgres
Password: (da .env)
Max Wait Time: 500 ms
Max Total Connections: 50
```

### 2. RedisConnectionPoolService

```
Name: Redis-Cache-Pool
Connection String: redis:6379
Database Index: 0
Pool Size: 20
```

### 3. StandardHttpContextMap (per HITL)

```
Name: HITL-HTTP-Context
Request Expiration: 30 seconds
```

## 📝 Importazione Template

### Via UI

1. Accedi a NiFi: https://localhost:8443/nifi
2. Trascina un **Process Group** sul canvas
3. Click destro → **Upload Template**
4. Seleziona file `.xml` da `nifi-templates/`
5. Trascina il template importato sul canvas
6. Configura i Controller Services
7. Start tutti i processor

### Creazione Manual Process Group (SP01 esempio)

Se non hai i template `.xml`, crea manualmente:

#### SP05 - Template Engine

1. **GenerateFlowFile** → Crea input
2. **InvokeHTTP** → POST a `http://groq-api/chat/completions`
   - HTTP Method: POST
   - Remote URL: `${groq.api.url}`
   - Headers: `Authorization: Bearer ${groq.api.key}`
3. **EvaluateJsonPath** → Estrai risposta
4. **UpdateAttribute** → Aggiungi metadata
5. **PutDatabaseRecord** → Salva in PostgreSQL

## 📊 Monitoring e Provenance

### Data Provenance

NiFi traccia automaticamente **ogni flowfile**:

1. Menu → **Data Provenance**
2. Filtra per Event Type, Component, Time
3. **Lineage Graph**: Visualizza percorso completo

### Metriche Real-time

- **Throughput**: FlowFiles/sec
- **Backpressure**: Code in attesa
- **Task Duration**: Tempo medio
- **Error Rate**: % fallimenti

## 🐛 Troubleshooting

### NiFi non parte

```bash
docker logs -f nifi-orchestrator
docker stats nifi-orchestrator
docker-compose restart nifi
```

### Processor in errore

1. Click destro → **View Configuration**
2. Tab **Settings** → **Automatically Retry**
3. **Bulletin Board** per errori

### FlowFile bloccati

1. Click destro su connection → **List Queue**
2. **Empty Queue** o **Drain**

## 🔐 Security

- **HTTPS**: Certificati validi in produzione
- **Authentication**: LDAP/OIDC in `nifi.properties`
- **Encrypt Config**: `nifi-toolkit encrypt-config.sh`

## 📈 Performance Tuning

```yaml
environment:
  - NIFI_JVM_HEAP_INIT=4g
  - NIFI_JVM_HEAP_MAX=8g
```

## 🆘 Support

- [Apache NiFi Docs](https://nifi.apache.org/docs.html)
- [Expression Language Guide](https://nifi.apache.org/docs/nifi-docs/html/expression-language-guide.html)

---

**Versione**: 1.0.0  
**Orchestrator**: Apache NiFi
