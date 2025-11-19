# 🏥 POC Classificatore Sinistri con Streamlit e Groq

Sistema di classificazione multi-dimensionale per email di sinistri medical malpractice utilizzando Groq AI.

## 📋 Descrizione

Applicazione web interattiva che classifica le comunicazioni da medici/ospedali verso compagnie assicurative in base a:

1. **Tipologia** (Natura dell'evento):
   - `0`: **Sinistro Avvenuto** - Danno/incidente già verificato
   - `1`: **Circostanza Potenziale** - Situazione di rischio potenziale

2. **Riferimento Temporale** (Fase della comunicazione):
   - `0`: **Fatto Iniziale** - Prima segnalazione del caso
   - `1`: **Follow-up** - Aggiornamento/integrazione documentale

## ✨ Caratteristiche

- ✅ **Classificazione Multi-Dimensionale**: Due dimensioni di classificazione simultanee
- 🧠 **Spiegazioni AI**: Ragionamento dettagliato del modello
- 📊 **Confidence Scores**: Punteggi di confidenza per ogni classificazione
- 🔑 **Indicatori Chiave**: Estrazione automatica degli elementi rilevanti
- 📈 **Storico Classificazioni**: Tracciamento delle classificazioni precedenti
- 💾 **Export Dati**: Download dello storico in formato CSV
- 🎨 **UI Moderna**: Interfaccia intuitiva con Streamlit

## 🚀 Installazione

### 1. Prerequisiti

```bash
# Python 3.8+
python --version

# Virtual environment (raccomandato)
python -m venv .venv
source .venv/bin/activate  # su macOS/Linux
# oppure
.venv\Scripts\activate.ps1  # su Windows
```

### 2. Installa le dipendenze

```bash
pip install streamlit pandas groq python-dotenv
```

Oppure se hai un `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Configura API Key Groq

**Opzione 1 - File .env (raccomandato):**

Il file `.env` deve essere nella **root del progetto** (`ZenIA/.env`):

```bash
# Dalla root del progetto
cd ../../  # Torna alla root (ZenIA/)
cp .env.example .env

# Modifica .env e inserisci la tua API key
nano .env
# GROQ_API_KEY=gsk_your_actual_key_here
```

**Nota**: L'app cerca automaticamente `.env` nella root, non serve metterlo in `src/llm_classifier`.

**Opzione 2 - Variabile d'ambiente:**
```bash
export GROQ_API_KEY="your-api-key-here"
```

**Opzione 3 - Inserimento nell'interfaccia web:**

Se non configuri .env o variabile d'ambiente, potrai inserire la chiave direttamente nell'app.

## 📱 Utilizzo

### Avvio Rapido

```bash
# Metodo 1: Usando lo script bash
./start_streamlit_groq.sh

# Metodo 2: Comando diretto
streamlit run streamlit_groq_classifier.py
```

L'applicazione si aprirà automaticamente nel browser all'indirizzo: **http://localhost:8501**

### Workflow

1. **Configura l'API Key** nella sidebar (se non impostata come variabile d'ambiente)
2. **Seleziona il modello AI** da utilizzare (default: Llama 3.1 70B)
3. **Inserisci il testo** dell'email da classificare
4. **Clicca "Classifica Email"** per ottenere i risultati
5. **Analizza i risultati**:
   - Classificazione principale (Tipologia + Riferimento)
   - Confidence scores per entrambe le dimensioni
   - Spiegazione dettagliata del ragionamento
   - Indicatori chiave identificati
   - Raccomandazioni basate sulla confidenza

### Esempi Precaricati

Nella sidebar trovi 4 bottoni con esempi per ogni categoria:
- 🚨 Sinistro Iniziale (0,0)
- 📋 Sinistro Follow-up (0,1)
- ⚠️ Circostanza Iniziale (1,0)
- 📝 Circostanza Follow-up (1,1)

## 🎯 Modelli Disponibili

- **Llama 3.1 8B Instant** - Veloce, ottimo per test rapidi
- **Llama 3.1 70B Versatile** - Più accurato (raccomandato)
- **Mixtral 8x7B** - Bilanciato velocità/accuratezza
- **Gemma 2 9B** - Alternativa efficiente

## 📊 Output

### Risultati Principali

```
🎯 Risultati Classificazione
├── Tipologia: Sinistro Avvenuto (0)
├── Riferimento: Fatto Iniziale (0)
├── Confidence Tipologia: 95.3%
└── Confidence Riferimento: 92.1%
```

### Classificazione Combinata

```
🚨 Sinistro Avvenuto - Fatto Iniziale (0, 0)
Sinistro già verificato - Prima segnalazione del caso
```

### Ragionamento AI

```
💡 Ragionamento e Motivazioni
Il testo indica chiaramente un evento avverso già verificato:
- Presenza di data specifica dell'evento
- Menzione esplicita di "errore procedurale"
- Richiesta di risarcimento dal paziente
- Documentazione clinica allegata
...
```

### Indicatori Chiave

```
🔑 Indicatori Chiave Identificati
[evento avverso] [errore procedurale] [richiede risarcimento]
[allego documentazione] [già verificato]
```

## 📁 Struttura File

```
llm_classifier/
├── streamlit_groq_classifier.py    # Applicazione principale
├── groq_integration.py              # Integrazione con Groq API
├── start_streamlit_groq.sh         # Script di avvio
└── README_STREAMLIT_GROQ.md        # Questa documentazione
```

## 🔧 Personalizzazione

### Modifica CSS

Il CSS personalizzato si trova nella sezione `st.markdown()` all'inizio del file. Puoi modificare:
- Colori del gradiente
- Stile delle card
- Dimensioni dei font
- Box informativi

### Aggiungi Nuovi Esempi

Nel dizionario `examples` nella sidebar, aggiungi nuove entry:

```python
examples = {
    "Tuo Esempio": "Testo dell'esempio...",
    # ...
}
```

### Modifica Soglie Confidence

Nelle raccomandazioni finali, modifica le soglie:

```python
if avg_confidence >= 0.8:  # Cambia 0.8 per soglia alta
    # ...
elif avg_confidence >= 0.6:  # Cambia 0.6 per soglia media
    # ...
```

## 🐛 Troubleshooting

### Errore: API Key non valida
```
⚠️ Inserisci la tua Groq API Key nella sidebar!
```
**Soluzione**: Verifica che la tua API key Groq sia corretta e attiva.

### Errore: Modulo non trovato
```
ModuleNotFoundError: No module named 'streamlit'
```
**Soluzione**: Installa le dipendenze con `pip install streamlit`

### Errore: groq_integration non trovato
```
ModuleNotFoundError: No module named 'groq_integration'
```
**Soluzione**: Assicurati che `groq_integration.py` sia nella stessa directory

### App non si apre nel browser
**Soluzione**: Apri manualmente http://localhost:8501

## 📈 Performance

### Latenza Media
- Llama 3.1 8B: ~1-2 secondi
- Llama 3.1 70B: ~2-4 secondi
- Mixtral 8x7B: ~1.5-3 secondi

### Costi (approssimativi)
- ~0.0001$ per 1K tokens
- ~500-800 tokens per email media
- ~0.00005$ per classificazione

## 🔐 Sicurezza

- ✅ API Key inserita tramite campo password (non visibile)
- ✅ Supporto variabili d'ambiente
- ✅ Nessun dato salvato permanentemente (solo session state)
- ✅ Storico locale cancellabile

## 📝 Note

- L'applicazione richiede una connessione internet attiva per comunicare con Groq API
- Lo storico delle classificazioni è mantenuto solo durante la sessione corrente
- I dati non vengono salvati su disco a meno che non si scarichi manualmente lo storico

## 🤝 Integrazione con il Notebook

Questo POC utilizza la stessa classe `GroqClassifier` del notebook Jupyter:
- `groq_study_notebook.ipynb` - Per analisi batch e testing
- `streamlit_groq_classifier.py` - Per classificazioni interattive singole

## 📞 Supporto

Per problemi o domande:
1. Verifica la documentazione Groq: https://console.groq.com/docs
2. Controlla i logs di Streamlit nella console
3. Verifica che tutte le dipendenze siano installate

## 🎉 Pronto!

Ora puoi avviare l'applicazione e iniziare a classificare le email!

```bash
./start_streamlit_groq.sh
```

Buona classificazione! 🚀
