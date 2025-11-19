# SP00 - Procedural Classifier

Sistema di classificazione procedimenti amministrativi → provvedimenti finali per la Pubblica Amministrazione.

## 🎯 Obiettivo

Classificare le **istanze di parte** (richieste dei cittadini/aziende) per:
1. **Identificare il procedimento amministrativo** corretto
2. **Determinare il tipo di provvedimento** finale da emettere

## 📋 Specifiche

### Input
- Oggetto dell'istanza
- Descrizione/motivazione
- Dati richiedente
- Eventuale normativa citata
- Allegati (tipologia e numero)

### Output
- **Procedimento amministrativo** identificato (es: "Autorizzazione Scarico Acque")
- **Tipo provvedimento** da emettere (es: "Determinazione Dirigenziale")
- **Confidence score** della classificazione
- **Normativa di riferimento** applicabile
- **Termini procedimentali** (scadenze)
- **Metadata richiesti** per il procedimento

### Dimensione di Classificazione

A differenza di SP04 (multi-dimensionale), SP00 classifica su **una sola dimensione**:

**PROCEDIMENTO AMMINISTRATIVO → PROVVEDIMENTO**

Esempi di mapping:
- Autorizzazione Scarico Acque → Determinazione Dirigenziale
- Permesso di Costruire → Determinazione Dirigenziale  
- Variante Urbanistica → Delibera Consiglio Comunale
- Licenza Commerciale → Determinazione Dirigenziale
- Occupazione Suolo Pubblico → Ordinanza Sindacale

## 🏗️ Architettura

```
SP00/
├── procedural_classifier/
│   ├── groq_procedural_classifier.py    # Classificatore LLM con Groq
│   ├── streamlit_procedural_app.py      # UI per testing
│   ├── api_procedural_classifier.py     # API FastAPI
│   ├── procedimenti_dataset.py          # Dataset procedimenti PA
│   └── test_procedural_classifier.py    # Test suite
├── README.md
└── QUICKSTART.md
```

## 🚀 Quick Start

### 1. Installazione Dipendenze

```bash
# Dalla root del progetto
cd src
pip install -r requirements.txt
```

### 2. Configurazione API Key

Crea un file `.env` nella cartella `src/`:

```bash
GROQ_API_KEY=your-groq-api-key-here
```

Ottieni una chiave gratuita su: https://console.groq.com

### 3. Test Rapido

```bash
cd SP00/procedural_classifier
python test_procedural_classifier.py
```

### 4. Avvia Interfaccia Streamlit

```bash
streamlit run streamlit_procedural_app.py
```

### 5. Avvia API FastAPI

```bash
uvicorn api_procedural_classifier:app --reload
```

API disponibile su: http://localhost:8000/docs

## 📊 Esempi di Classificazione

### Esempio 1: Autorizzazione Ambientale

**Input:**
```
Oggetto: Richiesta autorizzazione scarico acque reflue industriali
Richiedente: Industria Tessile Rossi S.p.A.
Descrizione: Richiesta autorizzazione per scarico acque reflue 
             provenienti da ciclo produttivo tessile...
```

**Output:**
```json
{
  "procedimento": "AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE",
  "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
  "categoria": "AMBIENTE",
  "autorita_competente": "DIRIGENTE_SETTORE_AMBIENTE",
  "normativa_base": ["D.Lgs 152/2006", "L.R. 62/1998"],
  "termini_giorni": 90,
  "confidence": 0.96
}
```

### Esempio 2: Urbanistica

**Input:**
```
Oggetto: Richiesta permesso di costruire
Richiedente: Mario Rossi
Descrizione: Richiesta permesso costruzione villetta unifamiliare...
```

**Output:**
```json
{
  "procedimento": "PERMESSO_DI_COSTRUIRE",
  "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
  "categoria": "URBANISTICA",
  "autorita_competente": "DIRIGENTE_EDILIZIA",
  "normativa_base": ["D.P.R. 380/2001"],
  "termini_giorni": 60,
  "confidence": 0.94
}
```

## 🧪 Dataset POC

Il sistema include un dataset di esempio con:

- 50+ tipologie di procedimenti amministrativi
- Mappatura procedimento → tipo provvedimento
- Normativa di riferimento per ogni procedimento
- Termini e scadenze procedurali
- Metadata richiesti

**Categorie Procedimenti:**
- Ambiente (VIA, scarichi, emissioni, bonifiche)
- Urbanistica (permessi costruire, varianti, certificati)
- Commercio (licenze, SCIA, occupazione suolo)
- Sociale (assegnazione alloggi, contributi)
- Mobilità (ZTL, parcheggi, autorizzazioni trasporto)
- Cultura (patrocini, utilizzo spazi)

## 🔧 Tecnologie

- **LLM**: Groq API (modelli Llama 3.1/3.3)
- **Framework**: FastAPI + Streamlit
- **NLP**: spaCy per Named Entity Recognition
- **Cache**: Redis (opzionale, per produzione)
- **Database**: PostgreSQL (opzionale, per produzione)

## 📈 Performance Target (POC)

- **Latency p95**: < 1 secondo
- **Accuracy**: > 90% su dataset test
- **Throughput**: ~60 classificazioni/minuto
- **Cache hit rate**: ~40% (con Redis)

## 🎓 Modalità POC

Questo è un **Proof of Concept** per:
- ✅ Sperimentare strategie di classificazione
- ✅ Testare diversi modelli LLM (Llama 3.1 8B vs 70B)
- ✅ Confrontare approcci (keyword-based vs LLM puro vs ibrido)
- ✅ Studiare accuracy e performance
- ✅ Definire prompt engineering ottimale

**NON è:**
- ❌ Sistema production-ready
- ❌ Integrato con database reali
- ❌ Con autenticazione/autorizzazione
- ❌ Scalabile per grandi volumi

## 📖 Documentazione Completa

Vedi:
- [Guida Rapida](./QUICKSTART.md)
- [Specifiche SP00](../../docs/use_cases/generazione%20atti%20amministrativi/01%20SP00%20-%20Procedural%20Classifier.md)
- [Architettura Generale](../../docs/use_cases/generazione%20atti%20amministrativi/00%20Architettura%20Generale%20Microservizi.md)

## 🤝 Contribuire

Questo è un progetto di ricerca e sperimentazione. Suggerimenti benvenuti!

## 📄 Licenza

Uso interno - Interzen POC
