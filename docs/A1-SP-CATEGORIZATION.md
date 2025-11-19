# A1 SubProjekti Categorization for Conformità Normativa Implementation

**Project**: ZenIA Documentation Phase 2 - A1 Conformità Normativa
**Status**: In Progress
**Created**: 2025-11-19
**Target Completion**: 2025-11-23

---

## Executive Summary

- **Total SPs**: 71 (SP28 reserved)
- **CRITICAL tier**: 10 SP (must apply template first)
- **HIGH tier**: 45 SP (apply template second)
- **MEDIUM tier**: 15 SP (apply template last)
- **Estimated effort**: 20-25 hours total for A1 template application

---

## CRITICAL Tier (10 SP) - APPLY FIRST ⭐

These SPs form the core foundation. Template application: ~10-12 hours (1-2 days)

| # | SP ID | Title | UC | GDPR | eIDAS | CAD | AGID | Priority |
|---|-------|-------|----|----|-------|-----|------|----------|
| 1 | SP01 | EML Parser & Email Intelligence | UC2, UC5 | ✅ | ✅ | ✅ | ❌ | **P0** |
| 2 | SP02 | Document Extractor & Attachment Classifier | UC1, UC5 | ✅ | ❌ | ✅ | ❌ | **P0** |
| 3 | SP04 | Knowledge Base & Legal Context Management | UC5 | ❌ | ❌ | ✅ | ❌ | **P0** |
| 4 | SP05 | Template Engine | UC5 | ❌ | ❌ | ✅ | ❌ | **P0** |
| 5 | SP07 | Content Classifier | UC1, UC5 | ✅ | ❌ | ✅ | ❌ | **P0** |
| 6 | SP12 | Semantic Search & Q&A Engine | UC1 | ✅ | ❌ | ✅ | ✅ | **P0** |
| 7 | SP29 | Digital Signature Engine | UC6 | ❌ | ✅ | ✅ | ❌ | **P0** |
| 8 | SP42 | Policy Engine | UC9 | ✅ | ❌ | ✅ | ❌ | **P0** |
| 9 | SP50 | Compliance Training & Certification | UC10 | ✅ | ❌ | ✅ | ✅ | **P0** |
| 10 | SP70 | Compliance & Audit Management | UC11 | ✅ | ❌ | ✅ | ❌ | **P0** |

**Notes**:
- SP01: Complex - manages email PEC signatures (eIDAS + GDPR)
- SP29: Core to digital signature stack (UC6)
- SP42, SP50, SP70: Compliance gatekeepers (UC9-11)
- All require CAD compliance
- 7 out of 10 require GDPR sections
- 2 out of 10 require eIDAS sections
- 3 out of 10 require AGID accessibility sections

**Approach**: Create detailed Conformità sections with all frameworks + HITL checkpoints

---

## HIGH Tier (45 SP) - APPLY SECOND ✓

Process, governance, and digital transformation. Template application: ~8-10 hours per batch

### UC1 - Document Management System (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP13 | Document Summarizer | ✅ | ❌ | ❌ |
| SP14 | Metadata Indexer | ❌ | ❌ | ❌ |
| SP15 | Document Workflow Orchestrator | ✅ | ❌ | ❌ |
| SP11 | Security & Audit | ✅ | ❌ | ❌ |

### UC2 - Digital Protocol System (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP16 | Correspondence Classifier | ✅ | ❌ | ❌ |
| SP17 | Register Suggester | ✅ | ❌ | ❌ |
| SP18 | Anomaly Detector | ✅ | ❌ | ❌ |
| SP19 | Protocol Workflow Orchestrator | ✅ | ❌ | ❌ |

### UC3 - Governance System (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP20 | Organization Management | ✅ | ❌ | ❌ |
| SP21 | Procedure Manager | ✅ | ❌ | ❌ |
| SP22 | Process Governance | ❌ | ❌ | ❌ |
| SP23 | Compliance Monitor | ✅ | ❌ | ❌ |

### UC4 - BPM & Process Automation (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP24 | Process Mining Engine | ✅ | ❌ | ❌ |
| SP25 | Predictive Planning & Forecasting | ❌ | ❌ | ❌ |
| SP26 | Intelligent Workflow Designer | ✅ | ❌ | ❌ |
| SP27 | Process Analytics | ✅ | ❌ | ❌ |

### UC5 - Integrated Document Production (5 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP03 | Procedural Classifier | ✅ | ❌ | ❌ |
| SP06 | Validator | ✅ | ❌ | ❌ |
| SP08 | Quality Checker | ✅ | ❌ | ❌ |
| SP09 | Workflow Engine | ✅ | ❌ | ❌ |
| SP10 | Control Dashboard | ✅ | ❌ | ✅ |

### UC6 - Digital Signature System (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP30 | Certificate Manager | ❌ | ✅ | ❌ |
| SP31 | Signature Workflow | ❌ | ✅ | ❌ |
| SP32 | Timestamp Authority & Marking | ❌ | ✅ | ❌ |

### UC7 - Archive Management & Preservation (5 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP33 | Archive Manager | ✅ | ❌ | ❌ |
| SP34 | Preservation Engine | ✅ | ❌ | ❌ |
| SP35 | Integrity Validator | ❌ | ❌ | ❌ |
| SP36 | Storage Optimizer | ❌ | ❌ | ❌ |
| SP37 | Archive Metadata Manager | ✅ | ❌ | ❌ |

### UC8 - SIEM Integration & Security (4 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP38 | SIEM Collector | ✅ | ❌ | ❌ |
| SP39 | SIEM Processor | ✅ | ❌ | ❌ |
| SP40 | SIEM Storage | ✅ | ❌ | ❌ |
| SP41 | SIEM Analytics & Reporting | ✅ | ❌ | ❌ |

### UC9 - Compliance & Risk Management (8 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP43 | Risk Assessment Engine | ✅ | ❌ | ❌ |
| SP44 | Compliance Monitoring System | ✅ | ❌ | ❌ |
| SP45 | Regulatory Intelligence Hub | ✅ | ❌ | ❌ |
| SP46 | Compliance Automation Platform | ✅ | ❌ | ❌ |
| SP47 | Compliance Analytics & Reporting | ✅ | ❌ | ✅ |
| SP48 | Compliance Intelligence Platform | ✅ | ❌ | ❌ |
| SP49 | Regulatory Change Management | ✅ | ❌ | ❌ |

### UC10 - User Support (6 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP51 | Help Desk System | ✅ | ❌ | ✅ |
| SP52 | Knowledge Base Management | ✅ | ❌ | ✅ |
| SP53 | Virtual Assistant & Chatbot | ✅ | ❌ | ✅ |
| SP54 | User Training Platform | ✅ | ❌ | ✅ |
| SP55 | Self-Service Portal | ✅ | ❌ | ✅ |

**Total HIGH Tier**: 45 SP
- GDPR required: 40/45 (89%)
- AGID required: 6/45 (13%)
- eIDAS required: 0/45 (0%)

---

## MEDIUM Tier (15 SP) - APPLY LAST ◆

Analytics, DevOps, and monitoring infrastructure. Template application: ~4-5 hours per batch

### UC10 - User Support (2 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP56 | Support Analytics & Reporting | ✅ | ❌ | ❌ |
| SP57 | User Feedback Management | ✅ | ❌ | ❌ |

### UC11 - Data Analysis & Reporting (13 SP)
| SP ID | Title | GDPR | eIDAS | AGID |
|-------|-------|------|-------|------|
| SP58 | Data Lake & Storage Management | ✅ | ❌ | ❌ |
| SP59 | ETL Pipeline & Data Processing | ✅ | ❌ | ❌ |
| SP60 | Advanced Analytics & Machine Learning | ✅ | ❌ | ❌ |
| SP61 | Self-Service Analytics Portal | ✅ | ❌ | ✅ |
| SP62 | Data Quality & Governance | ✅ | ❌ | ❌ |
| SP63 | Real-Time Analytics & Streaming | ✅ | ❌ | ❌ |
| SP64 | Predictive Analytics & Forecasting | ❌ | ❌ | ❌ |
| SP65 | Performance Monitoring & Alerts | ✅ | ❌ | ❌ |
| SP66 | Data Security & Compliance | ❌ | ❌ | ❌ |
| SP67 | API Gateway & Integration Layer | ✅ | ❌ | ❌ |
| SP68 | DevOps & CI/CD Pipeline | ✅ | ❌ | ❌ |
| SP69 | Disaster Recovery & Business Continuity | ✅ | ❌ | ❌ |
| SP72 | Incident Management & Escalation | ❌ | ❌ | ❌ |

**Total MEDIUM Tier**: 15 SP
- GDPR required: 12/15 (80%)
- AGID required: 1/15 (7%)
- eIDAS required: 0/15 (0%)

---

## Compliance Requirements Summary

| Framework | Total SPs | % | Critical | High | Medium |
|-----------|-----------|---|----------|------|--------|
| **CAD** | 71/71 | 100% | 10 | 45 | 15 |
| **GDPR** | 62/71 | 87% | 7 | 40 | 12 |
| **eIDAS** | 5/71 | 7% | 2 | 0 | 0 |
| **AGID** | 11/71 | 15% | 3 | 6 | 2 |

**CAD Compliance**: All 71 SPs
**GDPR Compliance**: 62 SPs (most DMS, classification, extraction, governance, monitoring)
**Exempt from GDPR**: SP05, SP25, SP35, SP36, SP64, SP66, SP72 (9 non-sensitive SPs)
**eIDAS Compliance**: 5 SPs (digital signature stack + email PEC validation)
**AGID Compliance**: 11 SPs (UI + accessibility requirements)

---

## Implementation Schedule

### Week 1: CRITICAL Tier (10 SP)
- **Days 1-2**: SP01, SP02, SP04, SP05 (foundation)
- **Days 3-4**: SP07, SP12, SP29 (processing + signatures)
- **Days 5**: SP42, SP50, SP70 (compliance)
- **Estimated effort**: 10-12 hours
- **Validation**: Full HITL checkpoint testing

### Week 2: HIGH Tier (45 SP)
- **Days 6-7**: UC1-2 batch (SP03, SP06, SP08-19) = 12 SP
- **Days 8-9**: UC3-4 batch (SP20-27) = 8 SP
- **Days 10**: UC5-6 batch (SP30-31) = 2 SP
- **Plus continuation...** (SP33-55 = 23 SP)
- **Estimated effort**: 8-10 hours per day = 40 hours total
- **Parallel validation**: Cross-reference with GLOSSARIO

### Week 3: MEDIUM Tier (15 SP)
- **Days 11-12**: SP56-57 + SP58-67 (10 SP)
- **Days 13-14**: SP68-72 (5 SP) + final validation
- **Estimated effort**: 4-5 hours
- **Final validation & commit**

---

## HITL Checkpoint Strategy

For each SP Conformità section, apply 1-2 key HITL checkpoints:

**CRITICAL SPs**: 2-3 HITL checkpoints
- #1: Regulatory Completeness (all frameworks)
- #2: Compliance Review (CAD/GDPR/eIDAS/AGID)
- #3: Approval & Monitoring (if critical compliance)

**HIGH SPs**: 1-2 HITL checkpoints
- #1: Compliance Review (CAD + relevant framework)
- #2: Approval (if governance-critical)

**MEDIUM SPs**: 1 HITL checkpoint
- #1: Monitoring Schedule (minimal intervention)

---

## Validation Checklist Before Merge

For each SP, before marking as complete:

- [ ] Template applied (section structure matches TEMPLATE-CONFORMITA-NORMATIVA.md)
- [ ] All applicable frameworks included (CAD, GDPR, eIDAS, AGID)
- [ ] HITL checkpoints defined with JSON tracking examples
- [ ] Responsibility mapping complete (RACI matrix)
- [ ] Guardrail compliance: section < 10 KB total
- [ ] Terminología: all terms match GLOSSARIO-TERMINOLOGICO.md
- [ ] Cross-references: links to other SPs where applicable
- [ ] Monitoring schedule: next review date specified
- [ ] Git: file updated with new timestamp + version bump

---

## Success Criteria for A1

- ✅ All 71 SPs have Conformità Normativa sections
- ✅ HITL checkpoints integrated (6 main checkpoint types)
- ✅ Guardrails enforced (no section > 10 KB)
- ✅ Full GLOSSARIO-TERMINOLOGICO.md alignment
- ✅ Zero broken cross-references
- ✅ Estimated increase to 97.5-98% completeness score
- ✅ Estimated increase to 95-96% quality score

---

**File version**: 1.0
**Last updated**: 2025-11-19
**Status**: Ready for implementation
