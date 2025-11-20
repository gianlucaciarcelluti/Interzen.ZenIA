# Guida alla Integrazione dell'Intelligenza Artificiale in ZenShareUp
## Caso d'Uso - Protocollo Informatico
### Documento confidenziale interno di Specifiche Funzionali

*Versione in Bozza 1.0 - Novembre 2025*

---

## 📑 Indice

### 1. [Obiettivo del Sistema](#-1-obiettivo-del-sistema)

### 2. [Perché non funziona la modalità "One-Shot"?](#-2-perché-non-funziona-la-modalità-one-shot)

### 3. [I Componenti del Sistema (7 Sottoprogetti)](#-3-i-componenti-del-sistema-7-sottoprogetti)
- **SP01 - EML Parser & Email Intelligence** 📧 (riutilizzato)
- **SP10 - Dashboard di Trasparenza** 📊 (riutilizzato)
- **SP11 - Sicurezza e Audit** 🔒 (riutilizzato)
- **SP16 - Correspondence Classifier** 📬
- **SP17 - Protocol Registry Suggester** 📋
- **SP18 - Anomaly Detector** 🚨
- **SP19 - Protocol Workflow Orchestrator** ⚙️

### 4. [Glossario](#-glossario)
- **Termini Protocollo**
- **Termini Tecnologici AI**
- **Termini Software e Infrastruttura**
- **Acronimi e Sigle**
- **Normative Citate**

### 5. [Conclusioni](#-conclusioni)

---

<div style="page-break-after: always;"></div>

## 🎯 1. Obiettivo del Sistema

### Cosa vogliamo fare?
Automatizzare il **processo di protocollazione informatica** in ZenShare Up, utilizzando l'intelligenza artificiale per riconoscere automaticamente il tipo di corrispondenza, suggerire la corretta categorizzazione secondo il titolario di archivio, proporre il registro di protocollo appropriato e rilevare anomalie, riducendo errori e migliorando l'affidabilità dei registri.

### Il problema attuale
Oggi, la protocollazione informatica richiede:

1. ⏰ **Tempo richiesto**: Minuti per classificare ogni email/PEC
2. 📄 **Rischio errori**: Categorizzazioni errate, registri sbagliati
3. 🔍 **Difficoltà riconoscimento**: Distinguere istanze da comunicazioni
4. 📚 **Conoscenza necessaria**: Familiarità con titolario di archivio
5. 🔄 **Ripetitività**: Processi manuali ripetitivi per ogni messaggio

### La nostra soluzione
Un **assistente digitale intelligente** che:

✅ Riconosce automaticamente PEC vs email ordinaria
✅ Classifica corrispondenza (istanza, comunicazione, richiesta, etc.)
✅ Suggerisce categorizzazione secondo titolario di archivio
✅ Propone registro di protocollo corretto
✅ Rileva anomalie (duplicati, mancati protocolli)
✅ Fornisce explainability completa delle decisioni
✅ Riduce i tempi da minuti a secondi + verifica umana
✅ Garantisce conformità normativa (CAD, GDPR)

---

## ❌ 2. Perché non funziona la modalità "One-Shot"?

### Cosa significa "One-Shot"?
Chiedere all'intelligenza artificiale di classificare tutto in un'unica volta senza passaggi intermedi.

### Esempio pratico - Approccio One-Shot
```
❌ RICHIESTA: "Classifica questa email per protocollo"

PROBLEMI:
1. L'AI non conosce il titolario specifico dell'ente
2. Non può verificare congruenza con normative
3. Non garantisce coerenza con registri esistenti
4. Non traccia il processo decisionale
```

### Perché questo non funziona?

#### 🚨 Problema 1: Complessità del titolario
Ogni ente ha titolari di archivio specifici con centinaia di categorie.

#### 🚨 Problema 2: Mancanza di contesto
Senza conoscenza dei registri esistenti, le decisioni possono essere incoerenti.

#### 🚨 Problema 3: Impossibile migliorare
Se l'output è sbagliato, non si sa quale aspetto correggere.

---

### ✅ La nostra soluzione: Approccio "Multi-Step"

Dividiamo il lavoro in fasi specializzate:

```
📥 INPUT: "Email PEC in arrivo"

PASSO 1 - Parsing: Estrai contenuto e metadati
PASSO 2 - Classificazione: Riconosci tipo corrispondenza
PASSO 3 - Categorizzazione: Applica titolario di archivio
PASSO 4 - Suggerimento: Proponi registro protocollo
PASSO 5 - Validazione: Rileva anomalie
PASSO 6 - Protocollo: Registra automaticamente

📤 OUTPUT: Email protocollata correttamente in secondi
```

---

## 🧩 3. I Componenti del Sistema (7 Sottoprogetti)

Immaginiamo il sistema come una **pipeline intelligente di protocollazione**.

---

<div style="page-break-after: always;"></div>

### **SP01 - EML Parser & Email Intelligence** 📧 (riutilizzato)

**Cosa fa**: Parsifica email/PEC e estrae contenuto intelligente.

**Come funziona**: Come in generazione atti, ma focalizzato su corrispondenza.

**Input/Output**: Email/PEC, output contenuto strutturato.

**Tecnologie**: IMAPClient, DistilBERT.

---

### **SP16 - Correspondence Classifier** 📬

**Cosa fa**: Classifica automaticamente il tipo di corrispondenza.

**Come funziona**: AI per riconoscere istanza vs comunicazione vs richiesta.

**Input/Output**: Testo email, output tipo corrispondenza e confidenza.

**Tecnologie**: BERT, spaCy.

---

### **SP17 - Protocol Registry Suggester** 📋

**Cosa fa**: Suggerisce il registro di protocollo corretto.

**Come funziona**: Applica regole e AI per matching con titolario.

**Input/Output**: Classificazione, output registro suggerito.

**Tecnologie**: Rule Engine, ML classifiers.

---

### **SP18 - Anomaly Detector** 🚨

**Cosa fa**: Rileva anomalie nel flusso di protocollazione.

**Come funziona**: Monitora pattern e rileva irregolarità.

**Input/Output**: Eventi protocollo, output alert anomalie.

**Tecnologie**: Isolation Forest, statistical analysis.

---

### **SP10 - Dashboard di Trasparenza** 📊 (riutilizzato)

**Cosa fa**: Mostra stato protocollazione e decisioni AI.

**Come funziona**: Interfaccia per monitoraggio real-time.

**Input/Output**: Dati da tutti SP, output dashboard.

**Tecnologie**: Streamlit, D3.js.

---

### **SP11 - Sicurezza e Audit** 🔒 (riutilizzato)

**Cosa fa**: Garantisce sicurezza e tracciabilità.

**Come funziona**: Audit trail per ogni operazione protocollo.

**Input/Output**: Eventi sistema, output log sicuri.

**Tecnologie**: ELK Stack, JWT.

---

### **SP19 - Protocol Workflow Orchestrator** ⚙️

**Cosa fa**: Coordina il flusso di protocollazione.

**Come funziona**: Orchestrazione pipeline protocollo.

**Input/Output**: Email in ingresso, output protocollo completato.

**Tecnologie**: Apache NiFi, Airflow.

---

## 📖 Glossario

### Termini Protocollo
- **Titolario di Archivio**: Schema di classificazione documenti.
- **Registro di Protocollo**: Libro ufficiale delle corrispondenze.

### Termini Tecnologici AI
- **Correspondence Classification**: Classificazione automatica corrispondenza.
- **Anomaly Detection**: Rilevamento irregolarità.

### Termini Software e Infrastruttura
- **IMAP**: Protocollo accesso email.
- **Titolario**: Classificazione archivistica.

### Acronimi e Sigle
- **PEC**: Posta Elettronica Certificata.
- **CAD**: Codice Amministrazione Digitale.

### Normative Citate
- CAD, GDPR.

---

## 🎉 5. Conclusioni

Il Protocollo Informatico trasforma la protocollazione in un processo intelligente e affidabile.</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC2 - Protocollo Informatico/Guida_UC2_Protocollo_Informatico.md
