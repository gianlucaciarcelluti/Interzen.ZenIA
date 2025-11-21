# Struttura Documentazione ZenIA - Guida Visuale

Questa pagina mostra visualmente come è organizzata la documentazione per massima chiarezza.

---

## 🏗️ Architettura Documentazione

```
docs/
├── GOVERNANCE LAYER (Root)
│   ├── README.md ⭐ ENTRY POINT
│   ├── ARCHITECTURE-OVERVIEW.md
│   ├── DEVELOPMENT-GUIDE.md
│   ├── COMPLIANCE-MATRIX.md
│   ├── COSTI-HOSTING-SERVIZI.md
│   ├── DOCUMENTATION-STRUCTURE-GUIDE.md ← Guide struttura
│   ├── SEQUENCE-DIAGRAMS-TEMPLATE.md
│   └── DOCUMENTATION-STRUCTURE-VISUAL.md ← This file
│
├── MICROSERVICES LAYER
│   └── microservices/
│       ├── MS-ARCHITECTURE-MASTER.md
│       ├── MS01-CLASSIFIER/ ⭐ Implementazione di riferimento
│       │   ├── README.md (5 min)
│       │   ├── SPECIFICATION.md (30 min + diagrammi)
│       │   ├── API.md (riferimento)
│       │   ├── DATABASE-SCHEMA.md (diagramma ER)
│       │   ├── init-schema.sql (DDL script)
│       │   ├── TROUBLESHOOTING.md
│       │   ├── docker-compose.yml
│       │   ├── kubernetes/
│       │   └── examples/
│       │       ├── request.json
│       │       └── response.json
│       │
│       ├── MS02-ANALYZER/ → Stessa struttura
│       ├── MS03-ORCHESTRATOR/ → Stessa struttura
│       └── ... MS04-MS16 (15 template structures)
│
├── USE CASES LAYER
│   └── use_cases/
│       ├── SP-MS-MAPPING-MASTER.md
│       │
│       ├── UC1 - Integrazione Email/
│       │   ├── 00_OVERVIEW.md
│       │   ├── 01_SPxx - NAME.md (for each SP in UC1)
│       │   │   ├── Descrizione
│       │   │   ├── Sequence Diagram
│       │   │   ├── Request Payload
│       │   │   ├── Response Payload (success + errors)
│       │   │   ├── Alternative Paths (cache, error, retry)
│       │   │   └── Integration in UC
│       │   ├── 02_ARCHITECTURE.md
│       │   └── 03_ACCEPTANCE-CRITERIA.md
│       │
│       ├── UC2 - Classificazione Documenti/ → Stesso schema
│       ├── UC3 - Governance/ → Stesso schema
│       ├── ...
│       │
│       ├── UC5 - Produzione Documentale Integrata/ ⭐
│       │   ├── 00_OVERVIEW.md
│       │   ├── CANONICAL-Complete-Flow.md
│       │   ├── 01_SP01 - EML Parser & Email Intelligence.md
│       │   ├── 01_SP02 - Document Extractor & Attachment Classifier.md
│       │   ├── 01_SP03 - Classificatore Procedurale.md
│       │   ├── 01_SP04 - Knowledge Base.md
│       │   ├── 01_SP05 - Template Engine.md
│       │   ├── ... SP06-SP12 ...
│       │   ├── 02_ARCHITECTURE.md
│       │   ├── 02_SUPPLEMENTARY - Overview Semplificato.md
│       │   ├── 03_ACCEPTANCE-CRITERIA.md
│       │   ├── 03 Human in the Loop (HITL).md
│       │   ├── TEMPLATE_SP_STRUCTURE.md ← Usa questo template
│       │   └── Guida_Generazione_Atti_Amministrativi.md
│       │
│       ├── UC6 - Firma Digitale Integrata/ → Same pattern
│       ├── UC7 - Conservazione Digitale/ → Same pattern
│       └── ... UC8-UC11 ...
```

---

## 📖 Gerarchia Lettura per Developer

```
Scenario 1: "Voglio capire il flusso UC5"
```

```
1. Leggi 2-3 min:
  └─ docs/use_cases/UC5 - .../00_OVERVIEW.md
    Cosa fa UC5, attori, SLA

2. Leggi diagrammi 5 min:
  └─ docs/use_cases/UC5 - .../CANONICAL-Complete-Flow.md
    Sequence diagram completo del flusso

3. Scegli SP (es. SP02):
  └─ docs/use_cases/UC5 - .../01_SP02 - Document Extractor.md
    ├─ Descrizione: cosa fa SP02
    ├─ Sequence: come funziona internamente
    ├─ Payloads: esempi request/response
    └─ Integrazione: come si collega ad altri SP
```

---

```
Scenario 2: "Devo implementare UC5-SP02"
```

```
1. Context UC (5 min):
   └─ docs/use_cases/UC5 - .../00_OVERVIEW.md

2. SP Details (10 min):
   └─ docs/use_cases/UC5 - .../01_SP02 - Document Extractor.md
      ├─ Descrizione SP (cosa, perché, MS coinvolti)
      ├─ Sequence diagram (flusso tecnico)
      ├─ Request/Response (struttura dati)
      └─ Alternative paths (cache, errors)

3. MS Implementation (30 min):
  └─ docs/microservices/MS02-ANALYZER/
    ├─ README.md (panoramica rapida)
    ├─ SPECIFICATION.md (approfondimento tecnico)
    ├─ API.md (endpoint di riferimento)
    ├─ DATABASE-SCHEMA.md (modello dati)
    └─ examples/ (esempi payload)

4. Setup Local (10 min):
   └─ docs/microservices/MS02-ANALYZER/
      ├─ docker-compose.yml (run locally)
      └─ DEVELOPMENT-GUIDE.md (workflow)

5. Deploy (15 min):
   └─ docs/microservices/MS02-ANALYZER/
      └─ kubernetes/ (production manifests)
```

**Totale: ~70 minuti** per passare da requisiti a deployment

---

```
Scenario 3: "Come faccio a testare UC5-SP02?"
```

```
1. Payload Examples (2 min):
  └─ docs/use_cases/UC5 - .../01_SP02 - Document Extractor.md
    ├─ Request Payload (copia/incolla in Postman)
    ├─ Response Success (output atteso)
    └─ Response Error (casi limite)

2. API Reference (5 min):
   └─ docs/microservices/MS02-ANALYZER/API.md
      ├─ Endpoint specification
      ├─ HTTP codes
      └─ Error responses

3. Acceptance Criteria (5 min):
   └─ docs/use_cases/UC5 - .../03_ACCEPTANCE-CRITERIA.md
      ├─ Test scenarios
      ├─ SLA thresholds
      └─ Rollback procedures

4. Examples Folder (direct):
   └─ docs/microservices/MS02-ANALYZER/examples/
      ├─ request.json (for curl/Postman)
      └─ response.json (expected output)
```

**Totale: ~12 minuti** per eseguire un test

---

## 🔄 Workflow Implementazione

### Phase 1: Discovery (Day 1)

```
Developer legge:
1. UC Overview (00_OVERVIEW.md) ← Understand what
2. SP Description (01_SPxx.md) ← Understand why
3. Sequence Diagram (01_SPxx.md) ← Understand how

Deliverable: Requirement specification document
```

### Phase 2: Architecture (Day 1-2)

```
Developer crea:
1. MS SPECIFICATION.md (architecture)
2. DATABASE-SCHEMA.md (ER diagram)
3. Sequence diagrams (multiple paths)

Validates:
- Architecture review meeting
- Database schema normalized
- SLA compliance
```

### Phase 3: Implementation (Day 2-4)

```
Developer implementa:
1. MS API endpoints
2. Database migrations
3. Business logic

Follows:
- examples/ for payload format
- SPECIFICATION.md for flow
- DEVELOPMENT-GUIDE.md for best practices
```

### Phase 4: Testing (Day 4-5)

```
Tester verifica:
1. SP request/response payloads
2. Sequence diagram flows
3. Error scenarios

Uses:
- examples/request.json for API calls
- 01_SPxx.md Alternative Paths for edge cases
- ACCEPTANCE-CRITERIA.md for SLA
```

### Phase 5: Deployment (Day 5)

```
Operations esegue il deploy di:
1. Kubernetes manifests (kubernetes/)
2. Startup procedures
3. Monitoring setup

References:
- DEVELOPMENT-GUIDE.md (CI/CD)
- docker-compose.yml (local equivalents)
- TROUBLESHOOTING.md (common issues)
```

---

## 📊 Documentation Levels

### Level 1: Governance (Root Level)
**Tempo di lettura**: 30 min totali
**Audience**: Tutti

```
README.md ⭐
├─ ARCHITECTURE-OVERVIEW.md (system design)
├─ DEVELOPMENT-GUIDE.md (workflow)
├─ COMPLIANCE-MATRIX.md (regulatory)
├─ DOCUMENTATION-STRUCTURE-GUIDE.md (this)
└─ SEQUENCE-DIAGRAMS-TEMPLATE.md (patterns)
```

### Level 2: Use Cases
**Tempo di lettura**: 15-30 min per UC
**Audience**: Product, Business Analyst, Developer

```
UC5/ Overview
├─ 00_OVERVIEW.md (what, why, who)
├─ 01 CANONICAL Sequence.md (big picture flow)
├─ 02_ARCHITECTURE.md (dependency matrix)
└─ 03_ACCEPTANCE-CRITERIA.md (testing)
```

### Level 3: Sub-Projects (SP)
**Tempo di lettura**: 10-15 min per SP
**Audience**: Sviluppatori, QA, Architetti

```
UC5/ Details
├─ 01_SP01 - NAME.md
│  ├─ Description (business + technical)
│  ├─ Sequence Diagram (flow)
│  ├─ Request Payload (with validation)
│  ├─ Response Payload (success + error)
│  └─ Integration (where in UC)
├─ 01_SP02 - NAME.md (same)
└─ 01_SP03 - NAME.md (same)
```

### Level 4: Microservices
**Tempo di lettura**: 35 min per MS
**Audience**: Sviluppatori, DevOps, Architetti

```
MS02-ANALYZER/
├─ README.md (5 min)
├─ SPECIFICATION.md (30 min)
├─ API.md (reference)
├─ DATABASE-SCHEMA.md (reference)
├─ TROUBLESHOOTING.md (reference)
├─ docker-compose.yml (local dev)
├─ kubernetes/ (production)
└─ examples/ (payloads)
```

---

## ✅ Documentation Completeness Checklist

### For UC (Use Case)

- [ ] **00_OVERVIEW.md**
  - [ ] Description (what, why, when, who)
  - [ ] Actors (roles, systems)
  - [ ] Triggers and postconditions
  - [ ] SLA and success metrics
  - [ ] Index of SPs with links

- [ ] **For each SP:**
  - [ ] Descrizione (business + technical)
  - [ ] MS coinvolti
  - [ ] Sequence diagram (happy path)
  - [ ] Request payload (with example)
  - [ ] Response payload success (with example)
  - [ ] Response payload error (with example)
  - [ ] Alternative paths (cache, error, retry)
  - [ ] Integration notes (where in flow)

- [ ] **02_ARCHITECTURE.md**
  - [ ] UC architecture diagram
  - [ ] SP dependency matrix
  - [ ] Execution timeline
  - [ ] Compliance mapping

- [ ] **03_ACCEPTANCE-CRITERIA.md**
  - [ ] Test scenarios
  - [ ] SLA thresholds
  - [ ] Error conditions
  - [ ] Rollback procedures

### For MS (Microservice)

- [ ] **README.md**
  - [ ] What is it (one paragraph)
  - [ ] Key responsibilities
  - [ ] Technology stack
  - [ ] Dependencies (input/output)

- [ ] **SPECIFICATION.md**
  - [ ] Overview
  - [ ] ER diagram (Mermaid)
  - [ ] Components description
  - [ ] Sequence diagrams (multiple flows)
  - [ ] Performance SLA

- [ ] **API.md**
  - [ ] Base URL and auth
  - [ ] Endpoints (method, path, request, response)
  - [ ] Error codes
  - [ ] Examples

- [ ] **DATABASE-SCHEMA.md**
  - [ ] ER diagram (Mermaid, all tables)
  - [ ] Table descriptions
  - [ ] Column definitions
  - [ ] Index strategy

- [ ] **init-schema.sql**
  - [ ] Complete DDL script

- [ ] **TROUBLESHOOTING.md**
  - [ ] Common problems
  - [ ] Diagnostic procedures
  - [ ] Solutions
  - [ ] Prevention strategies

- [ ] **docker-compose.yml**
  - [ ] All services
  - [ ] Environment variables
  - [ ] Health checks
  - [ ] Volume management

- [ ] **kubernetes/**
  - [ ] deployment.yaml
  - [ ] service.yaml
  - [ ] configmap.yaml

- [ ] **examples/**
  - [ ] request.json
  - [ ] response.json

---

## 🎯 Key Benefits of This Structure

### Per gli Sviluppatori
✅ Navigazione lineare e intuitiva
✅ Esempi pronti da copia/incollare
✅ Comprendere immediatamente le dipendenze MS
✅ Payload di test forniti

### Per i Tester
✅ Criteri di accettazione chiari
✅ Scenari di test derivati dai sequence diagram
✅ Esempi di payload per automazione
✅ Soglie SLA documentate

### Per le Operations
✅ SLA e tempi immediatamente visibili
✅ Sequence diagram per troubleshooting
✅ Dipendenze chiare (analisi impatto fallimenti)
✅ Procedure di deployment passo-passo

### Per gli Architetti
✅ Architettura visibile a più livelli
✅ Matrici delle dipendenze
✅ Tracciabilità della conformità
✅ Modelli di integrazione documentati

### Per il Business
✅ Panoramiche UC in linguaggio chiaro
✅ Attori e ruoli definiti
✅ SLA e metriche di successo definite
✅ Mappatura conformità verso le normative

---

## 🔗 Cross-References

Tutti i file sono interconnessi tramite link:

```
README.md
  ├─ ARCHITECTURE-OVERVIEW.md
  ├─ DEVELOPMENT-GUIDE.md
  ├─ DOCUMENTATION-STRUCTURE-GUIDE.md ← Start here
  │
  ├─ microservices/MS01-CLASSIFIER/
  │  ├─ README.md → links to use_cases/
  │  ├─ SPECIFICATION.md → links to database schema
  │  └─ API.md → links to examples/
  │
  └─ use_cases/UC5/
     ├─ 00_OVERVIEW.md → links to SP details
     ├─ 01_SP02.md
     │  ├─ Links to MS02-ANALYZER (implementer)
     │  ├─ Links to other SPs (dependencies)
     │  └─ Links to UC5 architecture
     └─ 03_ACCEPTANCE-CRITERIA.md → links to SLA in SPECIFICATION.md
```

---

**Versione**: 1.0
**Creato**: 2024-11-18
**Lingua**: Italiano
**Maintainer**: Team Documentazione ZenIA

---

## 🚀 Next Steps

1. **Applicare questa struttura** a UC5-UC11 SP
2. **Popolare ogni SP** con sequence diagram e payload
3. **Aggiornare la documentazione MS** con endpoint API reali
4. **Collegare tutto** tramite cross-reference in markdown
5. **Revisionare con il team** per chiarezza e completezza
