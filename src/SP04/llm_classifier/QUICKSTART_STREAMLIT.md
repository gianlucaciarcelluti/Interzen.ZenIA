# 🚀 Quick Start - Classificatore Sinistri Groq

## Avvio Rapido

### Su macOS/Linux:
```bash
# 1. Attiva virtual environment (se usi venv)
source .venv/bin/activate

# 2. Avvia l'app
./start_streamlit_groq.sh
```

### Su Windows:
```powershell
# 1. Attiva virtual environment (se usi venv)
.venv\Scripts\activate.ps1

# 2. Avvia l'app
.\start_streamlit_groq.ps1
```

### Alternativa (cross-platform):
```bash
streamlit run streamlit_groq_classifier.py
```

## Primo Utilizzo

1. **Apri il browser** su http://localhost:8501
2. **Inserisci la tua API Key Groq** nella sidebar
3. **Clicca su uno degli esempi** (es. "🚨 Sinistro Iniziale")
4. **Premi "🚀 Classifica Email"**
5. **Analizza i risultati**! 🎉

## Ottieni una API Key Groq

1. Vai su https://console.groq.com/
2. Crea un account (gratuito)
3. Vai su "API Keys"
4. Crea una nuova chiave
5. Configurala con uno dei metodi sotto

### Configurazione API Key (scegli uno)

**Metodo 1: File .env (raccomandato)**

Il file `.env` deve essere nella **root del progetto** (`ZenIA/.env`):

```bash
# Dalla directory src/llm_classifier, torna alla root
cd ../../

# Copia il template (se non esiste già)
cp .env.example .env

# Modifica .env e inserisci la tua chiave
nano .env
# Aggiungi: GROQ_API_KEY=gsk_your_actual_key_here
```

**Metodo 2: Variabile d'ambiente**
```bash
export GROQ_API_KEY="your-api-key-here"
```

**Metodo 3: Nell'interfaccia web**
- Inseriscila direttamente nella sidebar dell'app

## Comandi Utili

```bash
# Installa dipendenze
pip install streamlit pandas groq

# Verifica installazione
streamlit --version

# Cancella cache Streamlit
streamlit cache clear

# Avvia su porta diversa
streamlit run streamlit_groq_classifier.py --server.port 8502
```

## Test Veloce

Prova questo esempio:

**Input:**
```
Spett.le Compagnia, sono il Dr. Rossi e vi scrivo per segnalare un evento 
avverso verificatosi il 15/03/2024 presso il nostro reparto. Durante intervento 
chirurgico al ginocchio sx, per errore procedurale è stato operato il ginocchio 
dx del paziente. Il paziente è stato informato e richiede risarcimento. 
Allego documentazione clinica completa.
```

**Output Atteso:**
- Tipologia: 🚨 Sinistro Avvenuto (0)
- Riferimento: 📨 Fatto Iniziale (0)
- Confidence: >90% per entrambe

## Problemi Comuni

**"ModuleNotFoundError: No module named 'streamlit'"**
→ Esegui: `pip install streamlit`

**"GROQ_API_KEY non trovata"**
→ Inseriscila nella sidebar dell'app

**"Port 8501 already in use"**
→ Usa: `streamlit run streamlit_groq_classifier.py --server.port 8502`

## 📚 Documentazione Completa

Vedi `README_STREAMLIT_GROQ.md` per la documentazione dettagliata.

---

**Buona classificazione! 🎯**
