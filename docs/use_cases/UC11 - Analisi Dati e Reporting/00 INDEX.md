# UC11 - Analisi Dati e Reporting

**Status**: Active
**Version**: 1.0
**Last Updated**: 2025-11-19
**Owner**: Architecture Team

---

## 📌 Overview

Data lake, ETL, analytics avanzate, ML, dashboarding self-service e export dati con supporto big data.

### Obiettivi Principali

- **ETL e data processing**: ETL e data processing
- **Advanced analytics e ML models**: Advanced analytics e ML models
- **Self-service BI dashboards**: Self-service BI dashboards
- **Real-time streaming analytics**: Real-time streaming analytics

### Ambito (Scope)

Questo UC copre tutti gli aspetti della **Analisi Dati e Reporting**, incluse:
- Acquisizione e elaborazione dati
- Processamento e elaborazione
- Storage e conservazione
- Recupero e reporting

**Escluso**: Temi non strettamente correlati al presente UC sono trattati negli UC correlati.

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC11.md` | Architecture | ✅ | [Vai](./00 Architettura UC11.md) |
| SP58 - Data Lake & Storage Management | `01 SP58 - Data Lake & Storage Management.md` | Specification | ✅ | [Vai](./01 SP58 - Data Lake \& Storage Management.md) |
| SP59 - ETL & Data Processing Pipelines | `01 SP59 - ETL & Data Processing Pipelines.md` | Specification | ✅ | [Vai](./01 SP59 - ETL \& Data Processing Pipelines.md) |
| SP60 - Advanced Analytics & ML | `01 SP60 - Advanced Analytics & ML.md` | Specification | ✅ | [Vai](./01 SP60 - Advanced Analytics \& ML.md) |
| SP61 - Self-Service Analytics Portal | `01 SP61 - Self-Service Analytics Portal.md` | Specification | ✅ | [Vai](./01 SP61 - Self-Service Analytics Portal.md) |
| SP62 - Data Quality & Governance | `01 SP62 - Data Quality & Governance.md` | Specification | ✅ | [Vai](./01 SP62 - Data Quality \& Governance.md) |
| SP63 - Real-Time Analytics & Streaming | `01 SP63 - Real-Time Analytics & Streaming.md` | Specification | ✅ | [Vai](./01 SP63 - Real-Time Analytics \& Streaming.md) |
| SP64 - Predictive Analytics & Forecasting | `01 SP64 - Predictive Analytics & Forecasting.md` | Specification | ✅ | [Vai](./01 SP64 - Predictive Analytics \& Forecasting.md) |
| SP65 - Performance Monitoring & Alerting | `01 SP65 - Performance Monitoring & Alerting.md` | Specification | ✅ | [Vai](./01 SP65 - Performance Monitoring \& Alerting.md) |
| SP66 - Data Security & Compliance | `01 SP66 - Data Security & Compliance.md` | Specification | ✅ | [Vai](./01 SP66 - Data Security \& Compliance.md) |
| SP67 - API Gateway & Integration Layer | `01 SP67 - API Gateway & Integration Layer.md` | Specification | ✅ | [Vai](./01 SP67 - API Gateway \& Integration Layer.md) |
| SP68 - DevOps & CI CD Pipeline | `01 SP68 - DevOps & CI CD Pipeline.md` | Specification | ✅ | [Vai](./01 SP68 - DevOps \& CI CD Pipeline.md) |
| SP69 - Disaster Recovery & Business Continuity | `01 SP69 - Disaster Recovery & Business Continuity.md` | Specification | ✅ | [Vai](./01 SP69 - Disaster Recovery \& Business Continuity.md) |
| SP70 - Compliance & Audit Management | `01 SP70 - Compliance & Audit Management.md` | Specification | ✅ | [Vai](./01 SP70 - Compliance \& Audit Management.md) |
| SP71 - Performance Optimization & Scaling | `01 SP71 - Performance Optimization & Scaling.md` | Specification | ✅ | [Vai](./01 SP71 - Performance Optimization \& Scaling.md) |
| SP72 - Incident Management & Escalation | `01 SP72 - Incident Management & Escalation.md` | Specification | ✅ | [Vai](./01 SP72 - Incident Management \& Escalation.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### Data

- **[SP58](./01 SP58 - Data Lake \& Storage Management.md)** - Data Lake & Storage Management
- **[SP62](./01 SP62 - Data Quality \& Governance.md)** - Data Quality & Governance
- **[SP66](./01 SP66 - Data Security \& Compliance.md)** - Data Security & Compliance

### ETL

- **[SP59](./01 SP59 - ETL \& Data Processing Pipelines.md)** - ETL & Data Processing Pipelines

### Advanced

- **[SP60](./01 SP60 - Advanced Analytics \& ML.md)** - Advanced Analytics & ML

### Self

- **[SP61](./01 SP61 - Self-Service Analytics Portal.md)** - Self-Service Analytics Portal

### Real

- **[SP63](./01 SP63 - Real-Time Analytics \& Streaming.md)** - Real-Time Analytics & Streaming

### Predictive

- **[SP64](./01 SP64 - Predictive Analytics \& Forecasting.md)** - Predictive Analytics & Forecasting

### Performance

- **[SP65](./01 SP65 - Performance Monitoring \& Alerting.md)** - Performance Monitoring & Alerting
- **[SP71](./01 SP71 - Performance Optimization \& Scaling.md)** - Performance Optimization & Scaling

### API

- **[SP67](./01 SP67 - API Gateway \& Integration Layer.md)** - API Gateway & Integration Layer

### DevOps

- **[SP68](./01 SP68 - DevOps \& CI CD Pipeline.md)** - DevOps & CI CD Pipeline

### Disaster

- **[SP69](./01 SP69 - Disaster Recovery \& Business Continuity.md)** - Disaster Recovery & Business Continuity

### Compliance

- **[SP70](./01 SP70 - Compliance \& Audit Management.md)** - Compliance & Audit Management

### Incident

- **[SP72](./01 SP72 - Incident Management \& Escalation.md)** - Incident Management & Escalation

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ CAD
- ☑ GDPR
- ☑ D.Lgs 33/2013
- ☐ L. 241/1990 - Procedimento Amministrativo
- ☐ eIDAS - Regolamento 2014/910
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📂 Struttura File UC

```
UC11 - Analisi Dati e Reporting/
├── 00 INDEX.md                          ← START HERE
├── 00 Architettura UC11.md       ← Architecture
├── 01 SP58 - Data Lake & Storage Management.md
├── 01 SP59 - ETL & Data Processing Pipelines.md
├── 01 SP60 - Advanced Analytics & ML.md
├── 01 SP61 - Self-Service Analytics Portal.md
├── 01 SP62 - Data Quality & Governance.md
├── 01 SP63 - Real-Time Analytics & Streaming.md
├── 01 SP64 - Predictive Analytics & Forecasting.md
├── 01 SP65 - Performance Monitoring & Alerting.md
├── 01 SP66 - Data Security & Compliance.md
├── 01 SP67 - API Gateway & Integration Layer.md
├── 01 SP68 - DevOps & CI CD Pipeline.md
├── 01 SP69 - Disaster Recovery & Business Continuity.md
├── 01 SP70 - Compliance & Audit Management.md
├── 01 SP71 - Performance Optimization & Scaling.md
├── 01 SP72 - Incident Management & Escalation.md
```

---

## 🔗 Quick Links

### Per Role

| Role | Start Here | Tempo |
|------|-----------|-------|
| Product Manager | `00 Architettura UC11.md` | 15 min |
| Developer | Sequence Diagram | 30 min |
| Tester | Index + SP Rilevanti | 45 min |
| Compliance | Conformità Normativa section | 30 min |
| Architect | `00 Architettura UC11.md` | 1 hour |

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
