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
| SP02 - Document Extractor & Attachment Classifier | `01 SP02 - Estrattore Documenti e Classificatore Allegati.md` | Specification | ✅ | [Vai](./SP02 - Estrattore Documenti e Classificatore Allegati.md) |
| SP07 - Content Classifier | `01 SP07 - Classificatore Contenuti.md` | Specification | ✅ | [Vai](./SP07 - Classificatore Contenuti.md) |
| SP12 - Semantic Search & Q&A Engine | `01 SP12 - Ricerca Semantica e Motore Q&A.md` | Specification | ✅ | [Vai](./SP12 - Ricerca Semantica e Motore Q&A.md) |
| SP13 - Document Summarizer | `01 SP13 - Sintetizzatore Documenti.md` | Specification | ✅ | [Vai](./SP13 - Sintetizzatore Documenti.md) |
| SP14 - Metadata Indexer | `01 SP14 - Indicizzatore Metadati.md` | Specification | ✅ | [Vai](./SP14 - Indicizzatore Metadati.md) |
| SP15 - Document Workflow Orchestrator | `01 SP15 - Orchestratore Workflow Documenti.md` | Specification | ✅ | [Vai](./SP15 - Orchestratore Workflow Documenti.md) |
| Sequence - Document Processing Completo | `01 Sequence - Document Processing Completo.md` | Diagram | ✅ | C-SEQUENCES.md) |
| Sequence - Overview Semplificato | `01 Sequence - Overview Semplificato.md` | Diagram | ✅ | C-SEQUENCES-SIMPLIFIED.md) |
| Sequence - Ultra Semplificato | `01 Sequence - Ultra Semplificato.md` | Diagram | ✅ | C-SEQUENCES-ULTRA-SIMPLIFIED.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Document

- **[SP02](./SP02 - Estrattore Documenti e Classificatore Allegati.md)** - Document Extractor & Attachment Classifier
- **[SP13](./SP13 - Sintetizzatore Documenti.md)** - Document Summarizer
- **[SP15](./SP15 - Orchestratore Workflow Documenti.md)** - Document Workflow Orchestrator

### Content

- **[SP07](./SP07 - Classificatore Contenuti.md)** - Content Classifier

### Semantic

- **[SP12](./SP12 - Ricerca Semantica e Motore Q&A.md)** - Semantic Search & Q&A Engine

### Metadata

- **[SP14](./SP14 - Indicizzatore Metadati.md)** - Metadata Indexer

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
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC1.md       ← Architecture
├── 01 SP02 - Estrattore Documenti e Classificatore Allegati.md
├── 01 SP07 - Classificatore Contenuti.md
├── 01 SP12 - Ricerca Semantica e Motore Q&A.md
├── 01 SP13 - Sintetizzatore Documenti.md
├── 01 SP14 - Indicizzatore Metadati.md
├── 01 SP15 - Orchestratore Workflow Documenti.md
├── 01 Sequence - Document Processing Completo.md
├── 01 Sequence - Overview Semplificato.md
├── 01 Sequence - Ultra Semplificato.md
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
