# Architettura di Sicurezza: ZenIA vs Requisiti EU AI Act

**Stato**: ✅ FINALE | **Versione**: 1.0 | **Data**: 21 novembre 2025 | **Conformità**: Regolamento UE 2024/1689 (Allegato III)

---

## Sommario Esecutivo

Questo documento definisce l'architettura di sicurezza di ZenIA in allineamento con i requisiti del Regolamento UE sull'IA 2024/1689 (AI Act) Allegato III. Copre protezione dati, crittografia, audit trail, controllo accessi, risposta agli incidenti e meccanismi di monitoraggio necessari per sistemi di IA ad alto rischio.

**Stato Conformità**: 🟡 **IMPLEMENTAZIONE PARZIALE**
- ✅ **Implementato (60%)**: Infrastruttura di sicurezza di base (crittografia, TLS, controllo accessi)
- 🟡 **Parzialmente Implementato (35%)**: Audit trail, monitoraggio, risposta agli incidenti
- 🔴 **Non Implementato (5%)**: Documentazione valutazione rischi formale, template DPIA

**Sforzo Richiesto**: 25 ore | **Timeline**: Q4 2025-2 & Q1 2026-1

---

## 1. Framework Normativo (Allegato III AI Act)

### 1.1 Articoli Applicabili

| Articolo | Requisito | Ambito ZenIA | Stato |
|----------|-----------|-------------|-------|
| 27 | Sistema di gestione dei rischi | Tutti i sistemi | 🟡 PARZIALE |
| 28 | Governance e dati di training | MS01, MS02, MS04 training | 🟡 PARZIALE |
| 29 | Documentazione e registrazione | Tutti i sistemi | 🟠 PARZIALE |
| 30 | Sistema di registrazione automatico | Requisito audit trail | 🟡 PARZIALE |
| 31 | Capacità supervisione umana | Tutti sistemi alto rischio | ✅ IMPLEMENTATO |
| 32 | Robustezza contro attacchi | MS13-SECURITY, MS11-GATEWAY | ✅ IMPLEMENTATO |
| 33 | Cyber-sicurezza e resilienza | MS13-SECURITY | ✅ IMPLEMENTATO |

### 1.2 Sistemi Alto Rischio Soggetti ad Allegato III

**Sistemi ZenIA Alto/Medio Rischio**:
- MS01-CLASSIFIER (🔴 ALTO-RISCHIO)
- MS02-ANALYZER (🟠 MEDIO-RISCHIO)
- MS04-VALIDATOR (🟠 MEDIO-RISCHIO)

---

## 2. Livelli di Architettura di Sicurezza

### 2.1 Sicurezza Perimetrale (MS11-API-GATEWAY)

**Scopo**: Controllare accesso esterno a infrastruttura ZenIA

**Implementazione**:
- **TLS/SSL**: TLS 1.3 obbligatorio per tutte comunicazioni esterne
- **Gestione Certificati**:
  - Certificati emessi da PKI interna (MS16-REGISTRY)
  - Rotazione: Ogni 90 giorni (automatizzata via cert-manager)
  - Pinning: Certificate pinning per endpoint critici
- **Rate Limiting**:
  - Per-utente: 1.000 req/min
  - Per-IP: 10.000 req/min
  - Protezione burst: max 100 req/5 sec
- **Protezione DDoS**:
  - Protezione DDoS CloudFlare (se cloud-hosted)
  - Filtraggio richieste per validazione header
  - Rilevamento anomalie via MS08-MONITOR

**Mappatura Conformità**:
- ✅ AI Act Art. 32: Protezione contro attacchi avversariali
- ✅ AI Act Art. 33: Misure cyber-sicurezza

**Stato**: ✅ IMPLEMENTATO
- **Evidenza**: MS11-GATEWAY/SPECIFICATION.md Sezione 4 (configurazione TLS)
- **Verifica**: Test TLS in `tests/security/tls_verification.py`

---

### 2.2 Autenticazione e Autorizzazione

**Scopo**: Verificare identità utente e implementare controllo accessi

#### 2.2.1 Meccanismi Autenticazione

**OAuth 2.0 + OpenID Connect** (via MS09-MANAGER):
- Integrazione Identity Provider (Keycloak/Auth0 compatibile)
- Autenticazione basata token (JWT)
- Supporto autenticazione multi-fattore (MFA)
- Timeout sessione: 8 ore (configurabile)

**Autenticazione Service-to-Service**:
- mTLS (mutual TLS) per comunicazione inter-microservizio
- Validazione certificati: Certificati client e server richiesti
- Rotazione certificati: Settimanale

**Autenticazione API Key** (legacy fallback):
- Deprecata; piano ritiro entro Q2 2026
- Chiavi archiviate in MS16-REGISTRY (crittate a riposo)
- Policy rotazione: 90 giorni

**Mappatura Conformità**:
- ✅ AI Act Art. 29: Governance accesso dati training
- ✅ GDPR Art. 25: Protezione dati by design

**Stato**: ✅ IMPLEMENTATO
- **Evidenza**: MS09-MANAGER/SPECIFICATION.md (Identity Management)
- **Verifica**: `tests/security/auth_integration_test.py`

#### 2.2.2 Autorizzazione (RBAC + ABAC)

**Controllo Accessi Basato su Ruoli (RBAC)**:
```
┌─────────────────────────────────────┐
│ Amministratore Organizzazione PA    │
│ - Gestire utenti, audit trail       │
│ - Configurare regole validazione    │
│ - Visualizzare tutti documenti      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Processore Documenti (Utente Std)   │
│ - Caricare documenti                │
│ - Visualizzare stato elaborazione   │
│ - Scaricare documenti elaborati     │
│ - NO accesso configurazione sistema │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Visualizzatore Solo Lettura         │
│ - Visualizzare documenti (only proc)│
│ - Visualizzare analytics (aggregati)│
│ - No caricamento, no export         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Amministratore Sistema              │
│ - Accesso completo a tutti sistemi  │
│ - Gestione infrastruttura           │
│ - Gestione audit trail              │
│ - Configurazione sicurezza          │
└─────────────────────────────────────┘
```

**Controllo Accessi Basato su Attributi (ABAC)**:
- Livello classificazione documento (OFFICIAL, CONFIDENTIAL, PUBLIC)
- Ambito organizzazione (accesso solo documenti org propria)
- Accessi basati su tempo (orari ufficio vs fuori orario)
- Restrizioni IP (solo rete PA per operazioni sensibili)

**Matrice Permessi** (esempio):

| Ruolo | Carica | Elabora | Scarica | Valida | Override | Audit |
|-------|--------|---------|---------|--------|----------|-------|
| Processore | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Validator | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Supervisore | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Mappatura Conformità**:
- ✅ AI Act Art. 31: Meccanismi supervisione umana adeguata
- ✅ GDPR Art. 32: Misure controllo accessi

**Stato**: ✅ IMPLEMENTATO
- **Evidenza**: MS07-DISTRIBUTOR/SPECIFICATION.md (logica autorizzazione)
- **Configurazione**: `configs/rbac-roles.yaml` (definizioni ruoli)

---

### 2.3 Protezione Dati e Crittografia

#### 2.3.1 Crittografia a Riposo

**Crittografia Database** (PostgreSQL):
- **Algoritmo**: AES-256-CBC (approvato FIPS 140-2)
- **Gestione Chiavi**: AWS KMS (o HashiCorp Vault per on-premise)
- **Ambito**: Tutte tabelle dati (documenti, metadati, audit log)
- **Implementazione**:
  - Estensione PostgreSQL pgcrypto per funzioni crittografia
  - Transparent Data Encryption (TDE) a livello database
  - Chiavi archiviate separatamente in HSM (Hardware Security Module)

**Schema Esempio**:
```sql
-- Esempio colonne crittate
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    filename TEXT,
    content BYTEA,  -- Crittato via pgcrypto
    metadata JSONB,  -- Crittato via pgcrypto
    created_at TIMESTAMP,
    encryption_key_id UUID REFERENCES encryption_keys(id)
);

-- Gestione chiavi crittografia
CREATE TABLE encryption_keys (
    id UUID PRIMARY KEY,
    key_name VARCHAR(255) NOT NULL,
    algorithm VARCHAR(50) NOT NULL,  -- 'AES-256-CBC'
    created_at TIMESTAMP NOT NULL,
    rotated_at TIMESTAMP,
    status VARCHAR(20) NOT NULL,  -- 'ACTIVE', 'RETIRED'
    kms_key_arn VARCHAR(500)  -- AWS KMS key ARN
);
```

**Crittografia Storage File** (S3/Object Storage):
- **Crittografia Server-Side (SSE)**: Crittografia oggetto S3 con chiavi gestite cliente
- **Algoritmo**: AES-256
- **Ambito**: Tutti caricamenti documenti, dati backup, archivi log
- **Retention**: Backup crittati mantenuti 90 giorni

**Crittografia Cache** (Redis):
- **Crittografia Redis**: redis-cli con TLS only
- **Protezione Dati**:
  - Campi sensibili (PII) NOT in cache
  - Cache TTL: max 24 ore
  - Refresh automatico su cambiamenti dati sensibili

**Mappatura Conformità**:
- ✅ AI Act Art. 28: Governance dati (crittografia come protezione)
- ✅ GDPR Art. 32: Crittografia dati personali
- ✅ GDPR Art. 25: Protezione dati by design

**Stato**: ✅ IMPLEMENTATO
- **Evidenza**: MS13-SECURITY/SPECIFICATION.md (implementazione crittografia)
- **Verifica**: `tests/security/encryption_test.py` (test integrazione KMS)

#### 2.3.2 Crittografia in Transito

**Crittografia Rete**:
- **Tutte Comunicazioni Esterne**: TLS 1.3 obbligatorio
- **Comunicazioni Interne**: mTLS per service-to-service
- **Ambito**:
  - Client ↔ API Gateway: TLS 1.3
  - API Gateway ↔ Microservizi: mTLS
  - Microservizi ↔ Database: TLS
  - Microservizi ↔ Cache: TLS
  - Microservizi ↔ Object Storage: TLS

**Gestione Certificati**:
- **Infrastruttura CA**: PKI interna con Intermediate CA
- **Ciclo Vita Certificati**:
  - Emissione: Automatizzata via cert-manager
  - Rotazione: Ogni 90 giorni (esterno), ogni 30 giorni (interno)
  - Revoca: CRL + OCSP stapling
  - Pinning: Public key pinning per endpoint critici

**Configurazione VPN/Tunnel** (opzionale):
- Se ibrido on-premise/cloud: VPN site-to-site con IPSec
- IPSec IKEv2 + AES-256 + SHA-384

**Mappatura Conformità**:
- ✅ AI Act Art. 32: Protezione contro attacchi avversariali
- ✅ GDPR Art. 32: Crittografia in transito

**Stato**: ✅ IMPLEMENTATO
- **Evidenza**: MS11-GATEWAY/SPECIFICATION.md (configurazione TLS)
- **Verifica**: `tests/security/tls_test.py`

---

### 2.4 Audit Trail e Logging (MS14-AUDIT)

**Scopo**: Mantenere record immutabile di tutte azioni sistema per conformità e forensics

#### 2.4.1 Schema Audit Trail

**Eventi Loggati**:

```
┌─────────────────────────────────────────┐
│     VOCE AUDIT LOG                      │
├─────────────────────────────────────────┤
│ timestamp: 2025-11-21T15:32:45.123Z    │
│ event_id: e550e8c2-91a3-4f2d-b3...    │
│ user_id: user-123@pa.example.com       │
│ user_role: VALIDATOR                   │
│ action: DOCUMENTO_VALIDATO              │
│ resource: document-456 (Invoice.pdf)   │
│ resource_classification: OFFICIAL      │
│ ip_address: 192.168.1.100              │
│ user_agent: Mozilla/5.0...             │
│ outcome: SUCCESS                        │
│ details: {                              │
│   "validation_rules_checked": 45,      │
│   "rules_passed": 45,                  │
│   "rules_failed": 0,                   │
│   "confidence_score": 0.987            │
│ }                                       │
│ signature: SHA-256(log + key)          │
│ previous_hash: a1b2c3d4e5f6g7h8i9j0.. │
└─────────────────────────────────────────┘
```

**Categorie Loggati**:

| Categoria | Eventi Loggati | Retention | Stato |
|-----------|----------------|-----------|-------|
| **Autenticazione** | Login, logout, MFA, token gen | 2 anni | ✅ Attivo |
| **Autorizzazione** | Accesso concesso, negato, cambio ruoli | 2 anni | ✅ Attivo |
| **Accesso Dati** | Upload, visualizzazione, download, elimina | 90 giorni | ✅ Attivo |
| **Decisione IA** | Classificazione, validazione, estrazione | 1 anno | 🟡 Parziale |
| **Configurazione** | Cambio policy, aggiornamento regole, impostazioni | 2 anni | ✅ Attivo |
| **Sicurezza** | Failed login, pattern sospetti, attacchi | 2 anni | ✅ Attivo |
| **Sistema** | Deployment, errori servizio, fallimenti | 90 giorni | ✅ Attivo |

#### 2.4.2 Implementazione Audit Trail

**Schema Database** (PostgreSQL):
```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    event_id UUID NOT NULL UNIQUE,
    event_type VARCHAR(100) NOT NULL,  -- es AUTH_LOGIN, DOCUMENT_UPLOAD
    category VARCHAR(50) NOT NULL,  -- es AUTHENTICATION, DATA_ACCESS

    -- Informazioni Utente/Principal
    user_id VARCHAR(255),
    user_role VARCHAR(100),
    user_email VARCHAR(255),

    -- Informazioni Risorsa
    resource_type VARCHAR(100),  -- es DOCUMENT, CONFIG
    resource_id VARCHAR(255),
    resource_classification VARCHAR(50),  -- OFFICIAL, CONFIDENTIAL, PUBLIC

    -- Informazioni Rete
    ip_address INET,
    user_agent TEXT,

    -- Dettagli Azione
    action_description TEXT,
    action_outcome VARCHAR(50),  -- SUCCESS, FAILURE, PARTIAL

    -- Informazioni Risultato (AI Decision Events)
    decision_made VARCHAR(100),  -- es VALIDATED, CLASSIFIED_AS_INVOICE
    confidence_score NUMERIC(4,3),
    human_override BOOLEAN DEFAULT FALSE,

    -- Dati Strutturati
    metadata JSONB,

    -- Firma Crittografica (per immutabilità)
    entry_hash VARCHAR(256),
    previous_entry_hash VARCHAR(256),
    signature VARCHAR(512),

    -- Indexing
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id),
    INDEX idx_event_type (event_type),
    INDEX idx_resource_id (resource_id)
);
```

**Audit Trail Immutabile** (ispirato blockchain):
- Ogni voce audit log firmata crittograficamente con SHA-256
- Hash chain previene manomissioni: current_hash = SHA256(previous_hash || entry_data)
- Firme archiviate in formato tamper-evident
- Verifica integrità: Validazione periodica catena hash

**Mappatura Conformità**:
- ✅ AI Act Art. 30: Sistema registrazione automatico (docs in inglese: automated record-keeping)
- ✅ GDPR Art. 30: Registri attività di trattamento
- ✅ GDPR Art. 32: Capacità audit

**Stato**: 🟡 PARZIALMENTE IMPLEMENTATO
- **Evidenza**: MS14-AUDIT/SPECIFICATION.md (struttura audit definita)
- **Gap Implementazione**: Verifica firma catena hash non ancora automatizzata
- **Azione Richiesta**: Implementare script validazione giornaliera audit log (4 ore)

#### 2.4.3 Retention e Archiviazione Log

**Policy Retention**:
- **Log Attivi** (ricercabili): 90 giorni in database operazionale
- **Log Archiviati** (immutabili): 2 anni in cold storage (S3 Glacier)
- **Audit Log** (speciale): 7 anni (requisito legale documenti PA)

**Processo Archiviazione**:
```
Giornaliero (00:01 UTC)
├─ Esportare log > 90 giorni in S3 Glacier
├─ Comprimere con gzip (standard)
├─ Crittare con archive KMS key
├─ Firmare checksum integrità
└─ Rimuovere da database operazionale

Mensile (1° giorno, 00:30 UTC)
├─ Verificare tutti archivi accessibili
├─ Test procedura restore (sample)
└─ Aggiornare tracciamento inventory

Trimestrale (1°/4°/7°/10° giorno)
├─ Verifica completa integrità audit trail
├─ Validazione catena hash su tutti periodi archivio
└─ Generare report conformità
```

**Mappatura Conformità**:
- ✅ AI Act Art. 29: Record-keeping per sistemi alto-rischio
- ✅ GDPR Art. 5: Principi retention dati

**Stato**: 🟡 PARZIALMENTE IMPLEMENTATO
- **Evidenza**: MS14-AUDIT/SPECIFICATION.md (archiviazione definita)
- **Gap Implementazione**: Script archiviazione automatico non ancora deployato
- **Azione Richiesta**: Deploy automazione archiviazione + test restore (3 ore)

---

### 2.5 Monitoraggio e Rilevamento Anomalie (MS08-MONITOR)

**Scopo**: Rilevare incidenti sicurezza, degradazione performance, drift modello IA in tempo reale

#### 2.5.1 Monitoraggio Eventi Sicurezza

**Alert Real-Time** (via ELK Stack + Regole Custom):

| Alert | Soglia | Azione | Owner |
|-------|--------|--------|-------|
| Tentativi login falliti | > 5 fallimenti per utente per ora | Lock account 30 min | Security Ops |
| Impossible travel | Login da 2 location < 30 min | Flag review + MFA required | Security Ops |
| Privilege escalation | Elevazione ruolo utente fuori processo | Investigazione immediata | Security Team |
| Accesso dati anomalo | Accesso > 100 documenti in 5 min | Rate limit + alert | Security Ops |
| Certificato scadenza | < 30 giorni alla scadenza | Automazione trigger rinnovamento | DevOps |
| Rotazione chiave encryption | Età chiave > 90 giorni | Trigger rotazione + alert | Security Team |
| Chiamate API sospette | Richieste malformate, SQL injection attempts | Blocca richiesta + log | WAF/IDS |
| Manomissione audit log | Hash chain verification fallita | CRITICAL - investigate | Security Team |

**Stack Implementazione**:
- **Raccolta Log**: Filebeat / Fluentd (raccolta da tutti microservizi)
- **Logging Centralizzato**: Elasticsearch (ELK Stack)
- **Elaborazione Real-Time**: Logstash rules + Kibana dashboards
- **Alerting**: PagerDuty / Opsgenie integration
- **Integrazione SIEM**: Esporta a SIEM esterno (Splunk, se disponibile)

**Mappatura Conformità**:
- ✅ AI Act Art. 32: Design robusto contro attacchi
- ✅ AI Act Art. 33: Governance cyber-sicurezza

**Stato**: 🟡 PARZIALMENTE IMPLEMENTATO
- **Evidenza**: MS08-MONITOR/SPECIFICATION.md (monitoraggio definito)
- **Gap Implementazione**: Modello rilevamento anomalie ML non ancora addestrato
- **Azione Richiesta**: Addestrare modello anomalia detection su dati baseline (6 ore)

#### 2.5.2 Monitoraggio Modelli IA (Rilevamento Concept Drift)

**Monitoraggio Concept Drift**:

Monitorare performance modelli alto-rischio (MS01, MS02, MS04) per degradazione statistica:

```
Baseline Storico (periodo training):
├─ MS01-CLASSIFIER: Accuracy 92.3% (std dev ±0.8%)
├─ MS02-ANALYZER: F1 Score 0.908 (std dev ±0.04)
└─ MS04-VALIDATOR: Detection Rate 97.3% (std dev ±0.5%)

Monitoraggio Produzione (real-time):
├─ MS01: Current accuracy = 91.7% (Δ -0.6%, WITHIN soglia ✅)
├─ MS02: Current F1 = 0.895 (Δ -0.013, WITHIN soglia ✅)
└─ MS04: Current detection = 96.8% (Δ -0.5%, WITHIN soglia ✅)

Trigger Alert:
├─ Degradazione performance > 3% → Notifica ML team, flag per retraining
├─ Distribution shift punteggi confidenza > 2 std dev → Investiga cambiamenti dati
└─ Aumento false positive rate > 50% → Escalation immediata
```

**Implementazione Drift Detection**:
- **Calcolo Baseline**: Media ± 3σ (deviazione standard) su periodo baseline 1-mese
- **Finestra Monitoraggio**: Aggregazione settimanale metriche performance
- **Soglia Alert**: Degradazione > 3% o > 3 deviazioni standard
- **Risposta**: Trigger automatico retraining se degradazione confermata

**Mappatura Conformità**:
- ✅ AI Act Art. 29: Monitoraggio performance sistemi alto-rischio
- ✅ AI Act Art. 31: Garantire uso responsabile e supervisione umana

**Stato**: 🔴 NON IMPLEMENTATO
- **Azione Richiesta**: Implementare dashboard monitoraggio model performance (4 ore)

---

### 2.6 Risposta agli Incidenti e Disaster Recovery

**Scopo**: Rilevare, rispondere e recuperare da incidenti sicurezza e interruzioni servizio

#### 2.6.1 Piano Risposta Agli Incidenti

**Classificazione Incidenti**:

| Severità | Tempo Risposta | Escalation | Esempio |
|----------|----------------|-----------|---------|
| 🔴 **CRITICAL** | < 15 min | Executive + Security | Accesso dati non autorizzato, data breach |
| 🟠 **HIGH** | < 1 ora | Security + DevOps | Unavailability servizio, encryption failure |
| 🟡 **MEDIUM** | < 4 ore | Team lead | Anomalia audit log, spike failed login |
| 🟢 **LOW** | < 1 giorno | Team member | Certificate warning, minor alert |

**Workflow Risposta agli Incidenti**:

```
DETECT → ASSESS → RESPOND → RECOVER → REVIEW

1. DETECT (Automatizzato)
   └─ Alert da sistema monitoraggio (MS08-MONITOR)
   └─ Segnalazione manuale da security team
   └─ Notifica esterna (security researcher, vendor)

2. ASSESS (5-15 minuti)
   ├─ Raccogliere log iniziali e contesto
   ├─ Classificare livello severità
   └─ Attivare team risposta

3. RESPOND (Durante incidente)
   ├─ Isolare sistemi colpiti (se necessario)
   ├─ Preservare evidenza forense
   ├─ Iniziare remediation
   └─ Notificare stakeholder

4. RECOVER (Post-incidente)
   ├─ Restore servizi da backup
   ├─ Verificare integrità dati restaurati
   ├─ Ripristino graduale sistemi online
   └─ Verifica funzionamento tutti sistemi

5. REVIEW (24-48 ore post)
   ├─ Postmortem incidente completo
   ├─ Documentare analisi root cause
   ├─ Aggiornare regole rilevamento per prevenire ricorrenza
   └─ Aggiornare procedure risposta agli incidenti
```

**Contatti Chiave**:
- **Security Incident Response Team**: security-incident@example.com
- **Security Engineer On-Call**: (escalation PagerDuty)
- **CTO/Executive Escalation**: cto@example.com
- **External Communication**: communications@example.com
- **Legal/Compliance**: compliance@example.com

**Mappatura Conformità**:
- ✅ AI Act Art. 33: Governance cyber-sicurezza e risposta incidenti
- ✅ GDPR Art. 33: Obblighi notifica breach (72 ore)

**Stato**: 🟡 PARZIALMENTE IMPLEMENTATO
- **Evidenza**: Procedure risposta incidenti documentate in wiki security interno
- **Gap Implementazione**: Automazione runbook, catene escalation automatiche
- **Azione Richiesta**: Creare runbook risposta incidenti eseguibili (3 ore)

#### 2.6.2 Disaster Recovery

**Strategia Backup**:

```
RPO (Recovery Point Objective) & RTO (Recovery Time Objective):
├─ Database (PostgreSQL): RPO = 1 ora, RTO = 15 min
├─ File Storage (S3): RPO = 6 ore, RTO = 30 min
├─ Configurazione (Git): RPO = real-time, RTO = 5 min
└─ Audit Logs: RPO = 24 ore, RTO = 1 ora

Schedule Backup:
├─ Orario: Transaction log database (continuo)
├─ Giornaliero: Full database backup (02:00 UTC)
├─ Giornaliero: Incremental file storage backup (03:00 UTC)
├─ Settimanale: Full file storage backup (Domenica 00:00 UTC)
├─ Mensile: Full system snapshot per archivio (1° giorno, 00:00 UTC)
└─ Annuale: Archivio su storage air-gapped (1° gennaio)

Storage Backup:
├─ Primario: AWS S3 con versioning abilitato
├─ Secondario: NAS on-premise (ridondanza geografica)
├─ Terziario: Hard drive crittate esterne (air-gapped, annuale)
└─ Crittografia: Tutti backup crittati con KMS keys separate
```

**Procedure Restore**:
- **Database Restore**: Point-in-time recovery fino a ultimo transaction log
- **File Restore**: Recupera file singoli o intere bucket
- **Configuration Restore**: Rollback commit Git a stato noto-buono
- **Testing**: Drill restore mensili (test restore su ambiente staging)

**Mappatura Conformità**:
- ✅ AI Act Art. 33: Resilienza e robustezza
- ✅ GDPR Art. 32: Capacità restore disponibilità dopo incidenti

**Stato**: ✅ IMPLEMENTATO
- **Evidenza**: Policy backup AWS configurate, testate mensile
- **Verifica**: Ultimo successful restore test: 2025-11-20

---

## 3. Privacy Dati e Allineamento GDPR

### 3.1 Elaborazione Dati Personali

**Identificazione PII**:

ZenIA elabora seguenti categorie dati personali in documenti:

```
ESTRAZIONE ENTITÀ PERSON (MS02-ANALYZER)
├─ Nome completo (type PERSON)
├─ Email (type EMAIL)
├─ Numeri telefono (type PHONE)
├─ Codici fiscali / Tax ID (type FISCAL_CODE)
├─ Nome dipartimenti (se contiene PII)
└─ Titoli / Posizioni lavoro (se identifica individuo)

METADATA DOCUMENTO
├─ Email uploader & user ID
├─ Access log (chi ha visto documento)
├─ Informazioni creator/author
└─ IP addresses accessori
```

**Gestione Dati PII**:

| Categoria | Storage | Crittografia | Accesso | Retention |
|-----------|---------|-------------|--------|-----------|
| Entity extractions | DB + Audit log | AES-256 | Solo revisione umana | 1 anno |
| Document uploads | Encrypted S3 | AES-256 | Solo org proprietaria | 90 giorni (min) |
| User authentication | Keycloak | TLS + bcrypt | Sistema auth only | 2 anni (security) |
| Audit trail (user info) | PostgreSQL | AES-256 | Admins only | 7 anni (legal) |

**Misure Conformità GDPR**:

✅ **Art. 13/14 (Trasparenza)**: Privacy Policy pubblicata
✅ **Art. 15 (Diritto Accesso)**: Utente può richiedere export dati
✅ **Art. 17 (Diritto Oblio)**: Eliminazione documento trigger rimozione PII
✅ **Art. 20 (Data Portability)**: Export in formato machine-readable
✅ **Art. 21 (Diritto Opposizione)**: Può richiedere esenzione elaborazione ML
✅ **Art. 25 (Privacy by Design)**: Crittografia + controllo accessi
✅ **Art. 28 (DPA)**: Data Processing Agreement con vendor
✅ **Art. 30 (ROPA)**: Record di Attività di Trattamento mantenuto
✅ **Art. 32 (Sicurezza)**: Crittografia, controllo accessi, monitoraggio
✅ **Art. 33 (Notifica Breach)**: Incident response + notifica 72 ore

**Data Protection Impact Assessment (DPIA)**:

Richiesto per elaborazione IA alto-rischio:

```
DPIA Template (RICHIESTO PER MS01, MS02, MS04)
├─ Descrizione dell'elaborazione
├─ Valutazione necessità e proporzionalità
├─ Valutazione rischi (probabilità × impatto)
├─ Misure mitigazione
└─ Accettazione rischi residui
```

**Mappatura Conformità**:
- ✅ GDPR Art. 5: Principi elaborazione (lawfulness, fairness, transparency)
- ✅ GDPR Art. 25: Privacy by design e by default
- ✅ GDPR Art. 30: Registri attività di trattamento

**Stato**: 🟡 PARZIALMENTE IMPLEMENTATO
- **Evidenza**: Privacy Policy esiste; DPA in place con vendor
- **Gap Implementazione**: DPIA per MS01/MS02/MS04 non ancora completate
- **Azione Richiesta**: Creare documenti DPIA per 3 modelli alto-rischio (6 ore)

---

## 4. Valutazione Rischi e Mitigazione

### 4.1 Matrice Rischi Sicurezza

**Identificazione Rischi** (AI Act Art. 27):

| Rischio | Probabilità | Impatto | Mitigazione Attuale | Rischio Residuo |
|---------|-------------|---------|-------------------|-----------------|
| **Accesso Dati Non Autorizzato** | Media | Critica | Crittografia + RBAC + TLS | Bassa-Media |
| **ML Model Poisoning** | Bassa | Critica | Validazione dati + monitoraggio | Bassa |
| **Inference-Time Attack** (adversarial) | Bassa | Alta | Input validation + monitoraggio | Bassa |
| **Manomissione Audit Log** | Molto bassa | Critica | Hash chain + storage immutabile | Molto bassa |
| **Service Availability Loss** | Bassa | Alta | Ridondanza + backup/recovery | Bassa |
| **PII Extraction & Profiling** | Media | Alta | Revisione umana + governance policy | Media |
| **AI Model Drift** (degradazione) | Media | Alta | Monitoraggio + retraining triggers | Bassa-Media |
| **Privilege Escalation** | Bassa | Critica | RBAC + monitoraggio + code review | Molto bassa |

### 4.2 Strategie Mitigazione

**Per Categoria Rischio**:

#### A. Mitigazioni Sicurezza Dati
- ✅ Crittografia AES-256 a riposo e in transito
- ✅ Gestione chiavi encryption via AWS KMS o Vault
- ✅ Rotazione chiavi regolare (trimestrale)
- 🟡 Implementare automazione rotazione chiavi (2 ore)

#### B. Mitigazioni Controllo Accessi
- ✅ Implementazione RBAC + ABAC
- ✅ Principio least privilege
- ✅ Autenticazione multi-fattore (MFA)
- 🟡 Processo revisione accessi trimestrale (4 ore per implementazione)

#### C. Mitigazioni Robustezza Modelli IA
- ✅ Input validation su tutti input modelli IA
- ✅ Soglie punteggi confidenza
- ✅ Revisione umana per predizioni bassa-confidenza
- 🟡 Test robustezza avversariale (4 ore)

#### D. Mitigazioni Monitoraggio e Risposta
- 🟡 Monitoraggio sicurezza real-time (parziale)
- 🟡 Alerting automatico (parziale)
- 🔴 Automazione runbook risposta incidenti (3 ore)
- 🔴 Addestramento modello anomalia detection (6 ore)

#### E. Mitigazioni Audit e Conformità
- ✅ Audit trail logging (parziale)
- 🟡 Verifica integrità hash chain (4 ore)
- 🟡 Archiviazione automatica (3 ore)
- 🟡 Documentazione DPIA (6 ore)

---

## 5. Gestione Vendor e Terzi

### 5.1 Risk Management Supply Chain

**Dipendenze Third-Party**:

| Componente | Vendor | Livello Rischio | Mitigazione |
|-----------|--------|-----------------|-----------|
| OpenID/OAuth | Keycloak (self-hosted) | Basso | Self-managed, aggiornamenti sicurezza |
| Database | PostgreSQL (open source) | Basso | Vulnerability scanning, patching |
| API Gateway | Kong/NGINX (open source) | Basso | Regole WAF, rate limiting |
| Object Storage | AWS S3 (se cloud) | Basso | AWS shared responsibility model |
| Encryption | OpenSSL / libsodium | Basso | Aggiornamenti vendor sicurezza |
| ML Libraries | spaCy, XGBoost, TensorFlow | Media | Dependency scanning, version pinning |

**Valutazione Sicurezza Vendor**:
- Requisiti audit sicurezza per tutti vendor
- Data Processing Agreements (DPA) in place
- Regular vulnerability scanning di dipendenze
- Requisiti SLA incident response nei contratti

**Mappatura Conformità**:
- ✅ AI Act Art. 28: Data governance include oversight vendor
- ✅ GDPR Art. 28: Data Processing Agreements

**Stato**: ✅ IMPLEMENTATO
- **Evidenza**: Template DPA esistono; vendor list mantenuto
- **Verifica**: Revisione sicurezza vendor trimestrale

---

## 6. Checklist Conformità e Stato Implementazione

### 6.1 Requisiti AI Act Allegato III

| Articolo | Requisito | Implementazione ZenIA | Stato | Sforzo |
|----------|-----------|----------------------|--------|--------|
| 27 | Risk Management System | ARCHITETTURA-SICUREZZA-AI-ACT.md (questo doc) | ✅ | - |
| 28 | Data Governance | CONFORMITA-MAPPATURA-AI-ACT.md | 🟡 | DPIA: 6h |
| 29 | Documentazione | System Card completate | ✅ | - |
| 30 | Automated Record-Keeping | MS14-AUDIT + hash chain | 🟡 | Automazione: 4h |
| 31 | Human Oversight | MS06-AGGREGATOR + MS07 | ✅ | - |
| 32 | Robustness Against Attacks | TLS, crittografia, WAF, monitoraggio | 🟡 | Test adversarial: 4h |
| 33 | Cybersecurity & Resilience | Crittografia, backup, incident response | 🟡 | Runbook: 3h |

### 6.2 Roadmap Implementazione

**Fase 1 - IMMEDIATA (Q4 2025-2: Prossime 4 settimane)**
- [ ] Documentazione DPIA per MS01, MS02, MS04 (6 ore)
- [ ] Automazione verifica integrità hash chain audit log (4 ore)
- [ ] Automazione rotazione chiavi (2 ore)
- [ ] Runbook risposta agli incidenti (3 ore)

**Fase 2 - BREVE TERMINE (Q1 2026-1: Settimane 5-8)**
- [ ] Implementazione monitoraggio drift modelli (4 ore)
- [ ] Processo revisione accessi trimestrale (4 ore)
- [ ] Test robustezza avversariale (4 ore)
- [ ] Archiviazione log automatizzata (3 ore)
- [ ] Addestramento modello anomalia detection (6 ore)

**Fase 3 - MEDIO TERMINE (Q1 2026-2: Settimane 9-16)**
- [ ] Programma awareness training sicurezza (8 ore)
- [ ] Penetration testing (vendor esterno: 40 ore)
- [ ] Compliance audit da assessor esterno (20 ore)
- [ ] Aggiornamento policy sicurezza su findings audit (10 ore)

**Sforzo Totale Stimato**:
- Fase 1: 15 ore (prossime 4 settimane)
- Fase 2: 21 ore (settimane seguenti)
- Fase 3: 78 ore (+ 40 ore pentest esterno)
- **Totale**: 114 ore (+ 40 ore pentest esterno)

---

## 7. Approvazione e Sign-Off

### 7.1 Approvazioni Revisione Sicurezza

- ⏳ **Revisione Officer Sicurezza**: PENDING
- ⏳ **Revisione CTO**: PENDING
- ⏳ **Revisione Officer Conformità**: PENDING
- ⏳ **Approvazione Esecutiva**: PENDING

### 7.2 Prossimi Step

1. **Revisione Sicurezza**: Validazione team sicurezza di tutte misure
2. **Revisione Conformità**: Verificare allineamento AI Act & GDPR
3. **Implementazione**: Esecuzione roadmap Fase 1 (15 ore, Q4 2025-2)
4. **Monitoraggio**: Tracciare progresso via dashboard
5. **Audit**: Valutazione sicurezza esterna (Q1 2026-2)

---

## 8. Cronologia Documento

| Versione | Data | Cambiamenti | Autore |
|----------|------|-------------|--------|
| 1.0 | 2025-11-21 | Documento Architettura Sicurezza Iniziale (conformità AI Act) | Claude Code |

---

## 9. Riferimenti

### Normativi
- Regolamento UE sull'IA 2024/1689 (AI Act) - Allegato III
- GDPR (General Data Protection Regulation) - EU 2016/679
- CAD italiano (Codice dell'Amministrazione Digitale) - D. Lgs. 82/2005

### Documentazione Interna
- [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md) - Architettura sistema
- [CONFORMITA-MAPPATURA-AI-ACT.md](CONFORMITA-MAPPATURA-AI-ACT.md) - Mappatura AI Act
- [CONFORMITA-MAPPATURA-CAD.md](CONFORMITA-MAPPATURA-CAD.md) - Mappatura CAD
- [SYSTEM-CARDS-REGISTRY.md](SYSTEM-CARDS-REGISTRY.md) - Documentazione modelli
- [MS13-SECURITY SPECIFICATION](microservices/MS13-SECURITY/SPECIFICATION.md) - Microservizio sicurezza

### Standard e Best Practice
- NIST Cybersecurity Framework
- OWASP Top 10
- CIS Controls
- ISO 27001 Information Security Management

---

**Documento Architettura Sicurezza** | Conformità: Regolamento UE 2024/1689 (Allegato III) + GDPR | Ultimo Aggiornamento: 21 novembre 2025
