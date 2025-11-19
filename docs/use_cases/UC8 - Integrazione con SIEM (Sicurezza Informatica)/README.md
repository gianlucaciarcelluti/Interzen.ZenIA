# UC8 - Integrazione con SIEM (Sicurezza Informatica)

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Integrazione con Security Information and Event Management per monitoraggio sicurezza, alerting, anomaly detection.

### Obiettivi Principali

- **Raccolta log da tutti i componenti**: Raccolta log da tutti i componenti
- **Analisi anomalie e pattern detection**: Analisi anomalie e pattern detection
- **Alerting real-time su eventi critici**: Alerting real-time su eventi critici
- **Report compliance security**: Report compliance security

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Integrazione con SIEM (Sicurezza Informatica)**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC8.md` | Architecture | ✅ | [Vai](./00 Architettura UC8.md) |
| SP38 - SIEM Collector | `01 SP38 - Collettore SIEM.md` | Specification | ✅ | [Vai](./01 SP38 - Collettore SIEM.md) |
| SP39 - SIEM Processor | `01 SP39 - Elaboratore SIEM.md` | Specification | ✅ | [Vai](./01 SP39 - Elaboratore SIEM.md) |
| SP40 - SIEM Storage | `01 SP40 - Archiviazione SIEM.md` | Specification | ✅ | [Vai](./01 SP40 - Archiviazione SIEM.md) |
| SP41 - SIEM Analytics & Reporting | `01 SP41 - Analitiche SIEM e Reporting.md` | Specification | ✅ | [Vai](./01 SP41 - Analitiche SIEM e Reporting.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | [Vai](./01 Sequence diagrams.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### SIEM

- **[SP38](./01 SP38 - Collettore SIEM.md)** - SIEM Collector
- **[SP39](./01 SP39 - Elaboratore SIEM.md)** - SIEM Processor
- **[SP40](./01 SP40 - Archiviazione SIEM.md)** - SIEM Storage
- **[SP41](./01 SP41 - Analitiche SIEM e Reporting.md)** - SIEM Analytics & Reporting

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ CAD
- ☑ GDPR
- ☐ L. 241/1990 - Procedimento Amministrativo
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
UC8 - Integrazione con SIEM (Sicurezza Informatica)/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC8.md       ← Architecture
├── 01 SP38 - Collettore SIEM.md
├── 01 SP39 - Elaboratore SIEM.md
├── 01 SP40 - Archiviazione SIEM.md
├── 01 SP41 - Analitiche SIEM e Reporting.md
├── 01 Sequence diagrams.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC8.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC8.md` | 1 hour |

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
