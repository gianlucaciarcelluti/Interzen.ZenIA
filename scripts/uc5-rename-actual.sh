#!/bin/bash

# UC5 File Renaming - ACTUAL EXECUTION
# Date: 2025-11-20
# Purpose: Execute standardized naming convention (00-NN-NAME.md format)
# Uses: git mv to preserve commit history

set -e

UC5_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC5 - Produzione Documentale Integrata"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"

echo "🚀 Starting UC5 Actual Rename Execution..."
echo "📁 Target: $UC5_PATH"
echo ""

# Verify git repo and clean working tree
cd "$REPO_ROOT"
git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Not in git repo"; exit 1; }
echo "✅ Git repo verified"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  WARNING: Uncommitted changes detected"
    echo "Please commit or stash changes before proceeding"
    exit 1
fi
echo "✅ Working tree is clean"
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

echo "📝 Files to rename (from pilot test):"
while IFS='|' read -r old_name new_name; do
    echo "   $old_name → $new_name"
done < /tmp/uc5_renames.txt
echo ""

# Validate all files exist before starting renames
echo "⚠️  Validating files exist..."
files_found=0
files_missing=0
while IFS='|' read -r old_name new_name; do
    old_path="$UC5_PATH/$old_name"

    if [ -f "$old_path" ]; then
        ((files_found++))
    else
        echo "❌ NOT FOUND: $old_name"
        ((files_missing++))
    fi
done < /tmp/uc5_renames.txt

echo "✅ Found: $files_found / 9 files"
if [ "$files_missing" -gt 0 ]; then
    echo "❌ Missing: $files_missing files — aborting"
    exit 1
fi
echo ""

# Create SUPPLEMENTARY directory if needed
if [ ! -d "$UC5_PATH/SUPPLEMENTARY" ]; then
    echo "📂 Creating SUPPLEMENTARY directory..."
    mkdir -p "$UC5_PATH/SUPPLEMENTARY"
    echo "✅ SUPPLEMENTARY directory created"
fi
echo ""

# Execute git mv operations
echo "🔄 Executing git mv operations..."
files_renamed=0
while IFS='|' read -r old_name new_name; do
    old_path="$UC5_PATH/$old_name"
    new_path="$UC5_PATH/$new_name"

    if [ -f "$old_path" ]; then
        echo "   → Moving: $old_name"
        git mv "$old_path" "$new_path"
        ((files_renamed++))
    fi
done < /tmp/uc5_renames.txt

echo "✅ Renamed: $files_renamed / 9 files"
echo ""

# Verify renames completed
echo "📊 Verification:"
renamed_verified=0
while IFS='|' read -r old_name new_name; do
    new_path="$UC5_PATH/$new_name"

    if [ -f "$new_path" ]; then
        echo "✅ Verified: $new_name"
        ((renamed_verified++))
    else
        echo "❌ VERIFY FAILED: $new_name"
    fi
done < /tmp/uc5_renames.txt

echo ""
if [ "$renamed_verified" -eq 9 ]; then
    echo "✅ ALL RENAMES SUCCESSFUL!"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Update UC5/README.md with new file paths"
    echo "  2. Run: git status (review staged changes)"
    echo "  3. Run: git commit -m '...'"
    echo "  4. Run: bash scripts/uc1-rename-actual.sh (repeat for other UCs)"
    echo ""
else
    echo "⚠️  VERIFICATION FAILED — $((9 - renamed_verified)) files not found"
    exit 1
fi
