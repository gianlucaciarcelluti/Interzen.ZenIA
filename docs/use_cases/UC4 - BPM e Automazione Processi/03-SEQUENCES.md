# Sequence Diagrams - UC4 BPM e Automazione Processi

## Diagramma Completo del Flusso BPM

```mermaid
sequenceDiagram
    participant U as Utente
    participant DESIGNER as SP26 Designer
    participant MINING as SP24 Mining
    participant RPA as SP25 RPA Orchestrator
    participant ANALYTICS as SP27 Analytics
    participant GOVERNANCE as SP22 Governance
    participant DB as Database
    participant BOT as Bot

    U->>DESIGNER: Crea nuovo processo BPMN
    DESIGNER->>DESIGNER: Valida modello
    DESIGNER->>ANALYTICS: Richiedi ottimizzazioni AI
    ANALYTICS->>ANALYTICS: Analizza modello
    ANALYTICS-->>DESIGNER: Suggerimenti ottimizzazione
    DESIGNER->>GOVERNANCE: Deploy processo
    GOVERNANCE->>DB: Salva definizione processo
    GOVERNANCE-->>DESIGNER: Processo deployato

    U->>MINING: Analizza processi esistenti
    MINING->>DB: Query event logs
    DB-->>MINING: Dati storici
    MINING->>MINING: Process discovery
    MINING-->>U: Modello processo scoperto

    U->>RPA: Avvia automazione processo
    RPA->>RPA: Seleziona bot appropriato
    RPA->>BOT: Assegna task
    BOT->>BOT: Esegui automazione
    BOT-->>RPA: Risultato esecuzione
    RPA->>ANALYTICS: Report performance
    ANALYTICS->>ANALYTICS: Aggiorna metriche
    RPA-->>U: Task completato

    ANALYTICS->>ANALYTICS: Monitor KPI real-time
    ANALYTICS->>U: Alert anomalia
    U->>DESIGNER: Ottimizza processo
    DESIGNER->>GOVERNANCE: Aggiorna definizione
```

## Diagramma di Process Mining

```mermaid
sequenceDiagram
    participant USER as Data Analyst
    participant SP24 as Process Mining Engine
    participant SPARK as Apache Spark
    participant CLICKHOUSE as ClickHouse
    participant STORAGE as MinIO Storage

    USER->>SP24: Upload event log
    SP24->>STORAGE: Store raw data
    STORAGE-->>SP24: Storage confirmation

    SP24->>SP24: Preprocess data
    SP24->>SPARK: Distributed processing
    SPARK->>SPARK: Event correlation
    SPARK-->>SP24: Processed events

    SP24->>SP24: Apply mining algorithm
    SP24->>CLICKHOUSE: Store intermediate results
    CLICKHOUSE-->>SP24: Results stored

    SP24->>SP24: Generate BPMN model
    SP24->>CLICKHOUSE: Store analytics
    SP24-->>USER: Process model + insights

    USER->>SP24: Request conformance check
    SP24->>CLICKHOUSE: Query historical data
    CLICKHOUSE-->>SP24: Historical metrics
    SP24->>SP24: Calculate conformance
    SP24-->>USER: Conformance report
```

## Diagramma di RPA Orchestration

```mermaid
sequenceDiagram
    participant PROCESS as Business Process
    participant SP25 as RPA Orchestrator
    participant QUEUE as Celery Queue
    participant BOT as RPA Bot
    participant MONITOR as Monitoring System

    PROCESS->>SP25: Trigger automation task
    SP25->>SP25: Analyze task requirements
    SP25->>QUEUE: Queue task execution
    QUEUE-->>SP25: Task queued

    SP25->>BOT: Assign task to bot
    BOT->>BOT: Initialize automation
    BOT->>MONITOR: Report start execution

    BOT->>BOT: Execute automation steps
    BOT->>MONITOR: Update progress
    alt Exception occurs
        BOT->>SP25: Report exception
        SP25->>SP25: Analyze exception
        SP25->>BOT: Send recovery instructions
        BOT->>BOT: Execute recovery
    end

    BOT->>BOT: Complete automation
    BOT->>MONITOR: Report completion
    BOT-->>SP25: Task result

    SP25->>SP25: Validate results
    SP25->>PROCESS: Return results
    SP25->>MONITOR: Update analytics
```

## Diagramma di Intelligent Design

```mermaid
sequenceDiagram
    participant DESIGNER as Process Designer
    participant SP26 as Workflow Designer
    participant AI as AI Engine
    participant SIMULATOR as Process Simulator
    participant GOVERNANCE as SP22 Governance

    DESIGNER->>SP26: Open designer interface
    SP26->>SP26: Load templates
    SP26-->>DESIGNER: Available templates

    DESIGNER->>SP26: Create process model
    SP26->>SP26: Real-time validation
    SP26-->>DESIGNER: Validation feedback

    DESIGNER->>SP26: Request AI optimization
    SP26->>AI: Analyze current model
    AI->>AI: Generate suggestions
    AI-->>SP26: Optimization recommendations
    SP26-->>DESIGNER: AI suggestions

    DESIGNER->>SP26: Run simulation
    SP26->>SIMULATOR: Execute simulation
    SIMULATOR->>SIMULATOR: Calculate metrics
    SIMULATOR-->>SP26: Simulation results
    SP26-->>DESIGNER: Performance predictions

    DESIGNER->>SP26: Deploy process
    SP26->>GOVERNANCE: Validate for deployment
    GOVERNANCE->>GOVERNANCE: Compliance check
    GOVERNANCE-->>SP26: Deployment approval
    SP26-->>DESIGNER: Process deployed
```

## Diagramma di Analytics e Monitoring

```mermaid
sequenceDiagram
    participant PROCESS as Process Execution
    participant SP27 as Process Analytics
    participant CLICKHOUSE as ClickHouse
    participant SPARK as Spark ML
    participant DASHBOARD as Dashboard

    PROCESS->>SP27: Emit process event
    SP27->>CLICKHOUSE: Store event data
    CLICKHOUSE-->>SP27: Storage confirmation

    SP27->>SP27: Real-time KPI calculation
    SP27->>DASHBOARD: Update live metrics
    DASHBOARD-->>SP27: Update confirmation

    SP27->>SP27: Check for anomalies
    SP27->>SPARK: ML anomaly detection
    SPARK-->>SP27: Anomaly scores

    alt Anomaly detected
        SP27->>DASHBOARD: Trigger alert
        DASHBOARD->>SP27: Alert acknowledged
    end

    SP27->>SP27: Batch analytics processing
    SP27->>SPARK: Predictive modeling
    SPARK-->>SP27: Forecast results

    SP27->>DASHBOARD: Update predictions
    DASHBOARD-->>SP27: Display updated
```

## Diagramma Ultra-Semplificato

```mermaid
sequenceDiagram
    participant User as Utente
    participant System as Sistema BPM

    User->>System: Analizza processi
    System->>System: Process mining
    System-->>User: Modelli scoperti

    User->>System: Design workflow
    System->>System: AI optimization
    System-->>User: Workflow ottimizzato

    User->>System: Avvia automazione
    System->>System: RPA execution
    System-->>User: Task completato

    User->>System: Monitor performance
    System->>System: Analytics
    System-->>User: KPI e insights
```</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC4 - BPM e Automazione Processi/01 Sequence diagrams.md