# TROUBLESHOUTING - MS15-CONFIG

## Problemi comuni e soluzioni

### 1. Configurazione non aggiornata
- **Verifica**: Stato API `/api/config/{service}`
- **Soluzione**: Controlla permessi JWT, validità payload, stato DB

### 2. Rollback non riuscito
- **Verifica**: Versione richiesta, permessi RBAC
- **Soluzione**: Verifica storico versioni, riprova con versione valida

### 3. Notifiche eventi assenti
- **Verifica**: Stato Redis/EventBus, endpoint `/api/config/events/subscribe`
- **Soluzione**: Controlla connessione Redis, log microservizio

### 4. Errori autenticazione
- **Verifica**: Validità JWT, configurazione RBAC
- **Soluzione**: Rigenera token, controlla ruoli utente

### 5. Metriche Prometheus assenti
- **Verifica**: Endpoint `/metrics`, ServiceMonitor
- **Soluzione**: Verifica deployment exporter, configurazione ServiceMonitor

### 6. Backup/Restore DB
- **Verifica**: Stato dump, permessi storage
- **Soluzione**: Controlla policy backup, spazio disponibile

## Comandi utili

```bash
# Recupera configurazione
curl -H "Authorization: Bearer <token>" http://ms15-config:8080/api/config/MS11-API-GATEWAY

# Aggiorna configurazione
curl -X PUT -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
  -d '{"config": {"timeout": 60}}' http://ms15-config:8080/api/config/MS11-API-GATEWAY

# Rollback configurazione
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
  -d '{"version": 4}' http://ms15-config:8080/api/config/MS11-API-GATEWAY/rollback

# Verifica metriche
curl http://ms15-config:8080/metrics
```

## Log e diagnostica
- Log applicativo: `/var/log/ms15-config/app.log`
- Log DB: `/var/log/postgresql/`
- Log exporter: `/var/log/ms15-config/exporter.log`
