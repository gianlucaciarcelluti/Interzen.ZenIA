#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC7 - Sistema di Gestione Archivio e Conservazione"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc7_sp_renames.txt << 'EOF'
01 SP33 - Gestore Archivio.md|SP33 - Gestore Archivio.md
01 SP34 - Motore Conservazione.md|SP34 - Motore Conservazione.md
01 SP35 - Validatore Integrità.md|SP35 - Validatore Integrità.md
01 SP36 - Ottimizzatore Archiviazione.md|SP36 - Ottimizzatore Archiviazione.md
01 SP37 - Gestore Metadati Archivio.md|SP37 - Gestore Metadati Archivio.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc7_sp_renames.txt
echo "✅ UC7 SP rinominati"
