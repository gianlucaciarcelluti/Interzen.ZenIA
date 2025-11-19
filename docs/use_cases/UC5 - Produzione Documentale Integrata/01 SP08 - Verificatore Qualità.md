# SP08 - Quality Checker

## Quality Check Linguistico

Questo diagramma mostra tutte le interazioni del **Quality Checker (SP08)** nel processo di controllo qualità degli atti amministrativi.

```mermaid
sequenceDiagram
    autonumber
    participant WF as SP09 Workflow Engine
    participant QC as SP08 Quality Checker
    participant TPL as SP05 Template Engine
    participant NIFI_PROV as NiFi Provenance (Data Lineage)
    participant DB as PostgreSQL
    participant STORAGE as MinIO Storage
    participant DASH as SP10 Dashboard
    
    Note over WF,DASH: Fase 6: Quality Check Linguistico
    
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
        
        WF->>QC: POST /check-quality<br/>{document_refined}
        
        Note over WF,QC: Retry quality check
    end
    
    WF->>NIFI_PROV: Log provenance event<br/>QUALITY_CHECKED
    
    WF->>DB: Update workflow<br/>status: QUALITY_APPROVED
    
    WF->>STORAGE: Save final version v1.0
    
    WF->>DASH: Update dashboard<br/>{workflow_id, status: "QUALITY_APPROVED",<br/>quality_metrics}
    
    DASH->>DASH: Show quality scores<br/>Grammar/style report
    
    rect rgb(200, 255, 200)
        Note over QC: Quality Checker<br/>Tempo medio: 320ms<br/>SLA: 95% < 1s<br/>LanguageTool + spaCy
    end
```

## Payload Example: Quality Check Request

```json
{
  "document_validated": {
    "format": "XML",
    "content": "<delibera><premesse>Vista la richiesta...</premesse><motivazioni>Considerato che i documentazione...</motivazioni><dispositivo>DELIBERA...</dispositivo></delibera>",
    "doc_type": "DELIBERA_GIUNTA"
  },
  "quality_level": "STANDARD"
}
```

## Response Example: Quality Report

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
      },
      {
        "position": {"line": 45, "char": 78},
        "type": "SPELLING",
        "original": "urbanistco",
        "suggestion": "urbanistico",
        "rule_id": "IT_SPELLING"
      },
      {
        "position": {"line": 67, "char": 234},
        "type": "PUNCTUATION",
        "original": "approvazione,in merito",
        "suggestion": "approvazione, in merito",
        "rule_id": "IT_SPACING"
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
        "sentence": "Il piano viene approvato dalla Giunta",
        "suggestion": "Preferire forma attiva: La Giunta approva il piano"
      },
      {
        "type": "LONG_SENTENCE",
        "severity": "MEDIUM",
        "position": {"line": 56},
        "words": 42,
        "suggestion": "Spezzare in frasi più brevi per migliorare leggibilità"
      },
      {
        "type": "REDUNDANCY",
        "severity": "LOW",
        "position": {"line": 78},
        "phrase": "assolutamente necessario",
        "suggestion": "Rimuovere 'assolutamente' (pleonasmo)"
      }
    ]
  },
  "readability": {
    "gulpease_index": 62,
    "interpretation": "Testo difficile - livello universitario",
    "avg_sentence_length": 28.5,
    "avg_word_length": 5.2,
    "passive_voice_ratio": 0.23,
    "recommendation": "OK per atti amministrativi (target: 55-65)"
  },
  "terminology": {
    "technical_terms_count": 45,
    "consistency_score": 0.94,
    "unknown_terms": [],
    "terminologia_issues": [
      {
        "term": "PUC",
        "first_use_line": 12,
        "issue": "Acronimo non esplicitato alla prima occorrenza",
        "suggestion": "Piano Urbanistico Comunale (PUC)"
      }
    ]
  },
  "corrections_applied": 0,
  "corrections_suggested": 8,
  "processing_time_ms": 320
}
```
## 🏛️ Conformità Normativa

### Framework Normativi Applicabili

☑ CAD
☑ AI Act
☐ L. 241/1990 - Procedimento Amministrativo
☐ GDPR - Regolamento 2016/679
☐ eIDAS - Regolamento 2014/910
☐ D.Lgs 42/2004 - Codice Beni Culturali
☐ D.Lgs 152/2006 - Codice dell'Ambiente
☐ D.Lgs 33/2013 - Decreto Trasparenza

**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
| CAD | Art. 1, Art. 21, Art. 22, Art. 62 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| AI Act | Art. 6, Art. 13, Art. 22 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa" del template standard.

---


## Funzionalità Chiave SP08

### Tipi di Controllo

#### 1. Grammar Check (LanguageTool)
- **Grammatica**: Concordanze, tempi verbali, pronomi
- **Ortografia**: Errori di battitura, spelling
- **Punteggiatura**: Virgole, punti, spaziatura
- **Regole IT**: ~2.000 regole specifiche italiano

#### 2. Style Analysis (spaCy + Custom)
- **Passive voice**: Rilevamento e suggerimento forma attiva
- **Sentence length**: Frasi troppo lunghe (>35 parole)
- **Redundancy**: Pleonasmi e ripetizioni
- **Clarity**: Ambiguità e oscurità
- **Tone**: Adeguatezza registro formale

#### 3. Readability (Gulpease)
Formula: `89 + (300 * frasi - 10 * lettere) / parole`

| Score | Interpretazione | Target |
|-------|-----------------|--------|
| 80-100 | Molto facile - elementari | - |
| 60-80 | Facile - medie | - |
| 40-60 | Difficile - superiori | - |
| **55-65** | **Difficile - universitario** | **✅ Atti amministrativi** |
| 0-40 | Molto difficile | - |

#### 4. Terminology Check
- **Consistency**: Uso uniforme dei termini
- **Acronimi**: Prima occorrenza esplicitata
- **Technical terms**: Glossario amministrativo
- **Legal terms**: Terminologia giuridica corretta

### Livelli di Qualità

| Livello | Score | Azione |
|---------|-------|--------|
| EXCELLENT | 90-100 | Auto-approval |
| GOOD | 75-89 | Auto-approval con note |
| ACCEPTABLE | 60-74 | Review + suggerimenti |
| POOR | <60 | LLM refinement obbligatorio |

### Auto-Correction vs Suggestion

#### Auto-Correction (se enabled)
- Spelling semplici
- Spaziatura punteggiatura
- Maiuscole/minuscole ovvie

#### Suggestion Only
- Passive voice
- Long sentences
- Redundancy
- Terminology

### Performance

- **Tempo medio**: 320ms
- **SLA target**: 95% < 1 secondo
- **Concurrent checks**: Max 20
- **Cache**: Quality rules in Redis (TTL: 30 giorni)

### Integration con SP01

Quando quality score < 60:
1. WF invoca SP01 per refinement
2. SP01 usa feedback specifici per migliorare
3. Loop max 2 iterazioni
4. Se ancora insufficiente → human review

### Custom Rules per PA

Regole specifiche per atti amministrativi:
- **Formule standard**: "Visto", "Richiamato", "Considerato"
- **Struttura**: Premesse → Motivazioni → Dispositivo
- **Date**: Formato italiano (gg/mm/aaaa)
- **Importi**: Euro con 2 decimali
- **Protocolli**: Formato standardizzato

### Tecnologie

- **Grammar**: LanguageTool (IT rules)
- **NLP**: spaCy (it_core_news_lg)
- **Readability**: Gulpease algorithm
- **Custom**: Python regex + glossari
- **Cache**: Redis per regole (30 giorni)
