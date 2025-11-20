#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC9 - Compliance & Risk Management"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc9_sp_renames.txt << 'EOF'
01 SP42 - Motore Politiche.md|SP42 - Motore Politiche.md
01 SP43 - Motore Valutazione Rischi.md|SP43 - Motore Valutazione Rischi.md
01 SP44 - Sistema Monitoraggio Conformità.md|SP44 - Sistema Monitoraggio Conformità.md
01 SP45 - Hub Intelligenza Normativa.md|SP45 - Hub Intelligenza Normativa.md
01 SP46 - Piattaforma Automazione Conformità.md|SP46 - Piattaforma Automazione Conformità.md
01 SP47 - Analitiche Conformità e Reporting.md|SP47 - Analitiche Conformità e Reporting.md
01 SP48 - Piattaforma Intelligenza Conformità.md|SP48 - Piattaforma Intelligenza Conformità.md
01 SP49 - Gestione Cambiamenti Normativi.md|SP49 - Gestione Cambiamenti Normativi.md
01 SP50 - Formazione Conformità e Certificazione.md|SP50 - Formazione Conformità e Certificazione.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc9_sp_renames.txt
echo "✅ UC9 SP rinominati"
