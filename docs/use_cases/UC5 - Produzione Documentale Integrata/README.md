# UC5 - Produzione Documentale Integrata

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
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
| SP01 - EML Parser & Email Intelligence | `01 SP01 - Parser EML e Intelligenza Email.md` | Specification | ✅ | [Vai](./01 SP01 - Parser EML e Intelligenza Email.md) |
| SP02 - Document Extractor & Attachment Classifier | `01 SP02 - Estrattore Documenti e Classificatore Allegati.md` | Specification | ✅ | [Vai](./01 SP02 - Estrattore Documenti e Classificatore Allegati.md) |
| SP03 - Procedural Classifier | `01 SP03 - Procedural Classifier.md` | Specification | ✅ | [Vai](./01 SP03 - Procedural Classifier.md) |
| SP04 - Knowledge Base | `01 SP04 - Base Conoscenze.md` | Specification | ✅ | [Vai](./01 SP04 - Base Conoscenze.md) |
| SP05 - Template Engine | `01 SP05 - Motore Template.md` | Specification | ✅ | [Vai](./01 SP05 - Motore Template.md) |
| SP06 - Validator | `01 SP06 - Validator.md` | Specification | ✅ | [Vai](./01 SP06 - Validator.md) |
| SP07 - Content Classifier | `01 SP07 - Classificatore Contenuti.md` | Specification | ✅ | [Vai](./01 SP07 - Classificatore Contenuti.md) |
| SP08 - Quality Checker | `01 SP08 - Verificatore Qualità.md` | Specification | ✅ | [Vai](./01 SP08 - Verificatore Qualità.md) |
| SP09 - Workflow Engine | `01 SP09 - Motore Workflow.md` | Specification | ✅ | [Vai](./01 SP09 - Motore Workflow.md) |
| SP10 - Dashboard | `01 SP10 - Pannello di Controllo.md` | Specification | ✅ | [Vai](./01 SP10 - Pannello di Controllo.md) |
| SP11 - Security & Audit | `01 SP11 - Sicurezza e Audit.md` | Specification | ✅ | [Vai](./01 SP11 - Sicurezza e Audit.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### EML

- **[SP01](./01 SP01 - Parser EML e Intelligenza Email.md)** - SP- EML Parser & Email Intelligence

### Document

- **[SP02](./01 SP02 - Estrattore Documenti e Classificatore Allegati.md)** - Document Extractor & Attachment Classifier

### Procedural

- **[SP03](./01 SP03 - Procedural Classifier.md)** - Procedural Classifier

### Knowledge

- **[SP04](./01 SP04 - Base Conoscenze.md)** - Knowledge Base

### Template

- **[SP05](./01 SP05 - Motore Template.md)** - Template Engine

### Validator.md

- **[SP06](./01 SP06 - Validator.md)** - Validator

### Content

- **[SP07](./01 SP07 - Classificatore Contenuti.md)** - Content Classifier

### Quality

- **[SP08](./01 SP08 - Verificatore Qualità.md)** - Quality Checker

### Workflow

- **[SP09](./01 SP09 - Motore Workflow.md)** - Workflow Engine

### Dashboard.md

- **[SP10](./01 SP10 - Pannello di Controllo.md)** - Dashboard

### Security

- **[SP11](./01 SP11 - Sicurezza e Audit.md)** - Security & Audit

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
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC5.md       ← Architecture
├── 01 SP01 - Parser EML e Intelligenza Email.md
├── 01 SP02 - Estrattore Documenti e Classificatore Allegati.md
├── 01 SP03 - Procedural Classifier.md
├── 01 SP04 - Base Conoscenze.md
├── 01 SP05 - Motore Template.md
├── 01 SP06 - Validator.md
├── 01 SP07 - Classificatore Contenuti.md
├── 01 SP08 - Verificatore Qualità.md
├── 01 SP09 - Motore Workflow.md
├── 01 SP10 - Pannello di Controllo.md
├── 01 SP11 - Sicurezza e Audit.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC5.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC5.md` | 1 hour |

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
