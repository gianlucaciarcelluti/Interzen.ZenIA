# Matrice Dipendenze Sottoprogetti - UC5 Produzione Documentale Integrata

## Overview Dipendenze

```mermaid
graph TD
    ```markdown
    # Matrice Dipendenze Sottoprogetti - UC5 Produzione Documentale Integrata

    ## Overview Dipendenze

    ```mermaid
    graph TD
        subgraph Input
            PEC[PEC/Email]
            DOCS[Documenti]
        end

        subgraph Processing
            SP01[SP01<br/>Parser EML]
            SP02[SP02<br/>Document Extractor]
            SP03[SP03<br/>Classificatore Procedurale]
            SP07[SP07<br/>Classificatore Contenuti]
            SP04[SP04<br/>Knowledge Base]
            SP05[SP05<br/>Motore Template]
            SP06[SP06<br/>Validator]
            SP08[SP08<br/>Quality Checker]
        end

        subgraph Orchestration & Output
            SP09[SP09<br/>Motore Workflow]
            SP10[SP10<br/>Dashboard]
            SP11[SP11<br/>Sicurezza & Audit]
        end

        PEC --> SP01
        DOCS --> SP02

        SP01 --> SP02
        SP02 --> SP03
        SP02 --> SP07

        SP03 --> SP04
        SP03 --> SP05
        SP04 --> SP05

        SP05 --> SP06
        SP06 --> SP08
        SP07 --> SP08

        SP01 -.-> SP09
        SP02 -.-> SP09
        SP03 -.-> SP09
        SP05 -.-> SP09
        SP06 -.-> SP09
        SP08 -.-> SP09

        SP09 --> SP10
        SP01 --> SP11
        SP02 --> SP11
        SP09 --> SP11
    ```

    ## Matrice Dipendenze Dettagliata

    | SP | Nome | Dipendenze In | Dipendenze Out | Criticità | Dati |
    |---|---|---|---|---|---|
    | **SP01** | Parser EML | PEC/Email | SP02, SP09, SP11 | CRITICA | Email parsate + allegati |
    | **SP02** | Document Extractor | SP01, Documenti | SP03, SP07, SP09, SP11 | CRITICA | Testo estratto + metadata |
    | **SP03** | Classificatore Procedurale | SP02 | SP04, SP05, SP09 | ALTA | Classificazione + tipo procedimento |
    | **SP04** | Knowledge Base | SP03 | SP05 | MEDIA | Normativa + template + riferimenti |
    | **SP05** | Motore Template | SP03, SP04 | SP06, SP09 | ALTA | Bozza documento dal template |
    | **SP06** | Validator | SP05 | SP08, SP09 | ALTA | Risultati validazione + errori |
    | **SP07** | Classificatore Contenuti | SP02 | SP08, SP09 | MEDIA | Tag di classificazione contenuti |
    | **SP08** | Quality Checker | SP06, SP07 | SP09 | MEDIA | Punteggio qualità + suggerimenti |
    | **SP09** | Motore Workflow | Tutti gli SP (dip. soft) | SP10, SP11 | CRITICA | Stato workflow + esecuzione |
    | **SP10** | Dashboard | SP09 | Visualizzazione | MEDIA | Visualizzazione UI |
    | **SP11** | Sicurezza & Audit | Tutti gli SP | Log | CRITICA | Traccia di audit + eventi di sicurezza |

    ## Flusso Dati Principale

    ```
    PEC/Email
      ↓
    SP01 (Parser EML)
      ├─→ SP02 (Document Extractor)
      │     ├─→ SP03 (Classificatore Procedurale)
      │     │     ├─→ SP04 (Knowledge Base)
      │     │     │     ↓
      │     │     └─→ SP05 (Motore Template)
      │     │           ├─→ SP06 (Validator)
      │     │           │     ↓
      │     │           └─→ SP08 (Quality Checker)
      │     │                 ↓
      │     └─→ SP07 (Classificatore Contenuti)
      │           ↓
      │         SP08 (Quality Checker)
      │
      └─→ SP09 (Motore Workflow) ◄─── Tutti gli SP
            ├─→ SP10 (Dashboard)
            └─→ SP11 (Sicurezza & Audit)
    ```

    ## Dipendenze Critiche (Hard Dependencies)

    ### 1. SP01 → SP02 (Pipeline di input)
    - **Tipo**: Dipendenza hard
    - **Dato**: Email parsata con allegati
    - **Criticità**: CRITICA - Nessun parsing email = nessun processo documentale
    - **SLA**: Parsing email < 2s
    - **Mitigazione**: Accodamento per volumi elevati, retry su failure

    ### 2. SP02 → SP03/SP07 (Classificazione documenti)
    - **Tipo**: Dipendenza hard
    - **Dato**: Contenuto documento estratto
    - **Criticità**: CRITICA - La classificazione è necessaria per il routing
    - **SLA**: Classificazione < 5s per documento
    - **Mitigazione**: Cache delle classificazioni, processing asincrono per documenti grandi

    ### 3. SP03 → SP05 (Da procedura a template)
    - **Tipo**: Dipendenza hard
    - **Dato**: Classificazione procedimento
    - **Criticità**: ALTA - La selezione del template dipende dal tipo di procedimento
    - **SLA**: Selezione template < 1s
    - **Mitigazione**: Pre-load dei template, versioning

    ### 4. SP05 → SP06 → SP08 (Generazione → Validazione)
    - **Tipo**: Dipendenze sequenziali hard
    - **Dato**: Documento generato → errori di validazione → controlli di qualità
    - **Criticità**: ALTA - Il controllo qualità è obbligatorio
    - **SLA**: Validazione completa < 10s
    - **Mitigazione**: Validazione parallela, caching

    ### 5. SP09 (Motore Workflow)
    - **Tipo**: Orchestratore centrale
    - **Dato**: Coordina tutti gli SP
    - **Criticità**: CRITICA - SPOF per l'esecuzione del workflow
    - **SLA**: Step workflow < 500ms
    - **Mitigazione**: High availability, istanze multiple, coda per step in attesa

    ### 6. SP11 (Sicurezza & Audit)
    - **Tipo**: Preoccupazione trasversale
    - **Dato**: Riceve eventi da tutti gli SP
    - **Criticità**: CRITICA - Requisito di non ripudio
    - **SLA**: Logging audit < 100ms (asincrono)
    - **Mitigazione**: Logging asincrono, audit log immutabile

    ## Dipendenze Soft (Optional/Async)

    - **SP04**: La Knowledge Base può essere obsoleta/cacheata (aggiornata asincrono)
    - **SP07**: La classificazione dei contenuti è un miglioramento opzionale
    - **SP10**: La dashboard è in sola lettura, può essere ritardata

    ## Dipendenze Cicliche

    ✅ **NESSUNA dipendenza ciclica** - Struttura DAG (Directed Acyclic Graph) confermata.

    Catene lineari:
    - PEC → SP01 → SP02 → SP03 → SP05 → SP06 → SP08
    - PEC → SP01 → SP02 → SP07 → SP08
    - Tutti → SP09 → SP10/SP11

    ## Matrice Tecnologica

    | SP | Linguaggio | Framework | DB |
    |---|---|---|---|
    | SP01 | Python | email-parser | PostgreSQL |
    | SP02 | Python | Tesseract, spaCy | PostgreSQL |
    | SP03 | Python | DistilBERT | PostgreSQL |
    | SP04 | Python | RAG, Mistral | Vector DB |
    | SP05 | Python | LangChain, GPT-4 | PostgreSQL |
    | SP06 | Python | BERT | PostgreSQL |
    | SP07 | Python | spaCy | PostgreSQL |
    | SP08 | Python | LanguageTool | PostgreSQL |
    | SP09 | Python | Apache NiFi | PostgreSQL |
    | SP10 | React | Streamlit | -Redis |
    | SP11 | Python | FastAPI | PostgreSQL, ELK |

    ## KPI per SP

    - **SP01**: Latency parsing email < 2s, accuratezza estrazione allegati > 99%
    - **SP02**: Accuratezza OCR > 95%, latency estrazione documento < 5s
    - **SP03**: Accuratezza classificazione > 90%, rilevamento procedimento > 95%
    - **SP04**: Accuratezza ricerca KB > 85%, confidenza matching template > 80%
    - **SP05**: Latency generazione documento < 10s, accuratezza applicazione template > 98%
    - **SP06**: Latency validazione < 2s, accuratezza rilevamento errori > 90%
    - **SP07**: Accuratezza tagging contenuti > 85%
    - **SP08**: Accuratezza punteggio qualità > 90%, rilevanza suggerimenti > 80%
    - **SP09**: Latency esecuzione workflow < 500ms, tasso completamento > 99%
    - **SP10**: Refresh dashboard < 5s, uptime > 99.9%
    - **SP11**: Latency logging audit < 100ms, completezza 100%

    ## Ordine Implementazione Consigliato

    1. **Fase 1 - Fondazione**: SP04 (Knowledge Base - livello dati)
    2. **Fase 2 - Input Processing**: SP01 (Parser EML), SP02 (Document Extractor)
    3. **Fase 3 - Classificazione**: SP03 (Procedurale), SP07 (Contenuti)
    4. **Fase 4 - Generazione & Validazione**: SP05 (Motore Template), SP06 (Validator)
    5. **Fase 5 - Qualità**: SP08 (Quality Checker)
    6. **Fase 6 - Orchestrazione**: SP09 (Motore Workflow)
    7. **Fase 7 - Cross-Cutting**: SP11 (Sicurezza), SP10 (Dashboard)

    ## Rischi e Mitigazioni

    ### SPOF (Single Point of Failure)
    - **SP09 Motore Workflow**: Orchestratore centrale
      - **Mitigazione**: Cluster HA, auto-failover, coda per step in attesa
    - **SP01 Parser EML**: Gateway di input
      - **Mitigazione**: Sistema di code, retry, parsing di fallback
    - **SP05 Motore Template**: Generazione documenti
      - **Mitigazione**: Caching template, gestione versioni, template di fallback

    ### Colli di bottiglia prestazionali
    - **SP02 OCR**: Computazione intensiva
      - **Mitigazione**: Accelerazione GPU, processing asincrono, code
    - **SP05 Generazione LLM**: Limiti token
      - **Mitigazione**: Chunking dei documenti, rate limiting, caching
    - **SP03 Inference modello**: Latency ML
      - **Mitigazione**: Ottimizzazione modelli, inferenza batch, caching

    ### Scenari di Fallimento
    - **SP01 fallisce**: Nessun processamento email - coda e retry
    - **SP03 fallisce**: Usare procedimento di default o intervento manuale
    - **SP05 fallisce**: Usare placeholder template + revisione HITL
    - **SP09 fallisce**: Usare coda sequenziale + esecuzione manuale
    - **SP11 fallisce**: Log su file + recovery asincrona

    ## HITL (Human-in-the-Loop)

    Considerazioni speciali per UC5: interfaccia HITL per:
    - Classificazioni incerte (SP03 < 80% confidenza)
    - Problemi generazione template (errori validazione SP05)
    - Tipologie procedimento complesse (override manuale)
    - Problemi qualità documento (suggerimenti SP08)

    Il manager HITL coordina con SP09 Motore Workflow per il tracciamento delle decisioni.

    ## Strategia di Test

    | Tipo | Scenario | Catena di Dipendenze |
    |---|---|---|
    | Unit | SP individuale | Nessuna |
    | Integration | SP01+SP02+SP03 | Input → Processing |
    | E2E | PEC → Documento Generato | Tutti gli SP in sequenza |
    | Load | 1000 email/ora | Tutti gli SP sotto carico |
    | Chaos | Fallimento SP | Fallback + recovery |


    ```

