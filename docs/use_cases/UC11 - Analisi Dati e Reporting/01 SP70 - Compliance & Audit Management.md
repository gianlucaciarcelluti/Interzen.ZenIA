# SP70 - Compliance & Audit Management System

## Descrizione Componente

Il **SP70 Compliance & Audit Management System** fornisce una piattaforma completa per la gestione della conformità normativa e il tracciamento delle attività di audit nel sistema ZenIA. Implementa monitoraggio della conformità CAD/GDPR/AgID, audit trail completo, SLA tracking dal lato compliance, e automazione dei report di compliance per garantire la tracciabilità e la conformità normativa continua.

**Differenziazione**: SP70 si focalizza sulla **conformità e audit trail** dal lato governance, mentre SP72 (Incident Management & Escalation) gestisce gli **incident operativi**.

## Responsabilità

- **Compliance Monitoring**: Monitoraggio conformità CAD, GDPR, linee guida AgID
- **Audit Trail**: Tracciamento completo di tutte le attività per forensics e audit
- **Compliance Reporting**: Generazione report compliance per stakeholder e auditor
- **Policy Tracking**: Monitoraggio aderenza a policy e procedure
- **Violation Detection**: Identificazione e alert su violazioni normative
- **SLA Monitoring**: Monitoraggio rispetto a SLA compliance dal lato governance
- **Audit Documentation**: Documentazione completa audit trail e investigazioni
- **Compliance Analytics**: Analytics compliance trends e risk identification

## Architettura Interna

```
┌─────────────────────────────────────────────────────────────┐
│            INCIDENT DETECTION & PROCESSING                  │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Alert Intake      Classification Engine    Routing      ││
│  │ ┌──────────────┐  ┌──────────────────┐   ┌──────────┐  ││
│  │ │ - Metrics    │  │ - Severity       │   │ - Teams  │  ││
│  │ │ - Logs       │  │ - Impact         │   │ - Skills │  ││
│  │ │ - Events     │  │ - Urgency        │   │ - Avail. │  ││
│  │ │ - Health     │  │ - ML Clustering  │   │ - Dist.  │  ││
│  │ └──────────────┘  └──────────────────┘   └──────────┘  ││
└─────────────────────────────────────────────────────────────┘
│            LIFECYCLE MANAGEMENT LAYER                       │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Status Tracker    Escalation Engine    Communication   ││
│  │ ┌──────────────┐  ┌──────────────────┐ ┌──────────┐   ││
│  │ │ - Open       │  │ - SLA Monitoring │ │ - Email  │   ││
│  │ │ - In Progress│  │ - Auto Escalate  │ │ - Slack  │   ││
│  │ │ - Pending    │  │ - Manual Override│ │ - SMS    │   ││
│  │ │ - Resolved   │  │ - History        │ │ - Tickets│   ││
│  │ └──────────────┘  └──────────────────┘ └──────────┘   ││
└─────────────────────────────────────────────────────────────┘
│            POST-MORTEM & LEARNING LAYER                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ RCA Automation       Knowledge Mgmt     Analytics       ││
│  │ ┌──────────────────┐ ┌──────────────┐  ┌──────────┐   ││
│  │ │ - Timeline       │ │ - Patterns   │  │ - MTTR   │   ││
│  │ │ - Correlation    │ │ - Solutions  │  │ - MTTD   │   ││
│  │ │ - Prevention     │ │ - Prevention │  │ - Trends │   ││
│  │ │ - Action Items   │ │ - Database   │  │ - KPIs   │   ││
│  │ └──────────────────┘ └──────────────┘  └──────────┘   ││
└─────────────────────────────────────────────────────────────┘
│                    DATA LAYER                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ PostgreSQL        Elasticsearch      Redis              ││
│  │ ┌────────────────┐ ┌────────────────┐ ┌────────────┐   ││
│  │ │ - Incidents    │ │ - Full Text    │ │ - Session  │   ││
│  │ │ - Timeline     │ │ - Correlation  │ │ - Queue    │   ││
│  │ │ - Escalation   │ │ - Trends       │ │ - Cache    │   ││
│  │ │ - Assignments  │ │ - Analysis     │ │ - Feedback │   ││
│  │ └────────────────┘ └────────────────┘ └────────────┘   ││
└─────────────────────────────────────────────────────────────┘
```

## Input/Output

### Input
- **Alerts**: Da monitoring (Prometheus, Datadog, ELK)
- **Event Streams**: Da services (Kafka topics)
- **Health Checks**: Da sistema monitoring (SP63)
- **User Reports**: Segnalazioni manuali via portal
- **Escalation Policies**: Regole escalation per team/service

### Output
- **Incident Tickets**: Issue documentate e tracciabili
- **Notifications**: Alert a team e management
- **Escalation Actions**: Incremento priorità e engagement
- **Post-Mortem Reports**: RCA e action items
- **Analytics**: Dashboard incident trends e KPIs

## Dipendenze

### Upstream
```
SP63 (Monitoring & Alerting) → SP70
  Data: Alerts, health events, performance metrics
  Timing: Real-time alert feed
  SLA: Incident creation < 30 sec from alert

SP64 (Security & Compliance) → SP70
  Data: Security violations, compliance alerts
  Timing: Event-driven
  SLA: Security incident < 15 sec
```

### Downstream
```
SP70 → SP10 (Dashboard)
  Data: Incident list, SLA status, escalation info
  Timing: Real-time updates
  SLA: < 500ms

SP70 → SP69 (Performance Optimization)
  Data: Incident patterns, recurring issues
  Timing: Daily/weekly analysis
  SLA: Report < 1 hour

SP70 → Compliance
  Data: Incident audit trail, resolution records
  Timing: On-demand / daily
  SLA: Report < 30 min
```

## Stack Tecnologico

| Componente | Tecnologia | Versione | Scopo |
|-----------|-----------|----------|-------|
| Language | Python | 3.11 | Core engine |
| API | FastAPI | 0.104+ | REST endpoints |
| Message Queue | Kafka | 3.5+ | Alert ingestion |
| Database | PostgreSQL | 15+ | Incident storage |
| Search | Elasticsearch | 8.10+ | Incident search |
| Cache | Redis | 7.2+ | Real-time state |
| Workflow | Temporal | Latest | Escalation workflows |
| Notifications | SendGrid/Twilio | API | Multi-channel alerts |

## API Endpoints

**POST /api/v1/incidents/create**

Request:
```json
{
  "alert_source": "prometheus",
  "alert_name": "HighCPUUsage",
  "severity": "critical",
  "affected_services": ["SP63", "SP64"],
  "description": "CPU usage > 90%",
  "metadata": {
    "threshold": 90,
    "current_value": 95,
    "duration_seconds": 300
  }
}
```

Response:
```json
{
  "incident_id": "INC-2025-001234",
  "status": "open",
  "created_at": "2025-11-17T15:30:00Z",
  "assigned_to": "platform-team",
  "severity": "critical",
  "sla_response_time": 15,
  "sla_resolution_time": 60
}
```

**POST /api/v1/incidents/{incident_id}/escalate**

Request:
```json
{
  "reason": "SLA at risk",
  "escalation_level": 2,
  "notify_managers": true
}
```

Response:
```json
{
  "incident_id": "INC-2025-001234",
  "escalation_level": 2,
  "escalated_to": ["team-lead", "manager"],
  "escalation_timestamp": "2025-11-17T15:45:00Z",
  "new_sla_response_time": 5
}
```

**POST /api/v1/incidents/{incident_id}/resolve**

Request:
```json
{
  "resolution_notes": "Restarted service SP63",
  "root_cause": "Memory leak in cache layer",
  "prevention_actions": [
    "Increase monitoring frequency",
    "Add memory limits to container"
  ],
  "knowledge_base_link": "kb_123"
}
```

Response:
```json
{
  "incident_id": "INC-2025-001234",
  "status": "resolved",
  "resolution_time_minutes": 15,
  "sla_met": true,
  "postmortem_scheduled": true
}
```

**GET /api/v1/incidents/analytics**
```
?start_date=2025-11-01&end_date=2025-11-30&severity=critical

Response:
{
  "total_incidents": 45,
  "critical": 3,
  "high": 12,
  "medium": 20,
  "low": 10,
  "avg_response_time_minutes": 8.5,
  "avg_resolution_time_minutes": 45.2,
  "sla_compliance": 97.8,
  "top_services": [
    {"service": "SP63", "incident_count": 8},
    {"service": "SP64", "incident_count": 6}
  ],
  "trends": {...}
}
```

## Database Schema

```sql
CREATE TABLE incidents (
  id SERIAL PRIMARY KEY,
  incident_id VARCHAR(50) UNIQUE,
  title VARCHAR(255),
  description TEXT,
  severity VARCHAR(20),  -- critical, high, medium, low
  impact VARCHAR(255),
  status VARCHAR(20),  -- open, in_progress, escalated, resolved
  created_at TIMESTAMPTZ DEFAULT NOW(),
  created_by VARCHAR(255),
  assigned_to VARCHAR(255),
  resolved_at TIMESTAMPTZ,
  resolution_notes TEXT,
  root_cause TEXT,
  INDEX idx_incident_id (incident_id),
  INDEX idx_status (status),
  INDEX idx_severity (severity),
  INDEX idx_created_at (created_at DESC)
);

CREATE TABLE incident_timeline (
  id SERIAL PRIMARY KEY,
  incident_id INT REFERENCES incidents(id),
  event_type VARCHAR(50),  -- created, assigned, escalated, resolved
  event_timestamp TIMESTAMPTZ DEFAULT NOW(),
  actor VARCHAR(255),
  details JSONB,
  INDEX idx_incident_id (incident_id),
  INDEX idx_event_timestamp (event_timestamp DESC)
);

CREATE TABLE escalation_policies (
  id SERIAL PRIMARY KEY,
  team_id VARCHAR(255),
  service_name VARCHAR(255),
  policy_json JSONB,  -- escalation levels, timers, contacts
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(team_id, service_name)
);

CREATE TABLE sla_tracking (
  id SERIAL PRIMARY KEY,
  incident_id INT REFERENCES incidents(id),
  sla_response_minutes INT,
  sla_resolution_minutes INT,
  response_met BOOLEAN,
  resolution_met BOOLEAN,
  response_at TIMESTAMPTZ,
  resolution_at TIMESTAMPTZ,
  INDEX idx_incident_id (incident_id)
);
```

## Performance & KPIs

| Metrica | Target |
|---------|--------|
| **Alert-to-Incident Latency** | < 30 sec |
| **Assignment Latency** | < 2 min |
| **Escalation Latency** | < 5 min |
| **MTTD (Mean Time To Detect)** | < 1 min |
| **MTTR (Mean Time To Resolve)** | < 1 hour |
| **SLA Compliance** | > 95% |
| **Incident Accuracy** | > 90% (no false positives) |

## Security & Compliance

- **Data Protection**: Encryption at-rest (PII redaction)
- **Access Control**: Role-based incident access
- **Audit Trail**: Immutable event log
- **Compliance**: Incident documentation for regulatory requirements
- **Privacy**: GDPR-compliant incident data handling

## Testing Strategy

- **Unit**: Classification, routing logic (> 85% coverage)
- **Integration**: Alert → incident → escalation → resolution
- **E2E**: Full incident lifecycle from detection to post-mortem
- **Load**: Handle 10,000+ alerts/hour
- **Chaos**: Simulate failures, network issues, delays

## Implementazione Timeline

1. **Phase 1**: Alert ingestion + incident creation
2. **Phase 2**: Assignment + escalation workflows
3. **Phase 3**: SLA tracking + post-mortem automation
4. **Phase 4**: AI-powered RCA + prevention recommendations

---

**Documento**: SP70 - Compliance & Audit Management System
**Ruolo**: Governance & Compliance (Cross-Cutting Infrastructure)
**Associato a**: UC11 - Analisi Dati e Reporting (Infrastructure)
**MS Primario**: MS14 - Generic Audit Engine
**MS Supporto**: MS13 - Generic Security Engine
**Status**: DOCUMENTATO
**Created**: 2025-11-17

**Nota Importante**: SP70 gestisce conformità e audit trail dal lato governance/compliance. Per la gestione operativa degli incident (alert, escalation, post-mortem), vedere SP72 Incident Management & Escalation.
