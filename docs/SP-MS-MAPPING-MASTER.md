# Master Mapping: 70 Sottoprogetti (SP) ↔ 16 Microservizi (MS)

## Filosofia Architetturale

**SP (Sottoprogetti)**: Componenti logici, specifici per dominio/caso d'uso, descrivono COSA fare e per quale business value
**MS (Microservizi)**: Componenti fisici, generici, riusabili, descrivono COME implementare una capability tecnica

Ogni SP può usare 1+ MS; ogni MS supporta multipli SP da diversi UC.

---

## 1. MAPPING COMPLETO SP → MS

### UC1: Sistema di Gestione Documentale (6 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP02 | Document Extractor & Attachment Classifier | OCR, estrazione metadati, classificazione tipo doc | **MS01** Classifier | MS05 Storage | UC1, UC2, UC5 |
| SP07 | Content Classifier | Classificazione contenuto semantica, tagging | **MS01** Classifier | MS02 Analyzer | UC1, UC2, UC5, UC7 |
| SP12 | Semantic Search & Q&A Engine | Ricerca semantica, question answering | **MS02** Analyzer | MS06 Knowledge Base | UC1 |
| SP13 | Document Summarizer | Generazione riassunti, abstract documenti | **MS02** Analyzer | MS06 Knowledge Base | UC1 |
| SP14 | Metadata Indexer | Indicizzazione metadati, full-text search | **MS05** Storage | MS10 Analytics | UC1 |
| SP15 | Document Workflow Orchestrator | Orchestrazione pipeline processing documenti | **MS03** Orchestrator | MS08 Workflow | UC1 |

### UC2: Protocollo Informatico (4 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP16 | Correspondence Classifier | Classificazione tipo corrispondenza (email/PEC/istanza) | **MS01** Classifier | MS02 Analyzer | UC2 |
| SP17 | Registry Suggester | Suggerimenti classificazione titolario/registro | **MS01** Classifier | MS06 Knowledge Base | UC2 |
| SP18 | Anomaly Detector | Rilevamento pattern anomali, duplicati, irregolarità | **MS02** Analyzer | MS14 Audit | UC2, UC8, UC9 |
| SP19 | Protocol Workflow Orchestrator | Orchestrazione workflow protocollazione, registrazione | **MS03** Orchestrator | MS08 Workflow | UC2 |

### UC3: Governance (Organigramma, Procedimenti, Procedure) (4 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP20 | Organization Chart Manager | Gestione organigramma, ruoli, responsabilità | **MS06** Knowledge Base | MS03 Orchestrator | UC3 |
| SP21 | Procedure Manager | Gestione procedimenti amministrativi, linking normativa | **MS06** Knowledge Base | MS08 Workflow | UC3 |
| SP22 | Process Governance | Mappatura processi, gap analysis vs normativa | **MS02** Analyzer | MS06 Knowledge Base | UC3 |
| SP23 | Compliance Monitor | Controllo conformità policy/procedure, alert predittivi | **MS04** Validator | MS14 Audit | UC3, UC9 |

### UC4: BPM e Automazione Processi (4 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP24 | Process Mining Engine | Process mining, discovery, analisi flussi | **MS02** Analyzer | MS10 Analytics | UC4 |
| SP25 | Forecasting & Predictive Scheduling Engine | Forecasting workload, predizione colli bottiglia, ottimizzazione scheduling | **MS02** Analyzer | MS10 Analytics | UC4 |
| SP26 | Intelligent Workflow Designer | Progettazione workflow, routing intelligente, task assignment | **MS08** Workflow | MS01 Classifier | UC4 |
| SP27 | Process Analytics | Analisi performance processi, predizioni colli bottiglia | **MS10** Analytics | MS02 Analyzer | UC4 |

### UC5: Produzione Documentale Integrata (11 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP01 | EML Parser & Email Intelligence | Parsing email, estrazione metadati, attachment handling | **MS07** ETL | MS01 Classifier | UC5, UC2 |
| SP02 | Document Extractor & Attachment Classifier | (vedi UC1) | **MS01** Classifier | MS05 Storage | UC5, UC1 |
| SP03 | Procedural Classifier | Classificazione tipo procedimento amministrativo | **MS01** Classifier | MS06 Knowledge Base | UC5 |
| SP04 | Knowledge Base | Repository conoscenza, normativa, template, linee guida | **MS06** Knowledge Base | MS02 Analyzer | UC5 |
| SP05 | Template Engine | Generazione documenti da template e dati strutturati | **MS08** Workflow | MS06 Knowledge Base | UC5 |
| SP06 | Validator | Validazione semantica, completezza documenti, conformità | **MS04** Validator | MS01 Classifier | UC5, UC6, UC7 |
| SP07 | Content Classifier | (vedi UC1) | **MS01** Classifier | MS02 Analyzer | UC5, UC1 |
| SP08 | Quality Checker | Controllo qualità testo, grammatica, coerenza | **MS04** Validator | MS02 Analyzer | UC5 |
| SP09 | Workflow Engine | Orchestrazione workflow generazione atti, approvazioni | **MS08** Workflow | MS03 Orchestrator | UC5 |
| SP10 | Dashboard | Dashboard esplicabilità, monitoring, analytics | **MS12** User Interface | MS10 Analytics | UC5, UC1 |
| SP11 | Security & Audit | Security audit, logging completo, tracciabilità | **MS13** Security | MS14 Audit | UC5 |

### UC6: Firma Digitale Integrata (4 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP29 | Digital Signature Engine | Esecuzione firme digitali, validazione certificati, gestione provider firma | **MS13** Security | MS04 Validator | UC6 |
| SP30 | Certificate Manager | Gestione certificati digitali, lifecycle, validazione catena certificati | **MS13** Security | MS04 Validator | UC6 |
| SP31 | Signature Workflow | Orchestrazione processi firma multi-firmatari, deleghe, scadenze, escalation, notifiche | **MS03** Orchestrator | MS06 Knowledge Base | UC6 |
| SP32 | Timestamp Authority & Temporal Marking | RFC 3161 timestamp generation, marcature temporali, TSA integration, validazione timestamp | **MS13** Security | MS04 Validator, MS14 Audit | UC6 |

### UC7: Conservazione Digitale (5 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP33 | Archive Manager | Gestione pacchetti versamento (SIP), orchestrazione conservazione | **MS01** Classifier | MS07 ETL | UC7 |
| SP34 | Preservation Engine | Predizione rischi leggibilità, formati obsoleti, decay analysis, preservazione digitale | **MS02** Analyzer | MS10 Analytics | UC7 |
| SP35 | Integrity Validator | Controllo integrità pacchetti, validazione hash, verifica completezza | **MS04** Validator | MS05 Storage | UC7 |
| SP36 | Storage Optimizer | Gestione storage conservazione, replica, backup, ottimizzazione | **MS05** Storage | MS14 Audit | UC7 |
| SP37 | Archive Metadata Manager | Gestione metadati, indicizzazione, ricerca, fascicolazione | **MS06** Knowledge Base | MS04 Validator, MS14 Audit | UC7 |

### UC8: Integrazione con SIEM (4 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP38 | SIEM Collector | Log aggregation, event ingestion, source integration | **MS02** Analyzer | MS13 Security | UC8 |
| SP39 | SIEM Processor | Event processing, correlation, normalization | **MS02** Analyzer | MS10 Analytics | UC8 |
| SP40 | SIEM Storage | Event storage, indexing, retention management | **MS09** Notification | MS13 Security | UC8 |
| SP41 | SIEM Analytics & Reporting | Security analytics, reporting, dashboards, forensics | **MS16** Monitoring | MS14 Audit | UC8 |

### UC9: Compliance & Risk Management (9 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP42 | Policy Engine | Motore centrale per la gestione, enforcement e monitoraggio delle policy normative | **MS06** Knowledge Base | MS03 Orchestrator | UC9 |
| SP43 | Risk Assessment Engine | Motore intelligente per la valutazione, quantificazione e monitoraggio dei rischi aziendali | **MS02** Analyzer | MS10 Analytics | UC9 |
| SP44 | Compliance Monitoring System | Sistema centrale per il monitoraggio continuo della conformità normativa | **MS04** Validator | MS14 Audit | UC9 |
| SP45 | Regulatory Intelligence Hub | Centro nevralgico per l'intelligence normativa e distribuzione informazioni regolamentari | **MS06** Knowledge Base | MS02 Analyzer | UC9 |
| SP46 | Compliance Automation Platform | Piattaforma centrale per l'automazione completa dei processi di compliance | **MS03** Orchestrator | MS10 Analytics | UC9 |
| SP47 | Compliance Analytics & Reporting | Sistema centrale per l'analisi avanzata dei dati compliance e reporting | **MS10** Analytics | MS12 User Interface | UC9 |
| SP48 | Compliance Intelligence Platform | Piattaforma centrale per l'intelligence compliance avanzata con AI e machine learning | **MS02** Analyzer | MS10 Analytics | UC9 |
| SP49 | Regulatory Change Management | Sistema centrale per la gestione intelligente dei cambiamenti regolamentari | **MS06** Knowledge Base | MS02 Analyzer | UC9 |
| SP50 | Compliance Training | Training compliance, awareness, certificazioni, assessment | **MS12** User Interface | MS06 Knowledge Base | UC9 |

### UC10: Supporto all'Utente (7 SP)

| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP51 | Help Desk System | Sistema helpdesk, ticketing, knowledge base | **MS09** Notification | MS06 Knowledge Base | UC10 |
| SP52 | Knowledge Base Management | Gestione KB per support, indexing, search | **MS06** Knowledge Base | MS10 Analytics | UC10 |
| SP53 | Virtual Assistant & Chatbot | Assistente conversazionale, Q&A contestuale | **MS02** Analyzer | MS06 Knowledge Base | UC10 |
| SP54 | User Training Platform | Platform training, guide, tutorial interattivi | **MS12** User Interface | MS06 Knowledge Base | UC10 |
| SP55 | Self-Service Portal | Portal self-service, FAQ, guide risorse | **MS12** User Interface | MS06 Knowledge Base | UC10 |
| SP56 | Support Analytics & Reporting | Analytics support tickets, trend, satisfazione utenti | **MS10** Analytics | MS12 User Interface | UC10 |
| SP57 | User Feedback Management | Gestione feedback utenti, surveys, insights | **MS10** Analytics | MS02 Analyzer | UC10 |

### UC11: Analisi Dati e Reporting (15 SP)

#### 11.A Analytics Core (7 SP)
| SP | Nome | Responsabilità | MS Primario | MS Supporto | UC riferimento |
|---|---|---|---|---|---|
| SP58 | Data Lake & Storage Management | Gestione data lake, storage ottimizzato, datalake governance | **MS05** Storage | MS07 ETL | UC11 |
| SP59 | ETL & Data Processing Pipelines | Pipeline ETL, data transformation, quality checks | **MS07** ETL | MS05 Storage | UC11 |
| SP60 | Advanced Analytics & ML | ML pipelines, predictive models, forecasting | **MS10** Analytics | MS02 Analyzer | UC11 |
| SP61 | Self-Service Analytics Portal | Portal BI self-service, dashboards, drill-down | **MS12** User Interface | MS10 Analytics | UC11 |
| SP62 | Data Quality & Governance | Data governance, quality metrics, DQ dashboard | **MS04** Validator | MS10 Analytics | UC11 |
| SP63 | Real-Time Analytics & Streaming | Analytics real-time, streaming data, event processing | **MS10** Analytics | MS07 ETL | UC11 |
| SP64 | Predictive Analytics & Forecasting | Forecasting, trend prediction, scenario analysis | **MS10** Analytics | MS02 Analyzer | UC11 |

#### 11.B Infrastrutture Cross-Cutting (8 SP)
| SP | Nome | Responsabilità | MS Primario | MS Supporto | **Natura** | UC riferimento |
|---|---|---|---|---|---|---|
| SP65 | Performance Monitoring & Alerting | Monitoring, observability, alerting, SLA | **MS16** Monitoring | MS10 Analytics | **Cross-Cutting** | UC11 |
| SP66 | Data Security & Compliance | Security, encryption, access control, compliance | **MS13** Security | MS14 Audit | **Cross-Cutting** | UC11 |
| SP67 | API Gateway & Integration Layer | API gateway, service mesh, integration patterns | **MS11** Integration Hub | MS15 Configuration | **Infra** | UC11 |
| SP68 | DevOps & CI/CD Pipeline | CI/CD automation, deployment, infrastructure-as-code | **MS15** Configuration | MS16 Monitoring | **Infra** | UC11 |
| SP69 | Disaster Recovery & Business Continuity | DR planning, backup, failover, recovery procedures | **MS13** Security | MS16 Monitoring | **Infra** | UC11 |
| SP70 | Compliance & Audit Management | Compliance management, audit trails, SLA monitoring | **MS14** Audit | MS13 Security | **Cross-Cutting** | UC11 |
| SP71 | Performance Optimization & Scaling | Scaling strategy, performance tuning, capacity planning | **MS16** Monitoring | MS15 Configuration | **Infra** | UC11 |
| SP72 | Incident Management & Escalation | Incident handling, escalation, post-mortem | **MS14** Audit | MS16 Monitoring | **Infra** | UC11 |

---

## 2. MAPPING INVERSO: MS → SP (Come ogni MS supporta gli SP)

| MS | Nome | Principali SP supportati | Multi-UC | Natura |
|---|---|---|---|---|
| **MS01** | Generic Classifier Engine | SP02, SP03, SP07, SP16, SP17, SP33 | UC1, UC2, UC5, UC7 | Core AI |
| **MS02** | Generic Analyzer Engine | SP12, SP13, SP18, SP22, SP24, SP27, SP34, SP38, SP39, SP43, SP44, SP53, SP60, SP64 | UC1-5, UC8-11 | Core AI |
| **MS03** | Generic Orchestrator Engine | SP15, SP19, SP26, SP48, SP09 | UC1-5 | Platform |
| **MS04** | Generic Validator Engine | SP06, SP08, SP23, SP31, SP35, SP42, SP45, SP62 | UC5-7, UC9, UC11 | Core AI |
| **MS05** | Generic Storage Manager | SP02, SP05, SP14, SP36, SP58 | UC1-2, UC5, UC7, UC11 | Infrastructure |
| **MS06** | Generic Knowledge Base | SP04, SP12-13, SP17, SP20, SP21, SP22, SP37, SP45, SP48, SP49, SP50, SP52, SP55, SP56, SP57 | UC1-5, UC7, UC9-10 | Platform |
| **MS07** | Generic ETL Pipeline | SP01, SP07, SP33, SP39, SP59, SP63 | UC2, UC5, UC7, UC11 | Infrastructure |
| **MS08** | Generic Workflow Engine | SP05, SP09, SP19, SP21, SP26 | UC2-5 | Platform |
| **MS09** | Generic Notification Engine | SP40, SP51 | UC2, UC8, UC10 | Platform |
| **MS10** | Generic Analytics & Reporting | SP12, SP14, SP24, SP27, SP34, SP39, SP43, SP44, SP46, SP56, SP60, SP61, SP62, SP63, SP64, SP65 | UC1, UC4, UC8-11 | Core Analytics |
| **MS11** | Generic Integration Hub | SP67 | UC11 | Infrastructure |
| **MS12** | Generic User Interface | SP10, SP46, SP50, SP51, SP54, SP61, SP65 | UC1, UC5, UC9-11 | Platform |
| **MS13** | Generic Security Engine | SP11, SP29, SP30, SP31, SP40, SP66, SP69 | UC5-6, UC8-9, UC11 | Cross-Cutting |
| **MS14** | Generic Audit Engine | SP11, SP18, SP23, SP32, SP37, SP41, SP47, SP70, SP72 | UC2, UC5-6, UC8-9, UC11 | Cross-Cutting |
| **MS15** | Generic Configuration Engine | SP68, SP71 | UC11 | Infrastructure |
| **MS16** | Generic Monitoring Engine | SP41, SP65, SP68, SP71, SP72 | UC8, UC11 | Cross-Cutting |

---

## 3. IDENTIFICAZIONE GAP NUMERICI - RISOLTO

### SP Documentati: 72 ✅
### SP Attesi: 72 ✅
### Gap Risolti:

| Gap | Numero | Posizione Logica | Soluzione | Status |
|---|---|---|---|---|
| **SP25** | UC4 (BPM) | Forecasting & Predictive Scheduling Engine | ✅ CREATO e documentato | RISOLTO |
| **SP28** | UC4 (BPM) | Intenzionalmente skipped (reserved for future expansion) | ⚠️ SKIPPED | INTENZIONALE |
| **SP31** | UC6 (Firma) | Timestamp Authority & Temporal Marking Manager (RFC 3161 compliant) | ✅ CREATO e documentato | RISOLTO |
| **SP32** | UC6 (Firma) | Post-Signature Auditor | ✅ CREATO e documentato | RISOLTO |
| **SP37** | UC7 (Archive) | Archive Metadata Manager | ✅ CREATO e documentato | RISOLTO |
| **SP50** | UC9 (Compliance) | Compliance Training & Certification Platform | ✅ CREATO e documentato | RISOLTO |
| **SP70** | UC11 (Infrastructure) | Incident Management & Escalation System | ✅ CREATO e documentato | RISOLTO |

### Cross-UC SP (Intenzionali):
- **SP48-SP50**: Shared tra UC9 (Compliance & Risk) e UC10 (User Support) - Policy Management, Risk Registry, Training shared across UC
- **UC11 SP65-SP72**: Classificati come "Infrastrutture Cross-Cutting" - enablers per TUTTI gli UC, non solo UC11-specific

---

## 4. COERENZA CONTROL: UC vs SP vs MS

### Verifiche di Coerenza Necessarie

#### UC1 (Document Management)
- ✓ SP02 referenziato: OK in 01 SP02
- ✓ SP07 referenziato: OK in 01 SP07
- ✓ SP12, SP13, SP14, SP15 referenziati: OK
- ✓ MS01, MS02, MS05, MS06, MS10, MS11, MS13 mapping: ALLINEATO

#### UC2 (Protocol)
- ✓ SP16, SP17, SP18, SP19 documentati: OK
- ⚠ SP01 non documentato in UC2 folder (dovrebbe avere doc UC2-specific)
- ✓ MS01, MS02, MS03, MS04, MS07, MS14, MS16 mapping: ALLINEATO

#### UC3 (Governance)
- ✓ SP20-23 documentati: OK
- ✓ MS03, MS04, MS06, MS08, MS14 mapping: ALLINEATO

#### UC4 (BPM)
- ✓ SP24, SP26, SP27 documentati
- ❌ **SP25 MISSING**: Gap nella numerazione
- ⚠ Matrice dipendenze documenta anche SP02, SP07 (inherited?), CONFUSIONE

#### UC5 (Integrated Document Production)
- ✓ SP01-11 documentati
- ✓ MS01-08, MS12-13 mapping: ALLINEATO
- ⚠ 2 architetture diverse: "00 REFACTORING - Nuova Architettura con EML" vs "00 Architettura Generale Microservizi"

#### UC6 (Digital Signature)
- ✓ SP30, SP31, SP33 documentati
- ❌ **SP33 MISSING**: Gap nella numerazione (dovrebbe essere Timestamp/TSA?)
- ✓ MS04, MS13, MS14, MS15 mapping: ALLINEATO (ma SP33 manca)

#### UC7-UC11
- ✓ SP34-SP72 documentati
- ⚠ **UC11 SP65-SP72**: Cross-cutting infra, non UC11-specifiche
  - SP67 (DevOps), SP68 (DR), SP70 (Scaling) sono operational, non analytics
  - Dovrebbero essere riclassificate o esplicitare dipendenza da tutti UC

---

## 5. RACCOMANDAZIONI ALLINEAMENTO

### Priority 1: Risolvere Ambiguità Architetturali

1. **UC2 Inherit: SP01 from UC5?**
   - UC2 matrice dipendenze referenzia SP01 ma non esiste doc UC2-specifica
   - Confermare: SP01 è riusato da UC2 oppure dovrebbe avere specializzazione?

2. **UC4 SP25 Gap**
   - Documentare perché manca
   - Se intenzionale → documentare in "gaps resolution"
   - Se dimenticato → creare SP25 Forecasting Engine o Scheduler

3. **UC6 SP33 Gap**
   - Probabilmente Timestamp Authority Manager
   - Necessario per validazione temporale firme digitali
   - Creare SP33 Timestamp & TSA Manager

4. **UC10 vs UC11: SP57**
   - SP57 "User Feedback Management" documentato sia UC10 che UC11?
   - Consolidare in una sola posizione

### Priority 2: Normalizzare Architetture

1. **UC1, UC5**: Hanno 2 diverse "00 Architettura"
   - UC5 ha sia "00 REFACTORING" che "00 Architettura Generale Microservizi"
   - Decidere quale è canonical e deprecare l'altra

2. **UC4, UC2**: Matrice dipendenze referenzia SP da altri UC (SP02, SP07)
   - Chiarire se sono inherited/shared o duplicated

### Priority 3: Riclassificare UC11 Infrastrutture

Opzioni:

**Opzione A: Mantieni UC11 come è** (attuale)
- Pro: Packaging implementativo "Analytics + Infra"
- Con: Semanticamente confuse (analytics ≠ infra)

**Opzione B: Crea sezione "Infrastructure & Operations"**
- Sposta SP65-SP72 fuori UC11
- UC11 diventa "Analytics & Reporting" puro
- Infra diventa cross-cutting a tutti UC

**Opzione C: Mantieni ma esplicita dipendenza**
- Documenta che UC11 SP65-SP72 sono "enablers" per TUTTI gli UC
- Chiaramente separati da SP58-64 (analytics genuine)

---

## 6. TEMPLATE COERENZA PER DOCUMENTAZIONE

Ogni SP deve:
```yaml
Nome: SP## - [Nome componente]
UC: [UC number]
MS Primario: MS##
MS Supporto: [MS##, MS##]
Responsabilità: [Clear bullet points]
Input: [Data types/format]
Output: [Data types/format]
Dipendenze: [SP## → SP##]
Natura: [Core AI | Platform | Infrastructure | Cross-Cutting]
```

Ogni UC deve:
```yaml
Numero: UC#
Nome: [Nome caso d'uso]
Descrizione: [Business value]
SP Inclusi: [SP##, SP##, ...]
MS Utilizzati: [MS##, MS##, ...]
Dipendenze UC: [UC# → UC#]
Tipo: [Business | Operational | Infrastructure]
```

---

## Gestione Errori

### Scenari di Errore Comuni

1. **Timeout Query**
   - Descrizione: Query supera tempo limite di esecuzione
   - Causa: Query complessa o dati voluminosi
   - Mitigation: Implementare timeout configurabile e fallback

2. **Connessione Database**
   - Descrizione: Perdita connessione ai servizi dipendenti
   - Causa: Servizio non disponibile o problemi rete
   - Mitigation: Retry logic con exponential backoff

3. **Validazione Dati**
   - Descrizione: Input non valido o formato errato
   - Causa: Client fornisce dati non conformi
   - Mitigation: Validazione input e error messages chiari

### Error Codes

| Code | Status | Descrizione | Azione |
|------|--------|-------------|--------|
| 400 | Bad Request | Input non valido | Correggi parametri request |
| 408 | Timeout | Operazione timeout | Riprova con parametri ridotti |
| 500 | Internal Error | Errore interno | Contatta supporto |
| 503 | Service Unavailable | Servizio non disponibile | Riprova più tardi |

### Recovery Procedures

- **Automatic Retry**: Sistema riprova automaticamente con backoff esponenziale
- **Graceful Degradation**: Fallback a cache o risultati parziali se disponibili
- **Error Logging**: Tutti gli errori registrati per analisi e monitoring
- **Alerting**: Notifiche su errori critici ai team di supporto

## 7. SUMMARY ALLINEAMENTO

- **70 SP in piano** ✓
- **16 MS identificati** ✓
- **Mapping SP→MS completo** ✓
- **Gaps SP25, SP33 da risolvere** ❌
- **UC11 Infrastrutture da classificare** ⚠
- **Architetture UC5 da normalizzare** ⚠
- **Matrici dipendenze UC2,4,6 incomplete** ⚠

