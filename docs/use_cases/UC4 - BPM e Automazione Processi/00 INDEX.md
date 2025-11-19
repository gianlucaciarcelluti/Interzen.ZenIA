# UC4 - BPM e Automazione Processi

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Orchestrazione e automazione dei processi aziendali con motore BPM, task management e integrazione di servizi.

### Obiettivi Principali

- **Disegno e orchestrazione processi BPM**: Disegno e orchestrazione processi BPM
- **Automazione task e workflow**: Automazione task e workflow
- **Integrazione microservizi**: Integrazione microservizi
- **Monitoring e KPI tracking**: Monitoring e KPI tracking

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **BPM e Automazione Processi**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC4.md` | Architecture | ✅ | [Vai](./00 Architettura UC4.md) |
| SP24 - Process Mining Engine | `01 SP24 - Process Mining Engine.md` | Specification | ✅ | [Vai](./01 SP24 - Process Mining Engine.md) |
| SP25 - Forecasting & Predictive Scheduling Engine | `01 SP25 - Forecasting & Predictive Scheduling Engine.md` | Specification | ✅ | [Vai](./01 SP25 - Forecasting \& Predictive Scheduling Engine.md) |
| SP26 - Intelligent Workflow Designer | `01 SP26 - Intelligent Workflow Designer.md` | Specification | ✅ | [Vai](./01 SP26 - Intelligent Workflow Designer.md) |
| SP27 - Process Analytics | `01 SP27 - Process Analytics.md` | Specification | ✅ | [Vai](./01 SP27 - Process Analytics.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | [Vai](./01 Sequence diagrams.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Process

- **[SP24](./01 SP24 - Process Mining Engine.md)** - Process Mining Engine
- **[SP27](./01 SP27 - Process Analytics.md)** - Process Analytics

### Forecasting

- **[SP25](./01 SP25 - Forecasting \& Predictive Scheduling Engine.md)** - Forecasting & Predictive Scheduling Engine

### Intelligent

- **[SP26](./01 SP26 - Intelligent Workflow Designer.md)** - Intelligent Workflow Designer

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ L. 241/1990
- ☑ CAD
- ☑ AI Act
- ☐ GDPR - Regolamento 2016/679
- ☐ eIDAS - Regolamento 2014/910
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
UC4 - BPM e Automazione Processi/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC4.md       ← Architecture
├── 01 SP24 - Process Mining Engine.md
├── 01 SP25 - Forecasting & Predictive Scheduling Engine.md
├── 01 SP26 - Intelligent Workflow Designer.md
├── 01 SP27 - Process Analytics.md
├── 01 Sequence diagrams.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC4.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC4.md` | 1 hour |

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
