-- =========================================
-- Database Initialization Script - Provvedimenti
-- =========================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================
-- SP01 - Template Engine Tables
-- =========================================

CREATE TABLE IF NOT EXISTS templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tipo_atto VARCHAR(100) NOT NULL,
    content_jinja TEXT NOT NULL,
    variables JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS generated_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL,
    template_id UUID REFERENCES templates(id),
    content TEXT NOT NULL,
    metadata JSONB,
    generation_method VARCHAR(50), -- 'gpt4', 'claude', 'cache'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP02 - Validator Tables
-- =========================================

CREATE TABLE IF NOT EXISTS validation_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name VARCHAR(255) NOT NULL,
    rule_type VARCHAR(50), -- 'semantic', 'structural', 'compliance'
    drools_rule TEXT,
    severity VARCHAR(20), -- 'critical', 'warning', 'info'
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS validation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL,
    document_id UUID REFERENCES generated_documents(id),
    validation_type VARCHAR(50),
    is_valid BOOLEAN,
    errors JSONB,
    warnings JSONB,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP03 - Knowledge Base Tables
-- =========================================

CREATE TABLE IF NOT EXISTS normativa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    tipo VARCHAR(100), -- 'legge', 'decreto', 'regolamento'
    numero VARCHAR(50),
    data_pubblicazione DATE,
    content TEXT,
    embedding VECTOR(1536), -- Requires pgvector extension
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS precedenti (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo_atto VARCHAR(100),
    content TEXT,
    embedding VECTOR(1536),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS context_retrievals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL,
    query TEXT,
    retrieved_documents JSONB,
    synthesis TEXT,
    retrieval_method VARCHAR(50), -- 'faiss', 'neo4j', 'combined'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP04 - Classifier Tables
-- =========================================

CREATE TABLE IF NOT EXISTS classification_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL,
    input_text TEXT,
    tipo_documento VARCHAR(100),
    categoria VARCHAR(100),
    sottocategoria VARCHAR(100),
    confidence_score FLOAT,
    classifier_used VARCHAR(50), -- 'distilbert', 'spacy', 'combined'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS classification_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model_name VARCHAR(255) NOT NULL,
    model_type VARCHAR(50),
    model_path TEXT,
    accuracy_metrics JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP05 - Quality Checker Tables
-- =========================================

CREATE TABLE IF NOT EXISTS quality_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL,
    document_id UUID REFERENCES generated_documents(id),
    grammar_score FLOAT,
    readability_score FLOAT,
    coherence_score FLOAT,
    issues JSONB,
    suggestions JSONB,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP08 - Security & Audit Tables
-- =========================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    token VARCHAR(500) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- Global Workflow Tables
-- =========================================

CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo_richiesta VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    steps_completed JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_steps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflows(id),
    step_name VARCHAR(100) NOT NULL,
    service VARCHAR(50), -- 'SP01', 'SP02', etc.
    status VARCHAR(50) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- Indexes for Performance
-- =========================================

CREATE INDEX IF NOT EXISTS idx_templates_tipo_atto ON templates(tipo_atto);
CREATE INDEX IF NOT EXISTS idx_generated_docs_workflow ON generated_documents(workflow_id);
CREATE INDEX IF NOT EXISTS idx_validation_results_workflow ON validation_results(workflow_id);
CREATE INDEX IF NOT EXISTS idx_classification_workflow ON classification_results(workflow_id);
CREATE INDEX IF NOT EXISTS idx_quality_checks_workflow ON quality_checks(workflow_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created ON audit_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
CREATE INDEX IF NOT EXISTS idx_workflow_steps_workflow ON workflow_steps(workflow_id);

-- =========================================
-- Sample Data
-- =========================================

-- Insert sample template
INSERT INTO templates (name, description, tipo_atto, content_jinja, variables)
VALUES (
    'Template Autorizzazione Scarico Acque',
    'Template base per autorizzazione scarico acque reflue',
    'Autorizzazione',
    'Il Dirigente del Settore Ambiente...',
    '{"richiedente": "string", "indirizzo": "string", "descrizione": "string"}'
)
ON CONFLICT DO NOTHING;

-- Insert sample user
INSERT INTO users (username, email, password_hash, role)
VALUES (
    'admin',
    'admin@provvedimenti.it',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5Tk5uX3dXqDMu', -- password: admin123
    'admin'
)
ON CONFLICT DO NOTHING;

