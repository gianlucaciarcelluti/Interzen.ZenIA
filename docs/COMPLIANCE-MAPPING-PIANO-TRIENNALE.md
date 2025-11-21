# 📋 Matrice di Conformità ZenIA vs Piano Triennale AgID 2024-2026

**Data Creazione**: 21 novembre 2025
**Versione**: 1.0 - DRAFT
**Status**: IN PROGRESS
**Priorità**: 🔴 P0 CRITICAL (Mandatory per PA)
**Sprint**: Q4 2025-2 / Q1 2026

---

## 📑 Indice

1. [Sommario Conformità](#sommario-conformità)
2. [Linee Strategiche AgID](#linee-strategiche-agid)
3. [Mappatura ZenIA](#mappatura-zenia)
4. [Gap Analysis](#gap-analysis)
5. [Azioni Correttive](#azioni-correttive)

---

## Sommario Conformità

### Status Generale: 🟠 PARZIALMENTE CONFORME (72% stima iniziale)

| Dimensione | Requisito Piano Triennale | Status | Effort |
|------------|---------------------------|--------|--------|
| **PaaSPA Compliance** | Compliance con modello Platform-as-a-Service | 🟡 YELLOW | 5 ore |
| **Centralizzazione Infrastrutture** | Migrazione a Poli Strategici Nazionali | ✅ GOOD | 0 ore |
| **ANPR Integration** | Integrazione servizi ANPR | ❌ MISSING | 15 ore |
| **Monitoring AgID** | Conformità piattaforma monitoraggio AgID | 🟡 PARTIAL | 8 ore |
| **API Portal** | Registrazione su API Gateway nazionale | ❌ MISSING | 10 ore |
| **Accessibility** | WCAG 2.1 AA compliance | 🟡 PARTIAL | 25 ore |
| **Modernizzazione Legacy** | Aggiornamento sistemi (non applicabile) | ✅ GOOD | - |
| **DevOps & CI/CD** | Pipeline moderne (DevOps culture) | ✅ GOOD | 0 ore |

**Totale Effort Stimato**: ~63 ore

---

## Linee Strategiche AgID

### Contesto: Piano Triennale per l'Informatica nella PA 2024-2026

Il Piano Triennale AgID definisce 5 pilastri strategici:
1. **PaaSPA** - Centralizzazione infrastrutture
2. **ANPR** - Anagrafe nazionale della popolazione
3. **Piattaforme Digitali** - Servizi transazionali
4. **Dati e Interoperabilità** - Open data e API
5. **Cybersecurity** - Difesa cibernetica nazionale

ZenIA rientra principalmente nei pilastri 1, 2, 4, 5.

---

## Pilastri del Piano Triennale

### Pilastro 1: PaaSPA (Platform-as-a-Service PA)

**Requisito**: Tutti i nuovi servizi PA devono funzionare su PaaSPA

#### PaaSPA Components

| Component | Requirement | Status | Implementation |
|-----------|-------------|--------|-----------------|
| **Container Orchestration** | Kubernetes-based deployment | ✅ GOOD | Cloud-native via Azure |
| **Service Mesh** | Istio or similar | 🟡 PARTIAL | Azure Service Fabric alternative |
| **Infrastructure as Code** | IaC with Terraform/Ansible | ✅ GOOD | [DEVELOPMENT-GUIDE.md](docs/DEVELOPMENT-GUIDE.md) |
| **Logging & Monitoring** | Centralized logging (ELK/Splunk) | ✅ GOOD | [MS08-MONITOR](docs/microservices/MS08-MONITOR/), [MS11-GATEWAY](docs/microservices/MS11-GATEWAY/) |
| **API Gateway** | Centralized API gateway | ✅ GOOD | [MS15-REGISTRY](docs/microservices/MS15-REGISTRY/) + MS11-GATEWAY |
| **Authentication/Authorization** | OAuth 2.0 / OpenID Connect | ✅ GOOD | [MS13-SECURITY](docs/microservices/MS13-SECURITY/) |
| **Secrets Management** | Azure Key Vault integration | ✅ GOOD | MS13-SECURITY |
| **Backup & Disaster Recovery** | Automated backups + failover | ✅ GOOD | Cloud provider native |

**Status**: ✅ GOOD - ZenIA is cloud-native and PaaSPA-compatible

**Note**: ZenIA è già deployata su Azure che è conforme a PaaSPA standard.

---

### Pilastro 2: ANPR (Anagrafe Nazionale della Popolazione)

**Requisito**: Integrazione con ANPR per dati anagrafici cittadini

#### ANPR Integration Points

| Integration | Requirement | Current | Target |
|-------------|-------------|---------|--------|
| **Person Lookup** | Query ANPR for person data | ❌ NOT IMPLEMENTED | MS02-ANALYZER should enrich entities |
| **Residency Verification** | Verify residency of extracted persons | ❌ NOT IMPLEMENTED | Optional feature |
| **Death Certificate Notification** | Handle deceased person data | ❌ NOT IMPLEMENTED | Optional |
| **Address Updates** | Sync address changes from ANPR | ❌ NOT IMPLEMENTED | Future scope |
| **Service Notifications** | Push notifications via ANPR | ❌ NOT IMPLEMENTED | Future scope |

**Status**: 🔴 RED - No ANPR integration currently

**Gap**: ANPR API integration module needed

**Priority**: Medium (Optional feature, not critical for MVP)

---

### Pilastro 3: Piattaforme Digitali Nazionali

**Requisito**: Integrazione con piattaforme PA (PAGOPA, ANPR, etc.)

#### Platform Integrations

| Platform | Requirement | Status | Detail |
|----------|-------------|--------|--------|
| **PAGOPA** | Payment gateway for subscription | ❌ NOT APPLICABLE | Document processing, not payment |
| **Notifiche.it** | Digital notifications | ❌ NOT IMPLEMENTED | Could notify PA of document status |
| **CIE (Carta ID)** | eID support | 🟡 PARTIAL | MS13-SECURITY supports mTLS |
| **SPID (SAML)** | SAML 2.0 SPID federations | ❌ NOT IMPLEMENTED | Could be authentication method |
| **eIDAS** | Digital signatures | ❌ NOT IMPLEMENTED | Input documents may have eIDAS signatures |

**Status**: 🟡 PARTIAL - Infrastructure compatible, integrations optional

---

### Pilastro 4: Dati e Interoperabilità

**Requisito**: Dati aperti (open data), interoperabilità, API standard

#### Data & Interoperability Requirements

| Component | Requirement | Status | Reference |
|-----------|-------------|--------|-----------|
| **Open Data Catalog** | Register in national CKAN catalog | ❌ MISSING | [COMPLIANCE-MAPPING-PNRR.md](docs/COMPLIANCE-MAPPING-PNRR.md#pilastro-3-open-data--trasparenza) |
| **DCAT-AP Metadata** | Metadata in DCAT-AP 2.0.1 format | ❌ MISSING | Identical to PNRR requirement |
| **API Standards** | OpenAPI 3.0 compliance | 🟡 PARTIAL | [COMPLIANCE-MAPPING-PNRR.md](docs/COMPLIANCE-MAPPING-PNRR.md#pilastro-2-interoperabilità--openapi) |
| **Data Format Standards** | JSON, XML with schema validation | ✅ GOOD | [ZENSHAREUP-ZENIA-INTEGRATION.md](docs/ZENSHAREUP-ZENIA-INTEGRATION.md) |
| **Linked Data** | JSON-LD support for semantic web | ❌ MISSING | Future enhancement |
| **Service Discovery** | Service registry (UDDI/similar) | 🟡 PARTIAL | [MS15-REGISTRY](docs/microservices/MS15-REGISTRY/) |

**Status**: 🟡 PARTIAL - Basic interoperability present, open data publishing missing

---

### Pilastro 5: Cybersecurity

**Requisito**: Difesa cibernetica, Zero Trust architecture, incident response

#### Cybersecurity Components

| Component | Requirement | Status | Reference |
|-----------|-------------|--------|-----------|
| **Zero Trust Architecture** | Assume breach mentality | ✅ GOOD | [ARCHITECTURE-OVERVIEW.md](docs/ARCHITECTURE-OVERVIEW.md#security-architecture) |
| **Encryption** | End-to-end encryption | ✅ GOOD | [MS13-SECURITY](docs/microservices/MS13-SECURITY/) |
| **Vulnerability Management** | Regular scanning + patching | 🟡 PARTIAL | CI/CD integration needed |
| **Incident Response** | 24/7 incident response | ✅ GOOD | On-call rotation |
| **DDoS Protection** | DDoS mitigation | ✅ GOOD | Cloud provider (Azure DDoS Protection) |
| **Penetration Testing** | Annual pentest + red team | 🟡 PARTIAL | Needs formalization |
| **Threat Intelligence** | Share threat data with CNAIPIC | ❌ MISSING | Advanced feature |
| **Compliance Audit** | Regular security audits | 🟡 PARTIAL | Annual audit needed |

**Status**: ✅ GOOD - Security posture strong

---

## Mappatura ZenIA

### Compliance Matrix

| Pilastro | Component | Status | Score | Action |
|----------|-----------|--------|-------|--------|
| **PaaSPA** | Cloud-native architecture | ✅ GOOD | 95% | Documentation update |
| **ANPR** | ANPR integration | ❌ MISSING | 0% | New feature (low priority) |
| **Piattaforme** | PAGOPA/eIDAS/SPID support | ❌ MISSING | 10% | Infrastructure ready, not integrated |
| **Dati** | Open data catalog | ❌ MISSING | 0% | Critical gap |
| **Dati** | OpenAPI compliance | 🟡 PARTIAL | 60% | Documentation completion |
| **Cybersecurity** | Zero Trust + encryption | ✅ GOOD | 90% | Documentation completion |

**Overall Score**: 72% (Partial Compliance)

---

### PaaSPA Compliance Detail

**Status**: ✅ EXCELLENT - Fully compliant

```
ZenIA Architecture vs PaaSPA Requirements:

✅ Container Orchestration
  - Deployed on Azure Kubernetes Service (AKS)
  - Auto-scaling capabilities

✅ Service Mesh
  - Azure Service Fabric provides equivalent features
  - Built-in service-to-service communication

✅ Infrastructure as Code
  - Terraform configurations in repo
  - Environment parity (dev/staging/prod)

✅ Centralized Logging
  - Azure Log Analytics integration
  - Aggregated logs across all services

✅ API Gateway
  - MS11-GATEWAY + MS15-REGISTRY
  - Centralized request handling

✅ Security
  - Azure Key Vault for secrets
  - mTLS for service-to-service

✅ Disaster Recovery
  - Multi-region failover
  - Automated backups

Recommendation: Update [ARCHITECTURE-OVERVIEW.md](docs/ARCHITECTURE-OVERVIEW.md) to explicitly document PaaSPA compliance.
```

---

### Open Data & CKAN Integration

**Status**: 🔴 RED - Not implemented

```
Current Gap:
❌ CKAN catalog registration
❌ DCAT-AP metadata publishing
❌ Public API for data discovery
❌ Linked data support (JSON-LD)

Solution: Identical to PNRR E-4 (CKAN Integration)
- Create DCAT-AP metadata schema
- Implement CKAN registration API
- Register ZenIA datasets in national catalog
- Enable semantic search via Linked Data

Effort: 15 hours (shared with PNRR)
Sprint: Q1 2026-1
```

---

### ANPR Integration

**Status**: 🔴 RED - Optional feature, not critical

```
Current Gap:
❌ ANPR person lookup not implemented
❌ No enrichment with ANPR data
❌ No address updates from ANPR

Nice-to-Have Features:
1. Person entity enrichment from ANPR
   - Current: MS02-ANALYZER extracts person name
   - Enhancement: Look up in ANPR, enrich with residency

2. Address validation
   - Current: Accept all addresses
   - Enhancement: Validate against ANPR addresses

3. Deceased person handling
   - Current: No special handling
   - Enhancement: Alert when document mentions deceased person

Priority: LOW (Not critical for MVP)
Effort: 15 hours (for phase 2)
Sprint: Q2 2026 or later
```

---

## Gap Analysis

### Critical Gaps (🔴 RED)

| Gap | Component | Impact | Effort | Sprint |
|-----|-----------|--------|--------|--------|
| Open Data Catalog | Data/Interoperability | PNRR + Piano Triennale | 15 hrs | Q1 2026-1 |
| ANPR Integration | ANPR Pillar | Optional enhancement | 15 hrs | Q2 2026 |

### Medium Priority Gaps (🟠 ORANGE)

| Gap | Component | Impact | Effort | Sprint |
|-----|-----------|--------|--------|--------|
| API Portal Registration | Piattaforme Digitali | Service discovery | 10 hrs | Q1 2026-1 |
| AgID Monitoring Compliance | Monitoring Pillar | Compliance tracking | 8 hrs | Q4 2025-2 |
| PaaSPA Documentation | PaaSPA Pillar | Explicit compliance claim | 5 hrs | Q4 2025-2 |

### Low Priority Gaps (🟡 YELLOW)

| Gap | Component | Impact | Effort | Sprint |
|-----|-----------|--------|--------|--------|
| SPID/CIE Integration | Piattaforme Digitali | Authentication option | 20 hrs | Q2 2026+ |
| Penetration Testing Formalization | Cybersecurity | Security assurance | 8 hrs | Q1 2026-1 |
| Threat Intelligence Sharing | Cybersecurity | Advanced feature | 10 hrs | Q3 2026+ |

---

## Azioni Correttive

### Q4 2025-2 (Settimane 5-8): Foundation

#### PT-1: PaaSPA Compliance Documentation
**Owner**: Solution Architect
**Effort**: 5 ore
**Output**: docs/PAASPA-COMPLIANCE-REPORT.md
**Actions**:
- Document cloud-native architecture vs PaaSPA checklist
- Verify all PaaSPA requirements satisfied
- Create PaaSPA compliance certificate template

#### PT-2: AgID Monitoring Integration
**Owner**: DevOps Lead
**Effort**: 8 ore
**Output**: Integration with AgID monitoring platform
**Actions**:
- Research AgID monitoring endpoint
- Implement metrics export
- Configure automatic reporting

#### PT-3: Security Audit Formalization
**Owner**: Security Officer
**Effort**: 5 ore
**Output**: docs/SECURITY-AUDIT-SCHEDULE.md
**Actions**:
- Define annual security audit schedule
- Select audit firm
- Create audit checklist

**Total Q4 2025-2**: 18 hours

### Q1 2026-1 (Settimane 9-16): Core Integration

#### PT-4: Open Data Catalog & CKAN Integration
**Owner**: Data Architect
**Effort**: 15 ore
**Output**: CKAN registration + DCAT-AP metadata
**Actions**:
- Create DCAT-AP metadata mapping
- Implement CKAN registration API
- Register ZenIA datasets
- Enable semantic search

#### PT-5: API Portal Registration
**Owner**: API Architect
**Effort**: 10 ore
**Output**: APIs registered on AgID API portal
**Actions**:
- Research AgID API portal requirements
- Register ZenIA APIs
- Add documentation
- Enable API discovery

#### PT-6: Penetration Testing
**Owner**: Security Team
**Effort**: 8 ore
**Output**: Penetration test report + remediation plan
**Actions**:
- Conduct security pentest
- Document findings
- Create remediation plan
- Fix critical issues

**Total Q1 2026-1**: 33 hours

### Q2 2026 (Future): Advanced Integration

#### PT-7: ANPR Integration (Optional)
**Owner**: Integration Architect
**Effort**: 15 ore
**Sprint**: Q2 2026
**Actions**:
- Integrate ANPR API
- Enrich person entities
- Validate addresses
- Test failover scenarios

---

## Evidence Collection per Piano Triennale

1. **PaaSPA Compliance** → docs/PAASPA-COMPLIANCE-REPORT.md (new)
2. **AgID Monitoring** → Integration status + metrics (new)
3. **Open Data** → CKAN registration + DCAT-AP (shared with PNRR)
4. **API Portal** → AgID portal registration (new)
5. **Cybersecurity** → Security audit report (new)
6. **DevOps Pipeline** → CI/CD documentation (existing)
7. **Accessibility** → WCAG 2.1 audit (shared with CAD)

---

## Cross-References

- **CAD D-1**: Accessibilità (A-3 WCAG 2.1) - shared effort
- **PNRR D-1**: Open data (E-4 CKAN) - shared effort
- **PNRR D-1**: API standards (E-1 OpenAPI) - shared effort
- **D-3**: Security architecture validation
- **T-3**: Security testing procedures

---

## Timeline Consolidato

### Q4 2025

| Task | Owner | Effort | Sprint |
|------|-------|--------|--------|
| PT-1: PaaSPA Documentation | Solution Architect | 5 hrs | Q4-2 |
| PT-2: AgID Monitoring | DevOps Lead | 8 hrs | Q4-2 |
| PT-3: Security Audit Schedule | Security Officer | 5 hrs | Q4-2 |

**Total Q4 2025**: 18 hours

### Q1 2026

| Task | Owner | Effort | Sprint |
|------|-------|--------|--------|
| PT-4: CKAN Integration | Data Architect | 15 hrs | Q1-1 |
| PT-5: API Portal Registration | API Architect | 10 hrs | Q1-1 |
| PT-6: Penetration Testing | Security Team | 8 hrs | Q1-1 |

**Total Q1 2026**: 33 hours

### Q2+ 2026

| Task | Owner | Effort | Sprint |
|------|-------|--------|--------|
| PT-7: ANPR Integration | Integration Architect | 15 hrs | Q2-1 |

**Total Estimate**: ~66 hours to reach 100% Piano Triennale compliance

---

## Roadmap Consolidato

```
Q4 2025-2 (Weeks 5-8)
├─ PT-1: PaaSPA Compliance Documentation ✓
├─ PT-2: AgID Monitoring Integration ✓
└─ PT-3: Security Audit Schedule ✓

Q1 2026-1 (Weeks 9-16)
├─ PT-4: Open Data CKAN Integration ✓
├─ PT-5: API Portal Registration ✓
├─ PT-6: Penetration Testing ✓
└─ CAD A-3: WCAG 2.1 Compliance Audit ✓

Q1 2026-2 (Weeks 17-24)
├─ PNRR E-4: CKAN Final Integration ✓
├─ PNRR E-5: Training Program ✓
└─ CAD A-1: WCAG 2.1 Remediation ✓

Q2 2026-1 (Weeks 25-32)
├─ PT-7: ANPR Integration (Optional)
└─ PNRR E-7: Carbon Footprint Reporting

Q4 2026
└─ Final Piano Triennale Compliance Certification ✓
```

---

*Generato come parte del backlog task D-1: Mappatura Completa Normative ZenIA*
