# 📘 CANONICAL - Sequence Diagram: Generazione Atto Amministrativo Completo

🏆 **CANONICAL REFERENCE**: Questo è il diagramma di sequenza autoritativo e completo per UC5. Contiene tutti i dettagli tecnici, API endpoints, payload JSON, timing, e strategie di caching/scalabilità.

**Versioni Supplementari**:
- [02 SUPPLEMENTARY - Overview Semplificato.md](02 SUPPLEMENTARY - Overview Semplificato.md) - Per stakeholder business
- [03 SUPPLEMENTARY - Ultra Semplificato.md](03 SUPPLEMENTARY - Ultra Semplificato.md) - Per presentazioni executive
- [04 DEPRECATED - Sequence Con SP00.md](04 DEPRECATED - Sequence Con SP00.md) - Versione archiviata (non usare)

---

## Flusso End-to-End: Da Email PEC a Pubblicazione

```mermaid
sequenceDiagram
    autonumber
    participant U as Cittadino/Operatore
    participant PEC as PEC Server
    participant UI as Web UI
    participant GW as API Gateway
    participant WF as Apache NiFi<br/>Workflow Orchestrator
    participant EML as SP01 EML Parser
    participant DOC as SP02 Document Extractor
    participant PROC as SP03 Procedural Classifier
    participant KB as SP04 Knowledge Base
    participant TPL as SP05 Template Engine<br/>(NiFi Process Group)
    participant VAL as SP06 Validator<br/>(NiFi Process Group)
    participant CLS as SP07 Classifier
    participant QC as SP08 Quality Checker<br/>(NiFi Process Group)
    participant SEC as SP11 Security & Audit<br/>(NiFi Process Group)
    participant DASH as SP10 Dashboard
    participant NIFI_PROV as NiFi Provenance<br/>(Data Lineage)
    participant PROT as Sistema Protocollo
    participant FIRMA as Firma Digitale
    participant DB as PostgreSQL
    participant CACHE as Redis Cache
    participant STORAGE as MinIO Storage
    
    Note over U,STORAGE: Fase 1: Ricezione Email PEC
    U->>PEC: Invia email PEC con istanza + allegati
    PEC->>WF: Notifica nuovo messaggio (.eml)
    WF->>SEC: Autentica e autorizza ricezione email
    SEC->>DB: Log email received event
    SEC-->>WF: Email validated
    
    WF->>WF: Inizia workflow generazione<br/>(workflow_id: WF-12345)
    WF->>DB: Crea record workflow<br/>status: EMAIL_RECEIVED
    WF->>NIFI_PROV: Log provenance event<br/>email.received
    WF->>STORAGE: Upload file .eml raw
    
    Note over U,STORAGE: Fase 2: Parsing Email e Estrazione Allegati
    WF->>EML: POST /parse-email<br/>{eml_file_path}
    EML->>EML: Parse headers/body/attachments
    EML->>EML: Valida firma digitale PEC
    EML->>EML: Classifica intent email
    EML->>STORAGE: Upload allegati estratti
    EML->>DB: Salva metadata email
    EML-->>WF: {email_metadata, attachments_list[],<br/>pec_validated: true}
    
    WF->>NIFI_PROV: Log provenance event<br/>email.parsed
    WF->>DB: Update workflow<br/>status: EMAIL_PARSED
    
    Note over U,STORAGE: Fase 3: Estrazione e Classificazione Documenti
    WF->>DOC: POST /extract-documents<br/>{attachments_list[]}
    
    par Elaborazione Parallela Allegati
        DOC->>DOC: Extract istanza.pdf<br/>(no OCR, native text)
        DOC->>DOC: Classifica: istanza_procedimento
        DOC->>DOC: NER: richiedente, CF, oggetto
    and
        DOC->>DOC: Extract documento_identita.pdf.p7m<br/>(unwrap signature)
        DOC->>DOC: Classifica: documento_identita
        DOC->>DOC: NER: CF, nome, scadenza
    and
        DOC->>DOC: Extract planimetria.pdf<br/>(detect technical drawing)
        DOC->>DOC: Classifica: planimetria_tecnica
    end
    
    DOC->>DB: Salva dati estratti
    DOC->>STORAGE: Salva versioni processate
    DOC-->>WF: {documents[], validation_status,<br/>required_docs_present: true}
    
    WF->>NIFI_PROV: Log provenance event<br/>documents.extracted
    WF->>DB: Update workflow<br/>status: DOCUMENTS_EXTRACTED
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #1: Verifica Completezza Documentale
        WF->>UI: Mostra allegati classificati + dati estratti
        UI-->>U: {documents[], validation_status}<br/>Richiede verifica
        U->>UI: ✅ Conferma / ✏️ Richiedi integrazioni
        alt Integrazione richiesta
            UI->>GW: POST /workflows/{id}/request-integration
            GW->>WF: Genera email richiesta documenti
            WF->>PEC: Invia email a cittadino
            Note over WF: Attendi risposta (max 30gg)
        else Documenti OK
            UI->>GW: POST /hitl/checkpoint-1<br/>{workflow_id, decision: "confirmed"}
            GW->>WF: Salva decisione HITL #1
            WF->>DB: INSERT INTO hitl_interactions
            WF->>SEC: Traccia verifica documentale
        end
    end
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "DOCS_VERIFIED"}
    
    Note over U,STORAGE: Fase 4: Classificazione Procedimento Amministrativo
    WF->>PROC: POST /classify-procedure<br/>{istanza_data (da SP02), email_metadata}
    PROC->>CACHE: Check cached procedure classification
    alt Cache Miss
        PROC->>PROC: DistilBERT inference<br/>+ NER extraction istanza
        PROC->>KB: GET /retrieve-procedures<br/>{extracted_entities}
        KB->>KB: Semantic search procedimenti<br/>+ Graph traversal
        KB-->>PROC: {procedimenti_rilevanti,<br/>provvedimenti_correlati}
        PROC->>PROC: Ranking e confidence scoring
        PROC->>DB: Retrieve historical patterns
        PROC->>STORAGE: Fetch template samples
        PROC->>CACHE: Store classification result<br/>(TTL: 2h)
    end
    PROC-->>WF: {procedimento: "AUTORIZ_SCARICO_ACQUE",<br/>tipo_provvedimento: "DETERMINAZIONE",<br/>normativa_base: [...],<br/>confidence: 0.96}
    
    WF->>NIFI_PROV: Log provenance event<br/>procedure.classified
    WF->>DB: Update workflow<br/>status: PROCEDURE_CLASSIFIED
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #2: Conferma Procedimento
        WF->>UI: Mostra proposta procedimento
        UI-->>U: {procedimento, tipo_provv, normativa}<br/>Richiede conferma
        U->>UI: ✅ Conferma / ✏️ Modifica
        UI->>GW: POST /hitl/checkpoint-2<br/>{workflow_id, decision, motivazione}
        GW->>WF: Salva decisione HITL #2
        WF->>DB: INSERT INTO hitl_interactions<br/>{user_id, decision, timestamp}
        WF->>SEC: Traccia decisione umana
    end
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "PROCEDURE_CONFIRMED",<br/>procedure_data}
    DASH->>DASH: Store classification metrics<br/>Show procedimento timeline
    
    Note over U,STORAGE: Fase 5: Classificazione Tipo Documento Finale
    WF->>CLS: POST /classify<br/>{metadata, context, procedimento}
    CLS->>CACHE: Check cached classification
    alt Cache Miss
        CLS->>CLS: DistilBERT inference<br/>+ NER extraction
        CLS->>DB: Retrieve similar documents
        CLS->>STORAGE: Fetch historical templates
        CLS->>CACHE: Store classification result<br/>(TTL: 1h)
    end
    CLS-->>WF: {doc_type: "DELIBERA_GIUNTA",<br/>category: "URBANISTICA",<br/>metadata_extracted: {...},<br/>confidence: 0.94}
    
    WF->>NIFI_PROV: Log provenance event<br/>document.classified
    WF->>DB: Update workflow<br/>status: CLASSIFIED
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "CLASSIFIED",<br/>classification_data}
    DASH->>DASH: Store metrics<br/>Update real-time view
    
    Note over U,STORAGE: Fase 6: Recupero Normativa e Contesto Giuridico
    WF->>KB: POST /retrieve-context<br/>{doc_type, subject_matter, procedimento}
    KB->>CACHE: Check cached normativa
    alt Cache Miss
        KB->>KB: Semantic search (FAISS)<br/>top-k=5 documenti rilevanti
        KB->>KB: Graph traversal (Neo4j)<br/>relazioni normative
        KB->>KB: RAG pipeline con Mistral-7B<br/>genera sintesi normativa
        KB->>CACHE: Store normativa context<br/>(TTL: 24h)
    end
    KB-->>WF: {normativa_refs: ["L.241/1990", ...],<br/>legal_context: "sintesi normativa",<br/>precedents: [...]}
    
    WF->>DB: Update workflow<br/>context_retrieved: true
    
    Note over U,STORAGE: Fase 5: Generazione Template con AI
    WF->>TPL: POST /generate<br/>{doc_type, metadata, legal_context, procedimento}
    TPL->>CACHE: Check template cache
    alt Template da generare
        TPL->>DB: Load Jinja2 base template<br/>per tipo documento
        TPL->>TPL: GPT-4/Claude prompt engineering<br/>+ injection metadata + normativa
        TPL->>TPL: LangChain orchestration<br/>multi-step generation
        TPL->>STORAGE: Fetch firma digitale template
        TPL->>TPL: Compile template Jinja2<br/>con dati strutturati
    end
    TPL-->>WF: {document_draft: "XML/HTML",<br/>sections_generated: 12,<br/>generation_time: 2.3s}
    
    WF->>NIFI_PROV: Log provenance event<br/>document.generated (full lineage)
    WF->>DB: Update workflow<br/>status: DRAFT_GENERATED
    WF->>STORAGE: Save draft version v0.1-AI
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #3: Review Draft
        WF->>UI: Mostra draft generato
        UI-->>U: {document_draft, sections}<br/>Editor con track changes
        U->>UI: ✅ Approva / ✏️ Modifica sezioni
        UI->>GW: POST /hitl/checkpoint-3<br/>{workflow_id, modified_draft}
        GW->>WF: Salva modifiche HITL #3
        WF->>STORAGE: Save version v0.2-HUMAN
        WF->>DB: INSERT INTO document_versions<br/>{version, diff, user_id}
        WF->>SEC: Traccia modifiche documento
    end
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "DRAFT_REVIEWED",<br/>template_data, generation_metrics}
    DASH->>DASH: Visualize AI decision path<br/>Show SHAP values
    
    Note over U,STORAGE: Fase 6: Validazione Semantica e Conformità
    WF->>VAL: POST /validate<br/>{document_draft, doc_type, procedimento}
    VAL->>VAL: BERT semantic analysis<br/>coerenza interna
    VAL->>KB: GET /check-compliance<br/>{document, normativa_refs}
    KB->>KB: Cross-reference con DB normativo
    KB-->>VAL: {compliance_issues: [...],<br/>missing_refs: [...]}
    
    VAL->>VAL: Rule engine (Drools)<br/>validazioni strutturali
    VAL->>VAL: Aggregazione errori per severità
    VAL-->>WF: {validation_status: "WARNING",<br/>critical_issues: [],<br/>warnings: ["Manca CIG"],<br/>suggestions: [...]}
    
    alt Errori Critici Rilevati
        WF->>NIFI_PROV: Log provenance event<br/>document.validation.failed
        WF->>UI: Notifica errori critici
        UI-->>U: Mostra errori e suggerimenti
        U->>UI: Corregge metadata
        Note over U,UI: Loop di correzione
    end
    
    WF->>NIFI_PROV: Log provenance event<br/>document.validated
    WF->>DB: Update workflow<br/>status: VALIDATED
    WF->>STORAGE: Save validated version v0.2
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "VALIDATED",<br/>validation_report, issues}
    DASH->>DASH: Display validation details<br/>Highlight warnings/errors
    
    Note over U,STORAGE: Fase 7: Quality Check Linguistico
    WF->>QC: POST /check-quality<br/>{document_validated}
    QC->>QC: LanguageTool grammar check
    QC->>QC: spaCy NLP analysis<br/>(POS, dependencies)
    QC->>QC: Custom rules<br/>terminologia amministrativa
    QC->>QC: Readability score<br/>(Gulpease index)
    QC-->>WF: {grammar_errors: 3,<br/>style_warnings: 5,<br/>readability_score: 62,<br/>corrections: [...]}
    
    alt Qualità Insufficiente
        WF->>TPL: POST /refine<br/>{document, quality_issues}
        TPL->>TPL: LLM refinement con feedback
        TPL-->>WF: {document_refined}
    end
    
    WF->>NIFI_PROV: Log provenance event<br/>document.quality.checked (full audit)
    WF->>DB: Update workflow<br/>status: QUALITY_CHECKED
    WF->>STORAGE: Save final version v1.0
    
    rect rgb(255, 235, 59, 0.3)
        Note over U,WF: 🔄 HITL #4: Approvazione Finale
        WF->>UI: Mostra documento finale + report
        UI-->>U: {document_final, validation_report,<br/>quality_report}<br/>Richiede firma digitale
        U->>UI: 🔐 Firma digitale + Approva
        UI->>GW: POST /hitl/checkpoint-4<br/>{workflow_id, digital_signature,<br/>final_approval}
        GW->>WF: Salva approvazione HITL #4
        WF->>DB: INSERT INTO hitl_interactions<br/>{user_id, signature, timestamp}
        WF->>SEC: Traccia firma digitale<br/>(blockchain hash)
    end
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "FINAL_APPROVED",<br/>quality_metrics}
    DASH->>DASH: Show quality scores<br/>Grammar/style report
    
    Note over U,STORAGE: Fase 8: Review Umana e Approvazione
    WF->>UI: Invia per review umana
    UI-->>U: Visualizza documento finale<br/>+ explainability dashboard
    
    DASH->>U: Mostra dashboard interattiva:<br/>- Workflow timeline<br/>- AI decisions path<br/>- Confidence scores<br/>- Issues & warnings<br/>- Audit trail preview
    
    U->>UI: Review documento
    
    alt Richieste modifiche
        U->>UI: Richiedi modifiche
        UI->>WF: POST /revise<br/>{feedback, changes}
        Note over WF: Loop revisione
    else Approva documento
        U->>UI: Approva documento
        UI->>GW: POST /approve<br/>{workflow_id, signature}
    end
    
    GW->>WF: Procedi con pubblicazione
    WF->>DB: Update workflow<br/>status: APPROVED
    
    Note over U,STORAGE: Fase 8: Integrazione Sistemi Legacy
    WF->>PROT: POST /protocolla<br/>{documento, metadata}
    PROT-->>WF: {numero_protocollo: "12345/2025",<br/>timestamp: "2025-10-08T10:30:00Z"}
    
    WF->>FIRMA: POST /firma-digitale<br/>{documento, responsabile}
    FIRMA-->>WF: {documento_firmato,<br/>timestamp_marca_temporale}
    
    WF->>STORAGE: Save final signed document<br/>path: /documenti/2025/12345.pdf.p7m
    WF->>DB: Update workflow<br/>status: PUBLISHED,<br/>protocollo: "12345/2025"
    
    Note over U,STORAGE: Fase 9: Audit Trail e Notifiche
    WF->>SEC: POST /audit-log<br/>{workflow_complete, actions_log}
    SEC->>DB: Store immutable audit trail<br/>(blockchain hash)
    SEC->>SEC: Generate compliance report<br/>(GDPR Art. 22)
    
    WF->>NIFI_PROV: Log provenance event<br/>workflow.completed (retrieve full lineage)
    NIFI_PROV-->>WF: Complete data lineage report
    WF->>UI: Notifica completamento
    UI-->>U: ✅ Documento pubblicato<br/>Protocollo: 12345/2025
    
    WF->>DASH: Final update<br/>{workflow_id, status: "PUBLISHED",<br/>final_metrics, audit_summary}
    DASH->>DASH: Archive workflow data<br/>Update analytics
    DASH->>DASH: Generate completion report
    
    Note over U,STORAGE: Fase 10: Post-Processing e Analytics
    NIFI_PROV->>NIFI_PROV: Store complete provenance
    NIFI_PROV->>DB: Aggiorna analytics<br/>(tempi medi, success rate)
    NIFI_PROV->>CACHE: Invalida cache stale
    NIFI_PROV->>DASH: Send analytics events
    
    DASH->>DASH: Update KPI dashboards<br/>- Processing time trends<br/>- Success rate by doc type<br/>- AI confidence distribution<br/>- Human intervention rate
    
    rect rgb(200, 255, 200)
        Note over U: WORKFLOW COMPLETATO<br/>Tempo totale: ~25 secondi<br/>Intervento umano: 4 checkpoint HITL<br/>Dashboard: Metriche archiviate<br/>NiFi Provenance: Full data lineage tracciato
    end
```

## Data Flow Dettagliato

### Payload Example: Document Generation Request

```json
{
  "workflow_id": "WF-12345",
  "document_type": "DELIBERA_GIUNTA",
  "metadata": {
    "oggetto": "Approvazione Piano Urbanistico Zona Industriale",
    "proponente": "Assessorato Urbanistica",
    "responsabile_procedimento": "ing. Mario Rossi",
    "importo": 150000.00,
    "cig": "Z1234567890",
    "normativa_riferimento": ["L.R. 12/2005", "D.Lgs 42/2004"],
    "scadenza": "2025-12-31"
  },
  "allegati": [
    {"nome": "planimetria.pdf", "size": 2048576, "hash": "sha256:abc123..."},
    {"nome": "relazione_tecnica.pdf", "size": 512000, "hash": "sha256:def456..."}
  ],
  "user_context": {
    "user_id": "user_123",
    "role": "RESPONSABILE_UFFICIO",
    "permissions": ["CREATE_DELIBERA", "APPROVE_DELIBERA"]
  }
}
```

### Response Example: Classificazione (SP07 - Content Classifier)

```json
{
  "classification": {
    "document_type": "DELIBERA_GIUNTA",
    "category": "URBANISTICA",
    "subcategory": "PIANI_REGOLATORI",
    "confidence": 0.94
  },
  "metadata_extracted": {
    "date_mentions": ["2025-12-31"],
    "importi": [150000.00],
    "riferimenti_normativi": [
      {"tipo": "LEGGE_REGIONALE", "numero": "12/2005"},
      {"tipo": "DECRETO_LEGISLATIVO", "numero": "42/2004"}
    ],
    "entita": [
      {"tipo": "PERSONA", "nome": "Mario Rossi", "ruolo": "Responsabile Procedimento"},
      {"tipo": "ENTE", "nome": "Assessorato Urbanistica"}
    ],
    "cig": "Z1234567890"
  },
  "similarity_scores": [
    {"doc_id": "DOC-98765", "similarity": 0.87, "tipo": "DELIBERA_GIUNTA"},
    {"doc_id": "DOC-54321", "similarity": 0.82, "tipo": "DELIBERA_GIUNTA"}
  ],
  "processing_time_ms": 450
}
```

### Response Example: Knowledge Base (SP04)

```json
{
  "legal_context": {
    "normativa_principale": [
      {
        "riferimento": "L. 241/1990",
        "articolo": "Art. 5",
        "testo": "Il responsabile del procedimento...",
        "rilevanza": 0.95
      },
      {
        "riferimento": "D.Lgs 42/2004",
        "articolo": "Art. 146",
        "testo": "Autorizzazione paesaggistica...",
        "rilevanza": 0.89
      }
    ],
    "giurisprudenza": [
      {
        "fonte": "Consiglio di Stato",
        "sentenza": "n. 1234/2024",
        "massima": "In materia di piani urbanistici...",
        "rilevanza": 0.78
      }
    ],
    "precedenti_simili": [
      {
        "doc_id": "DELIB-2024-0123",
        "oggetto": "Piano Urbanistico Zona Artigianale",
        "similarity": 0.84,
        "esito": "APPROVATA"
      }
    ]
  },
  "knowledge_graph_path": [
    "L.R. 12/2005 -> modifica -> L.R. 3/1999",
    "D.Lgs 42/2004 -> rimanda -> Codice Beni Culturali"
  ],
  "rag_synthesis": "Per l'approvazione del Piano Urbanistico è necessario rispettare...",
  "confidence_score": 0.91,
  "processing_time_ms": 1200
}
```

### Response Example: Template Generation (SP05)

```json
{
  "document_draft": {
    "format": "XML",
    "content": "<delibera>...</delibera>",
    "sections": [
      {"id": "premesse", "tokens": 245, "status": "generated"},
      {"id": "motivazioni", "tokens": 487, "status": "generated"},
      {"id": "dispositivo", "tokens": 156, "status": "generated"},
      {"id": "allegati", "tokens": 89, "status": "referenced"}
    ]
  },
  "generation_metadata": {
    "model_used": "gpt-4-turbo",
    "temperature": 0.3,
    "tokens_consumed": 1234,
    "api_cost_euros": 0.0148,
    "generation_time_sec": 2.3
  },
  "template_info": {
    "template_id": "TPL-DELIB-URB-001",
    "version": "2.1.4",
    "last_updated": "2025-09-15",
    "variables_filled": 23,
    "variables_total": 25
  },
  "warnings": [
    "Campo 'data_approvazione_preventiva' non valorizzato - da verificare"
  ]
}
```

### Response Example: Validation (SP06)

```json
{
  "validation_result": {
    "status": "WARNING",
    "overall_score": 0.87,
    "timestamp": "2025-10-08T10:25:33Z"
  },
  "critical_issues": [],
  "warnings": [
    {
      "severity": "MEDIUM",
      "category": "METADATA_MISSING",
      "field": "cig",
      "message": "CIG obbligatorio per importi > €40.000",
      "suggestion": "Inserire CIG da ANAC",
      "auto_fixable": false
    }
  ],
  "conformity_checks": [
    {
      "rule": "PRESENZA_RESPONSABILE_PROCEDIMENTO",
      "status": "PASS",
      "normativa_ref": "L. 241/1990 Art. 5"
    },
    {
      "rule": "FORMATO_DATA_VALIDO",
      "status": "PASS"
    },
    {
      "rule": "RIFERIMENTI_NORMATIVI_VIGENTI",
      "status": "PASS",
      "details": "Tutte le norme citate sono in vigore"
    }
  ],
  "semantic_analysis": {
    "coherence_score": 0.92,
    "completeness_score": 0.89,
    "legal_consistency_score": 0.95
  },
  "suggestions": [
    "Aggiungere riferimento a delibera precedente n. 45/2024 per contesto",
    "Specificare tempistiche attuazione nel dispositivo"
  ],
  "processing_time_ms": 780
}
```

### Response Example: Quality Check (SP08)

```json
{
  "quality_report": {
    "overall_quality": "GOOD",
    "score": 82,
    "timestamp": "2025-10-08T10:26:15Z"
  },
  "grammar_check": {
    "errors_found": 3,
    "errors": [
      {
        "position": {"line": 23, "char": 145},
        "type": "AGREEMENT",
        "original": "i documentazione",
        "suggestion": "la documentazione",
        "rule_id": "IT_AGREEMENT_1"
      }
    ]
  },
  "style_check": {
    "warnings": 5,
    "issues": [
      {
        "type": "PASSIVE_VOICE",
        "severity": "LOW",
        "position": {"line": 34},
        "suggestion": "Preferire forma attiva per chiarezza"
      }
    ]
  },
  "readability": {
    "gulpease_index": 62,
    "interpretation": "Testo difficile - livello universitario",
    "avg_sentence_length": 28.5,
    "avg_word_length": 5.2,
    "passive_voice_ratio": 0.23
  },
  "terminology": {
    "technical_terms_count": 45,
    "consistency_score": 0.94,
    "unknown_terms": []
  },
  "corrections_applied": 0,
  "corrections_suggested": 8,
  "processing_time_ms": 320
}
```

### Audit Trail Example (SP11 - Security & Audit)

```json
{
  "audit_record": {
    "workflow_id": "WF-12345",
    "document_id": "DOC-67890",
    "audit_trail_id": "AUDIT-98765",
    "blockchain_hash": "0x1234567890abcdef...",
    "timestamp": "2025-10-08T10:30:45Z"
  },
  "actions_log": [
    {
      "seq": 1,
      "timestamp": "2025-10-08T10:20:00Z",
      "action": "WORKFLOW_INITIATED",
      "user_id": "user_123",
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0..."
    },
    {
      "seq": 2,
      "timestamp": "2025-10-08T10:20:05Z",
      "action": "DOCUMENT_CLASSIFIED",
      "service": "SP07",
      "confidence": 0.94,
      "processing_time_ms": 450
    },
    {
      "seq": 3,
      "timestamp": "2025-10-08T10:20:12Z",
      "action": "LEGAL_CONTEXT_RETRIEVED",
      "service": "SP04",
      "normativa_refs": ["L.241/1990", "D.Lgs 42/2004"],
      "processing_time_ms": 1200
    },
    {
      "seq": 4,
      "timestamp": "2025-10-08T10:22:35Z",
      "action": "TEMPLATE_GENERATED",
      "service": "SP05",
      "model": "gpt-4-turbo",
      "tokens_used": 1234,
      "api_cost_euros": 0.0148
    },
    {
      "seq": 5,
      "timestamp": "2025-10-08T10:25:33Z",
      "action": "DOCUMENT_VALIDATED",
      "service": "SP06",
      "validation_status": "WARNING",
      "warnings_count": 1
    },
    {
      "seq": 6,
      "timestamp": "2025-10-08T10:26:15Z",
      "action": "QUALITY_CHECKED",
      "service": "SP08",
      "quality_score": 82,
      "corrections_suggested": 8
    },
    {
      "seq": 7,
      "timestamp": "2025-10-08T10:28:00Z",
      "action": "HUMAN_APPROVED",
      "user_id": "user_123",
      "approval_level": "RESPONSABILE_UFFICIO",
      "signature": "BASE64_ENCODED_SIGNATURE"
    },
    {
      "seq": 8,
      "timestamp": "2025-10-08T10:29:15Z",
      "action": "PROTOCOLLED",
      "system": "PROTOCOLLO",
      "protocol_number": "12345/2025"
    },
    {
      "seq": 9,
      "timestamp": "2025-10-08T10:30:30Z",
      "action": "DIGITALLY_SIGNED",
      "system": "FIRMA_DIGITALE",
      "signer": "ing. Mario Rossi",
      "timestamp_authority": "InfoCert"
    },
    {
      "seq": 10,
      "timestamp": "2025-10-08T10:30:45Z",
      "action": "WORKFLOW_COMPLETED",
      "final_status": "PUBLISHED",
      "total_duration_sec": 645
    }
  ],
  "gdpr_compliance": {
    "purpose": "GENERAZIONE_ATTO_AMMINISTRATIVO",
    "legal_basis": "Art. 6(1)(e) GDPR - public interest",
    "data_subjects": ["Mario Rossi"],
    "retention_period": "10 years",
    "right_to_explanation": true,
    "automated_decision": true,
    "human_oversight": true
  },
  "security_events": [],
  "anomalies_detected": 0
}
```

## Performance Metrics

| Fase | Tempo Medio | Timeout | SLA |
|------|-------------|---------|-----|
| Email Parsing (SP01) | 800ms | 3s | 95% <2s |
| Document Extraction (SP02) | 2.5s | 10s | 90% <5s |
| Procedural Classification (SP03) | 520ms | 3s | 95% <2s |
| Knowledge Retrieval (SP04) | 1.2s | 5s | 90% <3s |
| Template Generation (SP05) | 2.3s | 10s | 90% <5s |
| Validation (SP06) | 780ms | 5s | 95% <2s |
| Content Classification (SP07) | 450ms | 2s | 95% <1s |
| Quality Check (SP08) | 320ms | 3s | 95% <1s |
| **Total End-to-End** | **~44s** | **90s** | **85% <60s** |

## Error Handling e Retry Logic

```mermaid
graph TD
    A[Servizio Chiamato] --> B{Risposta OK?}
    B -->|200 OK| C[Procedi]
    B -->|4xx Client Error| D[Log + Notifica Utente]
    B -->|5xx Server Error| E{Retry Count < 3?}
    E -->|Sì| F[Exponential Backoff]
    F --> G[Wait 2^n secondi]
    G --> A
    E -->|No| H[Circuit Breaker OPEN]
    H --> I[Fallback Strategy]
    I --> J{Fallback Possibile?}
    J -->|Sì| K[Usa Fallback]
    J -->|No| L[Fail Workflow]
    L --> M[Notifica Admin]
    
    style B fill:#e1f5ff
    style H fill:#f8d7da
    style C fill:#d4edda
```

## Caching Strategy

| Layer | Cache Type | TTL | Invalidazione |
|-------|-----------|-----|---------------|
| Email Parsing (SP01) | Redis | 1 ora | On new email version |
| Document Extraction (SP02) | Redis | 24 ore | On document update |
| Procedural Classification (SP03) | Redis | 2 ore | On document update |
| Normativa (SP04) | Redis | 24 ore | On legislative change |
| Template base (SP05) | Redis | 7 giorni | On template version update |
| Content Classification (SP07) | Redis | 1 ora | On document update |
| Quality rules (SP08) | Redis | 30 giorni | Manual purge |
| User sessions | Redis | 30 min | On logout |

## Scalability Patterns

- **SP01 EML Parser**: Async parsing con message queue per email batch
- **SP02 Document Extractor**: GPU-accelerated OCR con parallel processing
- **SP03 Procedural Classifier**: Caching procedimenti ricorrenti (43% hit rate)
- **SP04 Knowledge Base**: Read replicas per high-throughput queries
- **SP05 Template Engine**: Queue-based generation con Celery worker pool
- **SP06 Validator**: Parallel validation di sezioni indipendenti
- **SP07 Content Classifier**: Batch processing per upload massivi (100+ documenti)
- **SP08 Quality Checker**: Distributed processing con load balancing
- **NiFi FlowFiles**: Routing per `document_type` (load balancing con RouteOnAttribute)
