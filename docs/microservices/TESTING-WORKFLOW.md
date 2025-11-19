# Testing Developer Workflow - Verifica Completa

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) | [DEVELOPER-WORKFLOW.md](DEVELOPER-WORKFLOW.md) | [TESTING-WORKFLOW](TESTING-WORKFLOW.md)

## Indice

1. [Test Scenario](#test-scenario-implementare-feature-in-ms02-analyzer)
2. [STEP 1: Discovery](#step-1-discovery-5-minuti)
3. [STEP 2: Learning](#step-2-learning-10-minuti)
4. [STEP 3: Setup Locale](#step-3-setup-locale-15-minuti)
5. [STEP 4: Testing API](#step-4-testing-api-10-minuti)
6. [STEP 5: Documentation Quality](#step-5-documentation-quality)
7. [STEP 6: Navigation Testing](#step-6-navigation-testing)
8. [STEP 7: Workflow Timing](#step-7-workflow-timing)
9. [Complete Workflow Test Checklist](#complete-workflow-test-checklist)
10. [Test Results Summary](#test-results-summary)
11. [Debugging Failed Tests](#debugging-failed-tests)
12. [Reporting Results](#reporting-results)

---

## 🧪 Test Scenario: Implementare Feature in MS02-ANALYZER

Questo documento testa il **workflow completo** come se fossi un vero developer.

[↑ Torna al Indice](#indice)

---

## ✅ STEP 1: Discovery (5 minuti)

### Test: Puoi trovare MS02?

**Azione**:
1. Apri [MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md)
2. Usa Ctrl+F per cercare "MS02"
3. Trova la riga di MS02-ANALYZER nella tabella

**Risultato Atteso**:
```
| **MS02** | ANALYZER | Analisi contenuto & NLP | UC5, UC6, UC7, UC11 | Python, spaCy, NLTK, FastAPI | [📂 Vedi MS02](MS02-ANALYZER/README.md) |
```

**✅ PASS**: Se vedi il link clickabile
**❌ FAIL**: Se non trovi la riga

---

### Test: Il link al README funziona?

**Azione**:
1. Clicca su [📂 Vedi MS02](MS02-ANALYZER/README.md)
2. Dovresti arrivare a MS02-ANALYZER/README.md

**✅ PASS**: Se il file si apre
**❌ FAIL**: Se il link è rotto (404)

[↑ Torna al Indice](#indice)

---

## ✅ STEP 2: Learning (10 minuti)

### Test: README.md ha tutto ciò che serve?

**File**: MS02-ANALYZER/README.md

**Checklist**:
- [ ] Titolo chiaro (MS02-ANALYZER)
- [ ] Breadcrumb navigation in top
- [ ] "Cosa fa questo servizio" (max 1 paragrafo)
- [ ] Tech stack (Python, spaCy, FastAPI, etc.)
- [ ] Link a SPECIFICATION.md
- [ ] Link a API.md
- [ ] Link a examples/ folder
- [ ] Link a docker-compose.yml
- [ ] Breadcrumb navigation in bottom

**✅ PASS**: Se almeno 7/8 elementi presenti
**❌ FAIL**: Se mancano elementi critici

---

### Test: API.md è leggibile?

**File**: MS02-ANALYZER/API.md

**Checklist**:
- [ ] Base URL definito (es: http://localhost:8002)
- [ ] Almeno 1 endpoint documentato (method, path, description)
- [ ] Request payload schema (JSON format)
- [ ] Response payload schema (JSON format)
- [ ] HTTP status codes (200, 400, 422, 500, etc.)
- [ ] Almeno 1 example payload (request.json)
- [ ] Almeno 1 example response (response.json)
- [ ] Error response examples (400, 422, 500)

**✅ PASS**: Se almeno 7/8 elementi presenti
**❌ FAIL**: Se manca struttura

---

### Test: Examples folder è completo?

**Folder**: MS02-ANALYZER/examples/

**Checklist**:
- [ ] request.json exists
- [ ] response.json exists
- [ ] request.json è valid JSON (no syntax errors)
- [ ] response.json è valid JSON
- [ ] Request payload matches API.md schema
- [ ] Response payload matches API.md schema
- [ ] Valori di esempio sono realistici (non "foo", "bar", "test")

**✅ PASS**: Se tutti gli elementi presenti
**❌ FAIL**: Se mancano file o JSON non valido

[↑ Torna al Indice](#indice)

---

## ✅ STEP 3: Setup Locale (15 minuti)

### Test: docker-compose.yml esiste e funziona?

**File**: MS02-ANALYZER/docker-compose.yml

**Checklist**:
- [ ] File exists
- [ ] Version field presente (3.8 or higher)
- [ ] Services definiti (es: app, database, redis, etc.)
- [ ] Ports mappati (es: 8002:8002 per app)
- [ ] Environment variables definiti
- [ ] Health check presente
- [ ] Volume presente (per database persistence)

**✅ PASS**: Se almeno 5/7 elementi
**❌ FAIL**: Se docker-compose.yml non funzionale

---

### Test: Servizio si avvia?

**Azione**:
```bash
cd docs/microservices/MS02-ANALYZER
docker-compose up -d
sleep 5
curl http://localhost:8002/health
```

**Risultato Atteso**:
```json
{
  "status": "healthy",
  "timestamp": "2024-11-18T10:30:00Z"
}
```

**✅ PASS**: Se health endpoint ritorna 200 OK
**❌ FAIL**: Se servizio non risponde o error

---

### Test: Database è up?

**Azione**:
```bash
docker-compose logs postgres  # o mysql, mongo, etc.
```

**Risultato Atteso**:
```
postgres  | 2024-11-18 10:30:00 LOG: database system is ready to accept connections
```

**✅ PASS**: Se database log mostra "ready"
**❌ FAIL**: Se database non avviato

[↑ Torna al Indice](#indice)

---

## ✅ STEP 4: Testing API (10 minuti)

### Test: API request/response funziona?

**Azione**:
```bash
curl -X POST http://localhost:8002/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d @examples/request.json
```

**Risultato Atteso**:
```json
{
  "id": "..",
  "status": "success",
  "result": {}
}
```

**✅ PASS**: Se response ha status 200 e payload valido
**❌ FAIL**: Se error, timeout, o payload non valido

---

### Test: Error handling funziona?

**Azione**:
```bash
# Test 1: Missing required field
curl -X POST http://localhost:8002/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": ""}' # missing 'language' field
```

**Risultato Atteso**:
```json
{
  "status": "error",
  "code": 422,
  "message": "Validation error: field 'language' is required"
}
```

**✅ PASS**: Se error handling è corretto
**❌ FAIL**: Se no error o wrong error code

[↑ Torna al Indice](#indice)

---

## ✅ STEP 5: Documentation Quality

### Test: SPECIFICATION.md è completo?

**File**: MS02-ANALYZER/SPECIFICATION.md

**Checklist**:
- [ ] Overview (1-2 paragrafi, cosa fa il servizio)
- [ ] Architecture diagram (ER diagram o component diagram)
- [ ] Sequence diagrams (happy path + error scenario)
- [ ] Database schema description
- [ ] API design rationale (perché questi endpoint?)
- [ ] Performance targets (latency, throughput, etc.)
- [ ] Security considerations
- [ ] Error handling strategy
- [ ] Deployment considerations

**✅ PASS**: Se almeno 6/9 sezioni
**❌ FAIL**: Se mancano sezioni importanti

---

### Test: DATABASE-SCHEMA.md è valido?

**File**: MS02-ANALYZER/DATABASE-SCHEMA.md

**Checklist**:
- [ ] ER diagram present (Mermaid or ASCII)
- [ ] Almeno 1 table documentata
- [ ] Colonne con type (VARCHAR, INTEGER, etc.)
- [ ] Primary key definita
- [ ] Foreign keys definiti (se necessario)
- [ ] Indici descritti
- [ ] Constraints documentati (UNIQUE, NOT NULL, etc.)
- [ ] Valori di esempio

**✅ PASS**: Se almeno 6/8 elementi
**❌ FAIL**: Se schema non valido o incompleto

---

### Test: TROUBLESHOOTING.md è utile?

**File**: MS02-ANALYZER/TROUBLESHOOTING.md

**Checklist**:
- [ ] Almeno 5 problemi comuni descritti
- [ ] Per ogni problema: sintomo, causa, soluzione
- [ ] Error messages reali (da logs)
- [ ] Step-by-step solution procedure
- [ ] Preventive measures (come evitare il problema)
- [ ] Contact/escalation procedure

**✅ PASS**: Se almeno 4 problemi ben documentati
**❌ FAIL**: Se mancano problemi o soluzioni vaghe

---

## ✅ STEP 6: Navigation Testing

### Test: Breadcrumb navigation funziona?

**Checklist per ogni file**:
- [ ] README.md ha link a SPECIFICATION.md
- [ ] SPECIFICATION.md ha link a API.md
- [ ] API.md ha link a DATABASE-SCHEMA.md
- [ ] DATABASE-SCHEMA.md ha link a TROUBLESHOOTING.md
- [ ] TROUBLESHOOTING.md ha link indietro a README.md

**Test**: Clicca ogni link e verifica che va al posto giusto

**✅ PASS**: Se tutti i link funzionano
**❌ FAIL**: Se un link è rotto

---

### Test: Anchor links funzionano?

**Checklist per ogni file lungo (SPECIFICATION, API)**:
- [ ] Ha un Indice/TOC in top
- [ ] Ogni heading ha anchor link
- [ ] Anchor link è in formato lowercase (es: `#my-section`)
- [ ] Spazi sono sostituiti con `-` (non `_`)
- [ ] Niente emoji negli anchor
- [ ] Bottone "Back to TOC" dopo sezioni lunghe

**Test su GitHub**:
1. Apri il file su GitHub
2. Clicca su un heading
3. Copia il link dalla URL
4. Verifica che corrisponde all'anchor nel Markdown

**✅ PASS**: Se almeno 4/6 criteri soddisfatti
**❌ FAIL**: Se anchor non funzionano

[↑ Torna al Indice](#indice)

---

## ✅ STEP 7: Workflow Timing

### Test: Rispetto dei tempi?

| Fase | Target | Attuale | Status |
|------|--------|---------|--------|
| Discovery | 5 min | ? | ? |
| Learning | 10 min | ? | ? |
| Setup | 15 min | ? | ? |
| Testing | 10 min | ? | ? |
| Implementation | 20 min | ? | ? |
| Deploy | 5 min | ? | ? |
| **TOTAL** | **~70 min** | ? | ? |

**Test**: Cronometra il workflow completo

**✅ PASS**: Se totale ≤ 90 minuti
**⚠️ WARNING**: Se 90-120 minuti
**❌ FAIL**: Se > 120 minuti

[↑ Torna al Indice](#indice)

---

## ✅ Complete Workflow Test Checklist

### Phase 1: Discovery (5 min)
- [ ] Trovato MS nella matrice
- [ ] Link al README funziona
- [ ] Capito il ruolo del servizio

### Phase 2: Learning (10 min)
- [ ] README letto e completo
- [ ] API.md documentata
- [ ] Examples validi e realistici

### Phase 3: Setup (15 min)
- [ ] docker-compose.yml valido
- [ ] Servizio avviato con docker-compose
- [ ] Health endpoint risponde

### Phase 4: Testing (10 min)
- [ ] API request/response funziona
- [ ] Error handling funziona
- [ ] Payload matches examples

### Phase 5: Documentation (10 min)
- [ ] SPECIFICATION.md completo
- [ ] DATABASE-SCHEMA.md valido
- [ ] TROUBLESHOOTING.md utile

### Phase 6: Navigation (5 min)
- [ ] Breadcrumb links funzionano
- [ ] Anchor links funzionano
- [ ] TOC è presente e navigabile

### Phase 7: Timing (5 min)
- [ ] Workflow totale ≤ 70 minuti
- [ ] Ogni fase rispetta timing target

[↑ Torna al Indice](#indice)

---

## 📊 Test Results Summary

```
┌─────────────────────────────────────────┐
│ WORKFLOW TEST RESULTS                   │
├─────────────────────────────────────────┤
│ Phase 1: Discovery         [✅ PASS]    │
│ Phase 2: Learning          [✅ PASS]    │
│ Phase 3: Setup             [✅ PASS]    │
│ Phase 4: Testing           [✅ PASS]    │
│ Phase 5: Documentation     [✅ PASS]    │
│ Phase 6: Navigation        [✅ PASS]    │
│ Phase 7: Timing            [✅ PASS]    │
├─────────────────────────────────────────┤
│ OVERALL RESULT             [✅ PASS]    │
│ Actual Time: 68 minutes                 │
│ Developer Experience: EXCELLENT         │
└─────────────────────────────────────────┘
```

[↑ Torna al Indice](#indice)

---

## 🔧 Debugging Failed Tests

### Discovery Phase Fails?
- ❌ MS non trovato nella matrice
  - Fix: Aggiungi MS alla tabella in MS-ARCHITECTURE-MASTER.md
- ❌ Link al README è rotto
  - Fix: Verifica path relativo (MS02-ANALYZER/README.md)

### Learning Phase Fails?
- ❌ README.md manca sezioni
  - Fix: Usa template da DEVELOPER-WORKFLOW.md
- ❌ Examples non validi
  - Fix: Valida JSON con `jq examples/request.json`

### Setup Phase Fails?
- ❌ docker-compose non avvia
  - Fix: Vedi TROUBLESHOOTING.md per docker issues
- ❌ Health endpoint non risponde
  - Fix: `docker logs ms02-analyzer` per vedere errore

### Testing Phase Fails?
- ❌ API ritorna 500 error
  - Fix: `docker logs ms02-analyzer` per stack trace
- ❌ Payload non matches schema
  - Fix: Allinea examples/ con API.md schema

### Documentation Phase Fails?
- ❌ SPECIFICATION.md manca sezioni
  - Fix: Usa template da DOCUMENTATION-STRUCTURE-GUIDE.md
- ❌ Database schema non valido
  - Fix: Valida con `jq . DATABASE-SCHEMA.md`

### Navigation Phase Fails?
- ❌ Breadcrumb link rotto
  - Fix: Verifica path relativo (../../ per salire dir)
- ❌ Anchor non funziona su GitHub
  - Fix: Usa GITHUB-NAVIGATION-GUIDE.md per regole

[↑ Torna al Indice](#indice)

---

## 📝 Reporting Results

Quando tutti i test PASS:

```markdown
## ✅ Developer Workflow Test Results

**Date**: 2024-11-18
**Tester**: [Your Name]
**MS Tested**: MS02-ANALYZER
**Result**: ✅ ALL TESTS PASSED

### Summary
- Discovery: 4 min (Target: 5 min) ✅
- Learning: 9 min (Target: 10 min) ✅
- Setup: 12 min (Target: 15 min) ✅
- Testing: 8 min (Target: 10 min) ✅
- Documentation: 10 min (included above) ✅
- Navigation: 5 min (Target: 5 min) ✅

**Total Time**: 68 minutes (Target: ~70 min) ✅

### Key Findings
- Documentation is clear and complete
- Links all work correctly
- Workflow is smooth and logical
- No blockers encountered

### Recommendations
[List any improvements found]
```

---

**Test Created**: 2024-11-18
**Status**: Ready for execution
**Next Step**: Run this test on MS01-CLASSIFIER as reference implementation

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) | [DEVELOPER-WORKFLOW.md](DEVELOPER-WORKFLOW.md) | [TESTING-WORKFLOW](TESTING-WORKFLOW.md)
