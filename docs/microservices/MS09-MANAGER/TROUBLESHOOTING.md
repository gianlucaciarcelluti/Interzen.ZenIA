# Troubleshooting - MS09-MANAGER

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [API.md](API.md) | [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [← TROUBLESHOUTING.md](TROUBLESHOUTING.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms09--manager)

## 1. Panoramica Troubleshooting

Questa guida fornisce procedure diagnostiche e risoluzioni per i problemi più comuni in MS09-MANAGER. Il sistema include monitoraggio integrato e logging strutturato per facilitare l'identificazione e risoluzione dei problemi.

**Strumenti di Diagnosi**: Logs strutturati, metriche Prometheus, health checks, database queries
**Approccio**: Isolamento del problema → Raccolta evidenze → Applicazione fix → Verifica risoluzione

## 2. Workflow Non Si Avvia

### Sintomi
- Workflow rimane in stato "pending"
- Nessun progresso dopo la creazione
- Timeout nell'avvio

### Diagnosi

**1. Verifica Stato Database**
```sql
-- Controlla stato workflow instance
SELECT id, status, created_at, started_at, error_details
FROM workflow_instances
WHERE id = 'workflow-instance-id'
ORDER BY created_at DESC LIMIT 1;

-- Verifica presenza definizione workflow
SELECT id, name, status
FROM workflow_definitions
WHERE id = 'workflow-definition-id';
```

**2. Controlla Queue Message**
```bash
# Verifica messaggi in coda RabbitMQ
rabbitmqctl list_queues name messages_ready messages_unacknowledged

# Controlla connessione message broker
curl -f http://localhost:15672/api/queues/%2f/workflow-start-queue
```

**3. Analizza Logs Applicativi**
```bash
# Cerca errori nell'avvio workflow
grep "Failed to start workflow" /var/log/ms09-manager/application.log

# Verifica configurazione message broker
grep "RabbitMQ connection" /var/log/ms09-manager/application.log
```

### Risoluzioni

**A. Workflow Definition Non Valida**
```json
{
  "error": "Workflow definition validation failed",
  "details": {
    "field": "steps[0].service",
    "message": "Service 'invalid-service' not found"
  }
}
```

**Fix**: Correggere definizione workflow e ricaricare.

**B. Message Broker Non Disponibile**
```bash
# Riavvia connessione RabbitMQ
kubectl rollout restart deployment/ms09-manager

# Verifica configurazione
cat /app/config/application.yml | grep rabbitmq
```

**C. Database Connection Pool Esaurito**
```sql
-- Monitora pool connessioni
SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction';
```

**Fix**: Aumentare pool size in configurazione.

## 3. Workflow Bloccato in Stato "Running"

### Sintomi
- Workflow non progredisce
- Step singolo rimane "running" indefinitamente
- Timeout su operazioni esterne

### Diagnosi

**1. Identifica Step Bloccato**
```sql
-- Trova step bloccati
SELECT ws.step_id, ws.step_name, ws.status, ws.started_at,
       EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - ws.started_at))/3600 as running_hours
FROM workflow_steps ws
JOIN workflow_instances wi ON ws.workflow_instance_id = wi.id
WHERE wi.status = 'running'
  AND ws.status = 'running'
  AND ws.started_at < CURRENT_TIMESTAMP - INTERVAL '1 hour';
```

**2. Verifica Service Chiamato**
```sql
-- Controlla chiamate esterne fallite
SELECT se.step_id, se.status, se.error_details, se.started_at
FROM step_executions se
WHERE se.status = 'failed'
  AND se.started_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
ORDER BY se.started_at DESC;
```

**3. Analizza Timeout Configuration**
```yaml
# Verifica configurazione timeout
workflow:
  step:
    timeout:
      default: 30m
      service_call: 10m
      human_task: 24h
  retry:
    max_attempts: 3
    backoff:
      initial: 1s
      multiplier: 2
      max_delay: 5m
```

### Risoluzioni

**A. Timeout Step Non Configurato**
```json
{
  "steps": [
    {
      "id": "slow_service_call",
      "timeout": "60m",
      "retry": {
        "max_attempts": 5,
        "backoff": {
          "type": "exponential",
          "max_delay": "10m"
        }
      }
    }
  ]
}
```

**B. Service Esterno Non Risponde**
```bash
# Verifica health del servizio chiamato
curl -f http://ms04-validator.zenia.local/health

# Controlla circuit breaker
kubectl get pods -l app=ms04-validator
```

**C. Deadlock Database**
```sql
-- Identifica deadlock
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.usename AS blocked_user,
       blocking_activity.usename AS blocking_user,
       blocked_activity.query AS blocked_statement,
       blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

## 4. Errori di Compensazione

### Sintomi
- Workflow fallisce ma compensazione non avviene
- Risorse non rilasciate correttamente
- Stato inconsistente dopo failure

### Diagnosi

**1. Verifica Stato Compensazione**
```sql
-- Controlla compensazioni pendenti
SELECT wc.*, wi.status as workflow_status
FROM workflow_compensations wc
JOIN workflow_instances wi ON wc.workflow_instance_id = wi.id
WHERE wc.status IN ('pending', 'running', 'failed')
ORDER BY wc.created_at DESC;
```

**2. Analizza Saga Pattern**
```sql
-- Verifica ordine esecuzione saga
SELECT se.step_id, se.attempt_number, se.status, se.started_at, se.error_details
FROM step_executions se
WHERE se.step_id IN (
    SELECT id FROM workflow_steps
    WHERE workflow_instance_id = 'workflow-instance-id'
)
ORDER BY se.started_at;
```

**3. Controlla Compensation Logic**
```java
// Verifica implementazione compensazione
public class DocumentProcessingCompensation implements CompensationHandler {

    @Override
    public CompensationResult compensate(CompensationContext context) {
        try {
            // Cleanup temp files
            cleanupTempFiles(context.getWorkflowId());

            // Notify stakeholders
            notifyCompensation(context);

            return CompensationResult.success();
        } catch (Exception e) {
            log.error("Compensation failed", e);
            return CompensationResult.failure(e);
        }
    }
}
```

### Risoluzioni

**A. Compensation Handler Mancante**
```json
{
  "error_handling": {
    "compensation_steps": [
      {
        "id": "cleanup_resources",
        "service": "ms05-transformer",
        "action": "cleanup_temp_files",
        "parameters": {
          "workflow_id": "${workflow.id}"
        }
      }
    ]
  }
}
```

**B. Compensation Service Non Disponibile**
```bash
# Verifica servizio di compensazione
kubectl get pods -l app=compensation-service

# Riavvia servizio se necessario
kubectl rollout restart deployment/compensation-service
```

## 5. Problemi di Performance

### Sintomi
- Throughput basso (< 100 workflow/minuto)
- Latenza alta (> 5 secondi)
- CPU/Memory usage elevato

### Diagnosi

**1. Analizza Metriche Performance**
```sql
-- Query performance workflow
SELECT
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as workflows_created,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_duration,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (completed_at - started_at))) as p95_duration
FROM workflow_instances
WHERE created_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', created_at)
ORDER BY hour DESC;
```

**2. Controlla Resource Usage**
```bash
# Monitora risorse container
kubectl top pods -l app=ms09-manager

# Verifica limiti risorse
kubectl describe pod ms09-manager-xxxxx | grep -A 10 "Limits:"
```

**3. Analizza Query Database Lente**
```sql
-- Trova query lente
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements
WHERE query LIKE '%workflow%'
ORDER BY mean_time DESC
LIMIT 10;
```

### Risoluzioni

**A. Database Indexing Mancante**
```sql
-- Aggiungi indici mancanti
CREATE INDEX CONCURRENTLY idx_workflow_instances_tenant_status_created
    ON workflow_instances (tenant_id, status, created_at DESC);

CREATE INDEX CONCURRENTLY idx_workflow_steps_instance_status
    ON workflow_steps (workflow_instance_id, status);
```

**B. Connection Pool Undersized**
```yaml
# Aumenta pool connessioni
spring:
  datasource:
    hikari:
      maximum-pool-size: 50
      minimum-idle: 10
      connection-timeout: 30000
```

**C. Memory Leak Detection**
```java
// Aggiungi heap dump su OOM
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/app/logs/heapdump.hprof
-XX:+PrintGCDetails
-XX:+PrintGCTimeStamps
```

## 6. Problemi di Concorrenza

### Sintomi
- Race conditions tra workflow
- Stato inconsistente
- Duplicate processing

### Diagnosi

**1. Identifica Race Conditions**
```sql
-- Cerca aggiornamenti concorrenti
SELECT wi.id, wi.version, COUNT(*) as concurrent_updates
FROM workflow_instances wi
JOIN workflow_events we ON wi.id = we.workflow_instance_id
WHERE we.event_type = 'WorkflowUpdated'
  AND we.occurred_at >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
GROUP BY wi.id, wi.version
HAVING COUNT(*) > 1;
```

**2. Verifica Optimistic Locking**
```java
// Implementazione optimistic locking
@Transactional
public void updateWorkflowStatus(UUID workflowId, WorkflowStatus newStatus) {
    WorkflowInstance instance = repository.findById(workflowId)
        .orElseThrow(() -> new WorkflowNotFoundException(workflowId));

    if (instance.getVersion() != expectedVersion) {
        throw new ConcurrentModificationException(
            "Workflow was modified by another transaction"
        );
    }

    instance.setStatus(newStatus);
    instance.setVersion(instance.getVersion() + 1);
    repository.save(instance);
}
```

**3. Analizza Transaction Isolation**
```sql
-- Verifica livello isolamento
SHOW default_transaction_isolation;

-- Cerca lost updates
SELECT * FROM pg_stat_user_tables
WHERE n_tup_upd > 0 AND n_tup_hot_upd = 0
ORDER BY n_tup_upd DESC;
```

### Risoluzioni

**A. Implementa Pessimistic Locking**
```java
@Lock(LockModeType.PESSIMISTIC_WRITE)
public WorkflowInstance findByIdWithLock(UUID id) {
    return entityManager.find(WorkflowInstance.class, id);
}
```

**B. Usa Database Sequences per Versioning**
```sql
-- Sequence per versioning ottimistico
CREATE SEQUENCE workflow_version_seq;

ALTER TABLE workflow_instances
    ALTER COLUMN version SET DEFAULT nextval('workflow_version_seq');
```

## 7. Problemi di Rete e Connettività

### Sintomi
- Timeout nelle chiamate inter-service
- Connection refused
- Circuit breaker attivato

### Diagnosi

**1. Verifica Service Discovery**
```bash
# Controlla registrazione servizi
curl http://consul:8500/v1/catalog/services | jq '.ms09-manager'

# Verifica health checks
curl http://consul:8500/v1/health/service/ms09-manager
```

**2. Analizza Network Policies**
```yaml
# Verifica network policies Kubernetes
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ms09-network-policy
spec:
  podSelector:
    matchLabels:
      app: ms09-manager
  policyTypes:
    - Ingress
    - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: ms04-validator
    ports:
    - protocol: TCP
      port: 8080
```

**3. Monitora Circuit Breaker**
```java
// Configurazione circuit breaker
@CircuitBreaker(name = "ms04-validator", fallbackMethod = "fallbackValidation")
public ValidationResult validateDocument(Document doc) {
    return validatorClient.validate(doc);
}

public ValidationResult fallbackValidation(Document doc, Throwable t) {
    log.warn("Circuit breaker activated for document validation", t);
    return ValidationResult.unknown();
}
```

### Risoluzioni

**A. Service Mesh Configuration**
```yaml
# Configurazione Istio destination rule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: ms09-manager-dr
spec:
  host: ms09-manager
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http2MaxRequests: 1000
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
```

**B. Load Balancer Configuration**
```nginx
# Configurazione NGINX upstream
upstream ms09_manager_backend {
    least_conn;
    server ms09-manager-1:8080 weight=1;
    server ms09-manager-2:8080 weight=1;
    server ms09-manager-3:8080 weight=1;

    keepalive 32;
}

server {
    listen 80;
    location /api/v1/ {
        proxy_pass http://ms09_manager_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_read_timeout 300s;
    }
}
```

## 8. Problemi di Sicurezza

### Sintomi
- Accesso non autorizzato
- Token JWT invalidi
- Audit logs incompleti

### Diagnosi

**1. Verifica Token JWT**
```bash
# Decodifica token per debug
echo "eyJhbGciOiJSUzI1NiIs..." | jwt decode -

# Verifica firma
curl -X POST https://auth.zenia.local/oauth/introspect \
  -H "Authorization: Bearer {token}" \
  -d "token=eyJhbGciOiJSUzI1NiIs..."
```

**2. Analizza Audit Logs**
```sql
-- Query audit logs
SELECT event_type, user_id, resource_type, action, timestamp
FROM audit_events
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
  AND event_type = 'SECURITY_VIOLATION'
ORDER BY timestamp DESC;
```

**3. Controlla Role-Based Access**
```java
// Verifica configurazione sicurezza
@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/v1/workflows/**").hasAnyRole("USER", "ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthenticationConverter()))
            );

        return http;
    }
}
```

### Risoluzioni

**A. Aggiorna Token Signing Keys**
```bash
# Ruota chiavi JWT
kubectl create secret generic jwt-keys \
  --from-file=public-key.pem \
  --from-file=private-key.pem \
  --dry-run=client -o yaml | kubectl apply -f -

# Riavvia servizi
kubectl rollout restart deployment/ms09-manager
```

**B. Implementa Rate Limiting Avanzato**
```java
@Configuration
public class RateLimitConfig {

    @Bean
    public RateLimiterRegistry rateLimiterRegistry() {
        return RateLimiterRegistry.of(Map.of(
            "workflow_creation", RateLimiter.of("workflow_creation", RateLimiterConfig.custom()
                .limitForPeriod(10)
                .limitRefreshPeriod(Duration.ofMinutes(1))
                .timeoutDuration(Duration.ofSeconds(5))),
            "admin_operations", RateLimiter.of("admin_operations", RateLimiterConfig.custom()
                .limitForPeriod(5)
                .limitRefreshPeriod(Duration.ofMinutes(1)))
        ));
    }
}
```

## 9. Recovery Procedures

### 9.1 Workflow State Recovery

```bash
#!/bin/bash
# workflow-recovery.sh

WORKFLOW_ID=$1

echo "Starting recovery for workflow $WORKFLOW_ID"

# 1. Backup current state
pg_dump -t workflow_instances -t workflow_steps -t workflow_events \
  --data-only -f "/backup/workflow_${WORKFLOW_ID}_$(date +%s).sql"

# 2. Reset failed workflow
psql -c "UPDATE workflow_instances SET status = 'pending', error_details = NULL WHERE id = '$WORKFLOW_ID'"

# 3. Reset failed steps
psql -c "UPDATE workflow_steps SET status = 'pending', error_details = NULL WHERE workflow_instance_id = '$WORKFLOW_ID' AND status = 'failed'"

# 4. Clear Redis cache
redis-cli DEL "workflow:$WORKFLOW_ID:state"

# 5. Restart workflow processing
curl -X POST "http://localhost:8080/api/v1/workflows/$WORKFLOW_ID/restart" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

echo "Recovery completed for workflow $WORKFLOW_ID"
```

### 9.2 Database Corruption Recovery

```sql
-- Recovery da backup point-in-time
RESTORE DATABASE zenia_workflow_manager
FROM DISK = '/backups/workflow_manager_20240115_1200.bak'
WITH RECOVERY,
     STOPAT = '2024-01-15 12:30:00';

-- Verifica integrità dopo recovery
DBCC CHECKDB('zenia_workflow_manager') WITH NO_INFOMSGS;

-- Ricostruisci indici se necessario
ALTER INDEX ALL ON workflow_instances REBUILD;
ALTER INDEX ALL ON workflow_steps REBUILD;
```

### 9.3 Full System Recovery

```bash
#!/bin/bash
# disaster-recovery.sh

echo "Starting full system recovery..."

# 1. Stop all services
kubectl scale deployment --all --replicas=0 -n zenia

# 2. Restore database from backup
pg_restore -d zenia_workflow_manager /backups/full_backup_$(date +%Y%m%d).dump

# 3. Clear all caches
redis-cli FLUSHALL

# 4. Restore Elasticsearch indices
curl -X POST "localhost:9200/_snapshot/zenia_backup/snapshot_$(date +%Y%m%d)/_restore"

# 5. Start services gradually
kubectl scale deployment ms09-manager --replicas=1 -n zenia
sleep 30
kubectl scale deployment ms04-validator --replicas=2 -n zenia
sleep 30

# Continue with other services...

echo "Full system recovery completed"
```

## 10. Monitoring e Alerting

### 10.1 Key Metrics to Monitor

```yaml
# Prometheus metrics
groups:
  - name: workflow_metrics
    rules:
      - alert: WorkflowCreationFailed
        expr: rate(workflow_creation_failures_total[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Workflow creation is failing"

      - alert: WorkflowStuck
        expr: workflow_instances_status{status="running"} and workflow_age_seconds > 3600
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Workflow stuck in running state"

      - alert: HighErrorRate
        expr: rate(workflow_step_errors_total[5m]) / rate(workflow_step_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High workflow error rate detected"
```

### 10.2 Log Aggregation Queries

```sql
-- Error patterns analysis
SELECT
    DATE_TRUNC('hour', timestamp) as hour,
    error_type,
    COUNT(*) as occurrences,
    array_agg(DISTINCT workflow_id) as affected_workflows
FROM application_logs
WHERE level = 'ERROR'
  AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', timestamp), error_type
ORDER BY hour DESC, occurrences DESC;

-- Performance degradation detection
SELECT
    endpoint,
    AVG(response_time_ms) as avg_response_time,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms) as p95_response_time,
    COUNT(*) as request_count
FROM api_metrics
WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
GROUP BY endpoint
HAVING AVG(response_time_ms) > 1000
ORDER BY avg_response_time DESC;
```

## 11. Best Practices Troubleshooting

### 11.1 Prevenzione Problemi

1. **Monitoring Proattivo**: Implementare alert su metriche chiave
2. **Log Strutturati**: Usare logging strutturato per facile analisi
3. **Health Checks**: Implementare health checks completi
4. **Circuit Breakers**: Configurare circuit breaker per resilienza
5. **Graceful Degradation**: Implementare fallback per servizi critici

### 11.2 Debug Workflow

```java
// Debug workflow execution
@Aspect
@Component
public class WorkflowDebugAspect {

    @Around("execution(* WorkflowExecutor.execute(..))")
    public Object debugWorkflowExecution(ProceedingJoinPoint joinPoint) throws Throwable {
        Workflow workflow = (Workflow) joinPoint.getArgs()[0];
        long startTime = System.currentTimeMillis();

        try {
            log.debug("Starting workflow execution: {}", workflow.getId());
            Object result = joinPoint.proceed();
            log.debug("Workflow completed successfully: {} in {}ms",
                     workflow.getId(), System.currentTimeMillis() - startTime);
            return result;
        } catch (Exception e) {
            log.error("Workflow execution failed: {} after {}ms",
                     workflow.getId(), System.currentTimeMillis() - startTime, e);
            throw e;
        }
    }
}
```

### 11.3 Performance Profiling

```java
// Performance profiling
@Configuration
public class PerformanceConfig {

    @Bean
    public MeterRegistry meterRegistry() {
        return new CompositeMeterRegistry();
    }

    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }
}

// Usage
@Service
public class WorkflowService {

    @Timed(value = "workflow.creation", description = "Time taken to create workflow")
    public WorkflowInstance createWorkflow(WorkflowDefinition definition) {
        // Implementation
    }

    @Timed(value = "workflow.execution", description = "Time taken to execute workflow")
    public WorkflowResult executeWorkflow(WorkflowInstance instance) {
        // Implementation
    }
}
```

Questa guida dovrebbe coprire la maggior parte degli scenari di troubleshooting per MS09-MANAGER. Per problemi non coperti, consultare i logs dettagliati o contattare il team di supporto tecnico.