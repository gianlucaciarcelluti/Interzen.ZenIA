#!/bin/bash

# Script per abilitare i Controller Services
NIFI_URL="http://localhost:8080/nifi-api"

echo "🔧 Abilitazione Controller Services..."
echo ""

# Get all controller services
services=$(curl -s "$NIFI_URL/flow/process-groups/root/controller-services" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cs in data.get('controllerServices', []):
    print(f\"{cs['id']}|{cs['revision']['version']}|{cs['component']['name']}|{cs['component']['state']}\")
")

echo "$services" | while IFS='|' read -r id version name state; do
    if [ -n "$id" ]; then
        echo "📋 $name: $state"
        
        if [ "$state" = "DISABLED" ]; then
            echo "   → Abilitazione in corso..."
            
            # Enable the controller service
            response=$(curl -s -X PUT "$NIFI_URL/controller-services/$id/run-status" \
                -H "Content-Type: application/json" \
                -d "{
                    \"revision\": {
                        \"version\": $version
                    },
                    \"state\": \"ENABLED\"
                }")
            
            # Check if successful
            new_state=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('component', {}).get('state', 'ERROR'))" 2>/dev/null)
            
            if [ "$new_state" = "ENABLED" ]; then
                echo "   ✅ Abilitato con successo"
            else
                echo "   ⚠️  Potrebbe richiedere dipendenze (es. Redis/PostgreSQL in esecuzione)"
            fi
        else
            echo "   ✅ Già abilitato"
        fi
        echo ""
    fi
done

echo "🎯 Verifica finale stato Controller Services:"
curl -s "$NIFI_URL/flow/process-groups/root/controller-services" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cs in data.get('controllerServices', []):
    name = cs['component']['name']
    state = cs['component']['state']
    status = '✅' if state == 'ENABLED' else '❌'
    print(f'  {status} {name}: {state}')
"

echo ""
echo "✅ Processo completato"
