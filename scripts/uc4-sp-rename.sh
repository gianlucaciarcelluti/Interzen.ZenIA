#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC4 - BPM e Automazione Processi"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc4_sp_renames.txt << 'EOF'
01 SP24 - Motore Process Mining.md|SP24 - Motore Process Mining.md
01 SP25 - Motore Previsioni e Pianificazione Predittiva.md|SP25 - Motore Previsioni e Pianificazione Predittiva.md
01 SP26 - Progettista Workflow Intelligente.md|SP26 - Progettista Workflow Intelligente.md
01 SP27 - Analitiche Processi.md|SP27 - Analitiche Processi.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc4_sp_renames.txt
echo "✅ UC4 SP rinominati"
