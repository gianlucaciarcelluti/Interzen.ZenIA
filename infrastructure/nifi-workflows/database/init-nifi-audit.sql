-- =========================================
-- NiFi Audit Database Schema
-- =========================================
-- Database: nifi_audit
-- Purpose: Track all workflow executions and data flow
-- Created: 2025-11-04
-- =========================================

-- Connect to nifi_audit database
\connect nifi_audit

-- =========================================
-- Main Audit Table - Workflow Executions
-- =========================================

CREATE TABLE IF NOT EXISTS workflow_executions (
    id BIGSERIAL PRIMARY KEY,
    execution_id UUID NOT NULL UNIQUE,  -- Unique identifier for this execution chain
    workflow_name VARCHAR(100) NOT NULL,  -- SP01, SP02, etc.
    step_name VARCHAR(200) NOT NULL,  -- HTTP_Endpoint, Call_Microservice, etc.
    processor_id VARCHAR(100),  -- NiFi processor UUID
    flowfile_id VARCHAR(100),  -- NiFi FlowFile UUID
    
    -- Timing
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'RUNNING',  -- RUNNING, SUCCESS, FAILED, TIMEOUT
    
    -- Data payload
    input_data JSONB,  -- Input FlowFile content/attributes
    output_data JSONB,  -- Output FlowFile content/attributes
    attributes JSONB,  -- NiFi FlowFile attributes
    
    -- Error tracking
    error_message TEXT,
    error_details JSONB,
    retry_count INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_workflow_executions_execution_id ON workflow_executions(execution_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_workflow_name ON workflow_executions(workflow_name);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_started_at ON workflow_executions(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_workflow_status ON workflow_executions(workflow_name, status);

-- =========================================
-- HTTP Request Log Table
-- =========================================

CREATE TABLE IF NOT EXISTS http_requests (
    id BIGSERIAL PRIMARY KEY,
    execution_id UUID NOT NULL,  -- Links to workflow_executions
    
    -- HTTP Details
    method VARCHAR(10) NOT NULL,  -- POST, GET, etc.
    url TEXT NOT NULL,
    headers JSONB,
    query_params JSONB,
    request_body JSONB,
    
    -- Response
    response_code INTEGER,
    response_body JSONB,
    response_headers JSONB,
    response_time_ms INTEGER,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (execution_id) REFERENCES workflow_executions(execution_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_http_requests_execution_id ON http_requests(execution_id);
CREATE INDEX IF NOT EXISTS idx_http_requests_response_code ON http_requests(response_code);
CREATE INDEX IF NOT EXISTS idx_http_requests_created_at ON http_requests(created_at DESC);

-- =========================================
-- Error Log Table
-- =========================================

CREATE TABLE IF NOT EXISTS error_log (
    id BIGSERIAL PRIMARY KEY,
    execution_id UUID,  -- Can be NULL for system errors
    workflow_name VARCHAR(100),
    processor_name VARCHAR(200),
    
    -- Error details
    error_type VARCHAR(100),  -- VALIDATION, NETWORK, TIMEOUT, SYSTEM, etc.
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    error_context JSONB,
    
    -- Severity
    severity VARCHAR(20) DEFAULT 'ERROR',  -- DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_error_log_execution_id ON error_log(execution_id);
CREATE INDEX IF NOT EXISTS idx_error_log_severity ON error_log(severity);
CREATE INDEX IF NOT EXISTS idx_error_log_created_at ON error_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_error_log_workflow ON error_log(workflow_name);

-- =========================================
-- Performance Metrics Table
-- =========================================

CREATE TABLE IF NOT EXISTS performance_metrics (
    id BIGSERIAL PRIMARY KEY,
    execution_id UUID NOT NULL,
    workflow_name VARCHAR(100) NOT NULL,
    step_name VARCHAR(200) NOT NULL,
    
    -- Metrics
    processing_time_ms INTEGER,
    queue_time_ms INTEGER,
    bytes_in BIGINT,
    bytes_out BIGINT,
    records_processed INTEGER,
    
    -- Resource usage
    cpu_usage_percent DECIMAL(5,2),
    memory_usage_mb INTEGER,
    
    -- Metadata
    measured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (execution_id) REFERENCES workflow_executions(execution_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_performance_metrics_execution_id ON performance_metrics(execution_id);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_workflow ON performance_metrics(workflow_name);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_measured_at ON performance_metrics(measured_at DESC);

-- =========================================
-- Data Quality Checks Table
-- =========================================

CREATE TABLE IF NOT EXISTS data_quality_checks (
    id BIGSERIAL PRIMARY KEY,
    execution_id UUID NOT NULL,
    workflow_name VARCHAR(100) NOT NULL,
    
    -- Check details
    check_name VARCHAR(200) NOT NULL,
    check_type VARCHAR(50) NOT NULL,  -- SCHEMA, FORMAT, COMPLETENESS, CONSISTENCY, etc.
    check_result VARCHAR(20) NOT NULL,  -- PASS, FAIL, WARNING
    
    -- Results
    expected_value TEXT,
    actual_value TEXT,
    validation_rules JSONB,
    violations JSONB,
    
    -- Metadata
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (execution_id) REFERENCES workflow_executions(execution_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_data_quality_checks_execution_id ON data_quality_checks(execution_id);
CREATE INDEX IF NOT EXISTS idx_data_quality_checks_result ON data_quality_checks(check_result);
CREATE INDEX IF NOT EXISTS idx_data_quality_checks_workflow ON data_quality_checks(workflow_name);

-- =========================================
-- Workflow Statistics View (Materialized for performance)
-- =========================================

CREATE MATERIALIZED VIEW IF NOT EXISTS workflow_statistics AS
SELECT 
    workflow_name,
    DATE_TRUNC('hour', started_at) as hour,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END) as successful_executions,
    COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failed_executions,
    AVG(duration_ms) as avg_duration_ms,
    MIN(duration_ms) as min_duration_ms,
    MAX(duration_ms) as max_duration_ms,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duration_ms) as median_duration_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_ms) as p95_duration_ms
FROM workflow_executions
WHERE completed_at IS NOT NULL
GROUP BY workflow_name, DATE_TRUNC('hour', started_at);

CREATE UNIQUE INDEX IF NOT EXISTS idx_workflow_statistics_workflow_hour 
    ON workflow_statistics(workflow_name, hour);

-- =========================================
-- Trigger for automatic updated_at timestamp
-- =========================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_workflow_executions_updated_at 
    BEFORE UPDATE ON workflow_executions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =========================================
-- Helper Functions
-- =========================================

-- Function to get execution summary
CREATE OR REPLACE FUNCTION get_execution_summary(exec_id UUID)
RETURNS TABLE (
    workflow_name VARCHAR,
    total_steps INTEGER,
    completed_steps INTEGER,
    failed_steps INTEGER,
    total_duration_ms INTEGER,
    status VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        we.workflow_name,
        COUNT(*)::INTEGER as total_steps,
        COUNT(CASE WHEN we.status = 'SUCCESS' THEN 1 END)::INTEGER as completed_steps,
        COUNT(CASE WHEN we.status = 'FAILED' THEN 1 END)::INTEGER as failed_steps,
        SUM(we.duration_ms)::INTEGER as total_duration_ms,
        CASE 
            WHEN COUNT(CASE WHEN we.status = 'FAILED' THEN 1 END) > 0 THEN 'FAILED'
            WHEN COUNT(CASE WHEN we.status = 'RUNNING' THEN 1 END) > 0 THEN 'RUNNING'
            ELSE 'SUCCESS'
        END as status
    FROM workflow_executions we
    WHERE we.execution_id = exec_id
    GROUP BY we.workflow_name;
END;
$$ LANGUAGE plpgsql;

-- Function to get workflow health status
CREATE OR REPLACE FUNCTION get_workflow_health(workflow VARCHAR, hours INTEGER DEFAULT 24)
RETURNS TABLE (
    workflow_name VARCHAR,
    time_period VARCHAR,
    total_executions BIGINT,
    success_rate DECIMAL,
    avg_duration_ms DECIMAL,
    error_count BIGINT,
    health_status VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        workflow as workflow_name,
        hours || ' hours' as time_period,
        COUNT(*) as total_executions,
        ROUND(COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0) * 100, 2) as success_rate,
        ROUND(AVG(duration_ms), 2) as avg_duration_ms,
        COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as error_count,
        CASE 
            WHEN COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0) >= 0.95 THEN 'HEALTHY'
            WHEN COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0) >= 0.80 THEN 'DEGRADED'
            ELSE 'UNHEALTHY'
        END as health_status
    FROM workflow_executions
    WHERE workflow_name = workflow
        AND started_at >= NOW() - (hours || ' hours')::INTERVAL;
END;
$$ LANGUAGE plpgsql;

-- =========================================
-- Sample Queries (for reference)
-- =========================================

-- Get recent executions
-- SELECT * FROM workflow_executions ORDER BY started_at DESC LIMIT 100;

-- Get failed executions in last 24 hours
-- SELECT * FROM workflow_executions 
-- WHERE status = 'FAILED' 
--   AND started_at >= NOW() - INTERVAL '24 hours'
-- ORDER BY started_at DESC;

-- Get execution chain for a specific execution_id
-- SELECT * FROM workflow_executions 
-- WHERE execution_id = 'your-uuid-here'
-- ORDER BY started_at;

-- Get workflow performance summary
-- SELECT workflow_name, 
--        COUNT(*) as executions,
--        AVG(duration_ms) as avg_duration,
--        COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failures
-- FROM workflow_executions
-- WHERE started_at >= NOW() - INTERVAL '7 days'
-- GROUP BY workflow_name;

-- Refresh statistics (run periodically)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY workflow_statistics;

-- =========================================
-- Create NiFi User and Grant Privileges
-- =========================================

-- Create nifi user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = 'nifi') THEN
        CREATE USER nifi WITH PASSWORD 'nifi_password';
    END IF;
END
$$;

-- Grant database privileges
GRANT ALL PRIVILEGES ON DATABASE nifi_audit TO nifi;

-- Grant schema privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO nifi;

-- Grant table privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nifi;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nifi;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO nifi;

-- Grant future objects privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO nifi;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO nifi;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO nifi;
