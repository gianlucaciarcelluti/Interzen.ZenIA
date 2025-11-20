# Indice Documentazione ZenIA

Indice completo della documentazione della piattaforma ZenIA in lingua italiana.

---

## 📚 Documentazione Principale

### 🏗️ Architettura di Sistema
- **[ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md)** ⭐ INIZIA QUI
  - Panoramica sistema e livelli architettura
  - Matrice microservizi
  - Copertura casi d'uso
  - Pattern integrazione
  - Deployment e sicurezza

### 👨‍💻 Guida Sviluppo
- **[DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md)**
  - Setup environment locale
  - Workflow development
  - Testing e deployment
  - Debugging e troubleshooting
  - Best practice sicurezza

### ⚖️ Compliance e Normative
- **[COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)**
  - Normative italiane (L. 241/1990, CAD, ecc.)
  - Regolamenti UE (GDPR, eIDAS, AI Act)
  - Standard ISO/IEC
  - Linee guida AGID
  - Mapping UC-specific

### 💸 Costi e Hosting
- **[COSTI-HOSTING-SERVIZI.md](COSTI-HOSTING-SERVIZI.md)**
  - Stime costi di hosting, opzioni di infrastruttura e servizi gestiti

### 📊 Sequence Diagrams
- **[SEQUENCE-DIAGRAMS-TEMPLATE.md](SEQUENCE-DIAGRAMS-TEMPLATE.md)**
  - 6 pattern principali di sequence diagram
  - Template riusabili in Mermaid
  - Best practice e sintassi
  - Dove aggiungere i diagrammi
  - Esempi per ogni tipo di flusso

### 📐 Struttura Documentazione
- **[DOCUMENTATION-STRUCTURE-GUIDE.md](DOCUMENTATION-STRUCTURE-GUIDE.md)** ⭐ PER DEVELOPER
  - Gerarchia documentazione microservizio (8 livelli)
  - Gerarchia documentazione UC-SP (4 livelli)
  - Workflow di navigazione per developer
  - Template sequence diagram per SP
  - Template request/response payload
  - Best practice completezza documentazione

- **[DOCUMENTATION-STRUCTURE-VISUAL.md](DOCUMENTATION-STRUCTURE-VISUAL.md)** 📊 GUIDA VISUALE
  - Visualizzazione architettura documentazione
  - Workflow di lettura per 3 scenari diversi
  - Fasi implementazione (Discovery → Deployment)
  - Livelli documentazione (Governance → MS)
  - Checklist completezza per UC e MS

### 📝 Template Concreto SP
- **[use_cases/UC5 - Produzione Documentale Integrata/TEMPLATE-SP-STRUCTURE.md](use_cases/UC5%20-%20Produzione%20Documentale%20Integrata/TEMPLATE-SP-STRUCTURE.md)**
  - Esempio completo UC5-SP02
  - 7 sezioni standardizzate per SP
  - Sequence diagram con Mermaid
  - Request/Response payload con validazioni
  - Alternative paths (cache, error, retry)
  - Integrazione nel UC

---

## 🔧 Microservizi (16 Servizi)

### MS01-CLASSIFIER ⭐ (Reference Implementation)
**Classificatore intelligente di documenti**

| Documento | Descrizione | Tempo Lettura |
|-----------|-------------|---------------|
| [README.md](microservices/MS01-CLASSIFIER/README.md) | Quick start e overview | 5 min |
| [SPECIFICATION.md](microservices/MS01-CLASSIFIER/SPECIFICATION.md) | Architettura tecnica | 30 min |
| [API.md](microservices/MS01-CLASSIFIER/API.md) | Riferimento API completo | Riferimento |
| [DATABASE-SCHEMA.md](microservices/MS01-CLASSIFIER/DATABASE-SCHEMA.md) | ER diagrams + indici | Riferimento |
| [init-schema.sql](microservices/MS01-CLASSIFIER/init-schema.sql) | Script DDL PostgreSQL | - |
| [TROUBLESHOOTING.md](microservices/MS01-CLASSIFIER/TROUBLESHOOTING.md) | Problemi comuni | Come-necessario |
| [docker-compose.yml](microservices/MS01-CLASSIFIER/docker-compose.yml) | Setup locale | - |
| [kubernetes/](microservices/MS01-CLASSIFIER/kubernetes/) | Manifesti K8s | - |
| [examples/](microservices/MS01-CLASSIFIER/examples/) | Esempi request/response | - |

### MS02-MS16 (Template Structure)
Tutti i seguenti microservizi seguono lo **stesso pattern di MS01**:

- **MS02-ANALYZER** - Analisi contenuto & NLP
- **MS03-ORCHESTRATOR** - Gestione workflow
- **MS04-VALIDATOR** - Validazione dati
- **MS05-TRANSFORMER** - Trasformazione dati
- **MS06-AGGREGATOR** - Consolidamento dati
- **MS07-DISTRIBUTOR** - Consegna contenuti
- **MS08-MONITOR** - Monitoraggio sistema
- **MS09-MANAGER** - Orchestrazione risorse
- **MS10-LOGGER** - Logging centralizzato
- **MS11-GATEWAY** - API gateway
- **MS12-CACHE** - Layer caching
- **MS13-SECURITY** - Sicurezza & crittografia
- **MS14-AUDIT** - Audit & compliance
- **MS15-CONFIG** - Gestione configurazione
- **MS16-REGISTRY** - Service discovery

### Master Microservizi
- **[MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md)**
  - Matrice comparativa MS01-MS16
  - Dependency mapping
  - Performance SLA
  - Deployment procedures

---

## 📋 Casi d'Uso (11 Workflow)

Located in `use_cases/`:

### Workflow Core
1. **UC1** - Email Integration (Intake)
2. **UC2** - Document Classification
3. **UC3** - Metadata Extraction
4. **UC4** - Knowledge Base Integration
5. **UC5** - Produzione Documentale Integrata
6. **UC6** - Firma Digitale Integrata
7. **UC7** - Conservazione Digitale

### Funzionalità Avanzate
8. **UC8** - Intelligent Data Extraction
9. **UC9** - Automated Workflow
10. **UC10** - User Support & Ticketing
11. **UC11** - Analytics & Reporting

---

## 📊 Sub-Progetti Specializzati (SP01-SP72)

### Mapping Completo
- **[SP-MS-MAPPING-MASTER.md](SP-MS-MAPPING-MASTER.md)**
  - Tutti 72 SP
  - Mapping a MS
  - Responsabilità
  - Copertura UC

### Raggruppamenti per UC
- Ogni UC5, UC6, UC7 contiene mapping dettagliato dei suoi SP

---

## 🗺️ Navigazione per Ruolo

### 👤 Per Sviluppatori
1. Inizia: [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md)
2. Reference: [MS01-CLASSIFIER/README.md](microservices/MS01-CLASSIFIER/README.md)
3. Setup: Esegui `docker-compose up` in MS01
4. Deep dive: Leggi SPECIFICATION.md del servizio

**Checklist**:
- [ ] Lettura DEVELOPMENT-GUIDE
- [ ] Setup docker-compose locale
- [ ] Test API con examples/
- [ ] Lettura SPECIFICATION per cambio code
- [ ] Submissione PR con aggiornamento docs

### 🏛️ Per Architetti
1. Inizia: [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md)
2. Reference: [MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md)
3. Mapping: [SP-MS-MAPPING-MASTER.md](SP-MS-MAPPING-MASTER.md)
4. Compliance: [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)

**Checklist**:
- [ ] Lettura Architecture Overview
- [ ] Analisi MS dependency matrix
- [ ] Review UC-specific flows
- [ ] Compliance assessment
- [ ] Documentation sign-off

### ⚙️ Per Operations
1. Inizia: [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md#-deployment)
2. Kubernetes: Vedi `kubernetes/` folder in ogni MS
3. Monitoring: Prometheus/Grafana dashboard
4. Troubleshooting: TROUBLESHOOTING.md per ogni MS

**Checklist**:
- [ ] Kubernetes manifests verificati
- [ ] Monitoring dashboard setup
- [ ] Alerting rules configured
- [ ] Runbook completion
- [ ] Disaster recovery plan

### 👨‍⚖️ Per Compliance
1. Inizia: [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)
2. Reference: [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md#-sicurezza)
3. Mapping: Vedi ogni UC folder per mapping dettagliato

**Checklist**:
- [ ] Normative assessment completo
- [ ] MS13-SECURITY review
- [ ] GDPR compliance check
- [ ] Audit trail verification
- [ ] Annual compliance review

---

## 🚀 Quickstart per Ruolo

### Sviluppatore - Primi 30 minuti
```bash
# 1. Leggi intro (5 min)
cat DEVELOPMENT-GUIDE.md

# 2. Setup ambiente (10 min)
cd microservices/MS01-CLASSIFIER
docker-compose up -d

# 3. Test API (10 min)
curl http://localhost:8001/health
curl -X POST http://localhost:8001/api/v1/classify \
  -H "Content-Type: application/json" \
  -d @examples/request.json

# 4. Explore docs (5 min)
cat README.md
```

### Architetto - Primo Review (1 ora)
```bash
# 1. Architecture overview (20 min)
cat ARCHITECTURE-OVERVIEW.md

# 2. MS mapping (20 min)
cat MS-ARCHITECTURE-MASTER.md

# 3. Compliance review (20 min)
cat COMPLIANCE-MATRIX.md
```

### Operations - Setup Produzione (1-2 ore)
```bash
# 1. Read architecture (20 min)
cat ARCHITECTURE-OVERVIEW.md

# 2. Deploy Kubernetes (30 min)
kubectl apply -f microservices/MS01-CLASSIFIER/kubernetes/

# 3. Configure monitoring (30 min)
# Access Prometheus/Grafana dashboard

# 4. Test e verify (20 min)
curl http://ms01-classifier.zenia.local/health
```

---

## 📖 Struttura Documentazione per Microservizio

Ogni cartella microservizio (MS01-MS16) contiene:

```
MSxx-NAME/
├── README.md
│   └── Quick start 5 minuti
│
├── SPECIFICATION.md
│   └── Architettura tecnica 30 minuti
│
├── API.md
│   └── Endpoint reference
│
├── DATABASE-SCHEMA.md
│   ├── ER diagrams (Mermaid)
│   └── Punti a init-schema.sql
│
├── init-schema.sql
│   └── DDL script separato
│
├── TROUBLESHOOTING.md
│   └── Problemi comuni e soluzioni
│
├── docker-compose.yml
│   └── Setup locale
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
│
└── examples/
    ├── request.json
    └── response.json
```

---

## 🔍 Come Trovare Informazioni

### Conosco il Microservizio
- Vedi [MS-ARCHITECTURE-MASTER.md](microservices/MS-ARCHITECTURE-MASTER.md)
- Apri cartella `microservices/MSxx-NAME/`

### Conosco il Caso d'Uso (UC)
- Vedi `use_cases/UCxx-NAME/`
- Controlla matrice dipendenze per MS/SP coinvolti

### Conosco il Sub-Progetto (SP)
- Cerca in [SP-MS-MAPPING-MASTER.md](SP-MS-MAPPING-MASTER.md)
- Identifica MS responsabile
- Vedi documentazione MS corrispondente

### Devo Deployare su Kubernetes
- Leggi [ARCHITECTURE-OVERVIEW.md - Deployment](ARCHITECTURE-OVERVIEW.md#-deployment)
- Usa `kubernetes/` manifesti in ogni MS folder

### Cerco Compliance
- Vedi [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)
- Ricerca per normativa italiana/UE specifica

---

## 📌 File Critici

| File | Tipo | Uso |
|------|------|-----|
| ARCHITECTURE-OVERVIEW.md | Governance | Entry point architettura |
| DEVELOPMENT-GUIDE.md | Governance | Guide sviluppatori |
| COMPLIANCE-MATRIX.md | Governance | Mapping normative |
| MS-ARCHITECTURE-MASTER.md | Reference | Matrice MS |
| SP-MS-MAPPING-MASTER.md | Reference | Matrice SP |
| MS01-CLASSIFIER/* | Reference | Template documentazione |
| COSTI-HOSTING-SERVIZI.md | Governance | Costi hosting e opzioni servizi |

---

## 🆘 Ottieni Aiuto

### Technical Issues
- Vedi **TROUBLESHOOTING.md** nella cartella MS
- Controlla **[DEVELOPMENT-GUIDE.md - Debugging](DEVELOPMENT-GUIDE.md#-debugging)**

### Documentation Questions
- Controlla **[README.md](README.md)** (questo file)
- Cerca nella documentazione per parola chiave

### Compliance Questions
- Controlla **[COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md)**
- Contatta DPO: compliance-review@zenia.local

### Architecture Questions
- Vedi **[ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md)**
- Contatta architect: #zenia-architecture Slack

---

## 📈 Versioning & Updates

| Documento | Versione | Ultimo Update | Prossimo Review |
|-----------|----------|---------------|-----------------|
| ARCHITECTURE-OVERVIEW | 1.0 | 2024-11-18 | 2025-05-18 |
| DEVELOPMENT-GUIDE | 1.0 | 2024-11-18 | 2025-05-18 |
| COMPLIANCE-MATRIX | 1.0 | 2024-11-18 | 2025-05-18 |
| MS-ARCHITECTURE-MASTER | 1.0 | 2024-11-18 | 2025-02-18 |

---

## 🔐 Gestione Documentazione

### Come Contribuire
1. Leggi [DEVELOPMENT-GUIDE.md - Commit & PR](DEVELOPMENT-GUIDE.md#-guideline-commit--pr)
2. Aggiorna documentazione con code changes
3. Submit PR con docs updated

### Maintenance
- Review annuale completeness (maggio)
- Update compliance annuale (novembre)
- Bug fix e chiarimenti as-needed

---

**Versione**: 1.0
**Creata**: 2024-11-18
**Lingua**: Italiano
**Maintainers**: ZenIA Documentation Team
