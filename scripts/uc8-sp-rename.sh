#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC8 - Integrazione con SIEM (Sicurezza Informatica)"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc8_sp_renames.txt << 'EOF'
01 SP38 - Collettore SIEM.md|SP38 - Collettore SIEM.md
01 SP39 - Elaboratore SIEM.md|SP39 - Elaboratore SIEM.md
01 SP40 - Archiviazione SIEM.md|SP40 - Archiviazione SIEM.md
01 SP41 - Analitiche SIEM e Reporting.md|SP41 - Analitiche SIEM e Reporting.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc8_sp_renames.txt
echo "✅ UC8 SP rinominati"
