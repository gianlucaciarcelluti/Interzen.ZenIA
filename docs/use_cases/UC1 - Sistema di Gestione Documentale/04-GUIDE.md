# Guida alla Integrazione dell'Intelligenza Artificiale in ZenShareUp
## Caso d'Uso - Sistema di Gestione Documentale
### Documento confidenziale interno di Specifiche Funzionali

*Versione in Bozza 1.0 - Novembre 2025*

---

## 📑 Indice

### 1. [Obiettivo del Sistema](#-1-obiettivo-del-sistema)

### 2. [Perché non funziona la modalità "One-Shot"?](#-2-perché-non-funziona-la-modalità-one-shot)

### 3. [I Componenti del Sistema (8 Sottoprogetti)](#-3-i-componenti-del-sistema-8-sottoprogetti)
- **SP02 - Document Extractor & Attachment Classifier** 📎 (riutilizzato)
- **SP07 - Content Classifier** 🏷️ (riutilizzato)
- **SP10 - Dashboard di Trasparenza** 📊 (riutilizzato)
- **SP11 - Sicurezza e Audit** 🔒 (riutilizzato)
- **SP12 - Semantic Search & Q&A Engine** 🔍
- **SP13 - Document Summarizer** 📄
- **SP14 - Metadata Indexer** 🗂️
- **SP15 - Document Workflow Orchestrator** ⚙️

### 4. [Glossario](#-glossario)
- **Termini Documentali**
- **Termini Tecnologici AI**
- **Termini Software e Infrastruttura**
- **Acronimi e Sigle**
- **Normative Citate**

### 5. [Conclusioni](#-conclusioni)

---

<div style="page-break-after: always;"></div>

## 🎯 1. Obiettivo del Sistema

### Cosa vogliamo fare?
Automatizzare la **gestione intelligente dei documenti** in ZenShare Up, utilizzando l'intelligenza artificiale per classificare automaticamente documenti, estrarre metadati chiave, abilitare ricerca semantica e fornire riassunti intelligenti, riducendo i tempi di protocollazione e migliorando la reperibilità.

### Il problema attuale
Oggi, la gestione documentale in ZenShare Up richiede:

1. ⏰ **Tempo richiesto**: Ore per classificare e indicizzare documenti manualmente
2. 📄 **Rischio errori**: Classificazioni errate, metadati incompleti, documenti persi
3. 🔍 **Ricerca inefficiente**: Difficoltà nel trovare documenti specifici senza conoscenza esatta
4. 📚 **Mancanza di insight**: Nessun riassunto automatico o Q&A sui contenuti
5. 🔄 **Ripetitività**: Processi manuali ripetitivi per ogni documento

### La nostra soluzione
Un **assistente digitale intelligente** che:

✅ Classifica automaticamente i documenti (determine, delibere, contratti, fatture)  
✅ Estrae metadati chiave (oggetto, ente, scadenza, CIG/CUP)  
✅ Abilita ricerca semantica oltre il full text  
✅ Genera riassunti intelligenti per schede riepilogative  
✅ Fornisce risposte Q&A contestuali sui documenti  
✅ Riduce i tempi da ore a minuti (parte automatica) + verifica umana  
✅ Garantisce trasparenza e conformità (GDPR incluso)

---

## ❌ 2. Perché non funziona la modalità "One-Shot"?

### Cosa significa "One-Shot"?
Chiedere all'intelligenza artificiale di gestire tutto il documento in un'unica volta senza passaggi intermedi.

### Esempio pratico - Approccio One-Shot
```
❌ RICHIESTA: "Classifica questo documento e estrai i metadati"

PROBLEMI:
1. L'AI non sa quale schema di classificazione usare
2. Non può verificare l'accuratezza dei metadati estratti
3. Non garantisce la coerenza con il sistema esistente
4. Non traccia il processo per audit
```

### Perché questo non funziona?

#### 🚨 Problema 1: Complessità delle tassonomie
Un sistema documentale deve rispettare tassonomie specifiche (es. titolario di archivio, normative AgID).

#### 🚨 Problema 2: Mancanza di controlli
Con One-Shot non si può verificare coerenza o completezza.

#### 🚨 Problema 3: Impossibile migliorare
Se l'output è sbagliato, non si sa quale passaggio correggere.

---

### ✅ La nostra soluzione: Approccio "Multi-Step"

Dividiamo il lavoro in fasi specializzate:

```
📥 INPUT: "Documento PDF di una delibera"

PASSO 1 - Estrazione: Estrai testo e metadati base
PASSO 2 - Classificazione: Identifica tipo documento
PASSO 3 - Indicizzazione: Inserisci in indice semantico
PASSO 4 - Ricerca: Abilita Q&A e ricerca avanzata
PASSO 5 - Riassunto: Genera scheda riepilogativa
PASSO 6 - Dashboard: Mostra risultati e audit

📤 OUTPUT: Documento classificato, ricercabile, riassunto in secondi
```

---

## 🧩 3. I Componenti del Sistema (8 Sottoprogetti)

Immaginiamo il sistema come una **pipeline intelligente** per la gestione documentale.

---

<div style="page-break-after: always;"></div>

### **SP02 - Document Extractor & Attachment Classifier** 📎 (riutilizzato)

**Cosa fa**: Estrae testo e classifica allegati da documenti.

**Come funziona**: Come in generazione atti, ma focalizzato su documenti esistenti.

**Input/Output**: Documenti PDF/DOC, output testo estratto e classificazione base.

**Tecnologie**: Tesseract, PyPDF2, LayoutLM.

---

### **SP07 - Content Classifier** 🏷️ (riutilizzato)

**Cosa fa**: Classifica contenuto documento (delibera, contratto, etc.).

**Come funziona**: AI per categorizzazione automatica.

**Input/Output**: Testo estratto, output categoria e confidenza.

**Tecnologie**: DistilBERT, spaCy.

---

### **SP12 - Semantic Search & Q&A Engine** 🔍

**Cosa fa**: Abilita ricerca semantica e risposte a domande sui documenti.

**Come funziona**: Usa modelli AI per comprensione semantica.

**Input**: Query utente, output risultati rilevanti e risposte.

**Tecnologie**: FAISS, BERT, LangChain.

---

### **SP13 - Document Summarizer** 📄

**Cosa fa**: Genera riassunti intelligenti di documenti lunghi.

**Come funziona**: AI per estrazione punti chiave.

**Input**: Documento, output scheda riepilogativa.

**Tecnologie**: GPT-4, summarization models.

---

### **SP14 - Metadata Indexer** 🗂️

**Cosa fa**: Indicizza metadati per ricerca veloce.

**Come funziona**: Crea indici strutturati.

**Input**: Metadati estratti, output indice ricercabile.

**Tecnologie**: Elasticsearch, PostgreSQL.

---

### **SP10 - Dashboard di Trasparenza** 📊 (riutilizzato)

**Cosa fa**: Mostra stato documenti e risultati AI.

**Come funziona**: Interfaccia visuale per monitoraggio.

**Input**: Dati da tutti SP, output dashboard.

**Tecnologie**: Streamlit, D3.js.

---

### **SP11 - Sicurezza e Audit** 🔒 (riutilizzato)

**Cosa fa**: Garantisce sicurezza e tracciabilità.

**Come funziona**: Audit trail per ogni operazione.

**Input**: Eventi sistema, output log sicuri.

**Tecnologie**: ELK Stack, JWT.

---

### **SP15 - Document Workflow Orchestrator** ⚙️

**Cosa fa**: Coordina il flusso di processamento documenti.

**Come funziona**: Orchestrazione pipeline.

**Input**: Documento in ingresso, output processamento completo.

**Tecnologie**: Apache NiFi, Airflow.

---

## 📖 Glossario

### Termini Documentali
- **Titolario di Archivio**: Schema di classificazione documenti.
- **Metadati**: Informazioni descrittive del documento.

### Termini Tecnologici AI
- **Ricerca Semantica**: Ricerca basata su significato, non parole esatte.
- **Summarization**: Riassunto automatico di testi.

### Termini Software e Infrastruttura
- **FAISS**: Libreria per ricerca vettoriale.
- **Elasticsearch**: Motore di ricerca.

### Acronimi e Sigle
- **AgID**: Agenzia per l'Italia Digitale.

### Normative Citate
- GDPR, CAD.

---

## 🎉 5. Conclusioni

Il Sistema di Gestione Documentale trasforma ZenShare Up in una piattaforma intelligente, riducendo costi e migliorando efficienza.</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC1 - Sistema di Gestione Documentale/Guida_UC1_Sistema_Gestione_Documentale.md