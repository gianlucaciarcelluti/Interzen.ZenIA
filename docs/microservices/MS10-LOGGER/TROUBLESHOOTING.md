# Troubleshooting Guide - MS10-LOGGER

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [API.md](API.md) | [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [← TROUBLESHOOTING.md] | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms10--logger)

## 1. Panoramica Troubleshooting

Questa guida fornisce procedure diagnostiche e risolutive per i problemi più comuni che possono verificarsi in MS10-LOGGER. Il sistema di logging è critico per l'osservabilità della piattaforma ZenIA, quindi è essenziale una rapida risoluzione dei problemi.

**Strumenti di Diagnosi**: Kibana Dev Tools, Elasticsearch API, Logstash Monitoring, Kafka Tools
**Log Levels**: ERROR (sistemi critici), WARN (problemi potenziali), INFO (operazioni normali)
**Alert Integration**: Integrazione con MS08-MONITOR per alert automatici

## 2. Problemi di Ingestion dei Log

### 2.1 Logstash Non Riceve Log da Kafka

#### Sintomi
- Logstash pipeline mostra 0 eventi processati
- Kafka consumer lag aumenta
- Errori nei log di Logstash: "Unable to connect to Kafka"

#### Diagnosi
```bash
# Verifica stato Kafka
kubectl get pods -l app=kafka -n zenia-logging

# Controlla consumer group
kafka-consumer-groups --bootstrap-server kafka-cluster:9092 \
  --group logstash-group \
  --describe

# Verifica configurazione Logstash
curl -X GET "elasticsearch:9200/_logstash/state" | jq '.pipelines.main'
```

#### Risoluzione
```yaml
# logstash.yml - Configurazione corretta
input {
  kafka {
    bootstrap_servers => "kafka-01:9092,kafka-02:9092,kafka-03:9092"
    topics => ["zenia-logs"]
    group_id => "logstash-main"
    consumer_threads => 3
    auto_offset_reset => "latest"
    decorate_events => true
    codec => json {
      charset => "UTF-8"
    }
  }
}
```

**Comandi di Recovery**:
```bash
# Reset consumer offset se necessario
kafka-consumer-groups --bootstrap-server kafka-cluster:9092 \
  --group logstash-group \
  --topic zenia-logs \
  --reset-offsets --to-latest \
  --execute
```

### 2.2 Logstash Parsing Errors

#### Sintomi
- Logstash mostra "_grokparsefailure" tags
- Log non indicizzati correttamente
- Campi mancanti negli indici Elasticsearch

#### Diagnosi
```bash
# Verifica pattern Grok
curl -X GET "elasticsearch:9200/zenia-logs-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {"term": {"tags": "_grokparsefailure"}},
    "size": 10
  }'
```

#### Risoluzione
```ruby
# Correggere pattern Grok
filter {
  grok {
    match => {
      "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{DATA:correlation_id} %{GREEDYDATA:message}"
    }
    tag_on_failure => ["grok_parse_failure"]
  }

  # Fallback per log non strutturati
  if "_grokparsefailure" in [tags] {
    mutate {
      add_field => {
        "raw_message" => "%{message}"
        "parse_status" => "fallback"
      }
    }
  }
}
```

### 2.3 Elasticsearch Indexing Failures

#### Sintomi
- Logstash mostra errori di indexing
- Documenti rifiutati da Elasticsearch
- Cluster status giallo/rosso

#### Diagnosi
```bash
# Verifica cluster health
curl -X GET "elasticsearch:9200/_cluster/health?pretty"

# Controlla indice specifico
curl -X GET "elasticsearch:9200/zenia-logs-*/_stats?pretty"

# Verifica errori di indexing
curl -X GET "elasticsearch:9200/zenia-logs-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {"term": {"_index": "zenia-logs-*"}},
    "size": 0,
    "aggs": {
      "index_errors": {
        "terms": {"field": "_index"}
      }
    }
  }'
```

#### Risoluzione
```bash
# Aumenta timeout di indexing
curl -X PUT "elasticsearch:9200/zenia-logs-*/_settings" \
  -H 'Content-Type: application/json' \
  -d '{
    "index": {
      "refresh_interval": "30s",
      "translog.durability": "async"
    }
  }'

# Verifica mapping conflicts
curl -X GET "elasticsearch:9200/zenia-logs-*/_mapping?pretty"
```

## 3. Problemi di Performance

### 3.1 Alta Latenza di Query

#### Sintomi
- Query Elasticsearch > 5 secondi
- Timeout nelle ricerche
- CPU elevata sui nodi data

#### Diagnosi
```bash
# Analizza query lenta
curl -X GET "elasticsearch:9200/_cluster/state?pretty" | jq '.routing_table'

# Verifica shard allocation
curl -X GET "elasticsearch:9200/_cat/shards/zenia-logs-*?v"

# Controlla hot threads
curl -X GET "elasticsearch:9200/_nodes/hot_threads?threads=10"
```

#### Risoluzione
```json
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"tenant_id": "tenant-pa-roma"}},
        {"range": {"timestamp": {"gte": "now-1h"}}}
      ],
      "must": [
        {"match": {"message": "error"}}
      ]
    }
  },
  "sort": [{"timestamp": {"order": "desc"}}],
  "_source": ["timestamp", "level", "service", "message"],
  "size": 100
}
```

**Ottimizzazioni**:
```bash
# Forza merge segments
curl -X POST "elasticsearch:9200/zenia-logs-*/_forcemerge?max_num_segments=1"

# Aumenta cache fielddata
curl -X PUT "elasticsearch:9200/zenia-logs-*/_settings" \
  -H 'Content-Type: application/json' \
  -d '{
    "indices": {
      "fielddata": {
        "cache": "50%"
      }
    }
  }'
```

### 3.2 Memory Pressure su Elasticsearch

#### Sintomi
- OutOfMemoryError nei log
- Circuit breaker attivati
- Query rifiutate

#### Diagnosi
```bash
# Verifica heap usage
curl -X GET "elasticsearch:9200/_nodes/stats/jvm?pretty" | jq '.nodes[].jvm.mem'

# Controlla circuit breakers
curl -X GET "elasticsearch:9200/_nodes/stats/breaker?pretty"
```

#### Risoluzione
```yaml
# elasticsearch.yml - Configurazione memory
bootstrap.memory_lock: true
indices.breaker.total.limit: 70%
indices.breaker.fielddata.limit: 40%
indices.breaker.request.limit: 40%

# JVM options
-Xms8g
-Xmx8g
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
```

### 3.3 Kafka Lag Elevato

#### Sintomi
- Consumer lag > 10000 messaggi
- Logstash non tiene il passo con ingestion
- Timeout nei consumer

#### Diagnosi
```bash
# Verifica consumer lag
kafka-consumer-groups --bootstrap-server kafka-cluster:9092 \
  --group logstash-group \
  --describe

# Controlla throughput Kafka
kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list kafka-cluster:9092 \
  --topic zenia-logs
```

#### Risoluzione
```yaml
# Aumenta consumer threads
input {
  kafka {
    consumer_threads => 6
    max_poll_records => 1000
    fetch_min_bytes => 1048576
    fetch_max_wait_ms => 500
  }
}

# Aumenta partizioni se necessario
kafka-topics --bootstrap-server kafka-cluster:9092 \
  --alter --topic zenia-logs \
  --partitions 12
```

## 4. Problemi di Storage

### 4.1 Disco Pieno sui Nodi Hot

#### Sintomi
- Elasticsearch rifiuta scritture
- Cluster status rosso
- Alert "disk watermark exceeded"

#### Diagnosi
```bash
# Verifica disk usage
curl -X GET "elasticsearch:9200/_nodes/stats/fs?pretty"

# Controlla watermark
curl -X GET "elasticsearch:9200/_cluster/settings?pretty" | jq '.persistent.cluster.routing.allocation.disk'
```

#### Risoluzione
```bash
# Aumenta watermark temporaneamente
curl -X PUT "elasticsearch:9200/_cluster/settings" \
  -H 'Content-Type: application/json' \
  -d '{
    "transient": {
      "cluster.routing.allocation.disk.watermark.low": "90%",
      "cluster.routing.allocation.disk.watermark.high": "95%",
      "cluster.routing.allocation.disk.watermark.flood_stage": "97%"
    }
  }'

# Forza rollover indice
curl -X POST "elasticsearch:9200/zenia-logs-*/_rollover"
```

### 4.2 Snapshot Failures

#### Sintomi
- Snapshot non completati
- Repository S3 non accessibile
- Timeout durante backup

#### Diagnosi
```bash
# Verifica stato snapshot
curl -X GET "elasticsearch:9200/_snapshot/_status?pretty"

# Controlla repository
curl -X GET "elasticsearch:9200/_snapshot/s3_repository?pretty"
```

#### Risoluzione
```json
{
  "type": "s3",
  "settings": {
    "bucket": "zenia-logging-backups",
    "region": "eu-west-1",
    "role_arn": "arn:aws:iam::123456789012:role/elasticsearch-snapshot-role",
    "base_path": "snapshots",
    "compress": true,
    "max_snapshot_bytes_per_sec": "100mb"
  }
}
```

## 5. Problemi di Sicurezza

### 5.1 Autenticazione Fallita

#### Sintomi
- 401 Unauthorized negli access log
- Token JWT scaduti
- API key non valida

#### Diagnosi
```bash
# Verifica token validity
curl -X POST "auth.zenia.local/oauth2/introspect" \
  -H "Content-Type: application/json" \
  -d '{"token": "jwt-token"}'

# Controlla audit logs
curl -X GET "elasticsearch:9200/zenia-audit-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "bool": {
        "must": [
          {"term": {"event_type": "AUTHENTICATION_FAILURE"}},
          {"range": {"timestamp": {"gte": "now-1h"}}}
        ]
      }
    }
  }'
```

#### Risoluzione
```bash
# Rotate API keys
curl -X POST "ms10-logger/v1/admin/keys/rotate" \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "ms01-classifier",
    "reason": "Security incident response"
  }'
```

### 5.2 Violazioni di Sicurezza

#### Sintomi
- Alert di sicurezza attivati
- Accessi non autorizzati rilevati
- Modifiche configurazione sospette

#### Diagnosi
```bash
# Query security events
curl -X GET "elasticsearch:9200/zenia-security-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "bool": {
        "must": [
          {"term": {"severity": "HIGH"}},
          {"range": {"timestamp": {"gte": "now-24h"}}}
        ]
      }
    },
    "sort": [{"timestamp": {"order": "desc"}}]
  }'
```

#### Risoluzione
```bash
# Blocca IP sospetto
curl -X POST "ms10-logger/v1/admin/security/block" \
  -H "Authorization: Bearer admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "ip_address": "192.168.1.100",
    "reason": "Brute force attack detected",
    "duration_hours": 24
  }'

# Audit configuration changes
curl -X GET "elasticsearch:9200/zenia-audit-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "term": {"action": "CONFIGURATION_CHANGE"}
    },
    "sort": [{"timestamp": {"order": "desc"}}],
    "size": 50
  }'
```

## 6. Problemi di Alerting

### 6.1 Alert Non Inviati

#### Sintomi
- Condizioni alert soddisfatte ma no notifiche
- Webhook failures
- Email non ricevute

#### Diagnosi
```bash
# Verifica alert rules
curl -X GET "ms10-logger/v1/alerts/rules?enabled=true" \
  -H "Authorization: Bearer token"

# Controlla alert history
curl -X GET "ms10-logger/v1/alerts/history?period=24h" \
  -H "Authorization: Bearer token"

# Verifica webhook endpoints
curl -X POST "https://monitoring.zenia.local/webhooks/test" \
  -H "Content-Type: application/json" \
  -d '{"test": "alert"}'
```

#### Risoluzione
```json
{
  "name": "Test Alert Rule",
  "description": "Test alert delivery",
  "enabled": true,
  "severity": "LOW",
  "query": {
    "match_all": {}
  },
  "condition": {
    "type": "always_true"
  },
  "actions": [
    {
      "type": "webhook",
      "url": "https://monitoring.zenia.local/webhooks/alert",
      "method": "POST",
      "headers": {
        "Authorization": "Bearer webhook-token",
        "Content-Type": "application/json"
      },
      "timeout_seconds": 30
    }
  ],
  "throttle_period": "5m"
}
```

### 6.2 Falsi Positivi negli Alert

#### Sintomi
- Alert attivati per condizioni normali
- Rumore eccessivo nelle notifiche
- Team desensitized agli alert

#### Diagnosi
```bash
# Analizza alert triggers
curl -X GET "ms10-logger/v1/alerts/analytics?period=7d" \
  -H "Authorization: Bearer token"

# Verifica soglie
curl -X GET "elasticsearch:9200/zenia-logs-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "query": {
      "range": {"timestamp": {"gte": "now-1h"}}
    },
    "aggs": {
      "error_rate": {
        "terms": {"field": "level"},
        "aggs": {
          "hourly": {
            "date_histogram": {
              "field": "timestamp",
              "interval": "1h"
            }
          }
        }
      }
    }
  }'
```

#### Risoluzione
```json
{
  "name": "Refined Error Rate Alert",
  "query": {
    "bool": {
      "must": [
        {"term": {"level": "ERROR"}},
        {"term": {"service": "ms01-classifier"}},
        {"range": {"timestamp": {"gte": "now-5m"}}}
      ],
      "must_not": [
        {"term": {"error_code": "OCR_QUALITY_LOW"}},
        {"term": {"error_code": "TEMPORARY_NETWORK_ISSUE"}}
      ]
    }
  },
  "condition": {
    "type": "threshold",
    "field": "doc_count",
    "operator": "gte",
    "value": 10,
    "time_window": "5m"
  },
  "throttle_period": "15m"
}
```

## 7. Problemi di Configurazione

### 7.1 Pipeline Configuration Errors

#### Sintomi
- Logstash non avvia
- Configurazione rifiutata
- Plugin errors

#### Diagnosi
```bash
# Valida configurazione
/usr/share/logstash/bin/logstash -f /etc/logstash/pipeline/ --config.test_and_exit

# Verifica plugin installati
/usr/share/logstash/bin/logstash-plugin list

# Controlla log di avvio
kubectl logs -f deployment/logstash -n zenia-logging
```

#### Risoluzione
```ruby
# Configurazione corretta pipeline
input {
  kafka {
    bootstrap_servers => ["kafka-01:9092", "kafka-02:9092"]
    topics => ["zenia-logs"]
    codec => json
    consumer_threads => 3
    session_timeout_ms => 30000
    request_timeout_ms => 40000
  }
}

filter {
  json {
    source => "message"
    target => "parsed"
  }

  date {
    match => ["timestamp", "ISO8601"]
    target => "@timestamp"
  }

  mutate {
    remove_field => ["message"]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "zenia-logs-%{+YYYY.MM.dd}"
    document_type => "_doc"
  }
}
```

### 7.2 Tenant Isolation Issues

#### Sintomi
- Log di un tenant visibili ad altri
- Query cross-tenant
- Violazioni isolamento dati

#### Diagnosi
```bash
# Verifica filtri tenant
curl -X GET "elasticsearch:9200/zenia-logs-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {"match_all": {}},
    "aggs": {
      "tenants": {"terms": {"field": "tenant_id", "size": 100}}
    }
  }'

# Controlla role mappings
curl -X GET "elasticsearch:9200/_security/role/zenia_log_viewer"
```

#### Risoluzione
```json
{
  "zenia_log_viewer": {
    "indices": [
      {
        "names": ["zenia-logs-*"],
        "privileges": ["read"],
        "query": {
          "term": {"tenant_id": "{{_user.metadata.tenant_id}}"}
        }
      }
    ]
  }
}
```

## 8. Recovery Procedures

### 8.1 Disaster Recovery

#### Cluster Failure Recovery
```bash
# 1. Verifica backup disponibili
curl -X GET "elasticsearch:9200/_snapshot/s3_repository/_all?pretty"

# 2. Chiudi indice se necessario
curl -X POST "elasticsearch:9200/zenia-logs-*/_close"

# 3. Restore da snapshot
curl -X POST "elasticsearch:9200/_snapshot/s3_repository/snapshot_20240115/_restore" \
  -H 'Content-Type: application/json' \
  -d '{
    "indices": "zenia-logs-*",
    "ignore_unavailable": true
  }'

# 4. Riapri indice
curl -X POST "elasticsearch:9200/zenia-logs-*/_open"
```

#### Data Loss Recovery
```bash
# 1. Identifica gap nei dati
curl -X GET "elasticsearch:9200/zenia-logs-*/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "query": {
      "range": {"timestamp": {"gte": "2024-01-15T10:00:00Z", "lte": "2024-01-15T11:00:00Z"}}
    },
    "aggs": {
      "hourly_count": {
        "date_histogram": {"field": "timestamp", "interval": "1h"}
      }
    }
  }'

# 2. Re-ingest da Kafka se disponibile
kafka-console-consumer --bootstrap-server kafka-cluster:9092 \
  --topic zenia-logs \
  --from-beginning \
  --max-messages 1000 > recovery_logs.json

# 3. Bulk re-index
curl -X POST "elasticsearch:9200/_bulk" \
  -H 'Content-Type: application/json' \
  --data-binary @recovery_logs.json
```

### 8.2 Performance Degradation Recovery

#### Memory Issues
```bash
# 1. Monitora heap usage
curl -X GET "elasticsearch:9200/_nodes/stats/jvm?pretty"

# 2. Force garbage collection
curl -X POST "elasticsearch:9200/_nodes/_all/jvm/gc"

# 3. Restart problematic nodes
kubectl delete pod elasticsearch-data-0 -n zenia-logging
```

#### Slow Queries
```bash
# 1. Identifica query lente
curl -X GET "elasticsearch:9200/_nodes/hot_threads?threads=5"

# 2. Aggiungi index hints
curl -X POST "elasticsearch:9200/zenia-logs-*/_forcemerge?max_num_segments=5"

# 3. Ottimizza mapping
curl -X PUT "elasticsearch:9200/zenia-logs-*/_mapping" \
  -H 'Content-Type: application/json' \
  -d '{
    "properties": {
      "correlation_id": {
        "type": "keyword",
        "index": true,
        "doc_values": false
      }
    }
  }'
```

## 9. Monitoraggio e Alert di Sistema

### 9.1 Metriche Chiave da Monitorare

```yaml
# Prometheus metrics
elasticsearch_cluster_health_status: 1
elasticsearch_cluster_nodes_number: 9
elasticsearch_indices_docs_total{index="zenia-logs-*"}: 1000000
logstash_pipeline_events_out_total: 50000
kafka_consumer_group_lag: 100

# Alert rules
groups:
  - name: logging_system
    rules:
      - alert: ElasticsearchClusterUnhealthy
        expr: elasticsearch_cluster_health_status != 1
        for: 5m
        labels:
          severity: critical

      - alert: LogstashPipelineStuck
        expr: rate(logstash_pipeline_events_out_total[5m]) < 100
        for: 10m
        labels:
          severity: warning

      - alert: HighKafkaConsumerLag
        expr: kafka_consumer_group_lag > 10000
        for: 5m
        labels:
          severity: warning
```

### 9.2 Log Patterns per Troubleshooting

```bash
# Error patterns
grep "ERROR.*Elasticsearch" /var/log/logstash/logstash.log
grep "WARN.*circuit breaker" /var/log/elasticsearch/elasticsearch.log
grep "timeout" /var/log/kafka/kafka.log

# Performance patterns
grep "slowlog" /var/log/elasticsearch/elasticsearch.log
grep "gc" /var/log/elasticsearch/gc.log
grep "lag" /var/log/kafka/kafka.log
```

Questa guida troubleshooting fornisce procedure complete per diagnosticare e risolvere i problemi più comuni in MS10-LOGGER, garantendo alta disponibilità e performance del sistema di logging centralizzato.