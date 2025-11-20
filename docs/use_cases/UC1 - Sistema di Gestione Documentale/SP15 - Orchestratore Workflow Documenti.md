# SP15 - Document Workflow Orchestrator

## Panoramica

**SP15 - Document Workflow Orchestrator** è il componente che coordina l'intero flusso di processamento dei documenti nel Sistema di Gestione Documentale. Gestisce l'orchestrazione delle pipeline, il routing intelligente, il monitoraggio dello stato e l'integrazione con sistemi esterni.

```mermaid
graph LR
    Input[Document<br/>Upload] --> SP15[SP15<br/>Orchestrator]
    SP15 --> SP02[SP02<br/>Extractor]
    SP15 --> SP07[SP07<br/>Classifier]
    SP15 --> SP12[SP12<br/>Search]
    SP15 --> SP13[SP13<br/>Summarizer]
    SP15 --> SP14[SP14<br/>Indexer]
    SP15 --> SP10[SP10<br/>Dashboard]
    SP15 --> SP11[SP11<br/>Security]

    SP15 -.-> NIFI[Apache NiFi<br/>Flow Mgmt]
    SP15 -.-> AIRFLOW[Airflow<br/>Scheduling]
    SP15 -.-> KAFKA[Kafka<br/>Events]
    SP15 -.-> REDIS[Redis<br/>State]

    style SP15 fill:#ffd700
```

## Responsabilità

### Core Functions

1. **Workflow Management**
   - Definizione pipeline processamento
   - Esecuzione sequenziale/asincrona
   - Gestione dipendenze componenti

2. **State Management**
   - Tracking stato documenti
   - Persistenza workflow
   - Recovery da failure

3. **Event Processing**
   - Streaming eventi documento
   - Trigger azioni automatiche
   - Notifiche real-time

4. **Integration Hub**
   - Connessione con sistemi esterni
   - API gateway per componenti
   - Data flow orchestration
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

## 🏛️ Conformità Normativa - SP15

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP15 (Document Workflow)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC1

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP15 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP15 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Responsabile della Protezione dei Dati (DPO))

---

### 6. Monitoraggio Conformità

**Schedule di Review**:
- **Trimestrale**: Compliance assessment + security audit
- **Semestrale**: Framework alignment review (CAD/GDPR/eIDAS/AGID)
- **Annuale**: Full compliance audit + risk assessment

**KPI Conformità**:
- Audit trail completeness: 100%
- Incident response time: <24h
- Compliance violations: 0 per quarter
- Certificate expiry (if eIDAS): Alert at 30 days

**Escalation**: Non-conformità → Compliance Manager → CTO → Legal

**Prossima review programmata**: 2026-02-17

---

## Riepilogo Conformità SP15

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsabile |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ✅ Sì | ✅ Compliant | DPO |
| eIDAS | ❌ No | N/A | - |
| AGID | ❌ No | N/A | - |

**Key Compliance Points**:
1. All CAD articles implemented
2. Data handling compliant with applicable regulations
3. Security controls in place (encryption, access control, audit logging)
4. Regular monitoring and review schedule established
5. Clear responsibility assignments (RACI)

**Prossima Review**: 2026-02-17

---



### Framework Normativi Applicabili

☑ CAD
☑ GDPR
☐ L. 241/1990 - Procedimento Amministrativo
☐ eIDAS - Regolamento 2014/910
☐ AI Act - Regolamento 2024/1689
☐ D.Lgs 42/2004 - Codice Beni Culturali
☐ D.Lgs 152/2006 - Codice dell'Ambiente
☐ D.Lgs 33/2013 - Decreto Trasparenza

**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
| CAD | Art. 1, Art. 21, Art. 22, Art. 62 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| GDPR | Art. 5, Art. 32 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP15

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP15 (Document Workflow)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC1

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP15 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP15 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Responsabile della Protezione dei Dati (DPO))

---

### 6. Monitoraggio Conformità

**Schedule di Review**:
- **Trimestrale**: Compliance assessment + security audit
- **Semestrale**: Framework alignment review (CAD/GDPR/eIDAS/AGID)
- **Annuale**: Full compliance audit + risk assessment

**KPI Conformità**:
- Audit trail completeness: 100%
- Incident response time: <24h
- Compliance violations: 0 per quarter
- Certificate expiry (if eIDAS): Alert at 30 days

**Escalation**: Non-conformità → Compliance Manager → CTO → Legal

**Prossima review programmata**: 2026-02-17

---

## Riepilogo Conformità SP15

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsabile |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ✅ Sì | ✅ Compliant | DPO |
| eIDAS | ❌ No | N/A | - |
| AGID | ❌ No | N/A | - |

**Key Compliance Points**:
1. All CAD articles implemented
2. Data handling compliant with applicable regulations
3. Security controls in place (encryption, access control, audit logging)
4. Regular monitoring and review schedule established
5. Clear responsibility assignments (RACI)

**Prossima Review**: 2026-02-17

---



---


## Architettura Tecnica

### Workflow Engine

```mermaid
graph TD
    A[Document Received] --> B{Document Type?}
    B -->|PDF| C[OCR Pipeline]
    B -->|DOC| D[Text Pipeline]
    B -->|Image| E[Image Pipeline]

    C --> F[SP02 Extract]
    D --> F
    E --> F

    F --> G[SP07 Classify]
    G --> H{Classification OK?}
    H -->|Yes| I[SP13 Summarize]
    H -->|No| J[Manual Review]

    I --> K[SP14 Index]
    K --> L[SP12 Search Ready]
    L --> M[Complete]

    J --> N[Human Intervention]
    N --> O[Retry Pipeline]

    style SP15 fill:#ffd700
```

### Tecnologie Utilizzate

| Componente | Tecnologia | Versione | Scopo |
|------------|------------|----------|--------|
| Flow Engine | Apache NiFi | 1.24 | Data flow orchestration |
| Scheduler | Apache Airflow | 2.8 | Workflow scheduling |
| Message Bus | Apache Kafka | 3.6 | Event streaming |
| State Store | Redis | 7.2 | Workflow state |
| API Gateway | Kong | 3.5 | API management |
| Monitoring | Prometheus | 2.47 | Metrics collection |

### Workflow Templates

#### Pipeline Base Documento

```yaml
name: document_processing_pipeline
steps:
  - name: extract
    component: SP02
    input: document_file
    output: extracted_text
    timeout: 30s
    retry: 3

  - name: classify
    component: SP07
    input: extracted_text
    output: classification
    depends_on: extract
    timeout: 10s

  - name: summarize
    component: SP13
    input: [extracted_text, classification]
    output: summary
    depends_on: classify
    timeout: 60s

  - name: index
    component: SP14
    input: [extracted_text, classification, summary]
    output: indexed_document
    depends_on: summarize
    timeout: 15s
```

### API Endpoints

```yaml
POST /api/v1/workflows/start
  - Input: {"document_id": "string", "pipeline": "string"}
  - Output: {"workflow_id": "string", "status": "started"}

GET /api/v1/workflows/{id}/status
  - Output: Current workflow status and progress

POST /api/v1/workflows/{id}/pause
  - Output: Pause confirmation

POST /api/v1/workflows/{id}/resume
  - Output: Resume confirmation

GET /api/v1/workflows/metrics
  - Output: Workflow performance metrics
```

### Configurazione

```yaml
sp15:
  nifi:
    url: 'http://nifi:8080'
    registry: 'http://nifi-registry:18080'
  airflow:
    dag_folder: '/opt/airflow/dags'
    default_timeout: '1h'
  kafka:
    brokers: ['kafka:9092']
    topics:
      document_events: 'document-events'
      workflow_events: 'workflow-events'
  redis:
    host: 'redis:6379'
    db: 1
    key_prefix: 'workflow:'
```

### Performance Metrics

- **Throughput**: 100 documenti/minuto
- **Latency Media**: 45s per pipeline completa
- **Success Rate**: >95%
- **Scalability**: Auto-scaling basato load
- **Reliability**: 99.9% uptime

### Sicurezza

- **Authentication**: JWT per API access
- **Authorization**: RBAC per workflow operations
- **Crittografia**: TLS per comunicazioni
- **Audit**: Log completo operazioni

### Evoluzione

1. **Event-driven**: Reattività eventi real-time
2. **AI Optimization**: Routing intelligente workflow
3. **Multi-cloud**: Orchestrazione ibrida
4. **Low-code**: Designer workflow visuale</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC1 - Sistema di Gestione Documentale/01 SP15 - Document Workflow Orchestrator.md
