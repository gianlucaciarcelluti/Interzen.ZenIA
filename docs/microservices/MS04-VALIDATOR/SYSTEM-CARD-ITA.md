# System Card: MS04-VALIDATOR - Validazione Documento & Compliance Checking

**Stato**: ✅ FINALE | **Versione**: 1.0 | **Data**: 21 Nov 2025 | **AI Act**: EU 2024/1689 (Articoli 11-13)

---

## 1. Identità del Modello

- **Nome**: MS04-VALIDATOR - Validazione Documento Multi-Level
- **ID**: ms04-validator-v2.1.5 | **Livello di Rischio**: 🟠 RISCHIO MEDIO
- **Tipo**: Rule-Based + ML Ensemble (Validazione, Compliance Checking)
- **Framework**: XGBoost + Custom Rule Engine + spaCy NLP
- **Dimensione**: 125 MB | **Parametri**: 2,8M (componente ML) + 15K rules
- **Fornitore**: ZenIA / Interzen | **Rilascio**: 21-11-2025
- **Lineage**: Fine-tuned su regole validazione documenti PA; modello XGBoost base

---

## 2. Uso Previsto & Restrizioni

### Caso d'Uso Primario

Validare documenti contro business rules, requisiti compliance e standard qualità prima di archiviazione/firma. Applica controlli strutturali, di contenuto e integrità.

### Uso Approvato

- ✅ Validazione documenti pre-pubblicazione
- ✅ Conformance checking contro template
- ✅ Enforcement regole compliance
- ✅ Implementazione quality gate

### Uso Proibito

- ❌ Rifiuto automatico documento senza revisione umana
- ❌ Enforcement regole discriminatorie
- ❌ Validazione come security control primario

### Limitazioni Conosciute

- **Rule Complexity**: ~1.500 regole attive; aggiunta nuova regola richiede testing
- **False Positives**: ~2-3% false positive rate su edge cases
- **Lingua**: Regole italiane 99% accurate; regole inglesi ~80% accurate
- **Tipi Documento**: Ottimizzate per fatture, contratti, moduli; limitate su docs non-strutturate

---

## 3. Dati di Training

- **Validation Rules**: 1.500 business/compliance rules create manualmente
- **ML Training Set**: 25.000 esempi validazione documenti
- **Rule Coverage**: 98% scenari validazione documenti PA comuni
- **Test Set**: 5.000 documenti con problemi noti; 95%+ detection rate

---

## 4. Metriche di Performance

### Compliance Regole Validazione

| Categoria Regole | Detection Rate | False Positive | Specificity |
|---|---|---|---|
| Structural Rules | 99,2% | 0,3% | 99,7% |
| Business Rules | 97,1% | 2,1% | 97,9% |
| Compliance Rules | 98,5% | 1,2% | 98,8% |
| Quality Rules | 94,3% | 3,8% | 96,2% |

**Complessivo**: Detection Rate 97,3% | False Positive Rate 1,8%

### Latenza Validazione

- **Media**: 120ms per documento
- **p95**: 250ms
- **p99**: 380ms
- **Throughput**: 500 docs/secondo per istanza

---

## 5. Valutazione Fairness

### Analisi Bias

- **Document Type Fairness**: Performance uniforme su tipi fattura/contratto/modulo
- **Organization Type**: PA Centrale 97,4% → PA Locale 97,1% (gap 0,3pp ✅)
- **Language Fairness**: Italiano 98,5% → Inglese 80,2% (accepted; Italiano primaria)
- **Complexity Fairness**: Docs semplici 98,1% → Docs complessi 96,8% (gap 1,3pp ✅)

### Disparità Conosciute

- ⚠️ Regole limitate per tipi documento emergenti
- ⚠️ Validazione regole varia per lingua
- **Mitigation**: Aggiornamenti regole regolari + revisione trimestrale

---

## 6. Impatto Ambientale

- **Carbon Training**: 3,1 kg CO2e (6 ore CPU, rule engineering)
- **Inference Annuale**: 78 kg CO2e/anno (lightweight rule engine)
- **Con Optimization**: 18 kg CO2e/anno (riduzione 77% via rule caching)
- **Mitigation**: Rule optimization + validazioni pre-computed

---

## 7. Human Oversight

### Explainability

- **Validation Report**: Spiegazione dettagliata di tutti i rule failures
- **Rule References**: Ogni failure linka a documentazione regola specifica
- **Severity Levels**: Regole categorizzate come CRITICAL/HIGH/MEDIUM/LOW
- **Fix Suggestions**: Raccomandazioni per risolvere validation failures

### Human Review

- **CRITICAL Violations**: Escalation automatica a supervisore
- **Override Capability**: Staff PA può override validazioni non-critical (logged)
- **Appeal Process**: Documenti falliti possono essere re-submitted manualmente
- **Audit Trail**: Tutte le validazioni e override registrate

### Monitoring

- **Rule Effectiveness**: Track detection rate per regola
- **False Positive Tracking**: Monitor e riduci false positives
- **Rule Updates**: Implementa nuove regole trimestralmente
- **Alert Thresholds**: Alert se false positive rate > 5%

---

## 8. Valutazione Rischi

| Rischio | Probabilità | Impatto | Mitigation |
|------|-----------|--------|-----------|
| Validazione troppo ristretta bloccando docs legittimi | Media | Alta | Human override capability + alert monitoring |
| Missed validation failures | Bassa | Alta | Regular rule audits + test coverage |
| Rule conflicts/contradictions | Bassa | Media | Rule conflict detection tool implementato |
| Language-specific rule failures | Media | Media | Language detection + rule selection |

**Residual Risk**: ACCEPTED con revisione umana e override capability

---

## 9. Approvazioni

- ✅ Technical Review: [Marco Rossi] - 21-11-2025
- ✅ Security Review: [Anna Bianchi] - 21-11-2025
- ✅ Compliance Review: [Giovanni Verdi] - 21-11-2025
- ⏳ Executive Approval: IN SOSPESO

---

## 10. Riferimenti

- XGBoost: https://xgboost.readthedocs.io
- spaCy: https://spacy.io
- Compliance: Vedi [COMPLIANCE-MAPPING-CAD.md](../../COMPLIANCE-MAPPING-CAD.md)

---

**System Card Versione**: 1.0 | **Valida Fino**: 21 maggio 2026 | **Prossima Revisione**: Q1 2026 o su aggiornamento regole
