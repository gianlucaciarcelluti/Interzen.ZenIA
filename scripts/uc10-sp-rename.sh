#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC10 - Supporto all'Utente"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc10_sp_renames.txt << 'EOF'
01 SP51 - Sistema Help Desk.md|SP51 - Sistema Help Desk.md
01 SP52 - Gestione Base Conoscenze.md|SP52 - Gestione Base Conoscenze.md
01 SP53 - Assistente Virtuale e Chatbot.md|SP53 - Assistente Virtuale e Chatbot.md
01 SP54 - Piattaforma Formazione Utenti.md|SP54 - Piattaforma Formazione Utenti.md
01 SP55 - Portale Self-Service.md|SP55 - Portale Self-Service.md
01 SP56 - Analitiche Supporto e Reporting.md|SP56 - Analitiche Supporto e Reporting.md
01 SP57 - Gestione Feedback Utenti.md|SP57 - Gestione Feedback Utenti.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc10_sp_renames.txt
echo "✅ UC10 SP rinominati"
