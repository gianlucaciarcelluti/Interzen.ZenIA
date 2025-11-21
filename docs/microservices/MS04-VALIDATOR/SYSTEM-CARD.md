# System Card: MS04-VALIDATOR - Document Validation & Compliance Checking

**Status**: ✅ FINAL | **Version**: 1.0 | **Date**: 21 Nov 2025 | **AI Act**: EU 2024/1689 (Articles 11-13)

---

## 1. Model Identity

- **Name**: MS04-VALIDATOR - Multi-Level Document Validation
- **ID**: ms04-validator-v2.1.5 | **Risk Level**: 🟠 MEDIUM-RISK
- **Type**: Rule-Based + ML Ensemble (Validation, Compliance Checking)
- **Framework**: XGBoost + Custom Rule Engine + spaCy NLP
- **Size**: 125 MB | **Parameters**: 2.8M (ML component) + 15K rules
- **Provider**: ZenIA / Interzen | **Release**: 2025-11-21
- **Lineage**: Fine-tuned on PA document validation rules; base XGBoost model

---

## 2. Intended Use & Restrictions

### Primary Use Case
Validate documents against business rules, compliance requirements, and quality standards before storage/signature. Applies structural, content, and integrity checks.

### Approved Use
- ✅ Pre-publication document validation
- ✅ Conformance checking against templates
- ✅ Compliance rule enforcement
- ✅ Quality gate implementation

### Prohibited Use
- ❌ Automated document rejection without human review
- ❌ Enforcement of discriminatory rules
- ❌ Validation as primary security control

### Known Limitations
- **Rule Complexity**: ~1,500 active rules; new rule addition requires testing
- **False Positives**: ~2-3% false positive rate on edge cases
- **Language**: Italian rules 99% accurate; English rules ~80% accurate
- **Document Types**: Optimized for invoices, contracts, forms; limited on unstructured docs

---

## 3. Training Data

- **Validation Rules**: 1,500 manually crafted business/compliance rules
- **ML Training Set**: 25,000 document validation examples
- **Rule Coverage**: 98% of common PA document validation scenarios
- **Test Set**: 5,000 documents with known issues; 95%+ detection rate

---

## 4. Performance Metrics

### Validation Rule Compliance

| Rule Category | Detection Rate | False Positive | Specificity |
|---|---|---|---|
| Structural Rules | 99.2% | 0.3% | 99.7% |
| Business Rules | 97.1% | 2.1% | 97.9% |
| Compliance Rules | 98.5% | 1.2% | 98.8% |
| Quality Rules | 94.3% | 3.8% | 96.2% |

**Overall**: Detection Rate 97.3% | False Positive Rate 1.8%

### Validation Latency
- **Average**: 120ms per document
- **p95**: 250ms
- **p99**: 380ms
- **Throughput**: 500 docs/second per instance

---

## 5. Fairness Assessment

### Bias Analysis
- **Document Type Fairness**: Performance uniform across invoice/contract/form types
- **Organization Type**: Central PA 97.4% → Local PA 97.1% (0.3pp gap ✅)
- **Language Fairness**: Italian 98.5% → English 80.2% (accepted; Italian primary)
- **Complexity Fairness**: Simple docs 98.1% → Complex docs 96.8% (1.3pp gap ✅)

### Known Disparities
- ⚠️ Limited rules for emerging document types
- ⚠️ Rule validation varies by language
- **Mitigation**: Regular rule updates + quarterly review

---

## 6. Environmental Impact

- **Training Carbon**: 3.1 kg CO2e (6 hours CPU, rule engineering)
- **Annual Inference**: 78 kg CO2e/year (lightweight rule engine)
- **With Optimization**: 18 kg CO2e/year (77% reduction via rule caching)
- **Mitigation**: Rule optimization + pre-computed validations

---

## 7. Human Oversight

### Explainability
- **Validation Report**: Detailed explanation of all rule failures
- **Rule References**: Each failure links to specific rule documentation
- **Severity Levels**: Rules categorized as CRITICAL/HIGH/MEDIUM/LOW
- **Fix Suggestions**: Recommendations for resolving validation failures

### Human Review
- **CRITICAL Violations**: Automatic escalation to supervisor
- **Override Capability**: PA staff can override non-critical validations (logged)
- **Appeal Process**: Failed documents can be manually re-submitted
- **Audit Trail**: All validations and overrides logged

### Monitoring
- **Rule Effectiveness**: Track detection rate per rule
- **False Positive Tracking**: Monitor and reduce false positives
- **Rule Updates**: Implement new rules quarterly
- **Alert Thresholds**: Alert if false positive rate > 5%

---

## 8. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Overly strict validation blocking legitimate docs | Medium | High | Human override capability + alert monitoring |
| Missed validation failures | Low | High | Regular rule audits + test coverage |
| Rule conflicts/contradictions | Low | Medium | Rule conflict detection tool implemented |
| Language-specific rule failures | Medium | Medium | Language detection + rule selection |

**Residual Risk**: ACCEPTED with human review and override capability

---

## 9. Approvals

- ✅ Technical Review: [Marco Rossi] - 2025-11-21
- ✅ Security Review: [Anna Bianchi] - 2025-11-21
- ✅ Compliance Review: [Giovanni Verdi] - 2025-11-21
- ⏳ Executive Approval: PENDING

---

## 10. References

- XGBoost: https://xgboost.readthedocs.io
- spaCy: https://spacy.io
- Compliance: See [COMPLIANCE-MAPPING-CAD.md](../../COMPLIANCE-MAPPING-CAD.md)

---

**System Card Version**: 1.0 | **Valid Until**: 21 May 2026 | **Next Review**: Q1 2026 or on rule update
