# Services - Status Microservizi

> **Architettura Apache NiFi**: Workflow orchestrati tramite NiFi Process Groups, microservizi esterni per funzionalità specifiche

## 📊 Stato Servizi (Aggiornato: Novembre 2025)

| Servizio | Stato | Implementazione | Container | Note |
|----------|-------|-----------------|-----------|------|
| **SP01** - EML Parser | ✅ MICROSERVIZIO | ✅ API FastAPI | ✅ sp01-eml-parser | Parsing email PEC in arrivo |
| **SP02** - Document Extractor | ✅ MICROSERVIZIO | ✅ API FastAPI | ✅ sp02-document-extractor | Estrazione testo allegati + OCR |
| **SP03** - Procedural Classifier | ✅ MICROSERVIZIO | ✅ API FastAPI | ✅ sp03-procedural-classifier | Classificazione procedimenti amministrativi |
| **SP04** - Knowledge Base | 🚧 MICROSERVIZIO | 🔶 API FastAPI | ✅ sp04-knowledge-base | RAG + FAISS (da completare) |
| **SP05** - Template Engine | ✅ NIFI PROCESS GROUP | ✅ NiFi InvokeHTTP + Groq API | ✅ Integrato in NiFi | Template rendering con Groq |
| **SP06** - Validator | ✅ NIFI PROCESS GROUP | ✅ NiFi RouteOnAttribute + Groq | ✅ Integrato in NiFi | Validazione semantica e business rules |
| **SP07** - Content Classifier | ⚠️ MICROSERVIZIO | 🔶 API FastAPI | ⚠️ Opzionale | Classificazione documenti (può usare Groq in NiFi) |
| **SP08** - Quality Checker | ✅ NIFI PROCESS GROUP | ✅ NiFi InvokeHTTP + LanguageTool | ✅ Integrato in NiFi | Quality & readability check |
| **SP09** - Workflow Engine | ✅ APACHE NIFI | ✅ NiFi Core | ✅ nifi | Orchestrazione workflow completa |
| **SP10** - Dashboard | 🔵 TODO | - | - | Dashboard analytics (futuro) |
| **SP11** - Security Audit | ✅ NIFI PROVENANCE | ✅ NiFi Provenance + JWT | ✅ Integrato in NiFi | Audit trail completo con data lineage |

### Servizi Supporto

| Servizio | Stato | Container | Utilizzo |
|----------|-------|-----------|----------|
| **FAISS Vector Search** | ⚠️ IN IMPLEMENTAZIONE | ⚠️ Opzionale | Per SP03 Knowledge Base |
| **ZooKeeper** | ✅ ATTIVO | ✅ zookeeper | Coordinazione cluster NiFi |

---

## 🚀 Architettura Attuale

### Infrastruttura Core (11 containers)
1. **Apache NiFi** - Workflow orchestration engine (porta 8443 HTTPS, 8080 HTTP)
2. **ZooKeeper** - Coordinazione cluster NiFi (porta 2181)
3. **PostgreSQL** - Database principale + pgvector (porta 5432)
4. **Redis** - Cache layer (porta 6379)
5. **Neo4j** - Knowledge graph (porte 7474/7687)
6. **MinIO** - Object storage (porte 9000/9001)
7. **SP01 EML Parser** - API FastAPI (porta 5001)
8. **SP02 Document Extractor** - API FastAPI (porta 5002)
9. **SP03 Procedural Classifier** - API FastAPI (porta 5003)
10. **SP04 Knowledge Base** - API FastAPI (porta 5004)
11. **HITL Manager** - Human-in-the-Loop (porta 5009)

### NiFi Process Groups (5 servizi implementati come Process Groups)
- `SP05-Template-Engine` - Generazione documenti con Groq (InvokeHTTP processors)
- `SP06-Validator` - Validazione multi-dimensionale (RouteOnAttribute + EvaluateJsonPath)
- `SP08-Quality-Checker` - Quality & readability check (InvokeHTTP + LanguageTool API)
- `SP09-Workflow-Engine` - Apache NiFi Core (orchestrazione completa)
- `SP11-Security-Audit` - Audit trail con NiFi Provenance (data lineage completo)

### Microservizi Dedicati (5 microservizi esterni)
- `sp01-eml-parser` (Python/FastAPI) - Parsing email PEC in arrivo
- `sp02-document-extractor` (Python/FastAPI) - Estrazione testo da allegati con OCR
- `sp03-procedural-classifier` (Python/FastAPI) - Classificazione procedimenti amministrativi
- `sp04-knowledge-base` (Python/FastAPI) - RAG + FAISS per knowledge retrieval
- `sp07-content-classifier` (Python/FastAPI) - Classificazione documenti (opzionale, Groq alternativa in NiFi)

---

## 📁 Struttura Cartelle

```
services/
├── README.md (questo file)
│
├── sp01/ ✅ MICROSERVIZIO EML PARSER
│   ├── app.py          # FastAPI per parsing email PEC
│   ├── Dockerfile      # Container configuration
│   ├── requirements.txt
│   └── README.md
│
├── sp02/ ✅ MICROSERVIZIO DOCUMENT EXTRACTOR
│   ├── app.py          # FastAPI estrazione testo + OCR
│   ├── Dockerfile      # Container configuration
│   ├── requirements.txt
│   └── README.md
│
├── sp03/ ✅ MICROSERVIZIO PROCEDURAL CLASSIFIER
│   ├── app.py          # FastAPI classificazione procedimenti
│   ├── Dockerfile      # Container configuration
│   ├── requirements.txt
│   └── README.md
│
├── sp04/ 🚧 MICROSERVIZIO KNOWLEDGE BASE
│   ├── app.py          # FastAPI con RAG + FAISS
│   ├── Dockerfile      # Container configuration
│   ├── requirements.txt
│   └── README.md
│
├── sp07/ ⚠️ MICROSERVIZIO OPZIONALE
│   ├── app.py          # FastAPI classificazione documenti
│   ├── Dockerfile      # Container configuration
│   ├── requirements.txt
│   └── README.md
│
└── hitl/ ✅ MICROSERVIZIO HITL
    ├── app.py          # FastAPI Human-in-the-Loop Manager
    ├── Dockerfile      # Container configuration
    ├── requirements.txt
    └── README.md

TOTALE: 6 microservizi in questa cartella
```

### ❌ Cosa NON Esiste in `services/`

Le seguenti cartelle **NON ESISTONO** perché implementate come NiFi Process Groups:

- ❌ `sp05/` - Template Engine → Implementato come NiFi Process Group (InvokeHTTP + Groq)
- ❌ `sp06/` - Validator → Implementato come NiFi Process Group (RouteOnAttribute + Groq)
- ❌ `sp08/` - Quality Checker → Implementato come NiFi Process Group (InvokeHTTP + LanguageTool)
- ❌ `sp09/` - Workflow Engine → Apache NiFi core
- ❌ `sp10/` - Dashboard → Non ancora implementato
- ❌ `sp11/` - Security Audit → NiFi Provenance + Audit logs

---

## 🔄 Migrazione da n8n ad Apache NiFi

### Vantaggi della Migrazione
- ✅ **Open Source 100%**: Nessun lock-in commerciale (n8n Fair-code)
- ✅ **Enterprise Grade**: Supporto clustering, HA, failover nativo
- ✅ **Data Provenance**: Tracciamento completo data lineage end-to-end
- ✅ **Compliance PA**: Audit trail immutabile per Pubblica Amministrazione
- ✅ **Scalabilità**: Gestione terabyte di dati con performance ottimali
- ✅ **Processori Nativi**: 300+ processori built-in senza custom code

### Consumo Risorse Comparato

| Componente | Memoria | CPU | Note |
|-----------|---------|-----|------|
| **Apache NiFi** | 4-8 GB | 2-4 cores | Richiede JVM, mais più potente |
| **ZooKeeper** | 512 MB - 1 GB | 1 core | Coordinazione cluster |
| **Microservizi (SP03, SP04, HITL)** | 500 MB each | 1 core each | Invariati |

**Totale Nuovo:** ~8 GB RAM, 6-8 cores (vs ~4 GB con n8n ma con funzionalità enterprise superiori)

---

## 🚀 Quick Start

### Avvio Infrastruttura

```bash
cd infrastructure/nifi-workflows

# 1. Copia e configura .env
cp .env.example .env
nano .env  # Configura GROQ_API_KEY, NIFI_USER, NIFI_PASSWORD

# 2. Avvia tutti i servizi
docker-compose up -d postgres redis zookeeper neo4j minio nifi

# 3. Attendi startup NiFi (~90 secondi per JVM)
./deploy.sh

# 4. Accedi NiFi UI
open https://localhost:8443/nifi
```

### Configurazione NiFi (Prima Volta)

1. **Login NiFi**: Usa credenziali da `.env` (NIFI_USER/NIFI_PASSWORD)
2. **Importa Templates**: Upload template XML da `nifi-templates/`
3. **Configura Controller Services**:
   - DBCPConnectionPool → PostgreSQL (postgres:5432/provvedimenti)
   - RedisConnectionPoolService → Redis (redis:6379)
   - StandardHttpContextMap → Per HITL Manager
4. **Avvia Process Groups**: Start WORKFLOW-GLOBALE orchestrator

### Verifica Servizi

```bash
# PostgreSQL
docker exec -it postgres psql -U postgres -c "\l"

# Redis
docker exec -it redis redis-cli ping

# Neo4j
curl http://localhost:7474

# MinIO
open http://localhost:9001  # user: minioadmin / minioadmin

# NiFi
curl -k https://localhost:8443/nifi-api/system-diagnostics

# ZooKeeper
echo ruok | nc localhost 2181  # Should return "imok"
```

### Verifica Microservizi

```bash
# SP01 EML Parser
curl http://localhost:5001/docs

# SP02 Document Extractor
curl http://localhost:5002/docs

# SP03 Procedural Classifier
curl http://localhost:5003/docs

# SP04 Knowledge Base
curl http://localhost:5004/docs

# SP07 Content Classifier (se attivo)
curl http://localhost:5007/docs

# HITL Manager
curl http://localhost:5009/docs
```

---

## 📝 Environment Variables

Copia `.env.example` → `.env` e configura:

```bash
# PostgreSQL
POSTGRES_PASSWORD=yourpassword

# Neo4j
NEO4J_PASSWORD=neo4jpassword

# MinIO
MINIO_USER=minioadmin
MINIO_PASSWORD=minioadmin

# NiFi
NIFI_USER=admin
NIFI_PASSWORD=adminadminadmin
NIFI_SENSITIVE_KEY=nifichangeme  # Min 12 caratteri

# Groq API (obbligatorio per SP01 Template Engine)
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## 🧪 Testing

```bash
# Test build microservizi
./test-builds.sh

# Test tutti i servizi
./test-all-services.sh
```

---

## 📚 Documentazione

- **NiFi UI**: https://localhost:8443/nifi
- **NiFi Provenance**: NiFi UI → Menu → Data Provenance
- **NiFi Templates**: `../nifi-templates/README.md`
- **Custom Processors**: `../nifi-extensions/README.md`
- **Architecture**: `../README.md`

---

## 🔧 Troubleshooting

### NiFi non si avvia
- Verifica memoria disponibile (min 8GB RAM)
- Controlla logs: `docker logs nifi -f`
- Aspetta 90-120 secondi per JVM startup

### ZooKeeper connection failed
- Verifica ZooKeeper running: `docker ps | grep zookeeper`
- Check logs: `docker logs zookeeper -f`
- Restart: `docker-compose restart zookeeper`

### Microservizi non rispondono
- Verifica build: `./test-builds.sh`
- Check logs: `docker logs sp03-knowledge-base -f`
- Rebuild: `docker-compose up -d --build sp03`

---

## 🎯 Prossimi Passi

1. ✅ Completare implementazione SP01 EML Parser
2. ✅ Completare implementazione SP02 Document Extractor
3. ✅ Rinominare SP00 in SP03 Procedural Classifier
4. ⏳ Completare implementazione RAG in SP04
5. ⏳ Implementare SP10 Dashboard (Streamlit + NiFi REST API)
6. ⏳ Creare NiFi templates aggiornati per tutti i Process Groups (SP05, SP06, SP08, SP11)
7. ⏳ Configurare NiFi cluster 3-node per HA
8. ⏳ Implementare monitoring con Prometheus + Grafana
