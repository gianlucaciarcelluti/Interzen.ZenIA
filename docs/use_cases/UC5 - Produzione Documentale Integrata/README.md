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

- ☑ CAD
- ☑ GDPR
- ☑ eIDAS
- ☐ L. 241/1990 - Procedimento Amministrativo
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

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

**Versione**: 1.0 (19 novembre 2025)
**Prossima Review**: 19 dicembre 2025
