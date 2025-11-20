# Riepilogo Casi d'Uso - Introduzione AI in ZenShare Up

Questo documento riepiloga i casi d'uso individuati nel documento "Specifiche_AI_ZenShareUp_V.3_19092025.docx", basati sulle aree di intervento per l'AI in ZenShare Up.

---

## ⚙️ Architettura Logica: SP (Sottoprogetti) vs MS (Microservizi)

### SP - Sottoprogetti (72 totali, escluso SP28 riservato)
**Definizione**: Componenti **logici e specifici per dominio**, descrivono COSA implementare e per quale business value.
- Es: SP02 "Document Extractor", SP16 "Correspondence Classifier"
- Organizzati per **caso d'uso** (6 SP in UC1, 4 SP in UC2, etc.)
- Facilitano **distribuzione del lavoro** e **descrizione funzionale**
- Ogni SP ha propria documentazione con responsabilità, input/output, dipendenze

**Nota Numerazione**: La numerazione SP01-SP72 ha un **gap intenzionale in SP28** (riservato per future estensioni architetturali). Per dettagli, vedi [SP28-RESERVED.md](../SP28-RESERVED.md).

### MS - Microservizi (16 totali)
**Definizione**: Componenti **fisici e generici**, rappresentano la **implementazione tecnica riusabile**.
- Es: MS01 "Generic Classifier Engine", MS02 "Generic Analyzer Engine"
- **Condivisi** tra multipli SP e UC
- Facilitano **riusabilità tecnica** e **scaling infrastrutturale**
- Ciascuno ha architettura, API, deployment centralizzati

### Relazione SP ↔ MS
- **1 SP** usa **1+ MS** (SP02 usa MS01 primario + MS05 supporto)
- **1 MS** supporta **multipli SP** da diversi UC (MS01 supporta SP02, SP03, SP07, SP16, SP17, SP34...)
- **Mapping completo**: vedi [SP-MS-MAPPING-MASTER.md](../SP-MS-MAPPING-MASTER.md)

---

## UC1 - Sistema di Gestione Documentale
**Cosa fa**: Classificazione automatica documenti (determine, delibere, contratti, fatture). Estrazione metadati e dati chiave. Ricerca semantica e Q&A. Summarization documenti lunghi.

**Caratteristiche principali**:
- Classificazione automatica tipologia documenti
- Estrazione metadati (oggetto, ente, scadenza, CIG/CUP)
- Ricerca semantica oltre full text
- Summarization per schede riepilogative
- Explainability: evidenzia parti documento per classificazione/risposta
- Valore: riduzione tempi protocollazione, reperibilità immediata

## UC2 - Protocollo Informatico
**Cosa fa**: Riconoscimento automatico tipologia corrispondenza (PEC vs email, istanza vs comunicazione). Suggerimenti categorizzazione per titolario. Pre-suggerimento registro protocollo. Detezione anomalie.

**Caratteristiche principali**:
- Riconoscimento linguistico + categorizzazione
- Suggerimento registro protocollo corretto
- Detezione anomalie (duplicati, PEC non protocollate)
- Explainability: log motivazioni classificazione
- Valore: meno errori protocollazione, affidabilità registri

## UC3 - Governance (Organigramma, Procedimenti, Procedure)
**Cosa fa**: Mappatura procedimenti con suggerimenti collegamenti. Assistente AI per policy/procedure. Analisi conformità gap tra procedimenti e normativa.

**Caratteristiche principali**:
- AI per mappatura procedimenti
- Assistente spiegazione regolamenti/procedure
- Analisi gap conformità
- Valore: governance chiara, supporto rispetto regole

## UC4 - BPM e Automazione Processi
**Cosa fa**: Routing intelligente basato su carico/ruolo/precedenti. Suggerimenti approvazioni. Predizione colli di bottiglia. Ottimizzazione processi. Rilevamento anomalie.

**Caratteristiche principali**:
- Routing intelligente workflow
- Suggerimenti instradamenti/approvazioni
- Predizione ottimizzazione flussi
- Rilevamento anomalie (tempi lunghi, step saltati)
- Explainability: dashboard "perché" assegnazione
- Valore: tempi ridotti, efficienza flussi

## UC5 - Produzione Documentale Integrata nel BPM (Atti, Delibere, Determine)
**Cosa fa**: Generazione automatica bozze da template e dati strutturati. Controllo semantico elementi obbligatori. Supporto redazione linguaggio normativo.

**Caratteristiche principali**:
- Generazione bozze automatiche
- Controllo semantico completezza (premessa normativa, riferimenti)
- Suggerimenti linguaggio corretto
- Valore: riduzione tempi redazione, qualità/conformità

## UC6 - Firma Digitale Integrata
**Cosa fa**: Validazione preventiva controlli intelligenti pre-firma. Verifica firme digitali multiple e marcature temporali.

**Caratteristiche principali**:
- Controlli intelligenti errori/incongruenze
- Verifica firme multiple e timestamp
- Valore: meno errori flussi firma, atti validi primo colpo

## UC7 - Conservazione Digitale
**Cosa fa**: Classificazione automatica pacchetti versamento (SIP). Preservazione predittiva rischi leggibilità. Controlli coerenza metadati/fascicolazione.

**Caratteristiche principali**:
- Classificazione pacchetti versamento
- Preservazione predittiva (formati obsoleti)
- Controlli coerenza metadati
- Valore: archivi sicuri, meno rischio non conformità AgID

## UC8 - Integrazione con SIEM (Sicurezza Informatica)
**Cosa fa**: Detection anomalie nei log (accessi insoliti, volumi anomali). Analisi predittiva incidenti.

**Caratteristiche principali**:
- AI per anomaly detection log
- Analisi predittiva incidenti
- Explainability: motivare alert
- Valore: maggiore sicurezza, riduzione data breach, supporto SOC/SIEM

## UC9 - Compliance & Risk Management
**Cosa fa**: Controllo conformità normativa (CAD, GDPR, linee guida AgID). Alert predittivi non conformità in protocollazione/firme/conservazione.

**Caratteristiche principali**:
- Controllo conformità CAD/GDPR/AgID
- Alert predittivi non conformità
- Valore: riduzione rischi compliance

## UC10 - Supporto all'Utente
**Cosa fa**: Assistente AI integrato per guida compilazione/protocollazione/creazione fascicoli. Helpdesk conversazionale contestuale.

**Caratteristiche principali**:
- Assistente guida processi
- Helpdesk conversazionale integrato
- Valore: supporto utenti in attività quotidiane

## UC11 - Analisi Dati e Reporting
**Cosa fa**: Dashboard predittive volumi protocollazione/trend acquisti/workload. Riconciliazione/correlazione automatica documenti (determina → ordine → fattura → pagamento).

**Caratteristiche principali**:
- Dashboard predittive trend
- Riconciliazione automatica documenti correlati
- Valore: supporto governance, allocazione risorse

---

# Mappatura Use Case ↔ Microservizi

## Elenco Microservizi

I microservizi rappresentano componenti generici e configurabili che sostituiscono i precedenti sottoprogetti specifici (SP). Ecco l'elenco completo:

- **MS01**: Generic Classifier Engine - Classificazione e categorizzazione intelligente di documenti, contenuti e corrispondenza
- **MS02**: Generic Analyzer Engine - Analisi semantica avanzata e processamento intelligente dei dati
- **MS03**: Generic Orchestrator Engine - Orchestrazione e coordinamento di processi distribuiti complessi
- **MS04**: Generic Validator Engine - Validazione semantica, strutturale e compliance di documenti/processi
- **MS05**: Generic Storage Manager - Gestione unificata dello storage e ottimizzazione dati
- **MS06**: Generic Knowledge Base - Repository centralizzato di conoscenza, metadati e informazioni strutturate
- **MS07**: Generic ETL Pipeline - Estrazione, trasformazione e caricamento dati da multiple fonti
- **MS08**: Generic Workflow Engine - Gestione e esecuzione di workflow e processi business
- **MS09**: Generic Notification Engine - Sistema unificato per notifiche e comunicazione multi-canale
- **MS10**: Generic Analytics & Reporting - Analisi dati, business intelligence e generazione report
- **MS11**: Generic Integration Hub - Integrazione con sistemi esterni e orchestrazione API
- **MS12**: Generic User Interface - Interfacce utente adattive e moderne per esperienze digitali
- **MS13**: Generic Security Engine - Sicurezza completa per dati, utenti e sistemi
- **MS14**: Generic Audit Engine - Audit, tracciamento e reporting delle attività di sistema
- **MS15**: Generic Configuration Engine - Gestione centralizzata delle configurazioni di sistema
- **MS16**: Generic Monitoring Engine - Monitoraggio completo e osservabilità delle performance

## Matrice di Utilizzo: SP per UC

La tabella seguente mostra la distribuzione dei **Sottoprogetti (SP)** per caso d'uso:

| UC | SP Inclusi | Numero | Tipo |
|----------|-----------|--------|------|
| UC1 | SP02, SP07, SP12, SP13, SP14, SP15 | 6 | Document Management |
| UC2 | SP01, SP16, SP17, SP18, SP19 | 5 | Protocol & Correspondence |
| UC3 | SP20, SP21, SP22, SP23 | 4 | Governance |
| UC4 | SP24, **SP25**, SP26, SP27 | 4 | BPM & Process Automation |
| UC5 | SP01-SP11 | 11 | Integrated Document Production |
| UC6 | SP29, SP30, SP31, SP32 | 4 | Digital Signature |
| UC7 | SP33, SP34, SP35, SP36, **SP37** | 5 | Digital Archive & Preservation |
| UC8 | SP38, SP39, SP40, SP41 | 4 | SIEM Integration |
| UC9 | SP42, SP43, SP44, SP45, SP46, SP47, SP48, SP49, **SP50** | 9 | Compliance & Risk |
| UC10 | SP51, SP52, SP53, SP54, SP55, SP56, SP57 | 7 | User Support |
| UC11 (Analytics) | SP58, SP59, SP60, SP61, SP62, SP63, SP64 | 7 | Analytics & Reporting |
| UC11 (Infrastructure) | SP65, SP66, SP67, SP68, SP69, SP70, **SP71**, **SP72** | 8 | Cross-Cutting Infrastructure |
| **TOTAL** | **SP01-SP72** | **72** | |

---

## 📚 Risorse Globali Documentazione

Prima di iniziare a consultare i singoli UC, consulta questi documenti centrali:

| Risorsa | Descrizione | Link |
|---------|-------------|------|
| **Glossario Terminologico** | 70+ termini standardizzati EN/IT | [GLOSSARIO-TERMINOLOGICO.md](../GLOSSARIO-TERMINOLOGICO.md) |
| **Conformità Normativa** | Mapping L.241/1990, CAD, GDPR, eIDAS, AI Act | [COMPLIANCE-MATRIX.md](../COMPLIANCE-MATRIX.md) |
| **JSON Payload Standard** | Template request/response standardizzati | [templates/json-payload-standard.md](../templates/json-payload-standard.md) |
| **Conformità Standard Template** | Template sezione conformità per SP | [templates/conformita-normativa-standard.md](../templates/conformita-normativa-standard.md) |
| **UC INDEX Standard Template** | Template per UC INDEX files | [templates/uc-index-standard.md](../templates/uc-index-standard.md) |

---

## 🎯 Quick Start per Ruoli

### Per Product Manager
1. Leggere overview UC qui sopra (5 min)
2. Aprire UC INDEX desiderato → `00 INDEX.md`
3. Leggere "Overview" e "Key Workflows" (10 min)

### Per Developer
1. Consultare GLOSSARIO-TERMINOLOGICO per termini standardizzati
2. Navigare a UC desiderato → `00 INDEX.md` → SP specifico
3. Leggere SPECIFICATION.md e JSON Payload examples
4. Riferirsi a JSON Payload Standard Template per nuove API

### Per Compliance Officer
1. Leggere COMPLIANCE-MATRIX.md per panoramica
2. Navigare a UC desiderato → `00 INDEX.md`
3. Consultare sezione "Conformità Normativa" in ogni SP
4. Verificare GDPR, CAD, eIDAS compliance

### Per Tech Writer
1. Consultare GLOSSARIO-TERMINOLOGICO per terminologia coerente
2. Usare template conformita-normativa-standard.md per nuovi SP
3. Riferirsi a json-payload-standard.md per documentare API
4. Mantenere coerenza EN/IT come da GLOSSARIO

---

## 📊 Statistiche Documentazione

- **Total UC**: 11 (UC1-UC11)
- **Total SP**: 72 (SP01-SP72, escluso SP28 riservato)
- **Total MS**: 16 (MS01-MS16)
- **UC INDEX**: 11 file creati (1 per UC)
- **Conformità Normativa**: 100% SP documented
- **Glossario Terminologico**: 70+ termini standardizzati
- **Broken Links**: 0 ✅
- **JSON Validation**: 100% ✅

---

## 🔗 Navigazione per UC

Seleziona un UC per accedere al suo INDEX centralizzato:

**Note - Gap Resolution Status**:
- ✅ **SP25** - "Forecasting & Predictive Scheduling Engine" (UC4) - CREATO e DOCUMENTATO
- ✅ **SP31** - "Timestamp Authority & Temporal Marking" (UC6) - CREATO e DOCUMENTATO
- ✅ **SP32** - "Post-Signature Auditor" (UC6) - CREATO e DOCUMENTATO
- ✅ **SP37** - "Archive Metadata Manager" (UC7) - CREATO e DOCUMENTATO
- ✅ **SP50** - "Compliance Training & Certification" (UC9) - CREATO e DOCUMENTATO
- ✅ **SP57** - "User Feedback Management" (UC10) - **CREATO e DOCUMENTATO** (aggiornamento di sessione)
- ✅ **SP70** - "Incident Management & Escalation" (UC11) - CREATO e DOCUMENTATO
- ✅ **SP71** - "Performance Optimization & Scaling" (UC11) - **CREATO e DOCUMENTATO** (aggiornamento di sessione)
- ✅ **SP72** - "Incident Management & Escalation" (UC11) - **CREATO e DOCUMENTATO** (aggiornamento di sessione)

**Struttura UC11**:
- **SP58-SP64**: Analytics Core (7 SP) - Data Lake, ETL, ML, Portal, Quality, Real-Time, Forecasting
- **SP65-SP72**: Infrastrutture Cross-Cutting (8 SP) - Monitoring, Security, API Gateway, DevOps, DR, Compliance, Performance Optimization, Incident Management
- Tutti gli SP65-SP72 sono **enablers per TUTTI gli UC**, non solo UC11-specifiche

**Matrici Dipendenze**:
- ✅ UC10: `03 Dependency Matrix UC10.md` - aggiornata con SP57
- ✅ UC11: `02 Matrice Dipendenze.md` - aggiornata con SP71 e SP72

---

## Matrice di Utilizzo: MS per UC

La tabella seguente mostra quali **Microservizi (MS)** sono utilizzati in ciascun caso d'uso. Un ✓ indica che il MS è utilizzato nel UC con configurazioni specifiche per il dominio.

| UC | MS01 | MS02 | MS03 | MS04 | MS05 | MS06 | MS07 | MS08 | MS09 | MS10 | MS11 | MS12 | MS13 | MS14 | MS15 | MS16 |
|----------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| UC1 | ✓ |  |  |  | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ |  |  |  |
| UC2 | ✓ |  | ✓ | ✓ |  |  | ✓ |  | ✓ |  |  |  |  | ✓ |  | ✓ |
| UC3 |  |  | ✓ | ✓ |  | ✓ |  | ✓ |  |  | ✓ |  | ✓ | ✓ |  |  |
| UC4 |  |  | ✓ | ✓ |  |  | ✓ | ✓ | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ |
| UC5 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  | ✓ |  |  |  | ✓ |  |  |  |  |
| UC6 |  |  | ✓ | ✓ |  |  |  | ✓ |  |  |  |  | ✓ | ✓ | ✓ |  |
| UC7 |  |  |  | ✓ | ✓ | ✓ | ✓ |  |  |  |  |  | ✓ | ✓ |  | ✓ |
| UC8 |  |  |  |  |  |  | ✓ |  | ✓ | ✓ |  |  | ✓ | ✓ |  | ✓ |
| UC9 |  |  |  | ✓ |  | ✓ |  | ✓ | ✓ | ✓ |  |  | ✓ | ✓ |  |  |
| UC10 |  |  |  |  |  | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ | ✓ |  |  |
| UC11 |  | ✓ |  |  | ✓ |  | ✓ |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/riepilogo_casi_uso.md
