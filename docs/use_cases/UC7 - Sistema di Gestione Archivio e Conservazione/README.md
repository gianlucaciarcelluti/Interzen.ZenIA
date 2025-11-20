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
| Architettura Generale | `00-ARCHITECTURE.md` | Architecture | ✅ | [Vai](./00-ARCHITECTURE.md) |
| SP33 - Archive Manager | `SP33 - Gestore Archivio.md` | Specification | ✅ | [Vai in UC6](../UC6%20-%20Firma%20Digitale%20Integrata/SP33%20-%20Gestore%20Archivio.md) |
| SP34 - Preservation Engine | `SP34 - Motore Conservazione.md` | Specification | ✅ | [Vai in UC6](../UC6%20-%20Firma%20Digitale%20Integrata/SP34%20-%20Motore%20Conservazione.md) |
| SP35 - Integrity Validator | `SP35 - Validatore Integrità.md` | Specification | ✅ | [Vai in UC6](../UC6%20-%20Firma%20Digitale%20Integrata/SP35%20-%20Validatore%20Integrit%C3%A0.md) |
| SP36 - Storage Optimizer | `SP36 - Ottimizzatore Archiviazione.md` | Specification | ✅ | [Vai in UC6](../UC6%20-%20Firma%20Digitale%20Integrata/SP36%20-%20Ottimizzatore%20Archiviazione.md) |
| SP37 - Archive Metadata Manager | `SP37 - Gestore Metadati Archivio.md` | Specification | ✅ | [Vai in UC6](../UC6%20-%20Firma%20Digitale%20Integrata/SP37%20-%20Gestore%20Metadati%20Archivio.md) |
| Sequence diagrams | `03-SEQUENCES.md` | Diagram | ✅ | [Vai](./03-SEQUENCES.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Archive

- **[SP33](../UC6%20-%20Firma%20Digitale%20Integrata/SP33%20-%20Gestore%20Archivio.md)** - Archive Manager (in UC6)
- **[SP37](../UC6%20-%20Firma%20Digitale%20Integrata/SP37%20-%20Gestore%20Metadati%20Archivio.md)** - Archive Metadata Manager (in UC6)

### Preservation

- **[SP34](../UC6%20-%20Firma%20Digitale%20Integrata/SP34%20-%20Motore%20Conservazione.md)** - Preservation Engine (in UC6)

### Integrity

- **[SP35](../UC6%20-%20Firma%20Digitale%20Integrata/SP35%20-%20Validatore%20Integrit%C3%A0.md)** - Integrity Validator (in UC6)

### Storage

- **[SP36](../UC6%20-%20Firma%20Digitale%20Integrata/SP36%20-%20Ottimizzatore%20Archiviazione.md)** - Storage Optimizer (in UC6)

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
├── README.md                            ← START HERE
├── 01-OVERVIEW.md                       ← SP Subprojects Overview
├── 00-ARCHITECTURE.md                   ← Architecture
├── 02-DEPENDENCIES.md                   ← Dependencies
├── 03-SEQUENCES.md                      ← Main Sequence Diagrams
├── 04-GUIDE.md                          ← Implementation Guide
│
└── NOTE: SP33-SP37 are in UC6 (Firma Digitale Integrata)
    for proper SP mapping organization
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
