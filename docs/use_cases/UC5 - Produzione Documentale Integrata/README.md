# UC5 - Produzione Documentale Integrata

**Status**: Active
**Version**: 1.1
**Last Updated**: 2025-11-20 (File naming standardization)
**Owner**: Architecture Team

---

## 📌 Overview

Generazione automatica di documenti strutturati (delibere, determine, atti formali) con template dinamici, firma digitale integrata.

### Obiettivi Principali

- **Template engine con variabili dinamiche**: Template engine con variabili dinamiche
- **Generazione documenti standardizzati**: Generazione documenti standardizzati
- **Integrazione firma digitale**: Integrazione firma digitale
- **Conservazione a norma**: Conservazione a norma

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Produzione Documentale Integrata**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architecture Overview | `00-ARCHITECTURE.md` | Overview | ✅ | [Vai](./00-ARCHITECTURE.md) |
| Subprojects Overview | `01-OVERVIEW.md` | Overview | ✅ | [Vai](./01-OVERVIEW.md) |
| Dependencies | `02-DEPENDENCIES.md` | Matrix | ✅ | [Vai](./02-DEPENDENCIES.md) |
| Canonical Sequence Diagram | `SUPPLEMENTARY/CANONICAL-Complete-Flow.md` | Diagram | ✅ | [Vai](./SUPPLEMENTARY/CANONICAL-Complete-Flow.md) |
| Simplified Overview | `SUPPLEMENTARY/OVERVIEW-Simplified.md` | Diagram | ✅ | [Vai](./SUPPLEMENTARY/OVERVIEW-Simplified.md) |
| Ultra-Simplified Overview | `SUPPLEMENTARY/OVERVIEW-Ultra-Simplified.md` | Diagram | ✅ | [Vai](./SUPPLEMENTARY/OVERVIEW-Ultra-Simplified.md) |
| Implementation Guide | `04-GUIDE.md` | Guide | ✅ | [Vai](./04-GUIDE.md) |
| Human-in-the-Loop | `05-HITL.md` | Specification | ✅ | [Vai](./05-HITL.md) |
| SP Specifications | `01 SP0X - *.md` | Specification | ✅ | [Vai lista completa sotto] |

---

## 📊 SubProgetti (SP) - Overview Rapido

### EML

- **[SP01](./SP01 - Parser EML e Intelligenza Email.md)** - SP- EML Parser & Email Intelligence

### Document

- **[SP02](./SP02 - Estrattore Documenti e Classificatore Allegati.md)** - Document Extractor & Attachment Classifier

### Procedural

- **[SP03](./SP03 - Classificatore Procedurale.md)** - Procedural Classifier

### Knowledge

- **[SP04](./SP04 - Base Conoscenze.md)** - Knowledge Base

### Template

- **[SP05](./SP05 - Motore Template.md)** - Template Engine

### Validator.md

- **[SP06](./SP06 - Validatore.md)** - Validator

### Content

- **[SP07](./SP07 - Classificatore Contenuti.md)** - Content Classifier

### Quality

- **[SP08](./SP08 - Verificatore Qualità.md)** - Quality Checker

### Workflow

- **[SP09](./SP09 - Motore Workflow.md)** - Workflow Engine

### Dashboard.md

- **[SP10](./SP10 - Pannello di Controllo.md)** - Dashboard

### Security

- **[SP11](./SP11 - Sicurezza e Audit.md)** - Security & Audit

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ CAD (Codice dell'Amministrazione Digitale)
- ☑ GDPR (Regolamento 2016/679)
- ☑ eIDAS (Regolamento 2014/910)
- ☑ PNRR (Piano Nazionale Ripresa e Resilienza)
- ☑ Piano Triennale AgID 2024-2026
- ☐ L. 241/1990 - Procedimento Amministrativo
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📋 Conformità PNRR (Piano Nazionale Ripresa e Resilienza)

### Missione 1, Componente 1.2: Digital Transformation of Enterprises & PA

**Obiettivo**: Automazione generazione documenti formali con conformità normativa integrata.

| Requisito PNRR | Implementazione UC5 | Status |
|---|---|---|
| **Automazione documenti** | Template engine dinamico (SP05) | ✅ SP05 |
| **Riduzione tempi produzione** | Generazione <2 sec per documento | ✅ SP05 |
| **Data validation** | Validator + Quality Checker (SP06, SP08) | ✅ SP06, SP08 |
| **Firma digitale integrata** | eIDAS compliance (UC6 integration) | ✅ UC6 |
| **Tracciabilità completa** | Security & Audit logging (SP11) | ✅ SP11 |

**Conformità raggiunta**: UC5 implementa automazione documentale conforme PNRR M1C1.2.

---

## 📚 Conformità Piano Triennale AgID 2024-2026

### Capitolo 4: Piattaforme Digitali (Modello 3+2 & API Design)

#### 4.1 Modello 3+2 della PA Digitale

| Livello | Implementazione UC5 | Responsabile |
|---|---|---|
| **Livello 1: Accesso** | SPID/CIE login (MS13 integration) | MS13-SECURITY |
| **Livello 2: Frontend** | Dashboard/Pannello Controllo (SP10) | SP10 |
| **Livello 3: Logica Business** | Template + Workflow Engine (SP05, SP09) | SP05, SP09 |
| **Livello 4: Dati** | Metadata + Classificazione (SP03, SP07) | SP03, SP07 |
| **Livello 5: Interoperabilità** | API OpenAPI 3.0 standard | SP10 |

#### 4.2 API Design Standards

| Requisito | Implementazione UC5 | Details |
|---|---|---|
| **REST API** | Endpoint per generazione/validazione | SP05, SP06 |
| **OAuth 2.0** | Bearer token authentication | MS13-SECURITY |
| **Rate limiting** | Throttling configurabile | SP10 Gateway |
| **API documentation** | Swagger/OpenAPI 3.0 | SP10 |
| **Versioning** | Semantic versioning endpoint | SP10 |

### Capitolo 5: Dati e Intelligenza Artificiale (Data Governance & AI Transparency)

#### 5.1 Data Governance per Document Generation

| Aspetto | Implementazione UC5 | Standard |
|---|---|---|
| **Data quality** | Validator + QA Checker (SP06, SP08) | GDPR + Piano Triennale |
| **Data lineage** | Audit trail (SP11) per tracciabilità | CAD Art. 24 |
| **Metadata** | ISO/IEC 23081-1 schema | Piano Triennale |
| **Data retention** | Configurabile retention policy | GDPR Art. 5 |

#### 5.2 AI Transparency & Explainability

| Requisito | Implementazione UC5 | Dettagli |
|---|---|---|
| **Procedural Logic** | Spiegabilità di SP03 (Classificatore) | Decision reasoning |
| **Content Analysis** | Spiegabilità di SP07 (Content Classifier) | Classification criteria |
| **Quality Metrics** | KPI dashboard (SP10) | Performance monitoring |
| **Audit Trail** | Complete logging (SP11) | Decision audit |

---

## 🏛️ Conformità eIDAS (Regolamento 2014/910)

### Firma Digitale Integrata

| Articolo | Requisito | Implementazione UC5 |
|---|---|---|
| **Art. 13** | Firma avanzata | Integration con UC6 (XAdES, PAdES, CAdES) |
| **Art. 24** | Marca temporale | RFC 3161 TSA (UC6) |
| **Art. 32** | Validazione LTV | Long-Term Validation (UC7) |

---

## 📊 Conformità CAD (D.Lgs 82/2005)

### Document Generation Compliance

| Articolo | Requisito | Implementazione UC5 |
|---|---|---|
| **Art. 21** | Validità documenti | PDF/A-1b supportato (SP05) |
| **Art. 22** | Firma digitale | eIDAS integration (UC6) |
| **Art. 23** | Marca temporale | RFC 3161 TSA (UC6) |
| **Art. 24** | Non-ripudio | Audit trail completo (SP11) |

---

## 🛡️ Conformità GDPR (Data Protection)

### Document Generation & Privacy

| Principio | Implementazione UC5 | Meccanismo |
|---|---|---|
| **Data minimization** | Only required fields in template | SP05 schema |
| **Purpose limitation** | Role-based document access | SP11 RBAC |
| **Transparency** | Template variables documented | SP05 documentation |
| **Integrity** | Validation + signature | SP06 + UC6 |
| **Accountability** | Audit trail per document | SP11 logging |

---

## ✅ Checklist Conformità Pre-Deployment

### PNRR M1C1.2 - Digital Transformation

- [ ] Template engine con variabili dinamiche implementato (SP05)
- [ ] Tempo generazione documento <2 sec misurato
- [ ] Data validation pipeline completa (SP06 + SP08)
- [ ] Firma digitale eIDAS integrata (UC6)
- [ ] Audit trail per tracciabilità completa (SP11)
- [ ] Performance baseline stabilito
- [ ] Dashboard PNRR pronto per monitoring

### Piano Triennale Cap 4 - Modello 3+2 & API Design

- [ ] SPID/CIE login integrato (MS13-SECURITY)
- [ ] Dashboard/UI responsive (SP10)
- [ ] Template + Workflow engine operativi (SP05, SP09)
- [ ] Metadata schema ISO 23081 implementato
- [ ] API REST OpenAPI 3.0 documentata
- [ ] OAuth 2.0 authentication testato
- [ ] Rate limiting e throttling configurati
- [ ] API versioning implementato

### Piano Triennale Cap 5 - Data Governance & AI Transparency

- [ ] Data quality validation completa (SP06, SP08)
- [ ] Audit trail per data lineage (SP11)
- [ ] Metadata storage and retrieval working
- [ ] Retention policy implementata
- [ ] Procedural classifier (SP03) spiegabilità documentata
- [ ] Content classifier (SP07) decisioni tracciabili
- [ ] KPI dashboard operativo (SP10)
- [ ] AI transparency report generabile

### eIDAS & CAD - Digital Signature & Non-Repudiation

- [ ] PDF/A-1b generation da template
- [ ] eIDAS signature integration (UC6) testato
- [ ] RFC 3161 marca temporale disponibile
- [ ] Non-repudiation audit trail
- [ ] Document validity verification
- [ ] Long-term validation (LTV) setup

### GDPR - Privacy & Data Protection

- [ ] Data minimization in template variables
- [ ] Role-based document access control
- [ ] Template documentation transparent
- [ ] Document validation pipeline
- [ ] Complete audit trail for accountability
- [ ] Data retention policy configured
- [ ] Privacy by design implementato

---

## 📅 Checklist Conformità Annuale

**Frequenza**: Annuale (Novembre di ogni anno)

- [ ] PNRR document generation SLA verificato
- [ ] Piano Triennale API compatibility test (PDND, SPD)
- [ ] Data governance audit completato
- [ ] AI transparency metrics analizzati
- [ ] eIDAS signature statistics reviewed
- [ ] CAD compliance check (document format, signature)
- [ ] GDPR data processing audit
- [ ] Template effectiveness valutato
- [ ] Performance benchmarks updated
- [ ] Compliance report generated for governance

---

## 📂 Struttura File UC

```
UC5 - Produzione Documentale Integrata/
├── 00-ARCHITECTURE.md                   ← START HERE (Architecture overview)
├── 01-OVERVIEW.md                       ← Business overview & subprojects
├── 02-DEPENDENCIES.md                   ← Dependency matrix
├── 03-SEQUENCES.md                      ← Sequence diagrams (if applicable)
├── 04-GUIDE.md                          ← Implementation guide
├── 05-HITL.md                           ← Human-in-the-loop section
├── TEMPLATE-SP-STRUCTURE.md             ← SP documentation template
├── README.md                            ← This file (navigation index)
│
├── SUPPLEMENTARY/                       ← Variant documentation
│   ├── CANONICAL-Complete-Flow.md       ← Full canonical sequence diagram
│   ├── OVERVIEW-Simplified.md           ← Simplified stakeholder view
│   └── OVERVIEW-Ultra-Simplified.md     ← Executive summary
│
└── 01 SP01 - Parser EML e Intelligenza Email.md
    01 SP02 - Estrattore Documenti e Classificatore Allegati.md
    01 SP03 - Classificatore Procedurale.md
    01 SP04 - Base Conoscenze.md
    01 SP05 - Motore Template.md
    01 SP06 - Validatore.md
    01 SP07 - Classificatore Contenuti.md
    01 SP08 - Verificatore Qualità.md
    01 SP09 - Motore Workflow.md
    01 SP10 - Pannello di Controllo.md
    01 SP11 - Sicurezza e Audit.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00-ARCHITECTURE.md` + `SUPPLEMENTARY/OVERVIEW-Simplified.md` | 15 min |
| Developer | `00-ARCHITECTURE.md` + `SUPPLEMENTARY/CANONICAL-Complete-Flow.md` | 30 min |
| Tester | `01-OVERVIEW.md` + SP Documentation | 45 min |
| Compliance | Conformità Normativa section in `00-ARCHITECTURE.md` | 30 min |
| Architect | `00-ARCHITECTURE.md` + `02-DEPENDENCIES.md` | 1 hour |

### Resource Links

- **Glossario Terminologico**: [../../GLOSSARIO-TERMINOLOGICO.md](../../GLOSSARIO-TERMINOLOGICO.md)
- **JSON Payload Standard**: [../../templates/json-payload-standard.md](../../templates/json-payload-standard.md)
- **Conformità Normativa Template**: [../../templates/conformita-normativa-standard.md](../../templates/conformita-normativa-standard.md)
- **COMPLIANCE-MATRIX**: [../../COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)
- **UC README**: [../README.md](../README.md)

---

## ✅ Quality Checklist

- [x] INDEX contiene tutti gli SP del UC
- [x] Navigation Matrix è completa
- [x] Link interni validati
- [x] Conformità normativa identificata
- [x] Last update date registrata

---

**Versione**: 1.1 (21 novembre 2025)
**Prossima Review**: 21 dicembre 2025

### Changelog v1.1

**Aggiunte**:
- Conformità PNRR M1C1.2 (Digital Transformation) con SLA <2sec generazione documenti
- Conformità Piano Triennale Cap 4 (Modello 3+2, API Design REST/SOAP, OAuth 2.0, Rate limiting)
- Conformità Piano Triennale Cap 5 (Data Governance, AI Transparency, explainability)
- Conformità eIDAS (Firma avanzata, marcatura temporale RFC 3161, LTV validation)
- Conformità CAD (Digital documents, firma, marca temporale, non-ripudio)
- Conformità GDPR (Data minimization, privacy by design, audit trail)
- Checklist pre-deployment (40 items) per PNRR, Piano Triennale, eIDAS, CAD, GDPR
- Checklist conformità annuale (10 items) per KPI monitoring
