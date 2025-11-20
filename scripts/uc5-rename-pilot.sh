#!/bin/bash

# UC5 File Renaming Pilot Test
# Date: 2025-11-20
# Purpose: Test standardized naming convention (00-NN-NAME.md format)

set -e

UC5_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC5 - Produzione Documentale Integrata"

echo "🚀 Starting UC5 Pilot Rename Test..."
echo "📁 Target: $UC5_PATH"
echo ""

# Verify git repo
cd "/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Not in git repo"; exit 1; }
echo "✅ Git repo verified"
echo ""

# Create mapping with newline-separated pairs
cat > /tmp/uc5_renames.txt << 'EOF'
00 Architettura Generale Microservizi.md|00-ARCHITECTURE.md
02 Sottoprogetti con Pipeline Operative.md|01-OVERVIEW.md
02 Matrice Dipendenze Sottoprogetti.md|02-DEPENDENCIES.md
03 Human in the Loop (HITL).md|05-HITL.md
Guida_Generazione_Atti_Amministrativi.md|04-GUIDE.md
TEMPLATE_SP_STRUCTURE.md|TEMPLATE-SP-STRUCTURE.md
01 CANONICAL - Generazione Atto Completo.md|SUPPLEMENTARY/CANONICAL-Complete-Flow.md
02 SUPPLEMENTARY - Overview Semplificato.md|SUPPLEMENTARY/OVERVIEW-Simplified.md
03 SUPPLEMENTARY - Ultra Semplificato.md|SUPPLEMENTARY/OVERVIEW-Ultra-Simplified.md
EOF

echo "📝 Files to rename:"
while IFS='|' read -r old_name new_name; do
    echo "   $old_name → $new_name"
done < /tmp/uc5_renames.txt
echo ""

# Create SUPPLEMENTARY dir if needed
if [ ! -d "$UC5_PATH/SUPPLEMENTARY" ]; then
    echo "📂 Creating SUPPLEMENTARY directory..."
    mkdir -p "$UC5_PATH/SUPPLEMENTARY"
fi
echo ""

echo "⚠️  DRY-RUN MODE: Validating files..."
echo ""

files_found=0
while IFS='|' read -r old_name new_name; do
    old_path="$UC5_PATH/$old_name"

    if [ -f "$old_path" ]; then
        echo "✅ Found: $old_name"
        ((files_found++))
    else
        echo "❌ NOT FOUND: $old_name"
    fi
done < /tmp/uc5_renames.txt

echo ""
echo "📊 Summary: $files_found / 9 files validated"
echo ""

if [ "$files_found" -eq 9 ]; then
    echo "✅ PILOT TEST SUCCESSFUL!"
    echo ""
    echo "Next: Run actual renames with:"
    echo "  bash scripts/uc5-rename-actual.sh"
else
    echo "⚠️  Some files missing — check paths above"
    exit 1
fi

echo ""
