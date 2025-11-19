#!/bin/bash
"""
Script per costruire tutti i processor groups SP02-SP11 in sequenza
"""

echo "═══════════════════════════════════════════════════════════"
echo "🏗️  COSTRUZIONE COMPLETA PROCESSOR GROUPS SP02-SP11"
echo "═══════════════════════════════════════════════════════════"
echo

# Array degli script da eseguire
scripts=(
    "build-sp02-via-api.py"
    "build-sp03-via-api.py"
    "build-sp04-via-api.py"
    "build-sp05-via-api.py"
    "build-sp06-via-api.py"
    "build-sp07-via-api.py"
    "build-sp08-via-api.py"
    "build-sp11-via-api.py"
)

# Esegui ogni script
for script in "${scripts[@]}"; do
    echo "🔧 Eseguendo $script..."
    if python3 "../process-groups/$script"; then
        echo "✅ $script completato con successo"
        echo
    else
        echo "❌ ERRORE in $script"
        exit 1
    fi
done

echo "═══════════════════════════════════════════════════════════"
echo "🎉 TUTTI I PROCESSOR GROUPS COSTRUITI CON SUCCESSO!"
echo "═══════════════════════════════════════════════════════════"
echo
echo "📊 Riepilogo Processor Groups creati:"
echo "  ✅ SP01 - EML Parser (porta 9091) - già esistente"
echo "  ✅ SP02 - Document Extractor (porta 9092)"
echo "  ✅ SP03 - Procedural Classifier (porta 9093)"
echo "  ✅ SP04 - Knowledge Base (porta 9094)"
echo "  ✅ SP05 - Template Engine (porta 9095)"
echo "  ✅ SP06 - Validator (porta 9096)"
echo "  ✅ SP07 - Content Classifier (porta 9097)"
echo "  ✅ SP08 - Quality Checker (porta 9098)"
echo "  ✅ SP11 - Security Audit (porta 9101)"
echo
echo "🔗 Endpoint disponibili:"
echo "  POST http://localhost:9091/sp01 - EML Parser"
echo "  POST http://localhost:9092/sp02 - Document Extractor"
echo "  POST http://localhost:9093/sp03 - Procedural Classifier"
echo "  POST http://localhost:9094/sp04 - Knowledge Base"
echo "  POST http://localhost:9095/sp05 - Template Engine"
echo "  POST http://localhost:9096/sp06 - Validator"
echo "  POST http://localhost:9097/sp07 - Content Classifier"
echo "  POST http://localhost:9098/sp08 - Quality Checker"
echo "  POST http://localhost:9101/sp11 - Security Audit"
echo
echo "📮 Test con Postman Collection aggiornata:"
echo "   File: ZenIa_Postman_Collection.json"
echo "   Sezione: 'NiFi Flows (via ListenHTTP)'"
echo
echo "═══════════════════════════════════════════════════════════"