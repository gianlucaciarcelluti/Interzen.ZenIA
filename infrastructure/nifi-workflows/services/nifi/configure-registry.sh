#!/bin/bash
set -e

# Script per configurare automaticamente NiFi Registry client
# Questo script attende che NiFi sia completamente avviato e poi registra il Registry

NIFI_API="http://localhost:8080/nifi-api"
REGISTRY_URL="http://nifi-registry:18080"
REGISTRY_NAME="NiFi Registry"
MAX_RETRIES=30
RETRY_INTERVAL=10

echo "================================================"
echo "🔧 Configurazione automatica NiFi Registry"
echo "================================================"

# Funzione per attendere che NiFi sia pronto
wait_for_nifi() {
    echo "⏳ Attendo che NiFi sia completamente avviato..."
    local retries=0
    
    while [ $retries -lt $MAX_RETRIES ]; do
        if curl -s -f "${NIFI_API}/flow/about" > /dev/null 2>&1; then
            echo "✅ NiFi è pronto!"
            return 0
        fi
        
        retries=$((retries + 1))
        echo "   Tentativo ${retries}/${MAX_RETRIES}... (attendo ${RETRY_INTERVAL}s)"
        sleep $RETRY_INTERVAL
    done
    
    echo "❌ Timeout: NiFi non è diventato pronto in tempo"
    return 1
}

# Funzione per verificare se il Registry è già configurato
check_existing_registry() {
    echo "🔍 Verifico se il Registry è già configurato..."
    
    local registries=$(curl -s -X GET "${NIFI_API}/controller/registry-clients" 2>/dev/null)
    
    if echo "$registries" | jq -e ".registries[] | select(.component.name == \"${REGISTRY_NAME}\")" > /dev/null 2>&1; then
        echo "✅ Registry '${REGISTRY_NAME}' è già configurato"
        return 0
    else
        echo "ℹ️  Registry non trovato, procedo con la configurazione"
        return 1
    fi
}

# Funzione per configurare il Registry
configure_registry() {
    echo "📝 Configurazione del Registry client..."
    
    # Ottieni la revisione corrente
    local revision=$(curl -s "${NIFI_API}/controller/revision" | jq -r '.revision.version')
    
    if [ -z "$revision" ] || [ "$revision" = "null" ]; then
        echo "⚠️  Impossibile ottenere la revisione, uso 0"
        revision=0
    fi
    
    # Crea il payload JSON per il Registry client
    local payload=$(cat <<EOF
{
  "revision": {
    "version": ${revision}
  },
  "component": {
    "name": "${REGISTRY_NAME}",
    "description": "NiFi Registry configurato automaticamente",
    "uri": "${REGISTRY_URL}",
    "type": "org.apache.nifi.registry.flow.NifiRegistryFlowRegistryClient"
  }
}
EOF
)
    
    echo "📤 Invio richiesta di configurazione..."
    local response=$(curl -s -X POST "${NIFI_API}/controller/registry-clients" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    if echo "$response" | jq -e '.id' > /dev/null 2>&1; then
        local registry_id=$(echo "$response" | jq -r '.id')
        echo "✅ Registry configurato con successo!"
        echo "   ID: ${registry_id}"
        echo "   Nome: ${REGISTRY_NAME}"
        echo "   URL: ${REGISTRY_URL}"
        return 0
    else
        echo "❌ Errore nella configurazione del Registry"
        echo "   Risposta: $response"
        return 1
    fi
}

# Esecuzione principale
main() {
    echo ""
    echo "Parametri di configurazione:"
    echo "  - NiFi API: ${NIFI_API}"
    echo "  - Registry URL: ${REGISTRY_URL}"
    echo "  - Registry Name: ${REGISTRY_NAME}"
    echo ""
    
    # Attendi che NiFi sia pronto
    if ! wait_for_nifi; then
        echo "❌ Impossibile procedere: NiFi non disponibile"
        exit 1
    fi
    
    echo ""
    
    # Verifica se il Registry è già configurato
    if check_existing_registry; then
        echo ""
        echo "================================================"
        echo "✅ Configurazione già presente, nessuna azione necessaria"
        echo "================================================"
        exit 0
    fi
    
    echo ""
    
    # Configura il Registry
    if configure_registry; then
        echo ""
        echo "================================================"
        echo "🎉 Configurazione completata con successo!"
        echo "================================================"
        echo ""
        echo "Ora puoi:"
        echo "  1. Aprire NiFi UI: http://localhost:8080/nifi"
        echo "  2. Fare clic destro sul canvas → 'Version' → 'Start version control'"
        echo "  3. Selezionare '${REGISTRY_NAME}' dal menu"
        echo ""
        exit 0
    else
        echo ""
        echo "================================================"
        echo "❌ Configurazione fallita"
        echo "================================================"
        exit 1
    fi
}

# Avvia lo script
main
