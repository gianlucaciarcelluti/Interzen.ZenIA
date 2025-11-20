#!/bin/bash
set -e
UC_PATH="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/docs/use_cases/UC11 - Analisi Dati e Reporting"
REPO_ROOT="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA"
cd "$REPO_ROOT" && git rev-parse --git-dir > /dev/null 2>&1 || { echo "❌ Non in repo git"; exit 1; }
if ! git diff-index --quiet HEAD --; then echo "⚠️  Modifiche non committate"; exit 1; fi
cat > /tmp/uc11_sp_renames.txt << 'EOF'
01 SP58 - Data Lake e Gestione Archiviazione.md|SP58 - Data Lake e Gestione Archiviazione.md
01 SP59 - Pipeline ETL e Elaborazione Dati.md|SP59 - Pipeline ETL e Elaborazione Dati.md
01 SP60 - Analitiche Avanzate e Machine Learning.md|SP60 - Analitiche Avanzate e Machine Learning.md
01 SP61 - Portale Analitiche Self-Service.md|SP61 - Portale Analitiche Self-Service.md
01 SP62 - Qualità Dati e Governance.md|SP62 - Qualità Dati e Governance.md
01 SP63 - Analitiche Real-Time e Streaming.md|SP63 - Analitiche Real-Time e Streaming.md
01 SP64 - Analitiche Predittive e Previsioni.md|SP64 - Analitiche Predittive e Previsioni.md
01 SP65 - Monitoraggio Prestazioni e Avvisi.md|SP65 - Monitoraggio Prestazioni e Avvisi.md
01 SP66 - Sicurezza Dati e Conformità.md|SP66 - Sicurezza Dati e Conformità.md
01 SP67 - Gateway API e Livello Integrazione.md|SP67 - Gateway API e Livello Integrazione.md
01 SP68 - DevOps e Pipeline CI CD.md|SP68 - DevOps e Pipeline CI CD.md
01 SP69 - Disaster Recovery e Continuità Aziendale.md|SP69 - Disaster Recovery e Continuità Aziendale.md
01 SP70 - Gestione Conformità e Audit.md|SP70 - Gestione Conformità e Audit.md
01 SP71 - Ottimizzazione Prestazioni e Scalabilità.md|SP71 - Ottimizzazione Prestazioni e Scalabilità.md
01 SP72 - Gestione Incidenti e Escalation.md|SP72 - Gestione Incidenti e Escalation.md
EOF
while IFS='|' read -r old_name new_name; do
    [ -f "$UC_PATH/$old_name" ] && git mv "$UC_PATH/$old_name" "$UC_PATH/$new_name"
done < /tmp/uc11_sp_renames.txt
echo "✅ UC11 SP rinominati"
