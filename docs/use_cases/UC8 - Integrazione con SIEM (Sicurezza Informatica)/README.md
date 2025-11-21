# UC8 - Integrazione con SIEM (Sicurezza Informatica)

**Status**: Active
**Version**: 1.1
**Last Updated**: 2025-11-21
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

## ⚡ Quick Start

1. **Raccolta Log**: Aggregazione log da tutti i MS e componenti
2. **Analisi**: Pattern detection e anomaly detection real-time
3. **Alerting**: Notifiche su eventi critici e violazioni sicurezza
4. **Compliance**: Report automatici per audit GDPR/CAD
5. **Investigazione**: Tracciamento forensico di incidenti

**Documentazione correlata**:
- [MS14 - AUDIT](../../microservices/MS14-AUDIT/README.md)
- [MS13 - SECURITY](../../microservices/MS13-SECURITY/README.md)

---

## 🗺️ Navigation Matrix

| Componente | File | Tipo | Status | Riferimento |
|-----------|------|------|--------|-------------|
| Architettura Generale | `00 Architettura UC8.md` | Architecture | ✅ | @-ARCHITETTURA.md) |
| SP38 - SIEM Collector | `01 SP38 - Collettore SIEM.md` | Specification | ✅ | [Vai](./SP38 - Collettore SIEM.md) |
| SP39 - SIEM Processor | `01 SP39 - Elaboratore SIEM.md` | Specification | ✅ | [Vai](./SP39 - Elaboratore SIEM.md) |
| SP40 - SIEM Storage | `01 SP40 - Archiviazione SIEM.md` | Specification | ✅ | [Vai](./SP40 - Archiviazione SIEM.md) |
| SP41 - SIEM Analytics & Reporting | `01 SP41 - Analitiche SIEM e Reporting.md` | Specification | ✅ | [Vai](./SP41 - Analitiche SIEM e Reporting.md) |
| Sequence diagrams | `01 Sequence diagrams.md` | Diagram | ✅ | C-SEQUENCES.md) |

---

## 📊 SubProgetti (SP) - Overview Rapido

### SIEM

- **[SP38](./SP38 - Collettore SIEM.md)** - SIEM Collector
- **[SP39](./SP39 - Elaboratore SIEM.md)** - SIEM Processor
- **[SP40](./SP40 - Archiviazione SIEM.md)** - SIEM Storage
- **[SP41](./SP41 - Analitiche SIEM e Reporting.md)** - SIEM Analytics & Reporting

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ CAD (Codice dell'Amministrazione Digitale)
- ☑ GDPR (Regolamento 2016/679)
- ☑ PNRR (Piano Nazionale Ripresa e Resilienza)
- ☑ Piano Triennale AgID 2024-2026
- ☑ NIS2 Directive (2022/2555/EU)
- ☐ L. 241/1990 - Procedimento Amministrativo
- ☐ eIDAS - Regolamento 2014/910
- ☐ AI Act - Regolamento 2024/1689
- ☐ D.Lgs 42/2004 - Codice Beni Culturali
- ☐ D.Lgs 152/2006 - Codice dell'Ambiente
- ☐ D.Lgs 33/2013 - Decreto Trasparenza

**Dettagli per SP**: Vedere sezione "🏛️ Conformità Normativa" in ogni SPECIFICATION.md di SP.

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📋 Conformità PNRR (Piano Nazionale Ripresa e Resilienza)

### Missione 1, Componente 1.4: Sicurezza Informatica della PA

**Obiettivo**: Rafforzare la capacità di rilevamento e risposta agli incidenti informatici nella Pubblica Amministrazione.

| Requisito PNRR | Implementazione UC8 | Status |
|---|---|---|
| **Monitoraggio 24/7** | SIEM con alerting real-time su tutti i componenti | ✅ SP38-SP41 |
| **Incident Response <30 min** | SLA di escalation automatica per eventi critici | ✅ SP39 Processor |
| **Log retention 12+ mesi** | Storage geo-ridondante con RTO 4h, RPO 1h | ✅ SP40 Storage |
| **Anomaly detection automatica** | ML-based pattern detection via SP39 | ✅ SP39 Processor |
| **Real-time alerting** | Push notifications + SOAR integration | ✅ SP38 Collector |
| **Compliance reporting** | Automatizzato per milestone PNRR | ✅ SP41 Analytics |

**Conformità raggiunta**: UC8 implementa tutte le misure richieste da M1C1.4 per la sicurezza della PA.

---

## 📚 Conformità Piano Triennale AgID 2024-2026

### Capitolo 5: Dati e Intelligenza Artificiale (Sicurezza Informatica)

#### 5.1 Requisiti SIEM

| Requisito Piano Triennale | Mappatura UC8 | Riferimento |
|---|---|---|
| **SIEM obbligatorio per PA** | Implementato come UC strategico | Intero UC |
| **Centralizzazione log** | SP38 Collettore raccoglie da tutti i componenti | SP38 |
| **Alerting real-time** | SP38 + SP39 con threshold configurabili | SP38-39 |
| **Threat intelligence** | SP39 integra feed di threat intelligence | SP39 |
| **Forensics & investigation** | SP41 fornisce ricerca storica e analytics avanzata | SP41 |

#### 5.2 Protezione Infrastrutture Critiche (NIS2 Compliance)

| Controllo NIS2 | Implementazione UC8 | SLA |
|---|---|---|
| **Identificazione risorse critiche** | Classificazione entità (essential/important) | Configurazione iniziale |
| **Monitoring real-time** | 24/7 SIEM con SLA 99.95% availability | SP38-41 |
| **Incident reporting (72h)** | UC9 integra notifica incidenti a CSIRT | UC9 |
| **Threat intelligence sharing** | SP39 sottoscrive feed pubblici/privati | SP39 |
| **Supply chain security** | Monitoring dipendenze esterne | SP39 |

### Capitolo 7: Sicurezza Informatica (NIS2 Implementation)

#### 7.1 Zero Trust Architecture

UC8 supporta Zero Trust mediante:
- **Verificazione continua**: SP39 monitora comportamenti anomali
- **Least privilege access**: Logging di tutti gli accessi
- **Encryption in transit**: TLS 1.3 su tutti i collector endpoint
- **Encryption at rest**: AES-256 per storage log sensibili

#### 7.2 Incident Management & Response

| Fase | Responsabile UC8 | Timing |
|---|---|---|
| **Detection** | SP38 + SP39 (anomaly detection) | <1 minuto |
| **Analysis** | SP39 Processor (correlation analysis) | <5 minuti |
| **Escalation** | SP38 Alerting (SOAR integration) | <10 minuti |
| **Response Coordination** | SP41 Analytics + UC9 | <30 minuti |
| **Evidence Collection** | SP40 Storage (immutable audit trail) | Continuamente |

---

## 🔐 Conformità NIS2 Directive (2022/2555/EU)

### Articolo 6: Identificazione Entità Critiche

UC8 implementa la categorizzazione:

```
TIPO ENTITÀ                      | MONITORING SPECIFICO
================================|=============================================
Essential Services (ES)          | • Monitoraggio 24/7 dedicato
- Pubblica Amministrazione       | • Alert SLA: 15 minuti per evento critico
- Sanità                         | • Incident reporting: 72 ore a CSIRT
- Telecomunicazioni              | • Threat assessment settimanale
                                 |
Important Entities (IE)          | • Monitoraggio standard 24/7
- Infrastrutture critiche        | • Alert SLA: 1 ora per evento critico
- Provider servizi digitali      | • Incident reporting: 30 giorni
                                 | • Threat assessment mensile
```

### Articolo 18: Incident Reporting Requirements

**Timeline di conformità UC8**:

| Fase | Deadline | Responsabile |
|---|---|---|
| **Rilevamento anomalia** | < 1 minuto | SP38 Collector |
| **Analisi preliminare** | < 5 minuti | SP39 Processor |
| **Classificazione incidente** | < 30 minuti | SP39 + UC9 |
| **Notifica interna** | < 2 ore | UC9 Compliance |
| **Notifica CSIRT** | < 72 ore | UC9 (Entità ES) |
| **Public disclosure** | Per legge | UC9 |

### Articolo 20: Supply Chain Security

UC8 monitora:
- **Third-party API health**: SP38 health check endpoints
- **Dependency vulnerabilities**: SP39 correlazione con CVE database
- **Authentication failures**: SP40 audit trail per accessi esterni
- **Data exfiltration attempts**: SP39 anomaly detection

---

## ✅ Checklist Conformità Pre-Deployment

### PNRR M1C1.4 - Sicurezza Informatica

- [ ] SIEM deployment completato su tutti i nodi (SP38)
- [ ] 24/7 monitoring attivato con SLA 99.95%
- [ ] Incident response SLA <30 minuti configurato
- [ ] Log retention 12+ mesi implementato (SP40)
- [ ] Anomaly detection ML models addestrati e validati
- [ ] Real-time alerting integrato con SOAR
- [ ] Backup geografico redundante (RTO 4h, RPO 1h) operativo
- [ ] Compliance dashboard PNRR pronto per audit

### NIS2 Directive - Incident Management

- [ ] Entità critiche classificate (Essential/Important)
- [ ] Monitoring 24/7 attivato per tutte le ES entities
- [ ] CSIRT notification procedure integrata in UC9
- [ ] 72-hour incident reporting workflow testato
- [ ] Threat intelligence feed attivo in SP39
- [ ] Supply chain dependencies mappate e monitorate
- [ ] Forensics & investigation tools disponibili (SP41)
- [ ] Incident response team trained and ready

### Piano Triennale Cap 5 & 7 - SIEM & Security

- [ ] SIEM correlazione events attivata (SP39)
- [ ] Threat intelligence sharing implementato
- [ ] Zero Trust monitoring attivato
- [ ] TLS 1.3 su tutti i collector endpoint
- [ ] AES-256 encryption per storage sensibile
- [ ] Access control logging completato
- [ ] Backup & disaster recovery testato
- [ ] Security audit annuale programmato

---

## 📅 Checklist Conformità Annuale

**Frequenza**: Annuale (Novembre di ogni anno)

- [ ] Audit trail completeness verificata (% copertura)
- [ ] NIS2 incident statistics analizzate
- [ ] PNRR KPI misurati e reportati (M1C1.4)
- [ ] Threat intelligence effectiveness valutata
- [ ] Anomaly detection model performance review
- [ ] Disaster recovery drill completato (RTO/RPO validation)
- [ ] Staff training su nuove minacce completato
- [ ] Compliance report generato per stakeholder
- [ ] Improvements plan documentato per anno successivo

---

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

**Versione**: 1.1 (21 novembre 2025)
**Prossima Review**: 21 dicembre 2025

### Changelog v1.1

**Aggiunte**:
- Conformità PNRR M1C1.4 (Sicurezza Informatica della PA) con SLA monitoraggio 24/7
- Conformità Piano Triennale Cap 5 & 7 (SIEM requirements e NIS2 compliance)
- Conformità NIS2 Directive (2022/2555/EU) con timeline incident reporting 72h
- Checklist pre-deployment per PNRR, NIS2 e Piano Triennale
- Checklist conformità annuale per audit e validation
