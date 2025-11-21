# PHASE 2 CONTINUATION PLAN — Diagrammi Mermaid e JSON Schema
**Aggiornato**: 20 novembre 2025
**Versione**: 1.0
**Status**: PIANIFICAZIONE DETTAGLIATA PER A2 E A3

---

## EXECUTIVE SUMMARY

Dopo il completamento della **Phase 1 (6 items completati)** e della **Phase 2 A1 (Conformità Normativa - 71 SP aggiornati)**, procediamo con:

- **A2 — Standardizzare Diagrammi Mermaid per SP Critici** (target: 13 SP)
- **A3 — JSON Payload Standard Template e Schema** (target: 5-10 SP)

**Stima Effort Totale**: 6-8 giorni (A2: 3-4g, A3: 2-3g)

**Incremento Completezza**: 97.1% → 99%+

---

## PHASE 2 A2: STANDARDIZZAZIONE DIAGRAMMI MERMAID

### Stato Attuale (Novembre 20, 2025)

**Analisi Coverage Diagrammi per SP Critici**:

| SP | Flowchart | Sequence | State | Totale | Status |
|----|-----------|----------|-------|--------|--------|
| SP01 (EML Parser) | 1 | 3 | 1 | **5** | ✅ COMPLETE |
| SP03 (Procedural Classifier) | ❌ | 1 | ❌ | 1 | 🔴 INCOMPLETE |
| SP04 (Knowledge Base) | ❌ | 1 | ❌ | 1 | 🔴 INCOMPLETE |
| SP05 (Template Engine) | ❌ | 1 | ❌ | 1 | 🔴 INCOMPLETE |
| SP06 (Validator) | ❌ | 1 | ❌ | 1 | 🔴 INCOMPLETE |
| SP07 (Content Classifier) | ❌ | 1 | ❌ | 1 | 🔴 INCOMPLETE |
| SP08 (Quality Checker) | ❌ | 1 | ❌ | 1 | 🔴 INCOMPLETE |
| SP09 (Workflow Engine) | ❌ | 1 | 1 | 2 | 🟡 PARTIAL |
| SP10 (Control Dashboard) | ❌ | 1 | ❌ | 1 | 🔴 INCOMPLETE |
| SP11 (Security & Audit) | 2 | 1 | ❌ | 3 | ✅ ACCEPTABLE |
| SP12 (Semantic Search) | 2 | ❌ | ❌ | 2 | 🔴 INCOMPLETE |
| SP29 (Digital Signature) | 1 | ❌ | ❌ | 1 | 🔴 INCOMPLETE |
| SP42 (Policy Engine) | ❌ | ❌ | ❌ | 0 | 🔴 MISSING |

### Target State (Post-A2)

**Standard richiesto**: Ogni SP critico DEVE AVERE:
- ✅ **1+ Flowchart** (architettura, componenti, flusso dati)
- ✅ **1+ Sequence Diagram** (interazioni, main flow)
- ✅ **1+ State Diagram** (lifecycle, stati, transizioni)

### Diagrammi da Aggiungere

#### 🔴 CRITICI (0-1 diagrammi total)

**SP03 - Procedural Classifier** [UC3]
- Add: 1 Flowchart (classification pipeline)
- Add: 1 State Diagram (procedure lifecycle)
- Current: 1 sequence diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP04 - Knowledge Base** [UC5]
- Add: 1 Flowchart (KB architecture & retrieval flow)
- Add: 1 State Diagram (document lifecycle in KB)
- Current: 1 sequence diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP05 - Template Engine** [UC5]
- Add: 1 Flowchart (template processing pipeline)
- Add: 1 State Diagram (template transformation states)
- Current: 1 sequence diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP06 - Validator** [UC5]
- Add: 1 Flowchart (validation rules & checks)
- Add: 1 State Diagram (validation process states)
- Current: 1 sequence diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP07 - Content Classifier** [UC1, UC5]
- Add: 1 Flowchart (classification algorithm flow)
- Add: 1 State Diagram (content classification states)
- Current: 1 sequence diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP08 - Quality Checker** [UC5]
- Add: 1 Flowchart (quality assessment pipeline)
- Add: 1 State Diagram (quality check states)
- Current: 1 sequence diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP10 - Control Dashboard** [UC5]
- Add: 1 Flowchart (dashboard data flow & updates)
- Add: 1 State Diagram (dashboard state management)
- Current: 1 sequence diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP42 - Policy Engine** [UC9]
- Add: 1 Flowchart (policy authoring & enforcement)
- Add: 1 Sequence Diagram (policy enforcement flow)
- Add: 1 State Diagram (policy lifecycle)
- Current: 0 diagrams
- Target Total: 3 diagrams
- Estimated Effort: 3-4 hours (new from scratch)

#### 🟡 PARTIAL (2 diagrammi)

**SP09 - Workflow Engine** [UC4, UC5]
- Add: 1 Flowchart (workflow orchestration architecture)
- Current: 1 sequence diagram + 1 state diagram
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

**SP12 - Semantic Search & Q&A** [UC1]
- Add: 1 Sequence Diagram (query processing flow)
- Add: 1 State Diagram (search request states)
- Current: 2 flowcharts
- Target Total: 4 diagrams (above minimum)
- Estimated Effort: 2-3 hours

**SP29 - Digital Signature Engine** [UC6]
- Add: 1 Sequence Diagram (signature request/response flow)
- Add: 1 State Diagram (signature lifecycle)
- Current: 1 flowchart
- Target Total: 3 diagrams
- Estimated Effort: 2-3 hours

### Implementation Plan A2

**Phase 2 A2 Work Breakdown**:


**Total Effort**: 13 SP × 2.5 hours avg = **32.5 hours ≈ 4 days**

### Diagram Templates & Examples

All diagrams will follow the **TEMPLATE-MERMAID-DIAGRAMMI.md** standards:

**Flowchart Pattern** (for SP03-SP10):
```
flowchart TD
    A[Input] --> B{Processing}
    B -->|Success| C[Output]
    B -->|Error| D[Error Handling]
    C --> E[Result]
    D --> E
```

**State Diagram Pattern** (for SP lifecycle):
```
stateDiagram-v2
    [*] --> Created
    Created --> Processing
    Processing --> Validated
    Validated --> Completed
    Validated --> Failed
    Failed --> [*]
    Completed --> [*]
```

**Sequence Diagram Pattern** (for SP interactions):
```
sequenceDiagram
    participant A as Component A
    participant B as Component B
    A->>B: Request
    B->>B: Process
    B-->>A: Response
```

---

## PHASE 2 A3: JSON PAYLOAD STANDARD TEMPLATE E SCHEMA

### Stato Attuale

✅ **JSON Coverage Excellent**:
- 519 JSON examples validati (100% valid)
- 31 file UC/SP con JSON
- Schema consistency: 70%

### Obiettivo A3

Creare:
1. **docs/templates/json-payload-standard.md** — template standardizzato
2. **docs/schemas/** — JSON Schema files per SP critici

### 1. JSON Payload Standard Template

**Location**: `docs/templates/json-payload-standard.md` (nuovi contenuti)

**Sections**:

```markdown
# JSON Payload Standard Template

## 1. Request Payload Pattern
{
  "metadata": {
    "request_id": "UUID v4",
    "timestamp": "ISO 8601",
    "version": "1.0",
    "correlation_id": "UUID v4 (for tracing)"
  },
  "data": {
    /* domain-specific data */
  },
  "options": {
    "async": boolean,
    "timeout": integer (ms)
  }
}

## 2. Response Success Pattern
{
  "success": true,
  "data": {
    /* domain-specific results */
  },
  "metadata": {
    "response_id": "UUID v4",
    "timestamp": "ISO 8601",
    "processing_time_ms": integer,
    "version": "1.0"
  }
}

## 3. Response Error Pattern
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { /* error details */ }
  },
  "metadata": {
    "response_id": "UUID v4",
    "timestamp": "ISO 8601",
    "version": "1.0"
  }
}

## 4. Batch Operation Pattern
{
  "batch_id": "UUID v4",
  "items": [
    { /* item 1 */ },
    { /* item 2 */ }
  ],
  "options": {
    "parallel": boolean,
    "continue_on_error": boolean
  }
}

## 5. Pagination Pattern
{
  "data": [ /* items */ ],
  "pagination": {
    "page": integer,
    "page_size": integer,
    "total_items": integer,
    "total_pages": integer,
    "has_next": boolean,
    "has_prev": boolean
  }
}
```

### 2. JSON Schema Files for Critical SPs

**Location**: `docs/schemas/`

#### SP01 - EML Parser & Email Intelligence
File: `SP01-EMAIL-PAYLOAD.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SP01 EML Parser Request",
  "type": "object",
  "required": ["eml_file_path", "workflow_id"],
  "properties": {
    "eml_file_path": {
      "type": "string",
      "format": "uri",
      "description": "S3 path to EML file"
    },
    "workflow_id": {
      "type": "string",
      "pattern": "^WF-[0-9]+$",
      "description": "Workflow identifier"
    },
    "options": {
      "type": "object",
      "properties": {
        "extract_attachments": { "type": "boolean" },
        "validate_signatures": { "type": "boolean" }
      }
    }
  }
}
```

#### SP07 - Content Classifier
File: `SP07-CLASSIFICATION-PAYLOAD.schema.json`

#### SP12 - Semantic Search
File: `SP12-SEARCH-PAYLOAD.schema.json`

#### SP29 - Digital Signature
File: `SP29-SIGNATURE-PAYLOAD.schema.json`

#### SP42 - Policy Engine
File: `SP42-POLICY-PAYLOAD.schema.json`

### Implementation Plan A3

```
WEEK 2 (Day 5):
├─ Create docs/templates/json-payload-standard.md (2 hours)
└─ Create docs/schemas/ folder structure (0.5 hour)

WEEK 3 (Days 1-2):
├─ SP01 schema + examples (1.5 hours)
├─ SP07 schema + examples (1.5 hours)
└─ SP12 schema + examples (1.5 hours)

WEEK 3 (Days 3):
├─ SP29 schema + examples (1 hour)
└─ SP42 schema + examples (1 hour)
```

**Total Effort A3**: **10 hours ≈ 1.5 days**

---

## METRICHE DI SUCCESSO PHASE 2

### Post-A2 Targets (Diagrammi)

| Metrica | Baseline | Target | Impact |
|---------|----------|--------|--------|
| SP critici con 3+ diagrammi | 2/13 (15%) | 13/13 (100%) | +1.2% completezza |
| Diagrammi totali nel sistema | 204 | ~260 | +28% copertura visiva |
| Sequence diagram coverage | 30% | 100% | Migliore leggibilità flussi |
| State diagram coverage | 10% | 85%+ | Chiarezza ciclo di vita |

### Post-A3 Targets (JSON Schema)

| Metrica | Baseline | Target | Impact |
|---------|----------|--------|--------|
| JSON schema files | 0 | 5+ | Validazione formale |
| SP con schema JSON | 0/5 | 5/5 (100%) | Sviluppatori guidati |
| Template consistency | 70% | 95%+ | Qualità payload standardizzata |

### SCORE COMPLESSIVO

```
Baseline (Post-A1):        97.1%
After A2 (Diagrammi):      98.3%
After A3 (JSON Schema):    98.8%
Final Target (Post-Phase 2): 99%+
```

---

## TIMELINE SUMMARY

```
PHASE 1 (COMPLETATO): 7-8 giorni
├─ C1: Infrastructure Naming
├─ C2: Link Rotti
├─ C3: UC README
├─ C4: TROUBLESHOOTING
├─ C5: SP Titoli
└─ C6: Glossario

PHASE 2 A1 (COMPLETATO): 4-5 giorni
└─ Conformità Normativa (71 SP)

PHASE 2 A2 (PROSSIMO): 3-4 giorni
├─ Flowchart per 9 SP
├─ Sequence per 4 SP
└─ State per 11 SP

PHASE 2 A3 (PROSSIMO): 1.5-2 giorni
├─ JSON Template
└─ 5 Schema files

FASE 3 (POST-PHASE 2): 4-5 giorni
├─ M1: Pseudo-codice opzionale
├─ M2: Indici UC mancanti
└─ M3: Badge MS

TOTALE EFFORT STIMATO:
- Phase 1: 7-8 giorni ✅ DONE
- Phase 2: 8-10 giorni (A1: ✅, A2: 🔲, A3: 🔲)
- Phase 3: 4-5 giorni
- **GRAND TOTAL: 19-23 giorni vs original 25-30 (23% FASTER)**
```

---

## DELIVERY MILESTONES

### 🎯 MILESTONE 1 (Fine Novembre 2025)
- ✅ Phase 1: COMPLETE
- ✅ Phase 2 A1: COMPLETE
- 🔲 Phase 2 A2: START (Diagrammi)

### 🎯 MILESTONE 2 (Inizio Dicembre 2025)
- 🔲 Phase 2 A2: COMPLETE
- 🔲 Phase 2 A3: START (JSON Schema)

### 🎯 MILESTONE 3 (Metà Dicembre 2025)
- 🔲 Phase 2 A3: COMPLETE
- 🔲 Documentation Score: 98.8%+

### 🎯 MILESTONE 4 (Fine Dicembre 2025)
- 🔲 Phase 3 (Nice-to-have): Optional completion
- 🔲 Final Documentation Score: 99%+

---

## RACCOMANDAZIONI IMMEDIATE

### 1. **START A2 — Diagrammi Mermaid**
- Priority: ALTA
- Effort: 4 giorni
- Owner: Tech Writer + Architect
- Deliverable: 32+ nuovi diagrammi Mermaid

### 2. **FOLLOW A3 — JSON Schema**
- Priority: MEDIA
- Effort: 1.5-2 giorni
- Owner: Tech Writer + Developer
- Deliverable: 5 schema files + template

### 3. **DEFER PHASE 3** (Nice-to-have)
- M1-M3 (pseudo-codice, indici, badge) → Q1 2026
- Focus: Completare A2+A3 first

---

## CHECKLIST PRONTO ALL'USO

### ✅ PRE-WORK A2
- [ ] Review TEMPLATE-MERMAID-DIAGRAMMI.md for patterns
- [ ] Identify diagram owners (architect, tech writer)
- [ ] Schedule blocked time: 4 giorni (3 giorni fulltime, 1 giorno review)

### ✅ PRE-WORK A3
- [ ] Review existing JSON examples in SP01, SP04, SP11
- [ ] Decide schema validation tool (ajv, jsonschema, etc.)
- [ ] Create docs/schemas/ folder structure

---

**Documento Creato**: 20 novembre 2025
**Versione**: 1.0
**Status**: 🟢 READY FOR IMPLEMENTATION
**Next Reviewer**: Tech Lead / Documentation Owner
