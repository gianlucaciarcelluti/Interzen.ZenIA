# API - MS14-AUDIT

## Endpoints Principali

### 1. Invia Log di Audit
- **POST** `/api/audit/log`
- **Autenticazione**: Bearer JWT
- **Body**:
```json
{
  "timestamp": "2025-11-19T10:15:00Z",
  "user": "utente1",
  "ip": "192.168.1.10",
  "action": "LOGIN",
  "resource": "MS11-API-GATEWAY",
  "outcome": "SUCCESS",
  "details": {"browser": "Chrome"}
}
```
- **Risposta**: `201 Created` / `400 Bad Request`

### 2. Ricerca Log
- **GET** `/api/audit/search`
- **Query**: `user`, `action`, `from`, `to`, `outcome`, `resource`
- **Autenticazione**: Bearer JWT, RBAC
- **Risposta**:
```json
[
  {
    "timestamp": "2025-11-19T10:15:00Z",
    "user": "utente1",
    "ip": "192.168.1.10",
    "action": "LOGIN",
    "resource": "MS11-API-GATEWAY",
    "outcome": "SUCCESS",
    "details": {"browser": "Chrome"}
  }
]
```

### 3. Esportazione Log
- **GET** `/api/audit/export`
- **Query**: `format=csv|json`, `from`, `to`
- **Autenticazione**: Bearer JWT, RBAC
- **Risposta**: File esportato

### 4. Metriche Prometheus
- **GET** `/metrics`
- **Risposta**: Prometheus exposition format

### 5. Forwarding/Alert
- **POST** `/api/audit/alert`
- **Body**: Evento critico
- **Autenticazione**: Interna (service account)

## Sicurezza API
- Tutte le chiamate protette da JWT
- RBAC su ricerca/esportazione
- Rate limiting e logging accessi

## OpenAPI
- Documentazione OpenAPI 3.0 disponibile su `/docs`
