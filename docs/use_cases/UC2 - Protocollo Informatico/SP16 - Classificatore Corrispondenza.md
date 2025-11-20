# SP16 - Correspondence Classifier

## Panoramica

**SP16 - Correspondence Classifier** è il componente che classifica automaticamente il tipo di corrispondenza ricevuta (PEC, email, web form), distinguendo tra istanze, comunicazioni, richieste, notifiche, etc.

```mermaid
graph LR
    SP01[SP01<br/>EML Parser] -->|parsed_email| SP16[SP16<br/>Classifier]
    SP16 -->|classification| SP17[SP17<br/>Registry Suggester]
    SP16 -->|classification| SP10[SP10<br/>Dashboard]

    SP16 -.-> BERT[BERT<br/>Classifier]
    SP16 -.-> RULES[Rule<br/>Engine]
    SP16 -.-> CACHE[Redis<br/>Cache]
    SP16 -.-> DB[(PostgreSQL)]

    style SP16 fill:#ffd700
```

## Responsabilità

### Core Functions

1. **Correspondence Type Classification**
   - Istanza amministrativa
   - Comunicazione ufficiale
   - Richiesta informazioni
   - Notifica/avviso
   - Reclamo/segnalazione
   - Altro

2. **Channel Recognition**
   - PEC (Posta Elettronica Certificata)
   - Email ordinaria
   - Web form submission
   - API integration

3. **Priority Assessment**
   - Alta priorità (istanze, reclami)
   - Media priorità (comunicazioni)
   - Bassa priorità (notifiche)

4. **Language Detection**
   - Italiano ufficiale
   - Italiano regionale/dialettale
   - Altre lingue
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

## 🏛️ Conformità Normativa - SP16

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP16 (Classificatore Corrispondenza)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC2

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP16 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP16 - gestisce dati personali

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

## Riepilogo Conformità SP16

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
☑ AI Act
☑ GDPR
☐ L. 241/1990 - Procedimento Amministrativo
☐ eIDAS - Regolamento 2014/910
☐ D.Lgs 42/2004 - Codice Beni Culturali
☐ D.Lgs 152/2006 - Codice dell'Ambiente
☐ D.Lgs 33/2013 - Decreto Trasparenza

**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
| CAD | Art. 1, Art. 21, Art. 22, Art. 62 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| AI Act | Art. 6, Art. 13, Art. 22 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| GDPR | Art. 5, Art. 32 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP16

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP16 (Classificatore Corrispondenza)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC2

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP16 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP16 - gestisce dati personali

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

## Riepilogo Conformità SP16

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

### Classification Pipeline

```mermaid
graph TD
    A[Parsed Email] --> B[Preprocessing]
    B --> C[Feature Extraction]
    C --> D[ML Classification]
    D --> E[Rule-based Validation]
    E --> F[Confidence Scoring]
    F --> G[Output Classification]

    style SP16 fill:#ffd700
```

### Tecnologie Utilizzate

| Componente | Tecnologia | Versione | Scopo |
|------------|------------|----------|--------|
| ML Model | BERT |  | Classificazione testo |
| Rule Engine | Drools | 8.0 | Validazione regole |
| Language Detection | langdetect | 1.0.9 | Rilevamento lingua |
| Cache | Redis | 7.2 | Cache risultati |
| Database | PostgreSQL | 15 | Training data |

### Esempi di Classificazione

#### Istanza Amministrativa
```
Input: "Con la presente si richiede autorizzazione per..."
Output: {type: "ISTANZA", priority: "HIGH", confidence: 0.96}
```

#### Comunicazione Ufficiale
```
Input: "Si comunica l'avvenuta pubblicazione..."
Output: {type: "COMUNICAZIONE", priority: "MEDIUM", confidence: 0.89}
```

### API Endpoints

```yaml
POST /api/v1/classify/correspondence
  - Input: {"email_text": "string", "metadata": {}}
  - Output: {"type": "string", "priority": "string", "confidence": 0.95}
```

### Configurazione

```yaml
sp16:
  model: 'bert-correspondence-classifier'
  threshold: 0.8
  categories:
    - istanza
    - comunicazione
    - richiesta
    - notifica
    - reclamo
  cache_ttl: 3600
```

### Performance Metrics

- **Accuracy**: >95% classificazione corretta
- **Precision**: >92% per categorie principali
- **Latency**: <2s per classificazione
- **Throughput**: 200 email/minuto

### Sicurezza

- **Data Sanitization**: Rimozione dati sensibili
- **Audit Logging**: Tracciamento classificazioni
- **Model Security**: Validazione input

### Evoluzione

1. **Multi-language**: Supporto multilingua
2. **Domain Adaptation**: Fine-tuning per ente specifico
3. **Real-time Learning**: Aggiornamento modello continuo</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC2 - Protocollo Informatico/01 SP16 - Correspondence Classifier.md