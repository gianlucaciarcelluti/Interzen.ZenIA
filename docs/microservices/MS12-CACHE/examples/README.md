# Esempi d'Uso - MS12-CACHE

Questa directory contiene esempi di payload, configurazioni e comandi per l'utilizzo di MS12-CACHE (Redis Cluster).

## 1. Cache API
```json
{
  "key": "cache:ms01:document:123",
  "value": {"class": "A", "score": 0.98},
  "expires_at": "2025-11-19T12:00:00Z"
}
```

## 2. Session Store
```json
{
  "key": "session:abc123",
  "user_id": "u001",
  "jwt": "...",
  "expires_at": "2025-11-19T12:00:00Z"
}
```

## 3. Rate Limiting
```json
{
  "key": "ratelimit:ms11-gateway:ip:1.2.3.4",
  "count": 42,
  "reset_at": "2025-11-19T12:10:00Z"
}
```

## 4. Pub/Sub
```json
{
  "channel": "events",
  "message": {"type": "update", "entity": "document", "id": "123"}
}
