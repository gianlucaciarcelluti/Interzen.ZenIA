# SP00 - Procedural Classifier: Riepilogo POC

## ✅ Completato

È stato creato il sottoprogetto **SP00 - Procedural Classifier** clonando e personalizzando SP04 per la classificazione di procedimenti amministrativi.

## 📁 Struttura Creata

```
src/SP00/
├── README.md                                    # Documentazione generale
├── QUICKSTART.md                                # Guida rapida
├── start_streamlit.py                           # Script avvio Python
├── start_streamlit.sh                           # Script avvio Bash
└── procedural_classifier/
    ├── __init__.py                              # Module init
    ├── groq_procedural_classifier.py            # Classificatore LLM (Groq)
    ├── procedimenti_dataset.py                  # Dataset 50+ procedimenti PA
    ├── streamlit_procedural_app.py              # Interfaccia web Streamlit
    └── test_procedural_classifier.py            # Suite di test
```

## 🎯 Funzionalità Implementate

### 1. Dataset Procedimenti Amministrativi
- **50+ procedimenti** mappati (Ambiente, Urbanistica, Commercio, Sociale, Mobilità, Cultura)
- **Generazione automatica** di istanze realistiche
- **Mapping procedimento → provvedimento** (es: "Autorizzazione Scarico Acque" → "Determinazione Dirigenziale")
- **Metadata completi**: normativa, termini, autorità competente

### 2. Classificatore LLM con Groq
- **Modello consigliato**: Llama 3.3 70B Versatile
- **Classificazione uni-dimensionale**: Procedimento → Provvedimento (a differenza di SP04 multi-dimensionale)
- **Output strutturato JSON** con:
  - Procedimento identificato
  - Tipo di provvedimento da emettere
  - Categoria e sottocategoria
  - Normativa di riferimento
  - Termini procedimentali
  - Confidence score
  - Metadata estratti
  - Motivazione della classificazione

### 3. Interfaccia Streamlit
- **UI intuitiva** per testing rapido
- **Esempi pre-caricati** per ogni categoria
- **Storico classificazioni** con export CSV
- **Visualizzazione dettagliata** risultati e metadata
- **Raccomandazioni automatiche** basate su confidence

### 4. Testing e Sperimentazione
- **Quick test** per verifica setup
- **Batch processing** con progress tracking
- **Resume capability** per classificazioni interrotte
- **Metriche dettagliate**: accuracy, latency, token usage

## 🚀 Come Iniziare

### Setup Veloce (3 minuti)

```bash
# 1. Vai nella directory SP00
cd src/SP00

# 2. Installa dipendenze (se non fatto)
pip install groq python-dotenv pandas tqdm streamlit

# 3. Configura API key nel file .env in src/
# Crea src/.env con:
# GROQ_API_KEY=your-groq-api-key-here

# 4. Avvia l'interfaccia
chmod +x start_streamlit.sh
./start_streamlit.sh

# Oppure su macOS:
python start_streamlit.py
```

### Test da Terminale

```bash
cd procedural_classifier
python test_procedural_classifier.py
```

Scegli:
- **1** = Quick test (1 istanza)
- **2** = Test con dataset (batch 10 istanze)
- **3** = Entrambi

## 📊 Differenze da SP04

| Aspetto | SP04 (Medical Malpractice) | SP00 (Procedimenti PA) |
|---------|---------------------------|------------------------|
| **Dominio** | Sinistri medical malpractice | Procedimenti amministrativi |
| **Dimensioni** | 2 (Tipologia + Riferimento Temporale) | 1 (Procedimento → Provvedimento) |
| **Input** | Email medico → assicurazione | Istanza cittadino/azienda → PA |
| **Output** | Classificazione binaria × 2 | Procedimento + Metadata completi |
| **Categorie** | 4 combinazioni (2×2) | 50+ procedimenti |
| **Metadata** | Limitati | Ricchi (normativa, termini, autorità) |
| **Guardrail** | Keyword + LLM ibrido | Da implementare (opzionale) |

## 🎓 Modalità POC

Questo è un **Proof of Concept** per:

### Obiettivi di Sperimentazione
- ✅ **Testare strategie** di classificazione (keyword vs LLM puro vs ibrido)
- ✅ **Confrontare modelli** (Llama 3.1 8B vs 3.3 70B)
- ✅ **Valutare accuracy** su diverse categorie di procedimenti
- ✅ **Ottimizzare prompt** engineering per massima precisione
- ✅ **Misurare performance** (latenza, throughput, costi)

### Non Include (Fase POC)
- ❌ Integrazione con database reali
- ❌ API REST production-ready
- ❌ Autenticazione/autorizzazione
- ❌ Scalabilità produzione
- ❌ Cache Redis distribuita
- ❌ Integrazione con Knowledge Base (SP03)

## 📈 Prossimi Passi Suggeriti

### 1. Testing e Validazione
```bash
# Testa con dataset completo
cd procedural_classifier
python test_procedural_classifier.py
# Scegli opzione 2

# Analizza risultati
# Identifica categorie con bassa accuracy
# Raffina prompt per casi problematici
```

### 2. Confronto Modelli
```python
from groq_procedural_classifier import ProceduralClassifier

# Test con modello veloce
classifier_8b = ProceduralClassifier(model="llama-3.1-8b-instant")

# Test con modello potente
classifier_70b = ProceduralClassifier(model="llama-3.3-70b-versatile")

# Confronta accuracy vs latenza
```

### 3. Espansione Dataset
```python
from procedimenti_dataset import PROCEDIMENTI_MAPPING

# Aggiungi nuovi procedimenti in PROCEDIMENTI_MAPPING
# Genera più varianti per procedimento
df = create_procedimenti_dataset(n_samples_per_procedimento=10)
```

### 4. Integrazione con SP03 (Knowledge Base)
- [ ] Collegare classificatore a KB per recupero normativa
- [ ] Arricchire output con info da grafo knowledge
- [ ] Implementare similarity search per procedimenti simili

### 5. Ottimizzazione Prompt
- [ ] Sperimentare con temperature diverse
- [ ] Testare prompt alternativi
- [ ] Aggiungere few-shot examples nel prompt

## 📚 Documentazione

- **README.md**: Panoramica generale del sottoprogetto
- **QUICKSTART.md**: Guida pratica step-by-step
- **RIEPILOGO.md**: Questo documento
- **Specifiche SP00**: `/docs/use_cases/generazione atti amministrativi/01 SP00 - Procedural Classifier.md`

## 💡 Suggerimenti d'Uso

### Per Testing Rapido
```bash
# Usa interfaccia Streamlit
./start_streamlit.sh

# Testa con esempi pre-caricati
# Analizza confidence e motivazioni
```

### Per Analisi Accuratezza
```python
# Test con dataset bilanciato
from procedimenti_dataset import create_procedimenti_dataset
df = create_procedimenti_dataset(n_samples_per_procedimento=5)

# Classifica e valuta
results = classifier.classify_batch(
    istanze=df['testo'].tolist(),
    true_labels=df['procedimento'].tolist()
)

# Analizza errori
errors = results[results['correct'] == False]
```

### Per Benchmark Performance
```python
import time

start = time.time()
results = classifier.classify_batch(istanze[:100])
duration = time.time() - start

print(f"Throughput: {100/duration:.1f} istanze/sec")
print(f"Avg latency: {duration/100:.3f}s")
```

## ✅ Checklist Completamento

- [x] Struttura directory SP00 creata
- [x] Dataset 50+ procedimenti implementato
- [x] Classificatore LLM Groq funzionante
- [x] Interfaccia Streamlit operativa
- [x] Suite di test implementata
- [x] Documentazione completa
- [x] Script di avvio creati
- [x] Esempi di utilizzo forniti

## 🎉 Risultato

Hai ora un **sottoprogetto SP00 completo e funzionante** per:
- Classificare istanze di parte → procedimenti amministrativi
- Sperimentare con diversi modelli LLM
- Valutare strategie di classificazione
- Studiare performance e accuracy

**Il sistema è pronto per essere testato e raffinato! 🚀**

---

**Data creazione**: 30 Ottobre 2025  
**Versione**: 1.0.0  
**Status**: ✅ POC Operativo
