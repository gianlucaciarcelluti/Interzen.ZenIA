# API Reference - MS07-DISTRIBUTOR

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms07--distributor)

## Panoramica API

MS07-DISTRIBUTOR espone un'API RESTful per la gestione delle distribuzioni di dati aggregati. L'API supporta autenticazione JWT e API keys, con rate limiting e comprehensive error handling.

**Base URL**: `https://ms07-distributor.zenia.local/api/v1`

**Autenticazione**: Bearer Token (JWT) o API Key header

## Endpoint Principali

### 1. Distribuzione Dati

#### 1.1 Submit Distribution
Invia una richiesta di distribuzione ai consumer configurati.

```http
POST /distribution/submit
Content-Type: application/json
Authorization: Bearer {jwt_token}
X-API-Key: {api_key}
```

**Request Body**:
```json
{
  "tenant_id": "tenant-123",
  "data_type": "aggregated_report",
  "priority": "normal",
  "payload": {
    "report_id": "rpt-456",
    "period": "2024-01-15",
    "data": {
      "total_documents": 1250,
      "processed_documents": 1245,
      "failed_documents": 5,
      "processing_time_ms": 45000,
      "accuracy_score": 0.987
    },
    "metadata": {
      "source_system": "ms06-aggregator",
      "batch_id": "batch-789",
      "quality_score": 0.95
    }
  },
  "destinations": [
    {
      "name": "ms09-reporter",
      "protocol": "REST",
      "endpoint": "https://ms09.zenia.local/api/reports",
      "method": "POST",
      "headers": {
        "Content-Type": "application/json"
      },
      "transform": "report_format_v1"
    },
    {
      "name": "data-lake",
      "protocol": "S3",
      "bucket": "zenia-reports",
      "key": "reports/2024/01/15/report-456.json",
      "region": "eu-south-1"
    }
  ],
  "options": {
    "callback_url": "https://webhook.example.com/distribution/callback",
    "timeout_seconds": 300,
    "max_retries": 3,
    "idempotency_key": "dist-2024-01-15-456"
  }
}
```

**Response**:
```json
{
  "distribution_id": "dist-uuid-123",
  "status": "accepted",
  "estimated_completion": "2024-01-15T10:05:00Z",
  "destinations_count": 2,
  "tracking_url": "/distribution/dist-uuid-123/status",
  "callback_registered": true
}
```

**Error Responses**:

**400 Bad Request - Validation Error**:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid destination configuration",
  "details": {
    "field": "destinations[0].endpoint",
    "issue": "Invalid URL format"
  }
}
```

**401 Unauthorized**:
```json
{
  "error": "AUTHENTICATION_FAILED",
  "message": "Invalid or expired token"
}
```

**429 Too Many Requests**:
```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded",
  "retry_after_seconds": 60
}
```

#### 1.2 Bulk Distribution
Invia multiple distribuzioni in un singolo batch.

```http
POST /distribution/bulk-submit
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "tenant_id": "tenant-123",
  "distributions": [
    {
      "data_type": "daily_report",
      "payload": {},
      "destinations": []
    },
    {
      "data_type": "weekly_summary",
      "payload": {},
      "destinations": []
    }
  ],
  "options": {
    "parallel_execution": true,
    "fail_fast": false,
    "callback_url": "https://webhook.example.com/bulk/callback"
  }
}
```

**Response**:
```json
{
  "batch_id": "batch-uuid-789",
  "total_distributions": 2,
  "accepted_distributions": 2,
  "distribution_ids": [
    "dist-uuid-123",
    "dist-uuid-124"
  ],
  "status": "processing",
  "tracking_url": "/distribution/batch/batch-uuid-789/status"
}
```

### 2. Monitoraggio Distribuzioni

#### 2.1 Get Distribution Status
Recupera lo stato di una distribuzione specifica.

```http
GET /distribution/{distribution_id}/status
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "distribution_id": "dist-uuid-123",
  "tenant_id": "tenant-123",
  "status": "completed",
  "priority": "normal",
  "submitted_at": "2024-01-15T10:00:00Z",
  "started_at": "2024-01-15T10:00:05Z",
  "completed_at": "2024-01-15T10:00:30Z",
  "progress_percentage": 100,
  "destinations": [
    {
      "name": "ms09-reporter",
      "status": "success",
      "attempts": 1,
      "started_at": "2024-01-15T10:00:10Z",
      "completed_at": "2024-01-15T10:00:15Z",
      "response_time_ms": 5000,
      "response_status": 200,
      "error_message": null
    },
    {
      "name": "data-lake",
      "status": "success",
      "attempts": 1,
      "started_at": "2024-01-15T10:00:20Z",
      "completed_at": "2024-01-15T10:00:25Z",
      "response_time_ms": 3000,
      "response_status": 200,
      "error_message": null
    }
  ],
  "metrics": {
    "total_latency_ms": 30000,
    "average_response_time_ms": 4000,
    "success_rate": 1.0,
    "retry_count": 0
  }
}
```

#### 2.2 Get Batch Status
Recupera lo stato di un batch di distribuzioni.

```http
GET /distribution/batch/{batch_id}/status
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "batch_id": "batch-uuid-789",
  "status": "completed",
  "total_distributions": 2,
  "completed_distributions": 2,
  "failed_distributions": 0,
  "submitted_at": "2024-01-15T10:00:00Z",
  "completed_at": "2024-01-15T10:01:00Z",
  "distributions": [
    {
      "distribution_id": "dist-uuid-123",
      "status": "completed",
      "destinations_count": 2,
      "success_count": 2,
      "failure_count": 0
    },
    {
      "distribution_id": "dist-uuid-124",
      "status": "completed",
      "destinations_count": 1,
      "success_count": 1,
      "failure_count": 0
    }
  ],
  "summary": {
    "total_destinations": 3,
    "successful_destinations": 3,
    "failed_destinations": 0,
    "average_completion_time_ms": 45000
  }
}
```

#### 2.3 List Distributions
Elenco distribuzioni con filtri e paginazione.

```http
GET /distribution/list?tenant_id=tenant-123&status=completed&limit=50&offset=0
Authorization: Bearer {jwt_token}
```

**Query Parameters**:
- `tenant_id`: Filtra per tenant
- `status`: Filtra per stato (pending, processing, completed, failed)
- `data_type`: Filtra per tipo dati
- `from_date`: Data inizio (ISO 8601)
- `to_date`: Data fine (ISO 8601)
- `limit`: Numero risultati (max 1000)
- `offset`: Offset per paginazione

**Response**:
```json
{
  "distributions": [
    {
      "distribution_id": "dist-uuid-123",
      "tenant_id": "tenant-123",
      "status": "completed",
      "data_type": "aggregated_report",
      "submitted_at": "2024-01-15T10:00:00Z",
      "completed_at": "2024-01-15T10:00:30Z",
      "destinations_count": 2,
      "success_count": 2,
      "failure_count": 0
    }
  ],
  "pagination": {
    "total_count": 1250,
    "limit": 50,
    "offset": 0,
    "has_more": true
  },
  "summary": {
    "total_distributions": 1250,
    "completed_distributions": 1200,
    "failed_distributions": 50,
    "success_rate": 0.96
  }
}
```

### 3. Configurazione Destinazioni

#### 3.1 Register Destination
Registra una nuova destinazione per le distribuzioni.

```http
POST /destinations/register
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**Request Body**:
```json
{
  "name": "external-analytics-api",
  "description": "External analytics platform API",
  "protocol": "REST",
  "configuration": {
    "endpoint": "https://analytics.example.com/api/data",
    "method": "POST",
    "headers": {
      "Authorization": "Bearer {token}",
      "Content-Type": "application/json"
    },
    "timeout_seconds": 30,
    "retry_policy": {
      "max_attempts": 3,
      "backoff_multiplier": 2.0
    }
  },
  "transform_config": {
    "input_format": "zenia_standard",
    "output_format": "analytics_v2",
    "field_mapping": {
      "report_id": "document_id",
      "data.total_documents": "total_count"
    }
  },
  "health_check": {
    "endpoint": "https://analytics.example.com/health",
    "interval_seconds": 60,
    "timeout_seconds": 10
  },
  "tags": ["analytics", "external", "production"]
}
```

**Response**:
```json
{
  "destination_id": "dest-uuid-456",
  "name": "external-analytics-api",
  "status": "active",
  "registered_at": "2024-01-15T09:00:00Z",
  "last_health_check": "2024-01-15T09:00:00Z",
  "health_status": "healthy"
}
```

#### 3.2 Update Destination
Aggiorna la configurazione di una destinazione esistente.

```http
PUT /destinations/{destination_id}
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

#### 3.3 List Destinations
Elenco destinazioni configurate con filtri.

```http
GET /destinations/list?status=active&protocol=REST
Authorization: Bearer {jwt_token}
```

**Response**:
```json
{
  "destinations": [
    {
      "destination_id": "dest-uuid-456",
      "name": "external-analytics-api",
      "protocol": "REST",
      "status": "active",
      "health_status": "healthy",
      "last_used": "2024-01-15T10:00:00Z",
      "usage_count": 1250,
      "tags": ["analytics", "external"]
    }
  ],
  "pagination": {
    "total_count": 15,
    "limit": 50,
    "offset": 0
  }
}
```

### 4. Callback e Webhook

#### 4.1 Distribution Callback
MS07 invia callback quando una distribuzione è completata.

```http
POST {callback_url}
Content-Type: application/json
X-Zenia-Signature: {signature}
```

**Request Body**:
```json
{
  "event_type": "distribution.completed",
  "distribution_id": "dist-uuid-123",
  "tenant_id": "tenant-123",
  "status": "completed",
  "completed_at": "2024-01-15T10:00:30Z",
  "destinations": [
    {
      "name": "ms09-reporter",
      "status": "success",
      "response_time_ms": 5000
    }
  ],
  "metrics": {
    "total_latency_ms": 30000,
    "success_rate": 1.0
  }
}
```

#### 4.2 Batch Callback
Callback per completion di un batch.

```http
POST {callback_url}
Content-Type: application/json
X-Zenia-Signature: {signature}
```

**Request Body**:
```json
{
  "event_type": "batch.completed",
  "batch_id": "batch-uuid-789",
  "status": "completed",
  "completed_at": "2024-01-15T10:01:00Z",
  "summary": {
    "total_distributions": 2,
    "completed_distributions": 2,
    "failed_distributions": 0,
    "success_rate": 1.0
  }
}
```

### 5. Health e Monitoring

#### 5.1 Health Check
Verifica lo stato di salute del servizio.

```http
GET /health/live
GET /health/ready
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.2.3",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "queue": "healthy",
    "workers": "healthy"
  }
}
```

#### 5.2 Metrics
Endpoint Prometheus per metriche.

```http
GET /metrics
```

**Response** (formato Prometheus):
```
# HELP zenia_distribution_requests_total Total distribution requests
# TYPE zenia_distribution_requests_total counter
zenia_distribution_requests_total{tenant_id="tenant-123",status="success"} 1250

# HELP zenia_distribution_latency_seconds Distribution latency in seconds
# TYPE zenia_distribution_latency_seconds histogram
zenia_distribution_latency_seconds_bucket{le="0.1"} 0
zenia_distribution_latency_seconds_bucket{le="0.5"} 950
zenia_distribution_latency_seconds_bucket{le="1.0"} 1200
```

### 6. Sicurezza e Autenticazione

#### 6.1 JWT Authentication
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 6.2 API Key Authentication
```http
X-API-Key: zk_1a2b3c4d5e6f7890abcdef1234567890
```

#### 6.3 Rate Limiting
- **Per tenant**: 1000 richieste/minuto
- **Per API key**: 100 richieste/minuto
- **Burst limit**: 200 richieste per burst

### 7. Error Handling

#### 7.1 Error Response Format
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "details": {
    "field": "destinations[0].endpoint",
    "issue": "URL scheme must be https"
  },
  "request_id": "req-uuid-123",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

#### 7.2 Common Error Codes
- `VALIDATION_ERROR`: Dati input non validi
- `AUTHENTICATION_FAILED`: Credenziali non valide
- `AUTHORIZATION_FAILED`: Permessi insufficienti
- `RATE_LIMIT_EXCEEDED`: Limite richieste superato
- `DESTINATION_UNAVAILABLE`: Destinazione non raggiungibile
- `TRANSFORMATION_FAILED`: Errore trasformazione dati
- `INTERNAL_ERROR`: Errore interno del sistema

### 8. SDK e Client Libraries

#### 8.1 Python Client
```python
from zenia_distributor import DistributorClient

client = DistributorClient(
    base_url="https://ms07-distributor.zenia.local",
    api_key="zk_1a2b3c4d5e6f7890abcdef1234567890"
)

# Submit distribution
response = client.submit_distribution({
    "tenant_id": "tenant-123",
    "data_type": "aggregated_report",
    "payload": {...},
    "destinations": [...]
})

# Check status
status = client.get_distribution_status(response["distribution_id"])
```

#### 8.2 JavaScript Client
```javascript
import { DistributorClient } from '@zenia/distributor-client';

const client = new DistributorClient({
  baseURL: 'https://ms07-distributor.zenia.local',
  apiKey: 'zk_1a2b3c4d5e6f7890abcdef1234567890'
});

// Submit distribution
const response = await client.submitDistribution({
  tenantId: 'tenant-123',
  dataType: 'aggregated_report',
  payload: {...},
  destinations: [...]
});

// Check status with polling
const status = await client.pollDistributionStatus(
  response.distributionId,
  { intervalMs: 5000, timeoutMs: 300000 }
);
```

### 9. Versioning e Compatibility

#### 9.1 API Versioning
- **Current Version**: v1
- **Version Header**: `Accept: application/vnd.zenia.distributor.v1+json`
- **Deprecation Policy**: 12 mesi notice per breaking changes

#### 9.2 Backward Compatibility
- **Additive Changes**: Nuovi campi opzionali sempre backward compatible
- **Breaking Changes**: Solo in nuove major version
- **Migration Guide**: Fornito per ogni major version upgrade

### 10. Best Practices

#### 10.1 Ottimizzazione Performance
- **Batch Submissions**: Usa bulk-submit per multiple distribuzioni
- **Idempotency Keys**: Implementa per evitare duplicati
- **Callback URLs**: Usa per notifiche asincrone invece di polling
- **Compression**: Abilita gzip per payload grandi

#### 10.2 Error Handling
- **Retry Logic**: Implementa exponential backoff client-side
- **Circuit Breaker**: Monitora failure rate e interrompi richieste
- **Fallback**: Prevedi strategie alternative per destination failure
- **Logging**: Log completo per troubleshooting

#### 10.3 Monitoring
- **Metrics Collection**: Monitora latency, throughput, error rate
- **Alert Configuration**: Setup alert per SLA violations
- **Dashboard**: Crea dashboard per monitoring real-time
- **Audit Trail**: Mantieni log completo per compliance