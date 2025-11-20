# Esempi Log Entries - MS10-LOGGER

Questa directory contiene esempi di payload JSON per diversi tipi di log gestiti da MS10-LOGGER.

## 1. Application Log Entry

**File**: `application-log-entry.json`
```json
{
  "$schema": "https://zenia.local/schemas/log-entry-v2.0.json",
  "id": "log-123456789-abcdef-001",
  "timestamp": "2024-01-15T10:30:45.123Z",
  "ingestion_timestamp": "2024-01-15T10:30:45.145Z",
  "processing_timestamp": "2024-01-15T10:30:45.167Z",

  "source": {
    "type": "application",
    "service": "ms01-classifier",
    "instance": "ms01-classifier-7x9k2",
    "version": "2.1.0",
    "environment": "production",
    "region": "eu-west-1"
  },

  "context": {
    "tenant_id": "tenant-pa-roma",
    "user_id": "user-pa-roma-789",
    "session_id": "session-pa-roma-20240115-001",
    "correlation_id": "corr-123-abc-456-def-789-ghi",
    "request_id": "req-456-def-789-ghi-jkl",
    "trace_id": "trace-789-ghi-jkl-mno-pqr"
  },

  "log": {
    "level": "INFO",
    "logger": "com.zenia.classifier.DocumentClassifier",
    "thread": "workflow-executor-5",
    "message": "Document classification completed successfully",
    "formatted_message": "2024-01-15 10:30:45.123 INFO [workflow-executor-5] com.zenia.classifier.DocumentClassifier - Document classification completed successfully"
  },

  "data": {
    "document_id": "DOC-2024-001234-ABC",
    "classification_result": {
      "category": "provvedimento",
      "confidence": 0.87,
      "subcategories": ["autorizzazione", "ambientale"],
      "processing_time_ms": 1250,
      "model_version": "pa-documents-v2.1"
    },
    "metrics": {
      "cpu_usage_percent": 45.2,
      "memory_usage_mb": 512.8,
      "response_time_ms": 1250
    }
  },

  "mdc": {
    "client_ip": "192.168.1.100",
    "user_agent": "ZenIA-PA-Portal/2.1.0",
    "request_method": "POST",
    "request_uri": "/api/v1/classify",
    "response_status": 200
  },

  "enrichment": {
    "geo": {
      "country_name": "Italy",
      "city_name": "Rome",
      "region_name": "Lazio",
      "location": {
        "lat": 41.9028,
        "lon": 12.4964
      }
    },
    "tenant_info": {
      "name": "Comune di Roma",
      "type": "PA",
      "region": "Lazio",
      "compliance_level": "high"
    },
    "user_info": {
      "full_name": "Mario Rossi",
      "role": "operator",
      "department": "Ambiente",
      "clearance_level": "standard"
    }
  },

  "processing": {
    "pipeline_version": "2.1.0",
    "processing_node": "logstash-02",
    "parsing_errors": [],
    "enrichment_errors": [],
    "warnings": []
  },

  "tags": ["application", "classification", "success"],
  "labels": {
    "severity": "info",
    "category": "business",
    "compliance": "gdpr-compliant"
  }
}
```

## 2. Error Log Entry

**File**: `error-log-entry.json`
```json
{
  "id": "log-123456789-abcdef-002",
  "timestamp": "2024-01-15T10:31:15.456Z",
  "ingestion_timestamp": "2024-01-15T10:31:15.478Z",
  "processing_timestamp": "2024-01-15T10:31:15.492Z",

  "source": {
    "type": "application",
    "service": "ms02-analyzer",
    "instance": "ms02-analyzer-4n5m7",
    "version": "2.1.0",
    "environment": "production"
  },

  "context": {
    "tenant_id": "tenant-pa-roma",
    "correlation_id": "corr-123-abc-456-def-789-ghi",
    "request_id": "req-456-def-789-ghi-jkl"
  },

  "log": {
    "level": "ERROR",
    "logger": "com.zenia.analyzer.TextAnalyzer",
    "thread": "analysis-pool-3",
    "message": "Failed to analyze document: OCR quality too low",
    "formatted_message": "2024-01-15 10:31:15.456 ERROR [analysis-pool-3] com.zenia.analyzer.TextAnalyzer - Failed to analyze document: OCR quality too low"
  },

  "data": {
    "document_id": "DOC-2024-001234-ABC",
    "error_details": {
      "error_code": "OCR_QUALITY_LOW",
      "error_message": "OCR confidence below threshold: 0.45 < 0.70",
      "ocr_confidence": 0.45,
      "threshold": 0.70,
      "attempts": 2,
      "processing_time_ms": 890
    },
    "retry_info": {
      "retry_count": 1,
      "max_retries": 3,
      "next_retry_at": "2024-01-15T10:31:45.456Z"
    }
  },

  "mdc": {
    "client_ip": "192.168.1.100",
    "request_method": "POST",
    "request_uri": "/api/v1/analyze",
    "response_status": 500
  },

  "enrichment": {
    "business_context": "Analisi documento provvedimento ambientale",
    "regulatory_reference": "D.Lgs. 152/2006"
  },

  "processing": {
    "pipeline_version": "2.1.0",
    "processing_node": "logstash-01",
    "parsing_errors": [],
    "enrichment_errors": [],
    "warnings": ["Low OCR confidence detected"]
  },

  "tags": ["application", "error", "ocr", "retry"],
  "labels": {
    "severity": "error",
    "category": "processing",
    "compliance": "gdpr-compliant"
  }
}
```

## 3. Security Event Entry

**File**: `security-event-entry.json`
```json
{
  "id": "sec-123456789-abcdef-003",
  "timestamp": "2024-01-15T10:32:30.000Z",
  "event_type": "SECURITY_VIOLATION",
  "severity": "HIGH",

  "source": {
    "service": "ms03-orchestrator",
    "instance": "ms03-orchestrator-4n2m8",
    "component": "authorization"
  },

  "actor": {
    "user_id": "user-pa-roma-789",
    "session_id": "session-pa-roma-20240115-001",
    "ip_address": "192.168.1.100",
    "user_agent": "ZenIA-PA-Portal/2.1.0",
    "location": {
      "country": "Italy",
      "city": "Rome"
    }
  },

  "resource": {
    "type": "api_endpoint",
    "identifier": "/api/v1/workflows/admin/bulk-action",
    "method": "POST",
    "parameters": {
      "action": "delete",
      "workflow_ids": ["wf-123", "wf-456", "wf-789"]
    }
  },

  "violation": {
    "type": "INSUFFICIENT_PERMISSIONS",
    "description": "User attempted to perform administrative action without required role",
    "required_roles": ["ADMIN", "WORKFLOW_ADMIN"],
    "actual_roles": ["USER"],
    "policy_id": "workflow-admin-policy-v2"
  },

  "context": {
    "correlation_id": "corr-123-abc-456-def-789-ghi",
    "request_id": "req-456-def-789-ghi-jkl",
    "tenant_id": "tenant-pa-roma",
    "session_start": "2024-01-15T09:30:00Z"
  },

  "result": {
    "status": "BLOCKED",
    "details": {
      "access_granted": false,
      "action_prevented": true,
      "response_status": 403
    }
  },

  "enrichment": {
    "risk_score": 8.5,
    "similar_events_count": 2,
    "user_risk_profile": "low",
    "ip_reputation": "trusted",
    "threat_intelligence": {
      "known_attack_patterns": ["privilege_escalation"],
      "attack_vector": "api_abuse"
    }
  },

  "mitigation": {
    "actions_taken": ["access_blocked", "alert_generated", "session_logged"],
    "recommended_actions": ["review_user_permissions", "monitor_user_activity", "consider_role_change"],
    "escalation_required": false
  },

  "processing": {
    "pipeline_version": "2.1.0",
    "processing_time_ms": 45,
    "alert_generated": true,
    "alert_id": "alert-sec-123456"
  }
}
```

## 4. Audit Log Entry

**File**: `audit-log-entry.json`
```json
{
  "id": "audit-123456789-abcdef-004",
  "timestamp": "2024-01-15T10:33:15.000Z",
  "event_type": "DATA_ACCESS",

  "actor": {
    "type": "user",
    "identifier": "user-pa-roma-789",
    "name": "Mario Rossi",
    "roles": ["USER"],
    "department": "Ambiente"
  },

  "action": {
    "name": "DOCUMENT_VIEW",
    "category": "READ",
    "description": "User viewed document details and content"
  },

  "resource": {
    "type": "document",
    "identifier": "DOC-2024-001234-ABC",
    "attributes": {
      "type": "provvedimento",
      "classification": "autorizzazione_ambientale",
      "size_bytes": 2048576,
      "created_date": "2024-01-10",
      "sensitivity_level": "personal_data"
    }
  },

  "context": {
    "tenant_id": "tenant-pa-roma",
    "session_id": "session-pa-roma-20240115-001",
    "correlation_id": "corr-123-abc-456-def-789-ghi",
    "ip_address": "192.168.1.100",
    "user_agent": "ZenIA-PA-Portal/2.1.0",
    "location": "Rome, Italy"
  },

  "result": {
    "status": "SUCCESS",
    "details": {
      "access_granted": true,
      "data_returned": true,
      "fields_accessed": ["content", "metadata", "classification", "attachments"],
      "access_duration_seconds": 45,
      "bytes_transferred": 2048576
    }
  },

  "compliance": {
    "gdpr_compliant": true,
    "retention_required": true,
    "retention_period_years": 7,
    "data_sensitivity": "personal",
    "legal_basis": "public_task",
    "regulatory_reference": "GDPR Art. 6(1)(e)"
  },

  "enrichment": {
    "business_context": "Consultazione provvedimento ambientale per verifica compliance",
    "regulatory_reference": "D.Lgs. 152/2006",
    "risk_assessment": "low",
    "anomaly_score": 0.1
  },

  "processing": {
    "pipeline_version": "2.1.0",
    "processing_time_ms": 25,
    "validation_errors": []
  }
}
```

## 5. Metrics Log Entry

**File**: `metrics-log-entry.json`
```json
{
  "id": "metrics-123456789-abcdef-005",
  "@timestamp": "2024-01-15T10:34:00.000Z",
  "service": "ms01-classifier",
  "instance": "ms01-classifier-7x9k2",
  "metric_type": "performance",
  "metric_name": "document_processing_time",
  "value": 1250.5,
  "unit": "milliseconds",

  "tags": {
    "tenant_id": "tenant-pa-roma",
    "document_type": "provvedimento",
    "processing_stage": "classification",
    "model_version": "v2.1"
  },

  "dimensions": {
    "environment": "production",
    "region": "eu-west-1",
    "instance_type": "c5.large"
  },

  "metadata": {
    "collection_interval": "1m",
    "aggregation_type": "histogram",
    "percentiles": {
      "p50": 1150,
      "p95": 2100,
      "p99": 3500
    },
    "sample_count": 45,
    "min_value": 850,
    "max_value": 4200
  },

  "context": {
    "correlation_id": "corr-123-abc-456-def-789-ghi",
    "workflow_id": "wf-20240115-001",
    "batch_size": 1
  },

  "system_metrics": {
    "cpu_usage_percent": 45.2,
    "memory_usage_mb": 512.8,
    "memory_total_mb": 2048,
    "disk_usage_percent": 23.5,
    "network_in_bytes_per_sec": 15432,
    "network_out_bytes_per_sec": 28941,
    "active_threads": 12,
    "heap_used_mb": 756,
    "heap_max_mb": 1024
  }
}
```

## 6. Bulk Ingestion Payload

**File**: `bulk-ingestion-payload.json`
```json
{
  "entries": [
    {
      "timestamp": "2024-01-15T10:30:45.123Z",
      "level": "INFO",
      "service": "ms01-classifier",
      "message": "Document classification started",
      "correlation_id": "corr-123-abc-456-def-789-ghi",
      "context": {
        "document_id": "DOC-2024-001234-ABC",
        "tenant_id": "tenant-pa-roma"
      }
    },
    {
      "timestamp": "2024-01-15T10:30:47.456Z",
      "level": "INFO",
      "service": "ms01-classifier",
      "message": "OCR processing completed",
      "correlation_id": "corr-123-abc-456-def-789-ghi",
      "context": {
        "document_id": "DOC-2024-001234-ABC",
        "ocr_confidence": 0.85,
        "processing_time_ms": 2300
      }
    },
    {
      "timestamp": "2024-01-15T10:30:49.789Z",
      "level": "INFO",
      "service": "ms01-classifier",
      "message": "Document classification completed",
      "correlation_id": "corr-123-abc-456-def-789-ghi",
      "context": {
        "document_id": "DOC-2024-001234-ABC",
        "classification": "provvedimento",
        "confidence": 0.87,
        "processing_time_ms": 1250
      }
    }
  ]
}
```

## 7. Logstash Configuration Example

**File**: `logstash-config-example.conf`
```ruby
# Logstash pipeline configuration example
input {
  kafka {
    bootstrap_servers => "kafka-cluster:9092"
    topics => ["zenia-logs", "zenia-events"]
    group_id => "logstash-main"
    consumer_threads => 3
    auto_offset_reset => "latest"
    decorate_events => true
    codec => json
  }

  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/ssl/certs/logstash.crt"
    ssl_key => "/etc/ssl/private/logstash.key"
  }
}

filter {
  # Parse JSON if not already parsed
  json {
    source => "message"
    target => "parsed"
  }

  # Normalize timestamp
  date {
    match => ["timestamp", "ISO8601"]
    target => "@timestamp"
    timezone => "UTC"
  }

  # Add processing timestamp
  mutate {
    add_field => {
      "processing_timestamp" => "%{+YYYY-MM-dd HH:mm:ss.SSS}"
      "pipeline_version" => "2.1.0"
    }
  }

  # Geo enrichment
  geoip {
    source => "[mdc][client_ip]"
    target => "geo"
    database => "/etc/logstash/geoip/GeoLite2-City.mmdb"
  }

  # Tenant enrichment
  translate {
    field => "[context][tenant_id]"
    destination => "tenant_info"
    dictionary => {
      "tenant-pa-roma" => '{"name":"Comune di Roma","type":"PA","region":"Lazio"}'
      "tenant-pa-milano" => '{"name":"Comune di Milano","type":"PA","region":"Lombardia"}'
    }
    exact => true
    override => true
  }

  # Error classification
  if [level] == "ERROR" or [level] == "FATAL" {
    mutate {
      add_tag => ["error_event"]
      add_field => { "error_category" => "application_error" }
    }
  }

  # Clean up
  mutate {
    remove_field => ["message"]
  }
}

output {
  # Main Elasticsearch output
  elasticsearch {
    hosts => ["es-hot-01:9200", "es-hot-02:9200", "es-hot-03:9200"]
    index => "zenia-logs-%{+YYYY.MM.dd}"
    document_type => "_doc"
    template => "/etc/logstash/templates/zenia-logs.json"
    template_name => "zenia-logs"
    template_overwrite => true
  }

  # Error events to separate index with higher replication
  if "error_event" in [tags] {
    elasticsearch {
      hosts => ["es-hot-01:9200"]
      index => "zenia-errors-%{+YYYY.MM.dd}"
      document_type => "_doc"
    }
  }

  # Security events
  if [event_type] == "SECURITY_VIOLATION" {
    elasticsearch {
      hosts => ["es-hot-01:9200"]
      index => "zenia-security-%{+YYYY.MM.dd}"
      document_type => "_doc"
    }
  }

  # Audit logs
  if [event_type] == "AUDIT" or [log_type] == "audit" {
    elasticsearch {
      hosts => ["es-hot-01:9200"]
      index => "zenia-audit-%{+YYYY.MM.dd}"
      document_type => "_doc"
    }
  }
}
```

## 8. Kibana Dashboard Export

**File**: `kibana-dashboard-export.ndjson`

Dashboard Object:
```json
{
  "type": "dashboard",
  "id": "zenia-logging-overview",
  "attributes": {
    "title": "ZenIA Logging Overview",
    "description": "Centralized logging dashboard for ZenIA platform",
    "panelsJSON": "[...]",
    "optionsJSON": "{\"useMargins\":true,\"syncColors\":true,\"syncCursor\":true,\"syncTooltips\":true}",
    "uiStateJSON": "{}",
    "version": 1,
    "kibanaSavedObjectMeta": {
      "searchSourceJSON": "{\"query\":{\"query\":\"\",\"language\":\"kuery\"},\"filter\":[]}"
    }
  }
}
```

Visualization Object:
```json
{
  "type": "visualization",
  "id": "error-rate-over-time",
  "attributes": {
    "title": "Error Rate Over Time",
    "description": "Time series chart showing error rates across services",
    "visState": "{\"title\":\"Error Rate Over Time\",\"type\":\"line\",\"params\":{\"type\":\"line\"}}"
  }
}
```

Questi esempi forniscono template completi per l'integrazione con MS10-LOGGER, coprendo tutti i principali tipi di log e configurazioni del sistema di logging centralizzato.
