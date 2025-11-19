-- =========================================
-- Database Initialization Script
-- PostgreSQL Compatible Version
-- =========================================

-- NOTE: Database creation is handled by docker-compose environment variables
-- This script assumes we are running inside the 'provvedimenti' database

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================================
-- SP00 - Procedural Classifier Tables
-- =========================================

CREATE TABLE IF NOT EXISTS procedimenti_amministrativi (
    id SERIAL PRIMARY KEY,
    codice VARCHAR(50) UNIQUE NOT NULL,
    denominazione VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    sottocategoria VARCHAR(100),
    normativa_base JSONB NOT NULL,
    termini_giorni INTEGER NOT NULL,
    silenzio_assenso BOOLEAN DEFAULT false,
    tipo_provvedimento_default VARCHAR(100) NOT NULL,
    autorita_competente VARCHAR(100) NOT NULL,
    metadata_required JSONB NOT NULL,
    fasi_procedurali JSONB NOT NULL,
    enti_coinvolti JSONB,
    template_id VARCHAR(50),
    keywords TEXT[],
    embedding vector(768),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_procedimenti_categoria ON procedimenti_amministrativi(categoria);
CREATE INDEX idx_procedimenti_keywords ON procedimenti_amministrativi USING GIN(keywords);
CREATE INDEX idx_procedimenti_embedding ON procedimenti_amministrativi USING ivfflat(embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS classificazioni_procedimenti (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(50) NOT NULL,
    istanza_oggetto TEXT NOT NULL,
    procedimento_id INTEGER REFERENCES procedimenti_amministrativi(id),
    confidence FLOAT NOT NULL,
    metadata_extracted JSONB,
    similarity_scores JSONB,
    cached BOOLEAN DEFAULT false,
    processing_time_ms INTEGER,
    classified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    classified_by VARCHAR(100)
);

CREATE INDEX idx_classificazioni_workflow ON classificazioni_procedimenti(workflow_id);
CREATE INDEX idx_classificazioni_procedimento ON classificazioni_procedimenti(procedimento_id);

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

CREATE TABLE IF NOT EXISTS classification_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL,
    document_text TEXT,
    predicted_class VARCHAR(100),
    confidence FLOAT,
    entities JSONB,
    suggested_templates JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP05 - Quality Checker Tables
-- =========================================

CREATE TABLE IF NOT EXISTS quality_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL,
    document_id UUID REFERENCES generated_documents(id),
    grammar_score FLOAT,
    style_score FLOAT,
    readability_score FLOAT,
    overall_score FLOAT,
    details JSONB,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP06 - Workflow Engine Tables
-- =========================================

CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo_richiesta VARCHAR(100) NOT NULL,
    current_state VARCHAR(50) NOT NULL, -- 'init', 'classifying', 'generating', etc.
    input_data JSONB,
    output_data JSONB,
    error_log JSONB,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_transitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflows(id),
    from_state VARCHAR(50),
    to_state VARCHAR(50),
    event VARCHAR(100),
    metadata JSONB,
    transitioned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP07 - Dashboard Tables
-- =========================================

CREATE TABLE IF NOT EXISTS dashboard_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value FLOAT,
    metadata JSONB,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bottleneck_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflows(id),
    phase VARCHAR(50),
    duration_ms INTEGER,
    is_bottleneck BOOLEAN,
    analysis JSONB,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- SP08 - Security & Audit Tables
-- =========================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflows(id),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(255),
    details JSONB,
    merkle_hash VARCHAR(64), -- SHA-256 hash
    previous_hash VARCHAR(64),
    block_index INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gdpr_compliance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES workflows(id),
    data_processed JSONB,
    consent_obtained BOOLEAN,
    retention_period INTEGER, -- days
    anonymization_applied BOOLEAN,
    compliance_report JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- HITL - Human in the Loop Tables
-- =========================================

CREATE TABLE IF NOT EXISTS hitl_interactions (
    id SERIAL PRIMARY KEY,
    workflow_id UUID NOT NULL REFERENCES workflows(id),
    hitl_point VARCHAR(50) NOT NULL,  -- PROCEDURAL_CLASSIFICATION, DOCUMENT_CLASSIFICATION, DRAFT_REVIEW, FINAL_APPROVAL
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- AI Suggestion
    ai_suggestion JSONB NOT NULL,
    ai_confidence DECIMAL(5,4),
    
    -- User Action
    user_action VARCHAR(20) NOT NULL,  -- CONFIRMED, MODIFIED, REJECTED
    user_id UUID NOT NULL REFERENCES users(id),
    user_changes JSONB,
    modification_reason TEXT,
    
    -- Metadata
    time_to_decision INTERVAL,  -- Quanto tempo l'utente ha impiegato
    session_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    
    -- Versioning
    document_version_before VARCHAR(20),
    document_version_after VARCHAR(20),
    
    -- Audit
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_hitl_workflow ON hitl_interactions(workflow_id);
CREATE INDEX idx_hitl_point ON hitl_interactions(hitl_point);
CREATE INDEX idx_hitl_user ON hitl_interactions(user_id);
CREATE INDEX idx_hitl_timestamp ON hitl_interactions(timestamp);

CREATE TABLE IF NOT EXISTS document_versions (
    id SERIAL PRIMARY KEY,
    workflow_id UUID NOT NULL REFERENCES workflows(id),
    version VARCHAR(20) NOT NULL,  -- 1.0-AI, 1.1-HUMAN, 1.2-HUMAN, etc.
    content TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,  -- SHA256 hash
    
    -- Diff tracking
    diff_from_previous JSONB,  -- JSON diff
    changes_summary TEXT,
    
    -- Metadata
    created_by VARCHAR(100) NOT NULL,  -- AI or user_id
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_ai_generated BOOLEAN NOT NULL,
    hitl_interaction_id INTEGER REFERENCES hitl_interactions(id),
    
    -- Statistics
    word_count INTEGER,
    section_count INTEGER,
    ai_content_percentage DECIMAL(5,2),
    human_content_percentage DECIMAL(5,2),
    
    UNIQUE(workflow_id, version)
);

CREATE INDEX idx_versions_workflow ON document_versions(workflow_id);
CREATE INDEX idx_versions_timestamp ON document_versions(created_at);
CREATE INDEX idx_versions_hitl ON document_versions(hitl_interaction_id);

CREATE TABLE IF NOT EXISTS hitl_checkpoints (
    id SERIAL PRIMARY KEY,
    workflow_id UUID NOT NULL REFERENCES workflows(id),
    checkpoint_name VARCHAR(50) NOT NULL,  -- PROCEDURAL_CLASSIFICATION, etc.
    status VARCHAR(20) NOT NULL,  -- PENDING, WAITING_USER, CONFIRMED, REJECTED
    data JSONB,  -- Dati specifici del checkpoint
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    timeout_at TIMESTAMPTZ
);

CREATE INDEX idx_checkpoints_workflow ON hitl_checkpoints(workflow_id);
CREATE INDEX idx_checkpoints_status ON hitl_checkpoints(status);

-- =========================================
-- Indexes for Performance
-- =========================================

-- Templates
CREATE INDEX idx_templates_tipo_atto ON templates(tipo_atto);
CREATE INDEX idx_templates_active ON templates(is_active);

-- Workflows
CREATE INDEX idx_workflows_state ON workflows(current_state);
CREATE INDEX idx_workflows_created ON workflows(created_at);

-- Normativa (requires pgvector extension)
-- CREATE INDEX idx_normativa_embedding ON normativa USING ivfflat (embedding vector_cosine_ops);

-- Audit Logs
CREATE INDEX idx_audit_logs_workflow ON audit_logs(workflow_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- Classification
CREATE INDEX idx_classification_workflow ON classification_history(workflow_id);

-- Quality Checks
CREATE INDEX idx_quality_workflow ON quality_checks(workflow_id);

-- =========================================
-- Functions and Triggers
-- =========================================

-- Auto-update timestamp trigger
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_templates_timestamp
BEFORE UPDATE ON templates
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_workflows_timestamp
BEFORE UPDATE ON workflows
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_normativa_timestamp
BEFORE UPDATE ON normativa
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- =========================================
-- Sample Data
-- =========================================

-- Insert sample template
INSERT INTO templates (name, description, tipo_atto, content_jinja, variables)
VALUES (
    'Template Base Autorizzazione',
    'Template di base per autorizzazioni generiche',
    'Autorizzazione',
    'OGGETTO: {{ oggetto }}\n\nVISTO il regolamento...\n\nDETERMINA\n\nArt. 1: {{ articolo_1 }}',
    '{"oggetto": "string", "articolo_1": "string"}'::jsonb
);

-- Insert sample validation rule
INSERT INTO validation_rules (rule_name, rule_type, drools_rule, severity)
VALUES (
    'Check Oggetto Required',
    'structural',
    'rule "Oggetto Required" when $doc: Document(oggetto == null) then errors.add("Campo oggetto obbligatorio"); end',
    'critical'
);

-- Insert sample user
INSERT INTO users (username, password_hash, role)
VALUES (
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU.1zQ.2V7tO', -- password: admin
    'admin'
);

-- =========================================
-- Extensions (uncomment if needed)
-- =========================================

-- Enable pgvector for embeddings
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable crypto functions
CREATE EXTENSION IF NOT EXISTS pgcrypto;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
