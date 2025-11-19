# 🆕 Nuove Funzionalità Groq Integration

## Panoramica

Il sistema di classificazione con Groq è stato aggiornato con tre funzionalità fondamentali per ottimizzare l'analisi di grandi volumi di dati rispettando i limiti dell'API gratuita.

---

## 1️⃣ Recupero Dinamico Modelli

### Descrizione
I modelli disponibili vengono ora recuperati automaticamente dall'API Groq tramite l'endpoint `/v1/models`, eliminando la necessità di aggiornamenti manuali.

### Utilizzo

```python
from groq_integration import GroqClassifier

classifier = GroqClassifier(api_key="your-api-key")

# Recupera tutti i modelli disponibili
available_models = classifier.fetch_available_models()
print(f"Modelli disponibili: {len(available_models)}")

# Ottieni modelli consigliati per il task
recommended = classifier.get_recommended_models()
print(f"Modelli consigliati: {recommended}")
```

### Output Esempio
```
Modelli disponibili: 15
🟢 llama-3.1-8b-instant (ctx: 8192)
🟢 llama-3.1-70b-versatile (ctx: 8192)
🟢 mixtral-8x7b-32768 (ctx: 32768)
...
```

---

## 2️⃣ Progress Bar con tqdm

### Descrizione
Visualizzazione in tempo reale del progresso dell'analisi con indicatori di:
- Numero email elaborate
- Percentuale completamento
- Tempo trascorso
- Tempo rimanente stimato (ETA)
- Velocità di elaborazione

### Utilizzo

```python
results = classifier.classify_batch(
    emails=test_emails,
    show_progress=True,  # Abilita progress bar
    save_interval=10     # Salva ogni 10 email
)
```

### Output Esempio
```
🚀 Nuova classificazione batch: 100 email
   Modello: llama-3.1-8b-instant
   Velocità attesa: ~120 email/min
   Salvataggio automatico ogni 10 email
================================================================================
Classificazione (llama-3.1-8b-instant): 45%|████▌     | 45/100 [00:22<00:27, 2.0email/s]
```

---

## 3️⃣ Persistenza e Ripresa Analisi

### Descrizione
Il sistema salva automaticamente il progresso su disco permettendo di:
- **Interrompere** l'analisi in qualsiasi momento (Ctrl+C)
- **Riprendere** esattamente dal punto di interruzione
- **Ottimizzare** il consumo di chiamate API
- **Evitare** riprocessamenti inutili

### Meccanismo
- Il progresso viene salvato in file `.pkl` nella directory `.cache`
- Ogni batch genera una chiave univoca basata su: modello, numero email, contenuto
- Salvataggio automatico ogni N email (configurabile)
- Cache automaticamente rimossa al completamento

### Utilizzo

```python
classifier = GroqClassifier(
    api_key="your-api-key",
    cache_dir="groq_study_results/.cache"  # Directory cache personalizzata
)

try:
    results = classifier.classify_batch(
        emails=test_emails,
        resume=True,        # Abilita ripresa automatica
        save_interval=10    # Salva ogni 10 email
    )
except KeyboardInterrupt:
    print("⏸️  Analisi interrotta! Riesegui per riprendere")
```

### Scenario d'Uso

#### Prima esecuzione:
```
🚀 Nuova classificazione batch: 200 email
   Modello: llama-3.1-70b-versatile
   Salvataggio automatico ogni 10 email
================================================================================
Classificazione: 35%|███▌      | 70/200 [01:15<02:20, 0.9email/s]
^C
⏸️  Analisi interrotta dall'utente
   Progresso salvato: 70/200 email
   Per riprendere, riesegui la stessa chiamata con resume=True
```

#### Ripresa (riesecuzione):
```
🔄 Ripresa analisi precedente:
   Già completate: 70/200 email
   Timestamp: 2025-10-06T14:23:45
   Modello: llama-3.1-70b-versatile
================================================================================
Classificazione: 100%|██████████| 200/200 [02:15<00:00, 1.5email/s]
✅ Batch completato!
```

---

## 📊 Confronto Modelli Aggiornato

Il metodo `compare_models()` ora supporta tutte le nuove funzionalità:

```python
comparison = classifier.compare_models(
    test_emails=test_emails,
    true_labels=true_labels,
    models=None,  # Usa modelli recuperati dall'API
    resume=True   # Supporta ripresa
)
```

### Output Esempio
```
🔍 Recupero modelli disponibili dall'API Groq...
   Trovati 15 modelli, uso i primi 5

🏁 BENCHMARK MULTI-MODELLO GROQ
================================================================================
Modelli da testare: 5
Email per modello: 100
Totale classificazioni: 500

Modelli testati: 40%|████      | 2/5 [03:45<05:37, 112s/model]

🤖 Testing: llama-3.1-8b-instant
--------------------------------------------------------------------------------
Classificazione (llama-3.1-8b-instant): 100%|██████████| 100/100 [00:45<00:00, 2.2email/s]
...
```

---

## 🎯 Esempio Completo

Vedi `example_groq_features.py` per esempi pratici di tutte le funzionalità.

```bash
# Attiva ambiente virtuale
source .venv/Scripts/activate.ps1

# Installa dipendenze aggiornate
pip install -r requirements.txt

# Esegui esempi
cd src/llm_classifier
python example_groq_features.py
```

---

## 📁 Struttura Cache

```
groq_study_results/
├── .cache/
│   ├── a3f2c1d5e8b9f4a7.pkl  # Stato analisi modello 1
│   ├── b8e4f7a2c9d1e6b3.pkl  # Stato analisi modello 2
│   └── ...
├── model_comparison.csv
└── classification_results_*.csv
```

### Gestione Cache

```python
# Reset completo - elimina tutta la cache
import shutil
shutil.rmtree("groq_study_results/.cache")

# La cache viene automaticamente pulita al completamento
# Per forzare rielaborazione, elimina il file .pkl specifico
```

---

## ⚙️ Configurazione Limiti API

### Groq Free Tier (stimato)
- Rate limit: ~30 richieste/minuto
- Daily limit: variabile

### Ottimizzazioni Implementate
- Delay 100ms tra richieste (max 10 req/s)
- Salvataggio automatico per minimizzare riprocessamenti
- Possibilità di distribuire analisi in più sessioni

```python
# Esempio: analisi distribuita nel tempo
# Giorno 1: analizza primi 3 modelli
comparison = classifier.compare_models(
    test_emails=emails,
    true_labels=labels,
    models=recommended[:3],  # Primi 3
    resume=True
)

# Giorno 2: analizza altri 3 modelli
comparison = classifier.compare_models(
    test_emails=emails,
    true_labels=labels,
    models=recommended[3:6],  # Successivi 3
    resume=True
)
```

---

## 🔧 Troubleshooting

### Cache non funziona
```python
# Verifica directory cache
import os
cache_dir = "groq_study_results/.cache"
print(f"Cache esiste: {os.path.exists(cache_dir)}")
print(f"File in cache: {os.listdir(cache_dir)}")
```

### Progress bar non visualizzata
```bash
# Reinstalla tqdm
pip install --upgrade tqdm
```

### Modelli non recuperati
```python
# Test connessione API
classifier = GroqClassifier(api_key="your-key")
models = classifier.fetch_available_models()
if not models:
    print("Verifica API key e connessione")
```

---

## 📚 Riferimenti

- [Groq API Documentation](https://console.groq.com/docs)
- [tqdm Documentation](https://tqdm.github.io/)
- Notebook: `groq_study_notebook.ipynb`
- Esempi: `example_groq_features.py`

---

## 🎓 Best Practices

1. **Usa `resume=True`** sempre per analisi lunghe
2. **Imposta `save_interval`** appropriato (10-20 per dataset grandi)
3. **Monitora la cache** per evitare accumulo eccessivo
4. **Testa con campioni piccoli** prima di analisi complete
5. **Distribuisci analisi** in più sessioni se necessario

---

**Versione**: 2.0  
**Data aggiornamento**: 06 Ottobre 2025  
**Autore**: Sistema di Classificazione Groq
