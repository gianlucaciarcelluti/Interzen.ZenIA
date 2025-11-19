# Quick Reference - Architettura ZenIA

Documento di orientamento veloce su struttura, mapping e organizzazione.

---

## 1. Numeri Chiave

```
11 Casi d'Uso (UC1-UC11)
├── 72 Sottoprogetti (SP01-SP72)
│   ├── Core Analytics (SP58-SP64): 7
│   ├── Infrastructure (SP65-SP72): 8
│   ├── User Support (SP51-SP57): 7
│   ├── Compliance (SP42-SP50): 9
│   ├── SIEM (SP38-SP41): 4
│   ├── Archive (SP33-SP37): 5
│   ├── Signature (SP29-SP32): 4
│   ├── Production Docs (SP01-SP11): 11
│   ├── BPM (SP24-SP27): 4
│   ├── Governance (SP20-SP23): 4
│   ├── Protocol (SP01, SP16-SP19): 5
│   └── Document Mgmt (SP02, SP07, SP12-SP15): 6

└── 16 Microservizi (MS01-MS16)
    ├── Core AI: MS01, MS02, MS04, MS10
    ├── Platform: MS03, MS06, MS08, MS09, MS12
    ├── Infrastructure: MS05, MS07, MS11, MS15
    └── Cross-Cutting: MS13, MS14, MS16
```

---

## 2. Mapping Rapido UC → SP → MS

### UC1: Document Management (6 SP)
```
SP02 Document Extractor → MS01 Classifier
SP07 Content Classifier → MS01 Classifier
SP12 Semantic Search → MS02 Analyzer
SP13 Summarizer → MS02 Analyzer
SP14 Metadata Indexer → MS05 Storage
SP15 Workflow Orchestrator → MS03 Orchestrator
```

### UC2: Protocol (5 SP)
```
SP01 EML Parser → MS07 ETL
SP16 Correspondence Classifier → MS01 Classifier
SP17 Registry Suggester → MS01 Classifier
SP18 Anomaly Detector → MS02 Analyzer
SP19 Workflow Orchestrator → MS03 Orchestrator
```

### UC3: Governance (4 SP)
```
SP20 Organization Chart → MS06 Knowledge Base
SP21 Procedure Manager → MS06 Knowledge Base
SP22 Process Governance → MS02 Analyzer
SP23 Compliance Monitor → MS04 Validator
```

### UC4: BPM (4 SP)
```
SP24 Process Mining → MS02 Analyzer
SP25 Forecasting & Predictive Scheduling → MS02 Analyzer
SP26 Intelligent Workflow Designer → MS08 Workflow
SP27 Process Analytics → MS10 Analytics
```

### UC5: Integrated Docs (11 SP)
```
SP01 EML Parser → MS07 ETL
SP02 Document Extractor → MS01 Classifier
SP03 Procedural Classifier → MS01 Classifier
SP04 Knowledge Base → MS06 Knowledge Base
SP05 Template Engine → MS08 Workflow
SP06 Validator → MS04 Validator
SP07 Content Classifier → MS01 Classifier
SP08 Quality Checker → MS04 Validator
SP09 Workflow Engine → MS08 Workflow
SP10 Dashboard → MS12 User Interface
SP11 Security & Audit → MS13 Security
```

### UC6: Digital Signature (4 SP)
```
SP29 Digital Signature Engine → MS13 Security
SP30 Certificate Manager → MS13 Security
SP31 Timestamp Authority & Temporal Marking → MS13 Security
SP32 Post-Signature Auditor → MS14 Audit
```

### UC7: Archive (5 SP)
```
SP33 Archive Manager → MS01 Classifier
SP34 Preservation Predictor → MS02 Analyzer
SP35 Integrity Validator → MS04 Validator
SP36 Storage Optimizer → MS05 Storage
SP37 Archive Metadata Manager → MS06 Knowledge Base
```

### UC8: SIEM (4 SP)
```
SP38 Log Anomaly Detector → MS02 Analyzer
SP39 Incident Predictor → MS02 Analyzer
SP40 Security Alert Manager → MS09 Notification
SP41 Incident Correlation & Analysis → MS16 Monitoring
```

### UC9: Compliance (9 SP)
```
SP42 Compliance Controller → MS04 Validator
SP43 Predictive Compliance Alerting → MS02 Analyzer
SP44 Risk Analyzer → MS02 Analyzer
SP45 Remediation Suggester → MS06 Knowledge Base
SP46 Compliance Dashboard → MS12 User Interface
SP47 Compliance Audit Trail → MS14 Audit
SP48 Policy Management → MS06 Knowledge Base
SP49 Risk Registry → MS06 Knowledge Base
SP50 Compliance Training → MS12 User Interface
```

### UC10: Support (7 SP)
```
SP51 Help Desk System → MS09 Notification
SP52 Knowledge Base Management → MS06 Knowledge Base
SP53 Virtual Assistant & Chatbot → MS02 Analyzer
SP54 User Training Platform → MS12 User Interface
SP55 Self-Service Portal → MS12 User Interface
SP56 Support Analytics & Reporting → MS10 Analytics
SP57 User Feedback Management → MS10 Analytics
```

### UC11: Analytics (15 SP)

**Core Analytics (7 SP)**:
```
SP58 Data Lake & Storage Management → MS05 Storage
SP59 ETL & Data Processing Pipelines → MS07 ETL
SP60 Advanced Analytics & ML → MS10 Analytics
SP61 Self-Service Analytics Portal → MS12 User Interface
SP62 Data Quality & Governance → MS04 Validator
SP63 Real-Time Analytics & Streaming → MS10 Analytics
SP64 Predictive Analytics & Forecasting → MS10 Analytics
```

**Infrastructure (8 SP - Cross-Cutting)**:
```
SP65 Performance Monitoring & Alerting → MS16 Monitoring
SP66 Data Security & Compliance → MS13 Security
SP67 API Gateway & Integration Layer → MS11 Integration Hub
SP68 DevOps & CI/CD Pipeline → MS15 Configuration
SP69 Disaster Recovery & Business Continuity → MS13 Security
SP70 Compliance & Audit Management → MS14 Audit
SP71 Performance Optimization & Scaling → MS16 Monitoring
SP72 Incident Management & Escalation → MS14 Audit
```

---

## 3. MS Usage by UC

| MS | UC1 | UC2 | UC3 | UC4 | UC5 | UC6 | UC7 | UC8 | UC9 | UC10 | UC11 |
|----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|------|
| MS01 Classifier | ✓ | ✓ |  |  | ✓ |  | ✓ |  |  |  |  |
| MS02 Analyzer | ✓ |  |  |  | ✓ |  |  | ✓ | ✓ | ✓ | ✓ |
| MS03 Orchestrator | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |  |  |  |  |
| MS04 Validator |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  | ✓ |  |  |
| MS05 Storage | ✓ |  |  |  | ✓ |  | ✓ |  |  |  | ✓ |
| MS06 Knowledge Base | ✓ |  | ✓ |  | ✓ |  |  |  | ✓ | ✓ |  |
| MS07 ETL |  | ✓ |  |  |  |  | ✓ |  |  |  | ✓ |
| MS08 Workflow |  |  | ✓ | ✓ | ✓ | ✓ |  |  |  |  |  |
| MS09 Notification |  | ✓ |  |  |  |  |  | ✓ | ✓ | ✓ |  |
| MS10 Analytics | ✓ |  |  | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ |
| MS11 Integration |  |  |  |  |  |  |  |  |  |  | ✓ |
| MS12 UI | ✓ |  |  |  | ✓ |  |  |  |  | ✓ | ✓ |
| MS13 Security | ✓ |  | ✓ |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| MS14 Audit |  | ✓ | ✓ |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| MS15 Config |  |  |  |  |  | ✓ |  |  |  |  | ✓ |
| MS16 Monitoring |  | ✓ |  | ✓ |  |  | ✓ | ✓ |  |  | ✓ |

---

## 4. SP per MS (Cosa supporta ogni MS)

### MS01 - Classifier
**SPs**: SP02, SP03, SP07, SP16, SP17, SP33
**Ruolo**: Classificazione documenti, corrispondenza, procedimenti
**Multi-UC**: UC1, UC2, UC5, UC7

### MS02 - Analyzer
**SPs**: SP12, SP13, SP18, SP22, SP24, SP27, SP34, SP38, SP39, SP43, SP44, SP53, SP60, SP64
**Ruolo**: Analisi semantica, NLP, ML inference
**Multi-UC**: UC1, UC5, UC8, UC9, UC10, UC11

### MS03 - Orchestrator
**SPs**: SP15, SP19, SP09, SP26, SP48
**Ruolo**: Orchestrazione workflow, task coordination
**Multi-UC**: UC1, UC2, UC3, UC4, UC5

### MS04 - Validator
**SPs**: SP06, SP08, SP23, SP31, SP35, SP42, SP45, SP62
**Ruolo**: Validazione semantica, strutturale, conformità
**Multi-UC**: UC5, UC6, UC7, UC9, UC11

### MS05 - Storage
**SPs**: SP02, SP14, SP36, SP58
**Ruolo**: Storage ottimizzato, indexing, caching
**Multi-UC**: UC1, UC5, UC7, UC11

### MS06 - Knowledge Base
**SPs**: SP04, SP12, SP13, SP17, SP20, SP21, SP22, SP37, SP45, SP48, SP49, SP50, SP52, SP55, SP56, SP57
**Ruolo**: Repository conoscenza, normativa, template, FAQ
**Multi-UC**: UC1, UC3, UC5, UC7, UC9, UC10

### MS07 - ETL
**SPs**: SP01, SP07, SP33, SP39, SP59, SP63
**Ruolo**: Data extraction, transformation, loading
**Multi-UC**: UC2, UC5, UC7, UC11

### MS08 - Workflow
**SPs**: SP05, SP09, SP19, SP21, SP26
**Ruolo**: BPM engine, workflow design, execution
**Multi-UC**: UC2, UC3, UC4, UC5

### MS09 - Notification
**SPs**: SP40, SP51
**Ruolo**: Alert, notification, communication multi-channel
**Multi-UC**: UC2, UC8, UC10

### MS10 - Analytics
**SPs**: SP12, SP14, SP24, SP27, SP34, SP39, SP43, SP44, SP46, SP56, SP60, SP61, SP62, SP63, SP64, SP65
**Ruolo**: Analytics, BI, reporting, forecasting
**Multi-UC**: UC1, UC4, UC8, UC9, UC10, UC11

### MS11 - Integration Hub
**SPs**: SP67
**Ruolo**: API gateway, service mesh, integration patterns
**Multi-UC**: UC11

### MS12 - User Interface
**SPs**: SP10, SP46, SP50, SP51, SP54, SP61, SP65
**Ruolo**: Dashboards, portals, user experience
**Multi-UC**: UC1, UC5, UC9, UC10, UC11

### MS13 - Security
**SPs**: SP11, SP29, SP30, SP31, SP40, SP66, SP69
**Ruolo**: Encryption, access control, security audit
**Multi-UC**: UC5, UC6, UC8, UC9, UC11

### MS14 - Audit
**SPs**: SP11, SP18, SP23, SP32, SP37, SP41, SP47, SP70, SP72
**Ruolo**: Audit logging, compliance tracking, forensics
**Multi-UC**: UC2, UC5, UC6, UC8, UC9, UC11

### MS15 - Configuration
**SPs**: SP68, SP71
**Ruolo**: Config management, IaC, environment setup
**Multi-UC**: UC11

### MS16 - Monitoring
**SPs**: SP41, SP65, SP68, SP71, SP72
**Ruolo**: Observability, metrics, alerting, incident mgmt
**Multi-UC**: UC8, UC11

---

## 5. Dipendenze Critiche

### Data Flow Principale
```
Email/PEC (SP01)
  ↓
Extract & Classify (SP02, SP07, SP16) via MS01
  ↓
Validate & Enrich (SP06, SP08, SP17) via MS04
  ↓
Route & Workflow (SP09, SP15, SP19) via MS08
  ↓
Store & Index (SP14, SP38) via MS05
  ↓
Dashboard & Analytics (SP10, SP56) via MS12, MS10
  ↓
Audit & Security (SP11, SP49) via MS13, MS14
```

### Punti Critici (Single Point of Failure)
- **MS03 Orchestrator**: Orchestrazione centrale per SP15, SP19, SP26, SP48, SP09
  - **Mitigazione**: High availability, circuit breaker, fallback

- **MS06 Knowledge Base**: Repository centrale per normativa, template, FAQ
  - **Mitigazione**: Read replicas, caching multi-layer

- **MS05 Storage**: Storage unificato
  - **Mitigazione**: Replication, backup, disaster recovery

---

## 6. GAP risolti ✅

| Gap | Posizione | Soluzione | Status |
|---|---|---|---|
| SP25 | UC4 (BPM) | Forecasting & Predictive Scheduling Engine | ✅ CREATO |
| SP31 | UC6 (Firma) | Timestamp Authority & Temporal Marking (RFC 3161) | ✅ CREATO |
| SP32 | UC6 (Firma) | Post-Signature Auditor | ✅ CREATO |
| SP37 | UC7 (Archive) | Archive Metadata Manager | ✅ CREATO |
| SP50 | UC9 (Compliance) | Compliance Training & Certification | ✅ CREATO |
| SP70 | UC11 (Infrastructure) | Incident Management & Escalation | ✅ CREATO |
| SP57 | UC10 | User Feedback Management (shared with UC10/UC11) | ✅ DOCUMENTATO |

---

## 7. Come Consultare questa Architettura

### Per Developer che implementa SP##
1. Consulta "[SP##-Nome]" in sezione 2
2. Identifica MS primario e supporto
3. Leggi doc `/docs/use_cases/UC#/01 SP##`
4. Consulta doc MS: `/docs/microservices/MS##`
5. Guarda dipendenze SP→SP e MS→MS
6. Usa [SP-DOCUMENTATION-TEMPLATE.md](./SP-DOCUMENTATION-TEMPLATE.md) se devi aggiornare

### Per Program Manager che coordina UC
1. Consulta tabella UC→SP in sezione 2
2. Conta SP totali e status di implementazione
3. Identifica dipendenze cross-SP in matrice dipendenze UC
4. Mappa risorse a SP critici
5. Pianifica ordine implementazione

### Per Architect che valida design
1. Consulta sezione "Dipendenze Critiche"
2. Verifica non c'è cyclic dependency
3. Identifica SPOF (Single Point of Failure)
4. Valida scaling strategy per MS bottleneck
5. Consulta [SP-MS-MAPPING-MASTER.md](./SP-MS-MAPPING-MASTER.md) per dettagli

### Per QA che testa integrazione
1. Consulta matrice UC→MS (sezione 3)
2. Identifica MS da testare per UC target
3. Leggi doc SP per input/output specs
4. Traccia data flow: SP→MS→SP
5. Valida SLA per latency, throughput

---

## 8. File di Riferimento Principale

| File | Scopo |
|---|---|
| [SP-MS-MAPPING-MASTER.md](./SP-MS-MAPPING-MASTER.md) | Mapping completo SP↔MS, analisi gap, raccomandazioni |
| [GAP-RESOLUTION.md](./GAP-RESOLUTION.md) | Dettagli gap SP25, SP33, SP57 e piano risoluzione |
| [SP-DOCUMENTATION-TEMPLATE.md](./SP-DOCUMENTATION-TEMPLATE.md) | Template standard per documentazione SP |
| [QUICK-REFERENCE-ARCHITECTURE.md](./QUICK-REFERENCE-ARCHITECTURE.md) | **QUESTO FILE** - Orientamento veloce |
| `/docs/use_cases/UC#/` | Folder per UC con architettura, SP singoli, matrici dipendenze |
| `/docs/microservices/MS##-*.md` | Specificazione MS singolo |

---

## 9. Checklist Coerenza

Usiamo questo per validare che documentazione è allineata:

- [ ] Ogni SP ha doc dedicato in folder UC
- [ ] Ogni SP doc specifica MS primario + supporto
- [ ] Ogni UC ha architettura con diagrama
- [ ] Ogni UC ha matrice dipendenze SP→SP
- [ ] Ogni MS ha doc con SPs che lo usano
- [ ] Gap SP25, SP33, SP57 documentati come risolti o in progress
- [ ] SP65-SP72 classificati come Cross-Cutting o UC11-specific
- [ ] UC5 ha 1 solo "00 Architettura" canonical
- [ ] Terminologia consistente (SP vs MS, SP## vs SP_##)

---

## 10. Contact & Escalation

Per domande su architettura:
- **SP specifico**: Consulta doc UC#/01 SP##.md
- **UC specifico**: Consulta doc UC#/00 Architettura
- **MS specifico**: Consulta doc /microservices/MS##.md
- **Mapping**: Consulta SP-MS-MAPPING-MASTER.md
- **Gap/Issue**: Consulta GAP-RESOLUTION.md

