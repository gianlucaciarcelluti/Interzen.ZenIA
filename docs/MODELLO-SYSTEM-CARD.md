# Modello System Card - Standard EU AI Office

**Versione**: 1.0
**Ultimo Aggiornamento**: 21 novembre 2025
**Stato**: MODELLO PER CONFORMITÀ AI ACT

---

## Panoramica

Questo modello definisce la struttura standard per le System Card secondo i requisiti del Regolamento UE sull'IA 2024/1689 (AI Act, Articoli 11-13).

Una System Card è un documento tecnico che fornisce informazioni complete su un sistema di IA ad alto rischio, includendo:
- Identità e versionamento del modello
- Caratteristiche dei dati di training
- Metriche di performance
- Valutazione di fairness e bias
- Impatto ambientale
- Limitazioni note e raccomandazioni d'uso

---

## Sezioni Standard per System Card

### 1. Identità del Modello e Versionamento

**Scopo**: Identificare univocamente il modello e tracciarne l'evoluzione

**Contenuti richiesti**:

```markdown
#### Identità del Modello
- **Nome Modello**: [Nome del modello]
- **ID Modello**: [ID univoco, es. ms01-classificatore-v2.3.1]
- **Versione**: [Versionamento semantico: major.minor.patch]
- **Data Rilascio**: [Data rilascio AAAA-MM-GG]
- **Organizzazione Provider**: ZenIA / Interzen
- **Contatti Provider**: [email/team]
- **Tipo Modello**: [Classificazione / Rilevamento / Estrazione / Trasformazione / Validazione]
- **Linguaggio Implementazione**: [Python / Java / etc.]
- **Framework/Libreria**: [TensorFlow / PyTorch / scikit-learn / etc.]
- **Licenza**: [Apache 2.0 / MIT / etc.]

#### Genealogia del Modello
- **Modello Genitore**: [Se fine-tuned, indicare modello base]
- **Data Training**: [Data inizio training]
- **Ultimo Aggiornamento**: [Data ultimo update]
- **Stato Deprecazione**: [Attivo / Deprecato / Pianificato per Ritiro]
- **Data Ritiro**: [Se applicabile]
```

---

### 2. Uso Previsto e Restrizioni

**Scopo**: Definire chiaramente l'uso previsto e le limitazioni

**Contenuti richiesti**:

```markdown
#### Caso d'Uso Principale
- **Obiettivo**: [Descrizione dell'obiettivo principale]
- **Tipo Dati Input**: [Tipo di dati in input: documenti, entità, metadati, etc.]
- **Formato Output**: [Tipo di output: classificazione, punteggi, entità, etc.]
- **Profilo Utente**: [Amministratori PA / Processori documenti / etc.]
- **Dominio Applicativo**: [Gestione documenti / Controllo conformità / etc.]

#### Casi d'Uso Approvati
- [ ] Caso d'uso 1: [Descrizione]
- [ ] Caso d'uso 2: [Descrizione]
- [ ] Caso d'uso 3: [Descrizione]

#### Casi d'Uso Proibiti
- ❌ Identificazione biometrica in tempo reale
- ❌ Social scoring
- ❌ Profiling discriminatorio
- ❌ [Altri casi d'uso da escludere]

#### Limitazioni Note
- **Restrizioni Tipo Dati**: [Es: solo documenti PDF e TXT]
- **Supporto Linguistico**: [Es: italiano primario, inglese secondario]
- **Dipendenze Qualità**: [Es: richiede qualità OCR > 85%]
- **Soglie Performance**: [Es: confidenza > 0.7 consigliata]
- **Limitazioni Scala**: [Es: solo batch processing, max 1000 doc/ora]
- **Modalità Fallimento**: [Descrizione scenari di fallimento noti]

#### Raccomandazioni per Uso Sicuro
- Raccomandazione 1: [Es: Usare soglie di confidenza per filtraggio]
- Raccomandazione 2: [Es: Implementare revisione umana per casi edge]
- Raccomandazione 3: [Es: Monitorare metriche di performance in produzione]
```

---

### 3. Caratteristiche Dati di Training

**Scopo**: Fornire tracciabilità completa dei dati di training (GDPR + AI Act)

**Contenuti richiesti**:

```markdown
#### Raccolta Dati
- **Fonte Dati**: [Fonte dati: documenti PA interni / dataset pubblici / etc.]
- **Periodo Raccolta**: [Data inizio - Data fine]
- **Licenze**: [Tipo di licenze per dati di training]
- **Governance Dati**: [Conformità GDPR, diritti d'autore]
- **Consenso**: [Consenso informato ottenuto: Sì/No/N.A.]

#### Caratteristiche Dataset
- **Totale Campioni**: [Numero esempi nel training set]
- **Split Training/Validazione/Test**: [Es: 70% / 15% / 15%]
- **Dimensione Campioni per Classe**:
  - Classe A: [N campioni]
  - Classe B: [N campioni]
  - Classe C: [N campioni]

#### Valutazione Qualità Dati
- **Tasso Dati Mancanti**: [% valori mancanti]
- **Rilevamento Outlier**: [Metodo e risultati]
- **Campioni Duplicati**: [% duplicati, metodo rimozione]
- **Processo Pulizia Dati**: [Descrizione preprocessing]
- **Punteggio Qualità**: [Punteggio 0-100]

#### Rappresentazione Demografica
- **Copertura Geografica**: [Es: 80% Italia, 20% EU]
- **Copertura Temporale**: [Es: 2020-2025]
- **Distribuzione Tipo Documento**: [Es: 40% fatture, 30% contratti, 30% altro]
- **Valutazione Diversità**: [Analisi fairness su gruppi demografici]
  - Per tipo documento: [Percentuali]
  - Per linguaggio: [Percentuali]
  - Per livello complessità: [Percentuali]

#### Augmentazione Dati
- **Tecniche Augmentazione**: [Es: parafrasamento, back-translation]
- **Ratio Augmentazione**: [% dati sintetici]
- **Controlli Qualità**: [Metodo validazione dati augmentati]
```

---

### 4. Architettura del Modello e Performance

**Scopo**: Descrivere l'architettura tecnica e metriche di performance

**Contenuti richiesti**:

```markdown
#### Architettura del Modello
- **Tipo Architettura**: [Es: Transformer, CNN, RNN, etc.]
- **Dettagli Architettura**: [Descrizione layer/componenti principali]
- **Numero Parametri**: [Totale e breakdown]
- **Dimensione Modello**: [MB/GB su disco]
- **Latenza Inference**: [Tempo medio predizione in ms]
- **Batch Processing**: [Supportato: Sì/No, dimensione]

#### Configurazione Training
- **Iperparametri**:
  - Learning rate: [Valore iniziale e schedule]
  - Batch size: [Numero]
  - Epoche: [Numero]
  - Optimizer: [Es: Adam, SGD]
  - Funzione loss: [Tipo]
  - Regularization: [Dropout, L1/L2, etc.]

- **Early Stopping**: [Criterio di stop]
- **Cross-Validation**: [Metodo usato]

#### Metriche Performance
- **Accuracy**: [Percentuale]
- **Precision**: [Per classe se multi-classe]
- **Recall**: [Per classe se multi-classe]
- **F1-Score**: [Valore]
- **AUC-ROC**: [Valore, se applicabile]
- **Matrice di Confusione**: [Tabella o descrizione]
- **Performance Per-Classe**: [Breakdown per classe]

#### Test Robustezza
- **Esempi Avversariali**: [Metodo test, risultati]
- **Performance Out-of-Distribution**: [Test su dati diversi da training]
- **Robustezza Rumore**: [Robustezza a rumore/errori OCR]
- **Performance Casi Edge**: [Performance su casi limite noti]
- **Degradazione Performance**: [Comportamento in condizioni degradate]

#### Confronto Baseline
- **Modello Baseline**: [Modello di confronto]
- **Miglioramento Performance**: [Percentuale miglioramento]
- **Metodologia Confronto**: [Come è stato fatto il confronto]
```

---

### 5. Valutazione Fairness

**Scopo**: Valutare potenziali bias e disparità nel modello

**Contenuti richiesti**:

```markdown
#### Analisi Bias
- **Attributi Protetti Identificati**:
  - Attributo 1: [Es: linguaggio, tipo documento]
  - Attributo 2: [Es: livello complessità]

#### Metriche Fairness
- **Parità Demografica**: [Descrizione e risultati]
- **Equalized Odds**: [Descrizione e risultati]
- **Disparate Impact**: [Analisi per attributi protetti]
- **Calibrazione**: [Sono le confidenze calibrate tra gruppi?]

#### Risultati Valutazione Bias
- **Performance Livello Gruppo**:
  - Gruppo A: Accuracy [X]%, Precision [Y]%, Recall [Z]%
  - Gruppo B: Accuracy [X]%, Precision [Y]%, Recall [Z]%
  - Gap Performance: [Differenza massima]

- **Disparità Identificate**: [Descrizione di disparità trovate]
- **Analisi Root Cause**: [Perché esistono disparità]

#### Strategie Mitigazione Bias
- **Strategia 1**: [Descrizione, es: campionamento bilanciato]
- **Strategia 2**: [Descrizione, es: vincoli fairness]
- **Strategia 3**: [Descrizione, es: post-processing]
- **Effettività**: [Come è stata misurata]

#### Limitazioni Fairness
- **Problemi Fairness Noti**: [Issues non risolti]
- **Piani Mitigazione Futuri**: [Plans per future versioni]

#### Processo Revisione Umana
- **Criteri Revisione Fairness**: [Criteri usati]
- **Team Revisione**: [Chi ha fatto la review]
- **Data Revisione**: [Data review]
- **Stato Approvazione**: [Approvato/Condizionato/Rifiutato]
```

---

### 6. Impatto Ambientale

**Scopo**: Quantificare l'impatto ambientale del modello (requisito AI Act)

**Contenuti richiesti**:

```markdown
#### Carbon Footprint Training
- **Consumo Energetico Totale**: [kWh]
- **Durata Training**: [ore]
- **Emissioni CO2**: [kg CO2e]
- **Carbon Intensity**: [gCO2e per kWh]
- **Localizzazione Data Center**: [% energia green]

#### Carbon Footprint Inference
- **Energia Media Inference**: [Wh per inference]
- **Richieste Annuali Previste**: [Numero]
- **Carbon Annuale Inference**: [kg CO2e/anno]

#### Misure Ottimizzazione
- **Compressione Modello**: [Distillazione / Quantizzazione / Pruning]
- **Ottimizzazione Inference**: [Batch processing / Caching]
- **Hosting Green**: [Informazioni provider energia]
- **Target Efficienza**: [Target riduzione CO2]

#### Impatto Ciclo Vita Totale
- **Emissioni Ciclo Vita Stimate**: [kg CO2e]
- **Equivalente Carbon Offset**: [Descrizione]
```

---

### 7. Supervisione Umana e Spiegabilità

**Scopo**: Descrivere come il modello è trasparente e come gli umani lo controllano

**Contenuti richiesti**:

```markdown
#### Spiegabilità Modello
- **Metodi Interpretabilità**:
  - Feature importance: [Metodo, es: SHAP]
  - Attention mechanisms: [Se presente]
  - Saliency maps: [Se applicabile]
  - Local explanations: [LIME / similar]

- **Disponibilità Spiegazione**: [Sempre disponibile / On request / N.A.]
- **Spiegazioni User-Facing**: [Come spiegate le decisioni agli utenti]

#### Trasparenza Decisioni
- **Punteggi Confidenza**: [Forniti: Sì/No]
- **Razionale Decisione**: [Come è spiegata la decisione]
- **Decisioni Alternative**: [Considerate durante inference]
- **Quantificazione Incertezza**: [Come misurata]

#### Capacità Override Umano
- **Processo Revisione Umana**: [Descrizione flusso review]
- **Meccanismo Override**: [Come si può rifiutare una decisione del modello]
- **Procedura Escalation**: [Quando escalare a supervisori]
- **Audit Trail**: [Come si registra override e motivazioni]

#### Monitoraggio e Tracciamento Performance
- **Monitoraggio Performance**: [Come si monitora in produzione]
- **Rilevamento Drift**: [Come si rileva data/model drift]
- **Trigger Retraining**: [Quando si fa retraining]
- **Dashboard Performance**: [Metriche visibili]

#### Formazione Utenti e Documentazione
- **Guida Utente**: [Documentazione per operatori PA]
- **Materiali Formazione**: [Se disponibili]
- **FAQ**: [Domande comuni e risposte]
- **Contatto Supporto**: [Chi contattare per problemi]
```

---

### 8. Valutazione Rischi e Mitigazione

**Scopo**: Identificare rischi specifici del modello e come sono mitigati

**Contenuti richiesti**:

```markdown
#### Identificazione Rischi
| Rischio | Probabilità | Impatto | Mitigazione |
|---------|-------------|---------|-------------|
| Bias contro tipi documento specifici | Media | Alta | Test fairness + campionamento stratificato |
| Performance catastrofica su edge cases | Bassa | Critica | Escalation revisione umana |
| Poisoning dati di training | Molto bassa | Critica | Validazione dati + audit trail |
| Concept drift nel tempo | Media | Media | Monitoraggio + retraining periodico |

#### Rischi Residui
- **Rischio 1**: [Descrizione di rischi rimasti dopo mitigazione]
- **Rischio 2**: [...]
- **Criteri Accettazione**: [Chi ha accettato questi rischi]

#### Assicurazione e Responsabilità
- **Assicurazione Responsabilità Prodotto**: [Dettagli copertura]
- **Allocazione Responsabilità**: [Provider vs. Responsabilità Utente]
```

---

### 9. Appendici e Dati Supporto

**Scopo**: Fornire dati supplementari per audit e compliance

**Contenuti richiesti**:

```markdown
#### A. Dettagli Matrice di Confusione
[Tabella completa con tutti numeri]

#### B. Performance per Tipo Documento
[Breakdown dettagliato per ogni tipo documento]

#### C. Grafici Analisi Fairness
[Grafici delle disparità per attributi protetti]

#### D. Campione Dataset Training
[Campione anonimizzato di dati di training, per illustrazione]

#### E. Artefatti Modello
- Pesi modello: [Percorso/URL]
- Tokenizer: [Dettagli]
- Configurazione: [Config file]
- Dipendenze: [requirements.txt]

#### F. Riferimenti e Citazioni
- [Pubblicazioni scientifiche su cui basato]
- [Dataset papers se usati public datasets]
- [Riferimenti normativi]

#### G. Cronologia Cambiamenti
| Versione | Data | Cambiamenti | Autore |
|----------|------|-------------|--------|
| 1.0 | 2025-11-21 | System Card Iniziale | [Nome] |
| 1.1 | [Data] | [Cambiamenti] | [Autore] |

#### H. Firme e Approvazioni
- **Revisione Ingegnere ML**: [Nome], [Data]
- **Revisione Sicurezza**: [Nome], [Data]
- **Revisione Conformità**: [Nome], [Data]
- **Approvazione Esecutiva**: [Nome], [Data]
```

---

## Linee Guida per il Completamento

### Requisiti Completezza

- ✅ Tutte le 9 sezioni devono essere completate
- ✅ Metriche quantitative (non solo qualitative)
- ✅ Confronti con baseline
- ✅ Identificazione chiara di rischi e limitazioni
- ✅ Piani di rimedio attuabili

### Standard Trasparenza

- ✅ Linguaggio accessibile (non solo jargon tecnico)
- ✅ Grafica e visualizzazioni dove possibile
- ✅ Numeri specifici (non vaghi come "buono" o "adeguato")
- ✅ Cross-references alla documentazione

### Requisiti Evidenza

- ✅ Dati tracciabili (modelli, dataset, metriche)
- ✅ Audit trail (quando creato, da chi, perché)
- ✅ Risultati test (non solo claim)
- ✅ Approvazioni (formali, non verbali)

---

## Checklist di Validazione

Prima di finalizzare una System Card:

### Completezza Contenuto
- [ ] Tutte le 9 sezioni compilate
- [ ] No "TBD" o testo placeholder
- [ ] Metriche quantitative fornite
- [ ] Valutazione rischi documentata
- [ ] Strategie mitigazione definite

### Standard Qualità
- [ ] Metriche performance verificate
- [ ] Analisi fairness condotta
- [ ] Impatto ambientale calcolato
- [ ] Test bias completati
- [ ] Processo supervisione umana documentato

### Conformità Normativa
- [ ] Requisiti AI Act Art. 13 coperti
- [ ] Provenienza dati GDPR documentata
- [ ] Meccanismi trasparenza descritti
- [ ] Capacità audit trail confermata
- [ ] Capacità override umano verificata

### Processo Approvazione
- [ ] Revisione tecnica completata
- [ ] Revisione sicurezza completata
- [ ] Revisione conformità completata
- [ ] Tutte le approvazioni documentate
- [ ] Cronologia cambiamenti mantenuta

---

## Processo di Revisione System Card

### Workflow di Revisione

1. **Fase Draft** (Autore):
   - Compilare tutte le sezioni
   - Eseguire validazione interna
   - Sottoporre a revisione

2. **Revisione Tecnica** (Ingegnere ML/Data Scientist):
   - Verificare accuratezza tecnica
   - Controllare metriche performance
   - Validare descrizione dati training
   - Tempo stimato: 4 ore

3. **Revisione Sicurezza** (Officer Sicurezza):
   - Valutare mitigazione rischi
   - Revisionare data governance
   - Validare audit trail
   - Tempo stimato: 2 ore

4. **Revisione Conformità** (Officer Conformità):
   - Verificare conformità AI Act
   - Controllare aderenza GDPR
   - Validare requisiti CAD
   - Tempo stimato: 3 ore

5. **Approvazione Esecutiva** (CTO/Direttore):
   - Approvazione finale
   - Accettazione rischi
   - Autorizzazione deployment
   - Tempo stimato: 1 ora

**Tempo Revisione Totale**: ~10 ore per System Card

---

## Distribuzione e Piano di Aggiornamento

### Pubblicazione
- Tutte le System Card pubblicate in: `docs/microservices/MSxx/SYSTEM-CARD.md`
- Tutte le System Card tracciate in: `docs/SYSTEM-CARDS-REGISTRY.md`
- Controllo versione: Repository GitHub

### Manutenzione
- Piano revisione: Trimestrale (o su aggiornamento modello)
- Trigger aggiornamento:
  - Retraining modello
  - Nuovo rilascio versione
  - Degradazione performance rilevata
  - Cambiamenti requisiti normativi
  - Preoccupazioni fairness identificate

### Archiviazione
- Mantenere tutte le versioni storiche
- Documentare razionale per cambiamenti
- Mantenere change log per modello

---

## Documenti Correlati

- [COMPLIANCE-MAPPING-AI-ACT.md](COMPLIANCE-MAPPING-AI-ACT.md) - Requisiti conformità AI Act
- [COMPLIANCE-MAPPING-CAD.md](COMPLIANCE-MAPPING-CAD.md) - Requisiti audit CAD
- [DEVELOPMENT-GUIDE.md](DEVELOPMENT-GUIDE.md) - Standard di sviluppo
- EU AI Office: https://ec.europa.eu/info/research-and-innovation_en

---

*Modello System Card - Standard EU AI Office (Nov 2025)*
