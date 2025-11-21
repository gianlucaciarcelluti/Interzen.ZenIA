# 📋 ZenIA

Sistema AI intelligente per la trasformazione digitale della Pubblica Amministrazione Italiana, basato su Apache NiFi e microservizi AI.

**Parte della suite ZenShareUp di Interzen Consulting** - Piattaforma completa per la digitalizzazione e modernizzazione dei processi amministrativi della PA.

## 🎯 Scopo del Progetto

ZenIA è una piattaforma AI completa per modernizzare i processi amministrativi della PA, integrando intelligenza artificiale in tutti gli aspetti della gestione documentale e dei workflow amministrativi.

**Valore Aggiunto**: Riduzione tempi operativi, miglioramento qualità documenti, automazione compliance, supporto decisionale intelligente.

## 🚀 Quick Start

### Prerequisiti
- Docker Desktop
- Python 3.11+
- Git

### Avvio Rapido dell'Infrastruttura

```bash
# 1. Clona il repository
git clone <repository-url>

# 2. Configura ambiente
cp infrastructure/nifi-workflows/.env.example infrastructure/nifi-workflows/.env
# Modifica .env con le tue API keys

# 3. Avvia l'infrastruttura
./infrastructure/nifi-workflows/deploy.sh
```

## 📚 Documentazione

### Casi d'Uso
- [📋 Riepilogo Casi d'Uso](docs/use_cases)
- [UC1 - Sistema di Gestione Documentale](docs/use_cases/UC1%20-%20Sistema%20di%20Gestione%20Documentale/)
- [UC2 - Protocollo Informatico](docs/use_cases/UC2%20-%20Protocollo%20Informatico/)
- [UC3 - Governance](docs/use_cases/UC3%20-%20Governance%20(Organigramma,%20Procedimenti,%20Procedure)/)
- [UC4 - BPM e Automazione Processi](docs/use_cases/UC4%20-%20BPM%20e%20Automazione%20Processi/)
- [UC5 - Produzione Documentale Integrata](docs/use_cases/UC5%20-%20Produzione%20Documentale%20Integrata/)
- [UC6 - Firma Digitale Integrata](docs/use_cases/UC6%20-%20Firma%20Digitale%20Integrata/)
- [UC7 - Sistema di Gestione Archivio e Conservazione](docs/use_cases/UC7%20-%20Sistema%20di%20Gestione%20Archivio%20e%20Conservazione/)
- [UC8 - Integrazione con SIEM](docs/use_cases/UC8%20-%20Integrazione%20con%20SIEM%20(Sicurezza%20Informatica)/)
- [UC9 - Compliance & Risk Management](docs/use_cases/UC9%20-%20Compliance%20&%20Risk%20Management/)
- [UC10 - Supporto all'Utente](docs/use_cases/UC10%20-%20Supporto%20all'Utente/)
- [UC11 - Analisi Dati e Reporting](docs/use_cases/UC11%20-%20Analisi%20Dati%20e%20Reporting/)

### Guide Tecniche
- [🏗️ Architettura Microservizi](docs/use_cases/UC5%20-%20Produzione%20Documentale%20Integrata/00-ARCHITECTURE.md)
- [🚀 Infrastructure README](infrastructure/README.md)
- [📦 Services Documentation](infrastructure/nifi-workflows/services/README.md)

## 🛠️ Troubleshooting

### Problemi Comuni
- **NiFi non si avvia**: Verifica log con `docker logs nifi-orchestrator`
- **PostgreSQL connection refused**: Riavvia container `docker restart postgres-db`
- **FlowFiles bloccati**: Ispeziona queue in NiFi UI

## 🤝 Contribuire

1. Fork del repository
2. Crea feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

## 📄 Licenza

[Inserire licenza]

## 👥 Contatti

[Inserire informazioni di contatto]
