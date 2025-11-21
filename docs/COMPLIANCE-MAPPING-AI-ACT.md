# 📋 Matrice di Conformità ZenIA vs EU AI Regulation 2024/1689

**Data Creazione**: 21 novembre 2025
**Versione**: 1.0 - DRAFT
**Status**: IN PROGRESS
**Priorità**: 🔴 CRITICAL
**Sprint**: Q4 2025-1

---

## 📑 Indice

1. [Sommario Conformità](#sommario-conformità)
2. [Requisiti AI Act per Sistemi High-Risk](#requisiti-ai-act-per-sistemi-high-risk)
3. [Mappatura per Componente ZenIA](#mappatura-per-componente-zenia)
4. [Gap Analysis](#gap-analysis)
5. [Azioni Correttive](#azioni-correttive)

---

## Sommario Conformità

### Status Generale: 🟡 PARZIALMENTE CONFORME (65% stima iniziale)

| Dimensione | Requisito | Status | Note |
|------------|-----------|--------|------|
| **Risk Classification** | Classificare sistemi ML per livello di rischio | 🟠 PARTIAL | In Progress: MS01, MS02, MS04, MS05 |
| **Transparency** | Documentazione trasparenza per high-risk | 🟡 YELLOW | Richiede System Cards |
| **Documentation** | Technical documentation completa | 🟠 PARTIAL | SPECIFICATION presenti, mancano System Cards |
| **Data Governance** | Tracciabilità dati training | 🔴 RED | Richiede implementazione |
| **Quality Management** | QMS per high-risk systems | 🔴 RED | Da implementare |
| **Post-Market Monitoring** | Monitoring procedures | 🟠 PARTIAL | MS08-MONITOR esiste, mancano metriche fairness |
| **Bias & Fairness** | Bias testing e mitigation | 🔴 RED | Da implementare |
| **Human Oversight** | Mechanical explicability | 🟠 PARTIAL | Presente in MS02-ANALYZER, MS06-AGGREGATOR |

---

## Requisiti AI Act per Sistemi High-Risk

### 1. Classificazione Sistemi di Rischio

**Articolo 6-9 (Risk Levels)**:
- **Prohibited**: Pratiche IA vietate (biometric categorization, social scoring) ✅ NON APPLICABILE
- **High-Risk**: Sistemi che impactano diritti fondamentali
- **General Risk**: Uso generico
- **Minimal Risk**: Uso senza impatto significativo

#### Mappatura ZenIA

| Microservizio | Funzione | Risk Level | Fonte | Status |
|--------------|----------|-----------|--------|--------|
| **MS01-CLASSIFIER** | Classificazione documenti via ML | 🔴 HIGH-RISK | [SPECIFICATION.md](microservices/MS01-CLASSIFIER/SPECIFICATION.md#risk-assessment) | ✅ MAPPED |
| **MS02-ANALYZER** | Estrazione entità e analisi | 🟠 MEDIUM-RISK | [SPECIFICATION.md](microservices/MS02-ANALYZER/SPECIFICATION.md) | ✅ MAPPED |
| **MS04-VALIDATOR** | Validazione con regole ML | 🟠 MEDIUM-RISK | [SPECIFICATION.md](microservices/MS04-VALIDATOR/SPECIFICATION.md) | ✅ MAPPED |
| **MS05-TRANSFORMER** | Trasformazione formati (no ML) | 🟢 LOW-RISK | [SPECIFICATION.md](microservices/MS05-TRANSFORMER/SPECIFICATION.md) | ✅ MAPPED |
| **MS13-SECURITY** | Encryption e security | 🟢 LOW-RISK | [SPECIFICATION.md](microservices/MS13-SECURITY/SPECIFICATION.md) | ✅ MAPPED |

---

### 2. Requisiti per High-Risk Systems (MS01, MS02, MS04)

#### A. Risk Assessment & Mitigation (Articolo 27)

**Requisito AI Act**: Valutazione completa dei rischi per diritti fondamentali

**ZenIA Implementation Status**:

| Sub-Requirement | Documentazione | Codice | Test | Status |
|-----------------|-----------------|--------|------|--------|
| Identificazione rischi | [ARCHITECTURE-OVERVIEW.md](ARCHITECTURE-OVERVIEW.md#security-architecture) | MS13-SECURITY | ❌ Missing | 🟡 PARTIAL |
| Scenario di fallimento | [SPECIFICATION.md](microservices/MS01-CLASSIFIER/SPECIFICATION.md#failure-scenarios) | MS01 README | ❌ Missing | 🟡 PARTIAL |
| Mitigation strategies | [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md) | In code | ⚠️ Manual | 🟠 PARTIAL |
| Residual risk assessment | ❌ Missing | ❌ Missing | ❌ Missing | 🔴 RED |

**Gap**: Documentazione di risk assessment formale mancante. Richiede template DPIA (Data Protection Impact Assessment).

---

#### B. Data & Data Governance (Articolo 10)

**Requisito AI Act**: Qualità e tracciabilità dati training

**ZenIA Implementation Status**:

| Sub-Requirement | Documentazione | Evidenza | Status |
|-----------------|-----------------|----------|--------|
| Qualità dati training | [MS01-CLASSIFIER/SPECIFICATION.md](microservices/MS01-CLASSIFIER/SPECIFICATION.md#training-data) | Dataset metadata | 🟡 PARTIAL |
| Bias detection | ❌ Not documented | ❌ Not implemented | 🔴 RED |
| Data provenance | ❌ Not documented | ❌ Not tracked | 🔴 RED |
| Data retention policy | [COMPLIANCE-MATRIX.md](COMPLIANCE-MATRIX.md) | ⚠️ Partial | 🟡 PARTIAL |
| GDPR Data Rights | [ZENSHAREUP-ZENIA-INTEGRATION.md](ZENSHAREUP-ZENIA-INTEGRATION.md) | MS07 compliance | 🟡 PARTIAL |

**Gap**: Mancano tracker di data lineage e bias detection framework.

---

#### C. Technical Documentation (Articolo 11)

**Requisito AI Act**: Documentazione tecnica completa per high-risk systems

**ZenIA Implementation Status**:

| Component | Doc Status | API | Schema | Test | Status |
|-----------|-----------|-----|--------|------|--------|
| **MS01-CLASSIFIER** | ✅ Complete | ✅ API.md | ✅ DATABASE-SCHEMA.md | ✅ README | ✅ GOOD |
| **MS02-ANALYZER** | ✅ Complete | ✅ API.md | ✅ DATABASE-SCHEMA.md | ✅ README | ✅ GOOD |
| **MS04-VALIDATOR** | ✅ Complete | ✅ API.md | ✅ DATABASE-SCHEMA.md | ✅ README | ✅ GOOD |
| **MS05-TRANSFORMER** | ✅ Complete | ✅ API.md | ✅ DATABASE-SCHEMA.md | ✅ README | ✅ GOOD |

**Status**: ✅ DOCUMENTAZIONE TECNICA PRESENTE

---

#### D. Transparency & Explainability (Articolo 12)

**Requisito AI Act**: Trasparenza su uso e limitazioni sistemi IA

**ZenIA Implementation Status**:

| Requirement | Documentation | Where | Status |
|-------------|----------------|-------|--------|
| System documentation | ✅ SPECIFICATION.md per MS | docs/microservices/MSxx/ | ✅ PRESENT |
| Intended use | ✅ README.md per MS | docs/microservices/MSxx/ | ✅ PRESENT |
| Known limitations | ⚠️ Partial | SPECIFICATION.md | 🟡 PARTIAL |
| User interaction guide | ⚠️ Basic | README.md | 🟡 PARTIAL |
| Output confidence scores | ❌ Not documented | MS01, MS02, MS04 | 🔴 RED |

**Gap**: Manca documentazione su confidence scores e threshold decisioning.

---

#### E. Human Oversight (Articolo 14)

**Requisito AI Act**: Capacità umana di monitorare e intervenire

**ZenIA Implementation Status**:

| Sub-Requirement | Implementation | Status |
|-----------------|-----------------|--------|
| Meaningful human review | ✅ MS06-AGGREGATOR | ✅ PRESENT |
| Audit trails | ✅ MS14-AUDIT | ✅ PRESENT |
| Override capability | ✅ MS07-DISTRIBUTOR | ✅ PRESENT |
| User training materials | ❌ Not present | 🔴 RED |
| Appeal/remediation mechanism | ⚠️ Partial (MS14) | 🟡 PARTIAL |

**Status**: ✅ PARTIAL - Infrastruttura presente, documentazione user-facing mancante.

---

### 3. System Card Template & Documentation

**Requisito AI Act (Articolo 13)**: Ogni high-risk system richiede System Card

#### System Card Structure (EU AI Office Standard)

```markdown
# System Card: [Model Name]

## 1. Model Identity
- Model name and version
- Provider information
- Release date
- Model type (classifier, analyzer, validator)

## 2. Intended Use
- Primary use case
- Restrictions on use
- User groups
- Known limitations

## 3. Technical Specifications
- Input/output specifications
- Performance metrics (accuracy, precision, recall, F1)
- Threshold values
- Confidence scores

## 4. Training Data
- Data sources
- Data characteristics (size, distribution, bias indicators)
- Data preparation (cleaning, augmentation)
- Training/validation/test splits

## 5. Fairness & Bias
- Fairness assessment
- Identified biases
- Bias mitigation strategies
- Fairness metrics

## 6. Performance Evaluation
- Evaluation metrics
- Benchmark comparisons
- Performance across demographic groups
- Performance degradation scenarios

## 7. Environmental Impact
- Energy consumption during training
- Carbon footprint
- Optimization measures

## 8. Human Oversight
- Audit trail capability
- Explainability mechanisms
- User appeal processes
```

**Status**: ❌ System Cards NOT YET CREATED (richiesto per Q4 2025-1/2)

---

## Mappatura per Componente ZenIA

### MS01-CLASSIFIER

**File di Riferimento**: [docs/microservices/MS01-CLASSIFIER/](microservices/MS01-CLASSIFIER/)

**Risk Level**: 🔴 HIGH-RISK

**AI Act Compliance Checklist**:

- [x] Risk assessment documentato → [SPECIFICATION.md](microservices/MS01-CLASSIFIER/SPECIFICATION.md#risk-assessment)
- [x] Technical documentation → [SPECIFICATION.md](microservices/MS01-CLASSIFIER/SPECIFICATION.md), [API.md](microservices/MS01-CLASSIFIER/API.md), [DATABASE-SCHEMA.md](microservices/MS01-CLASSIFIER/DATABASE-SCHEMA.md)
- [ ] System Card (AI Act 13) → **REQUIRED**
- [ ] Training data characteristics → [SPECIFICATION.md](microservices/MS01-CLASSIFIER/SPECIFICATION.md#training-data) **PARTIAL**
- [ ] Fairness assessment → **MISSING**
- [ ] Bias testing procedures → **MISSING**
- [ ] Environmental impact → **MISSING**
- [ ] Confidence scores documentation → **MISSING**
- [ ] Human oversight capability → ✅ [MS06-AGGREGATOR review](microservices/MS06-AGGREGATOR/)
- [ ] Audit trail → ✅ [MS14-AUDIT](microservices/MS14-AUDIT/)

**Priority Gaps**:
1. ❌ System Card creation
2. ❌ Fairness assessment framework
3. ❌ Confidence thresholds documentation

---

### MS02-ANALYZER

**File di Riferimento**: [docs/microservices/MS02-ANALYZER/](microservices/MS02-ANALYZER/)

**Risk Level**: 🟠 MEDIUM-RISK

**AI Act Compliance Checklist**:

- [x] Technical documentation → [SPECIFICATION.md](microservices/MS02-ANALYZER/SPECIFICATION.md), [API.md](microservices/MS02-ANALYZER/API.md)
- [ ] System Card (AI Act 13) → **REQUIRED for high-confidence outputs**
- [ ] Entity extraction accuracy metrics → [SPECIFICATION.md](microservices/MS02-ANALYZER/SPECIFICATION.md#performance) **PARTIAL**
- [ ] Fairness across document types → **MISSING**
- [ ] Bias in entity recognition → **MISSING**
- [ ] Explainability of extractions → ✅ [SPECIFICATION.md](microservices/MS02-ANALYZER/SPECIFICATION.md#explainability)
- [ ] Human review capability → ✅ [MS06-AGGREGATOR](microservices/MS06-AGGREGATOR/)

**Priority Gaps**:
1. ❌ System Card for entity extraction model
2. ❌ Cross-language fairness assessment
3. ❌ Performance metrics per entity type

---

### MS04-VALIDATOR

**File di Riferimento**: [docs/microservices/MS04-VALIDATOR/](microservices/MS04-VALIDATOR/)

**Risk Level**: 🟠 MEDIUM-RISK

**AI Act Compliance Checklist**:

- [x] Technical documentation → Complete
- [x] Validation rules documented → [SPECIFICATION.md](microservices/MS04-VALIDATOR/SPECIFICATION.md#validation-rules)
- [ ] System Card → **REQUIRED**
- [ ] Confidence scoring → **PARTIAL**
- [ ] Fairness in validation → **MISSING**
- [ ] Error analysis → [SPECIFICATION.md](microservices/MS04-VALIDATOR/SPECIFICATION.md#error-handling) **PARTIAL**
- [ ] Audit trail → ✅ [MS14-AUDIT](microservices/MS14-AUDIT/)

**Priority Gaps**:
1. ❌ System Card
2. ❌ Formal fairness assessment
3. ❌ False positive/negative analysis

---

### MS05-TRANSFORMER

**File di Riferimento**: [docs/microservices/MS05-TRANSFORMER/](microservices/MS05-TRANSFORMER/)

**Risk Level**: 🟢 LOW-RISK (No ML)

**Status**: ✅ NO AI ACT REQUIREMENTS (data transformation only, no decision-making)

---

## Gap Analysis

### Critical Gaps (🔴 RED)

| Gap | Impact | Effort | Sprint |
|-----|--------|--------|--------|
| System Cards per MS01, MS02, MS04 | AI Act violation | 30 hrs | Q4 2025-1/2 |
| Fairness assessment framework | No bias detection | 25 hrs | Q4 2025-2 |
| Data lineage tracking | No data governance | 20 hrs | Q1 2026-1 |
| Bias testing automation | No continuous monitoring | 30 hrs | Q1 2026-1 |
| Environmental impact assessment | Incomplete documentation | 10 hrs | Q4 2025-2 |

### Medium Priority Gaps (🟠 ORANGE)

| Gap | Impact | Effort | Sprint |
|-----|--------|--------|--------|
| Confidence threshold documentation | Limited transparency | 8 hrs | Q4 2025-1 |
| Cross-document fairness metrics | Incomplete assessment | 15 hrs | Q1 2026-1 |
| User appeal process documentation | Limited remediation | 10 hrs | Q1 2026-1 |

### Low Priority Gaps (🟡 YELLOW)

| Gap | Impact | Effort | Sprint |
|-----|--------|--------|--------|
| Performance benchmarking | Limited context | 8 hrs | Q1 2026-1 |
| Known limitations expansion | Better transparency | 6 hrs | Q4 2025-2 |

---

## Azioni Correttive

### Q4 2025-1 (Settimane 1-4)

#### D-1.1: Creare System Card Template
**Owner**: ML Engineer + Architect
**Effort**: 5 ore
**Output**: Template standardizzato

#### D-1.2: System Card per MS01-CLASSIFIER
**Owner**: ML Engineer
**Effort**: 8 ore
**Prerequisiti**: Dati training assessment, fairness baseline
**Output**: docs/microservices/MS01-CLASSIFIER/SYSTEM-CARD.md

#### D-1.3: System Card per MS02-ANALYZER
**Owner**: NLP Specialist
**Effort**: 6 ore
**Output**: docs/microservices/MS02-ANALYZER/SYSTEM-CARD.md

---

### Q4 2025-2 (Settimane 5-8)

#### D-1.4: System Card per MS04-VALIDATOR
**Owner**: ML Engineer
**Effort**: 6 ore
**Output**: docs/microservices/MS04-VALIDATOR/SYSTEM-CARD.md

#### D-1.5: Fairness Assessment Framework
**Owner**: Data Science Lead
**Effort**: 15 ore
**Output**: docs/FAIRNESS-ASSESSMENT-FRAMEWORK.md + tooling

#### D-1.6: Environmental Impact Assessment
**Owner**: DevOps Lead
**Effort**: 8 ore
**Output**: docs/ENVIRONMENTAL-IMPACT.md

---

### Q1 2026-1 (Settimane 9-12)

#### D-1.7: Data Lineage Implementation
**Owner**: Data Engineer
**Effort**: 20 ore
**Output**: Data lineage tracking system + documentation

#### D-1.8: Bias Testing Automation
**Owner**: QA Lead
**Effort**: 18 ore
**Output**: CI/CD integration for bias detection

#### D-1.9: Final AI Act Compliance Review
**Owner**: Compliance Officer + Architect
**Effort**: 10 ore
**Output**: AI Act Compliance Certification

---

## Evidence Collection Strategy

### Per High-Risk System:

1. **System Card** → docs/microservices/MSxx/SYSTEM-CARD.md
2. **Fairness Report** → docs/microservices/MSxx/FAIRNESS-ASSESSMENT.md
3. **Bias Testing Results** → test-reports/bias-testing/MSxx/
4. **Performance Metrics** → metrics/baseline/MSxx.json
5. **Audit Logs** → Vedi MS14-AUDIT implementation
6. **User Documentation** → docs/microservices/MSxx/USER-GUIDE.md (to create)

---

## Cross-References to Other Compliance Tasks

- **D-2 (System Cards Detail)**: Espande questo mapping con dettagli tecnici
- **D-3 (Security Architecture)**: Copre risk mitigation strategies
- **D-4 (GDPR Audit Trail)**: Integra audit trail requirements
- **A-1 (Multi-Tenancy)**: Validazione isolamento tenant
- **T-1 (Bias Testing)**: Implementazione fairness testing

---

## Prossimi Step

1. ✅ Completare questa matrice AI Act
2. → Creare matrice CAD (D-1 CAD)
3. → Creare matrice PNRR (D-1 PNRR)
4. → Creare matrice Piano Triennale (D-1 Piano Triennale)
5. → Review incrociato e consolidamento
6. → Commit finale

**Data Target Completion**: Fine Q4 2025-1 (entro 4 settimane)

---

*Generato come parte del backlog task D-1: Mappatura Completa Normative ZenIA*
