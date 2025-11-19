#!/bin/bash

NIFI_URL="http://localhost:8080/nifi-api"

echo "▶️  Avvio di tutti i processor nei workflow..."
echo ""

# Get all process groups
pgs=$(curl -s "$NIFI_URL/process-groups/root/process-groups" | jq -r '.processGroups[] | "\(.id)|\(.component.name)"')

while IFS='|' read -r pg_id pg_name; do
    echo "📦 Process Group: $pg_name"
    
    # Get all processors in this PG
    processors=$(curl -s "$NIFI_URL/process-groups/$pg_id/processors" | jq -r '.processors[] | "\(.id)|\(.component.name)|\(.component.state)|\(.revision.version)"')
    
    if [ -z "$processors" ]; then
        echo "   ⚠️  Nessun processor trovato"
        continue
    fi
    
    while IFS='|' read -r proc_id proc_name state version; do
        if [ "$state" = "STOPPED" ]; then
            echo "   ▶️  Avvio $proc_name..."
            
            # Start processor
            response=$(curl -s -X PUT "$NIFI_URL/processors/$proc_id/run-status" \
                -H "Content-Type: application/json" \
                -d "{\"revision\": {\"version\": $version}, \"state\": \"RUNNING\"}")
            
            if echo "$response" | grep -q "RUNNING"; then
                echo "      ✅ Avviato"
            else
                echo "      ⚠️  Errore: $(echo "$response" | jq -r '.status.aggregateSnapshot.runStatus // "Unknown"')"
            fi
        else
            echo "   ✅ $proc_name già in esecuzione"
        fi
    done <<< "$processors"
    
    echo ""
done <<< "$pgs"

echo "✅ Avvio completato"
echo ""
echo "🔍 Verifica stato:"
echo "   curl -s http://localhost:8080/nifi-api/flow/process-groups/root | jq '.processGroupFlow.flow.processGroups[].runningCount'"
