# UC2 - Protocollo Informatico

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Gestione del protocollo informatico con workflow di protocollazione, smistamento automatico, audit trail completo e integrazione con sistemi PA.

### Obiettivi Principali

- **Protocollazione digitale con numerazione progressiva**: Protocollazione digitale con numerazione progressiva
- **Smistamento automatico a organi competenti**: Smistamento automatico a organi competenti
- **Gestione workflow e approvazioni**: Gestione workflow e approvazioni
- **Tracciabilità completa con audit trail**: Tracciabilità completa con audit trail

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Protocollo Informatico**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC2.md` | Architecture | ✅ | [Vai](./00 Architettura UC2.md) |
| SP- EML Parser & Email Intelligence (UC2 Protocol) | `01 SP01 - EML Parser & Email Intelligence (UC2 Protocol).md` | Specification | ✅ | [Vai](./01 SP01 - EML Parser \& Email Intelligence (UC2 Protocol).md) |
| SP16 - Correspondence Classifier | `01 SP16 - Correspondence Classifier.md` | Specification | ✅ | [Vai](./01 SP16 - Correspondence Classifier.md) |
| SP17 - Registry Suggester | `01 SP17 - Registry Suggester.md` | Specification | ✅ | [Vai](./01 SP17 - Registry Suggester.md) |
| SP18 - Anomaly Detector | `01 SP18 - Anomaly Detector.md` | Specification | ✅ | [Vai](./01 SP18 - Anomaly Detector.md) |
| SP19 - Protocol Workflow Orchestrator | `01 SP19 - Protocol Workflow Orchestrator.md` | Specification | ✅ | [Vai](./01 SP19 - Protocol Workflow Orchestrator.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | [Vai](./01 Sequence diagrams.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### EML

- **[SP01](./01 SP01 - EML Parser \& Email Intelligence (UC2 Protocol).md)** - SP- EML Parser & Email Intelligence (UC2 Protocol)

### Correspondence

- **[SP16](./01 SP16 - Correspondence Classifier.md)** - Correspondence Classifier

### Registry

- **[SP17](./01 SP17 - Registry Suggester.md)** - Registry Suggester

### Anomaly

- **[SP18](./01 SP18 - Anomaly Detector.md)** - Anomaly Detector

### Protocol

- **[SP19](./01 SP19 - Protocol Workflow Orchestrator.md)** - Protocol Workflow Orchestrator

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
UC2 - Protocollo Informatico/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC2.md       ← Architecture
├── 01 SP01 - EML Parser & Email Intelligence (UC2 Protocol).md
├── 01 SP16 - Correspondence Classifier.md
├── 01 SP17 - Registry Suggester.md
├── 01 SP18 - Anomaly Detector.md
├── 01 SP19 - Protocol Workflow Orchestrator.md
├── 01 Sequence diagrams.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC2.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC2.md` | 1 hour |

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
