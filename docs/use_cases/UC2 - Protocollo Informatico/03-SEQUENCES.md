# Sequence Diagrams - UC2 Protocollo Informatico

## Diagramma Completo del Flusso di Protocollo

```mermaid
sequenceDiagram
    participant U as Utente
    participant FE as Frontend
    participant SP16 as SP16 Classifier
    participant SP17 as SP17 Suggester
    participant SP18 as SP18 Anomaly Detector
    participant SP19 as SP19 Orchestrator
    participant SP02 as SP02 Document Processor
    participant SP07 as SP07 Metadata Extractor
    participant DB as Database
    participant AUDIT as Audit Log

    U->>FE: Upload documento/email
    FE->>SP19: Inizia workflow protocollo
    SP19->>AUDIT: Log inizio workflow

    SP19->>SP16: Richiedi classificazione
    SP16->>SP16: Analizza contenuto
    SP16-->>SP19: Risultato classificazione

    SP19->>SP17: Richiedi suggerimenti protocollo
    SP17->>DB: Query titolario
    DB-->>SP17: Dati titolario
    SP17-->>SP19: Suggerimenti registro/titolario

    SP19->>SP18: Verifica anomalie
    SP18->>DB: Query pattern storici
    DB-->>SP18: Dati storici
    SP18-->>SP19: Status anomalie

    alt Anomalia rilevata
        SP19->>FE: Alert anomalia
        FE->>U: Notifica verifica manuale
        U->>FE: Conferma manuale
    end

    SP19->>SP02: Elabora documento
    SP02->>SP02: Estrai testo/metadata
    SP02-->>SP19: Documento elaborato

    SP19->>SP07: Estrai metadata avanzati
    SP07->>SP07: NER/AI analysis
    SP07-->>SP19: Metadata arricchiti

    SP19->>DB: Salva protocollo completo
    DB-->>SP19: Protocollo registrato

    SP19->>AUDIT: Log completamento
    SP19-->>FE: Workflow completato
    FE-->>U: Conferma registrazione
```

## Diagramma di Classificazione e Suggerimento

```mermaid
sequenceDiagram
    participant SP19 as Orchestrator
    participant SP16 as Classifier
    participant SP17 as Suggester
    participant CACHE as Redis Cache
    participant DB as PostgreSQL

    SP19->>SP16: Classifica corrispondenza
    SP16->>CACHE: Check cache classificazione
    alt Cache hit
        CACHE-->>SP16: Risultato cached
    else Cache miss
        SP16->>SP16: Esegui ML classification
        SP16->>CACHE: Salva risultato
    end
    SP16-->>SP19: Tipo corrispondenza

    SP19->>SP17: Suggerisci protocollo
    SP17->>DB: Query regole titolario
    DB-->>SP17: Regole attive
    SP17->>SP17: Applica regole business
    SP17->>CACHE: Check cache suggerimenti
    alt Cache hit
        CACHE-->>SP17: Suggerimento cached
    else
        SP17->>SP17: Calcolo ML prediction
        SP17->>CACHE: Salva suggerimento
    end
    SP17-->>SP19: Registro + titolario + priorità
```

## Diagramma di Rilevamento Anomalie

```mermaid
sequenceDiagram
    participant SP19 as Orchestrator
    participant SP18 as Anomaly Detector
    participant KAFKA as Kafka Stream
    participant ML as ML Model
    participant ALERT as Alert Manager

    SP19->>SP18: Analizza per anomalie
    SP18->>KAFKA: Stream protocollo data
    KAFKA-->>SP18: Batch dati recenti

    SP18->>ML: Predici anomalie
    ML-->>SP18: Score anomalia

    alt Anomalia rilevata
        SP18->>ALERT: Genera alert
        ALERT->>SP19: Notifica anomalia
        SP19->>SP19: Pausa workflow
    else
        SP18-->>SP19: Status OK
    end

    SP18->>KAFKA: Log analisi
```

## Diagramma Ultra-Semplificato

```mermaid
sequenceDiagram
    participant User as Utente
    participant System as Sistema Protocollo

    User->>System: Invia documento
    System->>System: Classifica
    System->>System: Suggerisci
    System->>System: Verifica
    System->>System: Registra
    System-->>User: Protocollo assegnato
```</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC2 - Protocollo Informatico/01 Sequence diagrams.md