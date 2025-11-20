# Diagrammi di Sequenza UC10

## Flusso Richiesta Supporto

```mermaid
sequenceDiagram
    participant U as User
    participant SP as Self-Service Portal
    participant VA as Virtual Assistant
    participant KB as Knowledge Base
    participant HD as Help Desk
    participant AG as Agent
    participant FB as Feedback System

    U->>SP: Accedi al portale
    SP->>U: Mostra cruscotto

    U->>SP: Cerca aiuto
    SP->>KB: Interroga knowledge base
    KB-->>SP: Restituisce risultati
    SP->>U: Mostra risultati ricerca

    U->>VA: Avvia chat
    VA->>U: Saluto e raccolta contesto

    U->>VA: Descrivi il problema
    VA->>VA: Riconoscimento intenti
    VA->>KB: Cerca soluzioni
    KB-->>VA: Restituisce articoli rilevanti

    alt Soluzione trovata
        VA->>U: Fornisce soluzione
        U->>VA: Conferma risoluzione
        VA->>FB: Richiedi feedback
        U->>FB: Valuta esperienza
    else Nessuna soluzione
        VA->>HD: Crea ticket
        HD->>AG: Assegna ad agente
        AG->>U: Contatta per risoluzione
        AG->>U: Risolve problema
        AG->>FB: Richiedi feedback
        U->>FB: Fornisci feedback
    end
```

## Flusso Risoluzione Ticket

```mermaid
sequenceDiagram
    participant U as User
    participant HD as Help Desk System
    participant RT as Routing Engine
    participant AG as Agent
    participant KB as Knowledge Base
    participant SA as Support Analytics
    participant FB as Feedback System

    U->>HD: Invia ticket
    HD->>RT: Inoltra ticket
    RT->>RT: Analizza priorità e categoria
    RT->>HD: Assegna alla coda

    HD->>AG: Notifica agente
    AG->>HD: Accetta ticket
    AG->>KB: Ricerca soluzione
    KB-->>AG: Fornisce conoscenza

    AG->>U: Contatta utente
    U->>AG: Fornisce dettagli
    AG->>AG: Lavora alla risoluzione

    AG->>HD: Aggiorna stato ticket
    HD->>SA: Registra metriche

    AG->>U: Fornisce soluzione
    U->>AG: Conferma risoluzione

    AG->>HD: Chiude ticket
    HD->>FB: Avvia survey di feedback
    FB->>U: Invia survey
    U->>FB: Compila survey

    FB->>SA: Invia dati di feedback
    SA->>SA: Aggiorna analytics
```

## Flusso Gestione Knowledge Base

```mermaid
sequenceDiagram
    participant AU as Author/Content Creator
    participant KB as Knowledge Base
    participant RV as Review System
    participant AP as Approval Workflow
    participant PB as Publishing System
    participant SR as Search Engine
    participant US as Users

    AU->>KB: Crea nuovo articolo
    KB->>AU: Modello articolo

    AU->>KB: Invia bozza
    KB->>RV: Invia per revisione
    RV->>RV: Controlli automatici
    RV->>AP: Inoltra per approvazione

    AP->>AP: Flusso di approvazione
    AP->>PB: Approva per pubblicazione

    PB->>KB: Pubblica articolo
    KB->>SR: Aggiorna indice di ricerca
    SR->>SR: Reindicizza contenuti

    US->>SR: Cerca nella knowledge
    SR->>US: Restituisce risultati
    US->>KB: Accede all'articolo

    KB->>KB: Traccia metriche di utilizzo
    KB->>AU: Invia analytics di utilizzo
```

## Flusso Interazione Assistente Virtuale

```mermaid
sequenceDiagram
    participant U as User
    participant VA as Virtual Assistant
    participant NLP as NLP Engine
    participant DM as Dialog Manager
    participant KB as Knowledge Base
    participant WF as Workflow Engine
    participant HD as Help Desk

    U->>VA: Invia messaggio
    VA->>NLP: Elabora testo
    NLP->>NLP: Tokenizza e analizza
    NLP-->>VA: Intenti e entità

    VA->>DM: Ottieni prossima azione
    DM->>DM: Aggiorna contesto
    DM-->>VA: Strategia di risposta

    alt Query alla knowledge
        VA->>KB: Cerca nella knowledge
        KB-->>VA: Restituisce articoli
        VA->>U: Fornisce informazioni
    else Avvio workflow
        VA->>WF: Inizia workflow
        WF-->>VA: Primo passo
        VA->>U: Richiede informazioni
    else Necessaria escalation
        VA->>HD: Crea ticket
        HD-->>VA: Ticket creato
        VA->>U: Conferma creazione ticket
    end

    VA->>VA: Aggiorna stato conversazione
    VA->>U: Invia risposta
```

## Flusso Self-Service Portal

```mermaid
sequenceDiagram
    participant U as User
    participant SP as Self-Service Portal
    participant SC as Service Catalog
    participant WF as Workflow Engine
    participant KB as Knowledge Base
    participant FB as Feedback System

    U->>SP: Login al portale
    SP->>SP: Carica preferenze utente
    SP->>U: Mostra cruscotto personalizzato

    U->>SC: Sfoglia servizi
    SC->>SC: Filtra e cerca
    SC-->>U: Mostra catalogo servizi

    U->>SC: Seleziona servizio
    SC->>WF: Verifica prerequisiti
    WF-->>SC: Prerequisiti soddisfatti

    SC->>WF: Avvia workflow guidato
    WF->>U: Primo modulo
    U->>WF: Invia dati modulo

    loop Passi del workflow
        WF->>WF: Elabora passo
        WF->>U: Passo successivo o completamento
    end

    WF->>U: Workflow completato
    WF->>FB: Avvia survey di soddisfazione
    FB->>U: Invia survey

    U->>FB: Compila survey
    FB->>SP: Aggiorna esperienza utente
```

## Flusso Piattaforma di Formazione

```mermaid
sequenceDiagram
    participant U as User
    participant TP as Training Platform
    participant UP as User Profiling
    participant LP as Learning Path Engine
    participant CM as Course Management
    participant AS as Assessment Engine
    participant CE as Certification Engine

    U->>TP: Accedi portale formazione
    TP->>UP: Valuta profilo utente
    UP->>UP: Analizza competenze e preferenze
    UP-->>TP: Profilo utente

    TP->>LP: Genera percorso di apprendimento
    LP->>LP: Adatta corsi al profilo
    LP-->>TP: Percorso raccomandato

    U->>CM: Iscriviti al corso
    CM->>CM: Verifica prerequisiti
    CM-->>U: Iscrizione confermata

    U->>CM: Avvia modulo formativo
    CM->>CM: Traccia avanzamento
    U->>CM: Completa modulo

    CM->>AS: Avvia valutazione
    AS->>U: Presenta domande
    U->>AS: Invia risposte

    AS->>AS: Valuta assessment
    AS-->>U: Risultati e feedback

    alt Assessment superato
        CM->>CE: Emissione certificato
        CE-->>U: Certificato digitale
    else Assessment non superato
        CM->>U: Percorso di recupero
    end
```

## Flusso Support Analytics

```mermaid
sequenceDiagram
    participant SY as Support Systems
    participant RA as Real-Time Analytics
    participant PA as Predictive Analytics
    participant BI as Business Intelligence
    participant DB as Dashboard
    participant RP as Report Engine
    participant MG as Management

    SY->>RA: Genera eventi
    RA->>RA: Elabora in real-time
    RA->>RA: Aggiorna metriche

    RA->>PA: Invia dati storici
    PA->>PA: Allena modelli
    PA->>PA: Genera previsioni

    DB->>BI: Richiesta dati dashboard
    BI->>RA: Ottieni metriche real-time
    BI->>PA: Ottieni previsioni
    BI-->>DB: Dashboard compilata

    MG->>RP: Richiesta report
    RP->>BI: Raccogli dati
    RP->>RP: Genera report
    RP-->>MG: Consegna report

    RA->>RA: Rileva anomalie
    RA->>SY: Genera alert
```

## Flusso Gestione Feedback

```mermaid
sequenceDiagram
    participant U as User
    participant FC as Feedback Collection
    participant SA as Sentiment Analysis
    participant FP as Feedback Processing
    participant AM as Action Management
    participant HD as Help Desk
    participant KB as Knowledge Base

    U->>FC: Fornisci feedback
    FC->>FC: Raccoglie da diversi canali
    FC->>SA: Invia per analisi

    SA->>SA: Analizza sentiment e intenti
    SA-->>FC: Risultati dell'analisi

    FC->>FP: Elabora feedback
    FP->>FP: Categoria e priorità
    FP->>AM: Determina azioni

    AM->>AM: Instrada azioni
    AM->>HD: Crea ticket (se necessario)
    AM->>KB: Aggiorna knowledge (se necessario)
    AM->>U: Invia risposte (se necessario)

    FP->>FP: Traccia completamento azioni
    FP->>FC: Aggiorna stato feedback
```

## Flusso di Integrazione Componenti UC10

```mermaid
sequenceDiagram
    participant U as User
    participant SP as Self-Service Portal
    participant VA as Virtual Assistant
    participant HD as Help Desk
    participant KB as Knowledge Base
    participant TP as Training Platform
    participant SA as Support Analytics
    participant FB as Feedback Management

    U->>SP: Accedi supporto
    SP->>VA: Instrada all'assistente
    VA->>KB: Interroga knowledge
    KB-->>VA: Restituisce soluzioni

    VA->>HD: Escala se necessario
    HD->>HD: Elabora ticket
    HD->>TP: Raccomanda formazione

    HD->>SA: Invia metriche
    SA->>SA: Analizza performance

    HD->>FB: Raccoglie feedback
    FB->>FB: Elabora e analizza
    FB->>KB: Aggiorna knowledge base
    FB->>HD: Attiva miglioramenti

    SA->>SP: Aggiorna contenuti portale
    SA->>VA: Migliora risposte
    SA->>HD: Ottimizza instradamento
```
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC10 - Supporto all'Utente/02 Sequence Diagrams UC10.md