# API Reference - MS06-AGGREGATOR

## Panoramica API

L'API REST di MS06-AGGREGATOR fornisce endpoint per l'aggregazione distribuita di dati, elaborazione batch e analisi real-time utilizzando Apache Spark.

**Base URL**: `http://ms06-aggregator:8006/api/v1`

**Autenticazione**: Bearer Token (JWT)

## Endpoint Aggregazione

### POST /aggregate

Aggregazione sincrona di dati.

**Parametri Header**:
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Body JSON**:
```json
{
  "aggregation_id": "agg-001",
  "sources": [
    {
      "type": "database",
      "connection": {
        "url": "postgresql://user:pass@host:5432/db",
        "table": "transactions"
      },
      "query": "SELECT * FROM transactions WHERE date >= '2024-01-01'"
    }
  ],
  "transformations": [
    {
      "type": "filter",
      "config": {
        "condition": "amount > 0"
      }
    },
    {
      "type": "aggregate",
      "config": {
        "group_by": ["date", "category"],
        "aggregations": [
          {"column": "amount", "function": "SUM", "alias": "total_amount"},
          {"column": "transaction_id", "function": "COUNT", "alias": "transaction_count"}
        ]
      }
    }
  ],
  "output": {
    "format": "json",
    "destination": {
      "type": "memory"
    }
  },
  "options": {
    "parallelism": 4,
    "cache_enabled": true
  }
}
```

**Risposta Successo (200)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "execution_time": 45.2,
  "result": {
    "aggregation_id": "agg-001",
    "summary": {
      "total_records_processed": 150000,
      "total_records_output": 365,
      "data_quality_score": 0.98,
      "processing_stages": [
        {"stage": "ingestion", "duration": 5.2, "records": 150000},
        {"stage": "transformation", "duration": 15.8, "records": 148500},
        {"stage": "aggregation", "duration": 12.1, "records": 365},
        {"stage": "validation", "duration": 3.4, "records": 365},
        {"stage": "output", "duration": 8.7, "records": 365}
      ]
    },
    "data": [
      {
        "date": "2024-01-01",
        "category": "urbanistica",
        "total_amount": 125000.50,
        "transaction_count": 25
      },
      {
        "date": "2024-01-01",
        "category": "edilizia",
        "total_amount": 89000.75,
        "transaction_count": 18
      }
    ],
    "metadata": {
      "schema": {
        "fields": [
          {"name": "date", "type": "date"},
          {"name": "category", "type": "string"},
          {"name": "total_amount", "type": "decimal"},
          {"name": "transaction_count", "type": "integer"}
        ]
      },
      "lineage": [
        {"source": "transactions_db", "transformation": "filter_valid", "records": 150000},
        {"transformation": "aggregate_by_date_category", "records": 365}
      ],
      "quality_report": {
        "validation_rules_passed": 5,
        "validation_rules_failed": 0,
        "data_quality_issues": []
      }
    }
  }
}
```

### POST /aggregate/async

Aggregazione asincrona di dati.

**Parametri**: Identici a `/aggregate`

**Risposta Successo (202)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "QUEUED",
  "estimated_completion": "2025-11-18T10:31:00Z",
  "queue_position": 2,
  "monitoring_url": "http://ms06-aggregator:8006/api/v1/status/550e8400-e29b-41d4-a716-446655440002"
}
```

### GET /status/{job_id}

Verifica stato aggregazione asincrona.

**Risposta (200)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "PROCESSING",
  "progress": {
    "percentage": 65,
    "current_stage": "Data aggregation",
    "stage_progress": {
      "ingestion": "completed",
      "transformation": "completed",
      "aggregation": "in_progress",
      "validation": "pending",
      "output": "pending"
    },
    "estimated_completion": "2025-11-18T10:30:45Z"
  },
  "result": null,
  "created_at": "2025-11-18T10:29:00Z",
  "updated_at": "2025-11-18T10:30:15Z"
}
```

### POST /aggregate/batch

Aggregazione batch di dataset multipli.

**Body JSON**:
```json
{
  "batch_id": "batch-001",
  "jobs": [
    {
      "aggregation_id": "agg-001",
      "sources": [{"type": "file", "path": "/data/transactions_2024.csv"}],
      "transformations": [{"type": "aggregate", "config": {"group_by": ["month"], "aggregations": [{"column": "amount", "function": "SUM"}]}}],
      "output": {"format": "parquet", "path": "/output/agg_001"}
    },
    {
      "aggregation_id": "agg-002",
      "sources": [{"type": "database", "table": "documents"}],
      "transformations": [{"type": "aggregate", "config": {"group_by": ["type"], "aggregations": [{"column": "size", "function": "AVG"}]}}],
      "output": {"format": "json", "path": "/output/agg_002"}
    }
  ],
  "options": {
    "parallel_jobs": 2,
    "priority": "NORMAL"
  },
  "callback_url": "http://ms03-orchestrator:8003/api/v1/callback/batch-aggregation"
}
```

**Risposta (202)**:
```json
{
  "batch_id": "batch-550e8400-e29b-41d4-a716-446655440003",
  "status": "QUEUED",
  "total_jobs": 2,
  "estimated_completion": "2025-11-18T10:32:00Z",
  "progress_url": "http://ms06-aggregator:8006/api/v1/batch/batch-550e8400-e29b-41d4-a716-446655440003/status"
}
```

### GET /batch/{batch_id}/status

Stato elaborazione batch.

**Risposta (200)**:
```json
{
  "batch_id": "batch-550e8400-e29b-41d4-a716-446655440003",
  "status": "PROCESSING",
  "progress": {
    "completed_jobs": 1,
    "total_jobs": 2,
    "percentage": 50,
    "current_job": "agg-002",
    "failed_jobs": 0
  },
  "job_results": [
    {
      "job_id": "job-001",
      "aggregation_id": "agg-001",
      "status": "COMPLETED",
      "records_processed": 150000,
      "execution_time": 32.5
    }
  ],
  "created_at": "2025-11-18T10:29:00Z",
  "updated_at": "2025-11-18T10:30:30Z"
}
```

## Endpoint Streaming

### POST /stream/start

Avvio aggregazione streaming.

**Body JSON**:
```json
{
  "stream_id": "stream-001",
  "source": {
    "type": "kafka",
    "topic": "transactions",
    "brokers": ["kafka-1:9092", "kafka-2:9092"],
    "group_id": "aggregator-group"
  },
  "window": {
    "type": "tumbling",
    "duration": "1 hour"
  },
  "aggregations": [
    {
      "name": "hourly_totals",
      "group_by": ["category"],
      "functions": [
        {"column": "amount", "function": "SUM"},
        {"column": "count", "function": "COUNT"}
      ]
    }
  ],
  "output": {
    "type": "kafka",
    "topic": "aggregated_transactions",
    "format": "json"
  }
}
```

**Risposta (200)**:
```json
{
  "stream_id": "stream-550e8400-e29b-41d4-a716-446655440004",
  "status": "STARTING",
  "monitoring_url": "http://ms06-aggregator:8006/api/v1/stream/stream-550e8400-e29b-41d4-a716-446655440004/status"
}
```

### POST /stream/{stream_id}/stop

Arresto aggregazione streaming.

**Risposta (200)**:
```json
{
  "stream_id": "stream-550e8400-e29b-41d4-a716-446655440004",
  "status": "STOPPING",
  "final_stats": {
    "total_processed": 1250000,
    "total_windows": 24,
    "avg_processing_time": 0.8,
    "error_count": 0
  }
}
```

### GET /stream/{stream_id}/status

Stato aggregazione streaming.

**Risposta (200)**:
```json
{
  "stream_id": "stream-550e8400-e29b-41d4-a716-446655440004",
  "status": "RUNNING",
  "stats": {
    "uptime": "2h 30m",
    "total_processed": 750000,
    "current_window": "2025-11-18T10:00:00Z",
    "processing_rate": 120.5,
    "lag_seconds": 2.3,
    "error_rate": 0.001
  },
  "active_windows": [
    {
      "window_start": "2025-11-18T09:00:00Z",
      "window_end": "2025-11-18T10:00:00Z",
      "records_processed": 50000,
      "partial_results": {
        "urbanistica": {"sum": 45000.25, "count": 125},
        "edilizia": {"sum": 32000.75, "count": 89}
      }
    }
  ]
}
```

## Endpoint Analisi Dati

### POST /analyze/schema

Analisi schema dati sorgente.

**Body JSON**:
```json
{
  "source": {
    "type": "database",
    "connection": {
      "url": "postgresql://user:pass@host:5432/db",
      "table": "transactions"
    }
  },
  "options": {
    "sample_size": 10000,
    "include_statistics": true
  }
}
```

**Risposta (200)**:
```json
{
  "schema": {
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "nullable": false,
        "statistics": {
          "distinct_count": 150000,
          "min": 1,
          "max": 150000
        }
      },
      {
        "name": "amount",
        "type": "decimal",
        "nullable": false,
        "statistics": {
          "min": 0.01,
          "max": 50000.00,
          "avg": 1250.50,
          "stddev": 875.25
        }
      },
      {
        "name": "date",
        "type": "date",
        "nullable": false,
        "statistics": {
          "min": "2024-01-01",
          "max": "2024-12-31",
          "distinct_count": 365
        }
      }
    ]
  },
  "data_quality": {
    "completeness": 0.98,
    "consistency": 0.95,
    "validity": 0.97
  },
  "recommendations": [
    "Consider partitioning by date for better query performance",
    "Amount field has outliers that may need filtering"
  ]
}
```

### POST /analyze/query

Ottimizzazione query aggregazione.

**Body JSON**:
```json
{
  "query": "SELECT date, category, SUM(amount) as total FROM transactions GROUP BY date, category",
  "source_stats": {
    "record_count": 1500000,
    "partitioning": ["date"]
  },
  "target_performance": {
    "max_execution_time": 300,
    "max_memory_usage": "2GB"
  }
}
```

**Risposta (200)**:
```json
{
  "original_query": "SELECT date, category, SUM(amount) as total FROM transactions GROUP BY date, category",
  "optimized_query": "SELECT date, category, SUM(amount) as total FROM transactions GROUP BY date, category ORDER BY date, category",
  "execution_plan": {
    "strategy": "hash_aggregate",
    "estimated_cost": 125000,
    "estimated_rows": 7300,
    "estimated_time": 45.2
  },
  "recommendations": [
    {
      "type": "index",
      "description": "Create composite index on (date, category)",
      "impact": "high"
    },
    {
      "type": "partitioning",
      "description": "Use date-based partitioning for faster aggregation",
      "impact": "medium"
    }
  ],
  "performance_prediction": {
    "execution_time_seconds": 42.5,
    "memory_usage_mb": 512,
    "cpu_utilization": 0.65
  }
}
```

### GET /analyze/performance

Metriche performance aggregazioni recenti.

**Risposta (200)**:
```json
{
  "performance_metrics": {
    "avg_execution_time": 45.2,
    "avg_records_per_second": 8500,
    "success_rate": 0.96,
    "resource_utilization": {
      "cpu_avg": 0.65,
      "memory_avg": 0.72,
      "disk_io_avg": 0.45
    }
  },
  "bottlenecks": [
    {
      "component": "data_ingestion",
      "bottleneck_type": "io_bound",
      "severity": "medium",
      "recommendation": "Consider using SSD storage or data caching"
    }
  ],
  "optimization_opportunities": [
    {
      "type": "parallelism",
      "description": "Increase parallelism from 4 to 8 for better CPU utilization",
      "expected_improvement": 0.25
    }
  ],
  "time_range": "last_24_hours"
}
```

## Endpoint Gestione

### GET /jobs

Elenco job aggregazione attivi.

**Parametri Query**:
- `status`: Filtra per stato (QUEUED, PROCESSING, COMPLETED, FAILED)
- `limit`: Numero massimo risultati (default 50)
- `offset`: Offset per paginazione

**Risposta (200)**:
```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "aggregation_id": "agg-001",
      "status": "COMPLETED",
      "created_at": "2025-11-18T10:29:00Z",
      "completed_at": "2025-11-18T10:30:45Z",
      "execution_time": 105.5,
      "records_processed": 150000
    },
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440002",
      "aggregation_id": "agg-002",
      "status": "PROCESSING",
      "created_at": "2025-11-18T10:30:00Z",
      "progress": 0.65,
      "estimated_completion": "2025-11-18T10:31:30Z"
    }
  ],
  "pagination": {
    "total": 25,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

### GET /health

Verifica stato del servizio.

**Risposta (200)**:
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "uptime": "5d 12h 30m",
  "spark": {
    "master": "running",
    "workers": 3,
    "total_cores": 12,
    "total_memory": "24GB"
  },
  "metrics": {
    "active_jobs": 8,
    "queued_jobs": 3,
    "completed_jobs_24h": 145,
    "failed_jobs_24h": 2,
    "avg_processing_time": 42.3
  },
  "timestamp": "2025-11-18T10:30:00Z"
}
```

### GET /metrics

Metriche dettagliate del servizio.

**Risposta (200)**:
```json
{
  "performance": {
    "requests_per_minute": 35.2,
    "average_response_time": 45.3,
    "error_rate": 0.038,
    "throughput_records_per_minute": 125000
  },
  "aggregation": {
    "total_processed_24h": 18000000,
    "success_rate": 0.962,
    "average_job_size": 125000,
    "popular_aggregations": {
      "sum_by_date": 0.35,
      "count_distinct": 0.25,
      "avg_by_category": 0.20
    }
  },
  "spark": {
    "active_tasks": 24,
    "completed_stages": 1450,
    "failed_stages": 12,
    "avg_task_duration": 8.5,
    "cache_hit_rate": 0.78
  },
  "system": {
    "cpu_usage": 0.65,
    "memory_usage": 0.74,
    "disk_usage": 0.42,
    "network_io": 125.5
  },
  "timestamp": "2025-11-18T10:30:00Z"
}
```

## Codici di Stato HTTP

- **200**: Successo
- **202**: Accepted (elaborazione asincrona avviata)
- **400**: Bad Request (parametri invalidi)
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **413**: Payload Too Large
- **422**: Unprocessable Entity (dati non aggregabili)
- **429**: Too Many Requests
- **500**: Internal Server Error
- **503**: Service Unavailable

## Rate Limiting

- **Authenticated requests**: 100/minuto per client
- **Anonymous requests**: 10/minuto per IP
- **Batch requests**: 20/minuto per client
- **Streaming requests**: 50/minuto per client
- **Analysis requests**: 200/minuto per client

## Versioning API

L'API utilizza versioning nell'URL path (`/api/v1/`).
Versioni future manterranno retrocompatibilità per 12 mesi.