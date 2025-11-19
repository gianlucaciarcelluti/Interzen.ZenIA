#!/bin/bash

# Script per eliminare tutti i controller services duplicati/invalidi

NIFI_URL="http://localhost:8080/nifi-api"
ROOT_PG_ID="4de44884-019a-1000-cc24-f93e40872335"

echo "🧹 Pulizia controller services..."

# Get all controller services
services=$(curl -s "$NIFI_URL/flow/process-groups/$ROOT_PG_ID/controller-services" | jq -r '.controllerServices[] | "\(.id)|\(.revision.version)|\(.component.name)"')

echo "Trovati $(echo "$services" | wc -l | tr -d ' ') controller services"

# Delete each one
echo "$services" | while IFS='|' read -r id version name; do
    if [ -n "$id" ]; then
        echo "  Eliminazione: $name (ID: $id, version: $version)"
        curl -s -X DELETE "$NIFI_URL/controller-services/$id?version=$version&disconnectedNodeAcknowledged=false" > /dev/null
    fi
done

echo "✅ Pulizia completata"
