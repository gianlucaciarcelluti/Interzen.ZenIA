# TROUBLESHOOTING - MS14-AUDIT

## Problemi comuni e soluzioni

### 1. Log non ricevuti
- **Verifica**: Stato API `/api/audit/log`, connessione microservizi
- **Soluzione**: Controlla configurazione endpoint, token JWT, network policy

### 2. Ricerca log lenta
- **Verifica**: Stato cluster Elasticsearch, risorse nodo
- **Soluzione**: Ottimizza query, verifica shard, aumenta risorse

### 3. Errori autenticazione
- **Verifica**: Validità JWT, configurazione RBAC
- **Soluzione**: Rigenera token, controlla ruoli utente

### 4. Alert/Forwarding non funzionante
- **Verifica**: Log exporter, stato SIEM
- **Soluzione**: Controlla endpoint SIEM, log exporter, network

### 5. Metriche Prometheus assenti
- **Verifica**: Endpoint `/metrics`, ServiceMonitor
- **Soluzione**: Verifica deployment exporter, configurazione ServiceMonitor

### 6. Backup/Restore Elasticsearch
- **Verifica**: Stato snapshot, permessi storage
- **Soluzione**: Controlla policy snapshot, spazio disponibile

## Comandi utili

```bash
# Verifica stato API
curl -H "Authorization: Bearer <token>" http://ms14-audit:8080/api/audit/log

# Query Elasticsearch
curl -XGET 'http://elasticsearch:9200/zenia-audit-logs-*/_search?q=action:LOGIN'

# Esportazione log
curl -H "Authorization: Bearer <token>" http://ms14-audit:8080/api/audit/export?format=csv

# Verifica metriche
curl http://ms14-audit:8080/metrics
```

## Log e diagnostica
- Log applicativo: `/var/log/ms14-audit/app.log`
- Log Elasticsearch: `/usr/share/elasticsearch/logs/`
- Log exporter: `/var/log/ms14-audit/exporter.log`
