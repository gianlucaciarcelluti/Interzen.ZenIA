#!/bin/bash

NIFI_URL="http://localhost:8080/nifi-api"

echo "🧹 Pulizia process group duplicati..."

# Get all process groups
pgs=$(curl -s "$NIFI_URL/process-groups/root/process-groups" | jq -r '.processGroups[] | "\(.id)|\(.component.name)|\(.revision.version)"')

# Track seen names
declare -A seen_names

while IFS='|' read -r id name version; do
    if [ -n "${seen_names[$name]}" ]; then
        echo "��️  Rimozione duplicato: $name (ID: $id)"
        
        # Stop all processors first
        curl -s -X PUT "$NIFI_URL/process-groups/$id" \
            -H "Content-Type: application/json" \
            -d "{\"id\":\"$id\",\"state\":\"STOPPED\"}" > /dev/null 2>&1
        
        sleep 1
        
        # Delete the process group
        curl -s -X DELETE "$NIFI_URL/process-groups/$id?version=$version&disconnectedNodeAcknowledged=false" > /dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            echo "   ✅ Rimosso"
        else
            echo "   ⚠️  Errore rimozione (potrebbe avere connessioni attive)"
        fi
    else
        seen_names[$name]=1
        echo "✅ Mantenuto: $name (ID: $id)"
    fi
done <<< "$pgs"

echo ""
echo "✅ Pulizia completata"
