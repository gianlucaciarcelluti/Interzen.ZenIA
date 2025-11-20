# SP18 - Anomaly Detector

## Panoramica

**SP18 - Anomaly Detector** è il componente responsabile dell'identificazione di anomalie e irregolarità nel flusso di protocollo, utilizzando tecniche di machine learning per rilevare comportamenti anomali.

```mermaid
graph LR
    SP16[SP16<br/>Classifier] -->|classification| SP18[SP18<br/>Anomaly Detector]
    SP17[SP17<br/>Suggester] -->|suggestion| SP18
    SP18 -->|anomaly| SP19[SP19<br/>Workflow Orchestrator]
    SP18 -->|alert| SP10[SP10<br/>Dashboard]

    SP18 -.-> ML[ML<br/>Models]
    SP18 -.-> RULES[Rule<br/>Engine]
    SP18 -.-> LOGS[(Protocol<br/>Logs)]
    SP18 -.-> ALERT[Alert<br/>System]

    style SP18 fill:#ffd700
```

## Responsabilità

### Core Functions

1. **Pattern Analysis**
   - Analisi sequenziale protocolli
   - Rilevamento duplicati
   - Controllo coerenza dati

2. **Anomaly Detection**
   - Protocolli fuori orario
   - Volumi anomali
   - Sequenze irregolari

3. **Fraud Detection**
   - Manipolazione numeri protocollo
   - Accessi non autorizzati
   - Modifiche sospette

4. **Alert Generation**
   - Notifiche real-time
   - Escalation automatica
   - Report periodici
## 🏛️ Conformità Normativa - SP18

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP18 (Rilevatore Anomalie)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC2

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP18 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP18 - gestisce dati personali

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

## Riepilogo Conformità SP18

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

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP18

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP18 (Rilevatore Anomalie)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC2

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP18 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP18 - gestisce dati personali

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

## Riepilogo Conformità SP18

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

### Detection Pipeline

```mermaid
graph TD
    A[Protocol Data] --> B[Feature Extraction]
    B --> C[Statistical Analysis]
    C --> D[ML Prediction]
    D --> E[Rule Validation]
    E --> F[Alert Generation]

    style SP18 fill:#ffd700
```

### Tecnologie Utilizzate

| Componente | Tecnologia | Versione | Scopo |
|------------|------------|----------|--------|
| ML Framework | Scikit-learn | 1.3 | Modelli anomalie |
| Time Series | Prophet | 1.1 | Analisi temporale |
| Streaming | Kafka Streams | 3.6 | Elaborazione real-time |
| Alert System | Prometheus Alertmanager | 0.26 | Gestione notifiche |

### Tipi di Anomalie

#### Protocollo Duplicato
```
Pattern: Stesso mittente, oggetto, data entro 24h
Threshold: Similarità > 0.85
Action: Flag per verifica manuale
```

#### Volume Anomale
```
Pattern: Protocolli/ora > 3σ dalla media
Threshold: Z-score > 3.0
Action: Alert supervisore
```

### API Endpoints

```yaml
POST /api/v1/detect/anomalies
  - Input: {"protocol_data": {}, "time_window": "1h"}
  - Output: {"anomalies": [], "severity": "string"}

GET /api/v1/anomalies/history
  - Query: ?from=2024-01-01&to=2024-01-31
  - Output: {"anomalies": [], "stats": {}}
```

### Configurazione

```yaml
sp18:
  detection_window: '24h'
  alert_threshold: 0.8
  ml_model: 'anomaly_detector.pkl'
  kafka_topic: 'protocol.events'
```

### Performance Metrics

- **Detection Rate**: >95% anomalie catturate
- **False Positive Rate**: <5%
- **Latency**: <500ms per analisi
- **Throughput**: 1000 protocolli/minuto

### Sicurezza

- **Data Isolation**: Separazione dati sensibili
- **Access Logging**: Audit completo accessi
- **Crittografia**: Crittografia dati in transito

### Evoluzione

1. **Advanced ML**: Deep learning per pattern complessi
2. **Behavioral Analysis**: Profili utente dinamici
3. **Integration**: Con sistemi antifrode esterni</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC2 - Protocollo Informatico/01 SP18 - Anomaly Detector.md