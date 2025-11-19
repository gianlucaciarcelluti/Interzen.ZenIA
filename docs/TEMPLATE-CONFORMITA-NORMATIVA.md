# Template Standard: Conformità Normativa

## Scopo

Questo template standardizza la sezione **Conformità Normativa** per tutti i 72 SubProjekti (SP). Incorpora:
- **Riferimenti normativi** (CAD, GDPR, eIDAS, AGID)
- **HITL patterns** (Human In The Loop) per decisioni critiche
- **Guardrail** per il contenimento del contesto
- **Mappatura alle responsabilità**

---

## Struttura Standard

### 1. Quadro Normativo di Riferimento

**Scope**: Identificare le normative applicabili a questo SP

**HITL Checkpoint #1 - Completezza Normativa**
- **Trigger**: Durante la progettazione dello SP
- **Cosa presenta il sistema**:
  - Elenco normative rilevate
  - Applicabilità (critica, alta, media, bassa)
  - Confidence score del mapping automatico
- **Azioni disponibili**:
  - ✅ **Conferma**: Normative identificate correttamente
  - ✏️ **Modifica**: Aggiungi/rimuovi/ajusta normative
  - 🔄 **Rifiuta**: Richiedi nuova analisi normativa
- **Tracciamento**:
  ```json
  {
    "hitl_point": "REGULATORY_COMPLETENESS",
    "sp_id": "SP01",
    "ai_suggestion": {
      "normative": ["CAD art. 1-12", "GDPR art. 1-99", "eIDAS artt. rilevanti"],
      "confidence": 0.92
    },
    "user_action": "MODIFIED",
    "user_changes": {
      "added": ["AGID Guidelines v2.0"],
      "removed": [],
      "adjusted": []
    }
  }
  ```

**Guardrail - Contesto Normativo**
- Non citare più di 5 normative principali per SP
- Se applicabili > 5: raggruppare per categoria (Data Protection, Digital Identity, Document Management, etc.)
- Includere solo articoli direttamente rilevanti (max 3 per normativa)

---

### 2. Conformità CAD (Codice Amministrazione Digitale)

**Scope**: Mappare l'SP ai requisiti della PA digitale italiana

**Elementi richiesti**:
- **Articoli CAD applicabili**: Elencare articoli di riferimento (es. art. 1, 13, 22, 64, etc.)
- **Obiettivi CAD supportati**: Quali obiettivi di trasformazione digitale supporta
- **Allineamento AGID**: Conformità ai standard AGID pubblicati
- **Responsabilità**: Chi è responsabile della conformità

**HITL Checkpoint #2 - CAD Compliance**
- **Trigger**: Prima della release dell'SP
- **Cosa presenta il sistema**:
  - Checklist CAD compliance
  - Articoli non ancora mappati
  - Conflitti o gap identificati
- **Azioni disponibili**:
  - ✅ **Approva Compliance**: Tutti i requisiti mappati
  - ✏️ **Modifica Mapping**: Ajusta mappature CAD
  - 🔄 **Richiedi Review Legale**: Escalation per ambiguità legali
- **Tracciamento**:
  ```json
  {
    "hitl_point": "CAD_COMPLIANCE_REVIEW",
    "sp_id": "SP05",
    "compliance_score": 0.98,
    "unmapped_requirements": [],
    "user_action": "APPROVED",
    "approval_notes": "Tutti gli articoli CAD applicabili sono stati correttamente mappati",
    "timestamp": "2025-11-19T15:30:00Z"
  }
  ```

**Guardrail - CAD Compliance**
- Documentare ogni art. CAD in una sola sezione per evitare duplicazioni
- Mapping deve essere bidirezionale: CAD article → SP requirement
- Se più articoli combinati: creare sezione esplicita di integrazione

---

### 3. Conformità GDPR (General Data Protection Regulation)

**Scope**: Gestione dei dati personali nel contesto dell'SP

**Elementi richiesti**:
- **Soggetti coinvolti**: Titolare, Responsabile, Incaricati
- **Dati personali gestiti**: Categorie di dati (ordinari, sensibili, genetici, biometrici, etc.)
- **Base legale**: Art. 6 GDPR - quale base legale giustifica il trattamento
- **Diritti interessati**: Diritto di accesso, rettifica, cancellazione, portabilità, obiezione
- **DPA (Data Protection Impact Assessment)**: Necessaria? Quando? Come integrata?
- **Sicurezza**: Misure tecniche e organizzative per proteggere i dati

**HITL Checkpoint #3 - GDPR Data Protection**
- **Trigger**: Per ogni SP che gestisce dati personali
- **Cosa presenta il sistema**:
  - Elenco dati personali processati
  - GDPR articles interested
  - Risk assessment preliminare
  - Suggerimenti per security controls
- **Azioni disponibili**:
  - ✅ **Approva DPA**: Data Protection Impact Assessment completo e accettato
  - ✏️ **Modifica Dati/Controlli**: Ajusta categorie dati o security controls
  - 🔄 **Richiedi DPA Completo**: Se rischio alto, formal DPA assessment obbligatorio
- **Tracciamento**:
  ```json
  {
    "hitl_point": "GDPR_DATA_PROTECTION",
    "sp_id": "SP07",
    "personal_data": {
      "categories": ["identification_data", "professional_data"],
      "processing": "Classification & Extraction",
      "retention_period": "3_years"
    },
    "gdpr_articles": ["6_processing_lawfulness", "13_transparent_info"],
    "dpa_required": true,
    "user_action": "MODIFIED",
    "user_changes": {
      "added_control": "Encryption at rest (AES-256)",
      "clarified_retention": "3 anni per conformità normativa"
    }
  }
  ```

**Guardrail - GDPR Data Scope**
- Documentare SOLO dati personali; escludere dati anonimizzati
- Per ogni categoria dati: 1 articolo GDPR min, 3 articoli max
- Se rischio alto (art. 35): DPA obbligatorio before implementation
- Security controls devono essere SPECIFICI a questa SP (non generici)

---

### 4. Conformità eIDAS (Electronic IDentification, Authentication and trust Services)

**Scope**: Servizi di firma digitale e identità elettronica

**Elementi richiesti** (applicabili solo per SP con firme digitali):
- **Livelli di Assicurazione Identificazione**: Basso, Sostanziale, Alto (art. 8 eIDAS)
- **Livelli di Assicurazione Autenticazione**: Basso, Sostanziale, Alto (art. 8 eIDAS)
- **Servizi di Fiducia Qualificati**: Se applicabile, quali servizi TSP (Trusted Service Provider) integrati
- **Marcatura Temporale**: RFC 3161 compliance per timestamping
- **Firma Avanzata vs Qualificata**: Quale livello di firma è richiesto
- **Certificati**: Quale CA (Certification Authority) e quale profilo di certificato

**HITL Checkpoint #4 - eIDAS Trust Services**
- **Trigger**: Se SP include firma digitale o identità elettronica
- **Cosa presenta il sistema**:
  - Assurance levels richiesti
  - TSP providers supportati
  - Certificazione chain validation
- **Azioni disponibili**:
  - ✅ **Approva Trust Configuration**: Livelli eIDAS corretti per use case
  - ✏️ **Modifica Trust Level**: Aumenta/diminuisci assurance level
  - 🔄 **Richiedi Certificazione**: Se dubbi su TSP selection
- **Tracciamento**:
  ```json
  {
    "hitl_point": "eIDAS_TRUST_SERVICES",
    "sp_id": "SP29",
    "signature_type": "Qualified Signature",
    "assurance_level": {
      "identification": "HIGH",
      "authentication": "SUBSTANTIAL"
    },
    "tsp_providers": ["Namirial", "Aruba"],
    "timestamp_rfc3161": true,
    "user_action": "CONFIRMED",
    "timestamp": "2025-11-19T16:00:00Z"
  }
  ```

**Guardrail - eIDAS Scope**
- Se NO firma/identità: non includere sezione eIDAS
- Se SI firma: obbligatorio specificare livello assurance (art. 8-9 eIDAS)
- Certificati: solo pubbliche CA attendibili (AGID lista ufficiale)
- Timestamp RFC 3161: obbligatorio per conservazione digitale

---

### 5. Conformità AGID (Agenzia per l'Italia Digitale)

**Scope**: Allineamento alle linee guida e standard AGID

**Elementi richiesti**:
- **Linee Guida Applicabili**: Quali linee guida AGID sono rilevanti (es. LG Acquisizione Software, LG Interoperabilità, etc.)
- **Ontologie e Standard**: Quali ontologie AGID usare (es. NDC - Ontologia Nazionale)
- **Interoperabilità**: Conforme a ModI (Modello di Interoperabilità)
- **Accessibilità**: WCAG 2.1 Level AA compliance (se interfaccia utente)
- **Privacy by Design**: Implementazione dei principi GDPR by design

**HITL Checkpoint #5 - AGID Alignment**
- **Trigger**: Prima della pubblicazione dell'SP
- **Cosa presenta il sistema**:
  - Checklist linee guida AGID
  - Gap analysis verso conformità
  - Best practices recommendations
- **Azioni disponibili**:
  - ✅ **Approva Alignment**: Conforme a linee guida AGID
  - ✏️ **Modifica Specifiche**: Ajusta per allineamento AGID
  - 🔄 **Richiedi AGID Review**: Se dubbi sulla conformità
- **Tracciamento**:
  ```json
  {
    "hitl_point": "AGID_ALIGNMENT",
    "sp_id": "SP12",
    "guidelines_applicable": ["LG Acquisizione Software", "LG Interoperabilità"],
    "accessibility_score": 0.95,
    "ontology_compliance": "NDC COMPLIANT",
    "privacy_by_design": true,
    "user_action": "APPROVED",
    "review_notes": "Conforme a tutti i requisiti AGID applicabili"
  }
  ```

**Guardrail - AGID Scope**
- Citare SOLO linee guida AGID ufficiali (da agid.gov.it)
- Se accessibilità: WCAG 2.1 Level AA è minimum (non AA-AAA per evitare scope creep)
- Interoperabilità: se no-interop requirement, documento esplicitamente "OUT OF SCOPE"

---

## 6. Mappatura di Responsabilità

**Scope**: Chi è responsabile di cosa in materia di conformità

**Elementi richiesti**:

| Aspetto | Responsabile | Tempistica | Verifiche |
|--------|-------------|-----------|-----------|
| Conformità CAD | [Role] | Prima release | AGID/Legal review |
| Conformità GDPR | DPO + [Responsabile SP] | Continuous | DPA, audits annuali |
| Conformità eIDAS | [Security/Legal] | Pre-production | TSP certification |
| Conformità AGID | [Architettura] | Before publication | AGID checklist |
| Compliance Monitoring | [Audit/Security] | Ongoing | Quarterly reports |

**HITL Checkpoint #6 - Responsibility Mapping**
- **Trigger**: Durante allocation di responsabilità nel progetto
- **Cosa presenta il sistema**:
  - RACI matrix preliminare
  - Role/responsible assignment
  - Escalation paths per non-conformità
- **Azioni disponibili**:
  - ✅ **Approva RACI**: Responsabilità assegnate e chiare
  - ✏️ **Modifica Assignments**: Ajusta chi responsabile
  - 🔄 **Richiedi Chiarimento**: Se ambiguità sul responsibility owner
- **Tracciamento**:
  ```json
  {
    "hitl_point": "RESPONSIBILITY_MAPPING",
    "sp_id": "SP42",
    "raci_matrix": {
      "cad_compliance": {"responsible": "mario.rossi", "accountable": "compliance_lead"},
      "gdpr_dpa": {"responsible": "dpo@company.it", "consulted": ["security_team"]},
      "agid_alignment": {"responsible": "arch_team", "informed": ["all_stakeholders"]}
    },
    "user_action": "APPROVED",
    "timestamp": "2025-11-19T17:00:00Z"
  }
  ```

---

## 7. Monitoraggio Conformità Continuo

**Scope**: Come verificare che la conformità sia mantenuta nel tempo

**Elementi richiesti**:
- **KPI di Conformità**: Metriche per misurare conformità
- **Audit Trail**: Registrazione di tutte le modifiche normative
- **Update Normative**: Procedura quando una normativa cambia
- **Incident Management**: Cosa fare se scoperta non-conformità

**HITL Checkpoint #7 - Compliance Monitoring**
- **Trigger**: Trimestralmente o quando normativa cambia
- **Cosa presenta il sistema**:
  - Compliance score attuale
  - Normative aggiornate da quella ultima review
  - Eventuali non-conformità scoperte
- **Azioni disponibili**:
  - ✅ **Approva Mantenimento**: Conformità ancora valida
  - ✏️ **Aggiorna Requisiti**: Normativa è cambiata, ajusta requirements
  - 🔄 **Escalate Non-Conformità**: Se trovati problemi, richiedi remediation
- **Tracciamento**:
  ```json
  {
    "hitl_point": "COMPLIANCE_MONITORING",
    "sp_id": "SP01",
    "review_date": "2025-11-19",
    "compliance_score": 0.98,
    "normative_changes": {
      "new": ["eIDAS 2.0 draft art. 45"],
      "modified": [],
      "obsolete": []
    },
    "non_conformities": [],
    "user_action": "APPROVED",
    "next_review": "2026-02-19"
  }
  ```

---

## 8. Sezione Riepilogo Conformità

Ogni SP deve includere al termine della sezione Conformità Normativa un riepilogo come:

```markdown
## Riepilogo Conformità [SP-ID]

### Status: ✅ COMPLIANT

| Framework | Compliance | Responsible | Last Review |
|-----------|-----------|-------------|------------|
| CAD | ✅ Compliant | [Name] | 2025-11-19 |
| GDPR | ✅ Compliant | DPO | 2025-11-19 |
| eIDAS | N/A | - | - |
| AGID | ✅ Compliant | Arch Team | 2025-11-19 |

**Critical Success Factors**:
- [CSF 1]
- [CSF 2]
- [CSF 3]

**Known Limitations**:
- [Limitation 1]
- [Limitation 2]

**Next Review**: [Date 3 months from now]
```

---

## 9. Guardrail - Contenimento Contesto

Per evitare che la sezione Conformità diventi ingestibile, applicare questi guardrail:

### Lunghezza Massima
- **CAD section**: max 2 KB (200 words)
- **GDPR section**: max 3 KB (300 words) se SP gestisce dati personali
- **eIDAS section**: max 2 KB se firma digitale, N/A altrimenti
- **AGID section**: max 1.5 KB
- **Monitoring section**: max 1 KB
- **Total Conformità section**: max 10 KB per SP

### Struttura Standardizzata
- NO lunghi paragrafi narrativi: usare bullet points
- NO citazioni complete di articoli: solo "art. X" + breve descrizione
- NO copypaste da normative: parafrasare in italiano semplice

### Reusability
- Parti comuni (es. CAD art. 1-10 principi generali): inserire una sola volta, poi link/reference
- Per SP simili (es. SP04, SP05, SP09): permesso condividere sezioni comuni se identiche

### Version Control
- Ogni cambio normativo = nuova versione della Conformità section
- Tracciare chi ha approvato tramite HITL checkpoint
- Mantenere history delle versioni (stored in git history)

---

## 10. Integrazione con GLOSSARIO-TERMINOLOGICO

**Importante**: Usare sempre le definizioni da GLOSSARIO-TERMINOLOGICO.md:

- **Titolare/Responsabile/Incaricato**: Vedi Sezione 11 - Regulatory Terms
- **CAD/GDPR/eIDAS/AGID**: Tutte definite nel Glossario
- **Terminologia tecnica** (encryption, hashing, etc.): Sempre in inglese nel contesto tecnico, italiano nella documentazione

**Validazione**: Prima di merge di qualsiasi SP:
1. Eseguire grep delle definizioni nel Glossario
2. Verificare che terminologia sia coerente con Glossario
3. Se termine mancante nel Glossario: aggiungere prima di merge

---

## Template per Specifiche SP

Usare questa struttura per ogni SP:

```markdown
## Conformità Normativa

### Quadro Normativo di Riferimento
[CAD + GDPR + eIDAS (se applicable) + AGID]

### Conformità CAD
- **Articoli**: [elenco]
- **Obiettivi**: [elenco]
- **Responsabile**: [name]

### Conformità GDPR (se applicable)
- **Dati trattati**: [categorie]
- **Base legale**: Art. 6(1)[lettera]
- **DPA**: [SI/NO/In Progress]
- **Controlli**: [bullet list max 5]
- **Responsabile**: DPO

### Conformità eIDAS (se applicable per firma)
- **Livello**: [Basso/Sostanziale/Alto]
- **TSP**: [provider]
- **Responsabile**: Security Team

### Conformità AGID
- **Linee guida**: [elenco]
- **Accessibilità**: [WCAG 2.1 Level]
- **Responsabile**: Architecture Team

### Monitoraggio
- **Review period**: Trimestrale
- **Last review**: [date]
- **Next review**: [date]
```

---

## Domande per Chiarimento

Prima di applicare il template, answers queste domande su ogni SP:

1. **Gestisce dati personali?** → Se SI: sezione GDPR obbligatoria
2. **Implementa firma digitale?** → Se SI: sezione eIDAS obbligatoria
3. **Ha interfaccia utente?** → Se SI: accessibilità WCAG 2.1
4. **È critica per PA?** → Se SI: CAD + AGID sezioni ampliate
5. **Quali normative industria-specific?** → Es. healthcare (sanità) ha norme extra

---

## Prossimi Step per A1

1. **Applicare template a SP critici**: SP01, SP05, SP07, SP12, SP29, SP42 (6 file, ~2-3 ore)
2. **Applicare a SP alto-priorità**: SP02-04, SP06, SP08-11, SP16-19, etc. (15-20 file, ~4-5 ore)
3. **Applicare a SP rimanenti**: (40+ file, ~6-8 ore)
4. **Validare cross-references** con GLOSSARIO-TERMINOLOGICO.md
5. **Commit finale A1**

---

**Template versione**: 1.0
**Creato**: 2025-11-19
**Basato su**: UC5 HITL patterns + GLOSSARIO-TERMINOLOGICO.md
