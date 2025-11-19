# API - MS12-CACHE

## API Redis (standard)
MS12-CACHE espone le API Redis standard (RESP, TCP/SSL, porta 6379/6380) e supporta:
- GET/SET/DEL/EXPIRE
- MGET/MSET
- HGET/HSET/HDEL
- INCR/DECR
- PUB/SUB
- ACL, AUTH

## Esempi di utilizzo

### 1. Cache-aside pattern
```python
# Python (redis-py)
import redis
r = redis.Redis(host='ms12-cache.zenia.svc.cluster.local', port=6379, password='...')
value = r.get('mykey')
if value is None:
    value = calcola_valore()
    r.set('mykey', value, ex=3600)
```

### 2. Session store
```json
{
  "session_id": "abc123",
  "user_id": "u001",
  "expires_at": "2025-11-19T12:00:00Z",
  "data": {"jwt": "..."}
}
```

### 3. Rate limiting
```json
{
  "key": "ratelimit:ms11-gateway:ip:1.2.3.4",
  "count": 42,
  "reset_at": "2025-11-19T12:10:00Z"
}
```

### 4. Pub/Sub
```python
# Pub/Sub esempio
p = r.pubsub()
p.subscribe('events')
for msg in p.listen():
    print(msg)
```

## Sicurezza API
- Solo accesso autenticato (password/ACL)
- TLS obbligatorio
- Audit log per comandi critici

---

**Vedi anche**: [README.md](./README.md) | [SPECIFICATION.md](./SPECIFICATION.md) | [DATABASE-SCHEMA.md](./DATABASE-SCHEMA.md) | [TROUBLESHOUTING.md](./TROUBLESHOUTING.md)
