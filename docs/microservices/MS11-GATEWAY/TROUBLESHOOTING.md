# MS11-GATEWAY - Troubleshooting Guide

> **Guida alla Risoluzione Problemi per API Gateway ZenIA**

[![Kong](https://img.shields.io/badge/Kong-%23000000.svg?style=flat&logo=kong&logoColor=white)](https://konghq.com)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=flat&logo=nginx&logoColor=white)](https://nginx.org)
[![Redis](https://img.shields.io/badge/Redis-%23DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io)

## 🚨 Problemi Comuni e Soluzioni

### 1. Gateway Inaccessibile (502 Bad Gateway)

**Sintomi:**
- Richieste API restituiscono `502 Bad Gateway`
- Kong non risponde sulla porta 8000
- Upstream services raggiungibili direttamente

**Diagnosi:**
```bash
# Verifica status Kong
docker-compose ps kong

# Controlla logs Kong
docker-compose logs kong | tail -50

# Test connessione upstream
curl -v http://localhost:8081/api/v1/classifier/health

# Verifica configurazione Kong
curl http://localhost:8001/status
```

**Soluzioni:**

**Kong non avviato:**
```bash
# Riavvia Kong
docker-compose restart kong

# Verifica database connection
docker-compose exec kong kong config -c /etc/kong/kong.conf
```

**Database PostgreSQL non disponibile:**
```bash
# Verifica PostgreSQL
docker-compose ps postgres
docker-compose logs postgres

# Test connessione DB
docker-compose exec kong psql -h postgres -U kong -d kong -c "SELECT 1;"
```

**Configurazione Kong corrotta:**
```bash
# Backup configurazione attuale
docker-compose exec kong kong config -c /etc/kong/kong.conf > kong_backup.conf

# Reset configurazione
docker-compose exec kong kong config db_import /dev/null

# Ricarica configurazione
docker-compose restart kong
```

## [Auto-generated heading level 2]
### 2. Autenticazione Fallita (401 Unauthorized)

**Sintomi:**
- `401 Unauthorized` per richieste autenticate
- JWT tokens rifiutati
- API keys non riconosciute

**Diagnosi:**
```bash
# Verifica JWT token
curl -H "Authorization: Bearer <token>" \
     http://localhost:8001/debug/jwt

# Controlla consumer
curl http://localhost:8001/consumers

# Verifica plugin JWT attivi
curl http://localhost:8001/plugins | jq '.data[] | select(.name=="jwt")'
```

**Soluzioni:**

**JWT Secret mancante:**
```bash
# Aggiungi JWT credential al consumer
curl -X POST http://localhost:8001/consumers/{consumer-id}/jwt \
  -d "algorithm=HS256" \
  -d "secret=your-secret-key"
```

**API Key non configurata:**
```bash
# Crea API key per consumer
curl -X POST http://localhost:8001/consumers/{consumer-id}/key-auth \
  -d "key=your-api-key"
```

**Plugin non abilitato sulla route:**
```bash
# Verifica plugin sulla route
curl http://localhost:8001/routes/{route-id}/plugins

# Aggiungi plugin JWT
curl -X POST http://localhost:8001/routes/{route-id}/plugins \
  -d "name=jwt" \
  -d "config.claims_to_verify=exp,nbf"
```

## [Auto-generated heading level 2]
### 3. Rate Limiting Superato (429 Too Many Requests)

**Sintomi:**
- `429 Too Many Requests`
- Headers rate limit mostrano limite raggiunto
- Richieste rallentate artificialmente

**Diagnosi:**
```bash
# Verifica rate limiting headers
curl -I http://localhost:8000/api/v1/test

# Controlla counters Redis
docker-compose exec redis redis-cli KEYS "ratelimit:*"

# Vedi configurazione plugin
curl http://localhost:8001/plugins | jq '.data[] | select(.name=="rate-limiting")'
```

**Soluzioni:**

**Aumenta limiti rate limiting:**
```bash
# Modifica configurazione plugin
curl -X PATCH http://localhost:8001/plugins/{plugin-id} \
  -d "config.minute=2000" \
  -d "config.hour=20000"
```

**Reset counters Redis:**
```bash
# Flush rate limiting keys
docker-compose exec redis redis-cli KEYS "ratelimit:*" | xargs redis-cli DEL
```

**Configura rate limiting per consumer:**
```bash
# Rate limiting specifico per consumer
curl -X POST http://localhost:8001/consumers/{consumer-id}/plugins \
  -d "name=rate-limiting" \
  -d "config.minute=5000"
```

## [Auto-generated heading level 2]
### 4. Routing Non Funzionante (404 Not Found)

**Sintomi:**
- `404 Not Found` per endpoint esistenti
- Routing non corrisponde ai path configurati
- Upstream services non raggiunti

**Diagnosi:**
```bash
# Lista routes configurate
curl http://localhost:8001/routes

# Verifica path matching
curl http://localhost:8001/routes | jq '.data[] | {name, paths, service}'

# Test route matching
curl -H "X-Test-Request: true" http://localhost:8000/debug/route
```

**Soluzioni:**

**Route non configurata:**
```bash
# Crea route per servizio
curl -X POST http://localhost:8001/routes \
  -d "service.id={service-id}" \
  -d "paths[]=/api/v1/new-endpoint" \
  -d "methods[]=GET" \
  -d "methods[]=POST"
```

**Path matching errato:**
```bash
# Aggiorna path route
curl -X PATCH http://localhost:8001/routes/{route-id} \
  -d "paths[]=/api/v1/correct-path"
```

**Service upstream non configurato:**
```bash
# Verifica servizio
curl http://localhost:8001/services/{service-id}

# Aggiorna URL servizio
curl -X PATCH http://localhost:8001/services/{service-id} \
  -d "url=http://correct-upstream:8080"
```

## [Auto-generated heading level 2]
### 5. Performance Degradation (Timeout/Latency Alta)

**Sintomi:**
- Timeout nelle risposte API
- Latenza > 5 secondi
- Throughput ridotto

**Diagnosi:**
```bash
# Verifica metriche Kong
curl http://localhost:8001/metrics

# Controlla upstream health
curl http://localhost:8001/upstreams/{upstream-id}/health

# Monitora Redis performance
docker-compose exec redis redis-cli INFO stats
```

**Soluzioni:**

**Timeout upstream:**
```bash
# Aumenta timeout servizio
curl -X PATCH http://localhost:8001/services/{service-id} \
  -d "read_timeout=120000" \
  -d "write_timeout=120000"
```

**Load balancing issues:**
```bash
# Verifica upstream targets
curl http://localhost:8001/upstreams/{upstream-id}/targets

# Aggiungi target healthy
curl -X POST http://localhost:8001/upstreams/{upstream-id}/targets \
  -d "target=new-upstream:8080" \
  -d "weight=100"
```

**Cache non funzionante:**
```bash
# Verifica plugin cache
curl http://localhost:8001/plugins | jq '.data[] | select(.name=="proxy-cache")'

# Clear cache Redis
docker-compose exec redis redis-cli FLUSHDB
```

## [Auto-generated heading level 2]
### 6. SSL/TLS Problemi

**Sintomi:**
- Errori SSL handshake
- Certificati rifiutati
- Mixed content warnings

**Diagnosi:**
```bash
# Verifica certificati
curl -v https://localhost:8443/

# Controlla configurazione SSL
openssl s_client -connect localhost:8443 -servername localhost

# Verifica SNI
curl http://localhost:8001/certificates
```

**Soluzioni:**

**Certificato scaduto:**
```bash
# Aggiorna certificato
curl -X PATCH http://localhost:8001/certificates/{cert-id} \
  -d "cert=$(cat new_cert.pem)" \
  -d "key=$(cat new_key.pem)"
```

**SNI non configurato:**
```bash
# Crea SNI mapping
curl -X POST http://localhost:8001/snis \
  -d "name=api.zenia.local" \
  -d "certificate.id={cert-id}"
```

## [Auto-generated heading level 2]
### 7. Plugin Non Funzionanti

**Sintomi:**
- Plugin non applicati alle richieste
- Configurazione plugin ignorata
- Errori plugin nei logs

**Diagnosi:**
```bash
# Lista plugin attivi
curl http://localhost:8001/plugins

# Verifica configurazione plugin
curl http://localhost:8001/plugins/{plugin-id}

# Controlla logs plugin
docker-compose logs kong | grep plugin
```

**Soluzioni:**

**Plugin non abilitato:**
```bash
# Abilita plugin su route
curl -X POST http://localhost:8001/routes/{route-id}/plugins \
  -d "name=cors" \
  -d "config.origins=http://localhost:3000"
```

**Configurazione plugin errata:**
```bash
# Correggi configurazione
curl -X PATCH http://localhost:8001/plugins/{plugin-id} \
  -d "config.allow_credentials=true"
```

## 🔍 Debug Tools

### Kong Debug Mode

```bash
# Abilita debug logging
export KONG_LOG_LEVEL=debug
docker-compose up kong

# Debug specifico plugin
curl -X POST http://localhost:8001/debug \
  -d "plugin=jwt" \
  -d "request.headers.Authorization=Bearer <token>"
```

## [Auto-generated heading level 2]
### Request Tracing

```bash
# Abilita correlation ID
curl -H "X-Correlation-ID: trace-123" \
     http://localhost:8000/api/v1/test

# Cerca nei logs
docker-compose logs | grep "trace-123"
```

## [Auto-generated heading level 2]
### Performance Profiling

```bash
# Abilita profiling Kong
export KONG_LUA_PROFILER=on
docker-compose restart kong

# Ottieni profile
curl http://localhost:8001/debug/profile
```

## 📊 Monitoraggio e Alerting

### Metriche Chiave da Monitorare

```prometheus
# Error rate per servizio
rate(kong_http_requests_total{status=~"5.."}[5m]) /
rate(kong_http_requests_total[5m]) > 0.05

# Latenza P95
histogram_quantile(0.95, rate(kong_http_request_duration_ms_bucket[5m]))

# Rate limiting violations
increase(kong_ratelimit_usage{limit_exceeded="true"}[5m])

# Upstream health
kong_upstream_healthy == 0
```

## [Auto-generated heading level 2]
### Log Analysis

```bash
# Error patterns
docker-compose logs kong | grep ERROR | tail -20

# Slow requests
docker-compose logs kong | grep "request_time" | awk '$NF > 5'

# Failed authentications
docker-compose logs kong | grep "401" | wc -l
```

## 🚨 Procedure di Emergenza

### Rollback Configurazione

```bash
# Backup configurazione attuale
curl http://localhost:8001/config > kong_config_backup.json

# Ripristina da backup
curl -X POST http://localhost:8001/config \
  -H "Content-Type: application/json" \
  -d @kong_config_backup.json
```

## [Auto-generated heading level 2]
### Failover Upstream

```bash
# Disabilita upstream problematico
curl -X PATCH http://localhost:8001/upstreams/{upstream-id}/targets/{target-id} \
  -d "weight=0"

# Abilita backup upstream
curl -X POST http://localhost:8001/upstreams/{upstream-id}/targets \
  -d "target=backup-upstream:8080" \
  -d "weight=100"
```

## [Auto-generated heading level 2]
### Emergency Shutdown

```bash
# Stop Kong gracefully
docker-compose exec kong kong quit

# Force stop se necessario
docker-compose kill kong

# Start in maintenance mode
docker-compose up -d nginx-maintenance
```

## 📞 Supporto e Escalation

### Livelli di Supporto

| Livello | Descrizione | SLA |
|---------|-------------|-----|
| **L1** | Troubleshooting base, restart services | 15 minuti |
| **L2** | Configurazione avanzata, plugin issues | 1 ora |
| **L3** | Problemi architetturali, custom development | 4 ore |

### Contatti di Supporto

- **Email**: support@gateway.zenia.local
- **Slack**: #gateway-support
- **PagerDuty**: +39 123 456 7890

### Escalation Matrix

```
Problema rilevato → L1 (15min) → L2 (1h) → L3 (4h) → Management
     ↓                     ↓         ↓         ↓
  Auto-recovery        Manual fix  Code fix  Business decision
```

## 📋 Checklist Troubleshooting

### Pre-Investigazione
- [ ] Ambiente corretto (dev/staging/prod)?
- [ ] Versione Kong compatibile?
- [ ] Database PostgreSQL raggiungibile?
- [ ] Redis cache funzionante?
- [ ] Upstream services healthy?

### Durante l'Analisi
- [ ] Logs Kong esaminati?
- [ ] Metriche Prometheus controllate?
- [ ] Configurazione Kong verificata?
- [ ] Test isolamento effettuati?
- [ ] Riproduzione problema riuscita?

### Post-Risoluzione
- [ ] Soluzione documentata?
- [ ] Test di regressione eseguiti?
- [ ] Monitoraggio aggiuntivo configurato?
- [ ] Runbook aggiornato?

---

**📖 Documentazione Correlata**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [API.md](API.md)
