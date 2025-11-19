# SP17 - Registry Suggester (Classification & Registry Assignment)

## Descrizione Componente

Lo **SP17 Registry Suggester** è il componente intelligente che suggerisce la corretta classificazione in titolario/registro amministrativo (numero di registro, categoria, settore) sulla base della corrispondenza ricevuta e già classificata.

Implementa logiche di matching semantico tra il contenuto della corrispondenza e i registri/titolari dell'Ente per proporre automaticamente la categoria più appropriata, riducendo errori di catalogazione e accelerando il processo di protocollazione.

## Responsabilità Principali

1. **Registry Knowledge Management**
   - Mantenimento catalogo titolari/registri dell'Ente
   - Gestione versioni titolario (evoluzione nel tempo)
   - Mappatura procedure alle categorie di registro
   - Support per registri multipli (uno per settore/area)

2. **Intelligent Matching**
   - Analisi semantica corrispondenza vs. registri disponibili
   - Suggerimenti top-N con confidence scores
   - Feedback loop per apprendimento da assegnazioni manuali
   - Handling ambiguità (multi-category fit)

3. **Registry Assignment**
   - Proposta numero di registro (auto-increment)
   - Assegnazione categoria principale + secondaria (optional)
   - Tracking meta-storico assegnazioni
   - Support per override manuale con giustificazione

4. **Compliance & Audit**
   - Validazione assegnazione vs. norme (CAD/AGID)
   - Audit trail decisioni assegnazione
   - Compliance reporting su distribuzione registri
   - Historical tracking per statistiche

## Input/Output

### Input
| Nome | Tipo | Fonte | Formato | Note |
|---|---|---|---|---|
| **Classified Email** | Email metadata + classification | SP16 | JSON | Da Correspondence Classifier |
| **Email Content** | Testo email, allegati | SP01 | Text/Binary | Per analisi semantica |
| **Registry Database** | Titolario/registro definitions | MS06 KB | JSONB | Elenco categorie valide |
| **Historical Assignments** | Assegnazioni passate | PostgreSQL | Log | Per machine learning |
| **Compliance Rules** | Regole vincolanti | Configuration | YAML | Vincoli CAD/AGID |

### Output
| Nome | Tipo | Destinazione | Formato | Note |
|---|---|---|---|---|
| **Registry Suggestions** | Ranked proposals | SP19 Orchestrator | JSON | Top-3 suggestions with scores |
| **Registry Assignment** | Assigned category | Archive/Protocol | JSON | Accepted assignment |
| **Assignment Audit** | Audit event | SP11 Audit | JSON | Chi, cosa, quando assegnato |
| **Registry Analytics** | Usage statistics | SP10 Dashboard | JSON | Distribution per category |

## Dipendenze

### Upstream (Cosa richiede)
```
SP16 (Correspondence Classifier) → SP17
  Data: Correspondence type, confidence, metadata
  Timing: Real-time (after classification)
  SLA: Suggestion < 2 sec

SP01 (EML Parser) → SP17
  Data: Email content, subject, sender, attachments
  Timing: On parsing completion
  SLA: < 2 sec processing
```

### Downstream (Cosa fornisce)
```
SP17 → SP19 (Protocol Workflow Orchestrator)
  Data: Registry assignment recommendation
  Timing: Real-time for auto-assignment, or on-demand
  SLA: < 2 sec suggestion

SP17 → SP10 (Dashboard)
  Data: Registry statistics, usage distribution
  Timing: Daily/weekly aggregation
  SLA: < 1 sec query

SP17 → Audit Trail
  Data: Assignment decisions + confidence
  Timing: Immediate logging
  SLA: < 100ms async
```

## Architettura Tecnica

```
Classified Email (from SP16)
  ↓
┌──────────────────────────────────────────┐
│      SP17 Registry Suggester             │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ Registry Knowledge Layer         │   │
│  │ - Titolario index               │   │
│  │ - Procedure mappings            │   │
│  │ - Versioning system             │   │
│  └──────────────────────────────────┘   │
│               ↓                          │
│  ┌──────────────────────────────────┐   │
│  │ Semantic Matching Engine         │   │
│  │ - NLP-based similarity           │   │
│  │ - ML classifier (SVM/Gradient)   │   │
│  │ - BM25 full-text fallback       │   │
│  │ - Confidence scoring             │   │
│  └──────────────────────────────────┘   │
│               ↓                          │
│  ┌──────────────────────────────────┐   │
│  │ Suggestion Ranking & Filter      │   │
│  │ - Top-N selection                │   │
│  │ - Threshold filtering            │   │
│  │ - Conflict resolution            │   │
│  │ - Manual override support        │   │
│  └──────────────────────────────────┘   │
│               ↓                          │
│  ┌──────────────────────────────────┐   │
│  │ Assignment & Audit               │   │
│  │ - Register assignment            │   │
│  │ - Immutable log                  │   │
│  │ - Feedback collection            │   │
│  └──────────────────────────────────┘   │
└──────────────────────────────────────────┘
  ↓
Registry Assignment (to SP19, Archive)
```

## Stack Tecnologico

| Componente | Tecnologia | Versione | Scopo |
|-----------|-----------|----------|-------|
| Language | Python | 3.11 | Core engine |
| API | FastAPI | 0.104+ | REST endpoints |
| ML | Scikit-learn + Mistral | Latest | Semantic matching |
| NLP | spaCy | 3.7+ | Text processing |
| Database | PostgreSQL | 15+ | Registry storage |
| Search | Elasticsearch | 8.10+ | Full-text fallback |
| Cache | Redis | 7.2+ | Classifier cache |

## API Endpoints

**POST /api/v1/registry/suggest**

Request:
```json
{
  "email_id": "msg_456",
  "correspondence_type": "istanza",
  "confidence_type": 0.92,
  "subject": "Richiesta accesso documenti amministrativi",
  "content_summary": "Richiesta di accesso ai documenti della gara....",
  "sender_department": "cittadino",
  "top_n": 5
}
```

Response:
```json
{
  "email_id": "msg_456",
  "suggestions": [
    {
      "rank": 1,
      "registry_category": "Appalti e Gare",
      "registry_code": "RG.03.01",
      "confidence": 0.94,
      "recommendation": "auto_assign"
    },
    {
      "rank": 2,
      "registry_category": "Accesso Civico",
      "registry_code": "RG.07.02",
      "confidence": 0.78,
      "recommendation": "secondary"
    },
    {
      "rank": 3,
      "registry_category": "Trasparenza",
      "registry_code": "RG.07.01",
      "confidence": 0.65,
      "recommendation": "fallback"
    }
  ],
  "auto_assign": true,
  "assigned_category": "RG.03.01",
  "assigned_number": "PT-2025-001234",
  "suggestion_timestamp": "2025-11-17T10:30:25Z"
}
```

**POST /api/v1/registry/assign**

Request:
```json
{
  "email_id": "msg_456",
  "assigned_category": "RG.03.01",
  "assigned_manually": false,
  "justification": null
}
```

Response:
```json
{
  "registry_number": "PT-2025-001234",
  "category": "RG.03.01",
  "assigned_at": "2025-11-17T10:30:30Z",
  "assigned_by": "system",
  "status": "active"
}
```

**GET /api/v1/registry/categories**
```
Response:
{
  "categories": [
    {
      "code": "RG.01.01",
      "name": "Delibere Giunta",
      "procedures": ["procedure_123", "procedure_124"]
    },
    ...
  ]
}
```

## Database Schema

```sql
CREATE TABLE registry_categories (
  id SERIAL PRIMARY KEY,
  category_code VARCHAR(50) UNIQUE,
  category_name VARCHAR(255),
  description TEXT,
  parent_category VARCHAR(50),
  active BOOLEAN DEFAULT true,
  version INT DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ,
  INDEX idx_code (category_code),
  INDEX idx_active (active)
);

CREATE TABLE registry_mappings (
  id SERIAL PRIMARY KEY,
  email_id VARCHAR(255),
  correspondence_type VARCHAR(100),
  suggested_category VARCHAR(50),
  suggested_confidence DECIMAL(3,2),
  assigned_category VARCHAR(50),
  assigned_by VARCHAR(255),
  assigned_at TIMESTAMPTZ,
  was_manual BOOLEAN,
  justification TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  INDEX idx_email_id (email_id),
  INDEX idx_assigned_category (assigned_category),
  INDEX idx_assigned_at (assigned_at DESC)
);

CREATE TABLE registry_suggestion_feedback (
  id SERIAL PRIMARY KEY,
  email_id VARCHAR(255),
  suggestion_rank INT,
  was_accepted BOOLEAN,
  feedback_type VARCHAR(50),  -- correct, incorrect, ambiguous
  feedback_comment TEXT,
  user_id VARCHAR(255),
  feedback_timestamp TIMESTAMPTZ DEFAULT NOW(),
  INDEX idx_email_id (email_id)
);

CREATE TABLE registry_analytics (
  id SERIAL PRIMARY KEY,
  category_code VARCHAR(50),
  date DATE,
  assignment_count INT,
  auto_assign_rate DECIMAL(3,2),
  manual_override_rate DECIMAL(3,2),
  avg_suggestion_confidence DECIMAL(3,2),
  INDEX idx_category_date (category_code, date DESC)
);
```

## Configurazione (YAML)

```yaml
sp17_registry_suggester:
  registry:
    source: "knowledge_base"
    refresh_interval_hours: 24
    support_multi_category: true

  matching_engine:
    algorithm: "semantic_ml"  # semantic_ml, bm25_fallback, hybrid
    confidence_threshold: 0.70
    top_n_suggestions: 5

    ml_model:
      name: "registry_classifier_v2"
      type: "gradient_boosting"
      retrain_frequency: "weekly"
      feedback_loop: true

  auto_assignment:
    enabled: true
    min_confidence: 0.85
    require_confirmation: false

  audit:
    log_all_suggestions: true
    immutable_log: true
    feedback_tracking: true

  compliance:
    enforce_cad_rules: true
    enforce_agid_rules: true
    validate_category_codes: true
```

## Performance & KPIs

| Metrica | Target |
|---------|--------|
| **Suggestion Latency** | < 2 sec |
| **Accuracy (top-1)** | > 90% |
| **Accuracy (top-3)** | > 95% |
| **Auto-assign Confidence** | > 85% |
| **User Override Rate** | < 10% (indicate good suggestions) |
| **Throughput** | 500 emails/min |
| **Availability** | 99.9% |

## Testing Strategy

- **Unit**: Semantic matching, scoring functions (> 85% coverage)
- **Integration**: Email classification → registry suggestion → assignment
- **E2E**: Full correspondence → protocol assignment workflow
- **ML**: Model accuracy validation, feedback loop testing
- **Load**: 500+ concurrent suggestion requests

## Implementazione Timeline

1. **Phase 1**: Registry knowledge base + BM25 fallback matching
2. **Phase 2**: ML-based semantic classifier
3. **Phase 3**: Feedback loop + continuous learning
4. **Phase 4**: Multi-registry support + advanced analytics

---

**Associato a**: UC2 - Protocollo Informatico
**MS Primario**: MS01 Generic Classifier Engine
**MS Supporto**: MS06 Generic Knowledge Base
**Status**: In Design
**Created**: 2025-11-17
