# MS11-GATEWAY - Esempi di Utilizzo

> **Esempi pratici per API Gateway ZenIA**

## 📋 Indice Esempi

- [Richiesta API Classificazione](#richiesta-api-classificazione)
- [Risposta Gateway](#risposta-gateway)
- [Configurazione Routing](#configurazione-routing)
- [Esempio WebSocket](#esempio-websocket)
- [GraphQL Query](#graphql-query)

## 🔄 Richiesta API Classificazione

### Request HTTP con JWT

```http
POST /api/v1/documents/classify
Host: api.zenia.local
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
X-Correlation-ID: req-123456789
X-API-Version: v1

{
  "document": {
    "id": "doc_001",
    "content": "Provvedimento di autorizzazione allo scarico di acque reflue nel fiume Po...",
    "metadata": {
      "source": "email",
      "received_at": "2025-11-18T09:30:00Z",
      "sender": "comune.milano@pec.it",
      "priority": "high",
      "type": "provvedimento_amministrativo"
    }
  },
  "options": {
    "confidence_threshold": 0.85,
    "extract_entities": true,
    "sentiment_analysis": false,
    "categories": [
      "autorizzazione_scarico_acque",
      "certificato_ambientale",
      "comunicazione_ufficiale"
    ]
  }
}
```

### Request con API Key

```http
POST /api/v1/analysis/extract
Host: api.zenia.local
X-API-Key: sk-zenia-prod-2025-abc123def456
Content-Type: application/json
X-Correlation-ID: req-987654321

{
  "content": "Si autorizza lo scarico di acque industriali nel corpo idrico...",
  "analysis_types": ["entities", "keywords", "sentiment"],
  "language": "it",
  "domain": "ambiente",
  "options": {
    "entity_types": ["PERSON", "ORG", "GPE", "DATE"],
    "keyword_min_score": 0.3,
    "max_keywords": 15
  }
}
```

## 📤 Risposta Gateway

### Risposta Successo

```json
{
  "request_id": "req-123456789",
  "correlation_id": "req-123456789",
  "timestamp": "2025-11-18T09:30:15Z",
  "processing_time_ms": 245,
  "result": {
    "category": "autorizzazione_scarico_acque",
    "confidence": 0.92,
    "subcategories": ["autorizzazione_industriale"],
    "entities": [
      {
        "text": "Comune di Milano",
        "type": "ORG",
        "confidence": 0.98,
        "position": {"start": 15, "end": 31}
      },
      {
        "text": "fiume Po",
        "type": "GPE",
        "confidence": 0.95,
        "position": {"start": 45, "end": 53}
      }
    ],
    "keywords": [
      {"word": "autorizzazione", "score": 0.95},
      {"word": "scarico", "score": 0.89},
      {"word": "acque", "score": 0.87}
    ]
  },
  "gateway_info": {
    "service": "ms01-classifier",
    "version": "1.2.0",
    "latency_ms": 12,
    "rate_limit_remaining": 987,
    "cached": false
  },
  "metadata": {
    "request_size_bytes": 2048,
    "response_size_bytes": 1536,
    "client_ip": "192.168.1.100",
    "user_agent": "ZenIA-Client/1.0"
  }
}
```

### Risposta Errore

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dati di input non validi",
    "details": {
      "field": "document.content",
      "issue": "content_required",
      "description": "Il campo content è obbligatorio"
    },
    "request_id": "req-123456789",
    "correlation_id": "req-123456789",
    "timestamp": "2025-11-18T09:30:10Z"
  },
  "gateway_info": {
    "service": "validation",
    "latency_ms": 8,
    "rate_limit_remaining": 999
  }
}
```

## ⚙️ Configurazione Routing

### Kong Declarative Config

```yaml
# kong.yml - Configurazione dichiarativa
_format_version: "3.0"

services:
  - name: classifier-service
    url: http://ms01-classifier:8080
    routes:
      - name: classifier-api
        paths:
          - /api/v1/documents
        methods: [GET, POST, PUT, DELETE]
        plugins:
          - name: jwt
            config:
              claims_to_verify: ["exp", "nbf", "iss"]
              key_claim_name: "kid"
          - name: rate-limiting
            config:
              minute: 1000
              hour: 10000
              policy: redis
              redis_host: redis
              redis_port: 6379
          - name: cors
            config:
              origins:
                - https://app.zenia.local
                - https://admin.zenia.local
              credentials: true
          - name: request-transformer
            config:
              add:
                headers:
                  - X-API-Version: v1
                  - X-Source: gateway
          - name: prometheus
            config:
              per_consumer: true
              status_code_metrics: true
              latency_metrics: true

  - name: analyzer-service
    url: http://ms02-analyzer:8081
    routes:
      - name: analyzer-api
        paths:
          - /api/v1/analysis
        methods: [POST]
        plugins:
          - name: key-auth
          - name: request-size-limiting
            config:
              allowed_payload_size: 10485760  # 10MB
          - name: response-transformer
            config:
              add:
                headers:
                  - X-Processed-By: gateway

consumers:
  - username: zenia-admin
    custom_id: admin-001
    acls:
      - group: admin
    jwt_secrets:
      - key: admin-key
        secret: admin-secret-hs256
    keyauth_credentials:
      - key: sk-admin-2025

  - username: zenia-user
    custom_id: user-001
    acls:
      - group: user
    jwt_secrets:
      - key: user-key
        secret: user-secret-hs256
    keyauth_credentials:
      - key: sk-user-2025

upstreams:
  - name: classifier-upstream
    algorithm: round-robin
    healthchecks:
      active:
        type: http
        http_path: /health
        timeout: 5
        interval: 30
        successes: 2
        failures: 3
    targets:
      - target: ms01-classifier-1:8080
        weight: 100
      - target: ms01-classifier-2:8080
        weight: 100
```

## [Auto-generated heading level 2]
### Nginx Load Balancing

```nginx
# nginx.conf - Reverse proxy configuration
upstream zenia_api {
    least_conn;
    server kong:8000 weight=5 max_fails=3 fail_timeout=30s;
    server kong-backup:8000 weight=1 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name api.zenia.local;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/zenia.crt;
    ssl_certificate_key /etc/ssl/private/zenia.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

    # Rate Limiting
    limit_req zone=api burst=20 nodelay;
    limit_req_status 429;

    # Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    location /api/v1/ {
        proxy_pass http://zenia_api;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 10s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;

        # Buffers
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Metrics
    location /metrics {
        proxy_pass http://prometheus:9090;
        allow 10.0.0.0/8;
        deny all;
    }
}
```

## 🔌 Esempio WebSocket

### Connessione Client

```javascript
// client-websocket.js
class ZenIAGatewayWS {
  constructor(url = 'wss://api.zenia.local/ws/v1/events') {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.subscriptions = new Set();
  }

  connect(token) {
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log('Connected to ZenIA Gateway');
        this.authenticate(token);
        this.reconnectAttempts = 0;
      };

      this.ws.onmessage = (event) => {
        this.handleMessage(JSON.parse(event.data));
      };

      this.ws.onclose = (event) => {
        console.log('Disconnected:', event.code, event.reason);
        this.handleReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

    } catch (error) {
      console.error('Connection failed:', error);
    }
  }

  authenticate(token) {
    this.send({
      type: 'auth',
      token: token,
      timestamp: new Date().toISOString()
    });
  }

  subscribe(channels, filter = {}) {
    const subscription = {
      type: 'subscribe',
      channels: Array.isArray(channels) ? channels : [channels],
      filter: filter,
      id: `sub_${Date.now()}`
    };

    this.send(subscription);
    this.subscriptions.add(subscription.id);
  }

  unsubscribe(subscriptionId) {
    this.send({
      type: 'unsubscribe',
      subscription_id: subscriptionId
    });
    this.subscriptions.delete(subscriptionId);
  }

  handleMessage(message) {
    console.log('Received:', message);

    switch (message.type) {
      case 'auth_success':
        console.log('Authentication successful');
        break;

      case 'subscription_success':
        console.log('Subscribed to:', message.channels);
        break;

      case 'event':
        this.handleEvent(message);
        break;

      case 'error':
        console.error('Gateway error:', message.error);
        break;

      case 'pong':
        // Heartbeat response
        break;
    }
  }

  handleEvent(event) {
    const { type, data, timestamp } = event;

    switch (type) {
      case 'workflow.status_changed':
        this.onWorkflowStatusChange(data);
        break;

      case 'document.processed':
        this.onDocumentProcessed(data);
        break;

      case 'system.alert':
        this.onSystemAlert(data);
        break;

      case 'metrics.updated':
        this.onMetricsUpdated(data);
        break;
    }
  }

  handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);

      setTimeout(() => {
        console.log(`Reconnecting (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        // Ricarica token se necessario
        const token = localStorage.getItem('zenia_token');
        if (token) {
          this.connect(token);
        }
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
      this.onMaxReconnectAttempts();
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        ...data,
        timestamp: new Date().toISOString()
      }));
    } else {
      console.warn('WebSocket not connected');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect');
    }
  }

  // Event handlers (da implementare)
  onWorkflowStatusChange(data) {
    console.log('Workflow status changed:', data);
    // Update UI
  }

  onDocumentProcessed(data) {
    console.log('Document processed:', data);
    // Update document list
  }

  onSystemAlert(data) {
    console.log('System alert:', data);
    // Show notification
  }

  onMetricsUpdated(data) {
    console.log('Metrics updated:', data);
    // Update dashboard
  }

  onMaxReconnectAttempts() {
    console.error('Failed to reconnect to Gateway');
    // Show offline message
  }
}

// Utilizzo
const gateway = new ZenIAGatewayWS();
const token = localStorage.getItem('zenia_token');

gateway.connect(token);

gateway.subscribe(['workflow.updates', 'document.processed'], {
  severity: 'high',
  services: ['ms01-classifier', 'ms02-analyzer']
});

// Cleanup
window.addEventListener('beforeunload', () => {
  gateway.disconnect();
});
```

### Eventi WebSocket

**Workflow Status Changed Event:**
```json
{
  "type": "event",
  "event_type": "workflow.status_changed",
  "id": "evt_123456",
  "timestamp": "2025-11-18T10:30:00Z",
  "correlation_id": "wf_789012",
  "data": {
    "workflow_id": "wf_789012",
    "status": "completed",
    "stage": "classification",
    "progress": 100,
    "result": {
      "category": "autorizzazione_scarico_acque",
      "confidence": 0.92
    },
    "processing_time_ms": 2450,
    "completed_at": "2025-11-18T10:30:00Z"
  }
}
```

**System Alert Event:**
```json
{
  "type": "event",
  "event_type": "system.alert",
  "id": "evt_123457",
  "timestamp": "2025-11-18T10:35:00Z",
  "correlation_id": "alert_345678",
  "data": {
    "alert_id": "alert_345678",
    "severity": "warning",
    "service": "ms01-classifier",
    "message": "High latency detected: 95th percentile > 2s",
    "details": {
      "metric": "request_duration_p95",
      "threshold": 2000,
      "current_value": 2450,
      "time_window": "5m"
    },
    "recommendations": [
      "Check upstream service health",
      "Review rate limiting configuration",
      "Consider scaling service instances"
    ]
  }
}
```

## [Auto-generated heading level 2]
### Variables e Risposta

```json
{
  "filter": {
    "category": "autorizzazione",
    "status": "processed",
    "dateFrom": "2025-11-01T00:00:00Z",
    "dateTo": "2025-11-18T23:59:59Z",
    "confidence": {
      "min": 0.8
    },
    "source": [
      "email",
      "upload"
    ],
    "tags": [
      "high_priority"
    ]
  },
  "pagination": {
    "first": 20,
    "after": "cursor_abc123"
  }
}
```

---

**📖 Vedi Anche**: [API.md](../API.md) | [SPECIFICATION.md](../SPECIFICATION.md)
