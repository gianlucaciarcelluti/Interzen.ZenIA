# Schema Database - MS06-AGGREGATOR

## Panoramica Database

Il database PostgreSQL di MS06-AGGREGATOR gestisce metadati di aggregazione, risultati aggregati, statistiche di processamento e configurazione dei job.

## Diagramma ER

```mermaid
erDiagram
    AGGREGATION_JOBS ||--o{ JOB_METRICS : "produces"
    AGGREGATION_JOBS ||--o{ JOB_LOGS : "generates"
    AGGREGATION_JOBS ||--o{ AGGREGATION_RESULTS : "produces"
    AGGREGATION_JOBS ||--o{ DATA_SOURCES : "reads_from"
    AGGREGATION_JOBS ||--o{ TRANSFORMATIONS : "applies"
    AGGREGATION_RESULTS ||--o{ RESULT_PARTITIONS : "divided_into"
    CLIENTS ||--o{ AGGREGATION_JOBS : "submitted_by"
    STREAMS ||--o{ STREAM_WINDOWS : "produces"
    STREAMS ||--o{ STREAM_METRICS : "monitored_by"
    SCHEMAS ||--o{ SCHEMA_FIELDS : "contains"
    SCHEMAS ||--o{ AGGREGATION_JOBS : "used_by"

    AGGREGATION_JOBS {
        uuid id PK
        uuid client_id FK
        varchar job_type
        varchar status
        jsonb configuration
        jsonb options
        integer records_processed
        integer records_output
        timestamp created_at
        timestamp started_at
        timestamp completed_at
    }

    DATA_SOURCES {
        uuid id PK
        uuid job_id FK
        varchar source_type
        varchar connection_string
        varchar table_name
        varchar file_path
        jsonb credentials
        varchar format
        timestamp created_at
    }

    TRANSFORMATIONS {
        uuid id PK
        uuid job_id FK
        varchar transformation_type
        jsonb configuration
        integer execution_order
        timestamp created_at
    }

    AGGREGATION_RESULTS {
        uuid id PK
        uuid job_id FK
        varchar result_format
        varchar storage_path
        bigint result_size
        jsonb metadata
        jsonb quality_metrics
        timestamp created_at
    }

    RESULT_PARTITIONS {
        uuid id PK
        uuid result_id FK
        varchar partition_key
        varchar partition_value
        varchar partition_path
        bigint partition_size
        integer record_count
        timestamp created_at
    }

    JOB_METRICS {
        uuid id PK
        uuid job_id FK
        varchar metric_name
        decimal metric_value
        varchar unit
        timestamp recorded_at
    }

    JOB_LOGS {
        uuid id PK
        uuid job_id FK
        varchar level
        varchar component
        text message
        jsonb context
        timestamp logged_at
    }

    CLIENTS {
        uuid id PK
        varchar client_name
        varchar email
        boolean is_active
        jsonb settings
        timestamp created_at
    }

    STREAMS {
        uuid id PK
        varchar stream_name
        varchar source_topic
        varchar sink_topic
        jsonb window_config
        jsonb aggregation_config
        varchar status
        timestamp created_at
        timestamp last_updated
    }

    STREAM_WINDOWS {
        uuid id PK
        uuid stream_id FK
        varchar window_type
        timestamp window_start
        timestamp window_end
        jsonb aggregated_data
        integer record_count
        timestamp created_at
    }

    STREAM_METRICS {
        uuid id PK
        uuid stream_id FK
        varchar metric_name
        decimal metric_value
        timestamp recorded_at
    }

    SCHEMAS {
        uuid id PK
        varchar schema_name
        varchar source_type
        jsonb schema_definition
        timestamp created_at
        timestamp last_updated
    }

    SCHEMA_FIELDS {
        uuid id PK
        uuid schema_id FK
        varchar field_name
        varchar field_type
        boolean nullable
        jsonb field_metadata
        timestamp created_at
    }
```

## Tabelle Principali

### aggregation_jobs

Tabella principale per i job di aggregazione.

```sql
CREATE TABLE aggregation_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    job_type VARCHAR(20) NOT NULL DEFAULT 'BATCH',
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    configuration JSONB NOT NULL DEFAULT '{}',
    options JSONB DEFAULT '{}',
    records_processed BIGINT DEFAULT 0,
    records_output BIGINT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indici
CREATE INDEX idx_jobs_client_id ON aggregation_jobs(client_id);
CREATE INDEX idx_jobs_status ON aggregation_jobs(status);
CREATE INDEX idx_jobs_type ON aggregation_jobs(job_type);
CREATE INDEX idx_jobs_created_at ON aggregation_jobs(created_at);
CREATE INDEX idx_jobs_configuration ON aggregation_jobs USING GIN(configuration);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "client_id": "550e8400-e29b-41d4-a716-446655440001",
  "job_type": "BATCH",
  "status": "COMPLETED",
  "configuration": {
    "sources": [
      {
        "type": "database",
        "table": "transactions",
        "query": "SELECT * FROM transactions WHERE date >= '2024-01-01'"
      }
    ],
    "transformations": [
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
    ]
  },
  "options": {
    "parallelism": 4,
    "cache_enabled": true
  },
  "records_processed": 150000,
  "records_output": 365,
  "created_at": "2025-11-18T10:15:00Z",
  "started_at": "2025-11-18T10:15:05Z",
  "completed_at": "2025-11-18T10:30:00Z"
}
```

### data_sources

Fonti dati configurate per i job.

```sql
CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES aggregation_jobs(id),
    source_type VARCHAR(50) NOT NULL,
    connection_string TEXT,
    table_name VARCHAR(100),
    file_path TEXT,
    credentials JSONB,
    format VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indici
CREATE INDEX idx_sources_job_id ON data_sources(job_id);
CREATE INDEX idx_sources_type ON data_sources(source_type);
CREATE INDEX idx_sources_table ON data_sources(table_name);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "source_type": "database",
  "connection_string": "postgresql://user:pass@host:5432/db",
  "table_name": "transactions",
  "credentials": {
    "username": "aggregator_user",
    "password": "encrypted_password"
  },
  "format": "postgresql",
  "created_at": "2025-11-18T10:15:00Z"
}
```

### transformations

Trasformazioni applicate nei job.

```sql
CREATE TABLE transformations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES aggregation_jobs(id),
    transformation_type VARCHAR(50) NOT NULL,
    configuration JSONB NOT NULL DEFAULT '{}',
    execution_order INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indici
CREATE INDEX idx_transformations_job_id ON transformations(job_id);
CREATE INDEX idx_transformations_type ON transformations(transformation_type);
CREATE INDEX idx_transformations_order ON transformations(job_id, execution_order);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "transformation_type": "aggregate",
  "configuration": {
    "group_by": ["date", "category"],
    "aggregations": [
      {
        "column": "amount",
        "function": "SUM",
        "alias": "total_amount"
      },
      {
        "column": "transaction_id",
        "function": "COUNT",
        "alias": "transaction_count"
      }
    ]
  },
  "execution_order": 1,
  "created_at": "2025-11-18T10:15:00Z"
}
```

### aggregation_results

Risultati delle aggregazioni.

```sql
CREATE TABLE aggregation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID NOT NULL REFERENCES aggregation_jobs(id),
    result_format VARCHAR(20) NOT NULL,
    storage_path TEXT NOT NULL,
    result_size BIGINT,
    metadata JSONB DEFAULT '{}',
    quality_metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indici
CREATE INDEX idx_results_job_id ON aggregation_results(job_id);
CREATE INDEX idx_results_format ON aggregation_results(result_format);
CREATE INDEX idx_results_metadata ON aggregation_results USING GIN(metadata);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "result_format": "parquet",
  "storage_path": "/results/agg_550e8400-e29b-41d4-a716-446655440000/",
  "result_size": 5242880,
  "metadata": {
    "schema": {
      "fields": [
        {"name": "date", "type": "date"},
        {"name": "category", "type": "string"},
        {"name": "total_amount", "type": "decimal"},
        {"name": "transaction_count", "type": "integer"}
      ]
    },
    "partitioning": {
      "type": "date",
      "columns": ["date"]
    }
  },
  "quality_metrics": {
    "completeness": 0.98,
    "accuracy": 0.96,
    "consistency": 0.94
  },
  "created_at": "2025-11-18T10:30:00Z"
}
```

### result_partitions

Partizioni dei risultati aggregati.

```sql
CREATE TABLE result_partitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    result_id UUID NOT NULL REFERENCES aggregation_results(id),
    partition_key VARCHAR(100) NOT NULL,
    partition_value VARCHAR(255) NOT NULL,
    partition_path TEXT NOT NULL,
    partition_size BIGINT,
    record_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indici
CREATE INDEX idx_partitions_result_id ON result_partitions(result_id);
CREATE INDEX idx_partitions_key ON result_partitions(partition_key, partition_value);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "result_id": "550e8400-e29b-41d4-a716-446655440004",
  "partition_key": "date",
  "partition_value": "2024-01-15",
  "partition_path": "/results/agg_550e8400-e29b-41d4-a716-446655440000/date=2024-01-15/",
  "partition_size": 1536000,
  "record_count": 25,
  "created_at": "2025-11-18T10:30:00Z"
}
```

### streams

Configurazioni per aggregazioni streaming.

```sql
CREATE TABLE streams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stream_name VARCHAR(100) NOT NULL UNIQUE,
    source_topic VARCHAR(255) NOT NULL,
    sink_topic VARCHAR(255) NOT NULL,
    window_config JSONB NOT NULL DEFAULT '{}',
    aggregation_config JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'STOPPED',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indici
CREATE INDEX idx_streams_name ON streams(stream_name);
CREATE INDEX idx_streams_status ON streams(status);
CREATE INDEX idx_streams_topics ON streams(source_topic, sink_topic);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440006",
  "stream_name": "transaction_aggregator",
  "source_topic": "raw_transactions",
  "sink_topic": "aggregated_transactions",
  "window_config": {
    "type": "tumbling",
    "duration": "1 hour",
    "slide": "1 hour"
  },
  "aggregation_config": {
    "group_by": ["category"],
    "aggregations": [
      {"column": "amount", "function": "SUM"},
      {"column": "count", "function": "COUNT"}
    ]
  },
  "status": "RUNNING",
  "created_at": "2025-11-18T09:00:00Z",
  "last_updated": "2025-11-18T10:30:00Z"
}
```

### stream_windows

Finestre di aggregazione streaming.

```sql
CREATE TABLE stream_windows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    stream_id UUID NOT NULL REFERENCES streams(id),
    window_type VARCHAR(20) NOT NULL,
    window_start TIMESTAMP WITH TIME ZONE NOT NULL,
    window_end TIMESTAMP WITH TIME ZONE NOT NULL,
    aggregated_data JSONB NOT NULL DEFAULT '{}',
    record_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indici
CREATE INDEX idx_windows_stream_id ON stream_windows(stream_id);
CREATE INDEX idx_windows_time ON stream_windows(window_start, window_end);
CREATE INDEX idx_windows_type ON stream_windows(window_type);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440007",
  "stream_id": "550e8400-e29b-41d4-a716-446655440006",
  "window_type": "tumbling",
  "window_start": "2025-11-18T10:00:00Z",
  "window_end": "2025-11-18T11:00:00Z",
  "aggregated_data": {
    "urbanistica": {"sum": 45000.25, "count": 125},
    "edilizia": {"sum": 32000.75, "count": 89},
    "total": {"sum": 77000.00, "count": 214}
  },
  "record_count": 214,
  "created_at": "2025-11-18T11:00:00Z"
}
```

### schemas

Schemi dati per fonti e risultati.

```sql
CREATE TABLE schemas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    schema_name VARCHAR(100) NOT NULL UNIQUE,
    source_type VARCHAR(50) NOT NULL,
    schema_definition JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indici
CREATE INDEX idx_schemas_name ON schemas(schema_name);
CREATE INDEX idx_schemas_type ON schemas(source_type);
CREATE INDEX idx_schemas_definition ON schemas USING GIN(schema_definition);
```

**Esempio Record**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440008",
  "schema_name": "transaction_schema",
  "source_type": "database",
  "schema_definition": {
    "fields": [
      {
        "name": "id",
        "type": "integer",
        "nullable": false,
        "metadata": {"primary_key": true}
      },
      {
        "name": "amount",
        "type": "decimal",
        "nullable": false,
        "metadata": {"precision": 10, "scale": 2}
      },
      {
        "name": "date",
        "type": "date",
        "nullable": false
      },
      {
        "name": "category",
        "type": "string",
        "nullable": false,
        "metadata": {"max_length": 50}
      }
    ]
  },
  "created_at": "2025-11-01T00:00:00Z",
  "last_updated": "2025-11-18T10:00:00Z"
}
```

## Viste e Funzioni

### Vista: job_summary

```sql
CREATE VIEW job_summary AS
SELECT
    aj.id as job_id,
    aj.job_type,
    aj.status,
    aj.records_processed,
    aj.records_output,
    aj.created_at,
    aj.started_at,
    aj.completed_at,
    EXTRACT(EPOCH FROM (aj.completed_at - aj.started_at)) as execution_time_seconds,
    c.client_name,
    COUNT(ds.id) as source_count,
    COUNT(t.id) as transformation_count
FROM aggregation_jobs aj
LEFT JOIN clients c ON aj.client_id = c.id
LEFT JOIN data_sources ds ON aj.id = ds.job_id
LEFT JOIN transformations t ON aj.id = t.job_id
GROUP BY aj.id, aj.job_type, aj.status, aj.records_processed, aj.records_output,
         aj.created_at, aj.started_at, aj.completed_at, c.client_name;
```

### Vista: stream_performance

```sql
CREATE VIEW stream_performance AS
SELECT
    s.stream_name,
    s.status,
    COUNT(sw.id) as total_windows,
    AVG(sw.record_count) as avg_records_per_window,
    MAX(sw.created_at) as last_window_time,
    AVG(EXTRACT(EPOCH FROM (sw.window_end - sw.window_start))) as avg_window_duration
FROM streams s
LEFT JOIN stream_windows sw ON s.id = sw.stream_id
WHERE sw.created_at >= NOW() - INTERVAL '24 hours'
GROUP BY s.id, s.stream_name, s.status;
```

### Funzione: get_job_lineage

```sql
CREATE OR REPLACE FUNCTION get_job_lineage(
    p_job_id UUID
)
RETURNS TABLE (
    component_type VARCHAR,
    component_id UUID,
    component_name VARCHAR,
    execution_order INTEGER,
    status VARCHAR,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    -- Data sources
    SELECT
        'data_source'::VARCHAR,
        ds.id,
        ds.table_name::VARCHAR,
        0,
        'completed'::VARCHAR,
        ds.created_at
    FROM data_sources ds
    WHERE ds.job_id = p_job_id

    UNION ALL

    -- Transformations
    SELECT
        'transformation'::VARCHAR,
        t.id,
        t.transformation_type::VARCHAR,
        t.execution_order,
        'completed'::VARCHAR,
        t.created_at
    FROM transformations t
    WHERE t.job_id = p_job_id

    UNION ALL

    -- Results
    SELECT
        'result'::VARCHAR,
        ar.id,
        ar.result_format::VARCHAR,
        999,
        'completed'::VARCHAR,
        ar.created_at
    FROM aggregation_results ar
    WHERE ar.job_id = p_job_id

    ORDER BY execution_order, created_at;
END;
$$ LANGUAGE plpgsql;
```

### Funzione: get_stream_stats

```sql
CREATE OR REPLACE FUNCTION get_stream_stats(
    p_stream_id UUID,
    p_hours INTEGER DEFAULT 24
)
RETURNS TABLE (
    total_windows BIGINT,
    total_records BIGINT,
    avg_records_per_window DECIMAL,
    avg_window_duration INTERVAL,
    last_window_time TIMESTAMP,
    throughput_records_per_hour DECIMAL
) AS $$
DECLARE
    time_threshold TIMESTAMP;
BEGIN
    time_threshold := NOW() - (p_hours || ' hours')::INTERVAL;

    RETURN QUERY
    SELECT
        COUNT(*)::BIGINT,
        COALESCE(SUM(record_count), 0)::BIGINT,
        COALESCE(AVG(record_count), 0)::DECIMAL,
        COALESCE(AVG(window_end - window_start), '0 seconds'::INTERVAL),
        MAX(created_at),
        CASE
            WHEN COUNT(*) > 0 THEN
                COALESCE(SUM(record_count), 0)::DECIMAL / GREATEST(EXTRACT(EPOCH FROM (MAX(created_at) - MIN(created_at))) / 3600, 1)
            ELSE 0
        END
    FROM stream_windows
    WHERE stream_id = p_stream_id
    AND created_at >= time_threshold;
END;
$$ LANGUAGE plpgsql;
```

## Strategie di Partizionamento

### Partizionamento Temporale

```sql
-- Partizionamento mensile per aggregation_jobs
CREATE TABLE aggregation_jobs_y2025m11 PARTITION OF aggregation_jobs
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');

-- Partizionamento mensile per stream_windows
CREATE TABLE stream_windows_y2025m11 PARTITION OF stream_windows
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
```

### Partizionamento per Tipo Job

```sql
-- Partizionamento per tipo di job
CREATE TABLE aggregation_jobs_batch PARTITION OF aggregation_jobs
    FOR VALUES IN ('BATCH');

CREATE TABLE aggregation_jobs_stream PARTITION OF aggregation_jobs
    FOR VALUES IN ('STREAM');
```

## Backup e Recovery

### Strategia di Backup

- **Full Backup**: Settimanale (domenica 02:00)
- **Incremental Backup**: Giornaliero (02:00)
- **Log Backup**: Ogni 15 minuti
- **Retention**: 30 giorni per incrementali, 1 anno per full

### Recovery Objectives

- **RTO**: 4 ore per database completo
- **RPO**: 15 minuti perdita dati massima
- **Point-in-time Recovery**: Supportato fino a 24 ore indietro