#!/bin/bash

###############################################################################
# Script per eseguire tutte le verifiche sulla documentazione ZenIA
#
# Utilizzo: ./run_all_checks.sh [--quick] [--verbose]
# Output: report/ directory con 15 file JSON
#
# TIER 1 (Critical): SP/MS References, UC Archetype, SP Completeness, Headings, Mermaid
# TIER 2 (Warnings): Sections, Language, Payload, Cross-References
# TIER 3 (Lint):    Whitespace, Images, Duplicates, README Metadata
###############################################################################

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPORTS_DIR="$SCRIPT_DIR/reports"
QUICK_MODE=false
VERBOSE=false

# Parsing args
[[ "$1" == "--quick" ]] && QUICK_MODE=true
[[ "$1" == "--verbose" || "$2" == "--verbose" ]] && VERBOSE=true

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Track failed checks for final report
declare -a FAILED_CHECKS=()
declare -a FAILED_REPORTS=()
declare -a ISSUES_CHECKS=()
declare -a ISSUES_REPORTS=()
OVERALL_PASS=true

# Helper to map check name to report file
get_report_file() {
    local check_name="$1"
    case "$check_name" in
        "SP/MS References") echo "sp_ms_references.json" ;;
        "UC Archetype") echo "uc_archetype_validation.json" ;;
        "SP Completeness") echo "sp_completeness_validation.json" ;;
        "System Cards") echo "system_cards_validation.json" ;;
        "Markdown Headings") echo "markdown_headings_validation.json" ;;
        "Mermaid Diagrams") echo "mermaid_diagrams_validation.json" ;;
        "Section Completeness") echo "section_completeness_validation.json" ;;
        "Language Coherence") echo "language_coherence_validation.json" ;;
        "Payload Validation") echo "payload_validation.json" ;;
        "Cross-References") echo "cross_references_validation.json" ;;
        "Whitespace") echo "whitespace_formatting_validation.json" ;;
        "Orphaned Images") echo "orphaned_images_validation.json" ;;
        "Content Duplicates") echo "content_duplicates_validation.json" ;;
        "README Metadata") echo "readme_metadata_validation.json" ;;
        "JSON Examples") echo "json_validation.json" ;;
        "Links") echo "links_validation.json" ;;
        *) echo "unknown.json" ;;
    esac
}

# Helper functions
run_check() {
    local check_num=$1
    local check_name=$2
    local script=$3

    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}${check_num}${NC} ${check_name}..."
        output=$(python3 "$SCRIPT_DIR/$script" 2>&1)
        result=$?
        # print captured output so verbose mode shows details
        echo "$output"

        # If the check returned non-zero, mark overall as failed and record
        if [ $result -ne 0 ]; then
            OVERALL_PASS=false
            FAILED_CHECKS+=("$check_name")
            FAILED_REPORTS+=("$(get_report_file "$check_name")")
            return $result
        fi

        # also analyze the output for explicit error counts or error keywords
        if echo "$output" | grep -q "ERRORI TROVATI\|NEEDS WORK\|FAIL"; then
            OVERALL_PASS=false
            FAILED_CHECKS+=("$check_name")
            FAILED_REPORTS+=("$(get_report_file "$check_name")")
        else
            count_errors=$(echo "$output" | grep -i 'errori' | grep -oE '[0-9]+' | awk '{sum+=$1} END{print sum+0}')
            if [ -n "$count_errors" ] && [ "$count_errors" -gt 0 ]; then
                OVERALL_PASS=false
                FAILED_CHECKS+=("$check_name")
                FAILED_REPORTS+=("$(get_report_file "$check_name")")
            fi
        fi

        return $result
    else
        echo -ne "${BLUE}${check_num}${NC} ${check_name}... "
        output=$(python3 "$SCRIPT_DIR/$script" 2>&1)
        result=$?

        # Extract status from output
        # If the output contains explicit error keywords treat as failure
        if echo "$output" | grep -q "ERRORI TROVATI\|NEEDS WORK\|FAIL"; then
            echo -e "${RED}⚠️${NC}"
            FAILED_CHECKS+=("$check_name")
            FAILED_REPORTS+=("$(get_report_file "$check_name")")
            OVERALL_PASS=false
        else
            # detect explicit numeric error counts (e.g. "Errori: 13" or "ERRORI totali: 13")
            count_errors=$(echo "$output" | grep -i 'errori' | grep -oE '[0-9]+' | awk '{sum+=$1} END{print sum+0}')
            if [ -n "$count_errors" ] && [ "$count_errors" -gt 0 ]; then
                echo -e "${RED}⚠️${NC}"
                FAILED_CHECKS+=("$check_name")
                FAILED_REPORTS+=("$(get_report_file "$check_name")")
                OVERALL_PASS=false
            elif echo "$output" | grep -q "PERFECT\|EXCELLENT\|VALID\|PASS\|OK\|NESSUN\|ALL VALID"; then
                echo -e "${GREEN}✅${NC}"
            elif echo "$output" | grep -q "ISSUES FOUND\|NEEDS ATTENTION\|⚠️\|WARNING\|WARN"; then
                echo -e "${YELLOW}~${NC}"
                ISSUES_CHECKS+=("$check_name")
                ISSUES_REPORTS+=("$(get_report_file "$check_name")")
            else
                echo -e "${YELLOW}~${NC}"
                ISSUES_CHECKS+=("$check_name")
                ISSUES_REPORTS+=("$(get_report_file "$check_name")")
            fi
        fi
        # If the script returned non-zero, treat as failure even if output didn't include keywords
        if [ $result -ne 0 ]; then
            OVERALL_PASS=false
            # avoid double-adding the same failed check
            if ! printf "%s\n" "${FAILED_CHECKS[@]}" | grep -Fxq "$check_name"; then
                FAILED_CHECKS+=("$check_name")
                FAILED_REPORTS+=("$(get_report_file "$check_name")")
            fi
        fi
        return $result
    fi
}

# Helper to show report paths
show_report_hint() {
    echo ""
    echo -e "${CYAN}📁 View detailed reports:${NC}"

    if [ ${#FAILED_CHECKS[@]} -gt 0 ]; then
        echo ""
        echo -e "${RED}❌ Critical Issues:${NC}"
        for i in "${!FAILED_CHECKS[@]}"; do
            echo "   • ${FAILED_CHECKS[$i]}"
            echo "     ${CYAN}→ cat scripts/reports/${FAILED_REPORTS[$i]}${NC}"
        done
    fi

    if [ ${#ISSUES_CHECKS[@]} -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}⚠️ Warnings:${NC}"
        for i in "${!ISSUES_CHECKS[@]}"; do
            echo "   • ${ISSUES_CHECKS[$i]}"
            echo "     ${CYAN}→ cat scripts/reports/${ISSUES_REPORTS[$i]}${NC}"
        done
    fi
}

# Header
if [ "$VERBOSE" = true ]; then
    echo "📋 ZenIA Documentation Validation Suite"
    echo "========================================"
    echo "Mode: VERBOSE"
    echo ""
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trovato"
    exit 1
fi

mkdir -p "$REPORTS_DIR"

# ============================================================================
# TIER 1: CRITICAL CHECKS
# ============================================================================
if [ "$VERBOSE" = false ]; then
    echo "🏗️  TIER 1 (Critical):"
fi

run_check "1️⃣" "SP/MS References" "verify_sp_references.py"
SP_RESULT=$?

run_check "2️⃣" "UC Archetype" "verify_uc_archetype.py"
UC_ARCHETYPE_RESULT=$?

run_check "3️⃣" "SP Completeness" "verify_sp_completeness.py"
SP_COMPLETE_RESULT=$?

run_check "3️⃣ᵇ" "System Cards" "verify_system_cards.py"
SYSTEM_CARDS_RESULT=$?

run_check "4️⃣" "Markdown Headings" "verify_markdown_headings.py"
HEADING_RESULT=$?

run_check "5️⃣" "Mermaid Diagrams" "verify_mermaid_diagrams.py"
MERMAID_RESULT=$?

if [ "$VERBOSE" = false ]; then
    echo ""
fi

TIER1_PASS=true
[ $SP_RESULT -ne 0 ] && TIER1_PASS=false
[ $UC_ARCHETYPE_RESULT -ne 0 ] && TIER1_PASS=false
[ $SP_COMPLETE_RESULT -ne 0 ] && TIER1_PASS=false

# TIER 2: CONTENT QUALITY CHECKS
if [ "$QUICK_MODE" = false ]; then
    if [ "$VERBOSE" = false ]; then
        echo "📝 TIER 2 (Content):"
    fi

    run_check "6️⃣" "Section Completeness" "verify_section_completeness.py"
    SECTION_RESULT=$?

    run_check "7️⃣" "Language Coherence" "verify_language_coherence.py"
    LANGUAGE_RESULT=$?

    run_check "8️⃣" "Payload Validation" "verify_payload_validation.py"
    PAYLOAD_RESULT=$?

    run_check "9️⃣" "Cross-References" "verify_cross_references.py"
    CROSSREF_RESULT=$?

    if [ "$VERBOSE" = false ]; then
        echo ""
        echo "🧹 TIER 3 (Lint):"
    fi

    # TIER 3: LINT CHECKS
    run_check "🔟" "Whitespace" "verify_whitespace_formatting.py"
    WHITESPACE_RESULT=$?

    run_check "1️⃣ 1️⃣" "Orphaned Images" "verify_orphaned_images.py"
    IMAGE_RESULT=$?

    run_check "1️⃣ 2️⃣" "Content Duplicates" "verify_content_duplicates.py"
    DUPLICATE_RESULT=$?

    run_check "1️⃣ 3️⃣" "README Metadata" "verify_readme_metadata.py"
    README_RESULT=$?

    if [ "$VERBOSE" = false ]; then
        echo ""
    fi
fi

# LEGACY CHECKS
if [ "$VERBOSE" = false ]; then
    echo "📚 Legacy:"
fi

run_check "🔸" "JSON Examples" "verify_json_examples.py"
JSON_RESULT=$?

run_check "🔗" "Links" "verify_links.py"
LINKS_RESULT=$?

# ============================================================================
# FINAL DECISION
# ============================================================================
if [ "$VERBOSE" = false ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

# Decide final exit code based on overall pass state and TIER1
if [ "$TIER1_PASS" = true ]; then
    if [ "$VERBOSE" = false ]; then
        echo -e "${GREEN}✅ TIER 1 PASS${NC} - Documentation ready for commit"
    else
        echo ""
        echo "✅ TIER 1 CRITICAL: PASS"
        echo "✅ Documentation is ready for commit"
    fi
else
    if [ "$VERBOSE" = false ]; then
        echo -e "${RED}❌ TIER 1 FAIL${NC} - Fix critical issues before committing"
    else
        echo ""
        echo "❌ TIER 1 CRITICAL: FAIL"
        echo "❌ Fix critical issues before committing"
    fi
fi

# If any check reported failure or returned non-zero, exit with non-zero
if [ "$OVERALL_PASS" = true ]; then
    # Show hint if there are warnings
    if [ ${#ISSUES_CHECKS[@]} -gt 0 ] && [ "$VERBOSE" = false ]; then
        show_report_hint
    fi
    exit 0
else
    if [ "$VERBOSE" = false ]; then
        show_report_hint
    fi
    exit 1
fi
