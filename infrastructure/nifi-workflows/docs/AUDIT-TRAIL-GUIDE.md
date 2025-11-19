# NiFi Audit Trail System

Sistema completo di auditing e tracciabilità per i workflow NiFi del ZenIA.

## 📊 Panoramica

Il sistema di audit traccia:
- ✅ Tutte le esecuzioni dei workflow
- ✅ Richieste HTTP in ingresso e risposte
- ✅ Errori e fallimenti
- ✅ Metriche di performance
- ✅ Controlli di qualità dei dati

## 🗄️ Struttura Database

### Database: `nifi_audit`

#### Tabelle Principali:

1. **`workflow_executions`** - Traccia ogni step di ogni workflow
   - `execution_id` - UUID univoco per la catena di esecuzione
   - `workflow_name` - Nome del workflow (SP01, SP02, etc.)
   - `step_name` - Nome del processor
   - `status` - RUNNING, SUCCESS, FAILED, TIMEOUT
   - `input_data`, `output_data` - Payload JSONB
   - `duration_ms` - Durata esecuzione
   - `error_message` - Dettagli errori

2. **`http_requests`** - Log completo richieste HTTP
   - `method`, `url`, `headers`, `query_params`
   - `request_body`, `response_body`
   - `response_code`, `response_time_ms`

3. **`error_log`** - Centralizzazione errori
   - `error_type` - VALIDATION, NETWORK, TIMEOUT, SYSTEM
   - `severity` - DEBUG, INFO, WARNING, ERROR, CRITICAL
   - `stack_trace`, `error_context`

4. **`performance_metrics`** - Metriche dettagliate
   - `processing_time_ms`, `queue_time_ms`
   - `bytes_in`, `bytes_out`
   - `cpu_usage_percent`, `memory_usage_mb`

5. **`data_quality_checks`** - Validazioni qualità
   - `check_type` - SCHEMA, FORMAT, COMPLETENESS
   - `check_result` - PASS, FAIL, WARNING
   - `violations` - Dettagli anomalie

## 🚀 Setup Iniziale

### 1. Ricostruisci il Database

Il database `nifi_audit` viene creato automaticamente quando riavvii i container:

```bash
cd infrastructure/nifi-workflows

# Ferma i container
docker-compose down

# Riavvia (il database verrà inizializzato)
docker-compose up -d postgres

# Attendi che postgres sia pronto
docker-compose logs -f postgres | grep "database system is ready"
```

### 2. Verifica Creazione Database

```bash
# Connettiti al database
docker exec -it postgres-db psql -U postgres -d nifi_audit

# Verifica tabelle
\dt

# Dovresti vedere:
#  workflow_executions
#  http_requests
#  error_log
#  performance_metrics
#  data_quality_checks
```

### 3. Aggiungi Processor di Audit ai Workflow (Opzionale)

```bash
# Esegui lo script per aggiungere processor automaticamente
python3 services/add-audit-processors.py
```

**Nota**: Lo script aggiunge processor `UpdateAttribute`, `AttributesToJSON` e `PutDatabaseRecord` a ciascun workflow.

## 📝 Configurazione Manuale (Alternative)

Se preferisci configurare manualmente via NiFi UI:

### Per ogni workflow:

1. **Aggiungi UpdateAttribute dopo HTTP_Endpoint**
   - Proprietà custom:
     ```
     execution_id = ${UUID()}
     workflow_name = SP01_EML_Parser
     started_at = ${now():format('yyyy-MM-dd HH:mm:ss')}
     status = RUNNING
     flowfile_id = ${uuid}
     ```

2. **Aggiungi AttributesToJSON**
   - Attributes List: `execution_id,workflow_name,started_at,status,flowfile_id`
   - Destination: `flowfile-content`

3. **Aggiungi PutDatabaseRecord**
   - Record Reader: `JsonTreeReader`
   - Database Connection Pool: `PostgreSQL-Connection-Pool` (aggiorna connection string a `nifi_audit`)
   - Table Name: `workflow_executions`
   - Translate Field Names: `true`

## 📊 Query Utili

### Verificare Esecuzioni Recenti

```sql
-- Ultime 100 esecuzioni
SELECT 
    workflow_name,
    step_name,
    status,
    started_at,
    duration_ms,
    error_message
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 100;
```

### Esecuzioni Fallite Ultime 24h

```sql
SELECT 
    workflow_name,
    step_name,
    started_at,
    error_message,
    error_details
FROM workflow_executions
WHERE status = 'FAILED'
  AND started_at >= NOW() - INTERVAL '24 hours'
ORDER BY started_at DESC;
```

### Performance Summary per Workflow

```sql
SELECT 
    workflow_name,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END) as successful,
    COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failed,
    ROUND(AVG(duration_ms), 2) as avg_duration_ms,
    MAX(duration_ms) as max_duration_ms
FROM workflow_executions
WHERE started_at >= NOW() - INTERVAL '7 days'
GROUP BY workflow_name
ORDER BY total_executions DESC;
```

### Health Check Workflow

```sql
-- Usa la funzione helper
SELECT * FROM get_workflow_health('SP01_EML_Parser', 24);
```

### Catena Completa Esecuzione

```sql
-- Trova tutte le steps di una specifica esecuzione
SELECT 
    step_name,
    status,
    started_at,
    completed_at,
    duration_ms,
    input_data,
    output_data
FROM workflow_executions
WHERE execution_id = 'your-uuid-here'
ORDER BY started_at;
```

### Top Errori per Tipo

```sql
SELECT 
    error_type,
    COUNT(*) as error_count,
    COUNT(DISTINCT workflow_name) as affected_workflows
FROM error_log
WHERE created_at >= NOW() - INTERVAL '7 days'
GROUP BY error_type
ORDER BY error_count DESC;
```

## 📈 Visualizzazione Metriche

### Aggiornare Statistiche (eseguire periodicamente)

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY workflow_statistics;
```

### Visualizzare Statistiche Aggregate

```sql
SELECT 
    workflow_name,
    hour,
    total_executions,
    successful_executions,
    failed_executions,
    ROUND(avg_duration_ms, 2) as avg_duration,
    ROUND(p95_duration_ms, 2) as p95_duration
FROM workflow_statistics
WHERE hour >= NOW() - INTERVAL '24 hours'
ORDER BY hour DESC, workflow_name;
```

## 🔍 Monitoring & Alerting

### Workflow con Success Rate < 80%

```sql
SELECT 
    workflow_name,
    total_executions,
    success_rate,
    health_status
FROM get_workflow_health('SP01_EML_Parser', 24)
WHERE success_rate < 80;
```

### Slow Queries (P95 > 5 secondi)

```sql
SELECT 
    workflow_name,
    p95_duration_ms / 1000.0 as p95_seconds
FROM workflow_statistics
WHERE hour >= NOW() - INTERVAL '1 hour'
  AND p95_duration_ms > 5000
ORDER BY p95_duration_ms DESC;
```

## 🛠️ Manutenzione

### Cleanup Vecchi Record (> 30 giorni)

```sql
-- Elimina esecuzioni vecchie
DELETE FROM workflow_executions
WHERE started_at < NOW() - INTERVAL '30 days';

-- Elimina log errori vecchi
DELETE FROM error_log
WHERE created_at < NOW() - INTERVAL '30 days';

-- Elimina richieste HTTP vecchie
DELETE FROM http_requests
WHERE created_at < NOW() - INTERVAL '30 days';
```

### Vacuum & Analyze

```sql
VACUUM ANALYZE workflow_executions;
VACUUM ANALYZE http_requests;
VACUUM ANALYZE error_log;
```

## 🔐 Sicurezza

### Creare Utente Read-Only per Analytics

```sql
CREATE USER analytics_readonly WITH PASSWORD 'your_secure_password';
GRANT CONNECT ON DATABASE nifi_audit TO analytics_readonly;
GRANT USAGE ON SCHEMA public TO analytics_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_readonly;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO analytics_readonly;
```

## 📦 Backup

### Backup Giornaliero

```bash
# Backup completo database audit
docker exec postgres-db pg_dump -U postgres nifi_audit > nifi_audit_backup_$(date +%Y%m%d).sql

# Backup solo schema
docker exec postgres-db pg_dump -U postgres --schema-only nifi_audit > nifi_audit_schema.sql
```

### Restore

```bash
# Restore da backup
docker exec -i postgres-db psql -U postgres nifi_audit < nifi_audit_backup_20251104.sql
```

## 🎯 Best Practices

1. **Refresh Statistics Hourly**
   ```sql
   REFRESH MATERIALIZED VIEW CONCURRENTLY workflow_statistics;
   ```

2. **Monitor Error Rate**
   - Configura alert se error rate > 5%
   - Controlla `error_log` daily

3. **Archive Old Data**
   - Sposta record > 90 giorni in cold storage
   - Mantieni solo metriche aggregate

4. **Index Optimization**
   - Monitor query performance
   - Aggiungi indici custom per query frequenti

5. **Data Retention Policy**
   - workflow_executions: 30 giorni
   - http_requests: 30 giorni
   - error_log: 90 giorni
   - performance_metrics: 30 giorni (aggregate in statistics)

## 📞 Troubleshooting

### Il database non si crea

```bash
# Verifica logs postgres
docker-compose logs postgres | grep -i error

# Ricrea da zero
docker-compose down -v
docker-compose up -d postgres
```

### Processor PutDatabaseRecord fallisce

1. Verifica connection pool punta a `nifi_audit` database
2. Controlla JsonTreeReader sia configurato
3. Verifica permessi utente `nifi` sul database

### Query lente

```sql
-- Analizza query plan
EXPLAIN ANALYZE 
SELECT * FROM workflow_executions 
WHERE workflow_name = 'SP01_EML_Parser' 
  AND started_at >= NOW() - INTERVAL '1 day';

-- Se manca indice, aggiungi
CREATE INDEX idx_custom ON workflow_executions(workflow_name, started_at);
```

## 🔗 Riferimenti

- [NiFi PutDatabaseRecord Documentation](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-standard-nar/1.23.2/org.apache.nifi.processors.standard.PutDatabaseRecord/index.html)
- [PostgreSQL JSONB Functions](https://www.postgresql.org/docs/current/functions-json.html)
- [Materialized Views](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
