# UC File Renaming Strategy — Standardization Plan

**Data**: 20 novembre 2025
**Versione**: 1.0
**Stato**: READY FOR IMPLEMENTATION
**Impact**: Tutti i 11 UC, ~120 file da rinominare

---

## Executive Summary

Razionalizziamo la nomenclatura dei file nelle cartelle Use Case (UC1-UC11) eliminando i **prefissi numerici duplicati** (01, 02, 03...) e introducendo un **archetipo standard** che facilita la navigazione e la separazione chiara tra:
- 📄 Documenti di architettura UC
- 📋 Documentazione SP (sottoprogetti)
- 🔀 Diagrammi sequence
- 🔗 Matrici dipendenze
- 📖 Guide operative
- 📑 Documenti supplementari

---

## Il Problema Attuale

### Inconsistenze Critiche Identificate

1. **Prefisso "01" Usato Doppiamente**
   ```
   ❌ 01 SP03 - Classificatore Procedurale.md      (SP documentation)
   ❌ 01 Sequence diagrams.md                       (Sequence diagram)
   → Ambiguità di ordering in GitHub
   ```

2. **UC10 Non Segue Standard**
   ```
   ❌ 02 Sequence Diagrams UC10.md                 (should be 01 or 03)
   ❌ 03 Dependency Matrix UC10.md                 (should be 02 or 04)
   ```

3. **UC5 Usa Nomi Non-Standard**
   ```
   ❌ 01 CANONICAL - Generazione Atto Completo.md     (non-standard prefix)
   ❌ 02 SUPPLEMENTARY - Overview Semplificato.md      (inconsistent)
   ❌ 03 SUPPLEMENTARY - Ultra Semplificato.md         (numbering jump)
   ```

4. **SP Duplicati Across UCs**
   ```
   ❌ UC2 + UC5 hanno entrambi SP01
   ❌ UC1 + UC5 hanno entrambi SP02 e SP07
   ```

---

## Soluzione: Archetipo Standard

### Nuovo Schema di Nomenclatura

```
Per ogni UC cartella:

00-ARCHITECTURE.md                              # Architecture overview
01-OVERVIEW.md                                  # Business/functional overview
02-DEPENDENCIES.md                              # Dependency matrix
03-SEQUENCES.md                                 # Sequence diagrams (if applicable)
04-GUIDE.md                                     # Operational guide
05-HITL.md                                      # Human-in-the-loop (if applicable)

SP/                                             # ← Sottocartella separata
├── SP##-Name.md                                # SP documentation (sorted numerically)
└── (or as separate files in root with SP-NN prefix)

SUPPLEMENTARY/                                  # ← Sottocartella per docs aggiuntivi
├── CANONICAL-Complete-Flow.md
├── OVERVIEW-Simplified.md
└── OVERVIEW-Ultra-Simplified.md

README.md                                       # Index (standard)
```

### Vantaggi

✅ **Numerazione Logica** — 00, 01, 02... senza duplicati
✅ **Separazione Chiara** — SP docs separati dalla UC documentation
✅ **GitHub-Friendly** — Ordine alfabetico naturale
✅ **Scalabilità** — Facile aggiungere nuovi doc senza conflitti
✅ **Uniformità** — Stesso archetipo per tutte le 11 UC
✅ **Navigazione Intuitiva** — Chiaro il tipo di documento dal numero

---

## Dettagli Renaming per UC

### UC1 - Sistema di Gestione Documentale

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura Generale UC1.md | 00-ARCHITECTURE.md | Architecture |
| 01 SP02 - ... | SP/01-Document-Extractor.md | SP Documentation |
| 01 SP07 - ... | SP/02-Content-Classifier.md | SP Documentation |
| 01 SP12 - ... | SP/03-Semantic-Search.md | SP Documentation |
| 01 SP13 - ... | SP/04-Document-Summarizer.md | SP Documentation |
| 01 SP14 - ... | SP/05-Metadata-Indexer.md | SP Documentation |
| 01 SP15 - ... | SP/06-Document-Workflow-Orchestrator.md | SP Documentation |
| 01 Sequence - Document Processing Completo.md | 03-SEQUENCES.md | Sequences |
| 01 Sequence - Overview Semplificato.md | 03-SEQUENCES-SIMPLIFIED.md | Sequences |
| 01 Sequence - Ultra Semplificato.md | 03-SEQUENCES-ULTRA-SIMPLIFIED.md | Sequences |
| 02 Matrice Dipendenze... | 02-DEPENDENCIES.md | Dependencies |
| Guida_UC1_... | 04-GUIDE.md | Guide |
| README.md | README.md | Index |

**Note**:
- SP files rinumerati localmente (01-06 within UC1 context, not global SP numbers)
- Sequence diagrams consolidati in uno o tre file distinti

---

### UC2 - Protocollo Informatico

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura Generale UC2.md | 00-ARCHITECTURE.md | Architecture |
| 01 SP01 - Parser EML... | SP/01-EML-Parser.md | SP Documentation |
| 01 SP16 - ... | SP/02-Correspondence-Classifier.md | SP Documentation |
| 01 SP17 - ... | SP/03-Registry-Suggester.md | SP Documentation |
| 01 SP18 - ... | SP/04-Anomaly-Detector.md | SP Documentation |
| 01 SP19 - ... | SP/05-Protocol-Workflow-Orchestrator.md | SP Documentation |
| 01 Sequence diagrams.md | 03-SEQUENCES.md | Sequences |
| 02 Matrice Dipendenze.md | 02-DEPENDENCIES.md | Dependencies |
| Guida_UC2_... | 04-GUIDE.md | Guide |
| README.md | README.md | Index |

---

### UC3 - Governance

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura UC3.md | 00-ARCHITECTURE.md | Architecture |
| 01 SP20 - ... | SP/01-Organization-Chart-Manager.md | SP Doc |
| 01 SP21 - ... | SP/02-Procedure-Manager.md | SP Doc |
| 01 SP22 - ... | SP/03-Process-Governance.md | SP Doc |
| 01 SP23 - ... | SP/04-Compliance-Monitor.md | SP Doc |
| 01 Sequence diagrams.md | 03-SEQUENCES.md | Sequences |
| 02 Matrice Dipendenze.md | 02-DEPENDENCIES.md | Dependencies |
| Guida_UC3_... | 04-GUIDE.md | Guide |
| README.md | README.md | Index |

---

### UC4 - BPM e Automazione Processi

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura UC4.md | 00-ARCHITECTURE.md | Architecture |
| 00 SP28-RESERVED.md | RESERVED-SP28.md | Reserved |
| 01 SP24 - ... | SP/01-Process-Mining-Engine.md | SP Doc |
| 01 SP25 - ... | SP/02-Forecasting-Predictive.md | SP Doc |
| 01 SP26 - ... | SP/03-Intelligent-Workflow-Designer.md | SP Doc |
| 01 SP27 - ... | SP/04-Process-Analytics.md | SP Doc |
| 01 Sequence diagrams.md | 03-SEQUENCES.md | Sequences |
| 02 Matrice Dipendenze.md | 02-DEPENDENCIES.md | Dependencies |
| Guida_UC4_... | 04-GUIDE.md | Guide |
| README.md | README.md | Index |

---

### UC5 - Produzione Documentale Integrata (MOST COMPLEX)

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura Generale Microservizi.md | 00-ARCHITECTURE.md | Architecture |
| 01 CANONICAL - ... | SUPPLEMENTARY/CANONICAL-Complete-Flow.md | Canonical |
| 01 SP01 - ... | SP/01-EML-Parser.md | SP Doc |
| 01 SP02 - ... | SP/02-Document-Extractor.md | SP Doc |
| 01 SP03 - ... | SP/03-Procedural-Classifier.md | SP Doc |
| 01 SP04 - ... | SP/04-Knowledge-Base.md | SP Doc |
| 01 SP05 - ... | SP/05-Template-Engine.md | SP Doc |
| 01 SP06 - ... | SP/06-Validator.md | SP Doc |
| 01 SP07 - ... | SP/07-Content-Classifier.md | SP Doc |
| 01 SP08 - ... | SP/08-Quality-Checker.md | SP Doc |
| 01 SP09 - ... | SP/09-Workflow-Engine.md | SP Doc |
| 01 SP10 - ... | SP/10-Dashboard.md | SP Doc |
| 01 SP11 - ... | SP/11-Security-Audit.md | SP Doc |
| 02 Matrice Dipendenze... | 02-DEPENDENCIES.md | Dependencies |
| 02 SUPPLEMENTARY - Overview Semplificato.md | SUPPLEMENTARY/OVERVIEW-Simplified.md | Supplementary |
| 02 Sottoprogetti con Pipeline... | 01-OVERVIEW.md | Overview |
| 03 Human in the Loop... | 05-HITL.md | HITL |
| 03 SUPPLEMENTARY - Ultra Semplificato.md | SUPPLEMENTARY/OVERVIEW-Ultra-Simplified.md | Supplementary |
| Guida_Generazione_Atti... | 04-GUIDE.md | Guide |
| TEMPLATE_SP_STRUCTURE.md | TEMPLATE-SP-STRUCTURE.md | Template |
| README.md | README.md | Index |

**Note**: UC5 ora ha directory SUPPLEMENTARY/ per i 3 variant diagrams

---

### UC6-UC11 — Stesso Pattern

(Omesso per brevità — segue lo stesso schema di UC1-UC4)

---

## Implementation Strategy

### Phase 1: Planning & Validation (Current)
- ✅ Analisi completa struttura (DONE)
- ✅ Creazione piano migrazione (THIS DOCUMENT)
- 🔄 Validazione su UC5 (pilot test)

### Phase 2: UC5 Pilot Test
1. Crea backup cartella UC5
2. Rinomina 5-6 file in UC5 manualmente
3. Aggiorna cross-references in UC5 README
4. Testa rendering GitHub
5. Se OK → procedi con bulk

### Phase 3: Bulk Renaming (All UCs)
1. Per ogni UC (UC1-UC11):
   - Rinomina 00 Architettura → 00-ARCHITECTURE.md
   - Consolidate sequence files → 03-SEQUENCES.md
   - Rinomina dipendenze → 02-DEPENDENCIES.md
   - Rinomina guide → 04-GUIDE.md
   - Sposta SP files in sottocartella SP/ (opzionale)

2. Update all README.md:
   - Fix link path (00-ARCHITECTURE.md not "00 Architettura...")
   - Add table of contents with new structure

3. Update cross-references:
   - Docs root (ARCHITECTURE-OVERVIEW.md, etc.)
   - SP mapping files
   - VALIDATION-CHECKLIST.md

### Phase 4: Verification & QA
- Verifica tutti i link sono validi
- Test GitHub rendering per ogni UC
- Check git history (rename detected correctly)

---

## Git Commit Strategy

```bash
# Singolo commit per UC (5-6 files):
git mv "01 Old Name.md" "00-ARCHITECTURE.md"
git mv "02 Matrice..." "02-DEPENDENCIES.md"
...
git commit -m "docs(UC5): Standardize file naming — 00-NN-NAME.md archetipo"

# Alternative: Bulk commit con spiegazione estesa per ogni UC
```

---

## Affected Cross-References

### Files da Aggiornare

1. **docs/ARCHITECTURE-OVERVIEW.md**
   - Link a UC documentation
   - Update to new file paths

2. **docs/VALIDATION-CHECKLIST.md**
   - UC/SP references
   - Update path references

3. **docs/SP-MS-MAPPING-MASTER.md**
   - SP documentation links
   - Update to SP/ folder structure

4. **Tutti i UC README.md**
   - Internal links fra file UC
   - Update all path references

5. **docs/use_cases/README.md**
   - Master index per UCs
   - Update structure documentation

---

## Rollback Plan

Se qualcosa va male:

```bash
# Revert all renames (use git history):
git reset --hard HEAD~N
# or for individual files:
git checkout -- "docs/use_cases/UC5 - .../"
```

---

## Risks & Mitigations

| Risk | Probability | Mitigation |
|------|-----------|-----------|
| Broken links in cross-refs | HIGH | Update all refs before commit |
| GitHub render issues | MEDIUM | Test on branch before merge |
| Confusion during transition | MEDIUM | Clear commit messages + changelog |
| Missed duplicates (SP01, etc.) | MEDIUM | Verify SP mapping before/after |

---

## Timeline Estimate

| Phase | Task | Effort | Notes |
|-------|------|--------|-------|
| 1 | Planning & validation | ✅ DONE | This document |
| 2 | UC5 pilot test | 1-2 hours | Manual test, then bulk script |
| 3a | UC1-UC4 bulk rename | 2-3 hours | Script-assisted |
| 3b | UC6-UC11 bulk rename | 2-3 hours | Script-assisted |
| 4 | Cross-reference updates | 2-3 hours | Grep/sed + manual review |
| 5 | QA & verification | 1-2 hours | Link validation |
| **TOTAL** | | **8-13 hours** | Can parallelize with Phase 2 A3 |

---

## Next Steps

1. ✅ Review this plan
2. 🔄 **Execute UC5 Pilot** (1-2 hours)
3. 📋 **Create rename script** (automated bulk rename)
4. 🚀 **Run bulk rename** (UC1-UC11)
5. 🔗 **Update cross-references**
6. ✅ **QA & merge**

---

**Documento**: UC-RENAMING-STRATEGY.md
**Status**: READY FOR UC5 PILOT TEST
**Owner**: Tech Writer / Documentation Team
