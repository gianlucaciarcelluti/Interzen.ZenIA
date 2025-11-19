# 🤖 LLM Classifier - Groq Integration

Sistema di classificazione sinistri assicurativi con modelli LLM via Groq API.

---

## 🔐 Setup API Key (Semplificato!)

**Metodo Consigliato:** Usa il file `.env` nella root del progetto

```bash
# 1. Crea il file .env nella root
echo "GROQ_API_KEY=gsk_your_api_key_here" > .env

# 2. Fatto! La key viene caricata automaticamente
```

Il sistema ora usa `python-dotenv` per caricare automaticamente la `GROQ_API_KEY` dal file `.env`.

📚 **Documentazione completa:** [GROQ_ENV_SETUP.md](../../docs/GROQ_ENV_SETUP.md)

---

## 🆕 Versione 2.0 - Nuove Funzionalità

### 1. Recupero Dinamico Modelli
- ✅ Lista modelli aggiornata automaticamente da API Groq
- ✅ Selezione automatica modelli consigliati per il task
- ✅ No più hardcoding della lista modelli

### 2. Progress Bar Avanzata
- ✅ Visualizzazione real-time con `tqdm`
- ✅ ETA e velocità di elaborazione
- ✅ Indicatori di stato salvataggio

### 3. Persistenza e Ripresa
- ✅ Salvataggio automatico progresso
- ✅ Interruzione sicura con Ctrl+C
- ✅ Ripresa automatica dal punto di interruzione
- ✅ Ottimizzazione consumo API

---

## 📂 File Principali

```
llm_classifier/
├── groq_integration.py              ← Core del sistema (AGGIORNATO)
├── groq_study_notebook.ipynb        ← Notebook interattivo (AGGIORNATO)
├── example_groq_features.py         ← Esempi pratici (NUOVO)
├── medical_provider_dataset.py      ← Generatore dataset
├── GROQ_FEATURES_UPDATE.md          ← Documentazione completa (NUOVO)
└── groq_study_results/
    ├── .cache/                      ← Cache persistenza (AUTO)
    └── *.csv                        ← Risultati esportati
```

---

## 🚀 Quick Start

### 1. Setup
```bash
# Attiva ambiente
.\.venv\Scripts\Activate.ps1

# Installa dipendenze
pip install -r ../requirements.txt

# API Key
$env:GROQ_API_KEY = "gsk_..."
```

### 2. Test Funzionalità
```bash
python ../../tests/test_groq_features.py
```

### 3. Esempi Pratici
```bash
python example_groq_features.py
```

### 4. Notebook Completo
```bash
jupyter notebook groq_study_notebook.ipynb
```

---

## 💡 Esempio Base

```python
from groq_integration import GroqClassifier
import os

# Inizializza
classifier = GroqClassifier(
    api_key=os.environ.get("GROQ_API_KEY")
)

# Recupera modelli disponibili
models = classifier.get_recommended_models()
print(f"Modelli consigliati: {models}")

# Classifica batch con progress bar
results = classifier.classify_batch(
    emails=your_emails,
    show_progress=True,
    resume=True,           # Riprende se interrotto
    save_interval=10       # Salva ogni 10 email
)

# Confronta modelli
comparison = classifier.compare_models(
    test_emails=test_set,
    true_labels=labels,
    models=None,           # Usa modelli da API
    resume=True
)
```

---

## 🎯 Use Cases

### 1. Analisi Grande Dataset
```python
# 1000 email - con persistenza
results = classifier.classify_batch(
    emails=dataset_1000,
    labels=labels_1000,
    resume=True,
    save_interval=20
)
```

**Vantaggi:**
- Interrompi con Ctrl+C in qualsiasi momento
- Riprendi esattamente da dove hai interrotto
- Nessuna chiamata API sprecata

### 2. Studio Multi-Modello
```python
# Testa 5 modelli su 100 email = 500 chiamate
comparison = classifier.compare_models(
    test_emails=sample_100,
    true_labels=labels_100,
    resume=True  # Riprende se interrotto
)
```

**Vantaggi:**
- Progress bar per ogni modello
- Ripresa automatica se interrotto
- Risultati salvati incrementalmente

### 3. Analisi Distribuita
```python
# Giorno 1: Primi 500
classifier.classify_batch(
    emails[:500], labels[:500],
    resume=True
)

# Giorno 2: Successivi 500
classifier.classify_batch(
    emails[500:], labels[500:],
    resume=True
)
```

**Vantaggi:**
- Distribuisci carico API nel tempo
- Rispetta rate limits
- Cache separata per sessione

---

## 📊 Output Esempio

### Progress Bar
```
🚀 Nuova classificazione batch: 200 email
   Modello: llama-3.1-8b-instant
   Velocità attesa: ~120 email/min
   Salvataggio automatico ogni 10 email
================================================================================
Classificazione (llama-3.1-8b-instant): 65%|██████▌   | 130/200 [02:10<01:10, 1.0email/s]
```

### Interruzione e Ripresa
```
^C
⏸️  Analisi interrotta dall'utente
   Progresso salvato: 130/200 email
   Per riprendere, riesegui la stessa chiamata con resume=True

# Riesegui →

🔄 Ripresa analisi precedente:
   Già completate: 130/200 email
   Timestamp: 2025-10-06T14:23:45
   Modello: llama-3.1-8b-instant
================================================================================
Classificazione (llama-3.1-8b-instant): 100%|██████████| 200/200 [01:10<00:00, 2.8email/s]
```

---

## 📚 Documentazione

| Documento | Contenuto |
|-----------|-----------|
| **GROQ_FEATURES_UPDATE.md** | Guida completa nuove funzionalità |
| **../../docs/groq_integration_update_summary.md** | Dettagli tecnici modifiche |
| **../../docs/groq_persistence_quickstart.md** | Tutorial persistenza |
| **../../docs/GROQ_QUICK_REFERENCE.md** | Comandi rapidi |

---

## 🔧 Configurazione Avanzata

### Custom Cache Directory
```python
classifier = GroqClassifier(
    api_key="...",
    cache_dir="custom/.cache"
)
```

### Personalizza Salvataggio
```python
results = classifier.classify_batch(
    emails=emails,
    save_interval=5,  # Più frequente
    resume=True
)
```

### Disabilita Ripresa
```python
results = classifier.classify_batch(
    emails=emails,
    resume=False  # Ricomincia sempre
)
```

---

## 🗑️ Gestione Cache

### Visualizza Cache
```bash
ls groq_study_results/.cache
```

### Pulisci Cache
```bash
# Windows PowerShell
Remove-Item -Recurse -Force groq_study_results/.cache

# Ricrea
New-Item -ItemType Directory -Path groq_study_results/.cache
```

### Ispeziona Stato
```python
import pickle
import os

cache_files = os.listdir("groq_study_results/.cache")
if cache_files:
    with open(f"groq_study_results/.cache/{cache_files[0]}", 'rb') as f:
        state = pickle.load(f)
        print(f"Progresso: {state['current_index']} email")
        print(f"Modello: {state['model']}")
```

---

## 🎓 Dataset

### Generazione Dataset Test
```python
from medical_provider_dataset import create_mock_dataset

# Genera 1000 email simulate
df = create_mock_dataset()
df.to_csv("dataset_medical_provider_complete.csv", index=False)
```

### Struttura Dataset
- **Tipologia**: 0=Sinistro Avvenuto, 1=Circostanza Potenziale
- **Riferimento Temporale**: 0=Fatto Iniziale, 1=Follow-up
- **Combinazioni**: 4 (0-0, 0-1, 1-0, 1-1)
- **Bilanciamento**: 250 email per combinazione

---

## 🐛 Troubleshooting

### Import Error
```python
import sys
sys.path.append("path/to/llm_classifier")
```

### API Rate Limit
- Pausa tra richieste: 100ms (configurabile in `classify_single`)
- Usa `save_interval` maggiore per analisi lunghe
- Distribuisci analisi in più sessioni

### Cache Corrotta
```bash
# Elimina e ricrea
Remove-Item -Recurse -Force groq_study_results/.cache
New-Item -ItemType Directory -Path groq_study_results/.cache
```

---

## ✅ Best Practices

1. **Sempre `resume=True`** per dataset > 50 email
2. **`save_interval=10-20`** per bilanciare performance/sicurezza
3. **Test piccoli** prima di analisi complete
4. **Monitora cache** per evitare accumulo
5. **Distribuisci** analisi lunghe in più sessioni
6. **Verifica quota API** prima di analisi massive

---

## 📈 Performance

### Prima (v1.0)
- ❌ Nessun feedback durante analisi
- ❌ Perdita completa se interrotto
- ❌ Riprocessamento totale se fallito

### Dopo (v2.0)
- ✅ Progress bar real-time
- ✅ Salvataggio automatico incrementale
- ✅ Ripresa esatta da interruzione
- ✅ Zero chiamate API sprecate

---

## 🔗 Link Utili

- [Groq Console](https://console.groq.com)
- [Groq API Docs](https://console.groq.com/docs)
- [tqdm Documentation](https://tqdm.github.io/)

---

## 📝 Changelog

### v2.0 (06/10/2025)
- ✨ Recupero dinamico modelli da API
- ✨ Progress bar con tqdm
- ✨ Sistema persistenza completo
- ✨ Gestione interruzioni Ctrl+C
- ✨ Cache automatica
- 📚 Documentazione estesa
- 🧪 Test automatici

### v1.0
- ⚡ Classificazione base con Groq
- 📊 Confronto modelli
- 📈 Metriche accuracy

---

**Versione**: 2.0  
**Data**: 06 Ottobre 2025  
**Status**: ✅ Production Ready

---

**Inizia ora:** `jupyter notebook groq_study_notebook.ipynb` 🚀
