# Guida alla Integrazione dell'Intelligenza Artificiale in ZenShareUp
## Caso d'Uso - Generazione Automatica degli Atti Amministrativi
### Documento confidenziale interno di Specifiche Funzionali

*Versione in Bozza 2.0 - Ottobre 2025*

---

## 📑 Indice

### 1. [Obiettivo del Sistema](#-1-obiettivo-del-sistema)

### 2. [Perché non funziona la modalità "One-Shot"?](#-2-perché-non-funziona-la-modalità-one-shot)

### 3. [I Componenti del Sistema (11 Sottoprogetti)](#-3-i-componenti-del-sistema-11-sottoprogetti)
- **SP01 - EML Parser & Email Intelligence** 📧
- **SP02 - Document Extractor & Attachment Classifier** 📎
- **SP03 - Classificatore di Procedimenti Amministrativi** 🎯
- **SP04 - Archivio Normativo Intelligente** 📚
- **SP05 - Motore di Generazione Template** 🤖
- **SP06 - Validatore di Conformità** ✅
- **SP07 - Classificatore e Estrattore Dati** 🏷️
- **SP08 - Controllo Qualità Linguistica** 📝
- **SP09 - Motore di Orchestrazione** ⚙️
- **SP10 - Dashboard di Trasparenza** 📊
- **SP11 - Sicurezza e Audit** 🔒

### 4. [Glossario](#-glossario)
- **Termini Amministrativi**
- **Termini Tecnologici AI**
- **Termini Software e Infrastruttura**
- **Acronimi e Sigle**
- **Normative Citate**

### 5. [Conclusioni](#-conclusioni)

---

<div style="page-break-after: always;"></div>

## 🎯 1. Obiettivo del Sistema

### Cosa vogliamo fare?
Automatizzare la **creazione di documenti ufficiali** (delibere, determine, ordinanze) per la Pubblica Amministrazione utilizzando l'intelligenza artificiale, riducendo i tempi da ore a minuti e minimizzando gli errori.

### Il problema attuale
Oggi, quando un ufficio pubblico deve creare un atto amministrativo (es. una delibera comunale):

1. ⏰ **Tempo richiesto**: 2-4 ore di lavoro manuale
2. 📄 **Rischio errori**: Dimentica un riferimento normativo, sbaglia una data, omette un'autorizzazione
3. 🔍 **Verifica manuale**: Serve tempo per controllare conformità alle leggi
4. 📚 **Conoscenza necessaria**: L'operatore deve conoscere tutte le norme applicabili
5. 🔄 **Ripetitività**: Molti documenti sono simili tra loro ma vengono sempre riscritti da zero

### La nostra soluzione
Un **assistente digitale intelligente** che:

✅ Scrive automaticamente il documento seguendo le regole e i modelli corretti
✅ **Identifica automaticamente il procedimento amministrativo** dalla richiesta utente
✅ Inserisce i riferimenti normativi necessari in base al tipo di atto
✅ Controlla che tutto sia corretto prima di proporlo all'operatore
✅ Riduce i tempi da ore a **circa 23 secondi** (parte automatica) + 15 secondi (revisione umana)
✅ Garantisce tracciabilità e conformità alle normative (GDPR incluso)

---

## ❌ 2. Perché non funziona la modalità "One-Shot"?

### Cosa significa "One-Shot"?
Chiedere all'intelligenza artificiale (come ChatGPT) di scrivere tutto il documento in un'unica volta, senza passaggi intermedi.

### Esempio pratico - Approccio One-Shot
```
❌ RICHIESTA: "Scrivi una delibera per l'approvazione di un piano urbanistico"

PROBLEMI:
1. L'AI non sa quale modello specifico usare (ce ne sono decine)
2. Non conosce le normative locali applicabili
3. Non può verificare se i dati inseriti sono corretti
4. Non garantisce la qualità del linguaggio amministrativo
5. Non traccia il processo decisionale (obbligatorio per legge)
```

### Perché questo non funziona?

#### 🚨 Problema 1: Complessità delle regole
Un atto amministrativo deve rispettare:
- Leggi nazionali (es. Legge 241/1990)
- Leggi regionali specifiche
- Regolamenti comunali
- Giurisprudenza (sentenze dei tribunali)
- Prassi consolidate

**Analogia**: È come chiedere a qualcuno di cucinare un piatto gourmet senza dargli la ricetta, gli ingredienti o le attrezzature giuste.

#### 🚨 Problema 2: Assenza di controlli
Con One-Shot non si può:
- Verificare che i dati inseriti siano completi (es. manca il CIG?)
- Controllare che le norme citate siano ancora in vigore
- Assicurarsi che il linguaggio sia formalmente corretto
- Garantire che tutto sia logicamente coerente

**Analogia**: È come costruire una casa senza un architetto che controlli che le fondamenta siano solide.

#### 🚨 Problema 3: Mancanza di tracciabilità
La legge richiede di sapere:
- Chi ha fatto cosa
- Quando è stato fatto
- Su quale base (quale norma, quale precedente)
- Perché l'AI ha preso certe decisioni

**One-Shot = scatola nera**: Non si può dimostrare come si è arrivati al risultato.

#### 🚨 Problema 4: Impossibile migliorare
Se l'output è sbagliato:
- Non si sa quale passaggio ha generato l'errore
- Si deve ricominciare da zero
- Non si possono correggere solo le parti errate

---

<div style="page-break-after: always;"></div>

### ✅ La nostra soluzione: Approccio "Multi-Step"

Dividiamo il lavoro in **10 fasi specializzate**, ognuna con un compito preciso:

```
📥 INPUT: "Richiesta autorizzazione scarico acque reflue industriali"

PASSO 1 - Classificazione Procedimento: "È un PROCEDIMENTO DI AUTORIZZAZIONE SCARICO ACQUE"
          → Tipo provvedimento: DETERMINAZIONE DIRIGENZIALE
          → Normativa base: D.Lgs 152/2006, L.R. 62/1998
          → Termini: 90 giorni
          → Enti coinvolti: ARPA, ASL

PASSO 2 - Classificatore Documento: "È una DETERMINAZIONE, categoria AMBIENTE"

PASSO 3 - Recupero normativa specifica: "Serve D.Lgs 152/2006 art. 124, L.R. 62/1998"

PASSO 4 - Generatore: Scrive il documento seguendo il modello corretto

PASSO 5 - Validatore: "✅ OK: Tutti i metadata richiesti presenti, normativa corretta"

PASSO 6 - Controllo qualità: "Linguaggio corretto, leggibilità buona (82/100)"

PASSO 7 - Revisione umana: L'operatore approva

PASSO 8 - Pubblicazione: Protocollo + firma digitale automatici

PASSO 9 - Audit: Tutto viene registrato per trasparenza

📤 OUTPUT: Determinazione completa, conforme, protocollata in 38 secondi totali
```

**Risultato**: Ogni fase è controllabile, migliorabile e tracciabile. Se c'è un errore, si sa esattamente dove intervenire.

**Novità 2.0:** Il sistema ora identifica automaticamente il procedimento amministrativo dalla richiesta iniziale, selezionando il tipo di provvedimento corretto e la normativa applicabile!

---

## 🧩 3. I Componenti del Sistema (11 Sottoprogetti)

Immaginiamo il sistema come una **catena di montaggio intelligente** dove ogni stazione ha un compito specifico.

---

<div style="page-break-after: always;"></div>

### **SP01 - EML Parser & Email Intelligence** 📧

**Cosa fa (in parole semplici)**
È il primo componente che **intercetta le email in arrivo** alla PEC (Posta Elettronica Certificata) dell'ente e le analizza per capire se contengono richieste di servizi o istanze dei cittadini.

**Come funziona**
1. Monitora la casella PEC dell'ente in tempo reale
2. Estrae mittente, oggetto, corpo email e allegati
3. Analizza il contenuto con AI per capire se è una richiesta amministrativa
4. Classifica il tipo di richiesta (autorizzazione, concessione, comunicazione, ecc.)
5. Estrae informazioni chiave dal testo dell'email
6. Passa tutto al sistema per l'elaborazione automatica

**Input**
- Email in arrivo alla PEC (formato .eml)
- Allegati (PDF, DOC, immagini)

**Output**
- Metadata email: mittente, data/ora, oggetto
- Testo estratto e pulito
- Allegati separati e classificati per tipo
- Primo livello di classificazione: "È una richiesta amministrativa? Di che tipo?"
- Confidenza: quanto è sicuro che sia effettivamente una richiesta da processare
- Tempo impiegato: circa 300 millisecondi

**Tecnologie utilizzate**
- **IMAPClient / email parser**: Librerie Python per leggere email
- **PyPDF2 / python-docx**: Estrazione testo da allegati
- **DistilBERT**: AI per classificazione rapida del contenuto email
- **Redis**: Cache per non riprocessare email già analizzate

**Esempio pratico**
```
EMAIL IN ARRIVO:
Da: azienda.rossi@pec.it
Oggetto: Richiesta autorizzazione scarico acque reflue
Testo: "Spett.le Comune, con la presente si richiede..."
Allegati: [Planimetria.pdf, Relazione_tecnica.pdf]

OUTPUT SP01:
✅ RICONOSCIUTA: Richiesta amministrativa
✅ TIPO: Istanza autorizzazione ambientale
✅ MITTENTE: Azienda Rossi S.p.A. (P.IVA estratta)
✅ ALLEGATI: 2 documenti tecnici
✅ PRIORITÀ: Normale
✅ CONFIDENCE: 89%
→ Passa a SP02 per estrazione allegati
```

**Perché è importante?**
Automatizza il primo contatto con il cittadino, evitando che un operatore debba aprire manualmente centinaia di email al giorno per capire quali richiedono azioni amministrative.

---

### **SP02 - Document Extractor & Attachment Classifier** 📎

**Cosa fa (in parole semplici)**
Prende gli allegati ricevuti via email (da SP01) e li analizza per capire cosa contengono e estrarre informazioni utili.

**Come funziona**
1. Riceve i file allegati identificati da SP01
2. Estrae il testo da PDF, immagini scansionate (OCR), documenti Word
3. Classifica ogni allegato (es. "planimetria", "relazione tecnica", "documento identità")
4. Estrae dati strutturati (date, importi, codici, riferimenti normativi)
5. Valida la completezza: "mancano documenti obbligatori?"
6. Prepara i dati per il classificatore di procedimenti (SP03)

**Input**
- Allegati email (PDF, DOC, JPG, PNG)
- Metadata da SP01

**Output**
- Testo estratto da tutti gli allegati
- Classificazione di ogni documento
- Dati estratti: nomi, date, importi, codici CIG/CUP, P.IVA, ecc.
- Checklist completezza documentale
- Tempo impiegato: circa 800 millisecondi per documento

**Tecnologie utilizzate**
- **Tesseract OCR**: Estrazione testo da immagini/PDF scansionati
- **PyPDF2 / pdfplumber**: Estrazione testo da PDF nativi
- **LayoutLM / Donut**: AI specializzati nell'analisi layout documenti
- **spaCy**: Riconoscimento entità (NER) per estrarre dati
- **MinIO**: Storage per conservare allegati originali

**Esempio pratico**
```
INPUT: Planimetria.pdf + Relazione_tecnica.pdf

OUTPUT SP02:
📄 Documento 1: Planimetria.pdf
   Tipo: PLANIMETRIA_TECNICA
   Dati estratti:
   - Scala: 1:500
   - Comune: Torino
   - Foglio catastale: 12, Mappale: 345

📄 Documento 2: Relazione_tecnica.pdf
   Tipo: RELAZIONE_TECNICA_AMBIENTALE
   Dati estratti:
   - Progettista: Ing. Mario Rossi
   - Volume scarico: 500 m³/giorno
   - Tipo attività: Tessile industriale

✅ COMPLETEZZA: 80%
⚠️  MANCANTI:
   - Documento identità legale rappresentante
   - Visura camerale aggiornata
```

**Perché è importante?**
Evita che l'operatore debba leggere manualmente decine di pagine di allegati per capire cosa contengono ed estrarre le informazioni chiave.

---

### **SP03 - Classificatore di Procedimenti Amministrativi** 🎯

**Cosa fa (in parole semplici)**
È il componente che **legge la richiesta iniziale del cittadino o dell'azienda** (chiamata "istanza") e capisce:
- Quale **procedimento amministrativo** si deve avviare
- Quale **tipo di provvedimento** bisogna generare
- Quale **normativa** si applica
- Quali **documenti** servono
- Quali **uffici/enti** devono essere coinvolti

**Come funziona**
1. Riceve l'istanza dell'utente (es. "Richiesta autorizzazione scarico acque reflue industriali")
2. Analizza il testo con AI per capire di cosa si tratta
3. Cerca nel database dei procedimenti amministrativi quello più simile
4. Determina automaticamente il tipo di provvedimento da generare (Determinazione? Delibera? Ordinanza?)
5. Recupera tutte le informazioni necessarie per quel procedimento specifico

**Input**
- Testo richiesta: "Richiesta autorizzazione scarico acque reflue industriali per azienda tessile"
- Dati richiedente: Industria Tessile Rossi S.p.A.
- Allegati presentati: planimetria, relazione tecnica

**Output**
- **Procedimento identificato**: AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE
- **Tipo provvedimento**: DETERMINAZIONE_DIRIGENZIALE
- **Autorità competente**: Dirigente Settore Ambiente
- **Normativa di base**:
  - D.Lgs 152/2006 art. 124 (Disciplina degli scarichi)
  - L.R. 62/1998 art. 8 (Norme regionali tutela acque)
- **Termini**: 90 giorni
- **Enti da coinvolgere**: ARPA (parere obbligatorio), ASL (parere facoltativo)
- **Documenti richiesti**: localizzazione scarico, caratteristiche scarico, relazione tecnica, planimetria
- **Fasi procedurali**: Verifica completezza → Istruttoria tecnica → Pareri enti → Conferenza servizi → Determinazione finale
- **Confidenza**: 96% (quanto è sicuro l'AI)
- Tempo impiegato: circa 520 millisecondi

**Tecnologie utilizzate**
- **DistilBERT**: AI per classificazione veloce del procedimento
- **spaCy**: Software per riconoscere nomi, enti, riferimenti normativi
- **PostgreSQL**: Database con tutti i procedimenti amministrativi
- **Redis**: Memoria per non rifare classificazioni già fatte

**Esempio pratico**
```
RICHIESTA CITTADINO:
"Richiesta autorizzazione scarico acque reflue industriali
provenienti dal ciclo produttivo tessile, 500 m³/giorno"

OUTPUT SP03:
✅ PROCEDIMENTO IDENTIFICATO: Autorizzazione Scarico Acque Reflue
✅ PROVVEDIMENTO DA GENERARE: Determinazione Dirigenziale
✅ COMPETENZA: Dirigente Settore Ambiente
✅ NORMATIVA APPLICABILE:
   - D.Lgs 152/2006 art. 124
   - L.R. 62/1998 art. 8
✅ TERMINI PROCEDIMENTO: 90 giorni (no silenzio-assenso)
✅ ENTI DA COINVOLGERE:
   - ARPA: parere obbligatorio (30 giorni)
   - ASL: parere facoltativo (15 giorni)
✅ DOCUMENTI OBBLIGATORI:
   - Dati identificativi richiedente ✓ (presente)
   - Localizzazione scarico ✗ (mancante)
   - Caratteristiche scarico ✓ (presente)
   - Relazione tecnica ✓ (presente)
   - Planimetria ✓ (presente)
```

**Perché è importante?**
Prima di questo componente, l'operatore doveva:
1. Leggere la richiesta
2. Capire manualmente quale procedimento applicare
3. Cercare la normativa corretta
4. Verificare quali documenti servono
5. Controllare quali uffici coinvolgere

Ora tutto questo è **automatico** e richiede mezzo secondo invece di 10-15 minuti!

**🔍 CHECKPOINT HITL #1 - Conferma Classificazione Procedimento**
⚠️ **INTERVENTO UMANO OBBLIGATORIO**

Dopo che SP03 ha classificato il procedimento, il sistema **si ferma e chiede conferma all'operatore**:

```
┌─────────────────────────────────────────────────┐
│ 🤖 PROPOSTA AI (SP03)                          │
├─────────────────────────────────────────────────┤
│ Procedimento identificato:                      │
│ ➜ AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE          │
│                                                 │
│ Confidence: 96%                                 │
│ Tipo provvedimento: DETERMINAZIONE_DIRIGENZIALE │
│                                                 │
│ Normativa di riferimento:                       │
│  • D.Lgs. 152/2006 art. 124                     │
│  • L.R. 62/1998 art. 8                          │
│                                                 │
│ Enti da coinvolgere:                            │
│  • ARPA (parere obbligatorio)                   │
│  • ASL (parere facoltativo)                     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 👤 AZIONE RICHIESTA ALL'OPERATORE              │
├─────────────────────────────────────────────────┤
│ [ ] CONFERMA la classificazione                 │
│ [ ] MODIFICA il tipo di procedimento            │
│ [ ] AGGIUNGI procedimenti correlati             │
│ [ ] ANNULLA l'operazione                        │
│                                                 │
│ Motivazione (obbligatoria): _______________     │
└─────────────────────────────────────────────────┘
```

**Responsabilità legale**: La classificazione del procedimento è un atto amministrativo che richiede **responsabilità umana diretta** (Legge 241/90, art. 6). L'AI propone, ma l'operatore decide e traccia la scelta.

**Tracciabilità**: Ogni decisione viene registrata con:
- Chi ha deciso (utente autenticato)
- Cosa ha deciso (conferma/modifica)
- Quando ha deciso (timestamp)
- Perché ha deciso (motivazione obbligatoria)
- Eventuali modifiche apportate alla proposta AI

---

### **SP04 - Archivio Normativo Intelligente** 📚

**Cosa fa (in parole semplici)**
È la "biblioteca giuridica digitale" che sa quali leggi applicare e fornisce i testi corretti.

**Come funziona**
1. Quando serve sapere quale normativa applicare a un atto, questo componente cerca
2. Ha un database con 100.000+ documenti tra leggi, decreti, regolamenti, sentenze
3. Usa l'AI per capire quali sono rilevanti (ricerca semantica, non solo per parole chiave)
4. Crea una sintesi comprensibile dei riferimenti normativi
5. Tiene traccia di quali leggi modificano/abrogano altre leggi (grafo delle relazioni)

**Input**
- Tipo di documento
- Argomento (es. "urbanistica", "appalti")
- Eventualmente normativa già menzionata

**Output**
- Elenco normative rilevanti con grado di importanza
- Sintesi testuale: "Per l'approvazione del Piano Urbanistico è necessario rispettare..."
- Riferimenti a delibere simili già approvate
- Eventuali sentenze rilevanti
- Tempo impiegato: circa 1.2 secondi

**Tecnologie utilizzate**
- **FAISS**: Sistema di ricerca super-veloce tra milioni di documenti
- **Neo4j**: Database a grafo per tracciare relazioni tra leggi (es. "Legge A modifica Legge B")
- **Mistral-7B / Groq**: AI specializzata per creare sintesi leggibili
- **Redis**: Memoria veloce per non cercare sempre le stesse cose

**Esempio pratico**
```
RICHIESTA: "Normativa per delibera approvazione piano urbanistico"

OUTPUT:
📋 NORMATIVA PRINCIPALE:
- L. 241/1990 Art. 5 (Responsabile procedimento) - Rilevanza: 95%
- D.Lgs 42/2004 Art. 146 (Autorizzazione paesaggistica) - Rilevanza: 89%
- L.R. 12/2005 (Urbanistica regionale) - Rilevanza: 87%

📖 SINTESI:
"Per l'approvazione del Piano Urbanistico è necessario rispettare i vincoli
paesaggistici del D.Lgs 42/2004 e seguire la procedura con responsabile del
procedimento prevista dalla L. 241/1990..."

🔗 PRECEDENTI SIMILI:
- Delibera n. 123/2024 "Piano Zona Artigianale" (Similarità: 84%, Esito: APPROVATA)
```

**Aggiornamento dati**
- Automatico ogni trimestre dalla Gazzetta Ufficiale
- Alert per modifiche normative urgenti

---

<div style="page-break-after: always;"></div>

### **SP05 - Motore di Generazione Template** 🤖

**Come funziona**
1. Riceve il tipo di atto da creare (es. "Delibera di Giunta")
2. Prende i dati forniti (oggetto, importo, responsabile)
3. Recupera il modello corretto da un archivio
4. Inserisce i riferimenti normativi necessari
5. Genera il testo completo in linguaggio amministrativo formale

**Input**
- Tipo documento: "DELIBERA_GIUNTA"
- Dati: oggetto, proponente, importo, normativa
- Contesto normativo (fornito dal componente SP04)

**Output**
- Documento completo in formato strutturato (XML/HTML)
- 12 sezioni compilate (premesse, motivazioni, dispositivo, ecc.)
- Tempo impiegato: circa 2.3 secondi

**Tecnologie utilizzate**
- **GPT-4 / Claude**: AI per generazione testo (come ChatGPT ma specializzato)
- **LangChain**: Software che coordina l'AI in più passi
- **Jinja2**: Sistema di modelli per documenti (come i modelli Word, ma più avanzati)
- **Redis**: Memoria veloce per ricordare i modelli già usati

**Esempio pratico**
```
INPUT: "Delibera per approvazione piano urbanistico zona industriale, 150.000€"

OUTPUT:
"DELIBERA DELLA GIUNTA COMUNALE N. ___/2025
OGGETTO: Approvazione Piano Urbanistico Zona Industriale...

PREMESSO CHE:
- Il Comune intende procedere alla realizzazione...
- La normativa di riferimento è costituita da L. 241/1990...

VISTA la L.R. 12/2005...
VISTO il D.Lgs 42/2004...

DELIBERA
1. Di approvare il Piano Urbanistico..."
```

**🔍 CHECKPOINT HITL #3 - Revisione Documento Generato**
⚠️ **INTERVENTO UMANO OBBLIGATORIO**

Dopo che SP05 ha generato il documento, l'operatore **deve revisionarlo prima della validazione**:

```
┌─────────────────────────────────────────────────┐
│ 📄 DOCUMENTO GENERATO (SP05)                   │
├─────────────────────────────────────────────────┤
│ Tipo: DELIBERA_GIUNTA                           │
│ Lunghezza: 4.235 parole                         │
│ Sezioni generate: 12/12 ✓                      │
│                                                 │
│ Riferimenti normativi inseriti:                 │
│  • L. 241/1990 art. 5                           │
│  • L.R. 12/2005                                 │
│  • D.Lgs 42/2004 art. 146                       │
│                                                 │
│ Template utilizzato: DELIBERA_GIUNTA_v3.2       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 👤 REVISIONE RICHIESTA                         │
├─────────────────────────────────────────────────┤
│ [ ] APPROVA senza modifiche                     │
│ [ ] MODIFICA sezioni specifiche                 │
│ [ ] RIGENERA con istruzioni aggiuntive          │
│                                                 │
│ Editor con track changes disponibile ↓          │
│ [Apri editor per modifiche manuali]             │
│                                                 │
│ Sezioni da rivedere manualmente:                │
│ ☐ Premessa (motivazioni specifiche)            │
│ ☐ Dispositivo (condizioni particolari)         │
│ ☐ Visti (aggiungere delibere precedenti)       │
│                                                 │
│ Note di revisione: _______________              │
└─────────────────────────────────────────────────┘
```

**Responsabilità legale**: L'atto amministrativo è un documento ufficiale che impegna la PA. L'operatore deve verificare:
- Correttezza tecnico-giuridica
- Completezza delle motivazioni (Legge 241/90, art. 3)
- Assenza di errori materiali o refusi
- Adeguatezza del dispositivo al caso specifico

**Track Changes**: Tutte le modifiche manuali vengono evidenziate e tracciate nel sistema di versioning.

---

### **SP06 - Validatore di Conformità** ✅

**Cosa fa (in parole semplici)**
È il "revisore automatico" che controlla che il documento sia corretto e rispetti tutte le regole.

**Come funziona**
1. Legge il documento generato da SP05
2. Controlla la coerenza interna (non ci sono contraddizioni?)
3. Verifica che tutti i dati obbligatori siano presenti
4. Consulta la banca dati normativa (SP04) per controllare che le leggi citate siano giuste
5. Applica regole automatiche (es. "se importo > 40.000€, serve il CIG")
6. Segnala errori critici (bloccano il processo) o semplici avvisi

**Input**
- Documento generato da SP05
- Tipo di atto

**Output**
- Stato: OK / WARNING / ERRORE
- Lista errori critici (se presenti): "Manca responsabile procedimento"
- Lista avvisi: "Consigliato aggiungere riferimento a delibera precedente"
- Suggerimenti automatici per correggere
- Tempo impiegato: circa 780 millisecondi (meno di 1 secondo)

**Tecnologie utilizzate**
- **BERT**: AI specializzata nell'analisi del linguaggio
- **Drools**: Software che applica regole automatiche (es. "SE importo > X ALLORA serve Y")
- **PostgreSQL**: Database che conserva i risultati per audit

**Esempio pratico**
```
DOCUMENTO IN INPUT: Delibera con importo 150.000€ ma senza CIG

OUTPUT DEL VALIDATORE:
❌ ERRORE CRITICO: Manca responsabile procedimento (L. 241/1990 Art. 5)
⚠️  WARNING: CIG obbligatorio per importi > 40.000€
✅ OK: Tutti i riferimenti normativi sono vigenti
✅ OK: Coerenza semantica: 92%

SUGGERIMENTO: Inserire CIG da portale ANAC
```

---

### **SP07 - Classificatore e Estrattore Dati** 🏷️

**Cosa fa (in parole semplici)**
È il componente che "legge" i dati iniziali e capisce che tipo di documento serve e quali informazioni sono importanti.

**Come funziona**
1. Riceve i dati grezzi (testo libero + alcuni campi compilati)
2. Identifica il tipo di atto (Delibera? Determinazione? Ordinanza?)
3. Estrae automaticamente le informazioni chiave: date, importi, persone, normative menzionate
4. Categorizza l'argomento (Urbanistica? Bilancio? Personale?)
5. Cerca documenti simili già fatti in passato

**Input**
- Testo descrittivo: "Richiesta approvazione piano per zona industriale con vincoli paesaggistici..."
- Eventuali metadati già noti: proponente, importo, scadenza

**Output**
- Tipo documento: "DELIBERA_GIUNTA"
- Categoria: "URBANISTICA" > "PIANI_REGOLATORI"
- Confidenza: 94% (quanto è sicuro l'AI)
- Dati estratti automaticamente:
  - Date: 31/12/2025
  - Importi: 150.000€
  - Persone: Mario Rossi (Responsabile)
  - Normative: L.R. 12/2005, D.Lgs 42/2004
  - Codici: CIG Z1234567890
- Documenti simili già approvati in passato
- Tempo impiegato: circa 450 millisecondi

**Tecnologie utilizzate**
- **DistilBERT**: AI per classificazione veloce dei documenti
- **spaCy**: Software per riconoscere nomi, date, importi, leggi nel testo
- **FAISS**: Ricerca veloce tra documenti simili
- **Redis**: Memoria per risultati recenti

**Esempio pratico**
```
INPUT (testo libero):
"Assessorato Urbanistica richiede approvazione piano zona industriale.
Responsabile: ing. Mario Rossi. Budget: €150.000.
Normativa: L.R. 12/2005 e D.Lgs 42/2004. Scadenza: 31/12/2025"

OUTPUT AUTOMATICO:
📋 CLASSIFICAZIONE:
- Tipo: DELIBERA_GIUNTA (Confidenza: 94%)
- Categoria: URBANISTICA > PIANI_REGOLATORI

📊 DATI ESTRATTI:
- Date: [31/12/2025]
- Importi: [150.000,00 €]
- Persone: [Mario Rossi - Responsabile Procedimento]
- Enti: [Assessorato Urbanistica]
- Normativa: [L.R. 12/2005, D.Lgs 42/2004]
- CIG: Z1234567890

🔍 DOCUMENTI SIMILI:
- DOC-98765: Delibera Piano Zona Artigianale (Similarità: 87%)
```

**🔍 CHECKPOINT HITL #2 - Conferma Dati Estratti**
⚠️ **INTERVENTO UMANO OBBLIGATORIO**

Dopo che SP07 ha classificato ed estratto i dati, il sistema **richiede verifica umana**:

```
┌─────────────────────────────────────────────────┐
│ 🤖 DATI ESTRATTI (SP07)                        │
├─────────────────────────────────────────────────┤
│ Tipo atto: DELIBERA_GIUNTA (94%)                │
│                                                 │
│ Dati estratti:                                  │
│  ✓ Responsabile: ing. Mario Rossi              │
│  ✓ Importo: €150.000,00                        │
│  ✓ Scadenza: 31/12/2025                        │
│  ✓ Normativa: L.R. 12/2005, D.Lgs 42/2004      │
│  ✓ CIG: Z1234567890                            │
│  ⚠ Ufficio proponente: NON SPECIFICATO         │
│  ⚠ Numero delibera precedente: NON TROVATO     │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ � VERIFICA RICHIESTA                          │
├─────────────────────────────────────────────────┤
│ [ ] CONFERMA tutti i dati                       │
│ [ ] CORREGGI dati errati/incompleti             │
│ [ ] AGGIUNGI dati mancanti                      │
│                                                 │
│ Campi da integrare manualmente:                 │
│ • Ufficio proponente: _______________           │
│ • Numero delibera precedente: _________         │
│                                                 │
│ Correzioni a dati esistenti:                    │
│ • _________________________________             │
│                                                 │
│ Note operatore: _______________                 │
└─────────────────────────────────────────────────┘
```

**Responsabilità legale**: L'estrazione automatica può contenere errori di interpretazione. L'operatore **deve verificare** che tutti i dati siano corretti e completi prima di procedere (Legge 241/90, art. 2 - principio di accuratezza amministrativa).

**Tracciabilità**: Ogni correzione viene registrata con versioning dei dati.

---

### **SP08 - Controllo Qualità Linguistica** 📝

**Cosa fa (in parole semplici)**
È il "revisore automatico" che controlla che il documento sia scritto bene in italiano, senza errori grammaticali e con il linguaggio formale corretto.

**Come funziona**
1. Riceve il documento da controllare
2. Verifica grammatica e ortografia
3. Controlla punteggiatura e sintassi
4. Valuta la leggibilità (il testo è troppo complicato?)
5. Controlla che usi la terminologia amministrativa corretta
6. Assegna un punteggio di qualità complessivo

**Input**
- Documento generato (da SP05 o dopo correzioni)

**Output**
- Punteggio qualità: 82/100 (BUONO)
- Errori grammaticali trovati e suggerimenti
- Indice di leggibilità (scala Gulpease per italiano)
- Suggerimenti stilistici (es. "frase troppo lunga, dividere")
- Terminologia: segnala se usa termini colloquiali invece di tecnici
- Tempo impiegato: circa 320 millisecondi

**Tecnologie utilizzate**
- **LanguageTool**: Software professionale per correzione grammaticale italiana
- **spaCy**: Analisi linguistica avanzata
- **Gulpease**: Formula per calcolare leggibilità testi italiani
- **Redis**: Memoria per regole grammaticali

**Esempio pratico**
```
DOCUMENTO IN INPUT:
"Il Comune approva il piano urbanistico zona industriale con la
delibera dove sono previsti vincoli paesaggistici che bisogna rispettare
secondo normativa vigente..."

OUTPUT CONTROLLO QUALITÀ:
� PUNTEGGIO: 82/100 (BUONO)

✅ GRAMMATICA: OK
⚠️  STILE:
  - Riga 2: Frase troppo lunga (45 parole), consigliato dividere
  - Preferire forma impersonale: "sono previsti" → "si prevede"

� LEGGIBILITÀ: 68/100 (Gulpease) - Livello medio-alto

💡 SUGGERIMENTI:
- Sostituire "che bisogna rispettare" con "da osservare" (più formale)
- Specificare "normativa vigente" con riferimento preciso (D.Lgs...)
```

---

### **SP09 - Motore di Orchestrazione** ⚙️

**Cosa fa (in parole semplici)**
È il "direttore d'orchestra" che coordina tutti gli altri componenti e gestisce il flusso di lavoro completo.

**Come funziona**
1. Riceve la richiesta iniziale di creare un atto
2. Decide in che ordine chiamare gli altri componenti
3. Passa i dati da uno all'altro
4. Gestisce i casi problematici (es. se SP02 trova errori, fa correggere e riprova)
5. Si integra con i sistemi esterni (protocollo, firma digitale, archivio)
6. Traccia tutto il processo per audit

**Input**
- Richiesta creazione atto dall'utente
- Dati iniziali

**Output**
- Documento finale completo e protocollato
- Stato del processo ad ogni passo
- Log completo di tutto il flusso

**Tecnologie utilizzate**
- **Apache Airflow / Temporal.io**: Software per gestire workflow complessi
- **Apache NiFi**: Sistema di orchestrazione workflow con data lineage completo tramite Provenance
- **Docker/Kubernetes**: Contenitori per eseguire i vari servizi
- **PostgreSQL**: Database per stato del workflow

**Flusso tipico orchestrato**
```
1. Riceve richiesta utente (istanza)
2. Chiama SP11 → Autentica utente
3. Chiama SP01 → Riceve e parsifica email PEC
4. Chiama SP02 → Estrae allegati e documenti
5. ⭐ Chiama SP03 → Classifica PROCEDIMENTO (es. Autorizzazione Scarichi)
                  → Determina PROVVEDIMENTO (es. Determinazione Dirigenziale)
                  → Recupera normativa di base
6. Chiama SP07 → Classifica documento ed estrae dati
7. Chiama SP04 → Recupera normativa specifica aggiuntiva
8. Chiama SP05 → Genera documento (usa info da SP03 per template corretto)
9. Chiama SP06 → Valida documento (usa regole da SP03 per procedimento)
   └─ Se ERRORE: torna a step 8 dopo correzione
10. Chiama SP08 → Controlla qualità
   └─ Se insufficiente: chiama SP05 per raffinare
11. Invia a revisione umana
12. Chiamata sistema protocollo esterno
13. Chiamata sistema firma digitale
14. Chiama SP11 → Salva audit trail
15. Notifica completamento
```

**Tempo totale medio**: ~23 secondi parte automatica + ~15 secondi revisione umana

**Novità con SP01-SP03**: Il sistema ora riceve automaticamente richieste via PEC, estrae allegati e identifica il procedimento corretto, riducendo errori del 40%!

---

### **SP10 - Dashboard di Trasparenza** 📊

**Cosa fa (in parole semplici)**
È l'interfaccia visuale che mostra all'operatore come l'AI ha lavorato e permette di monitorare tutto il processo in tempo reale.

**Come funziona**
1. Riceve dati da tutti i componenti durante il processo
2. Mostra in tempo reale a che punto è il lavoro
3. Visualizza le decisioni prese dall'AI in modo comprensibile
4. Permette di esplorare perché l'AI ha fatto certe scelte
5. Mostra statistiche e metriche di qualità
6. Traccia la storia di ogni documento

**Input**
- Dati da tutti i componenti SP01-SP09
- Eventi del workflow
- Log delle operazioni

**Output (visualizzazioni)**
- **Timeline**: Mostra i passaggi del processo step-by-step
- **Metriche**: Tempo impiegato, confidenza AI, punteggi qualità
- **Spiegazioni**: "L'AI ha scelto questo modello perché il documento è simile a..."
- **Evidenziazioni**: Parti del testo generate dall'AI con grado di confidenza
- **Audit trail**: Chi ha fatto cosa e quando
- **Statistiche**: Quanti documenti al giorno, tasso di successo, errori comuni
- **Storico versioni**: Tutte le versioni del documento con track changes

**Tecnologie utilizzate**
- **Streamlit / React**: Framework per interfacce web moderne
- **D3.js**: Libreria per grafici e visualizzazioni interattive
- **SHAP / LIME**: Strumenti per spiegare decisioni AI
- **PostgreSQL**: Database per dati storici e analytics
- **WebSocket**: Comunicazione real-time con i componenti

**Esempio di visualizzazione**
```
┌─────────────────────────────────────────────────────────┐
│ WORKFLOW: Autorizzazione Scarico Acque - ID: WF-12345  │
│ Stato: ✅ COMPLETATO in 38 secondi                     │
├─────────────────────────────────────────────────────────┤
│ TIMELINE:                                               │
│ ✅ Email ricevuta        (300ms) Email PEC acquisita ⭐ │
│ ✅ Allegati estratti     (800ms) 2 documenti trovati ⭐ │
│ ✅ Classif. procedimento (520ms) Confidenza: 96% ⭐NEW │
│    → Procedimento: AUTORIZ_SCARICO_ACQUE                │
│    → Provvedimento: DETERMINAZIONE_DIRIGENZIALE         │
│ ✅ Classificazione doc   (450ms) Confidenza: 94%       │
│ ✅ Recupero normativa    (1.2s)  5 riferimenti trovati │
│ ✅ Generazione           (2.3s)  12 sezioni completate │
│ ✅ Validazione           (780ms) OK - nessun errore    │
│ ✅ Quality check         (320ms) Score: 82/100         │
│ ✅ Revisione umana       (15s)   Approvato             │
│ ✅ Protocollo            (3.5s)  N. 12345/2025         │
├─────────────────────────────────────────────────── ─────┤
│ DECISIONI AI:                                           │
│ 🎯 Procedimento: AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE   │
│    Motivo: Parole chiave "scarico acque reflue"         │
│    Similarità 91% con procedimento PROC-2024-00567      │
│                                                         │
│ 🤖 Modello usato: "DET-AMB-SCARICHI-v2.1"              │
│    Motivo: Template specifico per procedimento          │
│                                                         │
│ 🤖 Normativa principale: D.Lgs 152/2006, L.R. 62/1998  │
│    Motivo: Normativa base per procedimento + rilevanza  │
└─────────────────────────────────────────────────────────┘
```

**Perché è importante?**
Offre trasparenza totale sul processo automatico, permettendo agli operatori di:
- Capire come l'AI ha preso decisioni
- Controllare la qualità del lavoro svolto
- Tracciare la storia completa per audit
- Identificare problemi ricorrenti per migliorare

---

### **SP11 - Sicurezza e Audit** �

**Cosa fa (in parole semplici)**
Garantisce che tutto sia sicuro, tracciabile e conforme alle leggi sulla privacy (GDPR).

**Come funziona**
1. Autentica gli utenti (chi può fare cosa)
2. Registra ogni azione in modo immutabile (audit trail)
3. Rileva comportamenti anomali (es. troppi accessi, tentativi sospetti)
4. Protegge i dati sensibili (crittografia)
5. Genera report per gli audit di conformità
6. Gestisce i diritti degli interessati (GDPR: diritto all'oblio, spiegazione decisioni AI)

**Input**
- Eventi da tutti i componenti
- Log di accesso e operazioni
- Metriche di sistema

**Output**
- Report di sicurezza in tempo reale
- Alert su anomalie (es. "utente X ha tentato 5 accessi non autorizzati")
- Audit trail completo (chi, cosa, quando, perché)
- Certificazioni di conformità GDPR
- Report per il DPO (Data Protection Officer)

**Tecnologie utilizzate**
- **Isolation Forest + LSTM**: AI per rilevare comportamenti anomali
- **HashiCorp Vault**: Sistema per gestire password e chiavi segrete in sicurezza
- **ELK Stack**: Raccolta e analisi log centralizzata
- **JWT**: Sistema di autenticazione sicura
- **OpenSSL/TLS**: Crittografia dei dati in transito

**Funzioni di sicurezza**
```
🔐 AUTENTICAZIONE:
- Login con credenziali PA + autenticazione a due fattori
- Token temporanei (scadono dopo inattività)

🛡️ AUTORIZZAZIONE:
- Ruoli: Admin, Operatore, Revisore, Auditor
- Permessi granulari (es. "può creare delibere ma non ordinanze")

📋 AUDIT TRAIL (immutabile):
- 2025-10-08 10:15:23 | Mario.Rossi  | CREATE_WORKFLOW | WF-12345
- 2025-10-08 10:15:24 | AI-SP04      | CLASSIFY        | DELIBERA_GIUNTA
- 2025-10-08 10:15:28 | AI-SP01      | GENERATE        | Success
- ...

🚨 ANOMALY DETECTION:
- ALERT: Utente "test.user" ha fatto 50 richieste in 1 minuto (soglia: 20)
- ALERT: Accesso da IP insolito per utente "admin.pa"

🔒 GDPR COMPLIANCE:
- Pseudonimizzazione dati personali nei log
- Retention policy: 5 anni documenti, 2 anni log operativi
- Right to explanation: Ogni decisione AI è spiegabile tramite SP07
```

**Perché è importante?**
La gestione della sicurezza e della tracciabilità è **fondamentale per legge** (GDPR, CAD, LGPL). Garantisce che:
- Solo utenti autorizzati accedono al sistema
- Ogni azione è registrata e giustificabile
- I dati personali sono protetti
- Il sistema è auditabile da enti controllori
- Le decisioni AI sono spiegate e controllabili

---

<div style="page-break-after: always;"></div>

## 📖 Glossario

### Termini Amministrativi

**Atto Amministrativo**
Documento ufficiale emesso dalla Pubblica Amministrazione che produce effetti giuridici (es. autorizzazioni, divieti, approvazioni). Deve rispettare forma e procedure previste dalla legge.

**Albo Pretorio**
Spazio pubblico (fisico o digitale) dove vengono pubblicati gli atti ufficiali dell'ente per garantire trasparenza e conoscibilità ai cittadini. La pubblicazione ha valore legale.

**ANAC (Autorità Nazionale Anticorruzione)**
Ente pubblico che vigila su appalti, contratti pubblici e prevenzione della corruzione. Gestisce il portale per i CIG.

**ARPA (Agenzia Regionale Protezione Ambiente)**
Ente pubblico che si occupa di controlli ambientali, monitoraggio inquinamento e rilascio pareri tecnici su autorizzazioni ambientali.

**Audit Trail**
Registro cronologico completo di tutte le operazioni effettuate su un sistema, che documenta chi ha fatto cosa, quando e perché. Immutabile e obbligatorio per legge.

**CIG (Codice Identificativo Gara)**
Codice univoco obbligatorio per appalti pubblici sopra determinate soglie, richiesto per tracciabilità e trasparenza (Legge 136/2010).

**Conferenza di Servizi**
Riunione tra più enti pubblici per acquisire tutti i pareri necessari su un procedimento complesso in un'unica sede, accelerando i tempi.

**Delibera**
Atto collegiale adottato da un organo decisionale (Giunta, Consiglio Comunale) che esprime una volontà politica o amministrativa.

**Determinazione Dirigenziale**
Atto amministrativo firmato da un dirigente per l'attuazione di decisioni già prese o per atti gestionali di sua competenza (es. affidamento lavori, autorizzazioni).

**DPO (Data Protection Officer)**
Responsabile della protezione dei dati personali in un'organizzazione, obbligatorio per enti pubblici secondo il GDPR.

**GDPR (General Data Protection Regulation)**
Regolamento europeo (679/2016) sulla protezione dei dati personali, obbligatorio dal 2018. Impone trasparenza, sicurezza e diritti degli interessati.

**Istanza**
Richiesta formale presentata da un cittadino o azienda alla PA per ottenere un servizio, un'autorizzazione o un provvedimento.

**Ordinanza**
Atto urgente emesso da un'autorità amministrativa (Sindaco, Dirigente) per situazioni straordinarie o emergenze che richiedono decisioni rapide.

**Parere Obbligatorio**
Valutazione tecnica richiesta per legge a un ente terzo prima di adottare un provvedimento. Il procedimento non può concludersi senza questo parere.

**Parere Facoltativo**
Valutazione tecnica che può essere richiesta ma non è obbligatoria per legge. L'ente può decidere anche senza attendere il parere.

**Procedimento Amministrativo**
Insieme di atti e fasi che la PA deve seguire per arrivare a una decisione finale (provvedimento). Regolato dalla Legge 241/1990.

**Protocollo**
Numero univoco assegnato a un documento ufficiale al momento della registrazione, che certifica data e ora di acquisizione. Ha valore legale.

**Responsabile del Procedimento**
Funzionario pubblico designato per legge (L. 241/1990 art. 5) a curare l'istruttoria e garantire che il procedimento si concluda nei tempi previsti.

**Silenzio-Assenso**
Meccanismo per cui, se la PA non risponde entro i termini, la richiesta si intende automaticamente accolta (solo per procedimenti specifici previsti dalla legge).

### Termini Tecnologici AI

**AI (Artificial Intelligence / Intelligenza Artificiale)**
Tecnologia che permette ai computer di eseguire compiti che richiedono intelligenza umana: comprendere testo, prendere decisioni, riconoscere pattern.

**BERT (Bidirectional Encoder Representations from Transformers)**
Modello AI di Google specializzato nella comprensione del linguaggio naturale. Legge il testo in entrambe le direzioni per capire meglio il contesto.

**Blockchain**
Tecnologia di registro distribuito e immutabile, dove ogni operazione è registrata in modo permanente e non modificabile. Usata per audit trail certificati.

**Classificazione**
Processo con cui l'AI assegna una categoria a un documento (es. "questa è una Delibera", "questo è un Atto di Urbanistica").

**Claude**
Modello di AI conversazionale sviluppato da Anthropic, alternativa a GPT-4, specializzato in testi lunghi e ragionamento complesso.

**Confidenza (Confidence)**
Percentuale che indica quanto l'AI è sicura della sua risposta (es. 95% = molto sicura, 60% = incerta). Importante per decidere se serve revisione umana.

**DistilBERT**
Versione leggera e veloce di BERT, ottimizzata per classificazioni rapide mantenendo buona accuratezza.

**Embedding**
Rappresentazione numerica di un testo che l'AI può "comprendere". Permette di confrontare documenti per similarità anche se usano parole diverse.

**FAISS (Facebook AI Similarity Search)**
Software di Meta per ricerche ultra-veloci tra milioni di documenti basandosi sul significato, non solo sulle parole esatte.

**Fine-tuning**
Processo di addestramento di un'AI già esistente su dati specifici (es. delibere italiane) per migliorarne le prestazioni su quel dominio.

**GPT-4 (Generative Pre-trained Transformer 4)**
Modello AI di OpenAI (creatore di ChatGPT) molto potente per generazione di testo. Usato per scrivere documenti complessi.

**Groq**
Azienda che fornisce hardware specializzato per eseguire AI in modo estremamente veloce (fino a 10x più rapido di GPU normali).

**HITL (Human-in-the-Loop)**
Approccio dove l'essere umano interviene nel processo automatico per verificare, correggere o approvare decisioni dell'AI. Obbligatorio per atti amministrativi.

**Inference**
Processo con cui un'AI già addestrata elabora nuovi dati per produrre un risultato (es. classificare un documento, generare un testo).

**Jinja2**
Sistema di template (modelli riutilizzabili) per generare documenti dinamici, simile a Word ma molto più potente e automatizzabile.

**LangChain**
Framework software che coordina più operazioni AI in sequenza, permettendo di creare flussi complessi (es. "cerca normativa → scrivi documento → valida").

**LanguageTool**
Software open-source per correzione grammaticale e stilistica avanzata, supporta oltre 20 lingue incluso l'italiano.

**LIME (Local Interpretable Model-agnostic Explanations)**
Strumento che spiega perché l'AI ha preso una certa decisione, mostrando quali parti del testo hanno influenzato di più.

**LLM (Large Language Model)**
Modelli AI giganteschi (miliardi di parametri) addestrati su enormi quantità di testo per comprendere e generare linguaggio naturale (es. GPT-4, Claude).

**LSTM (Long Short-Term Memory)**
Tipo di AI specializzata nell'analizzare sequenze temporali, usata per rilevare pattern anomali nel tempo (es. comportamenti sospetti).

**Mistral-7B**
Modello AI francese open-source, molto efficiente, usato per sintesi e comprensione testi. "7B" indica 7 miliardi di parametri.

**Neo4j**
Database a grafo che rappresenta dati come nodi connessi (es. "Legge A modifica Legge B, che abroga Legge C"). Ottimo per relazioni complesse tra normative.

**NLP (Natural Language Processing)**
Branca dell'AI che si occupa di elaborare il linguaggio umano: capire testi, estrarre informazioni, tradurre, generare contenuti.

**One-Shot**
Approccio dove si chiede all'AI di completare un compito complesso in un'unica volta, senza passaggi intermedi (sconsigliato per atti amministrativi).

**Orchestrazione**
Coordinamento automatico di più servizi/componenti software che collaborano per completare un processo complesso.

**PostgreSQL**
Database relazionale open-source molto robusto, usato per conservare dati strutturati (metadata, audit trail, normative).

**Prompt**
Istruzione testuale data a un'AI per farle svolgere un compito (es. "Scrivi una delibera su questo argomento...").

**Redis**
Database in-memory (in RAM) ultra-veloce usato come cache per accelerare operazioni ripetute (es. template già caricati, classificazioni recenti).

**Retrieval (RAG - Retrieval Augmented Generation)**
Tecnica dove l'AI cerca informazioni in un database prima di generare una risposta, migliorando accuratezza e riducendo "allucinazioni".

**Ricerca Semantica**
Ricerca basata sul significato, non sulle parole esatte. Trova documenti rilevanti anche se usano termini diversi (es. cerca "casa" trova anche "abitazione").

**SHAP (SHapley Additive exPlanations)**
Strumento avanzato per spiegare decisioni AI calcolando quanto ogni informazione in input ha contribuito al risultato finale.

**spaCy**
Libreria Python per NLP: riconosce automaticamente nomi, date, luoghi, enti, importi in un testo (Named Entity Recognition).

**Template**
Modello predefinito di documento con parti fisse e parti variabili da compilare (es. "DELIBERA N. ___ DEL ___").

**Token**
Unità base di testo elaborata dall'AI (approssimativamente una parola o parte di essa). I modelli AI hanno limiti di token per richiesta.

**Transformer**
Architettura di rete neurale alla base dei moderni LLM (GPT, BERT, ecc.), molto efficace nel comprendere relazioni nel linguaggio.

**Validazione**
Processo di verifica automatica che controlla se un documento rispetta regole e requisiti predefiniti (es. presenza dati obbligatori, correttezza normativa).

**Workflow**
Flusso di lavoro: sequenza di passi da eseguire per completare un processo (es. classificazione → generazione → validazione → approvazione).

### Termini Software e Infrastruttura

**API (Application Programming Interface)**
Interfaccia che permette a programmi diversi di comunicare tra loro (es. SP01 chiama SP03 per ottenere normativa).

**Apache Airflow**
Software open-source per orchestrare workflow complessi, schedulare operazioni, gestire dipendenze tra task.

**Docker**
Tecnologia per "containerizzare" applicazioni: ogni componente gira in un ambiente isolato standardizzato, facile da spostare e scalare.

**D3.js**
Libreria JavaScript per creare visualizzazioni interattive avanzate (grafici, timeline, diagrammi) su web.

**ELK Stack (Elasticsearch, Logstash, Kibana)**
Suite di strumenti per raccogliere, analizzare e visualizzare log di sistema in tempo reale.

**FastAPI**
Framework Python moderno per creare API veloci e ben documentate, usato per servizi web ad alte prestazioni.

**HashiCorp Vault**
Software per gestire in sicurezza credenziali, password, chiavi di crittografia (segreti) con controllo accessi granulare.

**JWT (JSON Web Token)**
Standard per creare token di autenticazione sicuri che contengono informazioni cifrate sull'utente.

**Apache NiFi**
Piattaforma open-source enterprise per orchestrazione workflow e data routing con completa tracciabilità tramite Data Provenance.

**Kubernetes**
Sistema per gestire automaticamente container Docker su cluster di server, garantendo scalabilità e affidabilità.

**MinIO**
Sistema di storage ad oggetti open-source (simile ad Amazon S3) per conservare file, documenti, backup in modo scalabile.

**React**
Libreria JavaScript di Meta per creare interfacce web moderne, reattive e performanti.

**Streamlit**
Framework Python per creare rapidamente dashboard e applicazioni web per data science e AI.

**Temporal.io**
Piattaforma per orchestrare workflow complessi e di lunga durata, con gestione automatica di errori e retry.

### Acronimi e Sigle

**ASL** - Azienda Sanitaria Locale
**CIG** - Codice Identificativo Gara
**GDPR** - General Data Protection Regulation
**HITL** - Human-in-the-Loop
**LLM** - Large Language Model
**NER** - Named Entity Recognition
**NLP** - Natural Language Processing
**PA** - Pubblica Amministrazione
**RAG** - Retrieval Augmented Generation
**SP** - Sottoprogetto (SP01, SP02, SP03, ecc.)

### Normative Citate

**D.Lgs 42/2004** - Codice dei Beni Culturali e del Paesaggio
**D.Lgs 152/2006** - Codice dell'Ambiente (Testo Unico Ambientale)
**L. 136/2010** - Tracciabilità flussi finanziari (obbligo CIG)
**L. 241/1990** - Legge sul Procedimento Amministrativo (norme generali PA)
**L.R. 12/2005** - Esempio di Legge Regionale su Urbanistica (varia per regione)
**L.R. 62/1998** - Esempio di Legge Regionale su Tutela Acque (varia per regione)

**Reg. UE 679/2016** - Regolamento GDPR sulla protezione dati personali

---

<div style="page-break-after: always;"></div>

## 🎓 Conclusioni

### In sintesi

Il sistema **non sostituisce** l'operatore pubblico, ma diventa un **assistente intelligente** che:

1. **Automatizza il lavoro ripetitivo** (scrittura, ricerca normativa, controlli)
2. **Riduce gli errori** grazie a verifiche multiple automatiche
3. **Fa risparmiare tempo** (da 3-4 ore a meno di 1 minuto di lavoro effettivo)
4. **Garantisce conformità** alle leggi e trasparenza
5. **Lascia all'umano** le decisioni finali (approvazione, modifiche strategiche)

### Perché serve un approccio Multi-Step?

❌ **One-Shot = Scatola nera**: Non si sa come arriva al risultato, non è controllabile
✅ **Multi-Step = Catena di montaggio trasparente**: Ogni passaggio è verificabile e migliorabile

### Analogia finale

**Costruire una casa**:
- ❌ One-Shot: Chiedere a un robot di costruire tutta la casa in un colpo solo
  - Non si possono fare verifiche intermedie
  - Se sbaglia le fondamenta, crolla tutto
  - Non si può migliorare solo una parte

- ✅ Multi-Step: Costruire con fasi (fondamenta → muri → tetto → impianti → finiture)
  - Ogni fase ha specialisti e controlli
  - Se c'è un errore, si corregge solo quella fase
  - Si può migliorare ogni fase nel tempo
  - Il risultato finale è certificato e tracciato
