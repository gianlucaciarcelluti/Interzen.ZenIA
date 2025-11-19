-- =========================================
-- NiFi Audit Trail - Test Queries
-- =========================================
-- Questo file contiene query di test per verificare
-- il corretto funzionamento del sistema di audit
-- =========================================

\connect nifi_audit

-- Test 1: Inserimento record di test
INSERT INTO workflow_executions (
    execution_id,
    workflow_name,
    step_name,
    processor_id,
    status,
    input_data,
    output_data,
    attributes,
    started_at
) VALUES (
    gen_random_uuid(),
    'SP01_EML_Parser',
    'HTTP_Endpoint',
    'test-processor-id-001',
    'SUCCESS',
    '{"test": "input data", "source": "test"}'::jsonb,
    '{"test": "output data", "processed": true}'::jsonb,
    '{"filename": "test.eml", "content-type": "message/rfc822"}'::jsonb,
    NOW()
);

-- Test 2: Verifica inserimento
SELECT 
    execution_id,
    workflow_name,
    step_name,
    status,
    started_at,
    input_data->>'test' as test_input,
    output_data->>'processed' as processed
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 1;

-- Test 3: Inserimento richiesta HTTP
INSERT INTO http_requests (
    execution_id,
    method,
    url,
    request_body,
    response_code,
    response_body,
    response_time_ms
) 
SELECT 
    execution_id,
    'POST',
    'http://localhost:9091/sp01',
    '{"test": "request"}'::jsonb,
    200,
    '{"status": "ok"}'::jsonb,
    125
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 1;

-- Test 4: Verifica join tra tabelle
SELECT 
    we.workflow_name,
    we.step_name,
    hr.method,
    hr.url,
    hr.response_code,
    hr.response_time_ms
FROM workflow_executions we
JOIN http_requests hr ON we.execution_id = hr.execution_id
ORDER BY we.started_at DESC
LIMIT 5;

-- Test 5: Test funzione get_workflow_health
SELECT * FROM get_workflow_health('SP01_EML_Parser', 24);

-- Test 6: Inserimento errore
INSERT INTO error_log (
    execution_id,
    workflow_name,
    processor_name,
    error_type,
    error_message,
    severity
) 
SELECT 
    execution_id,
    'SP01_EML_Parser',
    'HTTP_Endpoint',
    'VALIDATION',
    'Test error message',
    'WARNING'
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 1;

-- Test 7: Query errori
SELECT 
    error_type,
    severity,
    error_message,
    created_at
FROM error_log
ORDER BY created_at DESC
LIMIT 5;

-- Test 8: Performance metrics
INSERT INTO performance_metrics (
    execution_id,
    workflow_name,
    step_name,
    processing_time_ms,
    queue_time_ms,
    bytes_in,
    bytes_out,
    records_processed
)
SELECT 
    execution_id,
    'SP01_EML_Parser',
    'HTTP_Endpoint',
    125,
    10,
    1024,
    2048,
    1
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 1;

-- Test 9: Verifica performance metrics
SELECT 
    workflow_name,
    step_name,
    processing_time_ms,
    bytes_in,
    bytes_out,
    measured_at
FROM performance_metrics
ORDER BY measured_at DESC
LIMIT 5;

-- Test 10: Data quality check
INSERT INTO data_quality_checks (
    execution_id,
    workflow_name,
    check_name,
    check_type,
    check_result,
    validation_rules
)
SELECT 
    execution_id,
    'SP01_EML_Parser',
    'Email Format Validation',
    'FORMAT',
    'PASS',
    '{"required_fields": ["from", "to", "subject"]}'::jsonb
FROM workflow_executions
ORDER BY started_at DESC
LIMIT 1;

-- Test 11: Summary statistico
SELECT 
    workflow_name,
    COUNT(*) as total_executions,
    COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END) as successful,
    COUNT(CASE WHEN status = 'FAILED' THEN 1 END) as failed,
    AVG(duration_ms) as avg_duration
FROM workflow_executions
GROUP BY workflow_name;

-- Test 12: Cleanup test data
-- DELETE FROM workflow_executions WHERE processor_id = 'test-processor-id-001';

ECHO '\n✅ Test completati con successo!';
ECHO '\n📊 Statistiche database:';

SELECT 
    'workflow_executions' as table_name,
    COUNT(*) as row_count
FROM workflow_executions
UNION ALL
SELECT 
    'http_requests',
    COUNT(*)
FROM http_requests
UNION ALL
SELECT 
    'error_log',
    COUNT(*)
FROM error_log
UNION ALL
SELECT 
    'performance_metrics',
    COUNT(*)
FROM performance_metrics
UNION ALL
SELECT 
    'data_quality_checks',
    COUNT(*)
FROM data_quality_checks;
