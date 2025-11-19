#!/bin/bash

# Script per organizzare i process group in una griglia ordinata sul canvas

NIFI_URL="http://localhost:8080/nifi-api"

# Configurazione griglia
COLUMNS=3
SPACING_X=500
SPACING_Y=400
START_X=50
START_Y=50

echo "🎨 Organizzazione layout canvas NiFi..."

# Array dei workflow nell'ordine desiderato
workflows=(
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

index=0
for workflow in "${workflows[@]}"; do
    # Calcola posizione nella griglia
    row=$((index / COLUMNS))
    col=$((index % COLUMNS))
    
    x=$((START_X + col * SPACING_X))
    y=$((START_Y + row * SPACING_Y))
    
    echo "📍 Posizionamento $workflow a ($x, $y)..."
    
    # Get process group details
    pg_response=$(curl -s "$NIFI_URL/process-groups/root/process-groups")
    pg_data=$(echo "$pg_response" | jq -r ".processGroups[] | select(.component.name == \"$workflow\")")
    
    if [ -z "$pg_data" ] || [ "$pg_data" = "null" ]; then
        echo "   ⚠️  Process group $workflow non trovato"
        ((index++))
        continue
    fi
    
    pg_id=$(echo "$pg_data" | jq -r '.id')
    version=$(echo "$pg_data" | jq -r '.revision.version')
    
    # Update position
    payload=$(cat <<EOF
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
    
    response=$(curl -s -X PUT "$NIFI_URL/process-groups/$pg_id" \
        -H "Content-Type: application/json" \
        -d "$payload")
    
    if echo "$response" | grep -q "position"; then
        echo "   ✅ Posizionato a ($x, $y)"
    else
        echo "   ⚠️  Errore posizionamento"
    fi
    
    ((index++))
done

echo ""
echo "✅ Layout organizzato in griglia ${COLUMNS} colonne"
echo ""
echo "📐 Layout finale:"
echo "   Riga 1: SP01, SP02, SP03"
echo "   Riga 2: SP04, SP05, SP06"
echo "   Riga 3: SP07, SP08, SP11"
echo ""
