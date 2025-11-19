# DATABASE-SCHEMA - MS12-CACHE

## Redis Structure

### 1. Chiavi principali
- `cache:<namespace>:<key>`: dati cache
- `session:<session_id>`: dati sessione
- `ratelimit:<service>:<ip>`: contatori rate limit
- `pubsub:<channel>`: canali eventi

### 2. Esempi di struttura

**Cache Entry**:
```json
{
  "key": "cache:ms01:document:123",
  "value": {"class": "A", "score": 0.98},
  "expires_at": "2025-11-19T12:00:00Z"
}
```

**Session Entry**:
```json
{
  "key": "session:abc123",
  "user_id": "u001",
  "jwt": "...",
  "expires_at": "2025-11-19T12:00:00Z"
}
```

**Rate Limit Entry**:
```json
{
  "key": "ratelimit:ms11-gateway:ip:1.2.3.4",
  "count": 42,
  "reset_at": "2025-11-19T12:10:00Z"
}
```

### 3. Policy di retention
- TTL configurabile per ogni chiave
- Sessioni: 1h-24h
- Cache: 5m-24h
- Rate limit: 1m-1h

### 4. Sicurezza dati
- Password e ACL su ogni comando
- TLS obbligatorio
- Audit log per accessi e modifiche

---

**Vedi anche**: [README.md](./README.md) | [SPECIFICATION.md](./SPECIFICATION.md) | [API.md](./API.md) | [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
