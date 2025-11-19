# UC7 - Sistema di Gestione Archivio e Conservazione

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Gestione dell'archivio documentale con conservazione digitale, scarto programmato e migrazione formati per preservazione long-term.

### Obiettivi Principali

- **Conservazione digitale a norma**: Conservazione digitale a norma
- **Scarto programmato secondo tabelle**: Scarto programmato secondo tabelle
- **Migrazione formati**: Migrazione formati
- **Metadati conservazione ISO/IEC**: Metadati conservazione ISO/IEC

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Sistema di Gestione Archivio e Conservazione**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC7.md` | Architecture | ✅ | [Vai](./00 Architettura UC7.md) |
| SP33 - Archive Manager | `01 SP33 - Archive Manager.md` | Specification | ✅ | [Vai](./01 SP33 - Archive Manager.md) |
| SP34 - Preservation Engine | `01 SP34 - Preservation Engine.md` | Specification | ✅ | [Vai](./01 SP34 - Preservation Engine.md) |
| SP35 - Integrity Validator | `01 SP35 - Integrity Validator.md` | Specification | ✅ | [Vai](./01 SP35 - Integrity Validator.md) |
| SP36 - Storage Optimizer | `01 SP36 - Storage Optimizer.md` | Specification | ✅ | [Vai](./01 SP36 - Storage Optimizer.md) |
| SP37 - Archive Metadata Manager | `01 SP37 - Archive Metadata Manager.md` | Specification | ✅ | [Vai](./01 SP37 - Archive Metadata Manager.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | [Vai](./01 Sequence diagrams.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Archive

- **[SP33](./01 SP33 - Archive Manager.md)** - Archive Manager
- **[SP37](./01 SP37 - Archive Metadata Manager.md)** - Archive Metadata Manager

### Preservation

- **[SP34](./01 SP34 - Preservation Engine.md)** - Preservation Engine

### Integrity

- **[SP35](./01 SP35 - Integrity Validator.md)** - Integrity Validator

### Storage

- **[SP36](./01 SP36 - Storage Optimizer.md)** - Storage Optimizer

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ CAD
- ☑ D.Lgs 42/2004
- ☐ L. 241/1990 - Procedimento Amministrativo
- ☐ GDPR - Regolamento 2016/679
- ☐ eIDAS - Regolamento 2014/910
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
UC7 - Sistema di Gestione Archivio e Conservazione/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC7.md       ← Architecture
├── 01 SP33 - Archive Manager.md
├── 01 SP34 - Preservation Engine.md
├── 01 SP35 - Integrity Validator.md
├── 01 SP36 - Storage Optimizer.md
├── 01 SP37 - Archive Metadata Manager.md
├── 01 Sequence diagrams.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC7.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC7.md` | 1 hour |

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
