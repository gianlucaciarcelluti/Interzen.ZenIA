# 🏛️ SP00 - Procedural Classifier

## ✅ Sottoprogetto Creato con Successo!

È stato clonato e personalizzato il sottoprogetto **SP00** da SP04 per la classificazione di **procedimenti amministrativi**.

## 📁 Struttura Creata

```
src/SP00/
├── README.md                                    # Questo file
├── QUICKSTART.md                                # Guida rapida
├── RIEPILOGO.md                                 # Riepilogo completo
├── start_streamlit.py                           # Avvio Streamlit (Python)
├── start_streamlit.sh                           # Avvio Streamlit (Bash)
└── procedural_classifier/
    ├── __init__.py                              # Module init
    ├── groq_procedural_classifier.py            # Classificatore principale
    ├── procedimenti_dataset.py                  # Dataset 50+ procedimenti
    ├── streamlit_procedural_app.py              # UI Streamlit
    ├── test_procedural_classifier.py            # Suite test
    └── esempio_workflow_integrazione.py         # Esempio integrazione
```

## 🎯 Cosa Fa SP00

Classifica **istanze di parte** (richieste cittadini/aziende) per identificare:

1. **Procedimento amministrativo** corretto
2. **Tipo di provvedimento** da emettere
3. **Normativa applicabile**
4. **Termini e scadenze**

### Esempio

**Input:**
```
Spettabile Comune, richiedo autorizzazione scarico acque reflue 
industriali da ciclo produttivo tessile. Portata: 500 m³/giorno.
```

**Output:**
```json
{
  "procedimento": "AUTORIZZAZIONE_SCARICO_ACQUE",
  "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
  "categoria": "AMBIENTE",
  "normativa_base": ["D.Lgs 152/2006"],
  "termini_giorni": 90,
  "confidence": 0.96
}
```

## 🚀 Come Provarlo (Veloce!)

### Prerequisiti

Se sei su **Windows**, ricorda di attivare il venv Python:

```bash
# Dalla root del progetto
source .venv/Scripts/activate  # PowerShell
# oppure
.venv\Scripts\activate.bat     # CMD
```

Su **macOS/Linux**:
```bash
source .venv/bin/activate
```

### Opzione 1: Interfaccia Streamlit (Consigliato)

```bash
# Dalla directory src/SP00
cd /Users/giangioiz/Documents/GitHub/Interzen/Interzen.POC/ZenIA/src/SP00

# Avvia Streamlit
streamlit run procedural_classifier/streamlit_procedural_app.py
```

Apri il browser su: **http://localhost:8501**

### Opzione 2: Test da Terminale

```bash
cd procedural_classifier
python test_procedural_classifier.py
```

Scegli:
- **1** = Quick test singola istanza
- **2** = Test con dataset (10 istanze)
- **3** = Entrambi

### Opzione 3: Generazione Dataset

```bash
cd procedural_classifier
python procedimenti_dataset.py
```

Genera un CSV con istanze di esempio.

## 📋 Configurazione API Key

Il sistema usa **Groq API** (gratuita) per la classificazione LLM.

### Setup

1. Ottieni API key gratuita: https://console.groq.com
2. Crea file `.env` in `src/`:

```bash
# src/.env
GROQ_API_KEY=your-groq-api-key-here
```

**Oppure** inserisci la key direttamente nell'interfaccia Streamlit.

## 🎓 Differenze da SP04

| Aspetto | SP04 | SP00 |
|---------|------|------|
| **Dominio** | Medical malpractice | Procedimenti PA |
| **Dimensioni** | 2 (multi-dim) | 1 (uni-dim) |
| **Categorie** | 4 (2×2) | 50+ procedimenti |
| **Output** | Tipologia + Riferimento | Procedimento + Metadata |
| **Guardrail** | Keyword + LLM | Da implementare |

## 📊 Dataset Incluso

- **50+ procedimenti** amministrativi
- **6 categorie**: Ambiente, Urbanistica, Commercio, Sociale, Mobilità, Cultura
- **Generazione automatica** di istanze realistiche
- **Metadata completi**: normativa, termini, autorità

### Esempi Procedimenti

- Autorizzazione Scarico Acque → Determinazione Dirigenziale
- Permesso di Costruire → Determinazione Dirigenziale
- Variante Urbanistica → Delibera Consiglio
- Licenza Commerciale → Determinazione Dirigenziale
- Occupazione Suolo Pubblico → Ordinanza

## 🧪 Modalità POC

Questo è un **Proof of Concept** per:

✅ Sperimentare strategie di classificazione  
✅ Testare diversi modelli LLM (8B vs 70B)  
✅ Valutare accuracy su varie categorie  
✅ Ottimizzare prompt engineering  
✅ Misurare performance e costi  

**Non è** un sistema production-ready (ancora).

## 📚 Documentazione Completa

- **[QUICKSTART.md](./QUICKSTART.md)** - Guida pratica passo-passo
- **[RIEPILOGO.md](./RIEPILOGO.md)** - Riepilogo dettagliato del progetto
- **[Specifiche SP00](../../docs/use_cases/generazione%20atti%20amministrativi/01%20SP00%20-%20Procedural%20Classifier.md)** - Specifiche tecniche

## 💡 Prossimi Passi

1. **Testare** il sistema con l'interfaccia Streamlit
2. **Valutare** accuracy su dataset completo
3. **Confrontare** modelli (8B vs 70B)
4. **Ottimizzare** prompt per casi specifici
5. **Espandere** dataset con nuovi procedimenti

## 🤝 Contributi

Suggerimenti e miglioramenti sono benvenuti!

## 📄 Licenza

Uso interno - Interzen POC

---

**Creato il**: 30 Ottobre 2025  
**Status**: ✅ Operativo  
**Versione**: 1.0.0
