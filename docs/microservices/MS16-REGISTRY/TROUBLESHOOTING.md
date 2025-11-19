# TROUBLESHOUTING - MS16-REGISTRY

## Problemi comuni e soluzioni

### 1. Servizio non registrato
- **Verifica**: Stato API `/api/registry/service`, payload
- **Soluzione**: Controlla permessi JWT, validità payload, stato DB

### 2. Health check falliti
- **Verifica**: Endpoint health_url, stato servizio
- **Soluzione**: Verifica reachability, log servizio, configurazione health check

### 3. Deregistrazione non riuscita
- **Verifica**: Permessi RBAC, nome servizio
- **Soluzione**: Verifica esistenza servizio, riprova con nome corretto

### 4. Notifiche eventi assenti
- **Verifica**: Stato Redis/EventBus, endpoint `/api/registry/events/subscribe`
- **Soluzione**: Controlla connessione Redis, log microservizio

### 5. Metriche Prometheus assenti
- **Verifica**: Endpoint `/metrics`, ServiceMonitor
- **Soluzione**: Verifica deployment exporter, configurazione ServiceMonitor

### 6. Backup/Restore DB
- **Verifica**: Stato dump, permessi storage
- **Soluzione**: Controlla policy backup, spazio disponibile

## Comandi utili

```bash
# Registra servizio
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
  -d '{"name": "ms11-api-gateway", "address": "10.0.0.11", "port": 8080}' http://ms16-registry:8080/api/registry/service

# Lista servizi
curl -H "Authorization: Bearer <token>" http://ms16-registry:8080/api/registry/services

# Health check
curl -H "Authorization: Bearer <token>" http://ms16-registry:8080/api/registry/health/ms11-api-gateway

# Deregistra servizio
curl -X DELETE -H "Authorization: Bearer <token>" http://ms16-registry:8080/api/registry/service/ms11-api-gateway

# Verifica metriche
curl http://ms16-registry:8080/metrics
```

## Log e diagnostica
- Log applicativo: `/var/log/ms16-registry/app.log`
- Log DB: `/var/log/postgresql/`
- Log exporter: `/var/log/ms16-registry/exporter.log`
