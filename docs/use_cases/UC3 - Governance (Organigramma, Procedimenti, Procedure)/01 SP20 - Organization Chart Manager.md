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

- **Access Control**: RBAC per livelli organigramma
- **Data Privacy**: Mascheramento dati sensibili
- **Audit Trail**: Log tutte modifiche struttura
- **Encryption**: Dati crittografati at rest/transit

### Evoluzione

1. **AI-Powered Org Design**: Suggerimenti ottimizzazione struttura
2. **Dynamic Reorganization**: Ristrutturazioni automatiche
3. **Workload Balancing**: Distribuzione automatica compiti</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC3 - Governance (Organigramma, Procedimenti, Procedure)/01 SP20 - Organization Chart Manager.md