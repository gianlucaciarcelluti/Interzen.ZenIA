# Analisi Costi Hosting e Consumi - ZenShare Up AI Services

## Premessa

Questo documento analizza i costi stimati mensili per l'implementazione dei servizi AI nei 11 casi d'uso identificati per ZenShare Up. L'analisi considera volumi realistici per un'amministrazione pubblica di medie dimensioni e confronta diverse opzioni di deployment per i modelli di linguaggio.

## Stime Volumi Mensili

Basandoci su un'amministrazione pubblica tipica con ~100 utenti attivi:

- **Documenti processati**: 10.000 (classificazione, estrazione metadati, summarization)
- **Protocolli gestiti**: 5.000 (riconoscimento tipologia, suggerimenti categorizzazione)
- **Ricerche semantiche**: 3.000 (Q&A, ricerca avanzata)
- **Documenti generati**: 500 (bozze atti, delibere, determine)
- **Conversazioni assistenza**: 1.000 (helpdesk AI, guide processi)
- **Eventi sicurezza analizzati**: 10.000 (anomaly detection log)
- **Report/analytics generati**: 200 (dashboard, riconciliazioni)

## Costi per Servizio Individuale

### UC1 - Sistema di Gestione Documentale
**Unità**: Documenti processati (10.000/mese)
- **Classificazione automatica**: 10.000 documenti
- **Estrazione metadati**: 10.000 documenti
- **Ricerca semantica**: 3.000 ricerche
- **Summarization**: 2.000 documenti

### UC2 - Protocollo Informatico
**Unità**: Protocolli gestiti (5.000/mese)
- **Riconoscimento tipologia**: 5.000 protocolli
- **Suggerimenti categorizzazione**: 5.000 protocolli
- **Detezione anomalie**: 5.000 controlli

### UC3 - Governance
**Unità**: Query di assistenza (500/mese)
- **Mappatura procedimenti**: 100 analisi
- **Assistente policy/procedure**: 400 query

### UC4 - BPM e Automazione Processi
**Unità**: Workflow processati (2.000/mese)
- **Routing intelligente**: 2.000 decisioni
- **Predizione colli di bottiglia**: 500 analisi
- **Rilevamento anomalie**: 2.000 controlli

### UC5 - Produzione Documentale Integrata
**Unità**: Documenti generati (500/mese)
- **Generazione bozze**: 500 documenti
- **Controllo semantico**: 500 validazioni
- **Suggerimenti linguaggio**: 500 assistenze

### UC6 - Firma Digitale Integrata
**Unità**: Firme validate (1.000/mese)
- **Controlli intelligenti**: 1.000 validazioni
- **Verifica firme multiple**: 500 controlli

### UC7 - Conservazione Digitale
**Unità**: Pacchetti versamento (200/mese)
- **Classificazione pacchetti**: 200 pacchetti
- **Preservazione predittiva**: 200 analisi
- **Controlli coerenza**: 200 validazioni

### UC8 - Integrazione con SIEM
**Unità**: Eventi analizzati (10.000/mese)
- **Anomaly detection**: 10.000 eventi
- **Analisi predittiva**: 1.000 analisi

### UC9 - Compliance & Risk Management
**Unità**: Controlli compliance (5.000/mese)
- **Controllo conformità**: 5.000 controlli
- **Alert predittivi**: 1.000 analisi

### UC10 - Supporto all'Utente
**Unità**: Conversazioni (1.000/mese)
- **Assistente processi**: 800 conversazioni
- **Helpdesk conversazionale**: 200 sessioni

### UC11 - Analisi Dati e Reporting
**Unità**: Report generati (200/mese)
- **Dashboard predittive**: 50 dashboard
- **Riconciliazione documenti**: 150 riconciliazioni

## Costi Infrastrutturali Self-Hosted

Per deployment self-hosted con Ollama su infrastruttura propria:

### Hardware Richiesto
- **GPU Server**: 2x NVIDIA A100 80GB (~€15.000 setup)
- **CPU Server**: 2x Intel Xeon 32-core (~€8.000 setup)
- **Storage**: 10TB NVMe SSD (~€5.000)
- **Network**: 10Gbps connectivity

### Costi Operativi Mensili
- **Elettricità**: ~€500/mese (server 24/7 con GPU)
- **Manutenzione**: ~€200/mese
- **Backup/Disaster Recovery**: ~€150/mese
- **Totale infrastruttura**: ~€850/mese

### Scalabilità
- Supporta fino a 100 utenti concorrenti
- Throughput: ~1.000 richieste/minuto
- Latenza: <500ms per inferenza

## Tabella Comparativa Costi per Modello

| Servizio/Modello | ChatGPT (OpenAI) | Claude (Anthropic) | LLama 3.1 70B (Groq) | LLama 3.1 70B (Self-hosted) |
|------------------|------------------|-------------------|----------------------|-----------------------------|
| **Prezzo Base** | $0.002/1K input tokens<br>$0.004/1K output | $0.008/1K input<br>$0.024/1K output | $0.20/milione tokens | €850/mese infrastruttura |
| **UC1 - Documentale** | ~$180/mese | ~$720/mese | ~$120/mese | ~€850/mese |
| **UC2 - Protocollo** | ~$90/mese | ~$360/mese | ~$60/mese | ~€850/mese |
| **UC3 - Governance** | ~$15/mese | ~$60/mese | ~$10/mese | ~€850/mese |
| **UC4 - BPM** | ~$60/mese | ~$240/mese | ~$40/mese | ~€850/mese |
| **UC5 - Produzione** | ~$80/mese | ~$320/mese | ~$50/mese | ~€850/mese |
| **UC6 - Firma** | ~$20/mese | ~$80/mese | ~$15/mese | ~€850/mese |
| **UC7 - Conservazione** | ~$10/mese | ~$40/mese | ~$7/mese | ~€850/mese |
| **UC8 - SIEM** | ~$200/mese | ~$800/mese | ~$130/mese | ~€850/mese |
| **UC9 - Compliance** | ~$100/mese | ~$400/mese | ~$65/mese | ~€850/mese |
| **UC10 - Supporto** | ~$50/mese | ~$200/mese | ~$35/mese | ~€850/mese |
| **UC11 - Reporting** | ~$40/mese | ~$160/mese | ~$25/mese | ~€850/mese |
| **TOTALE MENSILE** | **~$845/mese** | **~$3.380/mese** | **~$557/mese** | **~€850/mese** |
| **TOTALE ANNUALE** | **~$10.140** | **~$40.560** | **~$6.684** | **~€10.200** |

## Analisi Comparativa

### Vantaggi ChatGPT (OpenAI)
- ✅ Costi contenuti per volumi medio-bassi
- ✅ Alta qualità generazione testo
- ✅ API matura e affidabile
- ✅ Supporto enterprise
- ❌ Dipendenza da provider esterno
- ❌ Limitazioni compliance dati pubblici

### Vantaggi Claude (Anthropic)
- ✅ Eccellente per analisi e ragionamento
- ✅ Focus sicurezza e compliance
- ✅ Buon supporto enterprise
- ❌ Costi più elevati
- ❌ Meno ottimizzato per italiano

### Vantaggi LLama su Groq
- ✅ Buon compromesso costo/qualità
- ✅ Modello open-source customizzabile
- ✅ Performance elevate su Groq
- ✅ Possibilità fine-tuning
- ❌ Richiede ottimizzazione per italiano
- ❌ Dipendenza da Groq (se non self-hosted)

### Vantaggi Self-hosted Ollama
- ✅ Controllo totale dati e compliance
- ✅ Nessuna dipendenza esterna
- ✅ Customizzazione completa
- ✅ Costi prevedibili a lungo termine
- ❌ Costi iniziali infrastruttura elevati
- ❌ Manutenzione e aggiornamenti manuali
- ❌ Richiede competenze tecniche interne

## Raccomandazioni

### Per Amministrazioni Piccole/Medie
- **Raccomandato**: LLama su Groq (~€450/mese)
- **Alternativa**: ChatGPT (~€680/mese)

### Per Amministrazioni Large Enterprise
- **Raccomandato**: Mix ChatGPT per generazione + Self-hosted per compliance
- **Alternativa**: Claude per massima qualità

### Considerazioni Compliance
- Per dati pubblici sensibili: preferire self-hosted
- Per POC/demo: iniziare con API commerciali
- Valutare GDPR e AgID requirements per data residency

## Note Tecniche

- Stime basate su token consumption tipica per task italiani
- Costi infrastrutturali escludono personale IT
- Prezzi API soggetti a variazioni
- Volumi scalabili in base a crescita organizzazione
- Considerare costi sviluppo/integration aggiuntivi (~€50-100K iniziali)