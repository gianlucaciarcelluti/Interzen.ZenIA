#!/bin/bash
# Script: verifica_json_sp.sh
# Descrizione: Verifica quali SP hanno esempi JSON e quali no

echo "=== Verifica Esempi JSON negli SP ==="
echo

find docs/use_cases -name "01 SP*.md" | while read file; do
    sp_name=$(basename "$file" .md)
    echo "Analizzando: $sp_name"

    # Conta blocchi JSON
    json_count=$(grep -c '```json' "$file")

    if [ "$json_count" -gt 0 ]; then
        echo "  ✓ Ha $json_count esempi JSON"
    else
        echo "  ✗ Manca esempi JSON"
    fi
    echo
done

echo "=== Riepilogo ==="
total_sp=$(find docs/use_cases -name "01 SP*.md" | wc -l)
with_json=$(find docs/use_cases -name "01 SP*.md" -exec grep -l '```json' {} \; | wc -l)
without_json=$((total_sp - with_json))

echo "SP totali: $total_sp"
echo "Con JSON: $with_json"
echo "Senza JSON: $without_json"