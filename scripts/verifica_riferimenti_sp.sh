#!/bin/bash
# Script: verifica_riferimenti_sp.sh
# Descrizione: Verifica che tutti i riferimenti SP nelle matrici di dipendenza esistano

echo "=== Verifica Riferimenti SP ==="
echo

# Trova tutti gli SP esistenti
existing_sp=$(find docs/use_cases -name "01 SP*.md" | sed 's|.*/01 SP||; s| - .*||' | sort | uniq)

echo "SP esistenti trovati: $(echo "$existing_sp" | wc -l)"
echo "$existing_sp"
echo

# Verifica riferimenti nelle matrici
echo "Verificando riferimenti nelle matrici di dipendenza..."
find docs/use_cases -name "*Matrice Dipendenze*.md" | while read matrix_file; do
    echo "Analizzando: $(basename "$matrix_file")"

    # Estrai riferimenti SP dal file (pattern SP\d+)
    references=$(grep -o 'SP[0-9]\+' "$matrix_file" | sort | uniq)

    if [ -n "$references" ]; then
        echo "$references" | while read ref; do
            sp_num=$(echo "$ref" | sed 's/SP//')
            if echo "$existing_sp" | grep -q "^$sp_num$"; then
                echo "  ✓ $ref → esistente"
            else
                echo "  ✗ $ref → ORFANO (non trovato)"
            fi
        done
    else
        echo "  ⚠ Nessun riferimento SP trovato"
    fi
    echo
done

echo "=== Controllo collegamenti nei diagrammi ==="
# Verifica collegamenti nei diagrammi mermaid
find docs/use_cases -name "01 SP*.md" | while read sp_file; do
    sp_name=$(basename "$sp_file" .md)
    echo "Verificando collegamenti in: $sp_name"

    # Estrai riferimenti SP\d+ dal file
    refs=$(grep -o 'SP[0-9]\+' "$sp_file" | grep -v "$sp_name" | sort | uniq)

    if [ -n "$refs" ]; then
        echo "$refs" | while read ref; do
            sp_num=$(echo "$ref" | sed 's/SP//')
            if echo "$existing_sp" | grep -q "^$sp_num$"; then
                echo "  ✓ $ref → OK"
            else
                echo "  ✗ $ref → ORFANO"
            fi
        done
    else
        echo "  ⚠ Nessun riferimento esterno trovato"
    fi
    echo
done