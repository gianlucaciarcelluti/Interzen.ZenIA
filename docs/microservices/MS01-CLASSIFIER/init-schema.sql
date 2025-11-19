--
-- MS01 - Classifier Database Schema
-- PostgreSQL 14+
-- Schema initialization for zendata_classifier database
--

-- Create schema
CREATE SCHEMA IF NOT EXISTS classifier;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

---
-- TABLE 1: CLASSIFIER_MODELS
-- ML model versions and their performance metrics
---

CREATE TABLE classifier.classifier_models (
  id SERIAL PRIMARY KEY,
  model_name VARCHAR(100) NOT NULL,
  model_version VARCHAR(50) NOT NULL UNIQUE,

  -- Model Properties
  is_active BOOLEAN DEFAULT FALSE,
  model_file_path VARCHAR(500) NOT NULL,
  model_file_hash VARCHAR(64),
  model_size_mb BIGINT,

  -- Training Metadata
  training_date TIMESTAMP NOT NULL,
  training_samples INT,
  training_epochs INT,

  -- Performance Metrics
  accuracy NUMERIC(3,4) NOT NULL,
  precision NUMERIC(3,4),
  recall NUMERIC(3,4),
  f1_score NUMERIC(3,4),
  auc_score NUMERIC(3,4),

  -- Classes/Categories Supported
  supported_types TEXT ARRAY,
  support_count INT,

  -- Deployment
  deployed_at TIMESTAMP,
  deployed_by VARCHAR(100),
  deployment_notes TEXT,

  -- Lifecycle
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deprecated_at TIMESTAMP,

  -- Metadata
  hyperparameters JSONB,
  training_config JSONB,
  changelog TEXT,

  CONSTRAINT unique_active_version UNIQUE (is_active) WHERE is_active = TRUE
);

-- Indexes for classifier_models
CREATE INDEX idx_classifier_active_models ON classifier.classifier_models(is_active DESC, model_version DESC);
CREATE INDEX idx_classifier_version ON classifier.classifier_models(model_version);
CREATE INDEX idx_classifier_deployed_at ON classifier.classifier_models(deployed_at DESC);

---
-- TABLE 2: DOCUMENTS_CLASSIFICATIONS
-- Core classification results and document metadata
---

CREATE TABLE classifier.documents_classifications (
  id BIGSERIAL PRIMARY KEY,
  document_id UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
  filename VARCHAR(255) NOT NULL,
  file_hash VARCHAR(64) UNIQUE NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  file_size BIGINT NOT NULL,

  -- Classification Results
  primary_type VARCHAR(100) NOT NULL,
  primary_confidence NUMERIC(3,2) NOT NULL CHECK (primary_confidence BETWEEN 0 AND 1),
  secondary_types JSONB,
  category VARCHAR(100),
  urgency VARCHAR(20) DEFAULT 'normal',
  requires_manual_review BOOLEAN DEFAULT FALSE,

  -- Metadata
  detected_language VARCHAR(10),
  key_entities JSONB,
  document_date DATE,

  -- Quality Checks
  file_integrity_status VARCHAR(20) DEFAULT 'PENDING',
  format_compliance_status VARCHAR(20) DEFAULT 'PENDING',
  malware_scan_status VARCHAR(20) DEFAULT 'CLEAN',

  -- Routing
  routing_pipeline VARCHAR(100),
  workflow_id VARCHAR(100),
  sla_minutes INT,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  classified_at TIMESTAMP,

  -- Audit
  source_system VARCHAR(100),
  user_id VARCHAR(100),
  tenant_id UUID NOT NULL,

  -- Foreign Keys
  model_version_id INT REFERENCES classifier.classifier_models(id),

  CONSTRAINT fk_classifier_models FOREIGN KEY (model_version_id) REFERENCES classifier.classifier_models(id) ON DELETE SET NULL
);

-- Indexes for documents_classifications
CREATE INDEX idx_documents_tenant_created ON classifier.documents_classifications(tenant_id, created_at DESC);
CREATE INDEX idx_documents_document_id ON classifier.documents_classifications(document_id);
CREATE INDEX idx_documents_primary_type ON classifier.documents_classifications(primary_type);
CREATE INDEX idx_documents_workflow_id ON classifier.documents_classifications(workflow_id);
CREATE INDEX idx_documents_file_hash ON classifier.documents_classifications(file_hash);
CREATE INDEX idx_documents_classified_at ON classifier.documents_classifications(classified_at DESC);

---
-- TABLE 3: CLASSIFICATION_CACHE
-- High-performance cache for frequent classifications (TTL: 24 hours)
---

CREATE TABLE classifier.classification_cache (
  id BIGSERIAL PRIMARY KEY,
  document_hash VARCHAR(64) UNIQUE NOT NULL,
  file_signature VARCHAR(256) NOT NULL,

  -- Cached Classification
  classification_result JSONB NOT NULL,
  confidence_score NUMERIC(3,2),

  -- Cache Metadata
  cache_version INT DEFAULT 1,
  hit_count INT DEFAULT 0,
  last_hit_at TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,

  -- Source Information
  created_from_model_version VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for classification_cache
CREATE INDEX idx_cache_expires_at ON classifier.classification_cache(expires_at);
CREATE INDEX idx_cache_document_hash ON classifier.classification_cache(document_hash);
CREATE INDEX idx_cache_hit_count ON classifier.classification_cache(hit_count DESC);

-- Cleanup trigger for expired cache entries (optional)
-- This removes entries older than 24 hours
-- Run periodically: SELECT * FROM classifier.cleanup_expired_cache();

---
-- TABLE 4: CLASSIFICATION_AUDIT_LOG
-- Detailed audit trail for all classification operations (immutable)
---

CREATE TABLE classifier.classification_audit_log (
  id BIGSERIAL PRIMARY KEY,
  document_id UUID NOT NULL,

  -- Operation Details
  operation_type VARCHAR(50) NOT NULL CHECK (operation_type IN ('CLASSIFY', 'OVERRIDE', 'VERIFY', 'REVIEW')),
  classifier_version VARCHAR(50),

  -- Original vs Result
  original_classification JSONB,
  final_classification JSONB,
  confidence_before NUMERIC(3,2),
  confidence_after NUMERIC(3,2),

  -- User/System Info
  performed_by VARCHAR(100),
  user_role VARCHAR(50),
  reviewer_comment TEXT,

  -- Timestamps
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

  -- Compliance
  tenant_id UUID NOT NULL,
  is_manual_override BOOLEAN DEFAULT FALSE,
  requires_compliance_review BOOLEAN DEFAULT FALSE
);

-- Indexes for classification_audit_log
CREATE INDEX idx_audit_document_id ON classifier.classification_audit_log(document_id);
CREATE INDEX idx_audit_created_at ON classifier.classification_audit_log(created_at DESC);
CREATE INDEX idx_audit_tenant_id ON classifier.classification_audit_log(tenant_id);
CREATE INDEX idx_audit_operation_type ON classifier.classification_audit_log(operation_type);

---
-- TABLE 5: QUALITY_CHECK_RESULTS
-- Detailed results from security, format, and integrity checks
---

CREATE TABLE classifier.quality_check_results (
  id BIGSERIAL PRIMARY KEY,
  document_id UUID NOT NULL,

  -- File Integrity
  file_integrity_check VARCHAR(20) DEFAULT 'PENDING',
  checksum_algorithm VARCHAR(20),
  checksum_value VARCHAR(64),
  integrity_error TEXT,

  -- Format Compliance
  format_compliance_check VARCHAR(20) DEFAULT 'PENDING',
  format_standards JSONB,
  format_warnings TEXT ARRAY,

  -- Malware Scanning
  malware_scan_check VARCHAR(20) DEFAULT 'PENDING',
  malware_engine VARCHAR(50),
  malware_signature VARCHAR(255),
  quarantine_path VARCHAR(500),

  -- Size Validation
  size_check_valid BOOLEAN,
  size_min_bytes BIGINT DEFAULT 1024,
  size_max_bytes BIGINT DEFAULT 104857600,
  size_actual_bytes BIGINT,

  -- Overall Status
  overall_status VARCHAR(20) DEFAULT 'PENDING',
  check_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  check_duration_ms INT,

  -- Foreign Key
  CONSTRAINT fk_quality_documents FOREIGN KEY (document_id) REFERENCES classifier.documents_classifications(document_id) ON DELETE CASCADE
);

-- Indexes for quality_check_results
CREATE INDEX idx_quality_document_id ON classifier.quality_check_results(document_id);
CREATE INDEX idx_quality_check_timestamp ON classifier.quality_check_results(check_timestamp DESC);
CREATE INDEX idx_quality_overall_status ON classifier.quality_check_results(overall_status);

---
-- TABLE 6: CLASSIFICATION_PERFORMANCE_METRICS
-- Real-time performance tracking and SLA monitoring
---

CREATE TABLE classifier.classification_performance_metrics (
  id BIGSERIAL PRIMARY KEY,

  -- Time Bucket (5-minute buckets)
  bucket_time TIMESTAMP NOT NULL,
  bucket_duration_seconds INT DEFAULT 300,

  -- Throughput
  total_classifications INT DEFAULT 0,
  successful_classifications INT DEFAULT 0,
  failed_classifications INT DEFAULT 0,

  -- Latency (milliseconds)
  latency_p50 INT,
  latency_p95 INT,
  latency_p99 INT,
  latency_max INT,

  -- Accuracy (from audit log comparisons)
  model_accuracy NUMERIC(3,4),
  user_correction_rate NUMERIC(3,4),

  -- Cache Performance
  cache_hit_count INT DEFAULT 0,
  cache_miss_count INT DEFAULT 0,
  cache_hit_rate NUMERIC(3,4),

  -- Resource Usage
  cpu_percent NUMERIC(5,2),
  memory_mb INT,

  -- SLA Compliance
  sla_met BOOLEAN DEFAULT TRUE,
  sla_violations INT DEFAULT 0,

  -- Tenant Isolation
  tenant_id UUID
);

-- Indexes for classification_performance_metrics
CREATE INDEX idx_metrics_bucket_time ON classifier.classification_performance_metrics(bucket_time DESC);
CREATE INDEX idx_metrics_tenant_bucket ON classifier.classification_performance_metrics(tenant_id, bucket_time DESC);

---
-- GRANTS
-- Configure permissions for classifier_service user
---

GRANT ALL PRIVILEGES ON SCHEMA classifier TO classifier_service;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA classifier TO classifier_service;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA classifier TO classifier_service;
GRANT USAGE ON SCHEMA classifier TO classifier_service;

-- Grant specific table permissions
GRANT SELECT, INSERT, UPDATE ON classifier.classifier_models TO classifier_service;
GRANT SELECT, INSERT, UPDATE ON classifier.documents_classifications TO classifier_service;
GRANT SELECT, INSERT ON classifier.classification_cache TO classifier_service;
GRANT SELECT, INSERT ON classifier.classification_audit_log TO classifier_service;
GRANT SELECT, INSERT ON classifier.quality_check_results TO classifier_service;
GRANT SELECT, INSERT ON classifier.classification_performance_metrics TO classifier_service;

-- Grant sequence permissions for BIGSERIAL
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA classifier TO classifier_service;

---
-- COMMENTS
-- Table and column documentation
---

COMMENT ON TABLE classifier.classifier_models IS 'ML model versions and their performance metrics';
COMMENT ON TABLE classifier.documents_classifications IS 'Core classification results and document metadata';
COMMENT ON TABLE classifier.classification_cache IS 'High-performance cache for frequent classifications (TTL: 24 hours)';
COMMENT ON TABLE classifier.classification_audit_log IS 'Detailed audit trail for all classification operations (immutable)';
COMMENT ON TABLE classifier.quality_check_results IS 'Detailed results from security, format, and integrity checks';
COMMENT ON TABLE classifier.classification_performance_metrics IS 'Real-time performance tracking and SLA monitoring';

COMMENT ON COLUMN classifier.classifier_models.is_active IS 'Only one model can be active at a time';
COMMENT ON COLUMN classifier.documents_classifications.primary_confidence IS 'Confidence score between 0.0 and 1.0';
COMMENT ON COLUMN classifier.classification_audit_log.operation_type IS 'CLASSIFY, OVERRIDE, VERIFY, or REVIEW';
COMMENT ON COLUMN classifier.classification_cache.expires_at IS 'Cache expires 24 hours after creation';
