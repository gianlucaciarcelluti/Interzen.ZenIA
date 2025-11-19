# Database Schema - MS10-LOGGER

**Navigazione**: [README.md](README.md) | [SPECIFICATION.md](SPECIFICATION.md) | [API.md](API.md) | [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOUTING.md](TROUBLESHOUTING.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms10--logger)

## 1. Panoramica Architettura Database

MS10-LOGGER utilizza Elasticsearch come database primario per l'archiviazione e l'indicizzazione dei log, integrato con data tiering (Hot/Warm/Cold) per ottimizzare costi e performance. Il sistema supporta anche PostgreSQL per metadati e configurazioni.

**Database Primario**: Elasticsearch 8.x (Log Storage & Analytics)
**Database Secondario**: PostgreSQL 15 (Metadata & Configuration)
**Architettura**: Data Tiering con ILM (Index Lifecycle Management)
**Retention**: 7 anni per audit logs, 1 anno per application logs

## 2. Elasticsearch Index Schemas

### 2.1 Application Logs Index

#### Index Template: `zenia-logs`
```json
{
  "index_patterns": ["zenia-logs-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "refresh_interval": "30s",
      "index.codec": "best_compression",
      "index.routing.allocation.require.data": "hot",
      "analysis": {
        "analyzer": {
          "zenia_log_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "zenia_stop", "zenia_stemmer"]
          }
        },
        "filter": {
          "zenia_stop": {
            "type": "stop",
            "stopwords": ["_italian_", "log", "error", "info", "warn"]
          },
          "zenia_stemmer": {
            "type": "stemmer",
            "language": "italian"
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "id": {
          "type": "keyword",
          "index": true
        },
        "timestamp": {
          "type": "date",
          "format": "strict_date_optional_time||epoch_millis",
          "index": true
        },
        "ingestion_timestamp": {
          "type": "date",
          "format": "strict_date_optional_time||epoch_millis",
          "index": true
        },
        "processing_timestamp": {
          "type": "date",
          "format": "yyyy-MM-dd HH:mm:ss.SSS",
          "index": true
        },
        "level": {
          "type": "keyword",
          "index": true
        },
        "service": {
          "type": "keyword",
          "index": true
        },
        "instance": {
          "type": "keyword",
          "index": true
        },
        "version": {
          "type": "keyword",
          "index": true
        },
        "environment": {
          "type": "keyword",
          "index": true
        },
        "region": {
          "type": "keyword",
          "index": true
        },
        "correlation_id": {
          "type": "keyword",
          "index": true
        },
        "request_id": {
          "type": "keyword",
          "index": true
        },
        "session_id": {
          "type": "keyword",
          "index": true
        },
        "user_id": {
          "type": "keyword",
          "index": true
        },
        "tenant_id": {
          "type": "keyword",
          "index": true
        },
        "message": {
          "type": "text",
          "analyzer": "zenia_log_analyzer",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          },
          "index": true
        },
        "formatted_message": {
          "type": "text",
          "analyzer": "zenia_log_analyzer",
          "index": true
        },
        "context": {
          "type": "object",
          "dynamic": true,
          "properties": {
            "document_id": {"type": "keyword"},
            "workflow_id": {"type": "keyword"},
            "step_id": {"type": "keyword"},
            "processing_time_ms": {"type": "long"},
            "retry_count": {"type": "integer"},
            "error_code": {"type": "keyword"},
            "error_details": {"type": "text"}
          }
        },
        "mdc": {
          "type": "object",
          "dynamic": true,
          "properties": {
            "client_ip": {"type": "ip"},
            "user_agent": {"type": "text"},
            "request_method": {"type": "keyword"},
            "request_uri": {"type": "keyword"},
            "response_status": {"type": "integer"},
            "response_time_ms": {"type": "long"},
            "bytes_sent": {"type": "long"},
            "bytes_received": {"type": "long"}
          }
        },
        "metrics": {
          "type": "object",
          "dynamic": true,
          "properties": {
            "cpu_usage_percent": {"type": "float"},
            "memory_usage_mb": {"type": "float"},
            "disk_usage_percent": {"type": "float"},
            "network_in_bytes": {"type": "long"},
            "network_out_bytes": {"type": "long"},
            "active_threads": {"type": "integer"},
            "heap_used_mb": {"type": "float"},
            "heap_max_mb": {"type": "float"}
          }
        },
        "geo": {
          "type": "object",
          "properties": {
            "country_code": {"type": "keyword"},
            "country_name": {"type": "keyword"},
            "region_code": {"type": "keyword"},
            "region_name": {"type": "keyword"},
            "city_name": {"type": "keyword"},
            "postal_code": {"type": "keyword"},
            "location": {"type": "geo_point"},
            "timezone": {"type": "keyword"}
          }
        },
        "enrichment": {
          "type": "object",
          "dynamic": true,
          "properties": {
            "tenant_info": {
              "type": "object",
              "properties": {
                "name": {"type": "keyword"},
                "type": {"type": "keyword"},
                "region": {"type": "keyword"},
                "compliance_level": {"type": "keyword"}
              }
            },
            "user_info": {
              "type": "object",
              "properties": {
                "full_name": {"type": "text"},
                "role": {"type": "keyword"},
                "department": {"type": "keyword"},
                "clearance_level": {"type": "keyword"}
              }
            },
            "business_context": {
              "type": "object",
              "properties": {
                "document_type": {"type": "keyword"},
                "process_type": {"type": "keyword"},
                "urgency_level": {"type": "keyword"},
                "regulatory_reference": {"type": "keyword"}
              }
            }
          }
        },
        "processing": {
          "type": "object",
          "properties": {
            "pipeline_version": {"type": "keyword"},
            "processing_node": {"type": "keyword"},
            "parsing_errors": {"type": "text"},
            "enrichment_errors": {"type": "text"},
            "warnings": {"type": "text"},
            "processing_time_ms": {"type": "long"}
          }
        },
        "tags": {
          "type": "keyword",
          "index": true
        },
        "labels": {
          "type": "object",
          "dynamic": true
        },
        "pipeline_version": {
          "type": "keyword",
          "index": true
        }
      }
    }
  }
}
```

#### Index Lifecycle Management Policy
```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_age": "1d",
            "max_size": "50gb"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "allocate": {
            "number_of_replicas": 1,
            "include": { "data": "warm" }
          },
          "shrink": {
            "number_of_shards": 1
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "allocate": {
            "number_of_replicas": 0,
            "include": { "data": "cold" }
          },
          "set_priority": {
            "priority": 0
          },
          "searchable_snapshot": {
            "snapshot_repository": "cold_logs_snapshot"
          }
        }
      },
      "delete": {
        "min_age": "365d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### 2.2 Security Events Index

#### Index Template: `zenia-security`
```json
{
  "index_patterns": ["zenia-security-*"],
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 2,
      "refresh_interval": "10s",
      "index.codec": "best_compression",
      "index.routing.allocation.require.data": "hot"
    },
    "mappings": {
      "properties": {
        "id": {
          "type": "keyword",
          "index": true
        },
        "timestamp": {
          "type": "date",
          "format": "strict_date_optional_time||epoch_millis",
          "index": true
        },
        "event_type": {
          "type": "keyword",
          "index": true
        },
        "severity": {
          "type": "keyword",
          "index": true
        },
        "source": {
          "type": "object",
          "properties": {
            "service": {"type": "keyword"},
            "instance": {"type": "keyword"},
            "component": {"type": "keyword"},
            "version": {"type": "keyword"}
          }
        },
        "actor": {
          "type": "object",
          "properties": {
            "type": {"type": "keyword"},
            "identifier": {"type": "keyword"},
            "name": {"type": "text"},
            "roles": {"type": "keyword"},
            "ip_address": {"type": "ip"},
            "user_agent": {"type": "text"},
            "location": {
              "type": "object",
              "properties": {
                "country": {"type": "keyword"},
                "city": {"type": "keyword"},
                "coordinates": {"type": "geo_point"}
              }
            }
          }
        },
        "resource": {
          "type": "object",
          "properties": {
            "type": {"type": "keyword"},
            "identifier": {"type": "keyword"},
            "attributes": {"type": "object", "dynamic": true}
          }
        },
        "action": {
          "type": "object",
          "properties": {
            "name": {"type": "keyword"},
            "category": {"type": "keyword"},
            "description": {"type": "text"}
          }
        },
        "violation": {
          "type": "object",
          "properties": {
            "type": {"type": "keyword"},
            "description": {"type": "text"},
            "required_permissions": {"type": "keyword"},
            "actual_permissions": {"type": "keyword"},
            "policy_id": {"type": "keyword"}
          }
        },
        "result": {
          "type": "object",
          "properties": {
            "status": {"type": "keyword"},
            "details": {"type": "object", "dynamic": true}
          }
        },
        "context": {
          "type": "object",
          "properties": {
            "correlation_id": {"type": "keyword"},
            "request_id": {"type": "keyword"},
            "tenant_id": {"type": "keyword"},
            "session_start": {"type": "date"},
            "session_duration_ms": {"type": "long"}
          }
        },
        "enrichment": {
          "type": "object",
          "properties": {
            "risk_score": {"type": "float"},
            "similar_events_count": {"type": "integer"},
            "user_risk_profile": {"type": "keyword"},
            "ip_reputation": {"type": "keyword"},
            "threat_intelligence": {"type": "object", "dynamic": true}
          }
        },
        "mitigation": {
          "type": "object",
          "properties": {
            "actions_taken": {"type": "keyword"},
            "recommended_actions": {"type": "text"},
            "escalation_required": {"type": "boolean"},
            "escalation_level": {"type": "keyword"}
          }
        },
        "processing": {
          "type": "object",
          "properties": {
            "pipeline_version": {"type": "keyword"},
            "processing_time_ms": {"type": "long"},
            "alert_generated": {"type": "boolean"},
            "alert_id": {"type": "keyword"}
          }
        }
      }
    }
  }
}
```

#### Security Events ILM Policy
```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_age": "6h",
            "max_size": "10gb"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "2d",
        "actions": {
          "allocate": {
            "number_of_replicas": 1,
            "include": { "data": "warm" }
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "allocate": {
            "number_of_replicas": 0,
            "include": { "data": "cold" }
          },
          "set_priority": {
            "priority": 0
          },
          "searchable_snapshot": {
            "snapshot_repository": "security_snapshot"
          }
        }
      },
      "delete": {
        "min_age": "7y",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

### 2.3 Audit Logs Index

#### Index Template: `zenia-audit`
```json
{
  "index_patterns": ["zenia-audit-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 2,
      "refresh_interval": "5s",
      "index.codec": "best_compression",
      "index.routing.allocation.require.data": "hot"
    },
    "mappings": {
      "properties": {
        "id": {
          "type": "keyword",
          "index": true
        },
        "timestamp": {
          "type": "date",
          "format": "strict_date_optional_time||epoch_millis",
          "index": true
        },
        "event_type": {
          "type": "keyword",
          "index": true
        },
        "actor": {
          "type": "object",
          "properties": {
            "type": {"type": "keyword"},
            "identifier": {"type": "keyword"},
            "name": {"type": "text"},
            "roles": {"type": "keyword"},
            "department": {"type": "keyword"}
          }
        },
        "action": {
          "type": "object",
          "properties": {
            "name": {"type": "keyword"},
            "category": {"type": "keyword"},
            "description": {"type": "text"}
          }
        },
        "resource": {
          "type": "object",
          "properties": {
            "type": {"type": "keyword"},
            "identifier": {"type": "keyword"},
            "attributes": {"type": "object", "dynamic": true}
          }
        },
        "context": {
          "type": "object",
          "properties": {
            "tenant_id": {"type": "keyword"},
            "session_id": {"type": "keyword"},
            "correlation_id": {"type": "keyword"},
            "ip_address": {"type": "ip"},
            "user_agent": {"type": "text"},
            "location": {"type": "keyword"}
          }
        },
        "result": {
          "type": "object",
          "properties": {
            "status": {"type": "keyword"},
            "details": {"type": "object", "dynamic": true}
          }
        },
        "compliance": {
          "type": "object",
          "properties": {
            "gdpr_compliant": {"type": "boolean"},
            "retention_required": {"type": "boolean"},
            "retention_period_years": {"type": "integer"},
            "data_sensitivity": {"type": "keyword"},
            "regulatory_reference": {"type": "keyword"}
          }
        },
        "enrichment": {
          "type": "object",
          "properties": {
            "business_context": {"type": "text"},
            "regulatory_reference": {"type": "keyword"},
            "risk_assessment": {"type": "keyword"},
            "anomaly_score": {"type": "float"}
          }
        },
        "processing": {
          "type": "object",
          "properties": {
            "pipeline_version": {"type": "keyword"},
            "processing_time_ms": {"type": "long"},
            "validation_errors": {"type": "text"}
          }
        }
      }
    }
  }
}
```

#### Audit Logs ILM Policy (No Deletion)
```json
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_age": "1d",
            "max_size": "5gb"
          },
          "set_priority": {
            "priority": 100
          }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "allocate": {
            "number_of_replicas": 1,
            "include": { "data": "warm" }
          },
          "set_priority": {
            "priority": 50
          }
        }
      },
      "cold": {
        "min_age": "1y",
        "actions": {
          "allocate": {
            "number_of_replicas": 0,
            "include": { "data": "cold" }
          },
          "set_priority": {
            "priority": 0
          },
          "searchable_snapshot": {
            "snapshot_repository": "audit_snapshot"
          }
        }
      }
    }
  }
}
```

### 2.4 Metrics Index

#### Index Template: `zenia-metrics`
```json
{
  "index_patterns": ["zenia-metrics-*"],
  "template": {
    "settings": {
      "number_of_shards": 2,
      "number_of_replicas": 1,
      "refresh_interval": "10s",
      "index.codec": "best_compression"
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "strict_date_optional_time||epoch_millis"
        },
        "service": {
          "type": "keyword"
        },
        "instance": {
          "type": "keyword"
        },
        "metric_type": {
          "type": "keyword"
        },
        "metric_name": {
          "type": "keyword"
        },
        "value": {
          "type": "double"
        },
        "unit": {
          "type": "keyword"
        },
        "tags": {
          "type": "object",
          "dynamic": true
        },
        "dimensions": {
          "type": "object",
          "dynamic": true
        },
        "metadata": {
          "type": "object",
          "dynamic": true
        }
      }
    }
  }
}
```

## 3. PostgreSQL Schema

### 3.1 Configuration Tables

#### Alert Rules Table
```sql
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    enabled BOOLEAN DEFAULT true,
    severity VARCHAR(20) CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    query JSONB NOT NULL,
    condition JSONB NOT NULL,
    actions JSONB NOT NULL,
    throttle_period INTERVAL DEFAULT '10 minutes',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100),

    UNIQUE(tenant_id, name)
);

CREATE INDEX idx_alert_rules_tenant_enabled ON alert_rules(tenant_id, enabled);
CREATE INDEX idx_alert_rules_severity ON alert_rules(severity);
```

#### Alert Instances Table
```sql
CREATE TABLE alert_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id UUID NOT NULL REFERENCES alert_rules(id) ON DELETE CASCADE,
    tenant_id VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'ACKNOWLEDGED', 'RESOLVED', 'CLOSED')),
    severity VARCHAR(20) CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    context JSONB,
    triggered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    acknowledged_by VARCHAR(100),
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR(100),
    closed_at TIMESTAMP WITH TIME ZONE,
    closed_by VARCHAR(100),

    FOREIGN KEY (rule_id) REFERENCES alert_rules(id)
);

CREATE INDEX idx_alert_instances_tenant_status ON alert_instances(tenant_id, status);
CREATE INDEX idx_alert_instances_rule ON alert_instances(rule_id);
CREATE INDEX idx_alert_instances_triggered ON alert_instances(triggered_at);
```

#### Pipeline Configurations Table
```sql
CREATE TABLE pipeline_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    version VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED')),
    configuration JSONB NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100),

    UNIQUE(name, version)
);

CREATE INDEX idx_pipeline_configs_status ON pipeline_configs(status);
CREATE INDEX idx_pipeline_configs_name ON pipeline_configs(name);
```

#### Tenant Configurations Table
```sql
CREATE TABLE tenant_configs (
    tenant_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('PA', 'ENTERPRISE', 'DEMO')),
    region VARCHAR(50),
    compliance_level VARCHAR(20) DEFAULT 'STANDARD',
    log_retention_days INTEGER DEFAULT 365,
    security_retention_days INTEGER DEFAULT 2555, -- 7 years
    audit_retention_days INTEGER DEFAULT 2555,   -- 7 years
    max_daily_logs BIGINT DEFAULT 10000000,
    alert_email_recipients JSONB,
    webhook_endpoints JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tenant_configs_type ON tenant_configs(type);
CREATE INDEX idx_tenant_configs_region ON tenant_configs(region);
```

### 3.2 Audit Tables

#### Access Audit Table
```sql
CREATE TABLE access_audit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tenant_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(100),
    session_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),
    query JSONB,
    result_count INTEGER,
    response_time_ms INTEGER,
    status VARCHAR(20) DEFAULT 'SUCCESS',
    error_message TEXT,
    correlation_id VARCHAR(100)
);

CREATE INDEX idx_access_audit_tenant_timestamp ON access_audit(tenant_id, timestamp);
CREATE INDEX idx_access_audit_user ON access_audit(user_id);
CREATE INDEX idx_access_audit_action ON access_audit(action);
CREATE INDEX idx_access_audit_correlation ON access_audit(correlation_id);

-- Partition by month for performance
CREATE TABLE access_audit_y2024m01 PARTITION OF access_audit
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

#### Configuration Changes Audit Table
```sql
CREATE TABLE config_changes_audit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tenant_id VARCHAR(50),
    user_id VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL, -- CREATE, UPDATE, DELETE
    resource_type VARCHAR(50) NOT NULL,
    resource_id VARCHAR(255),
    old_values JSONB,
    new_values JSONB,
    change_reason TEXT,
    ip_address INET,
    user_agent TEXT
);

CREATE INDEX idx_config_changes_tenant_timestamp ON config_changes_audit(tenant_id, timestamp);
CREATE INDEX idx_config_changes_user ON config_changes_audit(user_id);
CREATE INDEX idx_config_changes_resource ON config_changes_audit(resource_type, resource_id);
```

## 4. Data Retention Policies

### 4.1 Elasticsearch Retention

#### Application Logs
- **Hot Tier**: 7 giorni
- **Warm Tier**: 30 giorni (da 7 giorni)
- **Cold Tier**: 365 giorni (da 30 giorni)
- **Delete**: Dopo 365 giorni

#### Security Events
- **Hot Tier**: 2 giorni
- **Warm Tier**: 30 giorni (da 2 giorni)
- **Cold Tier**: 7 anni (da 30 giorni)
- **Delete**: Dopo 7 anni

#### Audit Logs
- **Hot Tier**: 30 giorni
- **Warm Tier**: 1 anno (da 30 giorni)
- **Cold Tier**: Indefinito (da 1 anno, searchable snapshots)

#### Metrics
- **Hot Tier**: 24 ore
- **Warm Tier**: 7 giorni (da 24 ore)
- **Cold Tier**: 30 giorni (da 7 giorni)
- **Delete**: Dopo 30 giorni

### 4.2 PostgreSQL Retention

#### Alert Instances
- **Retention**: 1 anno
- **Archival**: Dopo 90 giorni, spostati su storage a freddo
- **Deletion**: Dopo 1 anno

#### Access Audit
- **Retention**: 7 anni (requisito GDPR)
- **Partitioning**: Per mese
- **Archival**: Dopo 2 anni, spostati su storage a freddo
- **Deletion**: Dopo 7 anni

#### Configuration Changes
- **Retention**: 7 anni
- **Archival**: Dopo 1 anno, spostati su storage a freddo
- **Deletion**: Dopo 7 anni

## 5. Backup e Recovery

### 5.1 Elasticsearch Snapshots

#### Snapshot Repositories
```json
{
  "type": "s3",
  "settings": {
    "bucket": "zenia-logging-backups",
    "region": "eu-west-1",
    "role_arn": "arn:aws:iam::123456789012:role/elasticsearch-snapshot-role",
    "base_path": "snapshots"
  }
}
```

#### Automated Snapshot Policy
```json
{
  "schedule": "0 30 1 * * ?",
  "name": "<daily-snap-{now/d}>",
  "repository": "s3_repository",
  "config": {
    "indices": "*",
    "ignore_unavailable": true,
    "include_global_state": false,
    "partial": false
  },
  "retention": {
    "expire_after": "30d",
    "min_count": 7,
    "max_count": 30
  }
}
```

### 5.2 PostgreSQL Backups

#### Backup Strategy
```bash
#!/bin/bash
# Daily PostgreSQL backup script

BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="zenia_logger"

# Create backup
pg_dump -h localhost -U zenia_logger -d $DB_NAME \
  --format=custom \
  --compress=9 \
  --file="$BACKUP_DIR/${DB_NAME}_${DATE}.backup"

# Retention: keep last 30 daily backups
find $BACKUP_DIR -name "${DB_NAME}_*.backup" -mtime +30 -delete
```

#### Point-in-Time Recovery
```sql
-- Create recovery configuration
SELECT pg_create_restore_point('before_major_config_change');

-- In case of recovery
-- 1. Stop PostgreSQL
-- 2. Restore from backup
-- 3. Start PostgreSQL in recovery mode
-- 4. Set recovery target
-- 5. Start PostgreSQL
```

## 6. Performance Optimization

### 6.1 Index Optimization

#### Index Settings for Query Performance
```json
{
  "settings": {
    "index": {
      "refresh_interval": "30s",
      "translog": {
        "durability": "async",
        "sync_interval": "5s"
      },
      "merge": {
        "scheduler": {
          "max_thread_count": 1
        }
      }
    }
  }
}
```

#### Index Templates for Time Series
```json
{
  "index_patterns": ["zenia-logs-2024-*"],
  "template": {
    "settings": {
      "index": {
        "lifecycle": {
          "name": "zenia_logs_lifecycle"
        },
        "routing": {
          "allocation": {
            "include": {
              "_tier_preference": "data_hot"
            }
          }
        }
      }
    }
  }
}
```

### 6.2 Query Optimization

#### Optimized Query Patterns
```json
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"tenant_id": "tenant-pa-roma"}},
        {"range": {"timestamp": {"gte": "now-1h", "lte": "now"}}}
      ],
      "must": [
        {"match": {"message": "error"}}
      ]
    }
  },
  "sort": [
    {"timestamp": {"order": "desc"}}
  ],
  "_source": ["timestamp", "level", "service", "message"],
  "size": 100
}
```

#### Aggregation Optimization
```json
{
  "size": 0,
  "query": {
    "range": {
      "timestamp": {
        "gte": "now-1h",
        "lte": "now"
      }
    }
  },
  "aggs": {
    "errors_by_service": {
      "terms": {
        "field": "service",
        "size": 10
      },
      "aggs": {
        "error_rate": {
          "bucket_script": {
            "buckets_path": {
              "total": "_count",
              "errors": "error_count>_count"
            },
            "script": "params.errors / params.total * 100"
          }
        }
      }
    }
  }
}
```

## 7. Monitoring e Alerting

### 7.1 Elasticsearch Monitoring

#### Cluster Health Metrics
```json
{
  "cluster_name": "zenia-logging",
  "status": "green",
  "timed_out": false,
  "number_of_nodes": 9,
  "number_of_data_nodes": 6,
  "active_primary_shards": 45,
  "active_shards": 90,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100.0
}
```

#### Index Metrics
```json
{
  "indices": {
    "zenia-logs-2024.01.15": {
      "health": "green",
      "status": "open",
      "index": "zenia-logs-2024.01.15",
      "uuid": "abc123",
      "pri": "3",
      "rep": "1",
      "docs.count": "1250000",
      "docs.deleted": "0",
      "store.size": "2.1gb",
      "pri.store.size": "1.05gb"
    }
  }
}
```

### 7.2 PostgreSQL Monitoring

#### Key Metrics to Monitor
```sql
-- Connection status
SELECT count(*) as active_connections
FROM pg_stat_activity
WHERE state = 'active';

-- Table sizes
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT schemaname, tablename, indexname,
       idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

Questa documentazione dello schema database fornisce tutte le specifiche per l'archiviazione, l'indicizzazione e la gestione dei dati di log in MS10-LOGGER, garantendo performance ottimali, compliance e disaster recovery.