# Troubleshooting Guide - MS07-DISTRIBUTOR

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [API.md](API.md) | [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms07--distributor)

## Panoramica Troubleshooting

Questa guida fornisce procedure diagnostiche e risoluzioni per i problemi più comuni in MS07-DISTRIBUTOR. Il sistema include comprehensive logging, metrics e health checks per facilitare l'identificazione e risoluzione dei problemi.

## Strumenti di Diagnostica

### 1. Health Check Endpoints

#### 1.1 Health Check Generale
```bash
curl -H "Authorization: Bearer {token}" \
     https://ms07-distributor.zenia.local/health/ready
```

**Response normale**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.2.3",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "queue": "healthy",
    "workers": "healthy",
    "destinations": "healthy"
  }
}
```

#### 1.2 Health Check Dettagliato
```bash
curl -H "Authorization: Bearer {token}" \
     https://ms07-distributor.zenia.local/health/detailed
```

**Include**: Connessioni database, stato queue, health destinazioni, performance metrics.

### 2. Log Analysis

#### 2.1 Log Levels
- **ERROR**: Errori critici che richiedono intervento
- **WARN**: Problemi che potrebbero diventare critici
- **INFO**: Eventi normali e informazioni operative
- **DEBUG**: Dettagli tecnici per troubleshooting

#### 2.2 Log Format Strutturato
```json
{
  "timestamp": "2024-01-15T10:00:00Z",
  "level": "ERROR",
  "service": "ms07-distributor",
  "component": "DistributionWorker",
  "distribution_id": "dist-uuid-123",
  "destination": "ms09-reporter",
  "error_code": "CONNECTION_TIMEOUT",
  "message": "Failed to connect to destination after 3 attempts",
  "stack_trace": "...",
  "metadata": {
    "attempt": 3,
    "total_attempts": 3,
    "last_error": "Connection timed out",
    "destination_url": "https://ms09.zenia.local/api/reports"
  }
}
```

### 3. Metrics Monitoring

#### 3.1 Metriche Chiave da Monitorare
```prometheus
# Throughput
zenia_distribution_requests_total{status="success"}
zenia_distribution_attempts_total{status="success"}

# Latency
histogram_quantile(0.95, zenia_distribution_latency_seconds)

# Error Rate
rate(zenia_distribution_requests_total{status="failed"}[5m]) /
rate(zenia_distribution_requests_total[5m])

# Queue Health
zenia_distribution_queue_depth
zenia_distribution_active_workers
```

## Problemi Comuni e Soluzioni

### Problema 1: Distribuzioni in Timeout

#### Sintomi
- Distribuzioni rimangono in stato "processing" per lungo tempo
- Errori "CONNECTION_TIMEOUT" nei log
- Aumento della queue depth

#### Diagnostica
```sql
-- Verifica distribuzioni bloccate
SELECT distribution_id, status, created_at,
       EXTRACT(EPOCH FROM (NOW() - created_at))/60 AS minutes_old
FROM distribution_jobs
WHERE status = 'processing'
  AND created_at < NOW() - INTERVAL '30 minutes';

-- Verifica health destinazioni
SELECT name, health_status, last_health_check,
       EXTRACT(EPOCH FROM (NOW() - last_health_check))/60 AS minutes_since_check
FROM destinations
WHERE health_status = 'unhealthy';
```

#### Soluzioni

**1. Verifica Connettività Destinazioni**
```bash
# Test connessione diretta
curl -v --connect-timeout 10 https://ms09.zenia.local/health

# Verifica DNS resolution
nslookup ms09.zenia.local

# Test network connectivity
telnet ms09.zenia.local 443
```

**2. Aumenta Timeout Configuration**
```yaml
# kubernetes/configmap.yaml
distribution:
  timeout_seconds: 300  # Aumenta da 60
  retry_backoff_multiplier: 2.0
  max_retry_delay: 300
```

**3. Implementa Circuit Breaker**
```python
# Verifica configurazione circuit breaker
@circuit_breaker(failure_threshold=5, recovery_timeout=60)
async def deliver_to_destination(destination, payload):
    # Implementation
    pass
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### Prevenzione
- Implementa health checks proattivi
- Configura alert per timeout frequenti
- Monitora latenza media destinazioni

---

### Problema 2: Alta Latenza di Distribuzione

#### Sintomi
- P95 latency > 500ms
- Code di distribuzione che si accumulano
- Timeout frequenti

#### Diagnostica
```sql
-- Analizza latenza per destinazione
SELECT
    destination_name,
    COUNT(*) AS total_attempts,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) AS avg_latency_seconds,
    MAX(EXTRACT(EPOCH FROM (completed_at - started_at))) AS max_latency_seconds,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) AS failed_attempts
FROM distribution_attempts
WHERE started_at >= NOW() - INTERVAL '1 hour'
GROUP BY destination_name
ORDER BY avg_latency_seconds DESC;

-- Verifica utilizzo risorse
SELECT
    COUNT(*) AS active_distributions,
    AVG(EXTRACT(EPOCH FROM (NOW() - created_at))) AS avg_queue_time_seconds
FROM distribution_jobs
WHERE status = 'processing';
```

#### Soluzioni

**1. Scala Workers Orizzontalmente**
```yaml
# kubernetes/deployment.yaml
replicas: 5  # Aumenta da 3

resources:
  requests:
    cpu: "1000m"  # Aumenta CPU allocation
    memory: "2Gi"
  limits:
    cpu: "2000m"
    memory: "4Gi"
```

**2. Ottimizza Connection Pooling**
```python
# config/connection_pool.py
connection_pools = {
    'ms09-reporter': {
        'max_connections': 50,
        'max_keepalive_connections': 20,
        'keepalive_expiry': 30.0
    }
}
```

**3. Implementa Batching**
```python
# Per destinazioni che supportano batch
async def batch_deliver(destinations, payloads):
    # Group by destination
    batches = group_by_destination(payloads)

    # Parallel delivery with semaphore
    semaphore = asyncio.Semaphore(10)
    tasks = []

    for destination, batch_payloads in batches.items():
        task = asyncio.create_task(
            deliver_batch_with_semaphore(semaphore, destination, batch_payloads)
        )
        tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### Prevenzione
- Monitora P95 latency con alert
- Implementa auto-scaling basato su queue depth
- Regular performance testing

---

### Problema 3: Errori di Autenticazione Destinazioni

#### Sintomi
- Errori 401/403 dalle destinazioni
- Aumento failure rate
- Log "AUTHENTICATION_FAILED"

#### Diagnostica
```sql
-- Verifica errori autenticazione recenti
SELECT
    destination_name,
    response_status_code,
    error_message,
    COUNT(*) AS occurrences
FROM distribution_attempts
WHERE response_status_code IN (401, 403)
  AND started_at >= NOW() - INTERVAL '1 hour'
GROUP BY destination_name, response_status_code, error_message
ORDER BY occurrences DESC;

-- Verifica configurazione credenziali
SELECT name, configuration
FROM destinations
WHERE name = 'problematic-destination';
```

#### Soluzioni

**1. Verifica Credenziali**
```bash
# Test autenticazione manuale
curl -H "Authorization: Bearer {test_token}" \
     https://destination.example.com/api/test

# Verifica expiry token
# Controlla se il token è scaduto o ruotato
```

**2. Aggiorna Credenziali in Configurazione**
```yaml
# kubernetes/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ms07-credentials
type: Opaque
data:
  ms09-reporter-token: <base64-encoded-new-token>
  external-api-key: <base64-encoded-new-key>
```

**3. Implementa Token Refresh Automatico**
```python
class TokenManager:
    def __init__(self, client_id, client_secret, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self._token = None
        self._expires_at = None

    async def get_valid_token(self):
        if self._token is None or self._is_expired():
            await self._refresh_token()
        return self._token

    async def _refresh_token(self):
        # Implement OAuth2 token refresh
        async with aiohttp.ClientSession() as session:
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }
            async with session.post(self.token_url, data=data) as response:
                token_data = await response.json()
                self._token = token_data['access_token']
                self._expires_at = datetime.now() + timedelta(seconds=token_data['expires_in'])
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### Prevenzione
- Implementa monitoring token expiry
- Alert automatici per authentication failures
- Regular rotation credenziali

---

### Problema 4: Perdita Messaggi in Queue

#### Sintomi
- Distribuzioni inviate ma non processate
- Queue depth rimane costante nonostante workers attivi
- Log "MESSAGE_NOT_FOUND" o "QUEUE_EMPTY"

#### Diagnostica
```sql
-- Verifica messaggi in queue
QUEUE_DEPTH = Gauge('zenia_distribution_queue_depth', 'Current queue depth')

# In Redis CLI
SCAN 0 MATCH "distribution:queue:*" COUNT 1000

# Verifica consumer group status
XPENDING distribution:queue:default GROUP workers

-- Controlla deadlock workers
SELECT
    COUNT(*) AS active_workers,
    COUNT(CASE WHEN updated_at < NOW() - INTERVAL '5 minutes' THEN 1 END) AS stale_workers
FROM worker_heartbeats;
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### Soluzioni

**1. Verifica Configurazione Redis**
```redis.conf
# Assicurati configurazione corretta
maxmemory 2gb
maxmemory-policy allkeys-lru
tcp-keepalive 300
timeout 300

# Per Redis Cluster
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
```

**2. Implementa Dead Letter Queue**
```python
class DistributionQueue:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.max_retries = 3
        self.dlq_key = "distribution:dlq"

    async def enqueue_with_retry(self, message, retry_count=0):
        if retry_count >= self.max_retries:
            await self.move_to_dlq(message)
            return

        try:
            await self.redis.xadd("distribution:queue", message)
        except Exception as e:
            logger.error(f"Failed to enqueue message: {e}")
            await asyncio.sleep(2 ** retry_count)  # Exponential backoff
            await self.enqueue_with_retry(message, retry_count + 1)

    async def move_to_dlq(self, message):
        await self.redis.xadd(self.dlq_key, {
            **message,
            "moved_to_dlq_at": datetime.now().isoformat(),
            "reason": "max_retries_exceeded"
        })
```

**3. Monitora Consumer Health**
```python
class WorkerHealthMonitor:
    def __init__(self, redis_client, worker_id):
        self.redis = redis_client
        self.worker_id = worker_id
        self.heartbeat_key = f"worker:heartbeat:{worker_id}"

    async def send_heartbeat(self):
        await self.redis.setex(
            self.heartbeat_key,
            60,  # Expire after 60 seconds
            json.dumps({
                "worker_id": self.worker_id,
                "timestamp": datetime.now().isoformat(),
                "status": "active"
            })
        )

    async def check_worker_health(self):
        # Check if worker is responding
        heartbeat = await self.redis.get(self.heartbeat_key)
        if not heartbeat:
            logger.warning(f"Worker {self.worker_id} appears to be dead")
            await self.restart_worker(self.worker_id)
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### Prevenzione
- Implementa monitoring queue depth
- Alert per workers non responsivi
- Regular backup queue messages

---

### Problema 5: Memory Leaks nei Workers

#### Sintomi
- Aumento graduale memory usage
- Restart frequenti dei pod
- Performance degradation over time

#### Diagnostica
```bash
# Verifica memory usage
kubectl top pods -n zenia

# Analizza heap dumps
jmap -dump:format=b,file=heap.bin <pid>
jhat heap.bin

# Monitora garbage collection
java -XX:+PrintGCDetails -XX:+PrintGCTimeStamps

# In Python
import tracemalloc
tracemalloc.start()
# ... run distribution
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024} MB")
print(f"Peak memory usage: {peak / 1024 / 1024} MB")
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### Soluzioni

**1. Implementa Connection Pooling Corretta**
```python
# config/connection_pool.py
class ConnectionPoolManager:
    def __init__(self):
        self.pools = {}
        self._cleanup_task = None

    async def get_pool(self, destination):
        if destination not in self.pools:
            self.pools[destination] = await self._create_pool(destination)

        pool = self.pools[destination]
        # Validate pool health
        if not await self._is_pool_healthy(pool):
            await self._recreate_pool(destination)

        return pool

    async def cleanup_stale_connections(self):
        """Cleanup ogni 5 minuti"""
        while True:
            await asyncio.sleep(300)
            for destination, pool in self.pools.items():
                await self._cleanup_pool(pool)
```

**2. Implementa Circuit Breaker per Memory**
```python
class MemoryCircuitBreaker:
    def __init__(self, threshold_mb=1024):
        self.threshold_mb = threshold_mb
        self.open = False

    def check_memory(self):
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024

        if memory_mb > self.threshold_mb:
            self.open = True
            logger.warning(f"Memory threshold exceeded: {memory_mb} MB")
            # Trigger graceful shutdown
            asyncio.create_task(self.graceful_shutdown())

        return not self.open

    async def graceful_shutdown(self):
        # Stop accepting new work
        # Complete current work
        # Shutdown gracefully
        pass
```

**3. Ottimizza Data Processing**
```python
# Usa streaming per large payloads
async def process_large_payload(payload):
    if len(payload) > 10 * 1024 * 1024:  # 10MB
        # Process in chunks
        chunk_size = 1024 * 1024  # 1MB chunks
        for i in range(0, len(payload), chunk_size):
            chunk = payload[i:i + chunk_size]
            await process_chunk(chunk)
            # Allow event loop to process other tasks
            await asyncio.sleep(0)
    else:
        # Process normally
        await process_payload(payload)
```

## [Auto-generated heading level 2]
### [Auto-generated heading level 3]
#### Prevenzione
- Implementa memory monitoring con alert
- Regular restart pods per prevenire memory leaks
- Profile application per identificare memory hotspots

---

## Procedure di Recovery

### 1. Recovery da Queue Full

```bash
# 1. Stop accepting new distributions
kubectl scale deployment ms07-distributor --replicas=0

# 2. Backup current queue
redis-cli --scan --pattern "distribution:queue:*" | head -1000 > queue_backup.txt

# 3. Clear queue if necessary
redis-cli DEL distribution:queue:default

# 4. Restart with increased capacity
kubectl scale deployment ms07-distributor --replicas=10

# 5. Monitor queue recovery
watch -n 5 'redis-cli LLEN distribution:queue:default'
```

## [Auto-generated heading level 2]
### 2. Recovery da Database Connection Loss

```sql
-- 1. Check database connectivity
SELECT 1;

-- 2. Verify replication status
SELECT * FROM pg_stat_replication;

-- 3. Failover to standby if needed
-- (Automatic failover configured)

-- 4. Reconnect application
kubectl rollout restart deployment/ms07-distributor
```

### 3. Recovery da Worker Crash

```bash
# 1. Check worker status
kubectl get pods -l app=ms07-distributor

# 2. View crash logs
kubectl logs <crashed-pod> --previous

# 3. Analyze core dump if available
# 4. Restart worker
kubectl delete pod <crashed-pod>

# 5. Verify recovery
kubectl logs -f <new-pod>
```

## Best Practices per Troubleshooting

### 1. Logging Strategy
- **Structured Logging**: JSON format per tutti i log
- **Correlation IDs**: Trace requests across components
- **Log Levels**: ERROR per problemi, WARN per potenziali problemi
- **Log Rotation**: Automatic rotation con retention policy

### 2. Monitoring Setup
- **RED Metrics**: Rate, Errors, Duration
- **USE Method**: Utilization, Saturation, Errors
- **Alert Rules**: Semplice ma efficace
- **Dashboard**: Real-time visibility

### 3. Runbook Automation
- **Automated Diagnosis**: Script per problemi comuni
- **Self-healing**: Auto-recovery dove possibile
- **Escalation**: Automatic ticket creation per problemi critici

### 4. Capacity Planning
- **Load Testing**: Regular performance testing
- **Resource Monitoring**: CPU, memory, network, disk
- **Scaling Policies**: Horizontal e vertical scaling
- **Cost Optimization**: Right-sizing resources

## Contatti e Escalation

### Team Support
- **DevOps**: `devops@zenia.it` - Infrastruttura e deployment
- **Backend**: `backend@zenia.it` - Logica applicativa
- **SRE**: `sre@zenia.it` - Reliability e performance

### Escalation Matrix
- **P1 (Critico)**: < 15 minuti - Sistema completamente down
- **P2 (Alto)**: < 1 ora - Funzionalità critiche compromesse
- **P3 (Medio)**: < 4 ore - Funzionalità non critiche
- **P4 (Basso)**: < 24 ore - Problemi minori

### Documentazione di Riferimento
- [API Documentation](./API.md)
- [Database Schema](./DATABASE-SCHEMA.md)
- [Kubernetes Configuration](./kubernetes/)
- [Monitoring Dashboards](https://grafana.zenia.local)