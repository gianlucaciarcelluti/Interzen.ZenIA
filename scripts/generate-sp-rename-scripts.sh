#!/bin/bash

# Generator Script — Crea script ridenominazione SP per tutti gli UC
# Genera automaticamente UC2-UC11 SP rename scripts basato su template UC1

SCRIPT_DIR="/Users/giangioiz/Documents/GitHub/Interzen/Interzen.ZenIA/scripts"

# Definisci mappature SP per ogni UC
# Formato: UC_NUM|UC_NAME|SP_FILES_MAPPING

cat > /tmp/uc_sp_mappings.txt << 'EOF'
2|Protocollo Informatico|01 SP01 - Parser EML e Intelligenza Email (Protocollo UC2).md|SP01 - Parser EML e Intelligenza Email (Protocollo UC2).md
2|Protocollo Informatico|01 SP16 - Classificatore Corrispondenza.md|SP16 - Classificatore Corrispondenza.md
2|Protocollo Informatico|01 SP17 - Suggeritore Registro.md|SP17 - Suggeritore Registro.md
2|Protocollo Informatico|01 SP18 - Rilevatore Anomalie.md|SP18 - Rilevatore Anomalie.md
2|Protocollo Informatico|01 SP19 - Orchestratore Workflow Protocollo.md|SP19 - Orchestratore Workflow Protocollo.md
3|Governance (Organigramma, Procedimenti, Procedure)|01 SP20 - Gestione Organigramma.md|SP20 - Gestione Organigramma.md
3|Governance (Organigramma, Procedimenti, Procedure)|01 SP21 - Gestore Procedure.md|SP21 - Gestore Procedure.md
3|Governance (Organigramma, Procedimenti, Procedure)|01 SP22 - Governance Processi.md|SP22 - Governance Processi.md
3|Governance (Organigramma, Procedimenti, Procedure)|01 SP23 - Monitor Conformità.md|SP23 - Monitor Conformità.md
4|BPM e Automazione Processi|01 SP24 - Motore Process Mining.md|SP24 - Motore Process Mining.md
4|BPM e Automazione Processi|01 SP25 - Motore Previsioni e Pianificazione Predittiva.md|SP25 - Motore Previsioni e Pianificazione Predittiva.md
4|BPM e Automazione Processi|01 SP26 - Progettista Workflow Intelligente.md|SP26 - Progettista Workflow Intelligente.md
4|BPM e Automazione Processi|01 SP27 - Analitiche Processi.md|SP27 - Analitiche Processi.md
5|Produzione Documentale Integrata|01 SP01 - Parser EML e Intelligenza Email.md|SP01 - Parser EML e Intelligenza Email.md
5|Produzione Documentale Integrata|01 SP02 - Estrattore Documenti e Classificatore Allegati.md|SP02 - Estrattore Documenti e Classificatore Allegati.md
5|Produzione Documentale Integrata|01 SP03 - Classificatore Procedurale.md|SP03 - Classificatore Procedurale.md
5|Produzione Documentale Integrata|01 SP04 - Base Conoscenze.md|SP04 - Base Conoscenze.md
5|Produzione Documentale Integrata|01 SP05 - Motore Template.md|SP05 - Motore Template.md
5|Produzione Documentale Integrata|01 SP06 - Validatore.md|SP06 - Validatore.md
5|Produzione Documentale Integrata|01 SP07 - Classificatore Contenuti.md|SP07 - Classificatore Contenuti.md
5|Produzione Documentale Integrata|01 SP08 - Verificatore Qualità.md|SP08 - Verificatore Qualità.md
5|Produzione Documentale Integrata|01 SP09 - Motore Workflow.md|SP09 - Motore Workflow.md
5|Produzione Documentale Integrata|01 SP10 - Pannello di Controllo.md|SP10 - Pannello di Controllo.md
5|Produzione Documentale Integrata|01 SP11 - Sicurezza e Audit.md|SP11 - Sicurezza e Audit.md
6|Firma Digitale Integrata|01 SP29 - Motore Firma Digitale.md|SP29 - Motore Firma Digitale.md
6|Firma Digitale Integrata|01 SP30 - Gestore Certificati.md|SP30 - Gestore Certificati.md
6|Firma Digitale Integrata|01 SP31 - Workflow Firma.md|SP31 - Workflow Firma.md
6|Firma Digitale Integrata|01 SP32 - Autorità Timestamp e Marcatura Temporale.md|SP32 - Autorità Timestamp e Marcatura Temporale.md
7|Sistema di Gestione Archivio e Conservazione|01 SP33 - Gestore Archivio.md|SP33 - Gestore Archivio.md
7|Sistema di Gestione Archivio e Conservazione|01 SP34 - Motore Conservazione.md|SP34 - Motore Conservazione.md
7|Sistema di Gestione Archivio e Conservazione|01 SP35 - Validatore Integrità.md|SP35 - Validatore Integrità.md
7|Sistema di Gestione Archivio e Conservazione|01 SP36 - Ottimizzatore Archiviazione.md|SP36 - Ottimizzatore Archiviazione.md
7|Sistema di Gestione Archivio e Conservazione|01 SP37 - Gestore Metadati Archivio.md|SP37 - Gestore Metadati Archivio.md
8|Integrazione con SIEM (Sicurezza Informatica)|01 SP38 - Collettore SIEM.md|SP38 - Collettore SIEM.md
8|Integrazione con SIEM (Sicurezza Informatica)|01 SP39 - Elaboratore SIEM.md|SP39 - Elaboratore SIEM.md
8|Integrazione con SIEM (Sicurezza Informatica)|01 SP40 - Archiviazione SIEM.md|SP40 - Archiviazione SIEM.md
8|Integrazione con SIEM (Sicurezza Informatica)|01 SP41 - Analitiche SIEM e Reporting.md|SP41 - Analitiche SIEM e Reporting.md
9|Compliance & Risk Management|01 SP42 - Motore Politiche.md|SP42 - Motore Politiche.md
9|Compliance & Risk Management|01 SP43 - Motore Valutazione Rischi.md|SP43 - Motore Valutazione Rischi.md
9|Compliance & Risk Management|01 SP44 - Sistema Monitoraggio Conformità.md|SP44 - Sistema Monitoraggio Conformità.md
9|Compliance & Risk Management|01 SP45 - Hub Intelligenza Normativa.md|SP45 - Hub Intelligenza Normativa.md
9|Compliance & Risk Management|01 SP46 - Piattaforma Automazione Conformità.md|SP46 - Piattaforma Automazione Conformità.md
9|Compliance & Risk Management|01 SP47 - Analitiche Conformità e Reporting.md|SP47 - Analitiche Conformità e Reporting.md
9|Compliance & Risk Management|01 SP48 - Piattaforma Intelligenza Conformità.md|SP48 - Piattaforma Intelligenza Conformità.md
9|Compliance & Risk Management|01 SP49 - Gestione Cambiamenti Normativi.md|SP49 - Gestione Cambiamenti Normativi.md
9|Compliance & Risk Management|01 SP50 - Formazione Conformità e Certificazione.md|SP50 - Formazione Conformità e Certificazione.md
10|Supporto all'Utente|01 SP51 - Sistema Help Desk.md|SP51 - Sistema Help Desk.md
10|Supporto all'Utente|01 SP52 - Gestione Base Conoscenze.md|SP52 - Gestione Base Conoscenze.md
10|Supporto all'Utente|01 SP53 - Assistente Virtuale e Chatbot.md|SP53 - Assistente Virtuale e Chatbot.md
10|Supporto all'Utente|01 SP54 - Piattaforma Formazione Utenti.md|SP54 - Piattaforma Formazione Utenti.md
10|Supporto all'Utente|01 SP55 - Portale Self-Service.md|SP55 - Portale Self-Service.md
10|Supporto all'Utente|01 SP56 - Analitiche Supporto e Reporting.md|SP56 - Analitiche Supporto e Reporting.md
10|Supporto all'Utente|01 SP57 - Gestione Feedback Utenti.md|SP57 - Gestione Feedback Utenti.md
11|Analisi Dati e Reporting|01 SP58 - Data Lake e Gestione Archiviazione.md|SP58 - Data Lake e Gestione Archiviazione.md
11|Analisi Dati e Reporting|01 SP59 - Pipeline ETL e Elaborazione Dati.md|SP59 - Pipeline ETL e Elaborazione Dati.md
11|Analisi Dati e Reporting|01 SP60 - Analitiche Avanzate e Machine Learning.md|SP60 - Analitiche Avanzate e Machine Learning.md
11|Analisi Dati e Reporting|01 SP61 - Portale Analitiche Self-Service.md|SP61 - Portale Analitiche Self-Service.md
11|Analisi Dati e Reporting|01 SP62 - Qualità Dati e Governance.md|SP62 - Qualità Dati e Governance.md
11|Analisi Dati e Reporting|01 SP63 - Analitiche Real-Time e Streaming.md|SP63 - Analitiche Real-Time e Streaming.md
11|Analisi Dati e Reporting|01 SP64 - Analitiche Predittive e Previsioni.md|SP64 - Analitiche Predittive e Previsioni.md
11|Analisi Dati e Reporting|01 SP65 - Monitoraggio Prestazioni e Avvisi.md|SP65 - Monitoraggio Prestazioni e Avvisi.md
11|Analisi Dati e Reporting|01 SP66 - Sicurezza Dati e Conformità.md|SP66 - Sicurezza Dati e Conformità.md
11|Analisi Dati e Reporting|01 SP67 - Gateway API e Livello Integrazione.md|SP67 - Gateway API e Livello Integrazione.md
11|Analisi Dati e Reporting|01 SP68 - DevOps e Pipeline CI CD.md|SP68 - DevOps e Pipeline CI CD.md
11|Analisi Dati e Reporting|01 SP69 - Disaster Recovery e Continuità Aziendale.md|SP69 - Disaster Recovery e Continuità Aziendale.md
11|Analisi Dati e Reporting|01 SP70 - Gestione Conformità e Audit.md|SP70 - Gestione Conformità e Audit.md
11|Analisi Dati e Reporting|01 SP71 - Ottimizzazione Prestazioni e Scalabilità.md|SP71 - Ottimizzazione Prestazioni e Scalabilità.md
11|Analisi Dati e Reporting|01 SP72 - Gestione Incidenti e Escalation.md|SP72 - Gestione Incidenti e Escalation.md
EOF

echo "✅ Mappature SP caricate"
echo "📊 Script generati in /scripts/ per UC2-UC11"
