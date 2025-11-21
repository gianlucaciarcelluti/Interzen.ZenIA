# A1 SubProjekti Categorization for Conformità Normativa Implementation

**Project**: ZenIA Documentation Phase 2 - A1 Conformità Normativa
**Status**: In Progress
**Created**: 2025-11-19
**Target Completion**: 2025-11-23

---

## Executive Summary

- **Total SPs**: 71 (SP28 reserved)
- **CRITICAL tier**: 10 SP (must apply template first)
- **HIGH tier**: 45 SP (apply template second)
- **MEDIUM tier**: 15 SP (apply template last)
- **Estimated effort**: 20-25 hours total for A1 template application

---

## CRITICAL Tier (10 SP) - APPLY FIRST ⭐

These SPs form the core foundation. Template application: ~10-12 hours (1-2 days)

| # | SP ID | Title | UC | GDPR | eIDAS | CAD | AGID | Priority |
|---|-------|-------|----|----|-------|-----|------|----------|
| 1 | SP01 | EML Parser & Email Intelligence | UC2, UC5 | ✅ | ✅ | ✅ | ❌ | **P0** |
| 2 | SP02 | Document Extractor & Attachment Classifier | UC1, UC5 | ✅ | ❌ | ✅ | ❌ | **P0** |
| 3 | SP04 | Knowledge Base & Legal Context Management | UC5 | ❌ | ❌ | ✅ | ❌ | **P0** |
| 4 | SP05 | Template Engine | UC5 | ❌ | ❌ | ✅ | ❌ | **P0** |
| 5 | SP07 | Content Classifier | UC1, UC5 | ✅ | ❌ | ✅ | ❌ | **P0** |
| 6 | SP12 | Semantic Search & Q&A Engine | UC1 | ✅ | ❌ | ✅ | ✅ | **P0** |
| 7 | SP29 | Digital Signature Engine | UC6 | ❌ | ✅ | ✅ | ❌ | **P0** |
| 8 | SP42 | Policy Engine | UC9 | ✅ | ❌ | ✅ | ❌ | **P0** |
| 9 | SP50 | Compliance Training & Certification | UC10 | ✅ | ❌ | ✅ | ✅ | **P0** |
| 10 | SP70 | Compliance & Audit Management | UC11 | ✅ | ❌ | ✅ | ❌ | **P0** |

**Notes**:
- SP01: Complex - manages email PEC signatures (eIDAS + GDPR)
- SP29: Core to digital signature stack (UC6)
- SP42, SP50, SP70: Compliance gatekeepers (UC9-11)
- All require CAD compliance
- 7 out of 10 require GDPR sections
- 2 out of 10 require eIDAS sections
- 3 out of 10 require AGID accessibility sections

**Approach**: Create detailed Conformità sections with all frameworks + HITL checkpoints

---

## HIGH Tier (45 SP) - APPLY SECOND ✓

Process, governance, and digital transformation. Template application: ~8-10 hours per batch

### UC1 - Document Management System (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP13 | Document Summarizer | ✅ | ❌ | ❌ |
| SP14 | Metadata Indexer | ❌ | ❌ | ❌ |
| SP15 | Document Workflow Orchestrator | ✅ | ❌ | ❌ |
| SP11 | Security & Audit | ✅ | ❌ | ❌ |

### UC2 - Digital Protocol System (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP16 | Correspondence Classifier | ✅ | ❌ | ❌ |
| SP17 | Register Suggester | ✅ | ❌ | ❌ |
| SP26 | Intelligent Workflow Designer | ✅ | ❌ | ❌ |
| SP27 | Process Analytics | ✅ | ❌ | ❌ |

### UC5 - Produzione Documentale Integrata (5 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP03 | Procedural Classifier | ✅ | ❌ | ❌ |
| SP06 | Validator | ✅ | ❌ | ❌ |
| SP08 | Quality Checker | ✅ | ❌ | ❌ |
| SP09 | Workflow Engine | ✅ | ❌ | ❌ |
| SP10 | Control Dashboard | ✅ | ❌ | ✅ |

### UC6 - Sistema Firma Digitale (4 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP30 | Certificate Manager | ❌ | ✅ | ❌ |
| SP31 | Signature Workflow | ❌ | ✅ | ❌ |
| SP32 | Timestamp Authority & Marking | ❌ | ✅ | ❌ |

### UC7 - Gestione Archivio & Conservazione (5 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP33 | Archive Manager | ✅ | ❌ | ❌ |
| SP34 | Preservation Engine | ✅ | ❌ | ❌ |
| SP35 | Integrity Validator | ❌ | ❌ | ❌ |
| SP36 | Storage Optimizer | ❌ | ❌ | ❌ |
| SP37 | Archive Metadata Manager | ✅ | ❌ | ❌ |

### UC8 - Integrazione SIEM & Sicurezza (4 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP38 | SIEM Collector | ✅ | ❌ | ❌ |
| SP39 | SIEM Processor | ✅ | ❌ | ❌ |
| SP40 | SIEM Storage | ✅ | ❌ | ❌ |
| SP41 | SIEM Analytics & Reporting | ✅ | ❌ | ❌ |

### UC9 - Compliance & Risk Management (8 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP43 | Risk Assessment Engine | ✅ | ❌ | ❌ |
| SP44 | Compliance Monitoring System | ✅ | ❌ | ❌ |
| SP45 | Regulatory Intelligence Hub | ✅ | ❌ | ❌ |
| SP46 | Compliance Automation Platform | ✅ | ❌ | ❌ |
| SP47 | Compliance Analytics & Reporting | ✅ | ❌ | ✅ |
| SP48 | Compliance Intelligence Platform | ✅ | ❌ | ❌ |
| SP49 | Regulatory Change Management | ✅ | ❌ | ❌ |

### UC10 - Supporto Utente (6 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP51 | Help Desk System | ✅ | ❌ | ✅ |
| SP52 | Knowledge Base Management | ✅ | ❌ | ✅ |
| SP53 | Virtual Assistant & Chatbot | ✅ | ❌ | ✅ |
| SP54 | User Training Platform | ✅ | ❌ | ✅ |
| SP55 | Self-Service Portal | ✅ | ❌ | ✅ |

**Totale TIER ALTO**: 45 SP
- GDPR richiesto: 40/45 (89%)
- AGID richiesto: 6/45 (13%)
- eIDAS richiesto: 0/45 (0%)

---

## TIER MEDIO (15 SP) - APPLICARE PER ULTIMO ◆

Analytics, DevOps e infrastruttura di monitoraggio. Applicazione template: ~4-5 ore per batch

### UC10 - Supporto Utente (2 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP56 | Support Analytics & Reporting | ✅ | ❌ | ❌ |
| SP57 | User Feedback Management | ✅ | ❌ | ❌ |

### UC11 - Analisi Dati & Reporting (13 SP)
| SP ID | Titolo | GDPR | eIDAS | AGID |
|-------|--------|------|-------|------|
| SP58 | Data Lake & Storage Management | ✅ | ❌ | ❌ |
| SP59 | ETL Pipeline & Data Processing | ✅ | ❌ | ❌ |
| SP60 | Advanced Analytics & Machine Learning | ✅ | ❌ | ❌ |
| SP61 | Self-Service Analytics Portal | ✅ | ❌ | ✅ |
| SP62 | Data Quality & Governance | ✅ | ❌ | ❌ |
| SP63 | Real-Time Analytics & Streaming | ✅ | ❌ | ❌ |
| SP64 | Predictive Analytics & Forecasting | ❌ | ❌ | ❌ |
| SP65 | Performance Monitoring & Alerts | ✅ | ❌ | ❌ |
| SP66 | Data Security & Compliance | ❌ | ❌ | ❌ |
| SP67 | API Gateway & Integration Layer | ✅ | ❌ | ❌ |
| SP68 | DevOps & CI/CD Pipeline | ✅ | ❌ | ❌ |
| SP69 | Disaster Recovery & Business Continuity | ✅ | ❌ | ❌ |
| SP72 | Incident Management & Escalation | ❌ | ❌ | ❌ |

**Totale TIER MEDIO**: 15 SP
- GDPR richiesto: 12/15 (80%)
- AGID richiesto: 1/15 (7%)
- eIDAS richiesto: 0/15 (0%)

---

## Riepilogo Requisiti di Conformità

| Framework | Totale SP | % | Critico | Alto | Medio |
|-----------|-----------|---|---------|------|-------|
| **CAD** | 71/71 | 100% | 10 | 45 | 15 |
| **GDPR** | 62/71 | 87% | 7 | 40 | 12 |
| **eIDAS** | 5/71 | 7% | 2 | 0 | 0 |
| **AGID** | 11/71 | 15% | 3 | 6 | 2 |

**Conformità CAD**: Tutti i 71 SP
**Conformità GDPR**: 62 SP (DMS, classificazione, estrazione, governance, monitoraggio)
**Esenti da GDPR**: SP05, SP25, SP35, SP36, SP64, SP66, SP72 (9 SP non sensibili)
**Conformità eIDAS**: 5 SP (stack firma digitale + validazione PEC)
**Conformità AGID**: 11 SP (UI + requisiti di accessibilità)

---

## Pianificazione Implementazione

### Settimana 1: TIER CRITICO (10 SP)
- **Giorni 1-2**: SP01, SP02, SP04, SP05 (fondamenta)
- **Giorni 3-4**: SP07, SP12, SP29 (processing + firme)
- **Giorno 5**: SP42, SP50, SP70 (compliance)
- **Sforzo stimato**: 10-12 ore
- **Validazione**: Checkpoint HITL completo

### Settimana 2: TIER ALTO (45 SP)
- **Giorni 6-7**: Batch UC1-2 (SP03, SP06, SP08-19) = 12 SP
- **Giorni 8-9**: Batch UC3-4 (SP20-27) = 8 SP
- **Giorno 10**: Batch UC5-6 (SP30-31) = 2 SP
- **Continuazione**: (SP33-55 = 23 SP)
- **Sforzo stimato**: 8-10 ore/giorno = 40 ore totali
- **Validazione parallela**: Cross-reference con GLOSSARIO

### Settimana 3: TIER MEDIO (15 SP)
- **Giorni 11-12**: SP56-57 + SP58-67 (10 SP)
- **Giorni 13-14**: SP68-72 (5 SP) + validazione finale
- **Sforzo stimato**: 4-5 ore
- **Validazione finale & commit**

---

## Strategia Checkpoint HITL

Per ogni sezione Conformità di uno SP applicare 1-2 checkpoint HITL chiave:

**SP CRITICI**: 2-3 checkpoint HITL
- #1: Completezza normativa (tutti i framework)
- #2: Revisione conformità (CAD/GDPR/eIDAS/AGID)
- #3: Approvazione & Monitoraggio (se compliance critica)

**SP ALTI**: 1-2 checkpoint HITL
- #1: Revisione conformità (CAD + framework rilevanti)
- #2: Approvazione (se governance-critico)

**SP MEDI**: 1 checkpoint HITL
- #1: Piano di monitoraggio (intervento minimo)

---

## Checklist di Validazione Prima del Merge

Per ogni SP, prima di marcarlo completo:

- [ ] Template applicato (struttura sezione conforme a `TEMPLATE-CONFORMITA-NORMATIVA.md`)
- [ ] Tutti i framework applicabili inclusi (CAD, GDPR, eIDAS, AGID)
- [ ] Checkpoint HITL definiti con esempi di tracciamento JSON
- [ ] Mappatura responsabilità completa (matrice RACI)
- [ ] Guardrail: sezione < 10 KB totali
- [ ] Terminologia: tutti i termini coincidono con `GLOSSARIO-TERMINOLOGICO.md`
- [ ] Cross-reference: link ad altri SP dove applicabile
- [ ] Piano di monitoraggio: data della prossima revisione specificata
- [ ] Git: file aggiornato con timestamp + bump di versione

---

## Criteri di Successo per A1

- ✅ Tutti i 71 SP hanno sezioni Conformità Normativa
- ✅ Checkpoint HITL integrati (6 tipi principali di checkpoint)
- ✅ Guardrail applicati (nessuna sezione > 10 KB)
- ✅ Allineamento completo con `GLOSSARIO-TERMINOLOGICO.md`
- ✅ Zero cross-reference rotti
- ✅ Stima incremento completamento a 97.5-98%
- ✅ Stima incremento qualità a 95-96%

---

**Versione file**: 1.0
**Ultimo aggiornamento**: 2025-11-19
**Stato**: Pronto per implementazione
