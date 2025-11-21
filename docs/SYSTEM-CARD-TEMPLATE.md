# System Card Template - EU AI Office Standard

**Version**: 1.0
**Last Updated**: 21 novembre 2025
**Status**: TEMPLATE FOR AI ACT COMPLIANCE

---

## Overview

Questo template definisce la struttura standard per System Card secondo i requisiti dell'EU AI Regulation 2024/1689 (AI Act, Articoli 11-13).

Una System Card è un documento tecnico che fornisce informazioni complete su un sistema di IA ad alto rischio, includendo:
- Identità e versioning del modello
- Caratteristiche dei dati di training
- Metriche di performance
- Valutazione di fairness e bias
- Impatto ambientale
- Limitazioni note e raccomandazioni d'uso

---

## Sezioni Standard per System Card

### 1. Model Identity & Versioning

**Scopo**: Identificare univocamente il modello e tracciarne l'evoluzione

**Contenuti richiesti**:

```markdown
#### Model Identity
- **Model Name**: [Nome del modello]
- **Model ID**: [ID univoco, es. ms01-classifier-v2.3.1]
- **Version**: [Semantic versioning: major.minor.patch]
- **Release Date**: [Data rilascio YYYY-MM-DD]
- **Provider Organization**: ZenIA / Interzen
- **Provider Contact**: [email/team]
- **Model Type**: [Classification / Detection / Extraction / Transformation / Validation]
- **Implementation Language**: [Python / Java / etc.]
- **Framework/Library**: [TensorFlow / PyTorch / scikit-learn / etc.]
- **License**: [Apache 2.0 / MIT / etc.]

#### Model Lineage
- **Parent Model(s)**: [Se fine-tuned, indicare modello base]
- **Training Date**: [Data inizio training]
- **Last Updated**: [Data ultimo update]
- **Deprecation Status**: [Active / Deprecated / Planned for Sunset]
- **Sunset Date**: [Se applicabile]
```

---

### 2. Intended Use & Restrictions

**Scopo**: Definire chiaramente l'uso previsto e le limitazioni

**Contenuti richiesti**:

```markdown
#### Primary Use Case
- **Objective**: [Descrizione dell'obiettivo principale]
- **Input Data Type**: [Tipo di dati in input: documents, entities, metadata, etc.]
- **Output Format**: [Tipo di output: classification, scores, entities, etc.]
- **User Demographic**: [PA administrators / Document processors / etc.]
- **Application Domain**: [Document management / Compliance checking / etc.]

#### Approved Use Cases
- [ ] Use case 1: [Descrizione]
- [ ] Use case 2: [Descrizione]
- [ ] Use case 3: [Descrizione]

#### Prohibited Use Cases
- ❌ Real-time biometric identification
- ❌ Social scoring
- ❌ Discriminatory profiling
- ❌ [Andere use cases da escludere]

#### Known Limitations
- **Data Type Restrictions**: [Es: solo documenti PDF e TXT]
- **Language Support**: [Es: Italian primary, English secondary]
- **Quality Dependencies**: [Es: requires OCR quality > 85%]
- **Performance Thresholds**: [Es: confidence > 0.7 recommended]
- **Scale Limitations**: [Es: batch processing only, max 1000 docs/hour]
- **Failure Modes**: [Descrizione dei scenari di fallimento noti]

#### Recommendations for Safe Use
- Recommendation 1: [Es: Use confidence thresholds for filtering]
- Recommendation 2: [Es: Implement human review for edge cases]
- Recommendation 3: [Es: Monitor performance metrics in production]
```

---

### 3. Training Data Characteristics

**Scopo**: Fornire tracciabilità completa dei dati di training (GDPR + AI Act)

**Contenuti richiesti**:

```markdown
#### Data Collection
- **Data Source(s)**: [Fonte dati: internal PA documents / public datasets / etc.]
- **Collection Period**: [Data inizio - Data fine]
- **Licensing**: [Type of licenses for training data]
- **Data Governance**: [Compliance con GDPR, diritti d'autore]
- **Consent**: [Informed consent obtained: Yes/No/N.A.]

#### Dataset Characteristics
- **Total Samples**: [Numero esempi nel training set]
- **Training/Validation/Test Split**: [Es: 70% / 15% / 15%]
- **Sample Size per Class**:
  - Class A: [N samples]
  - Class B: [N samples]
  - Class C: [N samples]

#### Data Quality Assessment
- **Missing Data Rate**: [% valori mancanti]
- **Outlier Detection**: [Metodo e risultati]
- **Duplicate Samples**: [% duplicati, metodo di rimozione]
- **Data Cleaning Process**: [Descrizione preprocessing]
- **Quality Score**: [Score 0-100]

#### Demographic Representation
- **Geographic Coverage**: [Es: 80% Italy, 20% EU]
- **Temporal Coverage**: [Es: 2020-2025]
- **Document Type Distribution**: [Es: 40% invoices, 30% contracts, 30% other]
- **Diversity Assessment**: [Analisi fairness across demographic groups]
  - By document type: [Percentuali]
  - By language: [Percentuali]
  - By complexity level: [Percentuali]

#### Data Augmentation
- **Augmentation Techniques**: [Es: paraphrasing, back-translation]
- **Augmentation Ratio**: [% synthetic data]
- **Quality Controls**: [Metodo validazione dati augmentati]
```

---

### 4. Model Architecture & Performance

**Scopo**: Descrivere l'architettura tecnica e le metriche di performance

**Contenuti richiesti**:

```markdown
#### Model Architecture
- **Architecture Type**: [Es: Transformer-based, CNN, RNN, etc.]
- **Architecture Details**: [Descrizione layer/componenti principali]
- **Number of Parameters**: [Totale e breakdown]
- **Model Size**: [MB/GB on disk]
- **Inference Latency**: [Tempo medio predizione in ms]
- **Batch Processing**: [Supportato: Yes/No, size]

#### Training Configuration
- **Hyperparameters**:
  - Learning rate: [Valore iniziale e schedule]
  - Batch size: [Numero]
  - Epochs: [Numero]
  - Optimizer: [Es: Adam, SGD]
  - Loss function: [Tipo]
  - Regularization: [Dropout, L1/L2, etc.]

- **Early Stopping**: [Criterio di stop]
- **Cross-Validation**: [Metodo usato]

#### Performance Metrics
- **Accuracy**: [Percentuale]
- **Precision**: [Per classe se multi-class]
- **Recall**: [Per classe se multi-class]
- **F1-Score**: [Valore]
- **AUC-ROC**: [Valore, se applicabile]
- **Confusion Matrix**: [Tabella o descrizione]
- **Per-Class Performance**: [Breakdown per classe]

#### Robustness Testing
- **Adversarial Examples**: [Metodo test, risultati]
- **Out-of-Distribution Performance**: [Test su dati diversi da training]
- **Noise Robustness**: [Robustezza a rumore/OCR errors]
- **Edge Cases Performance**: [Performance su casi limite noti]
- **Performance Degradation**: [Come performain condizioni degradate]

#### Baseline Comparisons
- **Baseline Model**: [Modello di confronto]
- **Performance Improvement**: [Percentuale miglioramento]
- **Comparison Methodology**: [Come è stato fatto il confronto]
```

---

### 5. Fairness Assessment

**Scopo**: Valutare potenziali bias e disparità nel modello

**Contenuti richiesti**:

```markdown
#### Bias Analysis
- **Protected Attributes Identified**:
  - Attribute 1: [Es: language, document type]
  - Attribute 2: [Es: complexity level]

#### Fairness Metrics
- **Demographic Parity**: [Descrizione e risultati]
- **Equalized Odds**: [Descrizione e risultati]
- **Disparate Impact**: [Analisi per protected attributes]
- **Calibration**: [Sono le confidenze calibrate across groups?]

#### Bias Evaluation Results
- **Group-Level Performance**:
  - Group A: Accuracy [X]%, Precision [Y]%, Recall [Z]%
  - Group B: Accuracy [X]%, Precision [Y]%, Recall [Z]%
  - Performance Gap: [Massima differenza]

- **Identified Disparities**: [Descrizione di disparità trovate]
- **Root Cause Analysis**: [Perché esistono disparità]

#### Bias Mitigation Strategies
- **Strategy 1**: [Descrizione, es: balanced sampling]
- **Strategy 2**: [Descrizione, es: fairness constraints]
- **Strategy 3**: [Descrizione, es: post-processing]
- **Effectiveness**: [Come è stata misurata]

#### Fairness Limitations
- **Known Fairness Issues**: [Issues non risolti]
- **Future Mitigation Plans**: [Plans per future versions]

#### Human Review Process
- **Fairness Review Criteria**: [Criteri usati]
- **Review Team**: [Chi ha fatto la review]
- **Review Date**: [Data review]
- **Approval Status**: [Approvato/Conditional/Rejected]
```

---

### 6. Environmental Impact

**Scopo**: Quantificare l'impatto ambientale del modello (AI Act requirement)

**Contenuti richiesti**:

```markdown
#### Training Carbon Footprint
- **Total Energy Consumption**: [kWh]
- **Training Duration**: [ore]
- **CO2 Emissions**: [kg CO2e]
- **Carbon Intensity**: [gCO2e per kWh]
- **Data Center Location**: [Energia green %]

#### Inference Carbon Footprint
- **Average Inference Energy**: [Wh per inference]
- **Expected Annual Requests**: [Numero]
- **Annual Inference Carbon**: [kg CO2e/year]

#### Optimization Measures
- **Model Compression**: [Distillation / Quantization / Pruning]
- **Inference Optimization**: [Batch processing / Caching]
- **Green Hosting**: [Energy provider info]
- **Efficiency Targets**: [Target riduzione CO2]

#### Total Lifecycle Impact
- **Estimated Lifecycle Emissions**: [kg CO2e]
- **Equivalent Carbon Offset**: [Descrizione]
```

---

### 7. Human Oversight & Explainability

**Scopo**: Descrivere come il modello è trasparente e come gli umani lo controllano

**Contenuti richiesti**:

```markdown
#### Model Explainability
- **Interpretability Methods**:
  - Feature importance: [Metodo, es: SHAP]
  - Attention mechanisms: [Se presente]
  - Saliency maps: [Se applicabile]
  - Local explanations: [LIME / similar]

- **Explanation Availability**: [Sempre disponibile / On request / N.A.]
- **User-Facing Explanations**: [Come spiegate le decisioni agli utenti]

#### Decision Transparency
- **Confidence Scores**: [Forniti: Yes/No]
- **Decision Rationale**: [Come è spiegata la decisione]
- **Alternative Decisions**: [Considerate durante inference]
- **Uncertainty Quantification**: [Come misurat]

#### Human Override Capability
- **Human Review Process**: [Descrizione flusso review]
- **Override Mechanism**: [Come si può rifiutare una decisione del modello]
- **Escalation Procedure**: [Quando escalare a supervisori]
- **Audit Trail**: [Come si registra override e motivazioni]

#### Monitoring & Performance Tracking
- **Performance Monitoring**: [Come si monitora in produzione]
- **Drift Detection**: [Come si rileva data/model drift]
- **Retraining Triggers**: [Quando si fa retraining]
- **Performance Dashboards**: [Metriche visibili]

#### User Training & Documentation
- **User Guide**: [Documentazione per PA operators]
- **Training Materials**: [Se disponibili]
- **FAQ**: [Common questions e answers]
- **Support Contact**: [Chi contattare per problemi]
```

---

### 8. Risk Assessment & Mitigation

**Scopo**: Identificare rischi specifici del modello e come sono mitigati

**Contenuti richiesti**:

```markdown
#### Risk Identification
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Bias against specific document types | Medium | High | Fairness testing + stratified sampling |
| Catastrophic performance on edge cases | Low | Critical | Human review escalation |
| Model poisoning via training data | Very Low | Critical | Data validation + audit trail |
| Concept drift over time | Medium | Medium | Monitoring + periodic retraining |

#### Residual Risks
- **Risk 1**: [Descrizione di rischi rimasti dopo mitigation]
- **Risk 2**: [...]
- **Acceptance Criteria**: [Chi ha accettato questi rischi]

#### Insurance & Liability
- **Product Liability Insurance**: [Coverage details]
- **Liability Allocation**: [Provider vs. User responsibility]
```

---

### 9. Appendices & Supporting Data

**Scopo**: Fornire dati supplementari per audit e compliance

**Contenuti richiesti**:

```markdown
#### A. Confusion Matrix Details
[Tabella completa con tutti numeri]

#### B. Performance by Document Type
[Breakdown dettagliato per ogni tipo documento]

#### C. Fairness Analysis Charts
[Grafici delle disparità per protected attributes]

#### D. Training Dataset Sample
[Campione anonimizzato di training data, per illustrazione]

#### E. Model Artifacts
- Model weights: [Percorso/URL]
- Tokenizer: [Details]
- Configuration: [Config file]
- Dependencies: [requirements.txt]

#### F. References & Citations
- [Pubblicazioni scientifiche su cui basato]
- [Dataset papers se usati public datasets]
- [Regulatory references]

#### G. Change History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-21 | Initial System Card | [Name] |
| 1.1 | [Date] | [Changes] | [Author] |

#### H. Sign-Off & Approvals
- **ML Engineer Review**: [Name], [Date]
- **Security Review**: [Name], [Date]
- **Compliance Review**: [Name], [Date]
- **Executive Approval**: [Name], [Date]
```

---

## Guidelines for Completion

### Completeness Requirements

- ✅ Tutti i 9 sections devono essere completati
- ✅ Metriche quantitative (non solo qualitative)
- ✅ Comparisons with baselines
- ✅ Clear identification of risks and limitations
- ✅ Actionable remediation plans

### Transparency Standards

- ✅ Linguaggio accessibile (non solo tecnico jargon)
- ✅ Grafica e visualizzazioni dove possibile
- ✅ Numeri specifici (non vaghi come "good" o "adequate")
- ✅ Cross-references a documentation

### Evidence Requirements

- ✅ Dati tracciabili (modelli, dataset, metriche)
- ✅ Audit trail (quando creato, da chi, perché)
- ✅ Test results (non solo claim)
- ✅ Approvals (formali, non verbali)

---

## Validation Checklist

Prima di finalizzare una System Card:

### Content Completeness
- [ ] All 9 sections filled
- [ ] No "TBD" or placeholder text
- [ ] Quantitative metrics provided
- [ ] Risk assessment documented
- [ ] Mitigation strategies defined

### Quality Standards
- [ ] Performance metrics verified
- [ ] Fairness analysis conducted
- [ ] Environmental impact calculated
- [ ] Bias testing completed
- [ ] Human oversight process documented

### Regulatory Compliance
- [ ] AI Act Art. 13 requirements covered
- [ ] GDPR data provenance documented
- [ ] Transparency mechanisms described
- [ ] Audit trail capability confirmed
- [ ] Human override capability verified

### Approval Process
- [ ] Technical review completed
- [ ] Security review completed
- [ ] Compliance review completed
- [ ] All approvals documented
- [ ] Change history maintained

---

## System Card Review Process

### Review Workflow

1. **Draft Phase** (Author):
   - Complete all sections
   - Perform internal validation
   - Submit for review

2. **Technical Review** (ML Engineer/Data Scientist):
   - Verify technical accuracy
   - Check performance metrics
   - Validate training data description
   - Estimated time: 4 hours

3. **Security Review** (Security Officer):
   - Assess risk mitigation
   - Review data governance
   - Validate audit trail
   - Estimated time: 2 hours

4. **Compliance Review** (Compliance Officer):
   - Verify AI Act compliance
   - Check GDPR adherence
   - Validate CAD requirements
   - Estimated time: 3 hours

5. **Executive Approval** (CTO/Director):
   - Final sign-off
   - Risk acceptance
   - Deployment authorization
   - Estimated time: 1 hour

**Total Review Time**: ~10 hours per System Card

---

## Distribution & Update Schedule

### Publication
- All System Cards published in: `docs/microservices/MSxx/SYSTEM-CARD.md`
- All System Cards tracked in: `docs/SYSTEM-CARDS-REGISTRY.md`
- Version control: GitHub repository

### Maintenance
- Review schedule: Quarterly (or on model update)
- Update triggers:
  - Model retraining
  - New version release
  - Performance degradation detected
  - Regulatory requirement changes
  - Fairness concerns identified

### Archival
- Keep all historical versions
- Document rationale for changes
- Maintain change log per model

---

## Related Documents

- [COMPLIANCE-MAPPING-AI-ACT.md](COMPLIANCE-MAPPING-AI-ACT.md) - AI Act compliance requirements
- [COMPLIANCE-MAPPING-CAD.md](COMPLIANCE-MAPPING-CAD.md) - CAD audit requirements
- [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md) - Development standards
- EU AI Office: https://ec.europa.eu/info/research-and-innovation_en

---

*System Card Template - EU AI Office Standard (Nov 2025)*
