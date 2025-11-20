# API Reference - MS08-MONITOR

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms08--monitor)

## Panoramica API

MS08-MONITOR espone API RESTful per l'accesso programmatico ai dati di monitoraggio, configurazione degli alert e gestione dei dashboard. L'API supporta autenticazione JWT e API keys, con rate limiting e comprehensive error handling.

**Base URL**: `https://ms08-monitor.zenia.local/api/v1`

**Autenticazione**: Bearer Token (JWT) o API Key header

## Endpoint Principali

### 1. Metrics API

#### 1.1 Query Metrics
Esegue query PromQL sui dati metriche.

```http
GET /metrics/query?query=up&time=2024-01-15T10:00:00Z&timeout=30s
Authorization: Bearer {jwt_token}
```

**Query Parameters**:
- `query`: Espressione PromQL
- `time`: Timestamp per query istantanea (RFC3339)
- `timeout`: Timeout query (default 30s)

**Response**:
```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "up",
          "job": "zenia-microservices",
          "service": "ms01-classifier",
          "instance": "10.0.1.15:8080"
        },
        "value": [1642159200, "1"]
      }
    ]
  },
  "stats": {
    "timings": {
      "evalTotalTime": 0.001,
      "resultSortTime": 0.0001,
      "queryPreparationTime": 0.0002
    }
  }
}
```

#### 1.2 Range Query Metrics
Query per intervallo di tempo.

```http
GET /metrics/query_range?query=rate(http_requests_total[5m])&start=2024-01-15T09:00:00Z&end=2024-01-15T10:00:00Z&step=60s
Authorization: Bearer {jwt_token}
```

**Query Parameters**:
- `query`: Espressione PromQL
- `start`: Timestamp inizio (RFC3339)
- `end`: Timestamp fine (RFC3339)
- `step`: Intervallo step (durata)

**Response**:
```json
{
  "status": "success",
  "data": {
    "resultType": "matrix",
    "result": [
      {
        "metric": {
          "__name__": "http_requests_total",
          "method": "GET",
          "status": "200"
        },
        "values": [
          [1642155600, "150"],
          [1642155660, "145"],
          [1642155720, "152"]
        ]
      }
    ]
  }
}
```

#### 1.3 Series Metadata
Recupera metadati per serie metriche.

```http
GET /metrics/series?match[]=up&match[]=http_requests_total&start=2024-01-15T09:00:00Z&end=2024-01-15T10:00:00Z
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "__name__": "up",
      "job": "zenia-microservices",
      "service": "ms01-classifier"
    },
    {
      "__name__": "http_requests_total",
      "method": "GET",
      "status": "200",
      "service": "ms01-classifier"
    }
  ]
}
```

### 2. Logs API

#### 2.1 Search Logs
Ricerca nei log aggregati.

```http
POST /logs/search
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "service": "ms01-classifier"
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": "2024-01-15T09:00:00Z",
              "lte": "2024-01-15T10:00:00Z"
            }
          }
        }
      ],
      "should": [
        {
          "match": {
            "level": "ERROR"
          }
        },
        {
          "match": {
            "level": "WARN"
          }
        }
      ]
    }
  },
  "size": 100,
  "from": 0,
  "sort": [
    {
      "@timestamp": {
        "order": "desc"
      }
    }
  ],
  "aggs": {
    "levels": {
      "terms": {
        "field": "level",
        "size": 10
      }
    }
  }
}
```

**Response**:
```json
{
  "took": 45,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1250,
      "relation": "eq"
    },
    "max_score": 8.5,
    "hits": [
      {
        "_index": "zenia-logs-2024-01-15",
        "_id": "log-123456",
        "_score": 8.5,
        "_source": {
          "@timestamp": "2024-01-15T09:45:30Z",
          "service": "ms01-classifier",
          "level": "ERROR",
          "message": "Document classification failed",
          "correlation_id": "corr-789",
          "error": {
            "type": "ModelLoadError",
            "message": "Failed to load ML model"
          }
        }
      }
    ]
  },
  "aggregations": {
    "levels": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "INFO",
          "doc_count": 950
        },
        {
          "key": "WARN",
          "doc_count": 250
        },
        {
          "key": "ERROR",
          "doc_count": 50
        }
      ]
    }
  }
}
```

#### 2.2 Log Aggregation
Aggregazioni sui log per analisi statistiche.

```http
POST /logs/aggregation
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "2024-01-15T00:00:00Z",
        "lte": "2024-01-15T23:59:59Z"
      }
    }
  },
  "aggs": {
    "services": {
      "terms": {
        "field": "service",
        "size": 20
      },
      "aggs": {
        "levels": {
          "terms": {
            "field": "level"
          },
          "aggs": {
            "hourly": {
              "date_histogram": {
                "field": "@timestamp",
                "calendar_interval": "hour"
              }
            }
          }
        }
      }
    }
  }
}
```

### 3. Traces API

#### 3.1 Search Traces
Ricerca traces distribuiti.

```http
GET /traces/search?service=ms01-classifier&operation=classify_document&start=2024-01-15T09:00:00Z&end=2024-01-15T10:00:00Z&limit=20
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "traces": [
    {
      "traceID": "7c2f8e8d9f1a4b2c",
      "spans": [
        {
          "traceID": "7c2f8e8d9f1a4b2c",
          "spanID": "3d7e9b2f8a1c",
          "operationName": "classify_document",
          "references": [],
          "startTime": 1642159200000000,
          "duration": 150000,
          "tags": {
            "service": "ms01-classifier",
            "tenant_id": "tenant-pa-roma",
            "document_type": "fascicolo_ambientale"
          },
          "logs": [
            {
              "timestamp": 1642159200050000,
              "fields": {
                "event": "model_loaded",
                "model_version": "v2.1"
              }
            }
          ],
          "process": {
            "serviceName": "ms01-classifier",
            "tags": {
              "version": "1.2.3"
            }
          }
        }
      ],
      "processes": {
        "p1": {
          "serviceName": "ms01-classifier",
          "tags": {
            "version": "1.2.3"
          }
        }
      },
      "warnings": null
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0,
  "errors": null
}
```

#### 3.2 Trace Dependencies
Analizza dipendenze tra servizi.

```http
GET /traces/dependencies?endTs=1642159200000000&lookback=3600000000
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "dependencies": [
    {
      "parent": "ms01-classifier",
      "child": "ms02-analyzer",
      "callCount": 1250
    },
    {
      "parent": "ms02-analyzer",
      "child": "ms03-orchestrator",
      "callCount": 1245
    },
    {
      "parent": "ms03-orchestrator",
      "child": "ms04-validator",
      "callCount": 1200
    }
  ]
}
```

### 4. Alerts API

#### 4.1 List Active Alerts
Elenco alert attivi.

```http
GET /alerts?status=firing&severity=critical&limit=50
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "alerts": [
    {
      "id": "alert-123",
      "name": "HighErrorRate",
      "severity": "critical",
      "status": "firing",
      "description": "Error rate > 5% for 5 minutes",
      "summary": "High error rate detected in ms01-classifier",
      "labels": {
        "alertname": "HighErrorRate",
        "service": "ms01-classifier",
        "severity": "critical"
      },
      "annotations": {
        "summary": "High error rate detected",
        "description": "Error rate is 7.5% which is above threshold of 5%",
        "runbook_url": "https://zenia.runbooks/high-error-rate"
      },
      "startsAt": "2024-01-15T10:00:00Z",
      "endsAt": null,
      "generatorURL": "https://prometheus.zenia.local/graph?g0.expr=rate%28zenia_errors_total%5B5m%5D%29+%2F+rate%28zenia_requests_total%5B5m%5D%29+%3E+0.05&g0.tab=1",
      "fingerprint": "fingerprint-123"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

#### 4.2 Create Alert Rule
Crea una nuova regola di alert.

```http
POST /alerts/rules
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "name": "CustomHighLatency",
  "description": "Alert for high processing latency",
  "query": "histogram_quantile(0.95, rate(zenia_processing_latency_seconds[5m])) > 2.0",
  "duration": "5m",
  "severity": "warning",
  "labels": {
    "team": "backend",
    "component": "processing"
  },
  "annotations": {
    "summary": "High processing latency detected",
    "description": "95th percentile latency is above 2 seconds",
    "runbook_url": "https://zenia.runbooks/high-latency"
  }
}
```

**Response**:
```json
{
  "id": "rule-456",
  "name": "CustomHighLatency",
  "status": "created",
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### 4.3 Alert History
Storico degli alert.

```http
GET /alerts/history?start=2024-01-14T00:00:00Z&end=2024-01-15T23:59:59Z&limit=100
Authorization: Bearer {jwt_token}
```

### 5. Dashboard API

#### 5.1 List Dashboards
Elenco dashboard disponibili.

```http
GET /dashboards?tag=production&limit=20
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "dashboards": [
    {
      "id": "dashboard-123",
      "title": "System Overview",
      "description": "Main system health dashboard",
      "tags": ["production", "overview"],
      "created": "2024-01-01T00:00:00Z",
      "updated": "2024-01-15T09:00:00Z",
      "url": "/d/dashboard-123/system-overview"
    }
  ],
  "total": 1
}
```

#### 5.2 Create Dashboard
Crea un nuovo dashboard.

```http
POST /dashboards
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "dashboard": {
    "title": "Custom Service Dashboard",
    "description": "Dashboard for custom service monitoring",
    "tags": ["custom", "service"],
    "timezone": "UTC",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ],
        "gridPos": {
          "h": 8,
          "w": 12,
          "x": 0,
          "y": 0
        }
      }
    ],
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "refresh": "5s"
  },
  "folderId": 0,
  "overwrite": false
}
```

### 6. Health API

#### 6.1 System Health
Stato di salute del sistema di monitoraggio.

```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.2.3",
  "checks": {
    "prometheus": {
      "status": "healthy",
      "timestamp": "2024-01-15T10:00:00Z",
      "response_time_ms": 15
    },
    "elasticsearch": {
      "status": "healthy",
      "timestamp": "2024-01-15T10:00:00Z",
      "cluster_status": "green",
      "response_time_ms": 25
    },
    "jaeger": {
      "status": "healthy",
      "timestamp": "2024-01-15T10:00:00Z",
      "response_time_ms": 10
    },
    "grafana": {
      "status": "healthy",
      "timestamp": "2024-01-15T10:00:00Z",
      "response_time_ms": 20
    }
  }
}
```

### 7. Configuration API

#### 7.1 Get Configuration
Recupera configurazione corrente.

```http
GET /config
Authorization: Bearer {jwt_token}
```

#### 7.2 Update Configuration
Aggiorna configurazione.

```http
PUT /config
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "prometheus": {
    "global": {
      "scrape_interval": "30s"
    }
  },
  "alerting": {
    "alertmanagers": [
      {
        "static_configs": [
          {
            "targets": ["alertmanager:9093"]
          }
        ]
      }
    ]
  }
}
```

### 8. Sicurezza e Autenticazione

#### 8.1 JWT Authentication
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 8.2 API Key Authentication
```http
X-API-Key: monitor_1a2b3c4d5e6f7890abcdef1234567890
```

#### 8.3 Rate Limiting
- **Per tenant**: 1000 richieste/minuto
- **Per API key**: 500 richieste/minuto
- **Burst limit**: 100 richieste per burst

### 9. Error Handling

#### 9.1 Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field": "query",
      "issue": "Invalid PromQL expression"
    }
  },
  "request_id": "req-uuid-123",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### 9.2 Common Error Codes
- `VALIDATION_ERROR`: Dati input non validi
- `AUTHENTICATION_FAILED`: Credenziali non valide
- `AUTHORIZATION_FAILED`: Permessi insufficienti
- `RATE_LIMIT_EXCEEDED`: Limite richieste superato
- `SERVICE_UNAVAILABLE`: Servizio temporaneamente non disponibile
- `QUERY_TIMEOUT`: Timeout esecuzione query
- `INTERNAL_ERROR`: Errore interno del sistema

### 10. SDK e Client Libraries

#### 10.1 Python Client
```python
from zenia_monitor import MonitorClient

client = MonitorClient(
    base_url="https://ms08-monitor.zenia.local",
    api_key="monitor_1a2b3c4d5e6f7890abcdef1234567890"
)

# Query metrics
result = client.query_metrics(
    query="up",
    time="2024-01-15T10:00:00Z"
)

# Search logs
logs = client.search_logs({
    "query": {
        "match": {"service": "ms01-classifier"}
    },
    "size": 100
})

# Get alerts
alerts = client.get_alerts(status="firing")
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### 10.2 JavaScript Client
```javascript
import { MonitorClient } from '@zenia/monitor-client';

const client = new MonitorClient({
  baseURL: 'https://ms08-monitor.zenia.local',
  apiKey: 'monitor_1a2b3c4d5e6f7890abcdef1234567890'
});

// Query metrics
const metrics = await client.queryMetrics({
  query: 'up',
  time: '2024-01-15T10:00:00Z'
});

// Real-time alerts subscription
const subscription = client.subscribeAlerts({
  severity: 'critical'
}, (alert) => {
  console.log('New alert:', alert);
});
```

### 11. Versioning e Compatibility

#### 11.1 API Versioning
- **Current Version**: v1
- **Version Header**: `Accept: application/vnd.zenia.monitor.v1+json`
- **Deprecation Policy**: 12 mesi notice per breaking changes

#### 11.2 Backward Compatibility
- **Additive Changes**: Nuovi campi opzionali sempre backward compatible
- **Breaking Changes**: Solo in nuove major version
- **Migration Guide**: Fornito per ogni major version upgrade

### 12. Best Practices

#### 12.1 Query Optimization
- **Time Ranges**: Limita range temporali per performance
- **Selectivity**: Usa filtri selettivi per ridurre dataset
- **Caching**: Sfrutta caching per query frequenti
- **Aggregation**: Usa aggregazioni server-side quando possibile

#### 12.2 Monitoring Best Practices
- **Alert Fatigue**: Configura soglie appropriate per evitare false positive
- **Correlation**: Correlazione tra metriche, log e traces per troubleshooting
- **Baselining**: Stabilisci baseline normali per anomaly detection
- **Documentation**: Documenta alert rules e runbook procedures

#### 12.3 Security Best Practices
- **Principle of Least Privilege**: Accesso minimo necessario
- **Audit Logging**: Log completo per compliance
- **Data Classification**: Classificazione dati per appropriate controlli
- **Regular Reviews**: Review periodico permessi e configurazioni