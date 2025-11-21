# UC1 - Sistema di Gestione Documentale

**Status**: Active
**Version**: 1.1
**Last Updated**: 2025-11-21
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

## ⚡ Quick Start

1. **Accesso Sistema**: Autenticazione via SPID/CIE tramite MS13-SECURITY
2. **Upload Documento**: Carica documenti tramite SP02 (Parser EML per email, estrazione allegati)
3. **Classificazione Automatica**: SP07 classifica contenuti, SP03 determina procedimento
4. **Ricerca Semantica**: Cerca documenti via SP12 con full-text + NLP
5. **Archiviazione**: SP14 indicizza metadati, documenti archiviati con conformità normativa

**Documentazione correlata**:
- [SP02 - Document Extractor](../UC5%20-%20Produzione%20Documentale%20Integrata/SP02%20-%20Estrattore%20Documenti%20e%20Classificatore%20Allegati.md)
- [SP12 - Semantic Search](./SP12%20-%20Ricerca%20Semantica%20e%20Motore%20Q%26A.md)
- [03-SEQUENCES.md](./03-SEQUENCES.md) - Flusso completo

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

- ☑ L. 241/1990 - Procedimento Amministrativo
- ☑ CAD (Codice dell'Amministrazione Digitale)
- ☑ GDPR (Regolamento 2016/679)
- ☑ PNRR (Piano Nazionale Ripresa e Resilienza)
- ☑ Piano Triennale AgID 2024-2026
- ☐ eIDAS - Regolamento 2014/910
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📋 Conformità PNRR (Piano Nazionale Ripresa e Resilienza)

### Missione 1, Componente 1.1-1.2: PA Modernization & Digital Transformation

**Obiettivo**: Modernizzazione della Pubblica Amministrazione tramite gestione documentale digitale e processi paperless.

| Requisito PNRR | Implementazione UC1 | Status |
|---|---|---|
| **Processi digital-first** | Gestione 100% digitale dei documenti | ✅ |
| **Riduzione tempi PA** | Workflow automatici (target -20%) | ✅ SP15 |
| **Interoperabilità** | API standardizzate per integrazione | ✅ SP14 |
| **Data integration** | Metadati standardizzati (ISO 23081) | ✅ SP14 |
| **Accessibility** | WCAG 2.1 AA compliance per ricerca | ✅ SP12 |

**Conformità raggiunta**: UC1 implementa digitalizzazione completa della gestione documentale per modernizzazione PA.

---

## 📚 Conformità Piano Triennale AgID 2024-2026

### Capitolo 3: Servizi (E-Services & Document Management)

#### 3.1 Gestione Documenti Informatici

| Requisito Piano Triennale | Mappatura UC1 | Riferimento |
|---|---|---|
| **Digitalizzazione documenti** | Acquisizione da molteplici fonti (SP02 in UC5) | SP02 |
| **Metadati standardizzati** | ISO/IEC 23081-1 metadata schema | SP14 |
| **Accessibilità servizi** | WCAG 2.1 AA per interfacce (SP12) | SP12 |
| **Interoperabilità** | API OpenAPI 3.0 standard | SP15 |
| **Ricerca semantica** | Full-text + NLP-based search | SP12 |

#### 3.2 Conservazione Digitale (Long-Term Preservation)

| Requisito | Implementazione UC1 | Riferimento |
|---|---|---|
| **Formato archivio** | PDF/A-1b per preservazione | SP14 |
| **Metadati preservation** | ISO 23081 + OAIS model | SP14 |
| **Validation periodica** | Hash validation + integrity check | SP14 |
| **Accessibilità storica** | 30+ year retention capability | SP14 |

### Capitolo 4: Piattaforme Digitali (Interoperability & Data Sharing)

#### 4.1 PDND (Piattaforma Dati Nazionale Dati) Integration

| Piattaforma | Implementazione UC1 | Status |
|---|---|---|
| **PDND Data Sharing** | SP14 exports metadati per PDND | ✅ |
| **API standardizzate** | REST/SOAP endpoint per interoperabilità | ✅ SP15 |
| **Single Digital Gateway** | Ricerca documento via SPD | ✅ SP12 |

#### 4.2 SPID/CIE Authentication

| Requisito | Implementazione UC1 | Status |
|---|---|---|
| **SPID login** | Integration con MS13-SECURITY | ✅ |
| **Permessi per ruolo** | RBAC per accesso documenti | ✅ |
| **Audit trail** | Logging accesso (chi, cosa, quando) | ✅ |

---

## 🛡️ Conformità CAD (D.Lgs 82/2005)

### Titolo I: Digital-First PA

| Articolo | Requisito | Implementazione UC1 |
|---|---|---|
| **Art. 1** | Principio digital-first | Documenti digitali 100% |
| **Art. 2** | Interoperabilità | API standardizzate |
| **Art. 3** | Accessibilità | WCAG 2.1 AA compliance |
| **Art. 5** | Privacy/Security | GDPR + audit trail |

### Titolo II: Digital Documents & Signatures

| Articolo | Requisito | Implementazione UC1 |
|---|---|---|
| **Art. 21** | Validità documenti | PDF/A-1b + metadata |
| **Art. 22** | Firma digitale | Support per XAdES/PAdES (UC6) |
| **Art. 23** | Marca temporale | RFC 3161 timestamp (UC6) |

### Titolo IV: Conservation (30+ years)

| Articolo | Requisito | Implementazione UC1 |
|---|---|---|
| **Art. 41** | Long-term preservation | 30+ year archiving capability |
| **Art. 42** | Autenticità | Catena custodia + hash validation |
| **Art. 43** | Integrità | Blockchain-optional integrity proof |

---

## 📊 Conformità GDPR (Data Protection)

### Data Governance per Document Management

| Principio | Implementazione UC1 | Meccanismo |
|---|---|---|
| **Lawfulness** | Audit trail per tracking autorità | SP14 logging |
| **Transparency** | Metadata disponibili (diritto accesso) | SP12 search |
| **Data minimization** | Classificazione + retention policy | SP14 metadata |
| **Integrity** | Hash validation + RBAC accesso | SP14 security |
| **Confidentiality** | Crittografia + role-based access | SP15 workflow |

---

## ✅ Checklist Conformità Pre-Deployment

### PNRR M1C1 - PA Modernization

- [ ] Processi digital-first implementati (0% carta)
- [ ] Workflow automatici con SLA configurati
- [ ] Tempi medi procedimento PA monitirati (<30 giorni target)
- [ ] API per integrazione P.A. testate
- [ ] Metadati standardizzati ISO 23081 implementati
- [ ] Accessibility audit WCAG 2.1 AA completato
- [ ] Performance baseline stabilito per dashboard PNRR

### Piano Triennale Cap 3 - Document Management

- [ ] Acquisizione da molteplici fonti (email, forms, upload)
- [ ] Metadati ISO/IEC 23081-1 schema implementato
- [ ] Full-text search + semantica attivati
- [ ] PDF/A-1b formato archivio supportato
- [ ] Ricerca WCAG 2.1 AA accessible
- [ ] API documentation (OpenAPI 3.0) completata
- [ ] Retention policy 30+ anni configurato

### Piano Triennale Cap 4 - PDND & Interoperability

- [ ] PDND data sharing endpoint implementato
- [ ] SPID/CIE login integrato
- [ ] Role-based access control testato
- [ ] Single Digital Gateway search compatibility
- [ ] API rate limiting e throttling configurato
- [ ] Authentication logging abilitato

### CAD Compliance - Digital Documents

- [ ] Validità documenti verificata (PDF/A-1b)
- [ ] Firma digitale support (XAdES/PAdES)
- [ ] Marca temporale RFC 3161 disponibile
- [ ] Catena di custodia documentata
- [ ] Hash validation implementato
- [ ] 30+ year archiving capability testato
- [ ] Audit trail per document access

### GDPR - Data Protection

- [ ] Privacy classification di documenti
- [ ] Data retention policy comunicata a staff
- [ ] Right to access (Art. 15) implementato
- [ ] Encryption for sensitive docs at rest & transit
- [ ] Role-based access control per documento
- [ ] Data subject access request procedure
- [ ] Audit log per data processing operations

---

## 📅 Checklist Conformità Annuale

**Frequenza**: Annuale (Novembre di ogni anno)

- [ ] PNRR KPI verificati (tempo medio, % digitale, accessibilità)
- [ ] Piano Triennale compliance audit completato
- [ ] CAD Art. 41-43 compliance check (preservation, authenticity)
- [ ] GDPR data processing audit
- [ ] Metadata schema update review
- [ ] API compatibility test (PDND, SPD)
- [ ] Archive integrity verification (hash validation)
- [ ] Performance metrics anaylizzati
- [ ] Staff training on digital document handling
- [ ] Compliance report for governance

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

**Versione**: 1.1 (21 novembre 2025)
**Prossima Review**: 21 dicembre 2025

### Changelog v1.1

**Aggiunte**:
- Conformità PNRR M1C1.1-1.2 (PA Modernization, Digital Transformation) con SLA tempi ridotti
- Conformità Piano Triennale Cap 3 (Document Management, Metadata ISO 23081, Conservation)
- Conformità Piano Triennale Cap 4 (PDND data sharing, SPID/CIE integration, Single Digital Gateway)
- Conformità CAD (Digital-first, Interoperability, Accessibility, 30+ year preservation)
- Conformità GDPR (Data governance, audit trail, role-based access control)
- Checklist pre-deployment (35 items) per PNRR, Piano Triennale, CAD, GDPR
- Checklist conformità annuale (10 items) per KPI monitoring e compliance verification
