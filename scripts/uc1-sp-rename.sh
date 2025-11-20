#!/bin/bash

# UC1 SP File Renaming — Rimuovi prefisso duplicato "01 "
# Data: 2025-11-20
# Scopo: Rinominazione file SP da "01 SPxx - ..." a "SPxx - ..."
# Usa: git mv per preservare storico commit

set -e

UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC1 - Sistema di Gestione Documentale"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
UC_NAME="UC1"

echo "🚀 Inizio ridenominazione SP $UC_NAME..."
echo "📁 Target: $UC_PATH"
echo ""

# Verifica repo git e working tree pulito
cd "$REPO_ROOT"
git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
echo "✅ Repo git verificato"

# Controlla modifiche non committate
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  AVVISO: Modifiche non committate rilevate"
    echo "Esegui commit o stash prima di procedere"
    exit 1
fi
echo "✅ Working tree pulito"
echo ""

# Crea mappatura file SP
cat > /tmp/uc1_sp_renames.txt << 'EOF'
01 SP02 - Estrattore Documenti e Classificatore Allegati.md|SP02 - Estrattore Documenti e Classificatore Allegati.md
01 SP07 - Classificatore Contenuti.md|SP07 - Classificatore Contenuti.md
01 SP12 - Ricerca Semantica e Motore Q&A.md|SP12 - Ricerca Semantica e Motore Q&A.md
01 SP13 - Sintetizzatore Documenti.md|SP13 - Sintetizzatore Documenti.md
01 SP14 - Indicizzatore Metadati.md|SP14 - Indicizzatore Metadati.md
01 SP15 - Orchestratore Workflow Documenti.md|SP15 - Orchestratore Workflow Documenti.md
EOF

echo "📝 File SP da rinominare:"
count=0
while IFS='|' read -r old_name new_name; do
    echo "   $old_name → $new_name"
    ((count++))
done < /tmp/uc1_sp_renames.txt
echo "   Totale: $count file"
echo ""

# Valida file esistono
echo "⚠️  Validazione file..."
files_found=0
while IFS='|' read -r old_name new_name; do
    old_path="$UC_PATH/$old_name"
    if [ -f "$old_path" ]; then
        ((files_found++))
    else
        echo "❌ NON TROVATO: $old_name"
    fi
done < /tmp/uc1_sp_renames.txt

echo "✅ Trovati: $files_found / $count file"
if [ "$files_found" -ne "$count" ]; then
    echo "❌ Alcuni file mancano — abort"
    exit 1
fi
echo ""

# Esegui ridenominazioni
echo "🔄 Esecuzione operazioni git mv..."
while IFS='|' read -r old_name new_name; do
    old_path="$UC_PATH/$old_name"
    new_path="$UC_PATH/$new_name"

    if [ -f "$old_path" ]; then
        echo "   → $old_name"
        git mv "$old_path" "$new_path"
    fi
done < /tmp/uc1_sp_renames.txt

echo "✅ Ridenominazioni completate"
echo ""
echo "📊 Prossimi step:"
echo "   1. git status (revisione modifiche staged)"
echo "   2. git commit -m '...'"
