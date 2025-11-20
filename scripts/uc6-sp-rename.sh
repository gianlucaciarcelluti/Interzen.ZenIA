#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC6 - Firma Digitale Integrata"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc6_sp_renames.txt << 'EOF'
01 SP29 - Motore Firma Digitale.md|SP29 - Motore Firma Digitale.md
01 SP30 - Gestore Certificati.md|SP30 - Gestore Certificati.md
01 SP31 - Workflow Firma.md|SP31 - Workflow Firma.md
01 SP32 - Autorità Timestamp e Marcatura Temporale.md|SP32 - Autorità Timestamp e Marcatura Temporale.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc6_sp_renames.txt
echo "✅ UC6 SP rinominati"
