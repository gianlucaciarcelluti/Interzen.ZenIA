# MS13-SECURITY - Microservice

**Status**: Active
**Version**: 1.1
**Last Updated**: 2025-11-21
**Owner**: Security Team

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)

---

## Avvio Rapido (5 minuti)

### Che cos'è MS13-SECURITY?
MS13-SECURITY fornisce Identity Management centralizzato (Keycloak) con autenticazione forte, autorizzazione RBAC/ABAC, e compliance con normative di sicurezza internazionali (PNRR, Piano Triennale, NIS2, eIDAS).

### Responsabilità principali
- **Autenticazione**: OAuth2, OIDC, SAML, MFA, SPID, CIE
- **Autorizzazione**: RBAC, ABAC, policy engine
- **Encryption**: AES-256 at rest, TLS 1.3 in transit, HSM key management
- **Compliance**: PNRR, NIS2, eIDAS, GDPR audit trail
- **Monitoraggio**: Security logging, anomaly detection, breach alerting

### Primi passi
1. Consulta [SPECIFICATION.md](SPECIFICATION.md) per le specifiche tecniche dettagliate
2. Controlla `docker-compose.yml` per il setup locale
3. Rivedi [API.md](API.md) per gli endpoint di integrazione
4. Esplora la cartella [examples/](examples/) per esempi di request/response

### Stack tecnologico
- **Linguaggio**: Python 3.10+
- **API**: FastAPI
- **Database**: PostgreSQL (encrypted)
- **Cache**: Redis (encrypted)
- **Identity Provider**: Keycloak 23.x (HA)
- **Key Management**: HSM (Hardware Security Module)

### Dipendenze
Vedi [SPECIFICATION.md](SPECIFICATION.md) per i dettagli sulle dipendenze.

---

## 🔐 Conformità Normativa

### Framework Normativi Applicabili

- ☑ PNRR (Piano Nazionale Ripresa e Resilienza)
- ☑ Piano Triennale AgID 2024-2026
- ☑ NIS2 Directive (2022/2555/EU)
- ☑ eIDAS (Regolamento 2014/910)
- ☑ GDPR (Regolamento 2016/679)
- ☐ CAD (Codice dell'Amministrazione Digitale)
- ☐ D.Lgs 82/2005 - Identità Digitale

Mappa completa: [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md)

---

## 📋 Conformità PNRR (Piano Nazionale Ripresa e Resilienza)

### Missione 1, Componente 1.4: Sicurezza Informatica

**Obiettivo**: Implementare Identity Management conforme a standard internazionali di sicurezza per PA.

| Requisito PNRR | Implementazione MS13 | Status |
|---|---|---|
| **Crittografia AES-256 at rest** | PostgreSQL + Redis con encryption at rest | ✅ |
| **TLS 1.3 in transit** | Keycloak con TLS 1.3 su tutti endpoint | ✅ |
| **Zero Trust architecture** | Continuous authentication + MFA mandatory | ✅ |
| **MFA obbligatorio** | OTP + WebAuthn (FIDO2) support | ✅ |
| **HSM key management** | Hardware Security Module per master keys | ✅ |
| **Audit trail immutabile** | Security events logged in append-only store | ✅ |

**Conformità raggiunta**: MS13 implementa tutte le misure richieste da M1C1.4 per identity & access management.

---

## 📚 Conformità Piano Triennale AgID 2024-2026

### Capitolo 4: Piattaforme Digitali (SPID & CIE Integration)

#### 4.1 Sistema Pubblico Identità Digitale (SPID)

| Requisito SPID | Implementazione MS13 | Status |
|---|---|---|
| **SPID Authentication** | Keycloak SAML 2.0 provider per SPID | ✅ |
| **Livello di garanzia** | Supporto L1, L2, L3 authentication | ✅ |
| **Attribute Provider** | SAML assertion con attributi SPID standard | ✅ |
| **Encryption** | TLS 1.3 + encrypted SAML assertions | ✅ |

**Configurazione SPID**:
```
Keycloak Client Configuration:
├─ Protocol: SAML 2.0
├─ Assertion Consumer Service URL: https://zenaria.example.it/auth/saml
├─ Attributes:
│  ├─ personalNumber (Codice Fiscale)
│  ├─ name (Nome)
│  ├─ familyName (Cognome)
│  ├─ email
│  ├─ phone
│  └─ organisationalUnitName (Agenzia/Ente)
└─ Signature: RSA-SHA256
```

#### 4.2 Carta Identità Elettronica (CIE) Integration

| Requisito CIE | Implementazione MS13 | Status |
|---|---|---|
| **CIE Authentication** | eIDAS certificate validation | ✅ |
| **eIDAS Qualified Certificate** | X.509 certificate chain validation | ✅ |
| **OCSP Stapling** | Real-time certificate validation | ✅ |
| **LDAP Directory** | Optional LDAP backend per CIE attributes | ✅ |

### Capitolo 7: Sicurezza Informatica

#### 7.1 Crittografia (FIPS 140-2 Compliance)

MS13 implementa crittografia conforme a FIPS 140-2 Level 2:

| Algoritmo | Utilizzo | Standard |
|---|---|---|
| **AES-256-GCM** | Database encryption at rest | FIPS 140-2 |
| **TLS 1.3** | Communication in transit | RFC 8446 |
| **RSA-2048+ o ECDSA** | Key generation & signing | FIPS 186-4 |
| **SHA-256+** | Hashing (password, tokens) | FIPS 180-4 |
| **Bcrypt** | Password hashing (cost=12) | OWASP ESAPI |

**Hardware Security Module Configuration**:
```
HSM Setup:
├─ Device: Thales HSM or equivalent (FIPS 140-2 Level 3)
├─ Master Keys: 2 keys, 3 escrow (ceremony-based)
├─ Key Slots:
│  ├─ SPID certificate (signing)
│  ├─ CIE certificate (validation)
│  ├─ Database encryption key
│  └─ Token signing key
├─ Backup: Encrypted backup with escrow
└─ Audit: All HSM operations logged
```

#### 7.2 Access Control (RBAC + ABAC)

MS13 implementa controllo accessi a due livelli:

**RBAC (Role-Based Access Control)**:
```
Roles in Keycloak:
├─ admin: Amministratori piattaforma
├─ compliance-officer: Verifica conformità
├─ security-auditor: Review di security events
├─ data-processor: Accesso dati personali
├─ document-manager: Gestione documenti
└─ end-user: Utenti finali con profilo base
```

**ABAC (Attribute-Based Access Control)**:
```
Policies based on:
├─ User Attributes: department, role, clearance_level
├─ Resource Attributes: classification, owner, created_date
├─ Environment Attributes: IP range, time_of_access, device_type
└─ Actions: read, write, delete, export, share
```

---

## 🔐 Conformità NIS2 Directive (2022/2555/EU)

### Articolo 6: Critical Infrastructure Protection

MS13 protegge infrastrutture critiche tramite:

| Controllo NIS2 | Implementazione MS13 | SLA |
|---|---|---|
| **Strong authentication** | MFA mandatory + SPID/CIE | 100% enforcement |
| **Encrypted storage** | AES-256 + HSM key management | At-rest encryption |
| **Secure communication** | TLS 1.3 + certificate pinning | In-transit encryption |
| **Access control** | RBAC + ABAC + continuous monitoring | Real-time |
| **Audit logging** | Immutable event log per GDPR/NIS2 | 12+ months retention |
| **Incident response** | Integration con UC8 SIEM per alerting | <15 min detection |

### Articolo 13: Supply Chain & Third-Party Security

MS13 monitora dipendenze di sicurezza:

- **Certificate Pinning**: SPID/CIE root certificate pinning
- **Dependency Scanning**: Regular CVE scanning per Keycloak + dependencies
- **HSM Vendor**: Compliance con Thales/IBM security standards
- **OAuth Provider Security**: Validation di SPID/CIE provider certificates

---

## 🏛️ Conformità eIDAS (Regolamento 2014/910)

### Articolo 13: Qualified Signatures

MS13 supporta qualified signatures per SPID/CIE:

```
eIDAS Signature Chain:
│
├─ Certificate Validation (Art. 24)
│  └─ X.509 certificate chain validation
│     ├─ Root CA (Pubblica Amministrazione)
│     ├─ Intermediate CA
│     └─ End-entity certificate (SPID/CIE)
│
├─ Signature Verification
│  └─ RSA-SHA256 or ECDSA signature validation
│     ├─ Integrity check (content hash match)
│     └─ Authenticity check (certificate validity)
│
├─ Timestamp (RFC 3161)
│  └─ Optional: Add TSA timestamp for legal proof
│
└─ Audit Trail
   └─ Log signature verification for compliance
```

### Articolo 24: Qualified Timestamping

MS13 integra marca temporale:
- **TSA Endpoint**: Optional integration con RFC 3161 Time Stamping Authority
- **Token Validity**: JWT tokens con timestamp per audit trail
- **Audit Log**: Security events with server timestamp

---

## ✅ Checklist Conformità Pre-Deployment

### PNRR M1C1.4 - Encryption & Zero Trust

- [ ] AES-256 encryption at rest abilitato per PostgreSQL
- [ ] TLS 1.3 su tutti i Keycloak endpoint (certificato valido)
- [ ] MFA (OTP + WebAuthn) obbligatorio per admin
- [ ] HSM integrato e master keys caricati
- [ ] Audit trail per security events (append-only)
- [ ] Password policy enforcement (complexity, rotation, history)
- [ ] Brute force detection attivato (<5 failed login attempts)
- [ ] Session management con timeout configurabile

### Piano Triennale Cap 4 - SPID/CIE Integration

- [ ] SPID SAML provider configurato e testato
- [ ] SPID certificate (firma) nel keystore
- [ ] CIE certificate chain validato
- [ ] OCSP stapling per CIE certificate validation
- [ ] Attributi SPID mappati in Keycloak (nome, cognome, CF)
- [ ] Livelli di garanzia SPID (L1, L2, L3) supportati
- [ ] User sync da SPID/CIE attribute provider

### Piano Triennale Cap 7 - Crittografia & Access Control

- [ ] FIPS 140-2 compliance verificato
- [ ] AES-256-GCM per database encryption
- [ ] RSA-2048+ or ECDSA per key generation
- [ ] SHA-256+ per password/token hashing
- [ ] RBAC roles configurate e assegnate
- [ ] ABAC policies definite per sensitive resources
- [ ] TLS certificate + pinning per SPID/CIE communication
- [ ] Certificate rotation procedure documentata

### NIS2 Directive - Critical Infrastructure

- [ ] Strong authentication (MFA) mandatory setup
- [ ] Encrypted storage: at-rest (AES) + in-transit (TLS)
- [ ] HSM key management with escrow backup
- [ ] Access control logging (who, what, when)
- [ ] Incident alerting (integration UC8 SIEM)
- [ ] Breach notification procedure integrata in UC9
- [ ] Dependency scanning & CVE monitoring
- [ ] Third-party certificate validation

### eIDAS - Signature & Timestamping

- [ ] X.509 certificate chain validation working
- [ ] SPID/CIE certificate pinning configured
- [ ] RSA-SHA256 signature verification tested
- [ ] Optional: RFC 3161 TSA integration
- [ ] Audit log per signature operations
- [ ] Certificate rotation procedure documented

---

## 📅 Checklist Conformità Annuale

**Frequenza**: Annuale (Novembre di ogni anno)

- [ ] HSM key rotation completata (ceremony)
- [ ] SPID/CIE certificate renewal verificato
- [ ] Penetration test on authentication endpoints
- [ ] FIPS 140-2 compliance audit completato
- [ ] MFA adoption rate verificato (% compliance)
- [ ] NIS2 incident statistics analizzati
- [ ] Password policy effectiveness valutato
- [ ] Access control audit (RBAC/ABAC roles review)
- [ ] Third-party security assessment (HSM vendor, OAuth provider)
- [ ] Training on identity security updated for staff

---

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)
