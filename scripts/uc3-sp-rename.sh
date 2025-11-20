#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC3 - Governance (Organigramma, Procedimenti, Procedure)"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc3_sp_renames.txt << 'EOF'
01 SP20 - Gestione Organigramma.md|SP20 - Gestione Organigramma.md
01 SP21 - Gestore Procedure.md|SP21 - Gestore Procedure.md
01 SP22 - Governance Processi.md|SP22 - Governance Processi.md
01 SP23 - Monitor Conformità.md|SP23 - Monitor Conformità.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc3_sp_renames.txt
echo "✅ UC3 SP rinominati"
