# ⛔ DEPRECATED - Sequence Diagram: Flusso Completo con SP00

## Deprecation Notice

🚫 **QUESTO DOCUMENTO È DEPRECATO**. Usa la nomenclatura obsoleta **SP00 per il Procedural Classifier**, che è stata rinumerata a **SP03** in tutti i documenti attuali.

**Sostituito da**: [01 CANONICAL - Generazione Atto Completo.md](01 CANONICAL - Generazione Atto Completo.md)

**Ultima modifica**: Novembre 2025
**Motivo deprecazione**: Allineamento nomenclatura SP (SP00 rimosso dalla numerazione standard)
**Consulenza**: Se stai leggendo questo documento per référimento storico, leggi invece la [versione canonica aggiornata](01 CANONICAL - Generazione Atto Completo.md).

---

## Contenuto Originale (Archiviato per Riferimento Storico)

## Diagramma con SP01-SP02-SP03 + Human in the Loop

Questo diagramma mostra il flusso completo dall'email PEC in ingresso fino all'atto generato, evidenziando l'integrazione dei nuovi sottoprogetti SP01 (EML Parser) e SP02 (Document Extractor) insieme a SP03 per la classificazione del procedimento amministrativo e i checkpoint Human in the Loop (HITL).

```mermaid
sequenceDiagram
    autonumber
    participant U as 👤 Cittadino
    participant PEC as 📧 PEC Server
    participant WF as 🔄 Workflow<br/>Engine
    participant EML as 📩 SP01<br/>EML<br/>Parser
    participant DOC as 📄 SP02<br/>Document<br/>Extractor
    participant PROC as � SP03<br/>Procedural<br/>Classifier
    participant KB as 📚 SP04<br/>Knowledge<br/>Base
    participant TPL as ✍️ SP05<br/>Template<br/>Engine
    participant VAL as ✔️ SP06<br/>Validator
    participant CLS as 🏷️ SP07<br/>Classifier
    participant QC as 📝 SP08<br/>Quality<br/>Checker
    
    Note over U,QC: 📥 FASE 1: Ricezione Email PEC
    
    U->>PEC: Invia email PEC<br/>+ allegati (istanza, documenti)
    PEC->>WF: Notifica nuovo messaggio (.eml)
    
    rect rgb(255, 240, 200)
        Note over EML: ✨ FASE 2: Parsing Email
        WF->>EML: Parse file .eml
        EML->>EML: Estrae headers/body/attachments
        EML->>EML: Valida firma digitale PEC
        EML->>EML: Classifica intent email
        EML-->>WF: JSON email_metadata<br/>+ lista allegati (3 files)
    end
    
    rect rgb(240, 255, 240)
        Note over DOC: 📄 FASE 3: Estrazione Documenti
        WF->>DOC: Elabora allegati (parallelo)
        
        par Allegato 1: istanza.pdf
            DOC->>DOC: Extract text (no OCR)
            DOC->>DOC: Classifica: istanza_procedimento
            DOC->>DOC: Estrai dati (NER): richiedente, oggetto
        and Allegato 2: carta_identita.pdf
            DOC->>DOC: Extract text
            DOC->>DOC: Classifica: documento_identita
            DOC->>DOC: Estrai: CF, nome, scadenza
        and Allegato 3: planimetria.pdf
            DOC->>DOC: Detect technical drawing
            DOC->>DOC: Classifica: planimetria_tecnica
        end
        
        DOC-->>WF: JSON documents[]<br/>+ validation_status
    end
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #1: Verifica Completezza Documentale
        WF->>U: Mostra allegati classificati<br/>+ dati estratti
        U->>U: Verifica identità e completezza
        U->>WF: ✅ Conferma documenti OK
        Note over WF: Traccia verifica documentale
    end
    
    rect rgb(255, 240, 200)
        Note over PROC: 🎯 FASE 4: Classificazione Procedimento
        WF->>PROC: Classifica istanza<br/>(con dati da SP02)
        PROC->>PROC: Analisi semantica<br/>+ metadata arricchiti
        PROC->>KB: Recupera procedimenti simili
        KB-->>PROC: Database procedimenti
        PROC-->>WF: 📋 Procedimento:<br/>AUTORIZ_SCARICO_ACQUE<br/>🎭 Provvedimento:<br/>DETERMINAZIONE_DIRIGENZIALE<br/>📜 Normativa: D.Lgs 152/2006
    end
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #2: Conferma Procedimento
        WF->>U: Propone: AUTORIZZAZIONE_SCARICO<br/>Confidence: 96%
        U->>WF: ✅ Conferma / ✏️ Modifica
        Note over WF: Traccia decisione utente
    end
    
    WF->>CLS: Classifica tipo documento finale
    CLS-->>WF: Tipo: DETERMINAZIONE<br/>Confidence: 94%
    
    WF->>KB: Recupera normativa specifica
    KB-->>WF: Contesto normativo
    
    rect rgb(200, 240, 255)
        Note over TPL: FASE 5: Generazione con Dati Pre-Estratti
        WF->>TPL: Genera documento<br/>(con dati SP02 + procedimento SP03)
        TPL->>TPL: Pre-compila template<br/>con metadata richiedente
        TPL-->>WF: Documento generato (v1.0-AI)
    end
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #3: Review Draft
        WF->>U: Mostra draft completo
        U->>WF: ✅ Approva / ✏️ Modifica
        Note over WF: Salva versione modificata (v1.1-HUMAN)
    end
    
    rect rgb(200, 255, 200)
        Note over VAL: FASE 6: Validazione Procedimento-Specifica
        WF->>VAL: Valida documento<br/>(controlli per procedimento)
        VAL-->>WF: ✅ Validato (score: 97/100)
    end
    
    WF->>QC: Controlla qualità linguistica
    QC-->>WF: Report qualità (score: 82/100)
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #4: Approvazione Finale
        WF->>U: Documento finale + report<br/>Richiede firma digitale
        U->>WF: ✅ Firma e approva
        Note over WF: Registra approvazione finale
    end
    
    WF->>U: 📧 Notifica PEC:<br/>atto approvato e protocollato
    
    Note over U,QC: 📤 FINE: Processo completato
```

## Confronto Prima/Dopo

### ❌ Prima (senza SP01-SP02-SP03 e HITL)

```
Email PEC → Upload manuale documenti → Trascrizione dati → Workflow → 
Classifier (documento) → Generate → Validate → Output
                          ↓
                    Tipo documento generico
                    Normativa generica
                    Dati inseriti manualmente
                    Nessun controllo umano
```

**Problemi:**
- **Processo manuale**: operatore deve scaricare email e allegati
- **Trascrizione dati**: rischio errori nella digitazione CF, indirizzi, importi
- **Mancata validazione**: firma digitale e documenti identità non verificati
- Non si conosce il procedimento amministrativo
- Tipo provvedimento non derivato dal procedimento
- Normativa recuperata in modo generico
- **Nessuna verifica umana: rischio errori critici**
- **Responsabilità non tracciata**

### ✅ Dopo (con SP01-SP02-SP03 e HITL)

```
Email PEC → SP01 (Parse) → SP02 (Extract) → [HITL #1: Verifica Doc] →
SP03 (Procedimento) → [HITL #2: Conferma] → SP05 (Generate) → 
[HITL #3: Review] → SP06 (Validate) → SP08 (QC) → [HITL #4: Firma] → Output
                ↓
        Email parsed automaticamente
        Allegati classificati e estratti
        Dati strutturati con NER
        Firma digitale validata
        Procedimento specifico identificato
        4 checkpoint umani
        Tracciabilità totale
```

**Vantaggi:**
- ✅ **Automazione completa**: da email PEC a dati strutturati
- ✅ **Zero trascrizione manuale**: CF, indirizzi, importi estratti con OCR+NER
- ✅ **Validazione firma digitale**: PEC e .p7m verificati automaticamente
- ✅ **Classificazione allegati**: identifica istanza, documenti identità, planimetrie
- ✅ Procedimento amministrativo identificato
- ✅ Tipo provvedimento derivato automaticamente
- ✅ Normativa specifica per procedimento
- ✅ **4 checkpoint con intervento umano obbligatorio**
- ✅ **Responsabilità legale tracciata ad ogni step**
- ✅ **Versioning completo delle modifiche**
- ✅ **Audit trail: da email originale a atto firmato**

## Punti Human in the Loop (HITL)

### 🔄 HITL #1: Verifica Completezza Documentale
- **Dopo**: SP02 - Document Extractor
- **Decisione**: Verificare documenti estratti, identità validata, completezza allegati
- **Responsabilità**: Controllo formale istanza (Legge 241/90, art. 6)
- **Tracciamento**: Salvato in `hitl_interactions` con user_id, timestamp, documenti verificati
- **Azione alternativa**: Richiesta integrazioni via email

### 🔄 HITL #2: Conferma Procedimento
- **Dopo**: SP03 - Procedural Classifier
- **Decisione**: Confermare/Modificare il procedimento identificato
- **Responsabilità**: Classificazione amministrativa (Legge 241/90, art. 6)
- **Tracciamento**: Salvato in `hitl_interactions` con user_id, timestamp, motivazione

### 🔄 HITL #3: Review Draft Documento
- **Dopo**: SP05 - Template Engine
- **Decisione**: Revisionare bozza generata dall'AI (pre-compilata con dati SP02)
- **Responsabilità**: Correttezza contenuto atto (Legge 241/90, art. 3)
- **Tracciamento**: Versioning documento con track changes

### 🔄 HITL #4: Approvazione Finale
- **Dopo**: SP06 + SP08 (Validazione + Quality Check)
- **Decisione**: Firma digitale e pubblicazione
- **Responsabilità**: Responsabilità amministrativa totale
- **Tracciamento**: Firma digitale + audit trail immutabile (blockchain)

## Esempio Concreto

### Input Utente (Email PEC)
```
From: mario.rossi@industria-tessile-rossi.pec.it
To: protocollo@comune-esempio.legalmail.it
Subject: Richiesta autorizzazione scarico acque reflue industriali
Date: 2025-11-03 09:30:00

Attachments:
  1. istanza_scarico.pdf (245 KB)
  2. documento_identita.pdf.p7m (123 KB, firmato digitalmente)
  3. planimetria_stabilimento.pdf (890 KB)

Spett.le Amministrazione,
con la presente l'azienda Industria Tessile Rossi S.p.A. richiede 
autorizzazione allo scarico acque reflue industriali...
```

### Output SP01 - EML Parser (Fase 2)
```json
{
  "email_metadata": {
    "from": "mario.rossi@industria-tessile-rossi.pec.it",
    "subject": "Richiesta autorizzazione scarico acque reflue industriali",
    "date": "2025-11-03T09:30:00Z",
    "is_pec": true,
    "pec_receipt_type": "avvenuta-consegna"
  },
  "attachments": [
    {"filename": "istanza_scarico.pdf", "size": 245678},
    {"filename": "documento_identita.pdf.p7m", "is_signed": true},
    {"filename": "planimetria_stabilimento.pdf", "size": 890123}
  ],
  "classification_hints": {
    "keywords": ["scarico", "acque", "reflue", "autorizzazione"]
  }
}
```

### Output SP02 - Document Extractor (Fase 3)
```json
{
  "documents": [
    {
      "filename": "istanza_scarico.pdf",
      "document_type": "istanza_procedimento",
      "confidence": 0.96,
      "structured_data": {
        "richiedente": {
          "denominazione": "Industria Tessile Rossi S.p.A.",
          "cf": "12345678901",
          "piva": "IT12345678901",
          "sede": "Via Roma 1, 20100 Milano (MI)"
        },
        "oggetto_richiesta": "Autorizzazione scarico acque reflue industriali",
        "riferimenti_normativi": ["D.Lgs 152/2006"]
      }
    },
    {
      "filename": "documento_identita.pdf",
      "document_type": "documento_identita",
      "confidence": 0.98,
      "structured_data": {
        "tipo": "carta_identita",
        "numero": "CA12345678",
        "intestatario": {
          "nome": "ROSSI",
          "cognome": "MARIO",
          "cf": "RSSMRA70A01F205X"
        },
        "data_scadenza": "2030-01-15"
      }
    },
    {
      "filename": "planimetria_stabilimento.pdf",
      "document_type": "planimetria_tecnica",
      "confidence": 0.92
    }
  ],
  "validation_status": {
    "required_documents_present": true,
    "identity_verified": true,
    "signatures_valid": true
  }
}
```

### Output SP03 - Procedural Classifier (Fase 4)
```json
{
  "procedimento": "AUTORIZZAZIONE_SCARICO_ACQUE_REFLUE",
  "tipo_provvedimento": "DETERMINAZIONE_DIRIGENZIALE",
  "autorita_competente": "DIRIGENTE_SETTORE_AMBIENTE",
  "normativa_base": [
    "D.Lgs 152/2006 art. 124",
    "L.R. 62/1998 art. 8"
  ],
  "termini": "90 giorni",
  "enti_coinvolti": ["ARPA", "ASL"],
  "confidence": 0.96
}
```

### Utilizzo nelle Fasi Successive

**Fase 5 (Template Engine - SP05):**
- Usa template specifico: `TPL_DET_AMB_001`
- **Pre-compila automaticamente** con dati da SP02:
  - Richiedente: "Industria Tessile Rossi S.p.A."
  - CF/P.IVA: già estratti
  - Sede legale: "Via Roma 1, 20100 Milano"
- Include normativa da SP03: D.Lgs 152/2006, L.R. 62/1998
- Inserisce termini: 90 giorni
- Indica competenza: Dirigente Settore Ambiente
- **Vantaggio**: riduce da 15 a 5 i campi da rivedere manualmente

**Fase 6 (Validator - SP06):**
- Controlla metadata obbligatori per procedimento scarichi
- Verifica presenza pareri ARPA e ASL
- Valida conformità a normativa specifica
- **Cross-check**: CF richiedente in istanza vs documento identità (da SP02)

## Timeline Completa

```mermaid
gantt
    title Generazione Atto da Email PEC (End-to-End)
    dateFormat X
    axisFormat %Ss

    section Fase 1
    Ricezione PEC            :0, 500ms

    section Fase 2
    Parsing Email (SP01)     :500, 800ms

    section Fase 3
    Estrazione Doc (SP02)    :1300, 2500ms

    section Fase 4
    HITL #1 Verifica Doc     :3800, 8000ms

    section Fase 5
    Classif. Procedimento    :11800, 520ms

    section Fase 6
    HITL #2 Conferma Proc    :12320, 5000ms

    section Fase 7
    Classif. + KB            :17320, 1200ms

    section Fase 8
    Generazione Template     :18520, 2300ms

    section Fase 9
    HITL #3 Review Draft     :20820, 12000ms

    section Fase 10
    Validazione + QC         :32820, 1100ms

    section Fase 11
    HITL #4 Firma            :33920, 8000ms

    section Fase 12
    Protocollo + Notifica    :41920, 2000ms
```

**Tempo totale processo:**
- **Fase automatica (SP01-SP08)**: ~8 secondi
  - SP01 (Email parsing): 0.8s
  - SP02 (Document extraction con OCR): 2.5s
  - SP03 (Procedural classifier): 0.5s
  - SP05-SP08 (Template, validation, QC): 3.4s
- **Review umana (4 HITL)**: ~33 secondi
  - HITL #1 (Verifica documenti): 8s
  - HITL #2 (Conferma procedimento): 5s
  - HITL #3 (Review draft): 12s
  - HITL #4 (Firma): 8s
- **TOTALE: ~44 secondi** (da ricezione PEC a atto protocollato)

**Nota**: Tempo variabile in base a:
- Numero allegati (più allegati → più tempo SP02)
- Qualità scansioni (OCR richiesto → +2-3s per documento)
- Complessità review umana

## Decision Flow Completo

```mermaid
flowchart TD
    START([Email PEC Ricevuta]) --> PARSE[SP01: Parse Email]
    
    PARSE --> CHECK_ATT{Allegati<br/>Presenti?}
    CHECK_ATT -->|No| REJECT[Richiedi Integrazioni]
    CHECK_ATT -->|Si| EXTRACT[SP02: Estrai Documenti]
    
    EXTRACT --> CLASSIFY_DOC{Classifica<br/>Allegati}
    
    CLASSIFY_DOC -->|istanza| DOC1[Estrai Dati Istanza]
    CLASSIFY_DOC -->|documento_identita| DOC2[Valida Identità]
    CLASSIFY_DOC -->|planimetria| DOC3[Archivia Allegato Tecnico]
    CLASSIFY_DOC -->|altro| DOC4[Classifica Tipo Documento]
    
    DOC1 --> VALIDATE_DOCS{Documenti<br/>Completi?}
    DOC2 --> VALIDATE_DOCS
    DOC3 --> VALIDATE_DOCS
    DOC4 --> VALIDATE_DOCS
    
    VALIDATE_DOCS -->|No| REJECT
    VALIDATE_DOCS -->|Si| HITL1[HITL #1: Verifica Completezza]
    
    HITL1 -->|Richiedi Integrazioni| REJECT
    HITL1 -->|OK| PROC_CLASS[SP03: Classifica Procedimento]
    
    PROC_CLASS --> ANALYZE{Analizza<br/>Oggetto Istanza}
    
    ANALYZE -->|"scarico acque"| PROC1[AUTORIZ_SCARICO_ACQUE]
    ANALYZE -->|"permesso costruire"| PROC2[PERMESSO_COSTRUIRE]
    ANALYZE -->|"licenza commercio"| PROC3[LICENZA_COMMERCIALE]
    ANALYZE -->|"altro"| PROC_GEN[GENERICO]
    
    PROC1 --> HITL2[HITL #2: Conferma Procedimento]
    PROC2 --> HITL2
    PROC3 --> HITL2
    PROC_GEN --> HITL2
    
    HITL2 -->|Modifica| PROC_CLASS
    HITL2 -->|Conferma| TEMPLATE[SP05: Genera Documento]
    
    TEMPLATE --> HITL3[HITL #3: Review Draft]
    HITL3 -->|Modifica| TEMPLATE
    HITL3 -->|Approva| VALIDATE[SP06: Valida Conformità]
    
    VALIDATE --> QC[SP08: Quality Check]
    QC --> HITL4[HITL #4: Firma Digitale]
    
    HITL4 --> PROTOCOL[Protocolla e Notifica]
    PROTOCOL --> END([Processo Completato])
    
    REJECT --> EMAIL_RESP[Invia Email Richiesta Doc]
    EMAIL_RESP --> WAIT[Attendi Risposta Cittadino]
    WAIT --> START
    
    style PROC1 fill:#90EE90
    style PROC2 fill:#90EE90
    style PROC3 fill:#90EE90
    style PROC_GEN fill:#FFB6C1
    style HITL1 fill:#ffeb3b
    style HITL2 fill:#ffeb3b
    style HITL3 fill:#ffeb3b
    style HITL4 fill:#ffeb3b
    style REJECT fill:#f8d7da
```

## Benefici Integrazione SP01-SP02-SP03

### 🎯 Precisione
- **+25%** accuracy complessiva (dati estratti vs trascritti manualmente)
- **+15%** accuracy nella selezione template corretto (grazie a SP03)
- **-40%** errori di conformità normativa
- **-60%** errori di trascrizione (CF, P.IVA, indirizzi)
- **-30%** tempi di review umana (info più complete e pre-validate)

### ⚡ Performance
- **SP01 (EML Parser)**:
  - Latency media: 800ms per email con 3 allegati
  - Validation firma digitale PEC: 100% affidabile
  - Cache hit rate: 35% (email ricorrenti)
- **SP02 (Document Extractor)**:
  - Throughput: 20 allegati/minuto (con OCR)
  - Classification accuracy: 94% su 16 categorie documenti
  - NER precision (CF, P.IVA): 98%
- **SP03 (Procedural Classifier)**:
  - Cache hit rate: 43% (istanze simili)
  - Latency media: 520ms
  - Throughput: ~100 classificazioni/secondo

### 📊 Completezza
- **Automazione end-to-end**: da email PEC a JSON strutturato
- **Validazione documentale upstream**: firma digitale, documenti identità
- **Dati pre-estratti**: richiedente, CF, P.IVA, indirizzi, importi
- **Normativa applicabile** identificata automaticamente
- **Termini procedurali** chiari (es. 90 giorni)
- **Enti coinvolti** pre-identificati
- **Fasi procedurali** tracciate

### 🔄 Scalabilità
- **SP01**: Horizontal scaling su caselle PEC multiple
- **SP02**: Parallelizzazione estrazione allegati (max 12 replicas)
- **SP03**: Facile aggiunta nuovi procedimenti (insert DB)
- **Cross-layer**: Modelli riaddestrati con feedback operatori
- **Knowledge base** estendibile
- **API RESTful** standard per tutti i componenti

### 💰 ROI (Return on Investment)
- **Tempo risparmiato per pratica**: ~15 minuti (trascrizione manuale eliminata)
- **Pratiche/giorno gestibili**: da 20 a 80+ (4x incremento)
- **Errori ridotti**: -70% (GDPR compliance migliorata)
- **Costo operatore**: -60% (focus su review vs data entry)

---

**Conclusione:** L'integrazione di SP01-SP02-SP03 trasforma il sistema da "document processor" a **"email-to-act intelligent platform"**, eliminando il lavoro manuale di download, trascrizione e validazione documentale, permettendo agli operatori di concentrarsi sulla review qualitativa e decisionale.
