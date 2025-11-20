# UC1 - Sistema di Gestione Documentale

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Gestione completa del ciclo di vita dei documenti, dall'acquisizione all'archivio, con classificazione, estrazione di metadati e ricerca semantica.

### Obiettivi Principali

- **Acquisizione e parsing di documenti da molteplici fonti**: Acquisizione e parsing di documenti da molteplici fonti
- **Classificazione automatica e estrazione di entità**: Classificazione automatica e estrazione di entità
- **Indicizzazione e ricerca semantica avanzata**: Indicizzazione e ricerca semantica avanzata
- **Archiviazione strutturata con metadati standardizzati**: Archiviazione strutturata con metadati standardizzati

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Sistema di Gestione Documentale**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| SP02 - Document Extractor & Attachment Classifier | `SP02 - Estrattore Documenti e Classificatore Allegati.md` | Specification | ✅ | [Vai in UC5](../UC5%20-%20Produzione%20Documentale%20Integrata/SP02%20-%20Estrattore%20Documenti%20e%20Classificatore%20Allegati.md) |
| SP07 - Content Classifier | `SP07 - Classificatore Contenuti.md` | Specification | ✅ | [Vai in UC5](../UC5%20-%20Produzione%20Documentale%20Integrata/SP07%20-%20Classificatore%20Contenuti.md) |
| SP12 - Semantic Search & Q&A Engine | `SP12 - Ricerca Semantica e Motore Q&A.md` | Specification | ✅ | [Vai](./SP12%20-%20Ricerca%20Semantica%20e%20Motore%20Q%26A.md) |
| SP13 - Document Summarizer | `SP13 - Sintetizzatore Documenti.md` | Specification | ✅ | [Vai](./SP13%20-%20Sintetizzatore%20Documenti.md) |
| SP14 - Metadata Indexer | `SP14 - Indicizzatore Metadati.md` | Specification | ✅ | [Vai](./SP14%20-%20Indicizzatore%20Metadati.md) |
| SP15 - Document Workflow Orchestrator | `SP15 - Orchestratore Workflow Documenti.md` | Specification | ✅ | [Vai](./SP15%20-%20Orchestratore%20Workflow%20Documenti.md) |
| Sequence - Document Processing Completo | `03-SEQUENCES.md` | Diagram | ✅ | [Vai](./03-SEQUENCES.md) |
| Sequence - Overview Semplificato | `03-SEQUENCES-SIMPLIFIED.md` | Diagram | ✅ | [Vai](./03-SEQUENCES-SIMPLIFIED.md) |
| Sequence - Ultra Semplificato | `03-SEQUENCES-ULTRA-SIMPLIFIED.md` | Diagram | ✅ | [Vai](./03-SEQUENCES-ULTRA-SIMPLIFIED.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Document

- **[SP02](../UC5%20-%20Produzione%20Documentale%20Integrata/SP02%20-%20Estrattore%20Documenti%20e%20Classificatore%20Allegati.md)** - Document Extractor & Attachment Classifier (in UC5)
- **[SP13](./SP13%20-%20Sintetizzatore%20Documenti.md)** - Document Summarizer
- **[SP15](./SP15%20-%20Orchestratore%20Workflow%20Documenti.md)** - Document Workflow Orchestrator

### Content

- **[SP07](../UC5%20-%20Produzione%20Documentale%20Integrata/SP07%20-%20Classificatore%20Contenuti.md)** - Content Classifier (in UC5)

### Semantic

- **[SP12](./SP12%20-%20Ricerca%20Semantica%20e%20Motore%20Q%26A.md)** - Semantic Search & Q&A Engine

### Metadata

- **[SP14](./SP14%20-%20Indicizzatore%20Metadati.md)** - Metadata Indexer

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ L. 241/1990
- ☑ CAD
- ☑ GDPR
- ☐ eIDAS - Regolamento 2014/910
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
UC1 - Sistema di Gestione Documentale/
├── README.md                            ← START HERE
├── 01-OVERVIEW.md                       ← SP Subprojects Overview
├── 00-ARCHITECTURE.md                   ← Architecture
├── 02-DEPENDENCIES.md                   ← Dependencies
├── 03-SEQUENCES.md                      ← Main Sequence Diagrams
├── 03-SEQUENCES-SIMPLIFIED.md           ← Simplified Diagrams
├── 03-SEQUENCES-ULTRA-SIMPLIFIED.md     ← Ultra-Simplified Diagrams
├── 04-GUIDE.md                          ← Implementation Guide
│
├── SP12 - Ricerca Semantica e Motore Q&A.md
├── SP13 - Sintetizzatore Documenti.md
├── SP14 - Indicizzatore Metadati.md
├── SP15 - Orchestratore Workflow Documenti.md
│
└── NOTE: SP02, SP07 are in UC5 (Produzione Documentale Integrata)
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC1.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC1.md` | 1 hour |

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
