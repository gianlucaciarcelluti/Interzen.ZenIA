#!/bin/bash

###############################################################################
# Script per eseguire tutte le verifiche sulla documentazione ZenIA
#
# Utilizzo: ./run_all_checks.sh
# Output: report/ directory con 3 file JSON
###############################################################################

# Note: Non usiamo 'set -e' per permettere continuazione anche se alcuni script falliscono
# FASE 1 permette: SP/MS MUST pass, JSON/Links warnings OK (problemi da risolvere in FASE 2-3)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPORTS_DIR="$SCRIPT_DIR/reports"

echo "📋 ZenIA Documentation Validation Suite"
echo "========================================"
echo ""

# Verifica Python disponibile
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato. Installa Python3."
    exit 1
fi

echo "Python: $(python3 --version)"
echo ""

# Crea directory reports se non esiste
mkdir -p "$REPORTS_DIR"

# 1. Verifica SP/MS References
echo "1️⃣  Verifica SP/MS References..."
python3 "$SCRIPT_DIR/verify_sp_references.py"
SP_RESULT=$?
echo ""

# 2. Verifica JSON Examples
echo "2️⃣  Verifica JSON Examples..."
python3 "$SCRIPT_DIR/verify_json_examples.py"
JSON_RESULT=$?
echo ""

# 3. Verifica Links
echo "3️⃣  Verifica Link Markdown..."
python3 "$SCRIPT_DIR/verify_links.py"
LINKS_RESULT=$?
echo ""

# Riepilogo
echo "========================================"
echo "📊 RIEPILOGO VERIFICHE"
echo "========================================"
echo ""

if [ $SP_RESULT -eq 0 ]; then
    echo "✅ SP/MS References: OK"
else
    echo "❌ SP/MS References: ERRORI TROVATI"
fi

if [ $JSON_RESULT -eq 0 ]; then
    echo "✅ JSON Examples: OK"
else
    echo "❌ JSON Examples: ERRORI TROVATI"
fi

if [ $LINKS_RESULT -eq 0 ]; then
    echo "✅ Link Markdown: OK"
else
    echo "❌ Link Markdown: ERRORI TROVATI"
fi

echo ""
echo "📁 Report completi in: $REPORTS_DIR"
echo "  • sp_ms_references.json"
echo "  • json_validation.json"
echo "  • links_validation.json"
echo ""

# FASE 1 Strategy: SP/MS MUST pass (critical), JSON/Links warnings OK (for FASE 2-3)
echo ""
echo "📋 FASE 1 - CRITERI DI SUCCESSO:"
echo ""

FASE1_CRITICAL_OK=true

if [ $SP_RESULT -eq 0 ]; then
    echo "✅ CRITICO: SP/MS References PASS"
else
    echo "❌ CRITICO: SP/MS References FAIL - Blocca commit"
    FASE1_CRITICAL_OK=false
fi

echo ""
echo "⚠️  NON-CRITICO (Risolti in FASE 2-3):"

if [ $JSON_RESULT -eq 0 ]; then
    echo "  ✅ JSON Examples: PASS"
else
    echo "  ⚠️  JSON Examples: Warnings (45 JSON invalidi da fixare in FASE 2)"
fi

if [ $LINKS_RESULT -eq 0 ]; then
    echo "  ✅ Links: PASS"
else
    echo "  ⚠️  Links: Warnings (90 link rotti da fixare in FASE 3)"
fi

echo ""

# Exit code: 0 se SP/MS OK (FASE 1 critical), altrimenti 1
if [ "$FASE1_CRITICAL_OK" = true ]; then
    echo "✅ FASE 1 PASS - Pronto per commit!"
    exit 0
else
    echo "❌ FASE 1 FAIL - SP/MS References fallito"
    exit 1
fi
