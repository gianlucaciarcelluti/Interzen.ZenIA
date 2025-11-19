# SP00 - Procedural Classifier: Guida Rapida

## 🎯 Obiettivo

Classificare automaticamente le **istanze di parte** (richieste presentate da cittadini/aziende alla PA) per identificare:

1. **Procedimento amministrativo** da attivare
2. **Tipo di provvedimento** finale da emettere
3. **Normativa applicabile** e termini

## 🚀 Quick Start in 5 Minuti

### 1. Prerequisiti

```bash
# Python 3.9+
python --version

# Verifica di essere nella directory src
cd src
```

### 2. Installa Dipendenze

```bash
pip install groq python-dotenv pandas tqdm
```

### 3. Configura API Key

Crea un file `.env` nella cartella `src/`:

```bash
GROQ_API_KEY=your-groq-api-key-here
```

**Ottieni una chiave gratuita su:** https://console.groq.com

### 4. Test Rapido

```bash
cd SP00/procedural_classifier
python test_procedural_classifier.py
```

Scegli opzione `1` per quick test.

### 5. Avvia Interfaccia Web

```bash
streamlit run streamlit_procedural_app.py
```

Apri il browser su: http://localhost:8501

## 📋 Esempi di Utilizzo

### Esempio 1: Test da Codice Python

```python
from groq_procedural_classifier import ProceduralClassifier

# Inizializza
classifier = ProceduralClassifier(model="llama-3.3-70b-versatile")

# Istanza di test
istanza = """
Spettabile Comune, la scrivente ABC S.p.A. richiede 
autorizzazione allo scarico di acque reflue industriali 
provenienti dal ciclo produttivo. Portata: 500 m³/giorno.
"""

# Classifica
result = classifier.classify_single(istanza)

# Risultato
print(f"Procedimento: {result['procedimento']}")
print(f"Provvedimento: {result['tipo_provvedimento']}")
print(f"Confidence: {result['confidence']:.2f}")
```

### Esempio 2: Batch Processing

```python
from procedimenti_dataset import create_procedimenti_dataset

# Crea dataset di test
df = create_procedimenti_dataset(n_samples_per_procedimento=5)

# Classifica batch
istanze = df['testo'].tolist()
true_labels = df['procedimento'].tolist()

results_df = classifier.classify_batch(
    istanze=istanze,
    true_labels=true_labels
)

# Analisi risultati
successful = results_df[results_df['success'] == True]
accuracy = successful['correct'].mean() * 100
print(f"Accuracy: {accuracy:.1f}%")
```

### Esempio 3: Interfaccia Streamlit

1. Avvia: `streamlit run streamlit_procedural_app.py`
2. Incolla il testo dell'istanza nell'area di testo
3. Clicca "Classifica Istanza"
4. Visualizza risultati dettagliati

## 📊 Output della Classificazione

```json
{
  "procedimento": "AUTORIZZAZIONE_SCARICO_ACQUE",
  "procedimento_denominazione": "Autorizzazione Scarico Acque Reflue",
  "categoria": "AMBIENTE",
  "sottocategoria": "TUTELA_ACQUE",
  "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
  "autorita_competente": "DIRIGENTE_SETTORE_AMBIENTE",
  "normativa_base": ["D.Lgs 152/2006", "L.R. 62/1998"],
  "termini_giorni": 90,
  "confidence": 0.96,
  "metadata_extracted": {
    "richiedente": "Persona Giuridica",
    "oggetto_sintetico": "Autorizzazione scarico acque reflue industriali",
    "keywords_chiave": ["scarico", "acque reflue", "industriali"]
  },
  "motivazione": "L'istanza richiede chiaramente...",
  "latency": 0.452,
  "tokens_used": 387
}
```

## 🔧 Configurazione Avanzata

### Cambiare Modello

```python
# Più veloce ma meno accurato
classifier = ProceduralClassifier(model="llama-3.1-8b-instant")

# Raccomandato: bilanciato velocità/accuratezza
classifier = ProceduralClassifier(model="llama-3.3-70b-versatile")
```

### Regolare Temperature

```python
# Più deterministica (raccomandato)
result = classifier.classify_single(istanza, temperature=0.1)

# Più creativa (sconsigliato per classificazione)
result = classifier.classify_single(istanza, temperature=0.7)
```

### Gestire Cache

```python
# Abilita resume da classificazioni interrotte
results_df = classifier.classify_batch(
    istanze=istanze,
    resume=True,          # Riprendi da dove interrotto
    save_interval=10      # Salva ogni 10 istanze
)
```

## 📈 Dataset di Test

Il sistema include un dataset di esempio con:

### Categorie Supportate

- **AMBIENTE**: VIA, scarichi, emissioni, bonifiche
- **URBANISTICA**: Permessi costruire, varianti, certificati
- **COMMERCIO**: Licenze, SCIA, occupazione suolo
- **SOCIALE**: Assegnazione alloggi, contributi
- **MOBILITÀ**: ZTL, parcheggi, autorizzazioni trasporto
- **CULTURA**: Patrocini, utilizzo spazi

### Generare Dataset Custom

```python
from procedimenti_dataset import create_procedimenti_dataset

# 50+ procedimenti × 5 istanze = 250+ esempi
df = create_procedimenti_dataset(n_samples_per_procedimento=5)

# Salva
df.to_csv("dataset_custom.csv", index=False)
```

## 🎯 Metriche di Performance (Target POC)

| Metrica | Target | Note |
|---------|--------|------|
| Accuracy | > 90% | Su dataset test bilanciato |
| Latenza p95 | < 1s | Con llama-3.3-70b |
| Throughput | ~60/min | Batch processing |
| Confidence avg | > 0.85 | Per istanze valide |

## ⚠️ Troubleshooting

### Errore: "API key richiesta"

```bash
# Verifica che .env esista e contenga:
cat src/.env

# Oppure esporta direttamente:
export GROQ_API_KEY='your-key-here'
```

### Errore: "Module not found"

```bash
# Verifica di essere nella directory corretta:
cd src/SP00/procedural_classifier

# Oppure aggiungi il path:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Errore: Rate Limit Groq

Il sistema ha già un delay di 100ms tra richieste. Se necessario:

```python
# Aumenta delay nel batch processing
# Modifica in groq_procedural_classifier.py:
time.sleep(0.2)  # Da 0.1 a 0.2
```

### Performance Lente

```python
# Usa modello più veloce:
classifier = ProceduralClassifier(model="llama-3.1-8b-instant")

# Riduci dimensione batch:
results = classifier.classify_batch(istanze[:20])  # Solo prime 20
```

## 📚 Prossimi Passi

### 1. Sperimentare Strategie

- [ ] Testare diversi modelli (8B vs 70B)
- [ ] Confrontare temperature (0.0 vs 0.3)
- [ ] Provare prompt engineering alternativi

### 2. Valutare Accuracy

- [ ] Eseguire test su dataset completo
- [ ] Analizzare errori di classificazione
- [ ] Identificare categorie problematiche

### 3. Ottimizzare Performance

- [ ] Benchmarking latenza per modello
- [ ] Test throughput batch
- [ ] Analisi cache hit rate

### 4. Espandere Dataset

- [ ] Aggiungere nuovi procedimenti
- [ ] Aumentare variabilità istanze
- [ ] Includere casi edge/ambigui

## 🤝 Support

Per domande o problemi:

1. Verifica questa guida
2. Controlla i file di esempio
3. Consulta la documentazione completa in `docs/`

## 📄 File Importanti

```
SP00/
├── README.md                                  # Documentazione generale
├── QUICKSTART.md                              # Questa guida
└── procedural_classifier/
    ├── groq_procedural_classifier.py          # Classificatore principale
    ├── procedimenti_dataset.py                # Dataset di test
    ├── streamlit_procedural_app.py            # Interfaccia web
    └── test_procedural_classifier.py          # Suite di test
```

## ✅ Checklist Setup Completo

- [ ] Python 3.9+ installato
- [ ] Dipendenze installate (`pip install ...`)
- [ ] File `.env` creato con API key
- [ ] Quick test eseguito con successo
- [ ] Interfaccia Streamlit funzionante
- [ ] Test con dataset completato

**Buon testing! 🚀**
