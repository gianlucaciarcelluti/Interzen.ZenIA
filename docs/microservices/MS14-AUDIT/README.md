# MS14-AUDIT - Microservice

**Status**: Active
**Version**: 1.1
**Last Updated**: 2025-11-21
**Owner**: Audit & Compliance Team

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)

---

## Avvio Rapido (5 minuti)

### Che cos'è MS14-AUDIT?
MS14-AUDIT fornisce audit trail immutabile centralizzato per tutta la piattaforma ZenIA, con conformità a PNRR, AI Act, e GDPR. Implementa event logging, evidence collection, breach notification, e compliance reporting automatici.

### Responsabilità principali
- **Event Collection**: Raccolta centralizzata di audit log da tutti i MS
- **Immutable Storage**: Append-only storage su Elasticsearch con integrity validation
- **Compliance Evidence**: Raccolta automatica di evidenze per PNRR milestone audit
- **Breach Notification**: Integration con UC9 per GDPR 72h incident reporting (Art. 33-34)
- **AI Act Records**: Tracciamento decisioni automatizzate (Art. 30) + human oversight (Art. 31)
- **Retention Management**: 12+ mesi retention policy con archivio sicuro

### Primi passi
1. Consulta [SPECIFICATION.md](SPECIFICATION.md) per le specifiche tecniche dettagliate
2. Controlla `docker-compose.yml` per il setup locale
3. Rivedi [API.md](API.md) per gli endpoint di integrazione
4. Esplora la cartella [examples/](examples/) per esempi di request/response

### Stack tecnologico
- **Linguaggio**: Python 3.10+
- **API**: FastAPI (OpenAPI 3.0)
- **Database**: Elasticsearch (cluster + replica)
- **Cache**: Redis Streams / Kafka
- **Monitoring**: Prometheus + Grafana
- **Security**: JWT, OAuth2, RBAC, TLS 1.3

### Dipendenze
Vedi [SPECIFICATION.md](SPECIFICATION.md) per i dettagli sulle dipendenze.

---

## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

- ☑ PNRR (Piano Nazionale Ripresa e Resilienza)
- ☑ AI Act (Regolamento 2024/1689)
- ☑ GDPR (Regolamento 2016/679)
- ☑ CAD (Codice dell'Amministrazione Digitale)
- ☑ NIS2 Directive (2022/2555/EU)
- ☐ eIDAS - Regolamento 2014/910
- ☐ D.Lgs 42/2004 - Codice Beni Culturali

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📋 Conformità PNRR (Piano Nazionale Ripresa e Resilienza)

### Missione 1, Componente 1.4: Audit Trail Immutabile

**Obiettivo**: Implementare audit trail immutabile per tracciabilità completa e evidence collection per milestone PNRR.

| Requisito PNRR | Implementazione MS14 | Status |
|---|---|---|
| **Audit trail immutabile** | Elasticsearch append-only con blockchain-optional | ✅ |
| **Evidence collection** | Automatic collection per PNRR milestone | ✅ |
| **Compliance dashboard** | Real-time reporting per audit trail | ✅ |
| **Log retention 12+ mesi** | Configurabile, default 12 months + archive | ✅ |
| **Tracciabilità chi/cosa/quando** | User, IP, timestamp, action, outcome logged | ✅ |
| **Integrità documentale** | Hash validation + digital signature | ✅ |

**Conformità raggiunta**: MS14 implementa audit trail completamente tracciabile per milestone compliance.

---

## 📚 Conformità AI Act (Regolamento 2024/1689)

### Articolo 14: Record Keeping Automatico

MS14 mantiene registri automatici di tutte le operazioni:

```
AI Act Record Keeping Requirements (Art. 14)
│
├─ Art. 14(1): Conservazione documenti di conformità
│  └─ MS14: Automated collection + signed storage
│
├─ Art. 27: Risk management documentation
│  └─ MS14: Links a UC9 (risk register)
│
├─ Art. 30: Automated decision records
│  └─ MS14: Logs di tutte le decisioni AI-driven
│
└─ Art. 31: Human oversight logging
   └─ MS14: Traccia approval/rejection human
```

### Articolo 30: Automated Decision Records

MS14 registra tutte le decisioni automatizzate per audit:

| Informazione | Registrata da MS14 | Utilizzo |
|---|---|---|
| **Decision ID** | Unique identifier per ogni decisione | Tracciabilità |
| **Input Data** | Parametri utilizzati per decisione | DPIA audit |
| **Decision Logic** | Quale policy/rule è stata applicata | Explainability |
| **Decision Output** | Risultato della decisione | Verification |
| **Timestamp** | Quando la decisione è stata presa | Timeline |
| **User/System** | Chi ha generato la decisione | Accountability |
| **Human Review** | Se e quando è stata revisionata | Oversight |

### Articolo 31: Human Oversight Logging

MS14 traccia intervento umano su decisioni AI:

| Evento | Registrato | SLA |
|---|---|---|
| **Automated Decision Made** | Decision log + notification | Real-time |
| **Human Review Requested** | Escalation log | < 1 hour |
| **Review Completed** | Approval/rejection + reviewer ID | < 24 hours |
| **Appeal Lodged** | Appeal log con motivazione | < 15 days |
| **Appeal Resolved** | Final decision + rationale | < 30 days |

---

## 🛡️ Conformità GDPR (Regolamento 2016/679)

### Articolo 5: Principle of Integrity and Confidentiality

MS14 implementa principi GDPR tramite:

| Principio GDPR | Implementazione MS14 | Control |
|---|---|---|
| **Lawfulness** | Audit trail per tracking legitimacy | Access logs |
| **Fairness** | Automated decision tracking (Art. 30) | Decision logs |
| **Transparency** | Availability of records per interessati | Data subject access |
| **Integrity** | Hash validation + digital signature | Immutability |
| **Confidentiality** | Encryption + access control | Role-based access |
| **Accountability** | Full audit trail per accountability | 12+ month retention |

### Articolo 32: Security of Processing

MS14 documenta misure di sicurezza:

- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Access Control**: Role-based access con RBAC
- **Authentication**: JWT + OAuth2 con MFA
- **Audit Trail**: Append-only Elasticsearch logs
- **Integrity**: Hash validation per log records
- **Confidentiality**: Role-based query filtering
- **Backup**: Elasticsearch snapshots con encryption

### Articolo 33-34: Breach Notification Procedure

MS14 integra con UC8 + UC9 per **Breach Notification Timeline**:

```
Data Breach Discovery Flow:
│
├─ T+0 (Detection)
│  ├─ UC8 SIEM: Anomaly detected
│  └─ MS14: Security event logged
│
├─ T+1 min (Classification)
│  └─ UC9 SP43: Risk assessment (breach vs anomaly)
│
├─ T+5 min (Escalation)
│  ├─ MS14: Breach log flagged as PNRR_INCIDENT
│  └─ UC9: Evidence collection initiated
│
├─ T+30 min (Internal Notification)
│  ├─ MS14: Alert generated for DPO/Security team
│  └─ UC9: Incident investigation started
│
├─ T+<72 hours (Authority Notification)
│  ├─ UC9: GDPR Art. 33 notification to authority
│  └─ MS14: Breach log with timeline + evidence
│
└─ T+<96 hours (Data Subject Notification)
   ├─ UC9: GDPR Art. 34 notification to interessati
   └─ MS14: Final incident report generated
```

---

## 📊 Conformità NIS2 Directive (2022/2555/EU)

### Logging & Monitoring per Critical Infrastructure

MS14 implementa logging conforme NIS2:

| Requisito NIS2 | Implementazione MS14 | Retention |
|---|---|---|
| **Authentication attempts** | Success/failure logged | 12+ mesi |
| **Access to sensitive data** | Who, what, when logged | 12+ mesi |
| **Configuration changes** | Before/after values logged | 12+ mesi |
| **Privilege escalation** | All sudo/admin actions logged | 12+ mesi |
| **Account creation/deletion** | User lifecycle logged | 12+ mesi |
| **Policy modifications** | Changes tracked with diffs | 12+ mesi |
| **Failed API calls** | Error patterns for anomaly detection | 12+ mesi |
| **External connections** | Network activity to third-parties | 12+ mesi |

---

## 🔍 Evidence Collection per PNRR

MS14 raccoglie automaticamente evidenze per PNRR milestone audit:

### Category A: Access Control Evidence

```
Evidence Type        | Generated By         | Metric
────────────────────┼─────────────────────┼──────────────────────
Authentication logs  | MS13 + MS14 | % successful logins per role
MFA usage           | MS13 audit | % users with MFA enabled
Privilege changes   | MS14 | Number of elevation events
Access denial events | MS14 | Attempts to access unauthorized resources
```

### Category B: Data Protection Evidence

```
Evidence Type        | Generated By         | SLA
────────────────────┼─────────────────────┼──────────────────
Encryption in use   | MS13 TLS/AES events | Real-time monitoring
Data access logs    | MS14 | User X accessed Resource Y at time Z
Data modification   | MS14 | Who changed what, when, what changed
Deletion events     | MS14 | Retention of deletion records
Backup verification | MS14 | RTO/RPO compliance checks
```

### Category C: Security Incident Evidence

```
Evidence Type        | Generated By         | Frequency
────────────────────┼─────────────────────┼───────────────
Failed login patterns| MS14 + UC8 | Real-time detection
Anomalous access    | UC8 SIEM + MS14 | Continuous
Configuration drift | MS14 | Daily baseline comparison
Vulnerability scans | UC8 SIEM | Weekly/Monthly
Patch compliance    | MS14 | Monthly verification
```

---

## ✅ Checklist Conformità Pre-Deployment

### PNRR M1C1.4 - Audit Trail Immutabile

- [ ] Elasticsearch cluster configurato con replica (minimo 3 node)
- [ ] Append-only mode abilitato (no delete/update)
- [ ] Encryption at rest per Elasticsearch
- [ ] TLS 1.3 su tutti i collector endpoint
- [ ] Log retention 12+ mesi configurato
- [ ] Backup automatico su storage esterno (daily)
- [ ] Hash validation per integrità log implementato
- [ ] Evidence collection dashboard pronto per milestone audit
- [ ] Compliance report generator testato
- [ ] Integration con UC8 + UC9 verified (incident escalation)

### AI Act - Record Keeping & Automated Decision

- [ ] Automated decision logging attivato (Art. 30)
- [ ] Decision ID generator implementato per uniqueness
- [ ] Input/output data preserved per DPIA
- [ ] Decision logic versioning per audit trail
- [ ] Human oversight escalation procedure testata (Art. 31)
- [ ] Appeal process logged (start → resolution)
- [ ] Timestamp accuracy verificata (TLS/NTP)
- [ ] Record retention 12+ mesi per AI Act Art. 14

### GDPR - Data Protection & Breach Notification

- [ ] Breach notification workflow integrato (T+72h SLA)
- [ ] DPA contact info configurato per automatic notification
- [ ] Data subject notification procedure documentata
- [ ] Role-based access control per audit trail (Art. 5)
- [ ] Encryption for sensitive audit logs
- [ ] Access logs per data subject (Art. 15 right to access)
- [ ] Audit trail per DPIA evidence (Art. 35)
- [ ] Data retention policy implementata

### NIS2 - Logging for Critical Infrastructure

- [ ] Authentication logging (success/failure)
- [ ] Sensitive data access logging
- [ ] Configuration change logging
- [ ] Privilege escalation logging
- [ ] Failed API call patterns monitored
- [ ] Log aggregation from all services operational
- [ ] Alert rules for anomaly detection
- [ ] Regular log analysis (monthly review)

---

## 📅 Checklist Conformità Annuale

**Frequenza**: Annuale (Novembre di ogni anno)

- [ ] Audit trail completeness verification (% copertura events)
- [ ] Evidence collection effectiveness per PNRR milestone
- [ ] AI Act automated decision statistics analyzed
- [ ] GDPR breach statistics reviewed (incident rate)
- [ ] NIS2 incident data analyzed (patterns, trends)
- [ ] Log retention policy compliance verified
- [ ] Elasticsearch cluster performance audit
- [ ] Backup recovery drill completato (restore test)
- [ ] Access control audit (who accessed what, when)
- [ ] Compliance report for governance stakeholder prepared

---

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)
