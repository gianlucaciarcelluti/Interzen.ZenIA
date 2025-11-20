# API Reference - MS10-LOGGER

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [← API.md](API.md) | [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms10--logger)

## 1. Panoramica API

MS10-LOGGER espone molteplici interfacce API per l'accesso ai log, analytics e configurazione del sistema di logging. Le API supportano autenticazione JWT, rate limiting e audit trail completo.

**Versione API**: v1.0
**Base URL**: `https://logger.zenia.local/ms10-logger/v1`
**Protocolli**: REST, GraphQL, WebSocket, Server-Sent Events
**Autenticazione**: JWT Bearer Token + API Key
**Rate Limiting**: 1000 req/min per tenant

## 2. Autenticazione e Autorizzazione

### 2.1 JWT Token Authentication

```http
POST /auth/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "ms01-classifier",
  "client_secret": "service-secret-key",
  "scope": "logs:read logs:write"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "logs:read logs:write"
}
```

### 2.2 API Key Authentication

```http
GET /logs/search?q=level:ERROR
Authorization: Bearer {jwt-token}
X-API-Key: ak-1234567890abcdef
X-Tenant-ID: tenant-pa-roma
```

### 2.3 Role-Based Permissions

| Ruolo | Permessi | Scope |
|-------|----------|-------|
| `log_viewer` | logs:read | Tenant-specific logs |
| `log_admin` | logs:read, logs:write, logs:delete | All tenant logs |
| `security_analyst` | logs:read, security:read | Security and audit logs |
| `system_monitor` | logs:read, metrics:read | System metrics and logs |

## 3. REST API

### 3.1 Log Ingestion

#### Bulk Log Ingestion
```http
POST /logs/bulk
Content-Type: application/json
Authorization: Bearer {service-token}
X-Tenant-ID: tenant-pa-roma

{
  "entries": [
    {
      "timestamp": "2024-01-15T10:30:45.123Z",
      "level": "INFO",
      "service": "ms01-classifier",
      "instance": "ms01-classifier-7x9k2",
      "message": "Document classification completed",
      "correlation_id": "corr-123-abc-456-def",
      "context": {
        "document_id": "DOC-2024-001234-ABC",
        "processing_time_ms": 1250
      },
      "mdc": {
        "user_id": "user-pa-roma-789",
        "request_id": "req-456-def-789-ghi"
      }
    }
  ]
}
```

**Response**:
```json
{
  "status": "success",
  "ingested_count": 1,
  "processing_time_ms": 45,
  "entries": [
    {
      "id": "log-123456789-abcdef-001",
      "status": "indexed",
      "index": "zenia-logs-2024.01.15"
    }
  ]
}
```

#### Single Log Entry
```http
POST /logs
Content-Type: application/json
Authorization: Bearer {service-token}
X-Tenant-ID: tenant-pa-roma

{
  "timestamp": "2024-01-15T10:31:00.000Z",
  "level": "ERROR",
  "service": "ms02-analyzer",
  "message": "Failed to analyze document: invalid format",
  "correlation_id": "corr-123-abc-456-def",
  "error": {
    "code": "INVALID_DOCUMENT_FORMAT",
    "details": "Document format not supported"
  }
}
```

### 3.2 Log Query

#### Search Logs
```http
GET /logs/search?q=level:ERROR AND service:ms01-classifier&from=0&size=50&sort=timestamp:desc
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
Accept: application/json
```

**Query Parameters**:
- `q`: Elasticsearch query string
- `from`: Offset for pagination
- `size`: Number of results (max 1000)
- `sort`: Sort field and order
- `fields`: Comma-separated list of fields to return
- `highlight`: Enable highlighting (true/false)

**Response**:
```json
{
  "took": 45,
  "timed_out": false,
  "hits": {
    "total": {
      "value": 1250,
      "relation": "eq"
    },
    "max_score": 8.542,
    "hits": [
      {
        "_index": "zenia-logs-2024.01.15",
        "_id": "log-123456789-abcdef-001",
        "_score": 8.542,
        "_source": {
          "timestamp": "2024-01-15T10:30:45.123Z",
          "level": "ERROR",
          "service": "ms01-classifier",
          "message": "Document classification failed: OCR quality too low",
          "correlation_id": "corr-123-abc-456-def",
          "context": {
            "document_id": "DOC-2024-001234-ABC",
            "error_code": "OCR_QUALITY_LOW"
          }
        },
        "highlight": {
          "message": ["Document classification <em>failed</em>: OCR quality too low"]
        }
      }
    ]
  }
}
```

#### Advanced Query with Filters
```http
POST /logs/search
Content-Type: application/json
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma

{
  "query": {
    "bool": {
      "must": [
        {"term": {"level": "ERROR"}},
        {"term": {"service": "ms01-classifier"}},
        {"range": {"timestamp": {"gte": "now-1h"}}}
      ],
      "should": [
        {"match": {"message": "OCR quality"}},
        {"match": {"correlation_id": "corr-123-abc"}}
      ]
    }
  },
  "sort": [
    {"timestamp": {"order": "desc"}}
  ],
  "size": 100,
  "_source": ["timestamp", "level", "service", "message", "correlation_id", "context"],
  "highlight": {
    "fields": {
      "message": {}
    }
  }
}
```

#### Get Log by ID
```http
GET /logs/{log_id}
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "id": "log-123456789-abcdef-001",
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "ERROR",
  "service": "ms01-classifier",
  "instance": "ms01-classifier-7x9k2",
  "message": "Document classification failed: OCR quality too low",
  "correlation_id": "corr-123-abc-456-def",
  "context": {
    "document_id": "DOC-2024-001234-ABC",
    "error_code": "OCR_QUALITY_LOW",
    "retry_count": 2
  },
  "mdc": {
    "user_id": "user-pa-roma-789",
    "request_id": "req-456-def-789-ghi",
    "client_ip": "192.168.1.100"
  },
  "enrichment": {
    "geo": {
      "country_name": "Italy",
      "city_name": "Rome"
    },
    "tenant_info": {
      "name": "Comune di Roma",
      "type": "PA"
    }
  }
}
```

#### Get Logs by Correlation ID
```http
GET /logs/correlation/{correlation_id}
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "correlation_id": "corr-123-abc-456-def",
  "logs": [
    {
      "id": "log-123456789-abcdef-001",
      "timestamp": "2024-01-15T10:30:00.000Z",
      "service": "ms01-classifier",
      "level": "INFO",
      "message": "Starting document classification"
    },
    {
      "id": "log-123456789-abcdef-002",
      "timestamp": "2024-01-15T10:30:45.123Z",
      "service": "ms01-classifier",
      "level": "ERROR",
      "message": "Document classification failed: OCR quality too low"
    },
    {
      "id": "log-123456789-abcdef-003",
      "timestamp": "2024-01-15T10:31:15.000Z",
      "service": "ms03-orchestrator",
      "level": "WARN",
      "message": "Workflow step failed, initiating retry"
    }
  ]
}
```

### 3.3 Analytics API

#### Get Error Analytics
```http
GET /analytics/errors?period=1h&service=ms01-classifier
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "period": "1h",
  "service": "ms01-classifier",
  "summary": {
    "total_errors": 45,
    "error_rate": 0.023,
    "unique_error_types": 8
  },
  "by_level": {
    "ERROR": 35,
    "FATAL": 8,
    "WARN": 2
  },
  "top_errors": [
    {
      "message": "OCR quality too low",
      "count": 15,
      "percentage": 33.3,
      "first_seen": "2024-01-15T09:15:00Z",
      "last_seen": "2024-01-15T10:45:00Z"
    },
    {
      "message": "Document format not supported",
      "count": 12,
      "percentage": 26.7,
      "first_seen": "2024-01-15T08:30:00Z",
      "last_seen": "2024-01-15T10:30:00Z"
    }
  ],
  "trends": [
    {
      "timestamp": "2024-01-15T09:00:00Z",
      "error_count": 5
    },
    {
      "timestamp": "2024-01-15T10:00:00Z",
      "error_count": 40
    }
  ]
}
```

#### Get Service Performance Metrics
```http
GET /analytics/performance?period=24h&services=ms01-classifier,ms02-analyzer
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "period": "24h",
  "services": ["ms01-classifier", "ms02-analyzer"],
  "metrics": {
    "ms01-classifier": {
      "avg_response_time_ms": 1250,
      "p95_response_time_ms": 2100,
      "p99_response_time_ms": 3500,
      "throughput_req_per_sec": 45.2,
      "error_rate_percent": 2.3,
      "cpu_usage_percent": 65.4,
      "memory_usage_mb": 1024.8
    },
    "ms02-analyzer": {
      "avg_response_time_ms": 890,
      "p95_response_time_ms": 1450,
      "p99_response_time_ms": 2200,
      "throughput_req_per_sec": 62.1,
      "error_rate_percent": 1.8,
      "cpu_usage_percent": 58.9,
      "memory_usage_mb": 896.3
    }
  },
  "trends": {
    "response_time": [
      {"timestamp": "2024-01-14T12:00:00Z", "ms01-classifier": 1150, "ms02-analyzer": 850},
      {"timestamp": "2024-01-15T12:00:00Z", "ms01-classifier": 1250, "ms02-analyzer": 890}
    ],
    "throughput": [
      {"timestamp": "2024-01-14T12:00:00Z", "ms01-classifier": 42.1, "ms02-analyzer": 58.7},
      {"timestamp": "2024-01-15T12:00:00Z", "ms01-classifier": 45.2, "ms02-analyzer": 62.1}
    ]
  }
}
```

#### Get Security Analytics
```http
GET /analytics/security?period=7d&severity=HIGH,CRITICAL
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "period": "7d",
  "severity_filter": ["HIGH", "CRITICAL"],
  "summary": {
    "total_events": 23,
    "by_severity": {
      "CRITICAL": 3,
      "HIGH": 12,
      "MEDIUM": 8
    },
    "by_type": {
      "UNAUTHORIZED_ACCESS": 8,
      "DATA_EXFILTRATION": 3,
      "BRUTE_FORCE": 5,
      "SUSPICIOUS_ACTIVITY": 7
    }
  },
  "top_threats": [
    {
      "type": "UNAUTHORIZED_ACCESS",
      "count": 8,
      "affected_users": 5,
      "affected_resources": 12,
      "trend": "increasing"
    },
    {
      "type": "BRUTE_FORCE",
      "count": 5,
      "blocked_ips": 15,
      "trend": "stable"
    }
  ],
  "timeline": [
    {
      "date": "2024-01-15",
      "events": 5,
      "critical_events": 1
    },
    {
      "date": "2024-01-14",
      "events": 8,
      "critical_events": 2
    }
  ]
}
```

### 3.4 Alert Management

#### Create Alert Rule
```http
POST /alerts/rules
Content-Type: application/json
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma

{
  "name": "High Error Rate Alert",
  "description": "Alert when error rate exceeds 5% for 5 minutes",
  "enabled": true,
  "severity": "HIGH",
  "query": {
    "bool": {
      "must": [
        {"term": {"level": "ERROR"}},
        {"range": {"timestamp": {"gte": "now-5m"}}}
      ]
    }
  },
  "condition": {
    "type": "threshold",
    "field": "doc_count",
    "operator": "gte",
    "value": 50
  },
  "actions": [
    {
      "type": "webhook",
      "url": "https://monitoring.zenia.local/webhooks/alert",
      "headers": {
        "Authorization": "Bearer webhook-token"
      }
    },
    {
      "type": "email",
      "recipients": ["alerts@zenia.local"],
      "subject": "High Error Rate Alert - {{service}}"
    }
  ],
  "throttle_period": "10m"
}
```

**Response**:
```json
{
  "id": "alert-rule-123456",
  "name": "High Error Rate Alert",
  "status": "active",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

#### Get Alert Rules
```http
GET /alerts/rules?enabled=true&severity=HIGH
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "rules": [
    {
      "id": "alert-rule-123456",
      "name": "High Error Rate Alert",
      "description": "Alert when error rate exceeds 5% for 5 minutes",
      "enabled": true,
      "severity": "HIGH",
      "query": {},
      "condition": {},
      "actions": [],
      "throttle_period": "10m",
      "last_triggered": "2024-01-15T09:45:00Z",
      "trigger_count": 3
    }
  ],
  "total": 1
}
```

#### Get Active Alerts
```http
GET /alerts/active?status=OPEN&severity=HIGH,CRITICAL
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "alerts": [
    {
      "id": "alert-789012",
      "rule_id": "alert-rule-123456",
      "status": "OPEN",
      "severity": "HIGH",
      "title": "High Error Rate Alert",
      "description": "Error rate exceeded 5% threshold",
      "triggered_at": "2024-01-15T10:45:00Z",
      "last_updated": "2024-01-15T10:50:00Z",
      "context": {
        "service": "ms01-classifier",
        "error_count": 67,
        "time_window": "5m",
        "threshold": 50
      },
      "acknowledged_by": null,
      "acknowledged_at": null
    }
  ],
  "total": 1
}
```

#### Acknowledge Alert
```http
POST /alerts/{alert_id}/acknowledge
Content-Type: application/json
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma

{
  "user_id": "user-pa-roma-789",
  "comment": "Investigating the issue with the classification service"
}
```

### 3.5 Configuration Management

#### Get Pipeline Configuration
```http
GET /config/pipelines/{pipeline_id}
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma
```

**Response**:
```json
{
  "id": "main-logstash-pipeline",
  "name": "Main Log Processing Pipeline",
  "version": "2.1.0",
  "status": "active",
  "configuration": {
    "input": {
      "kafka": {
        "bootstrap_servers": ["kafka-01:9092", "kafka-02:9092"],
        "topics": ["zenia-logs"],
        "consumer_threads": 3
      }
    },
    "filter": [
      {
        "json": {
          "source": "message"
        }
      },
      {
        "mutate": {
          "add_field": {
            "processing_timestamp": "%{+YYYY-MM-dd HH:mm:ss.SSS}"
          }
        }
      }
    ],
    "output": {
      "elasticsearch": {
        "hosts": ["es-hot-01:9200"],
        "index": "zenia-logs-%{+YYYY.MM.dd}"
      }
    }
  },
  "metrics": {
    "events_processed": 1542000,
    "events_per_second": 45.2,
    "processing_latency_ms": 125
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T08:00:00Z"
}
```

#### Update Pipeline Configuration
```http
PUT /config/pipelines/{pipeline_id}
Content-Type: application/json
Authorization: Bearer {jwt-token}
X-Tenant-ID: tenant-pa-roma

{
  "configuration": {
    "filter": [
      {
        "json": {
          "source": "message"
        }
      },
      {
        "mutate": {
          "add_field": {
            "processing_timestamp": "%{+YYYY-MM-dd HH:mm:ss.SSS}",
            "pipeline_version": "2.1.1"
          }
        }
      },
      {
        "geoip": {
          "source": "client_ip",
          "target": "geo"
        }
      }
    ]
  },
  "comment": "Added geoip enrichment filter"
}
```

## 4. GraphQL API

### 4.1 Schema Definition

```graphql
type Query {
  logs(
    tenantId: String!
    timeRange: TimeRange!
    filters: LogFilters
    pagination: Pagination
  ): LogConnection!

  log(id: ID!): LogEntry

  logsByCorrelationId(
    correlationId: String!
    tenantId: String!
  ): [LogEntry!]!

  errorAnalytics(
    tenantId: String!
    period: String!
    service: String
  ): ErrorAnalytics!

  performanceAnalytics(
    tenantId: String!
    period: String!
    services: [String!]
  ): PerformanceAnalytics!

  securityAnalytics(
    tenantId: String!
    period: String!
    severity: [String!]
  ): SecurityAnalytics!

  alerts(
    tenantId: String!
    status: [AlertStatus!]
    severity: [AlertSeverity!]
  ): [Alert!]!
}

type Mutation {
  ingestLogs(
    tenantId: String!
    entries: [LogEntryInput!]!
  ): IngestResult!

  createAlertRule(
    tenantId: String!
    rule: AlertRuleInput!
  ): AlertRule!

  acknowledgeAlert(
    alertId: ID!
    userId: String!
    comment: String
  ): Alert!
}

type LogEntry {
  id: ID!
  timestamp: DateTime!
  level: LogLevel!
  service: String!
  instance: String
  message: String!
  correlationId: String
  context: JSONObject
  mdc: JSONObject
  enrichment: JSONObject
  tags: [String!]
  labels: JSONObject
}

type LogConnection {
  edges: [LogEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type ErrorAnalytics {
  period: String!
  service: String
  summary: ErrorSummary!
  byLevel: JSONObject!
  topErrors: [TopError!]!
  trends: [ErrorTrend!]!
}

type PerformanceAnalytics {
  period: String!
  services: [String!]!
  metrics: JSONObject!
  trends: JSONObject!
}

input LogFilters {
  level: [LogLevel!]
  service: [String!]
  instance: [String!]
  correlationId: String
  message: String
  context: JSONObject
  tags: [String!]
}

input TimeRange {
  from: DateTime!
  to: DateTime
}

input Pagination {
  first: Int
  after: String
  last: Int
  before: String
}

enum LogLevel {
  TRACE
  DEBUG
  INFO
  WARN
  ERROR
  FATAL
}

enum AlertStatus {
  OPEN
  ACKNOWLEDGED
  RESOLVED
  CLOSED
}

enum AlertSeverity {
  LOW
  MEDIUM
  HIGH
  CRITICAL
}
```

### 4.2 Query Examples

#### Get Recent Error Logs
```graphql
query GetRecentErrors($tenantId: String!) {
  logs(
    tenantId: $tenantId
    timeRange: { from: "2024-01-15T00:00:00Z" }
    filters: { level: [ERROR, FATAL] }
    pagination: { first: 50 }
  ) {
    edges {
      node {
        id
        timestamp
        level
        service
        message
        correlationId
        context
      }
    }
    totalCount
  }
}
```

#### Get Error Analytics
```graphql
query GetErrorAnalytics($tenantId: String!, $period: String!) {
  errorAnalytics(tenantId: $tenantId, period: $period) {
    summary {
      totalErrors
      errorRate
      uniqueErrorTypes
    }
    topErrors {
      message
      count
      percentage
      firstSeen
      lastSeen
    }
    trends {
      timestamp
      errorCount
      uniqueErrors
    }
  }
}
```

#### Get Performance Metrics
```graphql
query GetPerformanceMetrics($tenantId: String!, $services: [String!]!) {
  performanceAnalytics(
    tenantId: $tenantId
    period: "24h"
    services: $services
  ) {
    metrics
    trends
  }
}
```

## 5. Streaming APIs

### 5.1 WebSocket API

#### Real-time Log Streaming
```javascript
// Client-side WebSocket connection
const ws = new WebSocket('wss://logger.zenia.local/ms10-logger/v1/stream/logs');

ws.onopen = function(event) {
  // Send authentication and subscription
  ws.send(JSON.stringify({
    type: 'subscribe',
    token: 'jwt-token',
    tenant_id: 'tenant-pa-roma',
    filters: {
      level: ['ERROR', 'WARN'],
      service: ['ms01-classifier', 'ms02-analyzer']
    }
  }));
};

ws.onmessage = function(event) {
  const logEntry = JSON.parse(event.data);
  console.log('New log entry:', logEntry);
};

// Server message format
{
  "type": "log_entry",
  "data": {
    "id": "log-123456789-abcdef-001",
    "timestamp": "2024-01-15T10:30:45.123Z",
    "level": "ERROR",
    "service": "ms01-classifier",
    "message": "Document classification failed",
    "correlation_id": "corr-123-abc-456-def"
  }
}
```

### 5.2 Server-Sent Events (SSE)

#### Real-time Alert Streaming
```http
GET /stream/alerts?tenant_id=tenant-pa-roma
Authorization: Bearer {jwt-token}
Accept: text/event-stream
```

**SSE Response**:
```
data: {"type": "alert_triggered", "data": {"id": "alert-123", "severity": "HIGH", "title": "High Error Rate"}}

data: {"type": "alert_resolved", "data": {"id": "alert-123", "resolved_at": "2024-01-15T11:00:00Z"}}

data: {"type": "heartbeat"}
```

### 5.3 Kafka Consumer API

#### Direct Kafka Consumption
```java
Properties props = new Properties();
props.put("bootstrap.servers", "kafka-cluster:9092");
props.put("group.id", "log-consumer-app");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("zenia-logs-enriched"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        JSONObject logEntry = new JSONObject(record.value());
        processLogEntry(logEntry);
    }
}
```

## 6. Error Handling

### 6.1 HTTP Status Codes

| Status Code | Description | Example |
|-------------|-------------|---------|
| 200 | Success | Query executed successfully |
| 201 | Created | Alert rule created |
| 400 | Bad Request | Invalid query syntax |
| 401 | Unauthorized | Invalid or missing token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Log entry or resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Elasticsearch cluster unavailable |
| 503 | Service Unavailable | Logstash pipeline down |

### 6.2 Error Response Format

```json
{
  "error": {
    "code": "INVALID_QUERY",
    "message": "Query syntax is invalid",
    "details": {
      "query": "level:ERROR AND",
      "error_offset": 15,
      "suggestion": "Missing field name after AND operator"
    },
    "timestamp": "2024-01-15T10:30:45.123Z",
    "request_id": "req-456-def-789-ghi-jkl",
    "path": "/logs/search",
    "method": "GET"
  }
}
```

### 6.3 Rate Limiting

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1642249200
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API rate limit exceeded",
    "details": {
      "limit": 1000,
      "remaining": 0,
      "reset_time": "2024-01-15T11:00:00Z",
      "retry_after_seconds": 60
    }
  }
}
```

## 7. SDK e Client Libraries

### 7.1 Python SDK

```python
from zenia_logger import ZenIALogger, LogLevel

# Initialize client
logger = ZenIALogger(
    base_url="https://logger.zenia.local/ms10-logger/v1",
    tenant_id="tenant-pa-roma",
    api_key="ak-1234567890abcdef"
)

# Search logs
results = logger.search_logs(
    query="level:ERROR AND service:ms01-classifier",
    time_range={"from": "now-1h"},
    size=100
)

# Ingest logs
logger.ingest_logs([
    {
        "timestamp": "2024-01-15T10:30:45.123Z",
        "level": LogLevel.ERROR,
        "service": "ms01-classifier",
        "message": "Document processing failed",
        "correlation_id": "corr-123-abc-456-def"
    }
])

# Get analytics
analytics = logger.get_error_analytics(
    period="1h",
    service="ms01-classifier"
)
```

## [Auto-generated heading level 2]
### 7.2 Java SDK

```java
ZenIALoggerClient client = new ZenIALoggerClient.Builder()
    .baseUrl("https://logger.zenia.local/ms10-logger/v1")
    .tenantId("tenant-pa-roma")
    .apiKey("ak-1234567890abcdef")
    .build();

// Search logs
SearchRequest request = SearchRequest.builder()
    .query("level:ERROR AND service:ms01-classifier")
    .timeRange(TimeRange.lastHours(1))
    .size(100)
    .build();

SearchResponse response = client.searchLogs(request);

// Ingest logs
List<LogEntry> entries = Arrays.asList(
    LogEntry.builder()
        .timestamp(Instant.now())
        .level(LogLevel.ERROR)
        .service("ms01-classifier")
        .message("Document processing failed")
        .correlationId("corr-123-abc-456-def")
        .build()
);

IngestResponse ingestResponse = client.ingestLogs(entries);

// Get analytics
ErrorAnalytics analytics = client.getErrorAnalytics(
    "1h", "ms01-classifier"
);
```

Questa documentazione API fornisce tutte le interfacce necessarie per interagire con MS10-LOGGER, coprendo ingestion, query, analytics, alert management e configurazione del sistema di logging centralizzato.
