# API - MS15-CONFIG

## Endpoints Principali

### 1. Recupera Configurazione
- **GET** `/api/config/{service}`
- **Autenticazione**: Bearer JWT
- **Risposta**:
```json
{
  "service": "MS11-API-GATEWAY",
  "version": 5,
  "config": {"timeout": 30, "logLevel": "INFO"},
  "updated_at": "2025-11-19T10:15:00Z"
}
```

### 2. Aggiorna Configurazione
- **PUT** `/api/config/{service}`
- **Autenticazione**: Bearer JWT, RBAC
- **Body**:
```json
{
  "config": {"timeout": 60, "logLevel": "DEBUG"},
  "note": "Aumentato timeout"
}
```
- **Risposta**: `200 OK` / `400 Bad Request`

### 3. Storico Versioni
- **GET** `/api/config/{service}/history`
- **Autenticazione**: Bearer JWT, RBAC
- **Risposta**:
```json
[
  {"version": 5, "updated_at": "2025-11-19T10:15:00Z", "user": "admin"},
  {"version": 4, "updated_at": "2025-11-18T09:00:00Z", "user": "admin"}
]
```

### 4. Rollback Configurazione
- **POST** `/api/config/{service}/rollback`
- **Body**: `{ "version": 4 }`
- **Autenticazione**: Bearer JWT, RBAC
- **Risposta**: `200 OK` / `400 Bad Request`

### 5. Notifiche Eventi
- **GET** `/api/config/events/subscribe`
- **Autenticazione**: Bearer JWT
- **Risposta**: Stream eventi push (SSE/WebSocket)

### 6. Metriche Prometheus
- **GET** `/metrics`
- **Risposta**: Prometheus exposition format

## Sicurezza API
- Tutte le chiamate protette da JWT
- RBAC su update/rollback
- Rate limiting e logging accessi

## OpenAPI
- Documentazione OpenAPI 3.0 disponibile su `/docs`
