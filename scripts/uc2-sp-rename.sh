#!/bin/bash
# UC2 SP File Renaming — Rimuovi prefisso duplicato "01 "
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC2 - Protocollo Informatico"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi

cat > /tmp/uc2_sp_renames.txt << 'EOF'
01 SP01 - Parser EML e Intelligenza Email (Protocollo UC2).md|SP01 - Parser EML e Intelligenza Email (Protocollo UC2).md
01 SP16 - Classificatore Corrispondenza.md|SP16 - Classificatore Corrispondenza.md
01 SP17 - Suggeritore Registro.md|SP17 - Suggeritore Registro.md
01 SP18 - Rilevatore Anomalie.md|SP18 - Rilevatore Anomalie.md
01 SP19 - Orchestratore Workflow Protocollo.md|SP19 - Orchestratore Workflow Protocollo.md
EOF

while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc2_sp_renames.txt
echo "✅ UC2 SP rinominati"
