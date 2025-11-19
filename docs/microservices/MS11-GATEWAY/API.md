# MS11-GATEWAY - Documentazione API

> **API Gateway ZenIA - Routing, Sicurezza e Monitoraggio Centralizzato**

[![REST](https://img.shields.io/badge/REST-%23000000.svg?style=flat&logo=rest&logoColor=white)](https://restfulapi.net)
[![GraphQL](https://img.shields.io/badge/GraphQL-%23E10098.svg?style=flat&logo=graphql&logoColor=white)](https://graphql.org)
[![WebSocket](https://img.shields.io/badge/WebSocket-%23000000.svg?style=flat&logo=websocket&logoColor=white)](https://websocket.org)
[![Kong](https://img.shields.io/badge/Kong-%23000000.svg?style=flat&logo=kong&logoColor=white)](https://konghq.com)

## 🎯 Overview API

MS11-GATEWAY espone tre principali interfacce API:

- **REST API** - Routing tradizionale request/response
- **GraphQL API** - Query flessibili e aggregate
- **WebSocket API** - Comunicazione real-time
- **Admin API** - Gestione configurazione Kong

### Endpoint Base

```
Produzione: https://api.zenia.local
Sviluppo:   http://localhost:8000
Admin:      http://localhost:8001
```

## 📋 REST API

### Autenticazione

Tutte le richieste devono includere autenticazione:

```bash
# JWT Token
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
     https://api.zenia.local/api/v1/documents/classify

# API Key
curl -H "X-API-Key: your-api-key" \
     https://api.zenia.local/api/v1/analysis/extract

# OAuth2
curl -H "Authorization: Bearer <oauth2-token>" \
     https://api.zenia.local/api/v1/workflow/status
```

### Routing dei Microservizi

#### MS01-CLASSIFIER

```http
# Classificazione documento
POST /api/v1/documents/classify
Content-Type: application/json
Authorization: Bearer <token>

{
  "document": {
    "content": "Contenuto del documento da classificare...",
    "metadata": {
      "source": "email",
      "priority": "high",
      "type": "provvedimento"
    }
  },
  "options": {
    "confidence_threshold": 0.8,
    "categories": ["autorizzazione", "certificato", "comunicazione"]
  }
}

# Risposta
{
  "request_id": "req_123456",
  "correlation_id": "corr_789012",
  "timestamp": "2025-11-18T10:30:00Z",
  "result": {
    "category": "autorizzazione",
    "confidence": 0.92,
    "subcategories": ["scarico_acque"],
    "processing_time_ms": 245
  },
  "metadata": {
    "gateway_latency_ms": 12,
    "upstream_service": "ms01-classifier",
    "rate_limit_remaining": 987
  }
}
```

#### MS02-ANALYZER

```http
# Analisi contenuto
POST /api/v1/analysis/extract
Content-Type: application/json
Authorization: Bearer <token>

{
  "content": "Testo da analizzare per entità e sentiment...",
  "analysis_types": ["entities", "sentiment", "keywords"],
  "language": "it",
  "options": {
    "extract_entities": true,
    "sentiment_analysis": true,
    "keyword_extraction": {
      "max_keywords": 10,
      "min_score": 0.1
    }
  }
}

# Risposta
{
  "request_id": "req_123457",
  "correlation_id": "corr_789013",
  "result": {
    "entities": [
      {
        "text": "Comune di Milano",
        "type": "LOCATION",
        "confidence": 0.95,
        "position": {"start": 10, "end": 25}
      }
    ],
    "sentiment": {
      "label": "positive",
      "score": 0.78,
      "confidence": 0.89
    },
    "keywords": [
      {"word": "autorizzazione", "score": 0.92},
      {"word": "ambiente", "score": 0.87}
    ]
  },
  "processing_time_ms": 156
}
```

#### MS03-ORCHESTRATOR

```http
# Avvia workflow
POST /api/v1/workflow/start
Content-Type: application/json
Authorization: Bearer <token>

{
  "workflow_type": "document_processing",
  "input": {
    "document_id": "doc_123",
    "source": "email",
    "priority": "normal"
  },
  "steps": [
    {
      "service": "ms01-classifier",
      "action": "classify",
      "config": {"confidence_threshold": 0.8}
    },
    {
      "service": "ms02-analyzer",
      "action": "extract_entities",
      "depends_on": ["ms01-classifier"]
    },
    {
      "service": "ms04-validator",
      "action": "validate_schema",
      "depends_on": ["ms02-analyzer"]
    }
  ],
  "callbacks": {
    "on_success": "https://app.zenia.local/webhook/success",
    "on_failure": "https://app.zenia.local/webhook/failure"
  }
}

# Risposta
{
  "workflow_id": "wf_123456",
  "status": "running",
  "started_at": "2025-11-18T10:30:00Z",
  "estimated_completion": "2025-11-18T10:32:00Z",
  "steps": [
    {
      "id": "step_1",
      "service": "ms01-classifier",
      "status": "completed",
      "duration_ms": 245
    },
    {
      "id": "step_2",
      "service": "ms02-analyzer",
      "status": "running"
    }
  ]
}
```

#### MS04-VALIDATOR

```http
# Validazione dati
POST /api/v1/validation/check
Content-Type: application/json
Authorization: Bearer <token>

{
  "data": {
    "provvedimento": {
      "numero": "123/2025",
      "data_emissione": "2025-11-18",
      "ente_rilascio": "Comune di Milano",
      "tipo_autorizzazione": "scarico_acque"
    }
  },
  "schema": "provvedimento_autorizzazione_v2.1",
  "validation_rules": [
    "required_fields",
    "data_consistency",
    "business_rules"
  ]
}

# Risposta
{
  "valid": true,
  "validation_id": "val_123456",
  "checks_performed": [
    {
      "rule": "required_fields",
      "status": "passed",
      "details": "Tutti i campi obbligatori presenti"
    },
    {
      "rule": "data_consistency",
      "status": "passed",
      "details": "Date valide e coerenti"
    }
  ],
  "warnings": [],
  "processing_time_ms": 89
}
```

### Monitoraggio e Health

```http
# Health check gateway
GET /health

# Risposta
{
  "status": "healthy",
  "timestamp": "2025-11-18T10:30:00Z",
  "version": "1.0.0",
  "upstreams": {
    "ms01-classifier": "healthy",
    "ms02-analyzer": "healthy",
    "ms03-orchestrator": "healthy"
  }
}

# Metriche Prometheus
GET /metrics

# Status rate limiting
GET /status/ratelimit

{
  "consumer": "user_123",
  "limits": {
    "minute": {"used": 45, "limit": 1000},
    "hour": {"used": 2340, "limit": 10000},
    "day": {"used": 15234, "limit": 50000}
  }
}
```

## 🔗 GraphQL API

### Schema Principale

```graphql
# Query
type Query {
  # Documenti
  documents(
    filter: DocumentFilter
    pagination: PaginationInput
  ): DocumentConnection!

  # Workflow
  workflows(
    status: WorkflowStatus
    pagination: PaginationInput
  ): WorkflowConnection!

  # Metriche
  metrics(
    timeframe: TimeframeInput
    services: [String!]
  ): MetricsResponse!

  # Configurazione
  configuration(
    service: String
    version: String
  ): ConfigurationResponse!
}

# Mutations
type Mutation {
  # Documenti
  classifyDocument(input: ClassifyDocumentInput!): ClassifyDocumentPayload!
  validateDocument(input: ValidateDocumentInput!): ValidateDocumentPayload!

  # Workflow
  startWorkflow(input: StartWorkflowInput!): StartWorkflowPayload!
  cancelWorkflow(workflowId: ID!): CancelWorkflowPayload!

  # Configurazione
  updateConfiguration(input: UpdateConfigurationInput!): UpdateConfigurationPayload!
}

# Subscriptions (WebSocket)
type Subscription {
  # Real-time updates
  workflowUpdates(workflowId: ID!): WorkflowUpdate!
  metricsUpdates(services: [String!]): MetricsUpdate!
  systemAlerts(severity: AlertSeverity): SystemAlert!
}
```

### Esempi Query

```graphql
# Query documenti con filtro
query GetDocuments {
  documents(
    filter: {
      category: "autorizzazione"
      dateFrom: "2025-11-01"
      dateTo: "2025-11-18"
      status: "processed"
    }
    pagination: {
      first: 20
      after: "cursor_123"
    }
  ) {
    edges {
      node {
        id
        title
        category
        confidence
        processedAt
        metadata {
          source
          priority
          processingTimeMs
        }
      }
      cursor
    }
    pageInfo {
      hasNextPage
      hasPreviousPage
      startCursor
      endCursor
    }
  }
}

# Mutation classificazione
mutation ClassifyDocument($input: ClassifyDocumentInput!) {
  classifyDocument(input: $input) {
    document {
      id
      category
      confidence
      processingTimeMs
    }
    errors {
      field
      message
    }
  }
}

# Variables
{
  "input": {
    "content": "Contenuto del documento...",
    "options": {
      "confidenceThreshold": 0.8,
      "categories": ["autorizzazione", "certificato"]
    }
  }
}
```

## 🔌 WebSocket API

### Connessione

```javascript
// Connessione WebSocket
const ws = new WebSocket('wss://api.zenia.local/ws/v1/events');

// Autenticazione
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'jwt-token-here'
  }));
};

// Ricezione messaggi
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Invio subscription
ws.send(JSON.stringify({
  type: 'subscribe',
  channels: ['workflow.updates', 'system.alerts'],
  filter: {
    severity: 'high',
    services: ['ms01-classifier', 'ms02-analyzer']
  }
}));
```

### Eventi Supportati

```typescript
interface WebSocketMessage {
  type: 'event' | 'subscription' | 'error' | 'pong';
  id: string;
  timestamp: string;
  correlation_id?: string;
  data: any;
}

// Eventi workflow
interface WorkflowEvent {
  type: 'workflow.started' | 'workflow.step_completed' | 'workflow.completed' | 'workflow.failed';
  workflow_id: string;
  step_id?: string;
  status: 'running' | 'completed' | 'failed';
  progress: number; // 0-100
  result?: any;
  error?: string;
}

// Eventi sistema
interface SystemEvent {
  type: 'system.alert' | 'service.health_changed' | 'rate_limit_exceeded';
  severity: 'info' | 'warning' | 'error' | 'critical';
  service: string;
  message: string;
  details?: any;
}

// Eventi metriche
interface MetricsEvent {
  type: 'metrics.update';
  service: string;
  metrics: {
    requests_per_second: number;
    average_response_time: number;
    error_rate: number;
    active_connections: number;
  };
}
```

### Esempio Client JavaScript

```javascript
class ZenIAWebSocketClient {
  constructor(url, token) {
    this.url = url;
    this.token = token;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected to ZenIA Gateway');
      this.authenticate();
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      this.handleMessage(JSON.parse(event.data));
    };

    this.ws.onclose = () => {
      console.log('Disconnected from ZenIA Gateway');
      this.handleReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  authenticate() {
    this.send({
      type: 'auth',
      token: this.token
    });
  }

  subscribe(channels, filter = {}) {
    this.send({
      type: 'subscribe',
      channels: channels,
      filter: filter
    });
  }

  handleMessage(message) {
    switch (message.type) {
      case 'event':
        this.handleEvent(message);
        break;
      case 'subscription':
        console.log('Subscribed to:', message.data.channels);
        break;
      case 'error':
        console.error('WebSocket error:', message.data);
        break;
      case 'pong':
        // Heartbeat response
        break;
    }
  }

  handleEvent(event) {
    console.log('Received event:', event);

    // Gestione eventi specifici
    switch (event.data.type) {
      case 'workflow.completed':
        this.onWorkflowCompleted(event.data);
        break;
      case 'system.alert':
        this.onSystemAlert(event.data);
        break;
    }
  }

  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

      setTimeout(() => {
        console.log(`Attempting reconnect ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
        this.connect();
      }, delay);
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  // Event handlers
  onWorkflowCompleted(data) {
    console.log('Workflow completed:', data.workflow_id);
    // Update UI, send notifications, etc.
  }

  onSystemAlert(data) {
    console.log('System alert:', data.message);
    // Show alert in UI
  }
}

// Utilizzo
const client = new ZenIAWebSocketClient('wss://api.zenia.local/ws/v1/events', 'jwt-token');
client.connect();

client.subscribe(['workflow.updates', 'system.alerts'], {
  severity: 'high'
});
```

## 🔧 Kong Admin API

### Gestione Servizi

```bash
# Lista servizi
GET /admin/services

# Crea servizio
POST /admin/services
{
  "name": "custom-service",
  "url": "http://custom-service:8080"
}

# Lista routes
GET /admin/routes

# Crea route
POST /admin/routes
{
  "service": {"id": "service-id"},
  "paths": ["/api/v1/custom"],
  "methods": ["GET", "POST"]
}
```

### Gestione Plugins

```bash
# Lista plugin disponibili
GET /admin/plugins/enabled

# Installa plugin su route
POST /admin/routes/{route-id}/plugins
{
  "name": "rate-limiting",
  "config": {
    "minute": 1000,
    "hour": 10000
  }
}

# Lista plugin attivi
GET /admin/plugins

# Rimuovi plugin
DELETE /admin/plugins/{plugin-id}
```

### Gestione Consumer

```bash
# Crea consumer
POST /admin/consumers
{
  "username": "api-consumer",
  "custom_id": "user-123"
}

# Aggiungi API key
POST /admin/consumers/{consumer-id}/key-auth
{
  "key": "api-key-here"
}

# Lista consumer
GET /admin/consumers
```

## 📊 Rate Limiting

### Headers di Risposta

```http
# Rate limit headers
X-RateLimit-Limit-Minute: 1000
X-RateLimit-Remaining-Minute: 987
X-RateLimit-Reset-Minute: 1637242800

X-RateLimit-Limit-Hour: 10000
X-RateLimit-Remaining-Hour: 9876
X-RateLimit-Reset-Hour: 1637246400
```

### Gestione Rate Limit Exceeded

```javascript
// Client-side handling
fetch('/api/v1/documents/classify', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(response => {
  if (response.status === 429) {
    const resetTime = response.headers.get('X-RateLimit-Reset-Minute');
    const waitTime = resetTime - Math.floor(Date.now() / 1000);

    console.log(`Rate limit exceeded. Retry in ${waitTime} seconds`);

    // Implement exponential backoff
    return new Promise(resolve => {
      setTimeout(() => resolve(fetch(request)), waitTime * 1000);
    });
  }
  return response;
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🔒 Sicurezza

### Certificate Pinning

```javascript
// Certificate pinning per client mobile
const publicKeyHashes = [
  'sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=',
  'sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB='
];

fetch('/api/v1/secure/endpoint', {
  headers: {
    'Authorization': `Bearer ${token}`
  },
  // Certificate pinning headers
  'Public-Key-Pins': publicKeyHashes.join('; ')
});
```

### Content Security Policy

```http
# CSP Headers
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## 📋 Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "details": {
      "limit": 1000,
      "remaining": 0,
      "reset_time": "2025-11-18T10:35:00Z"
    },
    "request_id": "req_123456",
    "correlation_id": "corr_789012",
    "timestamp": "2025-11-18T10:30:00Z"
  },
  "gateway_info": {
    "version": "1.0.0",
    "latency_ms": 12,
    "upstream_service": "ms01-classifier"
  }
}
```

### Error Codes

| Code | HTTP Status | Descrizione |
|------|-------------|-------------|
| `INVALID_TOKEN` | 401 | Token JWT non valido |
| `INSUFFICIENT_PERMISSIONS` | 403 | Permessi insufficienti |
| `RATE_LIMIT_EXCEEDED` | 429 | Limite richieste superato |
| `SERVICE_UNAVAILABLE` | 503 | Servizio upstream non disponibile |
| `BAD_REQUEST` | 400 | Richiesta malformata |
| `NOT_FOUND` | 404 | Endpoint non trovato |
| `INTERNAL_ERROR` | 500 | Errore interno gateway |

## 🔍 Testing

### Test Collection Postman

```json
{
  "info": {
    "name": "MS11-GATEWAY API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "JWT Login",
          "request": {
            "method": "POST",
            "header": [
              {"key": "Content-Type", "value": "application/json"}
            ],
            "body": {
              "mode": "raw",
              "raw": "{\"username\": \"test-user\", \"password\": \"test-pass\"}"
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth", "login"]
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {"key": "base_url", "value": "http://localhost:8000"}
  ]
}
```

---

**📖 Documentazione Correlata**: [SPECIFICATION.md](SPECIFICATION.md) | [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
