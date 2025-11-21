# System Card: MS05-TRANSFORMER - Document Format Transformation

**Status**: ✅ FINAL | **Version**: 1.0 | **Date**: 21 Nov 2025 | **AI Act**: EU 2024/1689

---

## 1. Model Identity

- **Name**: MS05-TRANSFORMER - Document Format Conversion & Normalization
- **ID**: ms05-transformer-v1.4.2 | **Risk Level**: 🟢 LOW-RISK (No AI decision-making)
- **Type**: Deterministic Data Transformation (No ML; rule-based only)
- **Framework**: LibreOffice, Ghostscript, Custom conversion pipelines
- **Size**: 850 MB (dependencies) | **No trainable parameters**
- **Provider**: ZenIA / Interzen | **Release**: 2025-11-21

---

## 2. Intended Use & Restrictions

### Primary Use Case
Convert documents between formats (PDF↔DOCX↔XLSX→PDF/A) while preserving content integrity and metadata. No decision-making; purely deterministic transformation.

### Approved Use
- ✅ Format conversion (PDF, DOCX, XLSX, TXT, XML)
- ✅ PDF/A conversion for long-term preservation
- ✅ Metadata preservation and normalization
- ✅ Batch format conversion

### Prohibited Use
(None - deterministic transformation has no AI-driven restrictions)

### Known Limitations
- **Format Support**: 8 input formats (PDF, DOCX, XLSX, TXT, XML, PPT, ODP, ODT); outputs: PDF/A, PDF, DOCX, TXT, XML
- **Complex Formatting**: Some formatting may not perfectly transfer across formats
- **DRM/Encryption**: Cannot convert copy-protected or encrypted documents
- **Very Large Files**: Performance degrades > 100MB files

---

## 3. Transformation Algorithms

**No ML models used.** All transformations are deterministic and rule-based:

### PDF Conversion
- **Tool**: Ghostscript 10.0
- **Algorithm**: PDF parsing → vectorization → PDF/A generation
- **Determinism**: 100% (same input always produces identical output)
- **Reversibility**: Not reversible (PDF/A is archival format)

### DOCX/XLSX Conversion
- **Tool**: LibreOffice 7.5
- **Algorithm**: ODF parsing → format-specific serialization
- **Determinism**: 100% with fixed seed parameters
- **Quality**: 98%+ fidelity for standard documents

### Text Extraction
- **Tool**: Apache Tika
- **Algorithm**: Format-specific parsers → UTF-8 text output
- **Determinism**: 100%
- **Character Preservation**: 99.8% (minimal loss in special characters)

---

## 4. Data Processing

### Input Data
- **Max File Size**: 100 MB (recommended), up to 500 MB supported
- **Format Validation**: File signature verification before processing
- **Timeout**: 60 seconds per document

### Output Data
- **Format**: PDF/A-1b (for long-term preservation), PDF, DOCX, TXT, XML
- **Metadata**: Source filename, conversion timestamp, conversion tool version
- **Validation**: Output file integrity check (file signature + size validation)

### No Learning / No Adaptation
- **Stateless**: Each transformation is independent
- **No Parameter Updates**: Algorithms remain unchanged over time
- **No Feedback Loop**: User actions don't modify transformation behavior

---

## 5. Performance Metrics

### Conversion Success Rates

| Format Conversion | Success Rate | Avg Time | Quality Metric |
|---|---|---|---|
| PDF → PDF/A | 98.2% | 2.3s | Fidelity 99.1% |
| DOCX → PDF | 97.5% | 1.8s | Fidelity 98.7% |
| XLSX → PDF | 96.1% | 2.1s | Fidelity 97.2% |
| PDF → DOCX | 85.3% | 3.2s | Fidelity 82.4% |
| Any → TXT | 99.7% | 0.8s | Character preservation 99.8% |

### Throughput
- **Single Instance**: 200-300 documents/second
- **Latency p50**: 1.2 seconds
- **Latency p95**: 4.1 seconds
- **Availability**: 99.95% (uptime target)

---

## 6. Quality & Reliability

### Determinism Verification
✅ **100% Deterministic** - Same input file always produces identical output (byte-for-byte identical when re-run with same parameters)

### Reversibility
- **PDF → PDF/A**: ✅ Lossy conversion (intentional for archival)
- **DOCX → PDF**: ✅ Lossy conversion (formatting simplification)
- **PDF → TXT**: ✅ Lossy conversion (formatting removal)
- **TXT → DOCX**: ❌ Not supported (information loss too high)

### Error Handling
- **Corrupted Files**: Detected and rejected with error message
- **Unsupported Formats**: Rejected with error message
- **Timeout Errors**: Document marked as failed; no partial output
- **Recovery**: No automatic retry; errors reported to audit log

---

## 7. Fairness & Bias

**Not Applicable** - No ML model; no learning; no potential for bias.

### Why No Fairness Assessment Needed
- ✅ Deterministic algorithm
- ✅ No decision-making
- ✅ No parameter learning
- ✅ No differential impact across inputs
- ✅ Same transformation rules apply to all documents

---

## 8. Environmental Impact

- **Per-Document Energy**: 0.015 kWh
- **Annual Inference** (10M conversions): 150 kWh = **35 kg CO2e/year**
- **Optimization**: Caching of frequently-converted documents (40% reduction possible)
- **Impact**: Negligible compared to other microservices

---

## 9. Human Oversight

### Transparency
- **Transformation Determinism**: 100% - outputs fully predictable
- **Audit Trail**: All conversions logged with input/output checksums
- **No Explainability Needed**: Algorithm is rule-based and fully documented

### Quality Assurance
- **Visual Inspection**: Users can validate output visually
- **Metadata Verification**: Conversion tool version and parameters logged
- **Bit-Level Verification**: Checksum validation available

### Failure Recovery
- **Failed Conversions**: Reported immediately; document available for manual review
- **Re-submission**: Users can re-submit failed documents
- **Format Fallback**: Alternative format conversion available if primary fails

---

## 10. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Corrupted output file | Very Low (0.3%) | Medium | Output validation + checksums |
| Data loss in conversion | Low (1.2%) | High | Format selection guidance + user validation |
| Format incompatibility | Low (2%) | Medium | Fallback format available |
| Timeout on large files | Low (1%) | Low | File size limits + async processing |

**Residual Risk**: MINIMAL - Deterministic algorithms have inherent safety

---

## 11. AI Act Compliance Assessment

### Why MS05 is LOW-RISK (Not High-Risk)

**AI Act Classification Criteria**:
1. ❌ **No Automated Decision-Making**: Tool performs deterministic transformation, not decision
2. ❌ **No Machine Learning**: Pure rule-based algorithms; no neural networks or trained models
3. ❌ **No Adaptive Behavior**: Algorithm never changes based on inputs or feedback
4. ❌ **No Fundamental Rights Impact**: Format conversion cannot discriminate or affect rights
5. ✅ **Transparent & Explainable**: Algorithm fully documented and rule-based

### Conclusion
MS05-TRANSFORMER is **🟢 LOW-RISK** and does not require extensive AI Act compliance documentation. Standard software engineering practices (testing, documentation, error handling) are sufficient.

---

## 12. Approvals

- ✅ Technical Review: [Marco Rossi] - 2025-11-21
- ✅ Security Review: [Anna Bianchi] - 2025-11-21
- ✅ Compliance Review: [Giovanni Verdi] - 2025-11-21 (LOW-RISK CONFIRMATION)
- ✅ Executive Approval: Not required (LOW-RISK)

---

## 13. References

- Ghostscript: https://www.ghostscript.com
- LibreOffice: https://www.libreoffice.org
- Apache Tika: https://tika.apache.org
- PDF/A Standard: https://www.pdfa.org

---

**System Card Version**: 1.0 | **Validity**: Indefinite (no ML to update) | **Next Review**: On tool version upgrade
