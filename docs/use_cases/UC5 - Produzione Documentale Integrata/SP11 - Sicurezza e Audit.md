# SP11 - Security & Audit

## Security, Autenticazione e Registro di Audit

Questo diagramma mostra tutte le interazioni del **Security & Audit (SP11)** per la sicurezza e tracciabilità.

```mermaid
sequenceDiagram
    autonumber
    participant U as Utente (Operatore)
    participant UI as Web UI
    participant GW as API Gateway
    participant SEC as SP11 Security & Audit
    participant WF as SP09 Workflow Engine
    participant DB as PostgreSQL
    participant BLOCKCHAIN as Blockchain

    Note over U,BLOCKCHAIN: Fase 1: Autenticazione e Autorizzazione

    U->>UI: Login

    UI->>GW: POST /auth/login<br/>{username, password}

    GW->>SEC: Autentica e autorizza richiesta

    SEC->>DB: Log access attempt

    SEC->>SEC: Verifica credenziali<br/>Check user permissions

    SEC->>SEC: Genera JWT token

    SEC-->>GW: JWT validated + user permissions

    GW-->>UI: {token, user_profile}

    UI-->>U: Login successful

    Note over U,BLOCKCHAIN: Workflow Execution (con Security Checks)

    U->>UI: Inizia workflow

    UI->>GW: POST /api/v1/workflows/documents<br/>Authorization: Bearer JWT

    GW->>SEC: Valida JWT token

    SEC->>SEC: Verify token signature<br/>Check expiration<br/>Extract user permissions

    alt Token Invalido o Scaduto
        SEC-->>GW: 401 Unauthorized
        GW-->>UI: Token expired
        UI-->>U: Richiedi re-login
    end

    SEC->>DB: Log authenticated action

    SEC-->>GW: Authorized - user_id: user_123

    GW->>WF: Inizia workflow

    Note over U,BLOCKCHAIN: Continuous Security Monitoring

    loop Every critical action
        WF->>SEC: Log action<br/>{workflow_id, action, user_id}

        SEC->>DB: Append to audit log

        SEC->>SEC: Anomaly detection<br/>Check suspicious patterns

        alt Anomalia rilevata
            SEC->>SEC: Trigger security alert
            SEC->>DB: Log security event
        end
    end

    Note over U,BLOCKCHAIN: Fase 9: Registro di Audit Completo

    WF->>SEC: POST /audit-log<br/>{workflow_complete, actions_log}

    SEC->>DB: Store immutable audit trail<br/>(blockchain hash)

    SEC->>BLOCKCHAIN: Compute Merkle tree hash

    BLOCKCHAIN-->>SEC: Hash: 0x1234567890abcdef...

    SEC->>DB: Store blockchain hash

    SEC->>SEC: Generate compliance report<br/>(GDPR Art. 22)

    SEC->>DB: Store GDPR compliance record

    SEC-->>WF: Audit log stored successfully

    Note over U,BLOCKCHAIN: Accesso Registro di Audit

    U->>UI: Richiedi audit trail<br/>workflow WF-12345

    UI->>GW: GET /audit/workflows/WF-12345

    GW->>SEC: Authorize access

    SEC->>SEC: Check user permissions<br/>(AUDIT_READ role)

    alt Non autorizzato
        SEC-->>GW: 403 Forbidden
    end

    SEC->>DB: Query audit trail

    DB-->>SEC: Audit records + blockchain hash

    SEC->>BLOCKCHAIN: Verify hash integrity

    BLOCKCHAIN-->>SEC: Hash verified ✅

    SEC-->>GW: {audit_trail, verified: true}

    GW-->>UI: Audit trail data

    UI-->>U: Visualizza audit trail<br/>con verifica blockchain

    rect rgb(200, 255, 200)
        Note over SEC: Security & Audit<br/>JWT Authentication<br/>Immutable Registro di Audit<br/>GDPR Compliance<br/>Blockchain Verification
    end
```
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

## 🏛️ Conformità Normativa - SP11

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP11 (Sicurezza e Audit)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC1

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP11 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP11 - gestisce dati personali

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

## Riepilogo Conformità SP11

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

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP11

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP11 (Sicurezza e Audit)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC1

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP11 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP11 - gestisce dati personali

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

## Riepilogo Conformità SP11

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


## Funzionalità Chiave SP11

### Autenticazione e Autorizzazione

#### JWT Token Structure

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": "user_123",
    "username": "mario.rossi@comune.it",
    "role": "RESPONSABILE_UFFICIO",
    "permissions": [
      "CREATE_DELIBERA",
      "APPROVE_DELIBERA",
      "CREATE_DETERMINA",
      "VIEW_AUDIT_LOG"
    ],
    "iss": "provvedimento-assistant",
    "exp": 1696845600,
    "iat": 1696842000,
    "jti": "token-uuid-12345"
  },
  "signature": "..."
}
```

#### Ruoli e Permessi

| Ruolo | Permessi | Descrizione |
|-------|----------|-------------|
| **ADMIN** | ALL | Amministratore sistema |
| **RESPONSABILE_UFFICIO** | CREATE_*, APPROVE_*, VIEW_* | Responsabile ufficio |
| **OPERATORE** | CREATE_*, VIEW_OWN | Operatore base |
| **REVISORE** | VIEW_*, AUDIT_READ | Solo lettura + audit |
| **GUEST** | VIEW_PUBLIC | Accesso limitato |

#### Permission Check

```mermaid
flowchart TD
    A["Input: user, action, resource"] --> B["Build required_permission string:<br/>required_permission = action + '_' + resource"]
    B --> C{{"Check:<br/>required_permission in user.permissions?"}}
    C -->|Yes| D["Return: True"]
    C -->|No| E["Return: False"]

    style A fill:#e1f5ff
    style D fill:#d4edda
    style E fill:#f8d7da
```

### Registro di Audit

#### Audit Record Structure

```json
{
  "audit_record": {
    "audit_trail_id": "AUDIT-98765",
    "workflow_id": "WF-12345",
    "document_id": "DOC-67890",
    "blockchain_hash": "0x1234567890abcdef...",
    "merkle_root": "0xabcdef1234567890...",
    "timestamp": "2025-10-08T10:30:45Z",
    "verification_status": "VERIFIED"
  },
  "actions_log": [
    {
      "seq": 1,
      "timestamp": "2025-10-08T10:20:00Z",
      "action": "WORKFLOW_INITIATED",
      "user_id": "user_123",
      "user_name": "Mario Rossi",
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0...",
      "session_id": "sess-abc123"
    },
    {
      "seq": 2,
      "timestamp": "2025-10-08T10:20:05Z",
      "action": "DOCUMENT_CLASSIFIED",
      "service": "SP07",
      "confidence": 0.94,
      "processing_time_ms": 450,
      "ai_model": "DistilBERT"
    },
    {
      "seq": 3,
      "timestamp": "2025-10-08T10:20:12Z",
      "action": "LEGAL_CONTEXT_RETRIEVED",
      "service": "SP04",
      "normativa_refs": ["L.241/1990", "D.Lgs 42/2004"],
      "processing_time_ms": 1200
    },
    {
      "seq": 4,
      "timestamp": "2025-10-08T10:22:35Z",
      "action": "TEMPLATE_GENERATED",
      "service": "SP05",
      "model": "gpt-4-turbo",
      "tokens_used": 1234,
      "api_cost_euros": 0.0148
    },
    {
      "seq": 5,
      "timestamp": "2025-10-08T10:25:33Z",
      "action": "DOCUMENT_VALIDATED",
      "service": "SP06",
      "validation_status": "WARNING",
      "warnings_count": 1
    },
    {
      "seq": 6,
      "timestamp": "2025-10-08T10:26:15Z",
      "action": "QUALITY_CHECKED",
      "service": "SP08",
      "quality_score": 82,
      "corrections_suggested": 8
    },
    {
      "seq": 7,
      "timestamp": "2025-10-08T10:28:00Z",
      "action": "HUMAN_APPROVED",
      "user_id": "user_123",
      "approval_level": "RESPONSABILE_UFFICIO",
      "signature": "BASE64_ENCODED_SIGNATURE"
    },
    {
      "seq": 8,
      "timestamp": "2025-10-08T10:29:15Z",
      "action": "PROTOCOLLED",
      "system": "PROTOCOLLO",
      "protocol_number": "12345/2025"
    },
    {
      "seq": 9,
      "timestamp": "2025-10-08T10:30:30Z",
      "action": "DIGITALLY_SIGNED",
      "system": "FIRMA_DIGITALE",
      "signer": "ing. Mario Rossi",
      "timestamp_authority": "InfoCert"
    },
    {
      "seq": 10,
      "timestamp": "2025-10-08T10:30:45Z",
      "action": "WORKFLOW_COMPLETED",
      "final_status": "PUBLISHED",
      "total_duration_sec": 645
    }
  ]
}
```

### GDPR Compliance

#### Article 22 - Right to Explanation

```json
{
  "gdpr_compliance": {
    "purpose": "GENERAZIONE_ATTO_AMMINISTRATIVO",
    "legal_basis": "Art. 6(1)(e) GDPR - public interest",
    "data_subjects": ["Mario Rossi"],
    "personal_data_processed": {
      "categories": ["nome", "ruolo", "firma_digitale"],
      "purposes": ["identificazione_responsabile", "firma_atto"],
      "retention_period": "10 years (normativa archivistica)"
    },
    "automated_decision": {
      "enabled": true,
      "human_oversight": true,
      "explainability_provided": true,
      "right_to_object": true
    },
    "data_protection_measures": [
      "Crittografia at rest (AES-256)",
      "Crittografia in transit (TLS 1.3)",
      "Access control (RBAC)",
      "Audit logging (immutable)",
      "Anonymization after retention period"
    ],
    "dpia_required": false,
    "dpo_contact": "dpo@comune.it"
  }
}
```

#### Minimizzazione Dati

```json
{
  "data_minimization": {
    "principle": "Collect only necessary data",
    "implementation": {
      "classification_model": "No personal data stored",
      "knowledge_base": "No personal data in normativa",
      "generation": "dati personali only from user input",
      "validation": "No additional personal data collected"
    },
    "storage": {
      "encrypted_fields": ["nome", "firma"],
      "anonymized_after": "10 years",
      "deletion_policy": "Automatic after 15 years"
    }
  }
}
```

### Blockchain Verification

#### Merkle Tree Construction

```mermaid
flowchart TD
    A["Input: actions_log (List of Actions)"] --> B["Create hashes list:<br/>hashes = [sha256 of each action.json]"]
    B --> C{{"Check:<br/>len(hashes) > 1?"}}

    C -->|No| H["Return: hashes[0]<br/>(Merkle root)"]
    C -->|Yes| D{{"Check:<br/>len(hashes) is odd?"}}

    D -->|Yes| E["Duplicate last hash:<br/>hashes.append(hashes[-1])"]
    D -->|No| F["Skip duplication"]

    E --> G["Combine hashes in pairs:<br/>hashes = [sha256(hashes[i] + hashes[i+1])<br/>for i in range(0, len(hashes), 2)]"]
    F --> G

    G --> C

    style A fill:#e1f5ff
    style H fill:#d4edda
```

#### Verification Process

```json
{
  "verification": {
    "workflow_id": "WF-12345",
    "stored_hash": "0x1234567890abcdef...",
    "computed_hash": "0x1234567890abcdef...",
    "match": true,
    "verification_timestamp": "2025-10-08T11:00:00Z",
    "verifier": "SP08-Security",
    "integrity_status": "VERIFIED"
  }
}
```

### Anomaly Detection

```json
{
  "anomaly_detection": {
    "rules": [
      {
        "rule": "MULTIPLE_FAILED_LOGINS",
        "threshold": 5,
        "action": "LOCK_ACCOUNT",
        "alert": "HIGH"
      },
      {
        "rule": "UNUSUAL_WORKFLOW_TIME",
        "threshold": "3x avg_time",
        "action": "LOG_WARNING",
        "alert": "MEDIUM"
      },
      {
        "rule": "PERMISSION_ESCALATION_ATTEMPT",
        "threshold": 1,
        "action": "BLOCK_IMMEDIATELY",
        "alert": "CRITICAL"
      },
      {
        "rule": "BULK_DOCUMENT_CREATION",
        "threshold": 50,
        "action": "RATE_LIMIT",
        "alert": "LOW"
      }
    ],
    "ml_based": {
      "enabled": true,
      "model": "Isolation Forest",
      "features": [
        "login_time",
        "workflow_duration",
        "document_type",
        "user_location"
      ]
    }
  }
}
```

### Security Events

```json
{
  "security_events": [
    {
      "event_id": "SEC-98765",
      "timestamp": "2025-10-08T10:15:23Z",
      "severity": "HIGH",
      "type": "FAILED_LOGIN_ATTEMPT",
      "user_id": "user_456",
      "ip_address": "203.0.113.45",
      "details": "Password incorrect (attempt 4/5)",
      "action_taken": "Account locked after 5th attempt"
    },
    {
      "event_id": "SEC-98766",
      "timestamp": "2025-10-08T10:45:12Z",
      "severity": "MEDIUM",
      "type": "PERMISSION_DENIED",
      "user_id": "user_789",
      "resource": "DELIBERA_GIUNTA",
      "action": "APPROVE",
      "details": "User lacks APPROVE_DELIBERA permission"
    }
  ]
}
```

### Compliance Reports

#### Monthly Security Report

```json
{
  "security_report": {
    "period": "2025-09",
    "metrics": {
      "total_logins": 1234,
      "failed_logins": 56,
      "security_events": 12,
      "critical_events": 0,
      "accounts_locked": 3,
      "permission_violations": 8
    },
    "audit_trails_created": 342,
    "blockchain_verifications": 342,
    "verification_success_rate": 1.0,
    "gdpr_requests": {
      "access_requests": 2,
      "deletion_requests": 0,
      "objection_requests": 0
    },
    "recommendations": [
      "Review permission model for user_789",
      "Enable MFA for ADMIN roles"
    ]
  }
}
```

### Conservazione Dati

```json
{
  "data_retention": {
    "audit_logs": {
      "retention_period": "15 years",
      "legal_basis": "Normativa archivistica PA",
      "deletion_policy": "Automatic after retention period"
    },
    "personal_data": {
      "retention_period": "10 years",
      "anonymization_after": "10 years",
      "deletion_policy": "Anonymization + encryption key deletion"
    },
    "security_events": {
      "retention_period": "7 years",
      "deletion_policy": "Automatic purge"
    },
    "blockchain_hashes": {
      "retention_period": "PERMANENT",
      "immutable": true
    }
  }
}
```

### Tecnologie

- **Authentication**: JWT (RS256)
- **Authorization**: RBAC (Role-Based Controllo Accesso)
- **Crittografia**: AES-256 (at rest), TLS 1.3 (in transit)
- **Hashing**: SHA-256 for blockchain
- **Blockchain**: Private Ethereum / Hyperledger Fabric
- **Anomaly Detection**: Isolation Forest (scikit-learn)
- **Database**: PostgreSQL (audit tables immutable)
- **Compliance**: GDPR Art. 22 compliance framework
