# API - MS16-REGISTRY

## Endpoints Principali

### 1. Registra Servizio
- **POST** `/api/registry/service`
- **Autenticazione**: Bearer JWT
- **Body**:
```json
{
  "name": "ms11-api-gateway",
  "address": "10.0.0.11",
  "port": 8080,
  "tags": ["api", "gateway"],
  "health_url": "http://10.0.0.11:8080/health"
}
```
- **Risposta**: `201 Created` / `400 Bad Request`

### 2. Lista Servizi
- **GET** `/api/registry/services`
- **Autenticazione**: Bearer JWT
- **Risposta**:
```json
[
  {
    "name": "ms11-api-gateway",
    "address": "10.0.0.11",
    "port": 8080,
    "tags": ["api", "gateway"],
    "status": "healthy"
  }
]
```

### 3. Health Check
- **GET** `/api/registry/health/{name}`
- **Autenticazione**: Bearer JWT
- **Risposta**:
```json
{
  "name": "ms11-api-gateway",
  "status": "healthy",
  "last_check": "2025-11-19T10:15:00Z"
}
```

### 4. Deregistra Servizio
- **DELETE** `/api/registry/service/{name}`
- **Autenticazione**: Bearer JWT, RBAC
- **Risposta**: `200 OK` / `404 Not Found`

### 5. Notifiche Eventi
- **GET** `/api/registry/events/subscribe`
- **Autenticazione**: Bearer JWT
- **Risposta**: Stream eventi push (SSE/WebSocket)

### 6. Metriche Prometheus
- **GET** `/metrics`
- **Risposta**: Prometheus exposition format

## Sicurezza API
- Tutte le chiamate protette da JWT
- RBAC su deregistrazione
- Rate limiting e logging accessi

## OpenAPI
- Documentazione OpenAPI 3.0 disponibile su `/docs`
