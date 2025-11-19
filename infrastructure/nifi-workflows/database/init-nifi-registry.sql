-- NiFi Registry Database Schema for PostgreSQL
-- This script creates the necessary tables for NiFi Registry
-- NOTE: This script is executed on the 'nifi_registry' database

\c nifi_registry

-- Create tables for flow persistence
CREATE TABLE IF NOT EXISTS bucket (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(1000),
    created TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS bucket_item (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(1000) NOT NULL,
    description VARCHAR(1000),
    created TIMESTAMP NOT NULL,
    modified TIMESTAMP NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    bucket_id VARCHAR(50) NOT NULL,
    CONSTRAINT fk_bucket_item_bucket FOREIGN KEY (bucket_id) REFERENCES bucket(id) ON DELETE CASCADE,
    CONSTRAINT uc_bucket_item_name UNIQUE (name, bucket_id)
);

CREATE INDEX IF NOT EXISTS idx_bucket_item_bucket_id ON bucket_item(bucket_id);
CREATE INDEX IF NOT EXISTS idx_bucket_item_modified ON bucket_item(modified);

CREATE TABLE IF NOT EXISTS flow (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    CONSTRAINT fk_flow_bucket_item FOREIGN KEY (id) REFERENCES bucket_item(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS flow_snapshot (
    flow_id VARCHAR(50) NOT NULL,
    version INTEGER NOT NULL,
    created TIMESTAMP NOT NULL,
    created_by VARCHAR(1000) NOT NULL,
    comments VARCHAR(1000),
    PRIMARY KEY (flow_id, version),
    CONSTRAINT fk_flow_snapshot_flow FOREIGN KEY (flow_id) REFERENCES flow(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_flow_snapshot_flow_id ON flow_snapshot(flow_id);

-- Extension registry tables
CREATE TABLE IF NOT EXISTS extension_bundle (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    bucket_id VARCHAR(50) NOT NULL,
    bundle_type VARCHAR(50) NOT NULL,
    group_id VARCHAR(1000) NOT NULL,
    artifact_id VARCHAR(1000) NOT NULL,
    CONSTRAINT fk_extension_bundle_bucket FOREIGN KEY (bucket_id) REFERENCES bucket(id) ON DELETE CASCADE,
    CONSTRAINT uc_extension_bundle_group_artifact UNIQUE (bucket_id, group_id, artifact_id)
);

CREATE INDEX IF NOT EXISTS idx_extension_bundle_bucket_id ON extension_bundle(bucket_id);

CREATE TABLE IF NOT EXISTS extension_bundle_version (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    extension_bundle_id VARCHAR(50) NOT NULL,
    version VARCHAR(50) NOT NULL,
    created TIMESTAMP NOT NULL,
    created_by VARCHAR(1000) NOT NULL,
    description VARCHAR(1000),
    sha_256_hex VARCHAR(64) NOT NULL,
    sha_256_supplied BOOLEAN NOT NULL DEFAULT false,
    build_tool VARCHAR(50),
    build_flags VARCHAR(1000),
    build_branch VARCHAR(1000),
    build_tag VARCHAR(1000),
    build_revision VARCHAR(1000),
    built TIMESTAMP,
    built_by VARCHAR(1000),
    CONSTRAINT fk_extension_bundle_version_bundle FOREIGN KEY (extension_bundle_id) REFERENCES extension_bundle(id) ON DELETE CASCADE,
    CONSTRAINT uc_extension_bundle_version UNIQUE (extension_bundle_id, version)
);

CREATE INDEX IF NOT EXISTS idx_extension_bundle_version_bundle_id ON extension_bundle_version(extension_bundle_id);

CREATE TABLE IF NOT EXISTS extension_bundle_version_dependency (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    extension_bundle_version_id VARCHAR(50) NOT NULL,
    group_id VARCHAR(1000) NOT NULL,
    artifact_id VARCHAR(1000) NOT NULL,
    version VARCHAR(50) NOT NULL,
    CONSTRAINT fk_extension_bundle_version_dependency FOREIGN KEY (extension_bundle_version_id) REFERENCES extension_bundle_version(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_extension_bundle_version_dependency_bundle_version_id ON extension_bundle_version_dependency(extension_bundle_version_id);

CREATE TABLE IF NOT EXISTS extension (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    extension_bundle_version_id VARCHAR(50) NOT NULL,
    name VARCHAR(1000) NOT NULL,
    display_name VARCHAR(1000),
    extension_type VARCHAR(50) NOT NULL,
    content TEXT,
    has_additional_details BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT fk_extension_bundle_version FOREIGN KEY (extension_bundle_version_id) REFERENCES extension_bundle_version(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_extension_bundle_version_id ON extension(extension_bundle_version_id);
CREATE INDEX IF NOT EXISTS idx_extension_name ON extension(name);
CREATE INDEX IF NOT EXISTS idx_extension_type ON extension(extension_type);

CREATE TABLE IF NOT EXISTS extension_tag (
    extension_id VARCHAR(50) NOT NULL,
    tag VARCHAR(1000) NOT NULL,
    PRIMARY KEY (extension_id, tag),
    CONSTRAINT fk_extension_tag_extension FOREIGN KEY (extension_id) REFERENCES extension(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_extension_tag_extension_id ON extension_tag(extension_id);

CREATE TABLE IF NOT EXISTS extension_provided_service_api (
    extension_id VARCHAR(50) NOT NULL,
    class_name VARCHAR(1000) NOT NULL,
    group_id VARCHAR(1000),
    artifact_id VARCHAR(1000),
    version VARCHAR(50),
    PRIMARY KEY (extension_id, class_name),
    CONSTRAINT fk_extension_provided_service_api_extension FOREIGN KEY (extension_id) REFERENCES extension(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_extension_provided_service_api_extension_id ON extension_provided_service_api(extension_id);

CREATE TABLE IF NOT EXISTS extension_restriction (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    extension_id VARCHAR(50) NOT NULL,
    required_permission VARCHAR(1000) NOT NULL,
    explanation TEXT,
    CONSTRAINT fk_extension_restriction_extension FOREIGN KEY (extension_id) REFERENCES extension(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_extension_restriction_extension_id ON extension_restriction(extension_id);

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
GRANT ALL PRIVILEGES ON DATABASE nifi_registry TO nifi;

-- Grant schema privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO nifi;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Grant to nifi user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO nifi;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO nifi;

-- Grant future objects privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO nifi;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO nifi;
