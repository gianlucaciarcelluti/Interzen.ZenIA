# SP21 - Procedure Manager

## Panoramica

**SP21 - Procedure Manager** gestisce il repository centralizzato delle procedure operative, fornendo funzionalità avanzate di versioning, approval workflow e ricerca intelligente.

```mermaid
graph LR
    AUTHORS[Procedure Authors] --> SP21[SP21<br/>Procedure Manager]
    APPROVERS[Approvers] --> SP21
    LEGACY[Legacy Procedures] --> SP21
    
    SP21 --> SP22[SP22<br/>Process Governance]
    SP21 --> SP10[SP10<br/>Dashboard]
    
    SP21 -.-> MONGO[(MongoDB<br/>Procedures)]
    SP21 -.-> GIT[(Git<br/>Versioning)]
    SP21 -.-> ELASTIC[(Elasticsearch<br/>Search)]
    SP21 -.-> WORKFLOW[(Approval<br/>Workflow)]
    
    style SP21 fill:#ffd700
```

## Responsabilità

### Core Functions

1. **Procedure Repository**
   - Archiviazione procedure strutturate
   - Metadata ricchi (tag, categorie, dipendenze)
   - Supporto multi-formato (PDF, DOCX, HTML)

2. **Version Control**
   - Git-based versioning procedure
   - Branching per draft/approval
   - Diff visualizzazione modifiche

3. **Approval Workflow**
   - Workflow configurabili approvazione
   - Multi-level approval chains
   - Automatic notifications

4. **Search & Access**
   - Ricerca full-text intelligente
   - Access control per ruolo/competenza
   - Usage tracking e analytics
## 🏛️ Conformità Normativa - SP21

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP21 (Procedure Manager)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC Appartenance**: UC3

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP21 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP21 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Data Protection Officer)

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

## Riepilogo Conformità SP21

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsible |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ✅ Sì | ✅ Compliant | DPO |
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

☑ L. 241/1990
☑ CAD
☐ GDPR - Regolamento 2016/679
☐ eIDAS - Regolamento 2014/910
☐ AI Act - Regolamento 2024/1689
☐ D.Lgs 42/2004 - Codice Beni Culturali
☐ D.Lgs 152/2006 - Codice dell'Ambiente
☐ D.Lgs 33/2013 - Decreto Trasparenza

**Per mappatura completa articoli → implementazioni**, vedi [Conformità Normativa Standard Template](../../templates/conformita-normativa-standard.md) e [COMPLIANCE-MATRIX.md](../../COMPLIANCE-MATRIX.md).

### Requisiti Principali Implementati

| Framework | Requisiti Principali | Status | Riferimenti |
|-----------|-------------------|--------|-------------|
| L. 241/1990 | Art. 1, Art. 3, Art. 6, Art. 27 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |
| CAD | Art. 1, Art. 21, Art. 22, Art. 62 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP21

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP21 (Procedure Manager)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC Appartenance**: UC3

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP21 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP21 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Data Protection Officer)

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

## Riepilogo Conformità SP21

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsible |
|-----------|-----------|--------|-------------|
| CAD | ✅ Sì | ✅ Compliant | CTO |
| GDPR | ✅ Sì | ✅ Compliant | DPO |
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


## Architettura Tecnica

### Document Model

```yaml
Procedure:
  id: string
  title: string
  version: semver
  status: enum[DRAFT, REVIEW, APPROVED, DEPRECATED]
  content: rich_text
  metadata:
    category: string
    tags: array[string]
    competencies: array[string]
    related_procedures: array[string]
  approval_chain: array[approval_step]
  created_by: string
  created_at: datetime
  last_modified: datetime

ApprovalStep:
  id: string
  role: string
  approver: string
  status: enum[PENDING, APPROVED, REJECTED]
  comments: string
  timestamp: datetime
```

### API Endpoints

```yaml
# CRUD Operations
GET /api/v1/procedures
POST /api/v1/procedures
GET /api/v1/procedures/{id}
PUT /api/v1/procedures/{id}
DELETE /api/v1/procedures/{id}

# Versioning
GET /api/v1/procedures/{id}/versions
POST /api/v1/procedures/{id}/versions
GET /api/v1/procedures/{id}/versions/{version}

# Approval Workflow
POST /api/v1/procedures/{id}/submit-approval
POST /api/v1/procedures/{id}/approve
POST /api/v1/procedures/{id}/reject

# Search
GET /api/v1/procedures/search?q={query}&filters={filters}
GET /api/v1/procedures/suggest?q={partial}
```

### Tecnologie Utilizzate

| Componente | Tecnologia | Versione | Scopo |
|------------|------------|----------|--------|
| Framework | FastAPI | 0.104 | API REST |
| Database | MongoDB | 7.0 | Documenti procedure |
| Versioning | Git | 2.40 | Version control |
| Search | Elasticsearch | 8.11 | Ricerca full-text |
| Workflow | Airflow | 2.8 | Approval workflows |

### Esempi di Utilizzo

#### Creazione Procedura

**POST /api/v1/procedures**
```json
{
  "title": "Protocollo Istanza Ambientale",
  "content": "<rich text content>",
  "metadata": {
    "category": "Amministrativo",
    "tags": ["ambiente", "protocollo", "istanza"],
    "competencies": ["protocollista", "tecnico_ambiente"]
  },
  "approval_chain": [
    {"role": "specialista_ambiente", "required": true},
    {"role": "responsabile_ufficio", "required": true}
  ]
}
```

#### Ricerca Procedure

**GET /api/v1/procedures/search?q=protocollo+ambiente&category=Amministrativo**

### Configurazione

```yaml
sp21:
  mongodb_url: 'mongodb://user:pass@host:27017/procedures'
  git_repo_path: '/data/procedures_repo'
  elasticsearch_url: 'http://search:9200'
  approval_timeout: '7d'
  max_versions: 50
```

### Performance Metrics

- **Search Latency**: <100ms per query
- **Upload Speed**: >10MB/s per documento
- **Version History**: <2s per diff calculation
- **Availability**: 99.9% uptime

### Sicurezza

- **Document Encryption**: Crittografia contenuti sensibili
- **Access Control**: Granular permissions per procedura
- **Audit Logging**: Tracciabilità accessi/modifiche
- **Version Integrity**: Hash verification per tampering

### Evoluzione

1. **AI-Powered Search**: Ricerca semantica procedure
2. **Automated Updates**: Aggiornamenti automatici procedure
3. **Integration Training**: Link diretto con LMS</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC3 - Governance (Organigramma, Procedimenti, Procedure)/01 SP21 - Procedure Manager.md