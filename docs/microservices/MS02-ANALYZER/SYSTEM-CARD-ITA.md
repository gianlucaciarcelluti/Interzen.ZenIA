# System Card: MS02-ANALYZER - Analisi Documenti & Estrazione Entità

**Stato**: ✅ FINALE | **Versione**: 1.0 | **Data**: 21 Nov 2025 | **AI Act**: EU 2024/1689 (Articoli 11-13)

---

## 1. Identità del Modello

- **Nome**: MS02-ANALYZER - Analisi Semantica & Estrazione Entità
- **ID**: ms02-analyzer-v1.8.2 | **Livello di Rischio**: 🟠 RISCHIO MEDIO
- **Tipo**: Multi-task NLP (Estrazione Entità, Analisi Semantica, Analisi Sentiment)
- **Framework**: spaCy 3.5 + Transformers (DistilBERT + custom transformers)
- **Dimensione**: 340 MB | **Parametri**: 8,5M | **Licenza**: Apache 2.0
- **Fornitore**: ZenIA / Interzen | **Rilascio**: 21-11-2025
- **Lineage**: Fine-tuned su documenti PA italiani; modello base: spacy-it-core-news-lg

---

## 2. Uso Previsto & Restrizioni

### Caso d'Uso Primario

Estrarre e classificare entità nominate (persone, organizzazioni, ubicazioni, importi, date) da documenti PA italiani per supportare l'analisi documenti, compilazione template e ricerca semantica.

### Uso Approvato

- ✅ Estrazione entità da documenti
- ✅ Analisi semantica per comprensione contenuti
- ✅ Estrazione informazioni per popolamento database
- ✅ Estrazioni solo revisionate da umani

### Uso Proibito

- ❌ Estrazione automatica PII senza governance
- ❌ Cross-linking entità persone per sorveglianza
- ❌ Profiling automatico basato su entità estratte

### Limitazioni Conosciute

- **Lingua**: Italiano primaria (96%+ accuracy); Inglese ~80% accuracy
- **Tipi Entità**: 12 tipi (Persona, Organizzazione, Ubicazione, Data, Importo, Codice_Fiscale, Email, Telefono, Tipo_Contratto, Livello_Rischio, Dipartimento, Altro)
- **Performance**: Ottimale su documenti formali (contratti, fatture); variabile su corrispondenza informale
- **Dipendenza OCR**: Richiede qualità OCR > 85%

---

## 3. Dati di Training

- **Dataset**: 32.000 documenti PA italiani, annotati manualmente con entità
- **Qualità Annotazioni**: Accordo inter-annotatore 94%
- **Split Dati**: 70% training, 15% validation, 15% test
- **Distribuzione Entità**: Bilanciata su tutti i 12 tipi di entità
- **GDPR**: Tutti i PII rimossi post-annotazione; dataset anonimizzato conservato

---

## 4. Metriche di Performance

### Performance Riconoscimento Entità (Test Set)

| Tipo Entità | Precision | Recall | F1-Score | Support |
|-----------|-----------|--------|----------|---------|
| PERSONA | 0,92 | 0,88 | 0,90 | 2.400 |
| ORGANIZZAZIONE | 0,89 | 0,85 | 0,87 | 1.800 |
| UBICAZIONE | 0,85 | 0,82 | 0,83 | 1.200 |
| DATA | 0,96 | 0,94 | 0,95 | 2.000 |
| IMPORTO | 0,91 | 0,89 | 0,90 | 1.600 |
| CODICE_FISCALE | 0,98 | 0,97 | 0,975 | 1.400 |
| EMAIL | 0,97 | 0,96 | 0,965 | 800 |
| TELEFONO | 0,94 | 0,92 | 0,93 | 600 |

**Complessivo**: F1 Macro = 0,908 | F1 Weighted = 0,913

### Performance Analisi Semantica

- Somiglianza semantica (cosine): 0,89 correlazione con rating somiglianza umana
- Topic modeling: 84% coherence score
- Sentiment detection: 87% accuracy (classificazione 3-way)

---

## 5. Valutazione Fairness

### Analisi Bias

- **Language Fairness**: Italiano 96% → Inglese 80% (accettabile; Italiano è primaria)
- **Entity Type Fairness**: Performance uniforme su tipi di entità (Macro F1 std dev: 0,04)
- **Document Complexity**: Docs semplici 94% F1 → Docs complessi 87% F1 (gap 6pp accettabile)
- **Organization Type Fairness**: PA Centrale 91,5% → PA Locale 89,8% (disparità 1,7pp ✅)

### Disparità Conosciute

- ⚠️ Performance ridotta su formati documento non-standard
- ⚠️ Accuracy inferiore per nomi entità non comuni (< 95% accuracy)
- **Mitigation**: Revisione manuale per estrazioni bassa-confidenza (< 0,75)

---

## 6. Impatto Ambientale

- **Carbon Training**: 8,3 kg CO2e (12 ore GPU training)
- **Inference Annuale**: 342 kg CO2e/anno (baseline)
- **Con Optimization**: 82 kg CO2e/anno (riduzione 76% via batching + caching)
- **Mitigation**: Model distillation implementata (18% speedup inference)

---

## 7. Human Oversight

### Explainability

- **Confidence Scores**: Per-entity confidence (0.0-1.0)
- **Highlighting**: Attention visualization mostrando quale testo ha influenzato il riconoscimento entità
- **Alternatives**: Top-3 tipi entità alternativi forniti per estrazioni ambigue

### Human Review

- **Automatic Escalation**: Confidence < 0,70 → coda revisione manuale
- **Override Capability**: Staff PA può correggere/override tutte le estrazioni
- **Audit Trail**: Tutte le correzioni registrate per feedback

### Monitoring

- **Real-Time Metrics**: Entity recognition accuracy per tipo
- **Drift Detection**: Alert se accuracy scende > 3%
- **Retraining**: Trimestrale con nuovi esempi annotati

---

## 8. Valutazione Rischi

| Rischio | Probabilità | Impatto | Mitigation |
|------|-----------|--------|-----------|
| Estrazione entità persona incorretta | Media | Alta | Threshold confidenza + revisione manuale |
| False positive rilevamento organizzazione | Media | Media | Validazione contro registry aziende |
| PII exposure in entità estratte | Bassa | Critica | Governance policy PII + audit |
| Concept drift nel tempo | Media | Media | Retraining trimestrale + monitoring |

**Residual Risk**: ACCEPTED con monitoring e processo revisione manuale

---

## 9. Approvazioni

- ✅ Technical Review: [Marco Rossi] - 21-11-2025
- ✅ Security Review: [Anna Bianchi] - 21-11-2025
- ✅ Compliance Review: [Giovanni Verdi] - 21-11-2025
- ⏳ Executive Approval: IN SOSPESO

---

## 10. Riferimenti

- spaCy Documentation: https://spacy.io
- Transformers: https://huggingface.co/docs/transformers
- Compliance: Vedi [COMPLIANCE-MAPPING-AI-ACT.md](../../COMPLIANCE-MAPPING-AI-ACT.md)

---

**System Card Versione**: 1.0 | **Valida Fino**: 21 maggio 2026 | **Prossima Revisione**: Q1 2026 o su aggiornamento modello
