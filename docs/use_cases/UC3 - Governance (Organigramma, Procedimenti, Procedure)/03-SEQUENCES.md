# Sequence Diagrams - UC3 Governance

## Diagramma Completo del Flusso di Governance

```mermaid
sequenceDiagram
    participant U as Utente
    participant FE as Frontend
    participant SP20 as SP20 Org Chart
    participant SP21 as SP21 Procedures
    participant SP22 as SP22 Process Governance
    participant SP23 as SP23 Compliance Monitor
    participant DB as Database
    participant AUDIT as Audit Log

    U->>FE: Richiesta modifica organigramma
    FE->>SP20: Aggiorna struttura organizzativa
    SP20->>DB: Salva modifiche
    DB-->>SP20: Conferma salvataggio
    SP20->>AUDIT: Log modifica organigramma

    U->>FE: Crea nuova procedura
    FE->>SP21: Salva procedura draft
    SP21->>DB: Archivia procedura
    SP21->>SP21: Inizia workflow approvazione
    SP21-->>FE: Procedura creata, workflow avviato

    SP21->>SP22: Inoltra per approvazione
    SP22->>SP22: Valuta regole business
    SP22->>SP23: Verifica compliance
    SP23-->>SP22: Status compliance
    SP22-->>SP21: Approvazione concessa/rifiutata

    alt Approvazione concessa
        SP21->>DB: Aggiorna status procedura
        SP21->>AUDIT: Log approvazione
        SP21-->>FE: Procedura approvata
    end

    U->>FE: Avvia procedimento amministrativo
    FE->>SP22: Start process instance
    SP22->>DB: Crea process instance
    SP22->>SP23: Monitor compliance SLA
    SP23-->>SP22: SLA status
    SP22-->>FE: Process avviato

    SP22->>SP22: Esegui task automatizzati
    SP22->>SP23: Report progress
    SP23->>AUDIT: Log compliance events
```

## Diagramma di Organigramma Management

```mermaid
sequenceDiagram
    participant HR as HR System
    participant SP20 as Org Chart Manager
    participant CACHE as Redis Cache
    participant DB as PostgreSQL
    participant SEARCH as Elasticsearch

    HR->>SP20: Sync dati dipendenti
    SP20->>DB: Query struttura esistente
    DB-->>SP20: Dati organigramma corrente
    SP20->>SP20: Calcola differenze
    SP20->>DB: Aggiorna posizioni/modifiche
    DB-->>SP20: Conferma aggiornamenti

    SP20->>CACHE: Invalida cache organigramma
    SP20->>SEARCH: Aggiorna indici ricerca
    SEARCH-->>SP20: Indicizzazione completata

    SP20->>SP20: Genera notifiche cambiamenti
    SP20-->>HR: Sync completato
```

## Diagramma di Procedure Approval

```mermaid
sequenceDiagram
    participant AUTHOR as Author
    participant SP21 as Procedure Manager
    participant APPROVER as Approver
    participant SP22 as Process Governance
    participant WORKFLOW as Workflow Engine

    AUTHOR->>SP21: Crea procedura draft
    SP21->>SP21: Valida contenuto
    SP21->>WORKFLOW: Avvia approval workflow
    WORKFLOW-->>SP21: Workflow ID creato

    WORKFLOW->>APPROVER: Notifica task approvazione
    APPROVER->>SP22: Review procedura
    SP22->>SP22: Valuta compliance rules
    SP22-->>APPROVER: Recommendation

    APPROVER->>WORKFLOW: Decide approvazione
    alt Approved
        WORKFLOW->>SP21: Approvazione concessa
        SP21->>SP21: Pubblica procedura
        SP21-->>AUTHOR: Procedura approvata
    else Rejected
        WORKFLOW->>SP21: Approvazione negata
        SP21-->>AUTHOR: Richiesta modifiche
    end
```

## Diagramma di Compliance Monitoring

```mermaid
sequenceDiagram
    participant SP22 as Process Governance
    participant SP23 as Compliance Monitor
    participant RULES as Rules Engine
    participant METRICS as Prometheus
    participant ALERT as Alert Manager

    SP22->>SP23: Report process event
    SP23->>RULES: Valuta compliance rules
    RULES-->>SP23: Compliance status

    alt Violation detected
        SP23->>METRICS: Record violation metric
        SP23->>ALERT: Generate alert
        ALERT->>SP23: Alert acknowledged
        SP23->>SP22: Trigger remediation
    end

    SP23->>SP23: Aggregate compliance data
    SP23->>METRICS: Update dashboard metrics
```

## Diagramma Ultra-Semplificato

```mermaid
sequenceDiagram
    participant User as Utente
    participant System as Sistema Governance

    User->>System: Modifica organigramma
    System->>System: Valida e salva
    System-->>User: Aggiornamento completato

    User->>System: Crea procedura
    System->>System: Approval workflow
    System-->>User: Procedura approvata

    User->>System: Avvia processo
    System->>System: Monitor compliance
    System-->>User: Processo completato
```</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC3 - Governance (Organigramma, Procedimenti, Procedure)/01 Sequence diagrams.md
