#!/bin/bash

###############################################################################
# Script per eseguire tutte le verifiche sulla documentazione ZenIA
#
# Utilizzo: ./run_all_checks.sh [--quick]
# Output: report/ directory con 15 file JSON
#
# TIER 1 (Critical): SP/MS References, UC Archetype, SP Completeness, Headings, Mermaid
# TIER 2 (Warnings): Sections, Language, Payload, Cross-References
# TIER 3 (Lint):    Whitespace, Images, Duplicates, README Metadata
# Legacy:           JSON, Links
###############################################################################

# Note: Non usiamo 'set -e' per permettere continuazione anche se alcuni script falliscono

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPORTS_DIR="$SCRIPT_DIR/reports"
QUICK_MODE=false

# Parsing args
if [[ "$1" == "--quick" ]]; then
    QUICK_MODE=true
fi

echo "📋 ZenIA Documentation Validation Suite (Complete)"
echo "=================================================="
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

# ============================================================================
# TIER 1: CRITICAL CHECKS (Structural)
# ============================================================================
echo ""
echo "🏗️  TIER 1 - CRITICAL STRUCTURAL CHECKS"
echo "=================================================="
echo ""

# 1. Verifica SP/MS References
echo "1️⃣  Verifica SP/MS References..."
python3 "$SCRIPT_DIR/verify_sp_references.py"
SP_RESULT=$?
echo ""

# 2. Verifica UC Archetype Completeness
echo "2️⃣  Verifica Completamento Archetipo UC..."
python3 "$SCRIPT_DIR/verify_uc_archetype.py"
UC_ARCHETYPE_RESULT=$?
echo ""

# 3. Verifica SP Completeness
echo "3️⃣  Verifica Completamento e Mappatura SP..."
python3 "$SCRIPT_DIR/verify_sp_completeness.py"
SP_COMPLETE_RESULT=$?
echo ""

# 4. Verifica Markdown Headings
echo "4️⃣  Verifica Coerenza Heading Markdown..."
python3 "$SCRIPT_DIR/verify_markdown_headings.py"
HEADING_RESULT=$?
echo ""

# 5. Verifica Mermaid Diagrams
echo "5️⃣  Verifica Validità Diagram Mermaid..."
python3 "$SCRIPT_DIR/verify_mermaid_diagrams.py"
MERMAID_RESULT=$?
echo ""

if [ "$QUICK_MODE" = true ]; then
    echo "⚡ QUICK MODE: Skipping TIER 2-3 checks"
    echo ""
else

# ============================================================================
# TIER 2: WARNING CHECKS (Content Quality)
# ============================================================================
echo ""
echo "📝 TIER 2 - CONTENT QUALITY CHECKS"
echo "=================================================="
echo ""

# 6. Verifica Section Completeness
echo "6️⃣  Verifica Completamento Sezioni SP..."
python3 "$SCRIPT_DIR/verify_section_completeness.py"
SECTION_RESULT=$?
echo ""

# 7. Verifica Language Coherence
echo "7️⃣  Verifica Coerenza Linguistica..."
python3 "$SCRIPT_DIR/verify_language_coherence.py"
LANGUAGE_RESULT=$?
echo ""

# 8. Verifica Payload Validation
echo "8️⃣  Verifica Validazione Payload JSON..."
python3 "$SCRIPT_DIR/verify_payload_validation.py"
PAYLOAD_RESULT=$?
echo ""

# 9. Verifica Cross References
echo "9️⃣  Verifica Validazione Cross-Reference..."
python3 "$SCRIPT_DIR/verify_cross_references.py"
CROSSREF_RESULT=$?
echo ""

# ============================================================================
# TIER 3: LINT CHECKS (Formatting & Metadata)
# ============================================================================
echo ""
echo "🧹 TIER 3 - FORMATTING & LINT CHECKS"
echo "=================================================="
echo ""

# 10. Verifica Whitespace
echo "🔟 Verifica Whitespace e Formattazione..."
python3 "$SCRIPT_DIR/verify_whitespace_formatting.py"
WHITESPACE_RESULT=$?
echo ""

# 11. Verifica Orphaned Images
echo "1️⃣1️⃣  Verifica Immagini Orfane..."
python3 "$SCRIPT_DIR/verify_orphaned_images.py"
IMAGE_RESULT=$?
echo ""

# 12. Verifica Content Duplicates
echo "1️⃣2️⃣  Verifica Duplicati di Contenuto..."
python3 "$SCRIPT_DIR/verify_content_duplicates.py"
DUPLICATE_RESULT=$?
echo ""

# 13. Verifica README Metadata
echo "1️⃣3️⃣  Verifica Metadati README..."
python3 "$SCRIPT_DIR/verify_readme_metadata.py"
README_RESULT=$?
echo ""

fi

# ============================================================================
# LEGACY CHECKS (Original)
# ============================================================================
echo ""
echo "📚 LEGACY CHECKS"
echo "=================================================="
echo ""

# JSON Examples
echo "🔸 Verifica JSON Examples..."
python3 "$SCRIPT_DIR/verify_json_examples.py"
JSON_RESULT=$?
echo ""

# Links
echo "🔗 Verifica Link Markdown..."
python3 "$SCRIPT_DIR/verify_links.py"
LINKS_RESULT=$?
echo ""

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "========================================"
echo "📊 SUMMARY - VALIDATION RESULTS"
echo "========================================"
echo ""

TIER1_PASS=true

# TIER 1 Results
echo "🏗️  TIER 1 (CRITICAL):"
if [ $SP_RESULT -eq 0 ]; then
    echo "  ✅ SP/MS References: OK"
else
    echo "  ❌ SP/MS References: FAIL"
    TIER1_PASS=false
fi

if [ $UC_ARCHETYPE_RESULT -eq 0 ]; then
    echo "  ✅ UC Archetype: OK"
else
    echo "  ⚠️  UC Archetype: ISSUES"
    TIER1_PASS=false
fi

if [ $SP_COMPLETE_RESULT -eq 0 ]; then
    echo "  ✅ SP Completeness: OK"
else
    echo "  ⚠️  SP Completeness: ISSUES"
    TIER1_PASS=false
fi

if [ $HEADING_RESULT -eq 0 ]; then
    echo "  ✅ Markdown Headings: OK"
else
    echo "  ⚠️  Markdown Headings: ISSUES"
fi

if [ $MERMAID_RESULT -eq 0 ]; then
    echo "  ✅ Mermaid Diagrams: OK"
else
    echo "  ⚠️  Mermaid Diagrams: WARNINGS"
fi

if [ "$QUICK_MODE" = false ]; then

# TIER 2 Results
echo ""
echo "📝 TIER 2 (CONTENT):"
if [ $SECTION_RESULT -eq 0 ]; then
    echo "  ✅ Section Completeness: OK"
else
    echo "  ⚠️  Section Completeness: ISSUES"
fi

if [ $LANGUAGE_RESULT -eq 0 ]; then
    echo "  ✅ Language Coherence: OK"
else
    echo "  ⚠️  Language Coherence: WARNINGS"
fi

if [ $PAYLOAD_RESULT -eq 0 ]; then
    echo "  ✅ Payload Validation: OK"
else
    echo "  ⚠️  Payload Validation: WARNINGS"
fi

if [ $CROSSREF_RESULT -eq 0 ]; then
    echo "  ✅ Cross-References: OK"
else
    echo "  ⚠️  Cross-References: WARNINGS"
fi

# TIER 3 Results
echo ""
echo "🧹 TIER 3 (LINT):"
if [ $WHITESPACE_RESULT -eq 0 ]; then
    echo "  ✅ Whitespace: OK"
else
    echo "  ⚠️  Whitespace: WARNINGS"
fi

if [ $IMAGE_RESULT -eq 0 ]; then
    echo "  ✅ Images: OK"
else
    echo "  ⚠️  Images: WARNINGS"
fi

if [ $DUPLICATE_RESULT -eq 0 ]; then
    echo "  ✅ Duplicates: OK"
else
    echo "  ⚠️  Duplicates: WARNINGS"
fi

if [ $README_RESULT -eq 0 ]; then
    echo "  ✅ README Metadata: OK"
else
    echo "  ⚠️  README Metadata: WARNINGS"
fi

fi

# Legacy Checks
echo ""
echo "📚 LEGACY:"
if [ $JSON_RESULT -eq 0 ]; then
    echo "  ✅ JSON Examples: OK"
else
    echo "  ⚠️  JSON Examples: ISSUES"
fi

if [ $LINKS_RESULT -eq 0 ]; then
    echo "  ✅ Links: OK"
else
    echo "  ⚠️  Links: ISSUES"
fi

echo ""
echo "📁 Report completi in: $REPORTS_DIR"
echo "   (15 file JSON con dettagli completi)"
echo ""

# ============================================================================
# FINAL DECISION
# ============================================================================
echo ""
echo "========================================"
echo "📋 FINAL DECISION"
echo "========================================"
echo ""

if [ "$TIER1_PASS" = true ]; then
    echo "✅ TIER 1 CRITICAL: PASS"
    echo "✅ Documentation is ready for commit"
    exit 0
else
    echo "❌ TIER 1 CRITICAL: FAIL"
    echo "❌ Fix critical issues before committing"
    exit 1
fi
