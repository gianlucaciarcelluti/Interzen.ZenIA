#!/bin/bash

# =========================================
# NiFi Workflow Setup Script
# Importa templates, configura controller services e avvia processors
# =========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

NIFI_URL="http://localhost:8080/nifi-api"

echo -e "${BLUE}🚀 Setup Workflow NiFi - ZenIA${NC}"
echo "=================================================="

# =========================================
# Function: Wait for service
# =========================================

wait_for_service() {
    local url=$1
    local service_name=$2
    local max_retries=30
    local retry_count=0

    echo -e "${YELLOW}⏳ Attendo $service_name...${NC}"

    while [ $retry_count -lt $max_retries ]; do
        if curl -s "$url" &> /dev/null; then
            echo -e "${GREEN}✅ $service_name disponibile${NC}"
            return 0
        fi
        echo "   Tentativo $((retry_count+1))/$max_retries..."
        sleep 5
        retry_count=$((retry_count+1))
    done

    echo -e "${RED}❌ $service_name non disponibile dopo $max_retries tentativi${NC}"
    return 1
}

# =========================================
# Function: Import template from file (Direct upload)
# =========================================

import_template() {
    local template_file=$1
    local flow_name=$2

    # Check if template already exists
    if template_exists "$flow_name"; then
        echo -e "${GREEN}✅ Template $flow_name già esistente${NC}" >&2
        # Get existing template ID
        local template_id=$(curl -s "$NIFI_URL/flow/templates" | jq -r ".templates[] | select(.template.name == \"$flow_name\") | .id")
        echo "$template_id"
        return 0
    fi

    echo -e "${YELLOW}📥 Upload template $flow_name da file...${NC}" >&2

    if [ ! -f "$template_file" ]; then
        echo -e "${RED}❌ File template non trovato: $template_file${NC}" >&2
        return 1
    fi

    local response=$(curl -s -X POST "$NIFI_URL/process-groups/root/templates/upload" \
        -F "template=@$template_file;type=text/xml")

    if echo "$response" | grep -q "already exists"; then
        echo -e "${GREEN}✅ Template $flow_name già esistente${NC}" >&2
        # Get existing template ID
        local existing_id=$(curl -s "$NIFI_URL/flow/templates" | jq -r ".templates[] | select(.template.name == \"$flow_name\") | .id")
        echo "$existing_id"
        return 0
    fi

    if echo "$response" | grep -q "template"; then
        local template_id=$(echo "$response" | jq -r '.template.id')
        echo -e "${GREEN}✅ Template $flow_name uploadato (ID: $template_id)${NC}" >&2
        echo "$template_id"
    else
        echo -e "${RED}❌ Errore upload template $flow_name${NC}" >&2
        echo "$response" >&2
        return 1
    fi
}

# =========================================
# Function: Instantiate template (Idempotent)
# =========================================

instantiate_template() {
    local template_id=$1
    local flow_name=$2
    local x=${3:-0}
    local y=${4:-0}

    # Clean template_id from any ANSI escape sequences
    template_id=$(echo "$template_id" | sed 's/\x1b\[[0-9;]*m//g' | tr -d '\r\n')

    # Check if process group already exists
    if process_group_exists "$flow_name"; then
        echo -e "${GREEN}✅ Process group $flow_name già esistente${NC}" >&2
        # Get existing process group ID
        local pg_response=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
        if [ $? -eq 0 ] && [ -n "$pg_response" ]; then
            local pg_id=$(echo "$pg_response" | jq -r ".processGroups[] | select(.component.name == \"$flow_name\") | .id" 2>/dev/null)
            if [ -n "$pg_id" ] && [ "$pg_id" != "null" ]; then
                echo "$pg_id"
                return 0
            fi
        fi
        echo "existing-pg-id"
        return 0
    fi

    echo -e "${YELLOW}🏗️  Istanziazione template $flow_name...${NC}" >&2

    local payload="{\"originX\": $x, \"originY\": $y, \"templateId\": \"$template_id\"}"

    local response=$(curl -s -X POST "$NIFI_URL/process-groups/root/template-instance" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if echo "$response" | grep -q "flow"; then
        local pg_id=$(echo "$response" | jq -r '.flow.id' 2>/dev/null)
        if [ -n "$pg_id" ] && [ "$pg_id" != "null" ]; then
            echo -e "${GREEN}✅ Template $flow_name istanziato (PG ID: $pg_id)${NC}" >&2
            echo "$pg_id"
        else
            echo -e "${GREEN}✅ Template $flow_name istanziato${NC}" >&2
            echo "new-pg-id"
        fi
    else
        # Check if it already exists (in case the check failed)
        if echo "$response" | grep -q "already exists\|duplicate\|exists"; then
            echo -e "${GREEN}✅ Process group $flow_name già esistente${NC}" >&2
            echo "existing-pg-id"
        else
            echo -e "${RED}❌ Errore istanziazione template $flow_name${NC}" >&2
            echo "$response" >&2
            return 1
        fi
    fi
}

# =========================================
# Function: Get controller service ID by name
# =========================================

get_controller_service_id() {
    local name=$1
    # Get root process group ID first
    local root_pg_id=$(curl -s "$NIFI_URL/flow/process-groups/root" 2>/dev/null | jq -r '.processGroupFlow.id' 2>/dev/null)
    if [ -z "$root_pg_id" ] || [ "$root_pg_id" = "null" ]; then
        return 1  # Failed to get root PG ID
    fi
    
    # Use the correct endpoint to get controller services
    local response=$(curl -s "$NIFI_URL/flow/process-groups/$root_pg_id/controller-services" 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$response" ]; then
        return 1  # API failed
    fi

    # Try to extract ID using jq from the correct path
    local cs_id=$(echo "$response" | jq -r ".controllerServices[]? | select(.component.name == \"$name\") | .id" 2>/dev/null | head -1)
    if [ -n "$cs_id" ] && [ "$cs_id" != "null" ]; then
        echo "$cs_id"
        return 0
    fi

    return 1  # Not found
}

# =========================================
# Function: Update controller service properties
# =========================================

update_controller_service_properties() {
    local cs_id=$1
    local name=$2
    shift 2  # Remove cs_id and name from arguments, rest are properties

    echo -e "${YELLOW}🔄 Aggiornamento proprietà controller service $name...${NC}"

    # Get current revision
    local current_revision=$(curl -s "$NIFI_URL/controller-services/$cs_id" | jq -r '.revision.version // 1' 2>/dev/null)
    if [ -z "$current_revision" ] || [ "$current_revision" = "null" ]; then
        current_revision=1
    fi

    local props_json=""
    local properties=("$@")
    for prop in "${properties[@]}"; do
        key=$(echo "$prop" | cut -d'=' -f1)
        value=$(echo "$prop" | cut -d'=' -f2-)
        # Escape quotes in value
        value=$(echo "$value" | sed 's/"/\\"/g')
        props_json="$props_json\"$key\": \"$value\","
    done
    props_json=${props_json%,}

    local payload=$(cat <<EOF
{
  "revision": {
    "version": $current_revision
  },
  "component": {
    "properties": {
      $props_json
    }
  }
}
EOF
)

    local response=$(curl -s -X PUT "$NIFI_URL/controller-services/$cs_id" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if echo "$response" | grep -q "id\|properties"; then
        echo -e "${GREEN}✅ Proprietà controller service $name aggiornate${NC}"
        return 0
    else
        echo -e "${RED}❌ Errore aggiornamento proprietà controller service $name${NC}"
        echo "$response" >&2
        return 1
    fi
}

# =========================================
# Function: Create or update controller service (Fully idempotent)
# =========================================

create_controller_service() {
    local name=$1
    local type=$2
    shift 2  # Remove name and type from arguments, rest are properties

    # Check if controller service already exists and get its ID
    local existing_id=$(get_controller_service_id "$name")
    if [ $? -eq 0 ] && [ -n "$existing_id" ]; then
        echo -e "${GREEN}✅ Controller service $name già esistente (ID: $existing_id)${NC}"
        # Update properties to ensure they are correct
        local properties=("$@")
        update_controller_service_properties "$existing_id" "$name" properties
        echo "$existing_id"
        return 0
    fi

    echo -e "${YELLOW}🔧 Creazione controller service $name...${NC}"

    local props_json=""
    local properties=("$@")
    for prop in "${properties[@]}"; do
        key=$(echo "$prop" | cut -d'=' -f1)
        value=$(echo "$prop" | cut -d'=' -f2-)
        # Escape quotes in value
        value=$(echo "$value" | sed 's/"/\\"/g')
        props_json="$props_json\"$key\": \"$value\","
    done
    props_json=${props_json%,}

    local payload=$(cat <<EOF
{
  "revision": {
    "version": 0
  },
  "component": {
    "name": "$name",
    "type": "$type",
    "properties": {
      $props_json
    }
  }
}
EOF
)

    local response=$(curl -s -X POST "$NIFI_URL/process-groups/root/controller-services" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if echo "$response" | grep -q "id"; then
        local cs_id=$(echo "$response" | jq -r '.id' 2>/dev/null)
        if [ -n "$cs_id" ] && [ "$cs_id" != "null" ]; then
            echo -e "${GREEN}✅ Controller service $name creato (ID: $cs_id)${NC}"
            echo "$cs_id"
        else
            echo -e "${GREEN}✅ Controller service $name creato${NC}"
            echo "new-service-id"
        fi
    else
        # Check if it already exists (in case the check failed)
        if echo "$response" | grep -q "already exists\|duplicate\|exists"; then
            echo -e "${GREEN}✅ Controller service $name già esistente${NC}"
            # Try to get the ID again
            local retry_id=$(get_controller_service_id "$name")
            if [ $? -eq 0 ] && [ -n "$retry_id" ]; then
                # Update properties for the existing service
                update_controller_service_properties "$retry_id" "$name" properties
                echo "$retry_id"
            else
                echo "existing-service-id"
            fi
        else
            echo -e "${RED}❌ Errore creazione controller service $name${NC}"
            echo "$response" >&2
            return 1
        fi
    fi
}

# =========================================
# Function: Enable controller service (Idempotent)
# =========================================

enable_controller_service() {
    local cs_id=$1
    local name=$2
    local version=${3:-1}

    # If cs_id is not valid, try to get it by name
    if [ "$cs_id" = "existing-service-id" ] || [ "$cs_id" = "new-service-id" ] || [ -z "$cs_id" ]; then
        local found_id=$(get_controller_service_id "$name")
        if [ $? -eq 0 ] && [ -n "$found_id" ]; then
            cs_id="$found_id"
            echo -e "${YELLOW}🔍 Trovato ID esistente per $name: $cs_id${NC}"
        else
            echo -e "${GREEN}✅ Controller service $name già abilitato (ID non disponibile)${NC}"
            return 0
        fi
    fi

    echo -e "${YELLOW}▶️  Abilitazione controller service $name...${NC}"

    local payload="{\"revision\": {\"version\": $version}, \"state\": \"ENABLED\"}"

    local response=$(curl -s -X PUT "$NIFI_URL/controller-services/$cs_id/run-status" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if echo "$response" | grep -q "ENABLED"; then
        echo -e "${GREEN}✅ Controller service $name abilitato${NC}"
    else
        echo -e "${YELLOW}⚠️  Controller service $name: potrebbe già essere abilitato${NC}"
        # Don't fail, just warn
    fi
}

# =========================================
# Function: Check if template exists
# =========================================

template_exists() {
    local name=$1
    local exists=$(curl -s "$NIFI_URL/flow/templates" | jq -r ".templates[]?.template.name // empty" | grep -c "^$name$")
    [ "$exists" -gt 0 ]
}

process_group_exists() {
    local name=$1
    # Try to get process groups - if API fails, assume it doesn't exist
    local response=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$response" ]; then
        return 1  # Assume it doesn't exist if API fails
    fi

    # Use jq to count exact matches
    local count=$(echo "$response" | jq -r "[.processGroups[] | select(.component.name == \"$name\")] | length" 2>/dev/null)
    if [ -z "$count" ] || [ "$count" = "null" ]; then
        return 1
    fi
    [ "$count" -gt 0 ]
}

# =========================================
# Function: Get or create NiFi Registry bucket (Idempotent)
# =========================================

get_registry_bucket_id() {
    local bucket_name=$1
    local response=$(curl -s "http://localhost:18080/nifi-registry-api/buckets" 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$response" ]; then
        return 1  # API failed
    fi

    # Extract bucket ID by name
    local bucket_id=$(echo "$response" | jq -r ".[] | select(.name == \"$bucket_name\") | .identifier" 2>/dev/null | head -1)
    if [ -n "$bucket_id" ] && [ "$bucket_id" != "null" ]; then
        echo "$bucket_id"
        return 0
    fi

    return 1  # Not found
}

get_or_create_registry_bucket() {
    local bucket_name=$1
    local description=${2:-"Bucket for $bucket_name workflows"}

    # Check if bucket already exists
    local existing_id=$(get_registry_bucket_id "$bucket_name")
    if [ $? -eq 0 ] && [ -n "$existing_id" ]; then
        echo -e "${GREEN}✅ Registry bucket $bucket_name già esistente (ID: $existing_id)${NC}" >&2
        echo "$existing_id"
        return 0
    fi

    echo -e "${YELLOW}🪣 Creazione bucket Registry $bucket_name...${NC}" >&2

    # Create bucket
    local payload=$(cat <<EOF
{
  "name": "$bucket_name",
  "description": "$description",
  "allowPublicRead": false
}
EOF
)

    local response=$(curl -s -X POST "http://localhost:18080/nifi-registry-api/buckets" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if echo "$response" | grep -q "identifier"; then
        local bucket_id=$(echo "$response" | jq -r '.identifier' 2>/dev/null)
        if [ -n "$bucket_id" ] && [ "$bucket_id" != "null" ]; then
            echo -e "${GREEN}✅ Bucket Registry $bucket_name creato (ID: $bucket_id)${NC}" >&2
            echo "$bucket_id"
        else
            echo -e "${GREEN}✅ Bucket Registry $bucket_name creato${NC}" >&2
            echo "new-bucket-id"
        fi
    else
        # Check if it already exists (race condition)
        if echo "$response" | grep -q "already exists\|duplicate"; then
            echo -e "${GREEN}✅ Bucket Registry $bucket_name già esistente${NC}" >&2
            local retry_id=$(get_registry_bucket_id "$bucket_name")
            if [ $? -eq 0 ] && [ -n "$retry_id" ]; then
                echo "$retry_id"
            else
                echo "existing-bucket-id"
            fi
        else
            echo -e "${RED}❌ Errore creazione bucket Registry $bucket_name${NC}" >&2
            echo "$response" >&2
            return 1
        fi
    fi
}

# =========================================
# Function: Get or create NiFi Registry Client (Idempotent)
# =========================================

get_registry_client_id() {
    local client_name=$1
    local response=$(curl -s "$NIFI_URL/controller/registry-clients" 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$response" ]; then
        return 1  # API failed
    fi

    # Extract registry client ID by name
    local client_id=$(echo "$response" | jq -r ".registries[]? | select(.component.name == \"$client_name\") | .id" 2>/dev/null | head -1)
    if [ -n "$client_id" ] && [ "$client_id" != "null" ]; then
        echo "$client_id"
        return 0
    fi

    return 1  # Not found
}

get_or_create_registry_client() {
    local client_name=$1
    local registry_url=$2
    local description=${3:-"Registry client for $client_name"}

    # Check if registry client already exists
    local existing_id=$(get_registry_client_id "$client_name")
    if [ $? -eq 0 ] && [ -n "$existing_id" ]; then
        echo -e "${GREEN}✅ Registry client $client_name già esistente (ID: $existing_id)${NC}" >&2
        echo "$existing_id"
        return 0
    fi

    echo -e "${YELLOW}🔗 Creazione Registry client $client_name...${NC}" >&2

    # Create registry client
    local payload=$(cat <<EOF
{
  "revision": {
    "version": 0
  },
  "component": {
    "name": "$client_name",
    "description": "$description",
    "type": "org.apache.nifi.registry.flow.NifiRegistryFlowRegistryClient",
    "properties": {
      "url": "$registry_url"
    }
  }
}
EOF
)

    local response=$(curl -s -X POST "$NIFI_URL/controller/registry-clients" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if echo "$response" | grep -q "id"; then
        local client_id=$(echo "$response" | jq -r '.id' 2>/dev/null)
        if [ -n "$client_id" ] && [ "$client_id" != "null" ]; then
            echo -e "${GREEN}✅ Registry client $client_name creato (ID: $client_id)${NC}" >&2
            echo "$client_id"
        else
            echo -e "${GREEN}✅ Registry client $client_name creato${NC}" >&2
            echo "new-client-id"
        fi
    else
        # Check if it already exists (race condition)
        if echo "$response" | grep -q "already exists\|duplicate"; then
            echo -e "${GREEN}✅ Registry client $client_name già esistente${NC}" >&2
            local retry_id=$(get_registry_client_id "$client_name")
            if [ $? -eq 0 ] && [ -n "$retry_id" ]; then
                echo "$retry_id"
            else
                echo "existing-client-id"
            fi
        else
            echo -e "${RED}❌ Errore creazione Registry client $client_name${NC}" >&2
            echo "$response" >&2
            return 1
        fi
    fi
}

# =========================================
# Function: Fix processor validation errors
# =========================================

fix_processor_validation_errors() {
    local pg_id=$1
    local pg_name=$2
    
    # Get all processors with validation errors
    local processor_data=$(curl -s "$NIFI_URL/process-groups/$pg_id/processors" 2>/dev/null)
    
    if [ -z "$processor_data" ] || [ "$processor_data" = "null" ]; then
        return 0
    fi
    
    local proc_count=$(echo "$processor_data" | jq -r '.processors | length' 2>/dev/null)
    
    if [ -z "$proc_count" ] || [ "$proc_count" = "0" ] || [ "$proc_count" = "null" ]; then
        return 0
    fi
    
    # Process each processor
    for ((i=0; i<proc_count; i++)); do
        local proc_id=$(echo "$processor_data" | jq -r ".processors[$i].id" 2>/dev/null)
        local proc_name=$(echo "$processor_data" | jq -r ".processors[$i].component.name" 2>/dev/null)
        local validation_errors=$(echo "$processor_data" | jq -r ".processors[$i].component.validationErrors[]?" 2>/dev/null)
        
        if [ -z "$validation_errors" ]; then
            continue
        fi
        
        # Check for unconnected relationship errors
        if echo "$validation_errors" | grep -q "is not connected to any component and is not auto-terminated"; then
            local relationships=$(echo "$validation_errors" | grep -oE "'[^']+' is not connected" | grep -oE "'[^']+'" | tr -d "'")
            
            if [ -n "$relationships" ]; then
                local proc_version=$(echo "$processor_data" | jq -r ".processors[$i].revision.version" 2>/dev/null)
                
                # Build auto-terminated relationships array
                local auto_term_array=$(echo "$relationships" | jq -R -s 'split("\n") | map(select(length > 0))')
                
                # Update processor to auto-terminate these relationships
                curl -s -X PUT "$NIFI_URL/processors/$proc_id" \
                    -H 'Content-Type: application/json' \
                    -d "{\"revision\":{\"version\":$proc_version},\"component\":{\"id\":\"$proc_id\",\"config\":{\"autoTerminatedRelationships\":$auto_term_array}}}" >/dev/null 2>&1
                
                if [ $? -eq 0 ]; then
                    echo -e "  ${GREEN}✅ Auto-terminated relationships in $proc_name: $(echo $relationships | tr '\n' ', ')${NC}"
                fi
            fi
        fi
    done
}

# =========================================
# Function: Start processors in process group (Idempotent)
# =========================================

start_processors() {
    local pg_id=$1
    local pg_name=$2

    # Skip if pg_id is not valid
    if [ "$pg_id" = "existing-pg-id" ] || [ "$pg_id" = "new-pg-id" ] || [ -z "$pg_id" ]; then
        echo -e "${GREEN}✅ Processors in $pg_name già gestiti${NC}"
        return 0
    fi

    echo -e "${YELLOW}▶️  Verifica/avvio processors in $pg_name...${NC}"

    # Get all processors with their details
    local processor_data=$(curl -s "$NIFI_URL/process-groups/$pg_id/processors" 2>/dev/null)
    
    if [ -z "$processor_data" ] || [ "$processor_data" = "null" ]; then
        echo -e "${GREEN}  ✅ Nessun processor da avviare in $pg_name${NC}"
        return 0
    fi

    # Extract processor count
    local proc_count=$(echo "$processor_data" | jq -r '.processors | length' 2>/dev/null)
    
    if [ -z "$proc_count" ] || [ "$proc_count" = "0" ] || [ "$proc_count" = "null" ]; then
        echo -e "${GREEN}  ✅ Nessun processor in $pg_name${NC}"
        return 0
    fi

    local started_count=0
    local already_running_count=0
    local failed_count=0

    # Process each processor by index
    for ((i=0; i<proc_count; i++)); do
        local proc_id=$(echo "$processor_data" | jq -r ".processors[$i].id" 2>/dev/null)
        local proc_name=$(echo "$processor_data" | jq -r ".processors[$i].component.name" 2>/dev/null)
        local proc_state=$(echo "$processor_data" | jq -r ".processors[$i].component.state" 2>/dev/null)
        local proc_version=$(echo "$processor_data" | jq -r ".processors[$i].revision.version" 2>/dev/null)

        if [ -z "$proc_id" ] || [ "$proc_id" = "null" ]; then
            continue
        fi

        # Skip if already running
        if [ "$proc_state" = "RUNNING" ]; then
            echo -e "${GREEN}  ✅ $proc_name già in esecuzione${NC}"
            already_running_count=$((already_running_count + 1))
            continue
        fi

        # Only start STOPPED processors
        if [ "$proc_state" = "STOPPED" ]; then
            echo -e "${CYAN}  ▶️  Avvio $proc_name...${NC}"
            
            local response=$(curl -s -X PUT "$NIFI_URL/processors/$proc_id/run-status" \
                -H "Content-Type: application/json" \
                -d "{\"revision\": {\"version\": $proc_version}, \"state\": \"RUNNING\"}" 2>/dev/null)

            if echo "$response" | grep -q '"state":"RUNNING"'; then
                echo -e "${GREEN}  ✅ $proc_name avviato con successo${NC}"
                started_count=$((started_count + 1))
            else
                echo -e "${RED}  ❌ Errore avvio $proc_name${NC}"
                failed_count=$((failed_count + 1))
            fi
        else
            echo -e "${YELLOW}  ⚠️  $proc_name in stato $proc_state (saltato)${NC}"
        fi
    done

    # Summary for this process group
    if [ $started_count -gt 0 ] || [ $already_running_count -gt 0 ] || [ $failed_count -gt 0 ]; then
        echo -e "${CYAN}  📊 Riepilogo $pg_name: $started_count avviati, $already_running_count già attivi, $failed_count errori${NC}"
    fi
}

# =========================================
# Main setup process
# =========================================

echo -e "${YELLOW}[1/8] Verifica servizi...${NC}"

# Wait for NiFi
wait_for_service "$NIFI_URL/system-diagnostics" "NiFi API"

echo -e "${GREEN}✅ Servizi disponibili${NC}"

# =========================================
# Step 1.5: Verify Audit Database
# =========================================

echo -e "${YELLOW}[1.5/8] Verifica database audit trail...${NC}"

# Check if nifi_audit database exists and has tables
AUDIT_DB_EXISTS=$(docker exec postgres-db psql -U postgres -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw nifi_audit && echo "yes" || echo "no")
AUDIT_TABLE_COUNT=0

if [ "$AUDIT_DB_EXISTS" = "yes" ]; then
    AUDIT_TABLE_COUNT=$(docker exec postgres-db psql -U postgres -d nifi_audit -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';" 2>/dev/null | tr -d ' ' || echo "0")
    
    if [ "$AUDIT_TABLE_COUNT" -eq "5" ]; then
        echo -e "${GREEN}✅ Database audit trail operativo ($AUDIT_TABLE_COUNT tabelle)${NC}"
    elif [ "$AUDIT_TABLE_COUNT" -gt "0" ]; then
        echo -e "${YELLOW}⚠️  Database audit trail parziale ($AUDIT_TABLE_COUNT/5 tabelle)${NC}"
    else
        echo -e "${YELLOW}⚠️  Database audit trail esiste ma senza tabelle${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Database audit trail non trovato${NC}"
    echo -e "${YELLOW}   💡 Esegui: docker exec postgres-db psql -U postgres -c 'CREATE DATABASE nifi_audit;'${NC}"
    echo -e "${YELLOW}   💡 Poi: docker exec -i postgres-db psql -U postgres -d nifi_audit < init-nifi-audit.sql${NC}"
fi

# =========================================
# Step 2: Configure NiFi Registry
# =========================================

echo -e "${YELLOW}[2/8] Configurazione NiFi Registry...${NC}"

# Wait for NiFi Registry
wait_for_service "http://localhost:18080/nifi-registry-api/buckets" "NiFi Registry API"

# Create bucket for versioning (idempotent)
BUCKET_NAME="ZenIA"
BUCKET_ID=$(get_or_create_registry_bucket "$BUCKET_NAME")

if [ -n "$BUCKET_ID" ] && [ "$BUCKET_ID" != "null" ] && [ "$BUCKET_ID" != "new-bucket-id" ] && [ "$BUCKET_ID" != "existing-bucket-id" ]; then
    echo -e "${GREEN}✅ Registry bucket configurato: $BUCKET_NAME (ID: $BUCKET_ID)${NC}"
else
    echo -e "${YELLOW}⚠️  Registry bucket configurato: $BUCKET_NAME${NC}"
fi

# Configure Registry Client in NiFi (idempotent)
REGISTRY_CLIENT_ID=$(get_or_create_registry_client "NiFi Registry" "http://nifi-registry:18080")

if [ -n "$REGISTRY_CLIENT_ID" ] && [ "$REGISTRY_CLIENT_ID" != "null" ] && [ "$REGISTRY_CLIENT_ID" != "new-client-id" ] && [ "$REGISTRY_CLIENT_ID" != "existing-client-id" ]; then
    echo -e "${GREEN}✅ Registry client configurato (ID: $REGISTRY_CLIENT_ID)${NC}"
else
    echo -e "${YELLOW}⚠️  Registry client configurato${NC}"
fi

# =========================================
# Step 3: Configure controller services
# =========================================

echo -e "${YELLOW}[3/8] Configurazione controller services...${NC}"

# Create PostgreSQL Controller Service
PG_PROPERTIES=(
    "Database Connection URL=jdbc:postgresql://postgres:5432/provvedimenti"
    "Database Driver Class Name=org.postgresql.Driver"
    "database-driver-locations=/opt/nifi/nifi-current/lib/postgresql-42.7.3.jar"
    "database-user=postgres"
    "Password=postgrespassword"
    "Max Wait Time=500 millis"
    "Max Total Connections=20"
    "Validation Query=SELECT 1"
)

PG_CS_ID=$(create_controller_service "PostgreSQL-Connection-Pool" "org.apache.nifi.dbcp.DBCPConnectionPool" "${PG_PROPERTIES[@]}")
if [ $? -ne 0 ]; then exit 1; fi

# Enable PostgreSQL Controller Service
enable_controller_service "$PG_CS_ID" "PostgreSQL-Connection-Pool" 1
if [ $? -ne 0 ]; then exit 1; fi

# Create Redis Controller Service
REDIS_PROPERTIES=(
    "Redis Mode=Standalone"
    "Connection String=redis:6379"
    "Database Index=0"
    "Communication Timeout=10 secs"
    "Cluster Max Redirects=5"
    "Pool - Max Total=20"
    "Pool - Max Idle=8"
    "Pool - Min Idle=0"
    "Pool - Block When Exhausted=true"
    "Pool - Max Wait Time=10 seconds"
    "Pool - Min Evictable Idle Time=60 seconds"
    "Pool - Time Between Eviction Runs=30 seconds"
    "Pool - Num Tests Per Eviction Run=-1"
    "Pool - Test On Create=false"
    "Pool - Test On Borrow=false"
    "Pool - Test On Return=false"
    "Pool - Test While Idle=true"
)

REDIS_CS_ID=$(create_controller_service "Redis-Cache-Pool" "org.apache.nifi.redis.service.RedisConnectionPoolService" "${REDIS_PROPERTIES[@]}")
if [ $? -ne 0 ]; then exit 1; fi

# Enable Redis Controller Service
enable_controller_service "$REDIS_CS_ID" "Redis-Cache-Pool" 1
if [ $? -ne 0 ]; then exit 1; fi

echo -e "${GREEN}✅ Controller services configurati e abilitati${NC}"

# =========================================
# STEP 4: Build Workflows via API (Infrastructure as Code)
# =========================================

echo ""
echo -e "${BLUE}[4/8] Creazione workflows via API...${NC}"

# Function to build workflow via Python script (idempotent)
build_workflow_via_api() {
    local script_name=$1
    local workflow_name=$2
    local pg_name=$3  # Process group name to check
    
    # Check if process group already exists
    if process_group_exists "$pg_name"; then
        echo -e "${GREEN}✅ Workflow $workflow_name già esistente${NC}" >&2
        return 0
    fi
    
    if [ -f "$script_name" ]; then
        echo -e "${YELLOW}🔨 Creazione workflow $workflow_name...${NC}" >&2
        if python3 "$script_name" 2>&1 | grep -q "success\|creato\|✅"; then
            echo -e "${GREEN}✅ Workflow $workflow_name creato${NC}" >&2
            return 0
        else
            # Check again if it was created (race condition)
            if process_group_exists "$pg_name"; then
                echo -e "${GREEN}✅ Workflow $workflow_name creato${NC}" >&2
                return 0
            else
                echo -e "${RED}❌ Errore creazione workflow $workflow_name${NC}" >&2
                return 1
            fi
        fi
    else
        echo -e "${YELLOW}⚠️  Script $script_name non trovato${NC}" >&2
        return 1
    fi
}

# Build all workflows (idempotent - checks existence first)
build_workflow_via_api "../process-groups/build-sp01-via-api.py" "SP01 EML Parser" "SP01_EML_Parser"
build_workflow_via_api "../process-groups/build-sp02-via-api.py" "SP02 Document Extractor" "SP02_Document_Extractor"
build_workflow_via_api "../process-groups/build-sp03-via-api.py" "SP03 Procedural Classifier" "SP03_Procedural_Classifier"
build_workflow_via_api "../process-groups/build-sp04-via-api.py" "SP04 Knowledge Base" "SP04_Knowledge_Base"
build_workflow_via_api "../process-groups/build-sp05-via-api.py" "SP05 Template Engine" "SP05_Template_Engine"
build_workflow_via_api "../process-groups/build-sp06-via-api.py" "SP06 Validator" "SP06_Validator"
build_workflow_via_api "../process-groups/build-sp07-via-api.py" "SP07 Content Classifier" "SP07_Content_Classifier"
build_workflow_via_api "../process-groups/build-sp08-via-api.py" "SP08 Quality Checker" "SP08_Quality_Checker"
build_workflow_via_api "../process-groups/build-sp11-via-api.py" "SP11 Security Audit" "SP11_Security_Audit"

echo -e "${GREEN}✅ Workflows creati via API${NC}"

# =========================================
# STEP 4.2: Create Ingress Endpoint Process Group
# =========================================

echo ""
echo -e "${BLUE}[4.2/8] Creazione Ingress Endpoint...${NC}"

# Check if Ingress PG already exists
if process_group_exists "Ingress_ContentListener"; then
    echo -e "${GREEN}✅ Ingress_ContentListener già esistente${NC}"
else
    echo -e "${YELLOW}🌐 Creazione Ingress_ContentListener Process Group...${NC}"
    
    if [ -f "../process-groups/create-ingress-process-group.py" ]; then
        python3 ../process-groups/create-ingress-process-group.py
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Ingress endpoint creato con successo${NC}"
            echo -e "${BLUE}ℹ️  Endpoint disponibile su: http://localhost:9099/contentListener/fascicolo${NC}"
        else
            echo -e "${YELLOW}⚠️  Creazione ingress endpoint fallita${NC}"
            echo -e "${YELLOW}💡 L'ingress può essere creato manualmente via NiFi UI${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Script create-ingress-process-group.py non trovato${NC}"
        echo -e "${YELLOW}💡 Usa create-ingress-endpoint.py come alternativa${NC}"
    fi
fi

# =========================================
# STEP 4.5: Organize Canvas Layout
# =========================================

echo ""
echo -e "${BLUE}[4.5/6] Organizzazione layout canvas...${NC}"

# Function to organize process groups in a grid
organize_canvas_layout() {
    local columns=3
    local spacing_x=500
    local spacing_y=400
    local start_x=50
    local start_y=50
    
    local workflows=(
        "Ingress_ContentListener"
        "SP01_EML_Parser"
        "SP02_Document_Extractor"
        "SP03_Procedural_Classifier"
        "SP04_Knowledge_Base"
        "SP05_Template_Engine"
        "SP06_Validator"
        "SP07_Content_Classifier"
        "SP08_Quality_Checker"
        "SP11_Security_Audit"
    )
    
    local index=0
    for workflow in "${workflows[@]}"; do
        local row=$((index / columns))
        local col=$((index % columns))
        
        local x=$((start_x + col * spacing_x))
        local y=$((start_y + row * spacing_y))
        
        # Get process group details
        local pg_response=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
        local pg_data=$(echo "$pg_response" | jq -r ".processGroups[] | select(.component.name == \"$workflow\")" 2>/dev/null)
        
        if [ -z "$pg_data" ] || [ "$pg_data" = "null" ]; then
            ((index++))
            continue
        fi
        
        local pg_id=$(echo "$pg_data" | jq -r '.id' 2>/dev/null)
        local version=$(echo "$pg_data" | jq -r '.revision.version' 2>/dev/null)
        
        # Update position
        local payload=$(cat <<EOF
{
  "revision": {
    "version": $version
  },
  "component": {
    "id": "$pg_id",
    "position": {
      "x": $x,
      "y": $y
    }
  }
}
EOF
)
        
        curl -s -X PUT "$NIFI_URL/process-groups/$pg_id" \
            -H "Content-Type: application/json" \
            -d "$payload" > /dev/null 2>&1
        
        echo -e "${YELLOW}  📍 $workflow → ($x, $y)${NC}" >&2
        
        ((index++))
    done
}

organize_canvas_layout

echo -e "${GREEN}✅ Canvas organizzato in griglia 3x3${NC}"

# Organize internal layouts of process groups
echo ""
echo -e "${BLUE}[4.6/7] Organizzazione layout interno process groups...${NC}"

if [ -f "../process-groups/organize-internal-layouts.py" ]; then
    python3 ../process-groups/organize-internal-layouts.py 2>&1 | grep -E "✅|Organizzazione layout:" | while read line; do
        echo -e "${YELLOW}$line${NC}" >&2
    done
    echo -e "${GREEN}✅ Layout interni organizzati${NC}"
else
    echo -e "${YELLOW}⚠️  Script organize-internal-layouts.py non trovato${NC}" >&2
fi

# =========================================
# STEP 5: Save Workflows to Registry (Version Control)
# =========================================

echo ""
echo -e "${BLUE}[5/8] Salvataggio workflows nel Registry per version control...${NC}"

# Function to save process group to registry
save_to_registry() {
    local pg_name=$1
    local flow_name=$2
    local description=${3:-"$pg_name workflow"}
    
    # Get process group ID
    local pg_response=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
    local pg_id=$(echo "$pg_response" | jq -r ".processGroups[] | select(.component.name == \"$pg_name\") | .id" 2>/dev/null | head -1)
    
    if [ -z "$pg_id" ] || [ "$pg_id" = "null" ]; then
        echo -e "${YELLOW}⚠️  Process group $pg_name non trovato, skip versioning${NC}" >&2
        return 0
    fi
    
    echo -e "${YELLOW}💾 Salvataggio $pg_name nel Registry...${NC}" >&2
    
    # Get current revision
    local pg_details=$(curl -s "$NIFI_URL/process-groups/$pg_id" 2>/dev/null)
    local version=$(echo "$pg_details" | jq -r '.revision.version // 0' 2>/dev/null)
    
    # Start version control
    local payload=$(cat <<EOF
{
  "processGroupRevision": {
    "version": $version
  },
  "versionControlInformation": {
    "registryId": "$REGISTRY_CLIENT_ID",
    "bucketId": "$REGISTRY_BUCKET_ID",
    "flowName": "$flow_name",
    "flowDescription": "$description",
    "comments": "Initial version created by setup script"
  }
}
EOF
)
    
    local response=$(curl -s -X PUT "$NIFI_URL/process-groups/$pg_id/version-control-information" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>/dev/null)
    
    if echo "$response" | grep -q "versionControlInformation\|bucketId"; then
        echo -e "${GREEN}✅ $pg_name salvato nel Registry${NC}" >&2
    else
        # Check if already under version control
        if echo "$response" | grep -q "already under version control\|already tracking"; then
            echo -e "${GREEN}✅ $pg_name già sotto version control${NC}" >&2
        else
            echo -e "${YELLOW}⚠️  $pg_name: impossibile salvare nel Registry (potrebbe già essere versionato)${NC}" >&2
        fi
    fi
}

# Save workflows to registry (if they were created)
save_to_registry "Ingress_ContentListener" "Ingress-ContentListener" "HTTP ingress endpoint workflow"
save_to_registry "SP01_EML_Parser" "SP01-EML-Parser" "Email parsing and extraction workflow"
save_to_registry "SP02_Document_Extractor" "SP02-Document-Extractor" "Document content extraction workflow"
save_to_registry "SP03_Procedural_Classifier" "SP03-Procedural-Classifier" "Procedural classification workflow"
save_to_registry "SP04_Knowledge_Base" "SP04-Knowledge-Base" "Knowledge base integration workflow"
save_to_registry "SP05_Template_Engine" "SP05-Template-Engine" "Document template generation workflow"
save_to_registry "SP06_Validator" "SP06-Validator" "Document validation workflow"
save_to_registry "SP07_Content_Classifier" "SP07-Content-Classifier" "Content classification workflow"
save_to_registry "SP08_Quality_Checker" "SP08-Quality-Checker" "Quality assurance workflow"
save_to_registry "SP11_Security_Audit" "SP11-Security-Audit" "Security audit workflow"

echo -e "${GREEN}✅ Workflows salvati nel Registry${NC}"

# =========================================
# Step 5.5: Create Inter-Process Group Connections
# =========================================

echo ""
echo -e "${BLUE}[5.5/8] Creazione connessioni tra Process Groups...${NC}"

# Check if we have the connection script
if [ -f "../connections/connect-process-groups.py" ]; then
    echo -e "${YELLOW}🔗 Collegamento Ingress → SP01 → HITL...${NC}"
    python3 ../connections/connect-process-groups.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Connessioni inter-PG create${NC}"
    else
        echo -e "${YELLOW}⚠️  Alcune connessioni potrebbero non essere state create${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Script connect-process-groups.py non trovato${NC}"
    echo -e "${YELLOW}💡 Le connessioni dovranno essere create manualmente via NiFi UI${NC}"
    echo -e "${YELLOW}   Connessioni richieste:${NC}"
    echo -e "${YELLOW}   - Ingress_ContentListener → SP01_EML_Parser${NC}"
    echo -e "${YELLOW}   - SP01_EML_Parser (Success) → SP11_Security_Audit${NC}"
fi

# =========================================
# Step 6: Start processors in all workflows
# =========================================

echo ""
echo -e "${YELLOW}[6/8] Avvio processors nei workflows...${NC}"

# Function to fix validation errors and start processors in a process group
start_pg_processors() {
    local pg_name=$1
    
    # Get process group ID
    local pg_response=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
    local pg_id=$(echo "$pg_response" | jq -r ".processGroups[] | select(.component.name == \"$pg_name\") | .id" 2>/dev/null | head -1)
    
    if [ -n "$pg_id" ] && [ "$pg_id" != "null" ]; then
        # First, fix validation errors
        fix_processor_validation_errors "$pg_id" "$pg_name"
        # Then start processors
        start_processors "$pg_id" "$pg_name"
    else
        echo -e "${YELLOW}⚠️  Process group $pg_name non trovato, skip processors start${NC}" >&2
    fi
}

# Start processors in all workflows
start_pg_processors "Ingress_ContentListener"
start_pg_processors "SP01_EML_Parser"
start_pg_processors "SP02_Document_Extractor"
start_pg_processors "SP03_Procedural_Classifier"
start_pg_processors "SP04_Knowledge_Base"
start_pg_processors "SP05_Template_Engine"
start_pg_processors "SP06_Validator"
start_pg_processors "SP07_Content_Classifier"
start_pg_processors "SP08_Quality_Checker"
start_pg_processors "SP11_Security_Audit"

echo -e "${GREEN}✅ Processors avviati${NC}"

# =========================================
# Step 6.5: Avvio Output/Input Ports
# =========================================

echo ""
echo -e "${YELLOW}[6.5/8] Avvio Output/Input Ports...${NC}"

# Function to start all ports in a process group
start_pg_ports() {
    local pg_name=$1
    
    # Get process group ID
    local pg_response=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
    local pg_id=$(echo "$pg_response" | jq -r ".processGroups[] | select(.component.name == \"$pg_name\") | .id" 2>/dev/null | head -1)
    
    if [ -z "$pg_id" ] || [ "$pg_id" == "null" ]; then
        return
    fi
    
    # Get flow details
    local flow=$(curl -s "$NIFI_URL/flow/process-groups/$pg_id" 2>/dev/null)
    
    # Start Output Ports
    local output_ports=$(echo "$flow" | jq -r '.processGroupFlow.flow.outputPorts[]? | select(.component.state == "STOPPED") | .id' 2>/dev/null)
    for port_id in $output_ports; do
        local port_name=$(echo "$flow" | jq -r ".processGroupFlow.flow.outputPorts[] | select(.id == \"$port_id\") | .component.name" 2>/dev/null)
        local version=$(curl -s "$NIFI_URL/output-ports/$port_id" 2>/dev/null | jq -r '.revision.version' 2>/dev/null)
        
        curl -s -X PUT "$NIFI_URL/output-ports/$port_id/run-status" \
            -H 'Content-Type: application/json' \
            -d "{\"revision\":{\"version\":$version},\"state\":\"RUNNING\",\"disconnectedNodeAcknowledged\":false}" >/dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "  ✅ Output Port avviato: ${CYAN}$port_name${NC} in $pg_name"
        fi
    done
    
    # Start Input Ports
    local input_ports=$(echo "$flow" | jq -r '.processGroupFlow.flow.inputPorts[]? | select(.component.state == "STOPPED") | .id' 2>/dev/null)
    for port_id in $input_ports; do
        local port_name=$(echo "$flow" | jq -r ".processGroupFlow.flow.inputPorts[] | select(.id == \"$port_id\") | .component.name" 2>/dev/null)
        local version=$(curl -s "$NIFI_URL/input-ports/$port_id" 2>/dev/null | jq -r '.revision.version' 2>/dev/null)
        
        curl -s -X PUT "$NIFI_URL/input-ports/$port_id/run-status" \
            -H 'Content-Type: application/json' \
            -d "{\"revision\":{\"version\":$version},\"state\":\"RUNNING\",\"disconnectedNodeAcknowledged\":false}" >/dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "  ✅ Input Port avviato: ${CYAN}$port_name${NC} in $pg_name"
        fi
    done
}

# Start ports in all process groups
start_pg_ports "Ingress_ContentListener"
start_pg_ports "SP01_EML_Parser"
start_pg_ports "SP02_Document_Extractor"
start_pg_ports "SP03_Procedural_Classifier"
start_pg_ports "SP04_Knowledge_Base"
start_pg_ports "SP05_Template_Engine"
start_pg_ports "SP06_Validator"
start_pg_ports "SP07_Content_Classifier"
start_pg_ports "SP08_Quality_Checker"
start_pg_ports "SP11_Security_Audit"

echo -e "${GREEN}✅ Output/Input Ports avviati${NC}"

# =========================================
# Step 6.6: Cleanup Invalid Audit Processors
# =========================================

echo ""
echo -e "${YELLOW}[6.6/8] Pulizia Audit processors invalidi...${NC}"

# Function to remove ALL audit processors and their connections (regardless of state)
cleanup_invalid_audit_processors() {
    local pg_name=$1
    
    # Get process group ID
    local pg_response=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
    local pg_id=$(echo "$pg_response" | jq -r ".processGroups[] | select(.component.name == \"$pg_name\") | .id" 2>/dev/null | head -1)
    
    if [ -z "$pg_id" ] || [ "$pg_id" == "null" ]; then
        return
    fi
    
    # Get flow details
    local flow=$(curl -s "$NIFI_URL/flow/process-groups/$pg_id" 2>/dev/null)
    
    # Find ALL Audit processors (regardless of state)
    local audit_processors=$(echo "$flow" | jq -r '.processGroupFlow.flow.processors[]? | select(.component.name | test("Audit_")) | .id' 2>/dev/null)
    
    for proc_id in $audit_processors; do
        local proc_name=$(echo "$flow" | jq -r ".processGroupFlow.flow.processors[] | select(.id == \"$proc_id\") | .component.name" 2>/dev/null)
        
        # First, stop the processor if running
        local proc_version=$(curl -s "$NIFI_URL/processors/$proc_id" 2>/dev/null | jq -r '.revision.version' 2>/dev/null)
        curl -s -X PUT "$NIFI_URL/processors/$proc_id/run-status" \
            -H 'Content-Type: application/json' \
            -d "{\"revision\":{\"version\":$proc_version},\"state\":\"STOPPED\",\"disconnectedNodeAcknowledged\":false}" >/dev/null 2>&1
        
        sleep 1  # Wait for processor to stop
        
        # Get updated flow after stopping
        flow=$(curl -s "$NIFI_URL/flow/process-groups/$pg_id" 2>/dev/null)
        
        # Delete all connections TO this processor
        local incoming_conns=$(echo "$flow" | jq -r ".processGroupFlow.flow.connections[]? | select(.component.destination.id == \"$proc_id\") | .id" 2>/dev/null)
        for conn_id in $incoming_conns; do
            local conn_version=$(curl -s "$NIFI_URL/connections/$conn_id" 2>/dev/null | jq -r '.revision.version' 2>/dev/null)
            curl -s -X DELETE "$NIFI_URL/connections/$conn_id?version=$conn_version&disconnectedNodeAcknowledged=false" >/dev/null 2>&1
        done
        
        # Delete all connections FROM this processor
        local outgoing_conns=$(echo "$flow" | jq -r ".processGroupFlow.flow.connections[]? | select(.component.source.id == \"$proc_id\") | .id" 2>/dev/null)
        for conn_id in $outgoing_conns; do
            local conn_version=$(curl -s "$NIFI_URL/connections/$conn_id" 2>/dev/null | jq -r '.revision.version' 2>/dev/null)
            curl -s -X DELETE "$NIFI_URL/connections/$conn_id?version=$conn_version&disconnectedNodeAcknowledged=false" >/dev/null 2>&1
        done
        
        # Finally delete the processor
        proc_version=$(curl -s "$NIFI_URL/processors/$proc_id" 2>/dev/null | jq -r '.revision.version' 2>/dev/null)
        curl -s -X DELETE "$NIFI_URL/processors/$proc_id?version=$proc_version&disconnectedNodeAcknowledged=false" >/dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✅ Rimosso Audit processor: ${CYAN}$proc_name${NC} da $pg_name"
        fi
    done
}

# Clean up audit processors in all process groups
cleanup_invalid_audit_processors "Ingress_ContentListener"
cleanup_invalid_audit_processors "SP01_EML_Parser"
cleanup_invalid_audit_processors "SP02_Document_Extractor"
cleanup_invalid_audit_processors "SP03_Procedural_Classifier"
cleanup_invalid_audit_processors "SP04_Knowledge_Base"
cleanup_invalid_audit_processors "SP05_Template_Engine"
cleanup_invalid_audit_processors "SP06_Validator"
cleanup_invalid_audit_processors "SP07_Content_Classifier"
cleanup_invalid_audit_processors "SP08_Quality_Checker"
cleanup_invalid_audit_processors "SP11_Security_Audit"

echo -e "${GREEN}✅ Audit processors invalidi rimossi${NC}"

# =========================================
# Step 7: Final Summary
# =========================================

echo ""
echo "=================================================="
echo -e "${GREEN}✅ SETUP WORKFLOW COMPLETATO${NC}"
echo "=================================================="
echo ""
echo "📊 Workflow configurati via Infrastructure as Code:"
echo ""
echo "  🔹 Ingress ContentListener (porta 9099)"
echo "  🔹 SP01 EML Parser"
echo "  🔹 SP02 Document Extractor"
echo "  🔹 SP03 Procedural Classifier"
echo "  🔹 SP04 Knowledge Base"
echo "  🔹 SP05 Template Engine"
echo "  🔹 SP06 Validator"
echo "  🔹 SP07 Content Classifier"
echo "  🔹 SP08 Quality Checker"
echo "  🔹 SP11 Security Audit"
echo ""
echo "🎨 Layout Canvas:"
echo "   ✅ Griglia 3x3 ordinata (spaziatura 500px x 400px)"
echo "   ✅ Layout interno organizzato in flusso orizzontale"
echo "   💡 Fai doppio click su un process group per vedere i dettagli"
echo ""
echo "🔹 Controller Services:"
# Extract only the UUID part from the controller service IDs
PG_CS_ID_CLEAN=$(echo "$PG_CS_ID" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)
REDIS_CS_ID_CLEAN=$(echo "$REDIS_CS_ID" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)
echo "   - PostgreSQL-Connection-Pool (ID: $PG_CS_ID_CLEAN)"
echo "   - Redis-Cache-Pool (ID: $REDIS_CS_ID_CLEAN)"
echo ""
echo "🔄 Stato Processors:"
echo "   Verifico stato di tutti i processors..."

# Count running and stopped processors across all process groups
total_running=0
total_stopped=0
total_invalid=0

all_pgs=$(curl -s "$NIFI_URL/process-groups/root/process-groups" 2>/dev/null)
for pg_name in "Ingress_ContentListener" "SP01_EML_Parser" "SP02_Document_Extractor" "SP03_Procedural_Classifier" "SP04_Knowledge_Base" "SP05_Template_Engine" "SP06_Validator" "SP07_Content_Classifier" "SP08_Quality_Checker" "SP11_Security_Audit"; do
    pg_id=$(echo "$all_pgs" | jq -r ".processGroups[] | select(.component.name == \"$pg_name\") | .id" 2>/dev/null | head -1)
    if [ -n "$pg_id" ] && [ "$pg_id" != "null" ]; then
        proc_stats=$(curl -s "$NIFI_URL/process-groups/$pg_id/processors" 2>/dev/null | jq -r '.processors[].component.state' 2>/dev/null)
        running=$(echo "$proc_stats" | grep "RUNNING" 2>/dev/null | wc -l | tr -d ' ')
        stopped=$(echo "$proc_stats" | grep "STOPPED" 2>/dev/null | wc -l | tr -d ' ')
        invalid=$(echo "$proc_stats" | grep "INVALID" 2>/dev/null | wc -l | tr -d ' ')
        total_running=$((total_running + running))
        total_stopped=$((total_stopped + stopped))
        total_invalid=$((total_invalid + invalid))
    fi
done

echo -e "   ✅ ${GREEN}$total_running processors in esecuzione${NC}"
if [ $total_stopped -gt 0 ]; then
    echo -e "   ⏸️  ${YELLOW}$total_stopped processors fermi${NC}"
fi
if [ $total_invalid -gt 0 ]; then
    echo -e "   ⚠️  ${RED}$total_invalid processors invalidi (controlla configurazione)${NC}"
fi

echo ""
echo "=================================================="
echo ""
echo "🧪 Test dell'endpoint:"
echo "   curl -X POST http://localhost:9099/contentListener/fascicolo \\"
echo "        -H 'Content-Type: message/rfc822' \\"
echo "        -d '@test-email.eml'"
echo ""
echo "📊 Monitora i logs:"
echo "   docker-compose logs -f nifi"
echo ""
echo "🔍 Verifica stato completo:"
echo "   curl -s http://localhost:8080/nifi-api/process-groups/root/process-groups | jq '.processGroups[].component.name'"
echo ""
echo "=================================================="