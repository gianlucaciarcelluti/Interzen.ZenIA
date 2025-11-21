# 📋 Matrice di Conformità ZenIA vs PNRR (Piano Nazionale Ripresa Resilienza)

**Data Creazione**: 21 novembre 2025
**Versione**: 1.0 - DRAFT
**Status**: IN PROGRESS
**Priorità**: 🟠 P1 HIGH (Mandatory - Linee guida per progetti digitali)
**Sprint**: Q4 2025-2 / Q1 2026-1

---

## 📑 Indice

1. [Sommario Conformità](#sommario-conformità)
2. [Pilastri PNRR per Digitale](#pilastri-pnrr-per-digitale)
3. [Mappatura ZenIA](#mappatura-zenia)
4. [Gap Analysis](#gap-analysis)
5. [Azioni Correttive](#azioni-correttive)

---

## Sommario Conformità

### Status Generale: ✅ BUONA CONFORMITÀ (78% stima iniziale)

| Dimensione | Requisito PNRR | Status | Effort |
|------------|-----------------|--------|--------|
| **Cloud Strategy** | Cloud-first con Poli Strategici Nazionali | ✅ GOOD | 2 ore |
| **API Standards** | Interoperabilità OpenAPI 3.0 | 🟡 PARTIAL | 8 ore |
| **Open Data** | Trasparenza e open data publishing | 🟠 PARTIAL | 12 ore |
| **Security** | Security-by-design architecture | ✅ GOOD | 0 ore |
| **Disaster Recovery** | Continuità servizio > 99.9% | ✅ GOOD | 0 ore |
| **Green Computing** | Efficienza energetica | 🟡 PARTIAL | 6 ore |
| **Skills & Training** | Competenze digitali | ❌ MISSING | 15 ore |
| **Monitoring** | Telemetria e monitoring 24/7 | ✅ GOOD | 2 ore |

**Totale Effort Stimato**: ~45 ore

---

## Pilastri PNRR per Digitale

```
Context: Missione 1 "Digitalizzazione, innovazione e competitività nel sistema produttivo"
```

Il PNRR stanzia €48,6 miliardi per la digitalizzazione della PA, infrastrutture digitali, e innovazione. ZenIA rientra nel programma di **modernizzazione dei servizi di documentazione amministrativa**.

---

### Pilastro 1: Cloud Strategy (Cloud-First)

**Requisito PNRR**: Strategie cloud-first basate su servizi offerti da Poli Strategici Nazionali

#### Cloud Infrastructure Assessment

| Requirement | Implementation | ZenIA Status | Reference |
|-------------|-----------------|--------------|-----------|
| **Multi-Cloud Support** | Azure (primary) + S3 (failover) + Filesystem (dev) | ✅ EXCELLENT | [ZENSHAREUP-ARCHITECTURE.md](ZENSHAREUP-ARCHITECTURE.md#storage-backends) |
| **Cloud Provider Selection** | AGID-approved providers (Azure qualified) | ✅ EXCELLENT | Microsoft Azure (Trusted Cloud) |
| **Data Sovereignty** | EU data residency (non-US data centers) | ✅ GOOD | EU-only Azure regions |
| **Cost Optimization** | Reserved instances, spot pricing | 🟡 PARTIAL | [COSTI-HOSTING-SERVIZI.md](COSTI-HOSTING-SERVIZI.md) - review needed |
| **Service Level Agreements** | >99.9% uptime SLA | ✅ GOOD | Cloud provider SLA |
| **Disaster Recovery** | RTO < 1 hour, RPO < 15 min | ✅ GOOD | Geo-redundant backups |

**Status**: ✅ EXCELLENT - ZenShareUp cloud strategy fully compliant

---

### Pilastro 2: Interoperabilità & OpenAPI

**Requisito PNRR**: API standardizzate per interoperabilità tra servizi PA

#### API Standardization

| Component | Requirement | Status | Reference |
|-----------|-------------|--------|-----------|
| **OpenAPI 3.0 Spec** | All APIs documented in OpenAPI 3.0 | 🟡 PARTIAL | [docs/microservices/MSxx/API.md](microservices/) |
| **Versioning Strategy** | Semantic versioning + backward compatibility | 🟡 PARTIAL | [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md) - needs explicit policy |
| **Error Handling** | Standardized HTTP status codes + error responses | 🟡 PARTIAL | Varies by service |
| **Authentication** | OAuth 2.0 / OpenID Connect | ✅ GOOD | [MS13-SECURITY](microservices/MS13-SECURITY/) |
| **Rate Limiting** | API rate limits + quotas | 🟡 PARTIAL | Implemented per service, not documented |
| **API Gateway** | Centralized API gateway | 🟡 PARTIAL | MS15-REGISTRY provides service discovery |
| **Documentation** | Auto-generated API docs | 🟡 PARTIAL | Need Swagger UI integration |

**Status**: 🟡 PARTIAL - Technical implementation good, formal documentation incomplete

**Gap**: Formal OpenAPI schema validation + Swagger UI generation

---

### Pilastro 3: Open Data & Trasparenza

**Requisito PNRR**: Dati aperti per trasparenza amministrativa, interoperabilità con piattaforme nazionali

#### Open Data Components

| Component | Requirement | Status | Detail |
|-----------|-------------|--------|--------|
| **Data Publishing** | Publicare metadati documentali | ❌ MISSING | Requires data publishing service |
| **CKAN Catalog** | Registrazione in catalogo CKAN | ❌ MISSING | Requires DCAT-AP integration |
| **Metadata Format** | DCAT-AP 2.0.1 (Dublin Core extended) | ❌ MISSING | Requires mapping |
| **License** | Chiara licenza dati (CC0, CC-BY, etc.) | ❌ MISSING | Requires license selection |
| **Machine-Readability** | JSON-LD, RDF formats | ❌ MISSING | Requires serialization |
| **API Accessibility** | REST API per accesso dati | 🟡 PARTIAL | MS07 provides access, no public API |
| **Non-Discrimination** | Uguali condizioni accesso | 🟡 PARTIAL | Depends on authentication |

**Status**: 🔴 RED - Open data publishing infrastructure missing

**Gap**: CKAN integration + metadata publishing framework

---

### Pilastro 4: Security by Design

**Requisito PNRR**: Architettura sicura (security-by-design, encryption, authentication)

#### Security Architecture

| Component | Requirement | Status | Reference |
|-----------|-------------|--------|-----------|
| **Encryption at Rest** | TDE + Azure encryption | ✅ EXCELLENT | [MS13-SECURITY](microservices/MS13-SECURITY/SPECIFICATION.md) |
| **Encryption in Transit** | TLS 1.3 for all connections | ✅ EXCELLENT | MS13-SECURITY |
| **Key Management** | HSM or Azure Key Vault | ✅ GOOD | [ZENSHAREUP-ARCHITECTURE.md](ZENSHAREUP-ARCHITECTURE.md) |
| **Authentication** | Multi-factor auth capability | ✅ GOOD | MS13-SECURITY + OAuth 2.0 |
| **Authorization** | Role-based access control (RBAC) | ✅ GOOD | [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md) |
| **Audit Logging** | Complete audit trail | ✅ EXCELLENT | [MS14-AUDIT](microservices/MS14-AUDIT/) |
| **Vulnerability Management** | Regular security scanning | 🟡 PARTIAL | CI/CD integration needed |
| **Incident Response** | Formal incident response plan | 🟡 PARTIAL | [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md) - needs detail |

**Status**: ✅ EXCELLENT - Security architecture solid

---

### Pilastro 5: Continuità Servizio & Disaster Recovery

**Requisito PNRR**: Continuità servizio, disaster recovery, backup strategy

#### Business Continuity Components

| Component | Requirement | Status | SLA Target |
|-----------|-------------|--------|------------|
| **Availability** | >99.9% uptime | ✅ EXCELLENT | Geo-redundant |
| **RTO (Recovery Time Objective)** | < 1 hour | ✅ GOOD | Cloud-native |
| **RPO (Recovery Point Objective)** | < 15 minutes | ✅ GOOD | Continuous replication |
| **Backup Strategy** | Daily automated backups | ✅ GOOD | [ZENSHAREUP-ARCHITECTURE.md](ZENSHAREUP-ARCHITECTURE.md) |
| **Backup Retention** | 30-day minimum retention | ✅ GOOD | Cloud provider native |
| **Backup Testing** | Regular restore tests | 🟡 PARTIAL | Needs formalization |
| **Failover Capability** | Automatic failover | ✅ GOOD | Cloud-native |
| **Documentation** | Disaster recovery runbooks | 🟡 PARTIAL | Needs creation |

**Status**: ✅ GOOD - Infrastructure strong, documentation incomplete

---

### Pilastro 6: Efficienza Energetica (Green Computing)

**Requisito PNRR**: Efficienza energetica, carbon footprint reduction

#### Green IT Components

| Component | Requirement | Status | Action |
|-----------|-------------|--------|--------|
| **Data Center Efficiency** | Use efficient cloud providers | ✅ GOOD | Azure Green Regions |
| **Code Efficiency** | Optimize algorithms & data structures | ✅ GOOD | [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md) |
| **Cloud Native** | Serverless where possible | 🟡 PARTIAL | Some services could be optimized |
| **Resource Monitoring** | Track energy usage | 🟡 PARTIAL | Azure Monitor available |
| **Carbon Reporting** | Annual carbon footprint | ❌ MISSING | Requires calculation framework |
| **Green Certification** | ISO 50001 / ISO 14001 | ❌ MISSING | Provider scope |

**Status**: 🟡 PARTIAL - Infrastructure efficient, formal reporting missing

**Gap**: Carbon footprint calculation + annual sustainability report

---

### Pilastro 7: Digital Skills & Competence Building

**Requisito PNRR**: Programmi di formazione, skill development per PA e cittadini

#### Training & Skills Components

| Component | Requirement | Status | Effort |
|-----------|-------------|--------|--------|
| **PA Staff Training** | Training materials for PA administrators | ❌ MISSING | 10 hours |
| **Developer Documentation** | Technical documentation for developers | ✅ GOOD | [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md) |
| **API Documentation** | Clear API usage guides | 🟡 PARTIAL | [API.md](microservices/MSxx/API.md) exists |
| **Video Tutorials** | Recorded training videos | ❌ MISSING | 20+ hours |
| **Certification Program** | Training certification | ❌ MISSING | Future scope |
| **Community Support** | Community forums / help desk | ❌ MISSING | Future scope |

**Status**: 🔴 RED - Training program completely missing

**Gap**: Comprehensive training materials for PA operators

---

### Pilastro 8: Monitoring & Telemetria

**Requisito PNRR**: Monitoraggio 24/7, telemetria, observability

#### Monitoring Components

| Component | Requirement | Status | Reference |
|-----------|-------------|--------|-----------|
| **Application Monitoring** | Real-time performance metrics | ✅ GOOD | [MS08-MONITOR](microservices/MS08-MONITOR/) |
| **Infrastructure Monitoring** | CPU, memory, disk, network | ✅ GOOD | Azure Monitor |
| **Log Aggregation** | Centralized logging | ✅ GOOD | [MS11-GATEWAY](microservices/MS11-GATEWAY/) |
| **Alerting** | Automatic alerts on anomalies | ✅ GOOD | MS08-MONITOR + cloud provider alerts |
| **SLA Monitoring** | Track SLA compliance | 🟡 PARTIAL | Need dashboard |
| **Incident Management** | Ticket creation from alerts | 🟡 PARTIAL | Manual currently |
| **Dashboards** | Real-time operational dashboards | 🟡 PARTIAL | Grafana/Kibana integration |

**Status**: ✅ GOOD - Core monitoring present, dashboards & SLA tracking incomplete

---

## Mappatura ZenIA

### Cloud Infrastructure Compliance

**Status**: ✅ EXCELLENT - Fully cloud-native, multi-cloud strategy

```
ZenShareUp Architecture:
├── Primary: Azure Blob Storage
├── Failover: AWS S3
└── Dev: Local Filesystem

Compliance:
✅ Cloud-first strategy → PNRR compliant
✅ Trusted Cloud provider → Microsoft Azure qualified
✅ EU data residency → EU-only regions
✅ >99.9% SLA → Geo-redundant architecture
✅ Disaster Recovery → Automated failover
```

### API Interoperability Compliance

**Status**: 🟡 PARTIAL - Technical implementation good, formal compliance incomplete

```
Current State:
✅ REST APIs → [docs/microservices/MSxx/API.md](docs/microservices/)
✅ JSON responses → Standardized format
✅ OpenAPI 3.0 → Documented (needs validation)
🟡 Versioning → Implicit, needs formal policy
🟡 Error handling → Inconsistent across services
🟡 Documentation → Exists but not auto-generated

Action Items:
→ Formal OpenAPI schema validation
→ Swagger UI integration
→ Standardized error responses
→ API versioning policy document
```

### Open Data & Transparency

**Status**: 🔴 RED - Framework completely missing

```
Current State:
❌ CKAN integration → Not implemented
❌ DCAT-AP metadata → Not published
❌ Open API access → Restricted to internal services
❌ Data licensing → Not defined

Action Items:
→ CKAN integration (MS15-REGISTRY)
→ Metadata mapping to DCAT-AP
→ Public API endpoint for document discovery
→ License selection & publication
→ CKAN registration
```

---

## Gap Analysis

### Critical Gaps (🔴 RED)

| Gap | Impact | Component | Effort | Sprint |
|-----|--------|-----------|--------|--------|
| Open Data Publishing | PNRR transparency requirement | Infrastructure | 20 hrs | Q1 2026-1 |
| Training Program | Digital skills requirement | Operations | 15 hrs | Q1 2026-1 |
| Carbon Footprint Reporting | Green computing requirement | Sustainability | 8 hrs | Q2 2026 |

### Medium Priority Gaps (🟠 ORANGE)

| Gap | Impact | Effort | Sprint |
|-----|--------|--------|--------|
| OpenAPI Formal Validation | Interoperability standards | 8 hrs | Q4 2025-2 |
| API Documentation Auto-Generation | Developer experience | 5 hrs | Q4 2025-2 |
| SLA Monitoring Dashboard | Compliance tracking | 6 hrs | Q1 2026-1 |
| DR Runbooks Documentation | Incident response | 4 hrs | Q4 2025-2 |

### Low Priority Gaps (🟡 YELLOW)

| Gap | Impact | Effort | Sprint |
|-----|--------|--------|--------|
| Cost Optimization Analysis | Financial efficiency | 3 hrs | Q1 2026-1 |
| Vulnerability Scanning CI/CD | Security posture | 5 hrs | Q1 2026-1 |
| Sustainability Metrics | Green initiative | 4 hrs | Q2 2026 |

---

## Azioni Correttive

### Q4 2025-2: API Standardization & DR Documentation

**E-1: OpenAPI Formal Compliance**
- Owner: API Architect
- Effort: 8 ore
- Output: docs/OPENAPI-COMPLIANCE-REPORT.md
- Actions:
  - Validate all MSxx/API.md against OpenAPI 3.0 schema
  - Fix schema errors
  - Generate openapi.yaml

**E-2: Swagger UI Integration**
- Owner: Frontend Developer
- Effort: 5 ore
- Output: API documentation portal
- Actions:
  - Deploy Swagger UI with OpenAPI spec
  - Configure authentication in UI
  - Link from README

**E-3: Disaster Recovery Runbooks**
- Owner: DevOps Lead
- Effort: 4 ore
- Output: docs/DISASTER-RECOVERY-RUNBOOK.md
- Actions:
  - Document failover procedures
  - Backup restoration steps
  - Recovery time estimates

### Q1 2026-1: Open Data & Training

**E-4: CKAN Integration & Open Data Publishing**
- Owner: Data Architect
- Effort: 15 ore
- Output: docs/OPEN-DATA-STRATEGY.md + MS15 enhancement
- Actions:
  - Document metadata schema (DCAT-AP)
  - Implement CKAN registration API
  - Create data publishing workflow
  - Register in CKAN catalog

**E-5: Digital Skills Training Program**
- Owner: Training Coordinator + Technical Writer
- Effort: 15 ore
- Output: docs/TRAINING-MATERIALS/ + videos
- Actions:
  - Create training modules for PA staff
  - Develop API usage guides
  - Record video tutorials
  - Create certification path

**E-6: SLA Monitoring Dashboard**
- Owner: DevOps Lead
- Effort: 6 ore
- Output: Grafana dashboard
- Actions:
  - Create SLA KPI dashboard
  - Automated SLA reporting
  - Alert escalation workflow

### Q2 2026: Green Computing & Sustainability

**E-7: Carbon Footprint Reporting**
- Owner: Sustainability Officer
- Effort: 8 ore
- Output: docs/SUSTAINABILITY-REPORT.md
- Actions:
  - Calculate annual carbon footprint
  - Identify optimization opportunities
  - Set reduction targets
  - Track progress quarterly

---

## Evidence Collection per PNRR

1. **Cloud Infrastructure** → [ZENSHAREUP-ARCHITECTURE.md](ZENSHAREUP-ARCHITECTURE.md) ✅ EXISTING
2. **API Standardization** → docs/OPENAPI-COMPLIANCE-REPORT.md (new)
3. **Open Data Strategy** → docs/OPEN-DATA-STRATEGY.md (new)
4. **Training Materials** → docs/TRAINING-MATERIALS/ (new)
5. **Disaster Recovery** → docs/DISASTER-RECOVERY-RUNBOOK.md (new)
6. **Sustainability Report** → docs/SUSTAINABILITY-REPORT.md (new)
7. **Monitoring Dashboards** → Grafana screenshots + SLA metrics (new)

---

## Cross-References

- **D-2**: System Cards per ML models
- **D-3**: Security Architecture details
- **A-4**: API OpenAPI 3.0 validation (identical task)
- **C-2**: Compliance monitoring (uses monitoring infrastructure)

---

## Timeline Stima

| Sprint | Task | Owner | Effort |
|--------|------|-------|--------|
| Q4 2025-2 | E-1, E-2, E-3 | API/DevOps Team | 17 hrs |
| Q1 2026-1 | E-4, E-5, E-6 | Data/Training/DevOps | 36 hrs |
| Q2 2026 | E-7 | Sustainability Officer | 8 hrs |

**Totale**: ~61 ore per raggiungere 100% PNRR compliance

---

*Generato come parte del backlog task D-1: Mappatura Completa Normative ZenIA*
