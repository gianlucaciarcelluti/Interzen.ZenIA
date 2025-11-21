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

## ⚡ Quick Start

1. **Ricezione**: Documenti da UC5 o UC6 (firmati/conservati)
2. **Archiviazione**: Metadati ISO/IEC 23081, formati PDF/A
3. **Retention**: Scarto programmato secondo tabelle di conservazione
4. **Migrazione**: Conversione formati per preservazione long-term
5. **Recovery**: Recupero documenti con integrità verificata

**Documentazione correlata**:
- [UC6 - Digital Signatures](../UC6%20-%20Firma%20Digitale%20Integrata/README.md)

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

### Dettagli Conformità PNRR

#### Missione 1: Digitalizzazione, Innovazione, Competitività

| Componente | Requisito | Implementazione MS | Implementazione SP | Note |
|-----------|-----------|-------------------|--------------------|-------|
| M1C1.3 | Consolidamento centro gestione | MS09-MANAGER, MS16-REGISTRY | SP01-Intake Manager | Cloud consolidation con architettura cloud-native |
| M1C1.4 | Sicurezza informatica della PA | MS13-SECURITY, MS08-MONITOR | SP11-Security & Audit | Crittografia, backup geo-redundante, disaster recovery |

#### Obiettivi PNRR per UC7

- **Disaster recovery**: RTO 4 ore, RPO 1 ora con backup geo-redundante
- **Cloud consolidation**: 100% cloud deployment con SPC (Stato per Cittadini)
- **Long-term preservation**: 30+ anni con formato PDF/A e OAIS model

### Dettagli Conformità Piano Triennale AgID 2024-2026

#### Capitolo 3: Servizi - Gestione Documenti Informatici

| Servizio | Requisito | Implementazione MS | Implementazione SP | Note |
|---------|-----------|-------------------|--------------------|-------|
| Gestione documenti | Digitalizzazione | MS01-CLASSIFIER, MS05-TRANSFORMER | SP06-Validator | Classificazione e conversione formato PDF/A |
| Conservazione | Long-term preservation | MS05-TRANSFORMER, MS06-AGGREGATOR | SP34-Preservation Engine | OAIS model, metadati ISO/IEC 23081 |

#### Capitolo 6: Infrastrutture

| Infrastruttura | Requisito | Implementazione MS | Implementazione SP | Note |
|---|-----------|-------------------|--------------------|-------|
| Cloud pubblico | Cloud adoption | MS09-MANAGER, MS13-SECURITY | SP11-Security & Audit | Deployment SPC con encryption at rest |
| Disaster recovery | Business continuity | MS08-MONITOR, MS13-SECURITY | SP11-Security & Audit | RTO 4h, RPO 1h, geo-redundanza |
| Backup automatico | Data preservation | MS06-AGGREGATOR | SP34-Preservation Engine | Backup quota giornaliero con verifica integrità |

### Dettagli Conformità CAD - D.Lgs 82/2005

#### Titolo IV: Conservazione

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 41 | Conservazione dati digitali | MS05-TRANSFORMER, MS06-AGGREGATOR | SP34-Preservation Engine | 30+ anni, OAIS model, PDF/A |
| Art. 42 | Autenticità documento | MS04-VALIDATOR | SP32-Timestamp Authority | Catena custodia digitale con marca temporale |
| Art. 43 | Integrità documento | MS13-SECURITY | SP11-Security & Audit | Hash validation, CRC check, blockchain optional |

### Dettagli Conformità D.Lgs 42/2004 - Codice Beni Culturali

| Articolo | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| Art. 1 | Tutela patrimonio documentale | MS06-AGGREGATOR, MS14-AUDIT | SP34-Preservation Engine | Metadati conservazione, versioning |
| Art. 2 | Standard conservazione | MS05-TRANSFORMER | SP35-Format Migration | ISO/IEC 14721 OAIS, ISO 19005 PDF/A |

### Standard Internazionali - Conservazione Digitale

| Standard | Requisito | Implementazione MS | Implementazione SP | Note |
|----------|-----------|-------------------|--------------------|-------|
| ISO 14721 | OAIS (Open Archival Info System) | MS06-AGGREGATOR, MS05-TRANSFORMER | SP34-Preservation Engine | Reference model per preservation |
| ISO 19005 | PDF/A (Long-term file format) | MS04-VALIDATOR, MS05-TRANSFORMER | SP35-Format Migration | PDF/A-1b per archivio 30+ anni |
| ISO 23081 | Metadata for preservation | MS02-ANALYZER | SP03-Procedural Classifier | Metadati standard per gestione archivi |
| ISO 15489 | Records Management | MS14-AUDIT, MS06-AGGREGATOR | SP04-Knowledge Base | Governance archivi documentali |

### Cross-References Compliance

- **Master Matrix**: [COMPLIANCE-MATRIX.md v2.1](../../COMPLIANCE-MATRIX.md) - Mapping completo AI Act, CAD, PNRR, Piano Triennale
- **PNRR Strategy**: [COMPLIANCE-UPDATE-STRATEGY.md](../../COMPLIANCE-UPDATE-STRATEGY.md) - Roadmap implementazione UC/MS

### ✅ Compliance Checklist UC7

**Prima di Deployment**:
- [ ] Formato PDF/A-1b implementato per archivio 30+ anni
- [ ] OAIS model integrato per gestione ciclo vita documentale
- [ ] Cloud storage con encryption at rest (AES-256) abilitato
- [ ] Backup geo-redundante con disaster recovery (RTO 4h, RPO 1h) testato
- [ ] Metadati ISO/IEC 23081 documentati per ogni record
- [ ] Hash validation e CRC check implementati per integrità
- [ ] Marca temporale RFC 3161 integrata da TSA certificata
- [ ] Versioning e audit trail immutabile per tutti i documenti

**Annual Compliance Review**:
- [ ] Integrità archivio verificata (hash check)
- [ ] Disaster recovery testato con recovery time misurato
- [ ] Backup completezza verificato
- [ ] Archivi obsoleti rivisti per scarto programmato
- [ ] Standard formati aggiornati (PDF/A, JPEG2000, TIFF)
- [ ] Certificazione ISO 27001 aggiornata
- [ ] Security audit eseguito su access control

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

**Versione**: 1.1 (21 novembre 2025 - PNRR & Piano Triennale compliance added)
**Prossima Review**: 21 dicembre 2025
