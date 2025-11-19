# PIANO DI AZIONE AGGIORNATO - NOVEMBRE 2025

**Data Aggiornamento**: 2025-11-19
**Versione**: 2.0 (aggiornato da PIANO-REFACTORING-DOCUMENTAZIONE.md v1.0)
**Basato su**: VALUTAZIONE-QUALITA-DOCUMENTAZIONE.md (analisi completa)
**Status**: PRONTO PER IMPLEMENTAZIONE

---

## SINTESI ESECUTIVA

Il Piano di Refactoring originale (v1.0) rimane **valido e well-structured**. Questa versione (v2.0) **riprioritizza i work items** basandosi su valutazione qualitativa completa e identifica **quick wins** per ottenere risultati visibili in 1-2 settimane.

### Nuovo Score Baseline: 90.3%
Target finale: **97%+ completezza**

---

## CONFRONTO PIANO v1.0 vs v2.0

| Aspetto | v1.0 | v2.0 | Cambiamento |
|---------|------|------|------------|
| **Completezza Target** | 98%+ | 97%+ | Più realistico |
| **Timeline** | 9 settimane | 5-6 settimane | Accelerato (quick wins) |
| **Effort** | 25 giorni | 25-30 giorni | Simile (consolidato) |
| **Prioritizzazione** | 5 fasi lineari | 4 blocchi paralleli | Più flessibile |
| **Scope Psedocodice** | Completo | Opzionale | Ridotto (pratica OK) |
| **Scope Diagrammi** | Aggiunta completa | Standardizzazione | Leggero (204 presenti) |

---

## PIANO AGGIORNATO - BLOCCHI DI LAVORO PARALLELI

### BLOCCO 1: CORREZIONI CRITICHE (Settimana 1)
**Goal**: Eliminare problemi evidenti e "quick wins"
**Timeline**: 3-4 giorni
**Effort**: 3 giorni/persona
**Parallelizzazione**: Sì, 2-3 persone

#### 1.1 Correggere Typo TROUBLESHOUTING → TROUBLESHOOTING ⚡
- **File interessati**: 6 MS (MS07, MS12, MS13, etc.)
- **Task**:
  1. Rinominare file `TROUBLESHOUTING.md` → `TROUBLESHOOTING.md`
  2. Aggiornare link interni (grep + sed)
  3. Eseguire verify_links.py per verifica
  4. Commit: "Fix: Correct TROUBLESHOUTING typo in 6 microservices"
- **Owner**: Developer (1 persona)
- **Effort**: 2-4 ore
- **Impact**: Risolve 33 link rotti (58% dei problemi)
- **Validator**: `python3 scripts/verify_links.py` (target: 56→23 errori)

#### 1.2 Standardizzare Titoli SP in Italiano ⚡
- **File interessati**: ~10-15 SP (campioni: SP12, SP42, etc.)
- **Task**:
  1. Identificare titoli parzialmente/completamente inglesi
  2. Tradurre titoli mantenendo chiarezza tecnica
  3. Aggiornare sommario in INDEX.md
  4. Commit: "Refactor: Standardize SP titles to Italian"
- **Owner**: Tech Writer (1 persona)
- **Effort**: 4-6 ore
- **Impact**: Coerenza visiva + first impression users
- **Mappatura Traduzioni**:
  - "Semantic Search & Q&A Engine" → "Ricerca Semantica e Motore Q&A"
  - "Policy Engine" → "Motore di Policy Normative"
  - "Registry Suggester" → "Suggeritore di Registro"
  - "Workflow Orchestrator" → "Orchestratore di Flussi Lavoro"
  - (vs continuare con pattern IT per coerenza)

#### 1.3 Documentare Gap SP28 (Riserva Futura)
- **Task**:
  1. Creare `docs/SP28-RESERVED.md` con motivazione riserva
  2. Aggiungere nota in `docs/riepilogo_casi_uso.md`
  3. Commit: "Docs: Document SP28 reserved gap"
- **Owner**: Tech Writer (0.5 persona)
- **Effort**: 2 ore
- **Impact**: Chiarezza architetturale

**Deliverables Blocco 1**:
- ✅ 0 typo TROUBLESHOUTING residui
- ✅ 10-15 titoli SP in italiano
- ✅ SP28 documentato
- ✅ Link rotti ridotti da 56 → ~23

---

### BLOCCO 2: QUALITÀ CONTENUTI (Settimane 2-3)
**Goal**: Standardizzare linguaggio, normative, JSON schema
**Timeline**: 6-7 giorni
**Effort**: 6-7 giorni/persona
**Parallelizzazione**: Sì, 2-3 persone

#### 2.1 Creare GLOSSARIO-TERMINOLOGICO.md ⚡
- **Task**:
  1. Scansionare documentazione per 50+ termini ricorrenti EN/IT
  2. Decidere standard: quando usare EN vs IT
  3. Creare `docs/GLOSSARIO-TERMINOLOGICO.md` con:
     - Definizione italiana
     - Termine inglese equivalente
     - Quando usare quale (con esempi)
     - Abbreviazioni standard
  4. Aggiungere link in `docs/INDEX.md`
- **Owner**: Tech Writer (1 persona)
- **Effort**: 1-2 giorni
- **Termini da Decidere** (campioni):

  | EN | IT | Decisione |
  |----|----|----|
  | policy | politica / norma | policy (uso IT per ambito "policy engine") |
  | workflow | flusso di lavoro | flusso di lavoro (standardizzare) |
  | enforcement | applicazione / forza | applicazione (standardizzare) |
  | intent | intento / proposito | intento (per ML context) |
  | query | ricerca / interrogazione | ricerca (standardizzare) |
  | dashboard | cruscotto / pannello | cruscotto (standardizzare) |
  | AI | IA | IA (italiana) con possibile "AI" in contesti tecnici EN |
  | Q&A | D&R | D&R (italiano) |
  | API | API | API (mantenerlo, termine tecnico universale) |
  | JSON | JSON | JSON (mantenerlo) |
  | REST | REST | REST (mantenerlo) |
  | Cache | Cache | Cache (mantenerlo) |

- **Deliverable**: `docs/GLOSSARIO-TERMINOLOGICO.md` (50+ termini + policy)

#### 2.2 Aggiungere Conformità Normativa Standard a Tutti gli SP
- **Task**:
  1. Creare template "Conformità Normativa" standardizzato:
     ```markdown
     ## Conformità Normativa

     ### Normative Principali
     - **CAD** (Codice Amministrazione Digitale): Art. XX
     - **GDPR/RGPD**: Art. XX (se applicabile)
     - **eIDAS**: Art. XX (se applicabile)
     - **AGID**: Linea guida XX

     ### Standard Tecnici
     - [Se applicabili]

     ### Linee Guida
     - [Se applicabili]
     ```
  2. Aggiungere sezione a 72 SP (priorità: UC1, UC5, UC6, UC7, UC9, UC11 prima)
  3. Commit: "Docs: Add standard legal compliance section to SP"
- **Owner**: Tech Writer + Legal/Compliance Expert (2 persone)
- **Effort**: 3-4 giorni
- **Impact**: Tracciabilità normativa per PA/compliance reviews
- **Validator**: Grep per "Conformità Normativa" in tutti gli SP

#### 2.3 Standardizzare Payload JSON - Creare Template
- **Task**:
  1. Analizzare pattern JSON attuali (SP01, SP04, SP10 come ref)
  2. Creare `docs/templates/json-payload-standard.md` con:
     - Struttura request standard
     - Struttura response standard
     - Error responses (400, 422, 503, etc.)
     - Convenzioni naming (snake_case vs camelCase decision)
     - Campo timestamp, request_id, metadata
  3. Aggiungere nota nei SP: "Vedi [Template JSON Standard](../templates/json-payload-standard.md)"
  4. Commit: "Docs: Add JSON payload standard template"
- **Owner**: Developer + Tech Writer (1.5 persone)
- **Effort**: 1-2 giorni
- **Deliverable**: `docs/templates/json-payload-standard.md` + reference in SP critici

**Deliverables Blocco 2**:
- ✅ GLOSSARIO-TERMINOLOGICO.md creato (50+ termini)
- ✅ 72 SP con sezione "Conformità Normativa"
- ✅ JSON payload standard template creato
- ✅ Score qualità linguistica: 85% → 92%

---

### BLOCCO 3: NAVIGAZIONE E LINKING (Settimane 4-5)
**Goal**: Migliorare accessibilità e eliminare link residui
**Timeline**: 5-6 giorni
**Effort**: 5-6 giorni/persona
**Parallelizzazione**: Sì, 2 persone

#### 3.1 Standardizzare e Completare Diagrammi Mermaid
- **Task**:
  1. Identificare SP critici con <2 diagrammi (~15-20 SP)
  2. Per ogni SP, aggiungere:
     - **Flowchart architetturale** (component interaction) se manca
     - **Sequence diagram** (main flow) se manca
     - **State diagram** (per workflow-heavy SP) se applicabile
  3. Standardizzare formato/colori Mermaid
  4. Commit: "Docs: Standardize Mermaid diagrams in critical SP"
- **Owner**: Architect + Tech Writer (1.5 persone)
- **Effort**: 3-4 giorni
- **Impact**: Uniformità visiva, facilita comprensione

#### 3.2 Aggiungere UC INDEX Centrali Mancanti
- **Task**:
  1. Per ogni UC (UC1-UC11), creare `00 INDEX.md` con:
     - Overview UC (2-3 paragrafi)
     - Tabella SP con link e descrizione 1-line
     - Matrice dipendenze (SP → MS mapping)
     - Link a architettura, guide, normative
  2. Aggiornare `docs/use_cases/README.md` con link a tutti INDEX
  3. Commit: "Docs: Add central INDEX to all UC folders"
- **Owner**: Tech Writer (1 persona)
- **Effort**: 2 giorni
- **Impact**: Navigation hub per developers

#### 3.3 Verificare e Correggere Link Residui
- **Task**:
  1. Eseguire verify_links.py
  2. Analizzare 23 link rotti residui (dopo fix TROUBLESHOUTING)
  3. Determinare se sono:
     - Template intenzionali (es. `../path/to/SP02.md`) → aggiungere commento
     - Link a file effettivamente mancanti → creare file o rimuovere link
     - Link generici → specificare
  4. Commit: "Docs: Fix remaining broken links"
- **Owner**: Developer (0.5 persona)
- **Effort**: 1 giorno
- **Target**: 23 → 0 link rotti

**Deliverables Blocco 3**:
- ✅ Diagrammi Mermaid standardizzati (200+ diagrammi, 100% coerenza)
- ✅ 11 UC INDEX creati/aggiornati
- ✅ 0 link rotti residui
- ✅ Score accessibilità: 75% → 95%

---

### BLOCCO 4: MIGLIORAMENTI AVANZATI (Settimane 6+, Opzionale)
**Goal**: Completeness e automazione avanzata
**Timeline**: 3-4 giorni (opzionale)
**Effort**: 3-4 giorni/persona
**Parallelizzazione**: Sì, 2 persone

#### 4.1 Aggiungere JSON Schema Formale a SP Critici (Opzionale)
- **Task**:
  1. Per SP01, SP07, SP12, SP29, SP42 creare:
     - File `SCHEMA.json` con JSON Schema per request/response
     - Link da SPECIFICATION.md a schema
  2. Commit: "Docs: Add JSON Schema to critical SP"
- **Owner**: Developer (1 persona)
- **Effort**: 1-2 giorni
- **Impact**: Validation e type safety documentation

#### 4.2 Aggiungere Badge Status e Quick Start a MS (Opzionale)
- **Task**:
  1. Per ogni MS (MS01-MS16), aggiungere in README.md:
     ```markdown
     ![Status](https://img.shields.io/badge/status-production-green)
     ![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
     ![Docs](https://img.shields.io/badge/docs-updated-blue)
     ```
  2. Aggiungere "Quick Start" section (5 min usage)
- **Owner**: Automation Engineer (1 persona)
- **Effort**: 1 giorno

#### 4.3 Creare DOCUMENTATION-MAINTENANCE.md (Opzionale)
- **Task**:
  1. Documentare processo manutenzione:
     - Come aggiungere nuovo SP
     - Checklist per SP completion
     - Processo review documentation
     - Cadenza aggiornamenti (trimestrale?)
  2. Commit: "Docs: Add maintenance guide"
- **Owner**: Tech Writer (1 persona)
- **Effort**: 1 giorno

**Deliverables Blocco 4** (se implementato):
- ✅ JSON Schema formale per SP critici
- ✅ Badge status MS
- ✅ Maintenance guide creato

---

## TIMELINE CONSOLIDATA

```
SETTIMANA 1 (19-25 novembre):
├─ Lunedì 19-20: Kickoff + Blocco 1 start
├─ Mercoledì 21-22: Blocco 1 completamento + Blocco 2 start
├─ Venerdì 24-25: Checkpoint; Blocco 1-2 QA
└─ Weekend: Review stakeholder

SETTIMANA 2 (26 nov - 2 dic):
├─ Lunedì 26: Blocco 2 continuazione
├─ Mercoledì 28: Blocco 2 completamento + Blocco 3 start
├─ Venerdì 1 dic: Checkpoint; Blocco 2-3 QA
└─ Weekend: Team sync

SETTIMANA 3 (3-9 dic):
├─ Lunedì 3: Blocco 3 continuazione
├─ Mercoledì 5: Blocco 3 completamento
├─ Venerdì 7: Checkpoint; Blocco 3 QA + Blocco 4 opzionale start
└─ Fine settimana: Preparation for go-live

SETTIMANA 4 (10-16 dic):
├─ Blocco 4 (opzionale) completamento
├─ Final QA e stakeholder review
├─ Preparation merge `docs/refactoring` → `main`
└─ Go-Live: 17 dicembre 2025

TOTALE: ~4 settimane (accelerato da v1.0: 9 settimane)
```

---

## METRICHE DI SUCCESSO - CHECKPOINTS

### Checkpoint 1 (Fine Settimana 1)
- ✅ 33 link rotti TROUBLESHOUTING fixed
- ✅ 10-15 titoli SP in italiano
- ✅ SP28 documentato
- **Expected Impact**: Link validi 541 → 574 (50/56 fixed)

### Checkpoint 2 (Fine Settimana 2)
- ✅ GLOSSARIO-TERMINOLOGICO.md creato
- ✅ 36+ SP con conformità normativa (50%)
- ✅ JSON template standardizzato
- **Expected Impact**: Score qualità linguistica: 85% → 90%

### Checkpoint 3 (Fine Settimana 3)
- ✅ Diagrammi Mermaid standardizzati
- ✅ 11 UC INDEX creati
- ✅ 23 link residui fixed
- **Expected Impact**: Link validi 100%, navigazione 95%

### Checkpoint 4 (Fine Settimana 4)
- ✅ Blocchi 1-4 completati/validati
- ✅ VALIDATION-CHECKLIST.md aggiornato
- ✅ Merge `docs/refactoring` → `main`
- **Final Score**: 90.3% → 97%+

---

## TEAM E ASSEGNAZIONI

| Ruolo | Effort | Persona | Blocchi |
|-------|--------|---------|---------|
| **Tech Writer** | 8-10 giorni | 1 FTE | 1.2, 1.3, 2.1, 2.2, 3.2, 4.3 |
| **Developer** | 6-8 giorni | 1 FTE (part-time) | 1.1, 2.3, 3.3, 4.1 |
| **Architect/Domain Expert** | 3-4 giorni | 1 consulente | 2.2 (normi), 3.1 (diagrams) |
| **Automation Engineer** | 1 giorno | 0.1 FTE | 4.2 (opzionale) |
| **QA/Review** | 2-3 giorni | 1 FTE | Tutti blocchi |

**Cost Estimate**: ~25-30 giorni/persona = ~1.5-2 FTE per 4 settimane

---

## RISCHI E MITIGAZIONI

| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|--------|------------|
| Titoli SP non completamente tradotti | MEDIA | BASSO | Review checklist con glossario |
| Link residui ancora rotti dopo fix | MEDIA | BASSO | Eseguire verify_links.py 2x |
| Conformità normativa incompleta | MEDIA | MEDIO | Template checklist + expert review |
| Diagrammi Mermaid inconsistenti | MEDIA | BASSO | Standardizzare colori/formato |
| Team bandwidth limitato | ALTA | ALTO | Parallelizzare blocchi; prioritizzare C1 |

---

## SUCCESS CRITERIA FINALE

### Score Baseline vs Target

| Metrica | Baseline | Target | Raggiunto |
|---------|----------|--------|-----------|
| Completezza Strutturale | 96.8% | 98%+ | ✅ (97%+) |
| Qualità Linguistica | 85% | 95% | ✅ (92%+) |
| Conformità Normativa | 60% (SP) | 90%+ | ✅ (85%+) |
| Link Validi | 90% | 100% | ✅ (99%+) |
| Diagrammi | 87% | 100% | ✅ (100%) |
| **SCORE COMPLESSIVO** | **90.3%** | **97%+** | ✅ **96%+** |

### Go-Live Criteria
- ✅ 0 link rotti
- ✅ 100% SP con conformità normativa
- ✅ Glossario EN/IT standardizzato
- ✅ CI/CD pipeline verde (all tests pass)
- ✅ Stakeholder sign-off

---

## PROSSIMI STEP IMMEDIATI

1. **Approvazione Piano** (Oggi)
   - Review e feedback stakeholder
   - Approvazione timeline e team

2. **Kickoff Ufficiale** (Giovedì 20 novembre)
   - Team sync 1h: review blocchi, assegnazioni, tools
   - Setup branch: `git checkout -b docs/refactoring`
   - Slack channel: `#zenia-docs-refactoring`

3. **Inizio Lavori Blocco 1** (Venerdì 21 novembre)
   - Inizio C1 (TROUBLESHOUTING fix): Developer
   - Inizio C2 (Titoli SP italiano): Tech Writer
   - Inizio C3 (SP28 doc): Tech Writer

4. **Weekly Sync** (Ogni venerdì ore 15:00)
   - Progress update
   - Blockers resolution
   - Scope adjustments if needed

---

## DOCUMENTO DI RIFERIMENTO

**Piano Originale**: `docs/PIANO-REFACTORING-DOCUMENTAZIONE.md` (v1.0)
**Valutazione Qualità**: `docs/VALUTAZIONE-QUALITA-DOCUMENTAZIONE.md` (v1.0)
**Script Validazione**: `scripts/verify_*.py` (3 script attivi)

---

**Coordinatore Refactoring**: [TBD - da assegnare]
**Data Approazione**: [TBD]
**Target Go-Live**: 17 Dicembre 2025

