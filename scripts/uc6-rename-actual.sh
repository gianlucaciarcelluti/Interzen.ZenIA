#!/bin/bash

# UC6 File Renaming - ACTUAL EXECUTION
# Date: 2025-11-20
# Purpose: Execute standardized naming convention (00-NN-NAME.md format)
# Uses: git mv to preserve commit history

set -e

UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC6 - Firma Digitale Integrata"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
UC_NAME="UC6"

echo "🚀 Starting $UC_NAME Actual Rename Execution..."
echo "📁 Target: $UC_PATH"
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
# Pattern: Old Name|New Name
cat > /tmp/uc6_renames.txt << 'EOF'
00 Architettura UC6.md|00-ARCHITECTURE.md
01 Sequence diagrams.md|03-SEQUENCES.md
02 Matrice Dipendenze.md|02-DEPENDENCIES.md
Guida_UC6_Firma_Digitale.md|04-GUIDE.md
EOF

echo "📝 Files to rename:"
while IFS='|' read -r old_name new_name; do
    echo "   $old_name → $new_name"
done < /tmp/uc6_renames.txt
echo ""

# Validate all files exist before starting renames
echo "⚠️  Validating files exist..."
files_found=0
files_missing=0
while IFS='|' read -r old_name new_name; do
    old_path="$UC_PATH/$old_name"

    if [ -f "$old_path" ]; then
        ((files_found++))
    else
        echo "❌ NOT FOUND: $old_name"
        ((files_missing++))
    fi
done < /tmp/uc6_renames.txt

echo "✅ Found: $files_found / 4 files"
if [ "$files_missing" -gt 0 ]; then
    echo "❌ Missing: $files_missing files — aborting"
    exit 1
fi
echo ""

# Execute git mv operations
echo "🔄 Executing git mv operations..."
files_renamed=0
while IFS='|' read -r old_name new_name; do
    old_path="$UC_PATH/$old_name"
    new_path="$UC_PATH/$new_name"

    if [ -f "$old_path" ]; then
        echo "   → Moving: $old_name"
        git mv "$old_path" "$new_path"
        ((files_renamed++))
    fi
done < /tmp/uc6_renames.txt

echo "✅ Renamed: $files_renamed / 4 files"
echo ""

# Verify renames completed
echo "📊 Verification:"
renamed_verified=0
while IFS='|' read -r old_name new_name; do
    new_path="$UC_PATH/$new_name"

    if [ -f "$new_path" ]; then
        echo "✅ Verified: $new_name"
        ((renamed_verified++))
    else
        echo "❌ VERIFY FAILED: $new_name"
    fi
done < /tmp/uc6_renames.txt

echo ""
if [ "$renamed_verified" -eq 4 ]; then
    echo "✅ ALL RENAMES SUCCESSFUL!"
    echo ""
    echo "📋 Next steps:"
    echo "  1. Update $UC_NAME/README.md with new file paths"
    echo "  2. Run: git status (review staged changes)"
    echo "  3. Run: git commit -m '...'"
    echo ""
else
    echo "⚠️  VERIFICATION FAILED — $((4 - renamed_verified)) files not found"
    exit 1
fi
