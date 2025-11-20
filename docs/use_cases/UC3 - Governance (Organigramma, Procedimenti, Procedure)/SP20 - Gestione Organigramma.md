# SP20 - Organization Chart Manager

## Panoramica

**SP20 - Organization Chart Manager** è il componente responsabile della gestione dinamica dell'organigramma aziendale, fornendo funzionalità avanzate per la creazione, modifica e visualizzazione delle strutture organizzative.

```mermaid
graph LR
    HR[HR Systems] --> SP20[SP20<br/>Org Chart Manager]
    LEGACY[Legacy Systems] --> SP20
    SP20 --> SP22[SP22<br/>Process Governance]
    SP20 --> SP10[SP10<br/>Dashboard]

    SP20 -.-> POSTGRES[(PostgreSQL<br/>Org Data)]
    SP20 -.-> REDIS[(Redis<br/>Cache)]
    SP20 -.-> ELASTIC[(Elasticsearch<br/>Search)]
    SP20 -.-> GRAPH[Graph DB<br/>Relations]

    style SP20 fill:#ffd700
```

## Responsabilità

### Core Functions

1. **Organigramma Management**
   - Creazione/modifica strutture gerarchiche
   - Gestione posizioni e ruoli
   - Relazioni organizzative dinamiche

2. **Integration HR**
   - Sync con sistemi risorse umane
   - Aggiornamenti automatici organico
   - Gestione cambi organizzativi

3. **Search & Discovery**
   - Ricerca avanzata posizioni/ruoli
   - Navigazione organigramma interattiva
   - Filtri per competenze/responsabilità

4. **Reporting & Analytics**
   - Report struttura organizzativa
   - Analisi carichi di lavoro
   - Trend organizzativi
## 🏛️ Conformità Normativa - SP20

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP20 (Organization Manager)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC3

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP20 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP20 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Responsabile della Protezione dei Dati (DPO))

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

## Riepilogo Conformità SP20

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsabile |
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

**Prossima Review**: 2026-02-17

---



### Framework Normativi Applicabili

☑ L. 241/1990
☑ CAD
☑ GDPR
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
| GDPR | Art. 5, Art. 32 | ✅ Implementato | [Dettagli](../../templates/conformita-normativa-standard.md) |

### Conformità Normativa - Checklist

- [ ] Tutti i framework normativi applicabili identificati
- [ ] Articoli rilevanti mappati alle responsabilità SP
- [ ] GDPR: Data protection by design implementato (se applicabile)
- [ ] eIDAS: Firma digitale supportata (se applicabile)
- [ ] AI Act: Supervisione umana e trasparenza (se applicabile)
- [ ] Tracciabilità audit completa mantenuta
- [ ] Documentation conformità aggiornata

**Nota**: Dettagli di conformità completi nella sezione "## 🏛️ Conformità Normativa - SP20

### 1. Quadro Normativo di Riferimento

**Framework applicabili a SP20 (Organization Manager)**:
- **CAD** (Codice Amministrazione Digitale): Art. 1, 13, 21-22, 62
- **GDPR** (Regolamento 2016/679): Art. 4, 5, 6, 12, 13, 32

**UC di Appartenenza**: UC3

---

### 2. Conformità CAD

**Applicabilità**: OBBLIGATORIO per tutti gli SP - SP20 è parte della trasformazione digitale PA

**Articoli CAD Principali**:
- Art. 1: Principi digitalizzazione
- Art. 13: Fascicolo informatico
- Art. 21-22: Documento informatico e conservazione
- Art. 62: Interoperabilità via API
- Art. 71: Accessibilità

**Responsabile**: CTO + Compliance Team (audit trimestrale)

---

### 3. Conformità GDPR

**Applicabilità**: CRITICA per SP20 - gestisce dati personali

**Elementi chiave**:
- Base legale: Art. 6(1)c (obbligo legale PA)
- Data Protection by Design: Art. 25 GDPR
- Sicurezza: Art. 32 GDPR (encryption, access control, audit logging)
- Retention: Conformità a regolamenti settore (tipicamente 3-10 anni)
- Diritti interessati: Art. 15-22 (accesso, rettifica, cancellazione)

**DPA (Data Protection Impact Assessment)**: Richiesta se high-risk processing

**Responsabile**: DPO (Responsabile della Protezione dei Dati (DPO))

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

## Riepilogo Conformità SP20

**Status**: ✅ COMPLIANT

| Framework | Applicabile | Status | Responsabile |
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

**Prossima Review**: 2026-02-17

---



---


## Architettura Tecnica

### Data Model

```yaml
OrganizationUnit:
  id: string
  name: string
  type: enum[DEPARTMENT, OFFICE, TEAM, POSITION]
  parent_id: string
  manager_id: string
  attributes: object
  created_at: datetime
  updated_at: datetime

Position:
  id: string
  title: string
  role_type: enum[MANAGER, SPECIALIST, COORDINATOR]
  competencies: array[string]
  responsibilities: array[string]
  unit_id: string
```

### API Endpoints

```yaml
# CRUD Operations
GET /api/v1/orgchart/units
POST /api/v1/orgchart/units
GET /api/v1/orgchart/units/{id}
PUT /api/v1/orgchart/units/{id}
DELETE /api/v1/orgchart/units/{id}

# Hierarchy Operations
GET /api/v1/orgchart/units/{id}/subtree
GET /api/v1/orgchart/units/{id}/path
POST /api/v1/orgchart/units/{id}/move

# Search Operations
GET /api/v1/orgchart/search?q={query}&filters={filters}
GET /api/v1/orgchart/positions/search

# Integration
POST /api/v1/orgchart/sync/hr
GET /api/v1/orgchart/sync/status
```

## [Auto-generated heading level 2]
### Tecnologie Utilizzate

| Componente | Tecnologia | Versione | Scopo |
|------------|------------|----------|--------|
| Framework | FastAPI | 0.104 | API REST |
| Database | PostgreSQL | 15 | Dati organigramma |
| Cache | Redis | 7.2 | Cache strutture |
| Search | Elasticsearch | 8.11 | Ricerca posizioni |
| Graph DB | Neo4j | 5.0 | Relazioni complesse |

### Esempi di Utilizzo

#### Creazione Unità Organizzativa

**POST /api/v1/orgchart/units**
```json
{
  "name": "Ufficio Ambiente",
  "type": "DEPARTMENT",
  "parent_id": "municipality_root",
  "manager_id": "user_123",
  "attributes": {
    "budget_code": "AMB001",
    "location": "Palazzo Comunale"
  }
}
```

#### Ricerca Posizioni

**GET /api/v1/orgchart/search?q=ambiente&filters={"type": "DEPARTMENT"}**

### Configurazione

```yaml
sp20:
  database_url: 'postgresql://user:pass@host:5432/orgchart'
  redis_url: 'redis://cache:6379'
  elasticsearch_url: 'http://search:9200'
  neo4j_url: 'bolt://graph:7687'
  cache_ttl: 3600
  sync_interval: '1h'
```

### Performance Metrics

- **Query Latency**: <50ms per query organigramma
- **Sync Performance**: <5min per sync HR completo
- **Search Accuracy**: >95% risultati rilevanti
- **Availability**: 99.9% uptime

### Sicurezza

- **Controllo Accesso**: RBAC per livelli organigramma
- **Data Privacy**: Mascheramento dati sensibili
- **Registro di Audit**: Log tutte modifiche struttura
- **Crittografia**: Dati crittografati at rest/transit

### Evoluzione

1. **AI-Powered Org Design**: Suggerimenti ottimizzazione struttura
2. **Dynamic Reorganization**: Ristrutturazioni automatiche
3. **Workload Balancing**: Distribuzione automatica compiti</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC3 - Governance (Organigramma, Procedimenti, Procedure)/01 SP20 - Organization Chart Manager.md