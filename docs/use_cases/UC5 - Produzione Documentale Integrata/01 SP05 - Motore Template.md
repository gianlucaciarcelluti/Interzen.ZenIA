# SP05 - Template Engine

## Generazione Template con AI

Questo diagramma mostra tutte le interazioni del **Template Engine (SP05)** nel processo di generazione degli atti amministrativi.

```mermaid
sequenceDiagram
    autonumber
    participant WF as Apache NiFi Workflow Orchestrator
    participant TPL as SP05 Template Engine
    participant CACHE as Redis Cache
    participant DB as PostgreSQL
    participant STORAGE as MinIO Storage
    participant NIFI_PROV as NiFi Provenance (Data Lineage)
    participant DASH as SP10 Dashboard
    
    Note over WF,DASH: Fase 4: Generazione Template con AI
    
    WF->>TPL: POST /generate<br/>{doc_type, metadata, legal_context}
    
    TPL->>CACHE: Check template cache
    
    alt Template da generare
        TPL->>DB: Load Jinja2 base template<br/>per tipo documento
        
        TPL->>TPL: GPT-4/Claude prompt engineering<br/>+ injection metadata + normativa
        
        TPL->>TPL: LangChain orchestration<br/>multi-step generation
        
        TPL->>STORAGE: Fetch firma digitale template
        
        TPL->>TPL: Compile template Jinja2<br/>con dati strutturati
    end
    
    TPL-->>WF: {document_draft: "XML/HTML",<br/>sections_generated: 12,<br/>generation_time: 2.3s}
    
    WF->>NIFI_PROV: Log provenance event<br/>DOCUMENT_GENERATED
    
    WF->>DB: Update workflow<br/>status: DRAFT_GENERATED
    
    WF->>STORAGE: Save draft version v0.1
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "DRAFT_GENERATED",<br/>template_data, generation_metrics}
    
    DASH->>DASH: Visualize AI decision path<br/>Show SHAP values
    
    Note over WF,DASH: Raffinamento Qualità (se necessario)
    
    alt Qualità Insufficiente (da SP08)
        WF->>TPL: POST /refine<br/>{document, quality_issues}
        
        TPL->>TPL: LLM refinement con feedback
        
        TPL-->>WF: {document_refined}
        
        WF->>STORAGE: Save refined version
    end
    
    rect rgb(200, 255, 200)
        Note over TPL: Template Engine<br/>Tempo medio: 2.3s<br/>SLA: 90% < 5s<br/>Cache TTL: 7 giorni
    end
```

## Payload Example: Template Generation Request

```json
{
  "doc_type": "DELIBERA_GIUNTA",
  "metadata": {
    "oggetto": "Approvazione Piano Urbanistico Zona Industriale",
    "proponente": "Assessorato Urbanistica",
    "responsabile_procedimento": "ing. Mario Rossi",
    "importo": 150000.00,
    "cig": "Z1234567890",
    "normativa_riferimento": ["L.R. 12/2005", "D.Lgs 42/2004"],
    "scadenza": "2025-12-31"
  },
  "legal_context": {
    "normativa_principale": [
      {
        "riferimento": "L. 241/1990",
        "articolo": "Art. 5",
        "testo": "Il responsabile del procedimento..."
      }
    ],
    "rag_synthesis": "Per l'approvazione del Piano Urbanistico è necessario rispettare..."
  }
}
```

## Response Example: Template Generated

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
## 🏛️ Conformità Normativa - SP05

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP05 (Template Engine)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62

**UC Appartenance**: UC5

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP05 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 6. Monitoraggio Conformità

**Schedule di Review**:
- **Trimestrale**: Compliance assessment + security audit
- **Semestrale**: Framework alignment review (CAD/GDPR/eIDAS/AGID)
- **Annuale**: Full compliance audit + risk assessment

**KPI Conformità**:
- Audit trail completeness: 100%
- Incident response time: <24h
- Compliance violations: 0 per quarter
- Certificate expiry (if eIDAS): Alert at 30 days

**Escalation**: Non-conformità → Compliance Manager → CTO → Legal

**Prossima review programmata**: 2026-02-17

---

## Riepilogo Conformità SP05

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsible |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ❌ No | N/A | - |
| eIDAS | ❌ No | N/A | - |
| AGID | ❌ No | N/A | - |

**Key Compliance Points**:
1. All CAD articles implemented
2. Data handling compliant with applicable regulations
3. Security controls in place (encryption, access control, audit logging)
4. Regular monitoring and review schedule established
5. Clear responsibility assignments (RACI)

**Next Review**: 2026-02-17

---



### Framework Normativi Applicabili

☑ CAD
☑ GDPR
☐ L. 241/1990 - Procedimento Amministrativo
☐ eIDAS - Regolamento 2014/910
☐ AI Act - Regolamento 2024/1689
☐ D.Lgs 42/2004 - Codice Beni Culturali
☐ D.Lgs 152/2006 - Codice dell'Ambiente
☐ D.Lgs 33/2013 - Decreto Trasparenza

**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
| CAD | Art. 1, Art. 21, Art. 22, Art. 62 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| GDPR | Art. 5, Art. 32 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP05

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP05 (Template Engine)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62

**UC Appartenance**: UC5

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP05 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 6. Monitoraggio Conformità

**Schedule di Review**:
- **Trimestrale**: Compliance assessment + security audit
- **Semestrale**: Framework alignment review (CAD/GDPR/eIDAS/AGID)
- **Annuale**: Full compliance audit + risk assessment

**KPI Conformità**:
- Audit trail completeness: 100%
- Incident response time: <24h
- Compliance violations: 0 per quarter
- Certificate expiry (if eIDAS): Alert at 30 days

**Escalation**: Non-conformità → Compliance Manager → CTO → Legal

**Prossima review programmata**: 2026-02-17

---

## Riepilogo Conformità SP05

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsible |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ❌ No | N/A | - |
| eIDAS | ❌ No | N/A | - |
| AGID | ❌ No | N/A | - |

**Key Compliance Points**:
1. All CAD articles implemented
2. Data handling compliant with applicable regulations
3. Security controls in place (encryption, access control, audit logging)
4. Regular monitoring and review schedule established
5. Clear responsibility assignments (RACI)

**Next Review**: 2026-02-17

---



---


## Funzionalità Chiave SP05

### Capacità AI
- **Prompt Engineering**: Ottimizzazione prompt per GPT-4/Claude
- **LangChain Orchestration**: Gestione multi-step generation
- **Template Jinja2**: Compilazione dinamica con variabili
- **Metadata Injection**: Integrazione automatica dati strutturati
- **Normativa Integration**: Inserimento riferimenti legislativi

### Performance
- **Tempo medio**: 2.3 secondi
- **SLA target**: 90% < 5 secondi
- **Cache Redis**: TTL 7 giorni per template base
- **Scalability**: Queue-based con Celery worker pool

### Tecnologie
- **AI Models**: GPT-4-turbo, Claude
- **Orchestration**: LangChain
- **Template Engine**: Jinja2
- **Storage**: MinIO per template e firme digitali
- **Cache**: Redis per template frequenti
