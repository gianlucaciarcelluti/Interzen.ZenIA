# 📋 Matrice di Conformità ZenIA vs CAD (D. Lgs. 82/2005)

**Data Creazione**: 21 novembre 2025
**Versione**: 1.0 - DRAFT
**Status**: IN PROGRESS
**Priorità**: 🔴 CRITICAL
**Sprint**: Q4 2025-1/2

---

## 📑 Indice

1. [Sommario Conformità](#sommario-conformità)
2. [Requisiti CAD per PA](#requisiti-cad-per-pa)
3. [Mappatura per Pilastro](#mappatura-per-pilastro)
4. [Gap Analysis](#gap-analysis)
5. [Azioni Correttive](#azioni-correttive)

---

## Sommario Conformità

### Status Generale: 🟠 PARZIALMENTE CONFORME (58% stima iniziale)

| Dimensione | Requisito CAD | Status | Effort |
|------------|---------------|--------|--------|
| **Accessibilità** | WCAG 2.1 AA compliance | 🟡 YELLOW | 25 ore |
| **Digital Preservation** | Conservazione digitale DPCM | 🟠 PARTIAL | 15 ore |
| **Digital Signature** | Firma digitale/autenticazione | ✅ PRESENT | 5 ore |
| **Data Protection** | GDPR compliance (CAD Art.3) | 🟠 PARTIAL | 20 ore |
| **Information Protocols** | Protocollazione informatica | 🟠 PARTIAL | 18 ore |
| **Document Management** | Gestione documenti digitali | ✅ GOOD | 0 ore |
| **Data Interoperability** | Interoperabilità dati | 🟠 PARTIAL | 12 ore |
| **Audit Trail** | Traccia di controllo/audit | ✅ PRESENT | 0 ore |

**Totale Effort Stimato**: ~95 ore (per raggiungere 100%)

---

## Requisiti CAD per PA

### 1. Accessibilità Digitale (CAD Art. 3-bis)

**Requisito**: Tutti i servizi digitali PA devono essere accessibili secondo WCAG 2.1 Level AA

#### Pillars of Accessibility

| WCAG Pillar | Requirement | ZenIA Status | Documentation |
|-------------|-------------|--------------|-----------------|
| **Perceivable** | Testi alternativi per immagini | 🟡 PARTIAL | [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md) |
| | Contrasto colori (4.5:1 for text) | ❌ NOT ASSESSED | Requires audit |
| | Audio/video captions | ❌ NOT APPLICABLE | No multimedia |
| **Operable** | Navigazione solo tastiera | 🟡 PARTIAL | Test required |
| | Focus order management | ❌ NOT ASSESSED | Requires audit |
| | No seizure risks | ✅ COMPLIANT | By design |
| **Understandable** | Linguaggio semplice | ✅ GOOD | [DOCUMENTATION-STRUCTURE-GUIDE.md](DOCUMENTATION-STRUCTURE-GUIDE.md) |
| | Consistent navigation | ✅ GOOD | [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md) |
| | Error prevention | 🟡 PARTIAL | MS04-VALIDATOR, MS06-AGGREGATOR |
| **Robust** | Valid markup | 🟡 PARTIAL | Requires WCAG validator |
| | Browser compatibility | ✅ GOOD | Multi-browser support |

**Status**: 🟡 YELLOW - Richiede formal accessibility audit (WAVE/Axe testing)

**Gap**: Manca accessibility audit formale e remediation plan.

---

### 2. Conservazione Digitale (CAD Art. 7)

**Requisito (DPCM 3/12/2013)**: Documenti digitali conservati per 30 anni con integrità garantita

#### Conservation Components

| Component | Implementation | ZenIA Status | Reference |
|-----------|-----------------|--------------|-----------|
| **Storage Medium** | Cloud storage (Azure/S3/Filesystem) | ✅ PRESENT | [ZENSHAREUP-ARCHITECTURE.md](ZENSHAREUP-ARCHITECTURE.md) |
| **Format Standardization** | PDF/A for long-term preservation | 🟠 PARTIAL | MS05-TRANSFORMER converts to PDF |
| **Metadata Preservation** | Document metadata tracking | ✅ GOOD | MS06-AGGREGATOR + MS14-AUDIT |
| **Integrity Verification** | Checksums (SHA-256) | ❌ MISSING | Requires implementation |
| **Audit Trail** | Complete audit log | ✅ PRESENT | [MS14-AUDIT](microservices/MS14-AUDIT/) |
| **Encryption at Rest** | TDE + Azure encryption | ✅ PRESENT | [MS13-SECURITY](microservices/MS13-SECURITY/SPECIFICATION.md) |
| **Lifecycle Management** | Retention policies | 🟡 PARTIAL | [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md) - needs detail |
| **Backup Strategy** | Geo-redundant backups | ✅ PRESENT | Cloud provider native |

**Status**: 🟠 PARTIAL - Infrastructure present, formal DPCM compliance documentation missing

**Gap**: Checksum verification system + formal DPCM compliance plan

---

### 3. Firma Digitale & Autenticazione (CAD Art. 8-20)

**Requisito**: Supporto a firma digitale qualificata (eIDAS 2014/910/EU)

#### Digital Signature Support

| Component | Implementation | Status | Reference |
|-----------|-----------------|--------|-----------|
| **Signature Verification** | eIDAS-compliant signature checking | ❌ NOT TESTED | To implement in MS13-SECURITY |
| **Certificate Validation** | X.509 certificate chain validation | ❌ MISSING | Requires implementation |
| **Timestamp Authority** | Trusted timestamp support | ❌ MISSING | Requires integration |
| **TSP Integration** | Time Stamp Provider integration | ❌ MISSING | Requires service |
| **Long-term Validation** | LTV signature support | ❌ MISSING | Advanced feature |

**Status**: 🔴 RED - Framework non implementato (ma non critico per documento processing)

**Note**: ZenIA riceve documenti firmati da SFTPGo/multifunzioni, ma non crea/verifica firme digitali in output. L'implementazione è responsabilità di ZenShareUp se richiesta.

---

### 4. GDPR Compliance (CAD Art. 3, integrated with GDPR)

**Requisito**: CAD integra GDPR requirements per data protection

#### Data Protection Elements

| Element | Requirement | Status | Reference |
|---------|-------------|--------|-----------|
| **Data Minimization** | Collect only necessary data | ✅ GOOD | MS07 distributes to ZenShareUp |
| **Purpose Limitation** | Clear use restrictions | 🟡 PARTIAL | [ZENSHAREUP-ZENIA-INTEGRATION.md](ZENSHAREUP-ZENIA-INTEGRATION.md) |
| **Consent Management** | Document user consent | ❌ MISSING | Requires consent layer |
| **Data Subject Rights** | Right to access, erasure, portability | 🟠 PARTIAL | [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md) |
| **Privacy by Design** | PbD principles in architecture | 🟠 PARTIAL | MS13-SECURITY, MS07 |
| **DPIA Requirements** | Data Protection Impact Assessment | ❌ MISSING | Requires assessment |
| **Breach Notification** | 72-hour breach reporting | ❌ MISSING | Requires incident response |
| **Data Retention** | Clear retention periods | 🟡 PARTIAL | Needs documentation |

**Status**: 🟠 PARTIAL - GDPR mapping incomplete

**Gap**: DPIA, consent management, breach notification procedures

---

### 5. Protocollazione Informatica (CAD Art. 40-45)

**Requisito**: Registro di protocollo informatico per documenti in ingresso/uscita

#### Protocolling Elements

| Element | Implementation | Status | Reference |
|---------|-----------------|--------|-----------|
| **Protocol Registration** | Each document registered with unique ID | ✅ PRESENT | MS06-AGGREGATOR assigns IDs |
| **Timestamp Recording** | Accurate time recording | ✅ PRESENT | MS14-AUDIT logs timestamps |
| **Metadata Recording** | Document metadata captured | ✅ GOOD | DATABASE-SCHEMA per MS |
| **Sender/Recipient Tracking** | Track origin/destination | ✅ PRESENT | MS01 (origin), MS07 (destination) |
| **Digital Signature of Registry** | Sign protocol register entries | ❌ MISSING | Advanced feature |
| **Immutability** | Registry entries cannot be altered | 🟡 PARTIAL | Audit log present, immutability not guaranteed |
| **Backup & Recovery** | Protocol registry backed up | ✅ PRESENT | Cloud backup |

**Status**: ✅ GOOD - Basic protocolling implemented, advanced features missing

---

### 6. Document Management (CAD Art. 20-25)

**Requisito**: Gestione sistematica di documenti digitali

#### Document Management Features

| Feature | Implementation | Status | Reference |
|---------|-----------------|--------|-----------|
| **Classification** | Document type classification | ✅ EXCELLENT | MS01-CLASSIFIER |
| **Metadata Management** | Full metadata tagging | ✅ GOOD | All MSxx DATABASE-SCHEMA |
| **Versioning** | Track document versions | ✅ PRESENT | MS05 handles versioning |
| **Searchability** | Full-text search capability | 🟡 PARTIAL | MS02 extracts text, search index missing |
| **Accessibility** | Easy document access | ✅ GOOD | Via MS07-DISTRIBUTOR APIs |
| **Retention Schedules** | Automated retention management | 🟡 PARTIAL | Manual currently |

**Status**: ✅ GOOD - Core DMS functionality present

---

### 7. Data Interoperability (CAD Art. 50-51)

**Requisito**: Interoperabilità con altri sistemi PA (ANPR, etc.)

#### Interoperability Components

| Component | Implementation | Status | Reference |
|-----------|-----------------|--------|-----------|
| **API Standards** | OpenAPI 3.0 compliance | 🟡 PARTIAL | [API.md](microservices/MSxx/API.md) exists, needs formal validation |
| **Data Format Standards** | XML, JSON standardization | ✅ GOOD | [ZENSHAREUP-ZENIA-INTEGRATION.md](ZENSHAREUP-ZENIA-INTEGRATION.md) |
| **ANPR Integration** | ANPR directory integration | ❌ MISSING | Requires implementation |
| **Service Discovery** | Service registry capability | 🟡 PARTIAL | MS15-REGISTRY present |
| **Error Handling** | Standardized error responses | 🟡 PARTIAL | Needs standardization |
| **Logging/Auditing** | Standardized audit logs | ✅ GOOD | MS14-AUDIT |

**Status**: 🟠 PARTIAL - Basic interoperability present, ANPR integration missing

---

## Mappatura per Pilastro

### Pilastro 1: Accessibilità (Art. 3-bis)

**Owner**: QA Lead + Frontend Team
**Sprint**: Q1 2026-1
**Effort**: 25 ore

#### Subtasks

1. **A-1.1: Accessibility Audit** (8 ore)
   - Tools: WAVE, Axe DevTools, NVDA screen reader
   - Output: docs/ACCESSIBILITY-AUDIT-REPORT.md
   - Target: Identify all WCAG 2.1 AA violations

2. **A-1.2: WCAG 2.1 AA Remediation** (15 ore)
   - Fix contrast ratios
   - Implement keyboard navigation
   - Add alt texts to diagrams
   - Ensure focus management
   - Output: Updated documentation + code fixes

3. **A-1.3: Accessibility Statement** (2 ore)
   - Create formal accessibility statement
   - Reference WCAG conformance
   - Provide contact for accessibility issues

---

### Pilastro 2: Conservazione Digitale (Art. 7)

**Owner**: DevOps Lead + Compliance Officer
**Sprint**: Q4 2025-2 / Q1 2026-1
**Effort**: 20 ore

#### Subtasks

1. **C-2.1: DPCM Compliance Mapping** (8 ore)
   - Map DPCM 3/12/2013 requirements to ZenShareUp storage
   - Document PDF/A conversion process
   - Output: docs/DIGITAL-PRESERVATION-PLAN.md

2. **C-2.2: Checksum Verification System** (10 ore)
   - Implement SHA-256 checksums for all stored documents
   - Periodic verification job
   - Corruption detection & alerting

3. **C-2.3: Retention Policy Implementation** (2 ore)
   - Define retention schedules per document type
   - Automatic purge process

---

### Pilastro 3: Firma Digitale (Art. 8-20)

**Owner**: Security Architect
**Sprint**: Q2 2026 (deferred, lower priority)
**Effort**: 30 ore

**Note**: Non critico per ZenIA (input processing), ma importante per interoperabilità.

#### Subtasks

1. **S-3.1: eIDAS Certificate Validation** (15 ore)
   - Implement X.509 chain validation
   - CRL/OCSP checking
   - Timestamp validation

2. **S-3.2: TSP Integration** (15 ore)
   - Integrate with Trusted Timestamp Provider
   - Long-term validation support

---

### Pilastro 4: GDPR Compliance (Art. 3)

**Owner**: Data Protection Officer (DPO)
**Sprint**: Q4 2025-2 / Q1 2026-1
**Effort**: 35 ore

#### Subtasks

1. **P-4.1: DPIA - Data Protection Impact Assessment** (10 ore)
   - Document data flows through ZenIA
   - Identify risks
   - Mitigation measures
   - Output: docs/DPIA-ZENIA.md

2. **P-4.2: Consent Management** (8 ore)
   - Document consent flows
   - User consent tracking
   - Consent withdrawal mechanism

3. **P-4.3: Data Rights Implementation** (10 ore)
   - Right to access: Query mechanism
   - Right to erasure: Purge system
   - Right to portability: Export functionality
   - Implementation guide

4. **P-4.4: Breach Response Plan** (7 ore)
   - Incident detection
   - 72-hour notification procedure
   - Documentation template

---

### Pilastro 5: Protocollazione (Art. 40-45)

**Owner**: Business Analyst + Architect
**Sprint**: Q4 2025-2
**Effort**: 15 ore

#### Subtasks

1. **PR-5.1: Protocol Registry Documentation** (8 ore)
   - Document MS06-AGGREGATOR as protocol registry
   - Formalize timestamp recording
   - Output: docs/PROTOCOL-REGISTRY-SPECIFICATION.md

2. **PR-5.2: Immutability Guarantee** (7 ore)
   - Implement append-only log system
   - Cryptographic seal for registry entries
   - Validation on access

---

### Pilastro 6: Document Management (Art. 20-25)

**Owner**: Information Architect
**Sprint**: Ongoing (already mostly done)
**Effort**: 5 ore

#### Subtasks

1. **DM-6.1: Full-Text Search Index** (5 ore)
   - Add Elasticsearch integration
   - Index MS02 extracted content
   - Search API development

---

### Pilastro 7: Interoperabilità (Art. 50-51)

**Owner**: Integration Architect
**Sprint**: Q1 2026-1 / Q2 2026
**Effort**: 30 ore

#### Subtasks

1. **I-7.1: OpenAPI 3.0 Validation** (8 ore)
   - Validate all [MSxx/API.md](microservices/MSxx/API.md) against OpenAPI spec
   - Generate OpenAPI schemas from code
   - Output: openapi.yaml for all services

2. **I-7.2: ANPR Integration** (15 ore)
   - Research ANPR API requirements
   - Implement ANPR data lookups
   - Error handling for ANPR unavailability

3. **I-7.3: Service Discovery** (7 ore)
   - Document MS15-REGISTRY functionality
   - Service registration/deregistration
   - Health check endpoints

---

## Gap Analysis

### Critical Gaps (🔴 RED)

| Gap | Impact | Component | Effort | Sprint |
|-----|--------|-----------|--------|--------|
| Accessibility Audit | WCAG 2.1 violation risk | UI/Docs | 8 hrs | Q1 2026-1 |
| DPIA (GDPR Impact Assessment) | Privacy risk | Data flow | 10 hrs | Q4 2025-2 |
| Breach Notification Procedure | Non-compliance risk | Security | 7 hrs | Q4 2025-2 |
| Checksum Verification | Digital preservation failure | Storage | 10 hrs | Q1 2026-1 |
| eIDAS Certificate Validation | Digital signature rejection | Security | 15 hrs | Q2 2026 |

### Medium Priority Gaps (🟠 ORANGE)

| Gap | Impact | Effort | Sprint |
|-----|--------|--------|--------|
| Consent Management System | GDPR data rights | 8 hrs | Q1 2026-1 |
| Data Rights Tools (access/erasure/portability) | GDPR compliance | 10 hrs | Q1 2026-1 |
| ANPR Integration | Interoperability | 15 hrs | Q1 2026-1 |
| Full-Text Search Index | Discoverability | 5 hrs | Q4 2025-2 |

### Low Priority Gaps (🟡 YELLOW)

| Gap | Impact | Effort | Sprint |
|-----|--------|--------|--------|
| OpenAPI Schema Formal Validation | Standards compliance | 8 hrs | Q1 2026-1 |
| Digital Signature Support (TSP) | Advanced feature | 15 hrs | Q2 2026 |
| Immutability Guarantee for Registry | Advanced security | 7 hrs | Q4 2025-2 |

---

## Azioni Correttive Immediate (Q4 2025-2)

### Settimana 5-6: GDPR & Protocollazione

- **D-4.1**: Completare DPIA ZenIA → 10 ore
- **D-4.2**: Documenti GDPR data flow → 5 ore
- **D-4.3**: Breach notification procedure → 7 ore
- **PR-5.1**: Protocol registry specification → 8 ore

**Totale Q4 2025-2**: 30 ore

### Q1 2026-1: Accessibilità & Interoperabilità

- **A-1.1**: Accessibility audit → 8 ore
- **A-1.2**: WCAG 2.1 remediation → 15 ore
- **I-7.1**: OpenAPI validation → 8 ore
- **I-7.2**: ANPR integration → 15 ore

**Totale Q1 2026-1**: 46 ore

---

## Evidence Collection per CAD

1. **Documentazione Accessibilità** → docs/ACCESSIBILITY-AUDIT-REPORT.md + ACCESSIBILITY-STATEMENT.md
2. **Piano Conservazione Digitale** → docs/DIGITAL-PRESERVATION-PLAN.md
3. **DPIA** → docs/DPIA-ZENIA.md
4. **Protocollo Informatico** → docs/PROTOCOL-REGISTRY-SPECIFICATION.md
5. **Audit Log** → MS14-AUDIT implementation + sample logs
6. **Retention Policy** → docs/DATA-RETENTION-POLICY.md

---

## Cross-References

- **D-2**: System Cards per ML models (AI Act requirement)
- **D-3**: Architettura Security
- **D-4**: GDPR + CAD Audit Trail (più dettagliato)
- **A-3**: WCAG 2.1 accessibility testing
- **T-4**: Accessibilità testing automation

---

*Generato come parte del backlog task D-1: Mappatura Completa Normative ZenIA*
