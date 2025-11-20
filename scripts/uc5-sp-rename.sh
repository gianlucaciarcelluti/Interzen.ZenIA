#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC5 - Produzione Documentale Integrata"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc5_sp_renames.txt << 'EOF'
01 SP01 - Parser EML e Intelligenza Email.md|SP01 - Parser EML e Intelligenza Email.md
01 SP02 - Estrattore Documenti e Classificatore Allegati.md|SP02 - Estrattore Documenti e Classificatore Allegati.md
01 SP03 - Classificatore Procedurale.md|SP03 - Classificatore Procedurale.md
01 SP04 - Base Conoscenze.md|SP04 - Base Conoscenze.md
01 SP05 - Motore Template.md|SP05 - Motore Template.md
01 SP06 - Validatore.md|SP06 - Validatore.md
01 SP07 - Classificatore Contenuti.md|SP07 - Classificatore Contenuti.md
01 SP08 - Verificatore Qualità.md|SP08 - Verificatore Qualità.md
01 SP09 - Motore Workflow.md|SP09 - Motore Workflow.md
01 SP10 - Pannello di Controllo.md|SP10 - Pannello di Controllo.md
01 SP11 - Sicurezza e Audit.md|SP11 - Sicurezza e Audit.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc5_sp_renames.txt
echo "✅ UC5 SP rinominati"
