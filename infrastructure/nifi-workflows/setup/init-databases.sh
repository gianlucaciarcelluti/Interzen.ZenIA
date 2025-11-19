#!/bin/bash
set -e

# Script per creare database multipli in PostgreSQL
# Questo script viene eseguito automaticamente da docker-entrypoint-initdb.d

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Enable pgvector extension on main database
    CREATE EXTENSION IF NOT EXISTS vector;
    
    -- Create nifi database (for future NiFi integrations if needed)
    SELECT 'CREATE DATABASE nifi' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nifi')\gexec
    
    -- Create nifi user with correct password from environment
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'nifi') THEN
            CREATE USER nifi WITH PASSWORD '${POSTGRES_PASSWORD}';
        END IF;
    END
    \$\$;
    
    -- Grant privileges to nifi user
    GRANT ALL PRIVILEGES ON DATABASE nifi TO nifi;
    GRANT ALL PRIVILEGES ON DATABASE provvedimenti TO postgres;
    
    -- Grant schema privileges
    \connect nifi
    GRANT ALL ON SCHEMA public TO nifi;

    -- Database per NiFi Registry
    \connect postgres
    SELECT 'CREATE DATABASE nifi_registry' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nifi_registry')\gexec
    GRANT ALL PRIVILEGES ON DATABASE nifi_registry TO postgres;
    
    -- Database per NiFi Registry Versioning
    SELECT 'CREATE DATABASE nifi_registry_versioning' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nifi_registry_versioning')\gexec
    GRANT ALL PRIVILEGES ON DATABASE nifi_registry_versioning TO postgres;
    
    -- Connect to nifi_registry to grant schema privileges
    \connect nifi_registry
    GRANT ALL ON SCHEMA public TO postgres;
    
    -- Connect to nifi_registry_versioning to grant schema privileges
    \connect nifi_registry_versioning
    GRANT ALL ON SCHEMA public TO postgres;
    
    -- Database per NiFi Audit Trail
    \connect postgres
    SELECT 'CREATE DATABASE nifi_audit' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nifi_audit')\gexec
    GRANT ALL PRIVILEGES ON DATABASE nifi_audit TO postgres;
    GRANT ALL PRIVILEGES ON DATABASE nifi_audit TO nifi;
    
    -- Connect to nifi_audit to grant schema privileges
    \connect nifi_audit
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO nifi;
EOSQL

echo "Database initialization completed successfully"
