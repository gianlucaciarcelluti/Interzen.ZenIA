# SP01 - EML Parser & Email Intelligence (UC2 - Protocollo Informatico Variant)

## Descrizione Componente (UC2 Variant)

Lo **SP01 EML Parser & Email Intelligence** per UC2 Protocollo Informatico è la componente specializzata per l'estrazione intelligente di informazioni da messaggi di posta elettronica (PEC, email standard) ai fini della protocollazione e della gestione del flusso documentale di corrispondenza.

Questa è una **variante UC2-specifica** del componente generale SP01 documentato in UC5. Si focalizza specificamente su:
- Estrazione dati per protocollazione automatica
- Riconoscimento mittenti/destinatari secondo standard PA
- Integrazione con sistemi di registro protocollo
- Conformità normative per protocollo informatico

## Relazione con UC5

**Canonical documentation**: [UC5 SP01 - EML Parser & Email Intelligence](../UC5 - Produzione Documentale Integrata/01 SP01 - EML Parser & Email Intelligence.md)

Questo documento è una **specializzazione UC2** che enfatizza gli aspetti specifici per protocollo informatico.

## Responsabilità (UC2 Specific)

### Core Functions

1. **Email Extraction for Protocol**
   - Parsing RFC 5321/5322 compliant emails (SMTP)
   - PEC (Posta Elettronica Certificata) validation e processing
   - Metadata extraction: From, To, CC, BCC, Subject, Date, Message-ID
   - Attachment inventory e cataloging
   - Digital signature validation (per allegati firmati)

2. **Protocol-Aware Parsing**
   - Riconoscimento automatico tipo corrispondenza (istanza, reclamo, comunicazione)
   - Estrazione dati anagrafici mittente per matching registro
   - Identificazione mittenti multipli (CC, BCC)
   - Tracciamento originale vs. inoltramenti
   - Metadata preservation per trail audit

3. **Integration with Protocol System**
   - Output structured per input diretti a SP16 (Correspondence Classifier)
   - Preparazione dati per protocollazione automatica
   - Compatibility con sistemi di registry/titolario (SP17)
   - Support per protocol assignment workflow (SP19)

4. **Security & Compliance**
   - PEC envelope validation (timestamp, signer validation)
   - DKIM/SPF/DMARC verification per email regolari
   - Malware scanning allegati
   - Encryption handling (S/MIME, PGP)

## Input/Output (UC2)

### Input
- **Email streams**: Da mailserver (POP3/IMAP) o PEC gateway
- **Archive imports**: Messaggi storici da archive
- **Configuration**: Regex per riconoscimento pattern specifici PA

### Output
- **Structured email data**: JSON con metadata
- **Protocol-ready metadata**: Set dati per registrazione automatica
- **Classification hints**: Suggestions per SP16 classifier
- **Audit trail**: Evento di ricezione + parsing timestamp

## Architettura Tecnica (UC2 Variant)

```
Email Input (POP3/IMAP/PEC)
  ↓
┌──────────────────────────────────┐
│  SP01 EML Parser (UC2 Protocol)  │
│                                  │
│  ┌────────────────────────────┐  │
│  │ PEC/Email Connector        │  │
│  │ - POP3 poller              │  │
│  │ - IMAP sync                │  │
│  │ - PEC gateway integration  │  │
│  └────────────────────────────┘  │
│               ↓                   │
│  ┌────────────────────────────┐  │
│  │ RFC Parser & Extractor     │  │
│  │ - RFC 5321/5322            │  │
│  │ - Metadata extraction      │  │
│  │ - Body parsing             │  │
│  │ - Attachment catalog       │  │
│  └────────────────────────────┘  │
│               ↓                   │
│  ┌────────────────────────────┐  │
│  │ Protocol Intelligence      │  │
│  │ - Correspondent matching   │  │
│  │ - Date/time extraction     │  │
│  │ - Subject normalization    │  │
│  │ - Classification hints     │  │
│  └────────────────────────────┘  │
│               ↓                   │
│  ┌────────────────────────────┐  │
│  │ Security Validator         │  │
│  │ - PEC envelope check       │  │
│  │ - Signature verification   │  │
│  │ - Malware scan             │  │
│  │ - Encryption handling      │  │
│  └────────────────────────────┘  │
└──────────────────────────────────┘
  ↓
Structured Protocol Data (JSON)
  ↓
  ├→ SP16 (Classifier)
  ├→ SP17 (Registry Suggester)
  ├→ SP19 (Workflow Orchestrator)
  └→ Audit Trail (SP11)
```

## API Endpoints (UC2)

**POST /api/v1/protocol/parse-email**

Request:
```json
{
  "email_source": "pec_gateway",
  "email_raw": "base64_encoded_eml",
  "expected_recipient": "ufficio.protocollo@pa.it"
}
```

Response:
```json
{
  "email_id": "msg_456",
  "from": {
    "name": "Rossi Mario",
    "email": "m.rossi@example.it",
    "type": "external"
  },
  "to": [
    {
      "email": "ufficio.protocollo@pa.it",
      "type": "internal"
    }
  ],
  "subject": "Istanza di accesso documenti",
  "received_date": "2025-11-17T10:30:00Z",
  "pec_timestamp": "2025-11-17T10:30:15Z",
  "pec_certified": true,
  "attachments": [
    {
      "filename": "documento.pdf",
      "mime_type": "application/pdf",
      "size_bytes": 15234,
      "hash_sha256": "abc123..."
    }
  ],
  "classification_hints": {
    "likely_type": "istanza",
    "confidence": 0.92
  },
  "protocol_ready": true,
  "audit_timestamp": "2025-11-17T10:30:20Z"
}
```

## Configurazione (YAML)

```yaml
sp01_uc2_protocol:
  email_sources:
    pec_gateway:
      connection: "imap://pec.provider.it:993"
      credentials: "${PEC_CREDENTIALS}"
      poll_interval_seconds: 60
      ssl: true

    standard_email:
      connection: "pop3://mail.pa.it:995"
      credentials: "${EMAIL_CREDENTIALS}"
      poll_interval_seconds: 300

  protocol_configuration:
    expected_recipients:
      - "ufficio.protocollo@pa.it"
      - "protocollo@example.pa.it"

    correspondent_database: "registry"

    classification_patterns:
      istanza:
        keywords: ["istanza", "richiesta", "domanda"]
        confidence_threshold: 0.85
      reclamo:
        keywords: ["reclamo", "lamentela", "contestazione"]
        confidence_threshold: 0.85

  security:
    pec_validation: true
    signature_verification: true
    malware_scan_enabled: true
    encryption_handling: "decrypt_and_log"

  audit:
    log_all_extractions: true
    immutable_trail: true
```

## Performance & KPIs

| Metrica | Target |
|---------|--------|
| **Email Parse Latency** | < 3 sec (normal), < 5 sec (with attachments) |
| **PEC Validation** | < 1 sec |
| **Attachment Processing** | < 10 sec (with virus scan) |
| **Extraction Accuracy** | > 99% (metadata), > 95% (classification hints) |
| **Throughput** | 500 emails/min |
| **Availability** | 99.9% |

## Integrazione UC2

**Upstream**:
- Email source (PEC/SMTP)

**Downstream**:
- **SP16** (Correspondence Classifier): Classificazione tipo corrispondenza
- **SP17** (Registry Suggester): Suggerimenti titolario/registro
- **SP18** (Anomaly Detector): Rilevamento duplicati/anomalie
- **SP19** (Protocol Workflow Orchestrator): Protocollazione automatica

**Data Flow UC2**:
```
Email (PEC/SMTP)
  ↓ SP01 (Parse)
  ├→ SP16 (Classify correspondence type)
  │   ├→ SP17 (Suggest registry entry)
  │   │   ↓
  │   └→ SP18 (Detect anomalies)
  │       ↓
  ├→ SP19 (Workflow orchestration)
  │   ├→ Auto-assign to responsible office
  │   ├→ Create protocol record
  │   └→ Route to SP09 (Document workflow)
  │
  └→ SP11 (Audit trail)
```

## Testing per UC2

- **Unit**: Email parsing, PEC validation, attachment extraction (> 85% coverage)
- **Integration**: Email → SP16 → SP17 → SP19 protocol workflow
- **E2E**: Complete email reception → protocol assignment
- **Load**: 500+ concurrent emails
- **Security**: PEC validation, signature verification, malware scanning

---
## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

☑ CAD
☐ L. 241/1990 - Procedimento Amministrativo
☐ GDPR - Regolamento 2016/679
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

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa" del template standard.

---


## Documentazione Correlata

- **Canonical**: [UC5 SP01 - EML Parser & Email Intelligence](../UC5 - Produzione Documentale Integrata/01 SP01 - EML Parser & Email Intelligence.md)
- **UC2 SP16**: [Correspondence Classifier](./01 SP16 - Correspondence Classifier.md)
- **UC2 SP17**: [Registry Suggester](./01 SP17 - Registry Suggester.md)
- **UC2 SP19**: [Protocol Workflow Orchestrator](./01 SP19 - Protocol Workflow Orchestrator.md)

---

**Associato a**: UC2 - Protocollo Informatico, UC5 - Produzione Documentale
**MS Primario**: MS07 Generic ETL Pipeline
**MS Supporto**: MS01 Generic Classifier Engine
**Status**: Inherited from UC5, specialized for UC2
**Created**: 2025-11-17
