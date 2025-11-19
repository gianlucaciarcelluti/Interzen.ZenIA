# 01 Sequence diagrams

## Diagramma di Sequenza 1: Raccolta e Normalizzazione Eventi Sicurezza

```mermaid
sequenceDiagram
    participant Agent as Wazuh Agent
    participant Collector as SP38 SIEM Collector
    participant Parser as Event Parser
    participant Normalizer as Event Normalizer
    participant Enricher as Event Enricher
    participant Producer as Kafka Producer
    participant Topic as Kafka Topic

    Agent->>Collector: Invia log eventi sicurezza
    activate Collector

    Collector->>Parser: Parse raw event
    activate Parser
    Parser-->>Collector: Parsed event data
    deactivate Parser

    Collector->>Normalizer: Normalizza event
    activate Normalizer
    Normalizer-->>Collector: Normalized event
    deactivate Normalizer

    Collector->>Enricher: Arricchisci event
    activate Enricher
    Enricher->>Enricher: Lookup GeoIP
    Enricher->>Enricher: Lookup Asset Info
    Enricher->>Enricher: Lookup Threat Intel
    Enricher-->>Collector: Enriched event
    deactivate Enricher

    Collector->>Producer: Invia a Kafka
    activate Producer
    Producer->>Topic: Publish event
    Producer-->>Collector: Delivery confirmation
    deactivate Producer

    Collector->>Collector: Update collection stats
    deactivate Collector
```

## Diagramma di Sequenza 2: Elaborazione e Correlazione Eventi

```mermaid
sequenceDiagram
    participant Consumer as Kafka Consumer
    participant Processor as SP39 SIEM Processor
    participant Filter as Initial Filter
    participant Correlator as Correlation Engine
    participant AnomalyDetector as Anomaly Detector
    participant ThreatDetector as Threat Detector
    participant AlertEngine as Alert Engine
    participant IncidentMgr as Incident Manager
    participant Storage as SP40 SIEM Storage

    Consumer->>Processor: Poll eventi da Kafka
    activate Processor

    loop Per ogni evento
        Processor->>Filter: Applica filtri iniziali
        activate Filter
        Filter-->>Processor: Event filtered/approved
        deactivate Filter

        Processor->>Correlator: Correlazione evento
        activate Correlator
        Correlator->>Correlator: Cerca correlazioni temporali
        Correlator->>Correlator: Cerca correlazioni attributi
        Correlator->>Correlator: Cerca correlazioni comportamentali
        Correlator-->>Processor: Evento correlato
        deactivate Correlator

        Processor->>AnomalyDetector: Rilevamento anomalie
        activate AnomalyDetector
        AnomalyDetector->>AnomalyDetector: Analisi statistica
        AnomalyDetector->>AnomalyDetector: Analisi comportamentale
        AnomalyDetector->>AnomalyDetector: Analisi ML
        AnomalyDetector-->>Processor: Score anomalia
        deactivate AnomalyDetector

        Processor->>ThreatDetector: Rilevamento minacce
        activate ThreatDetector
        ThreatDetector->>ThreatDetector: Match IOC
        ThreatDetector->>ThreatDetector: Match YARA rules
        ThreatDetector->>ThreatDetector: Analisi comportamentale
        ThreatDetector-->>Processor: Match minacce
        deactivate ThreatDetector

        Processor->>AlertEngine: Genera alert
        activate AlertEngine
        AlertEngine->>AlertEngine: Calcola severità
        AlertEngine->>AlertEngine: Verifica soppressioni
        AlertEngine->>AlertEngine: Invia notifiche
        AlertEngine-->>Processor: Alert generati
        deactivate AlertEngine

        Processor->>IncidentMgr: Gestisci incidenti
        activate IncidentMgr
        IncidentMgr->>IncidentMgr: Cerca incidenti correlati
        IncidentMgr->>IncidentMgr: Crea/aggiorna incidente
        IncidentMgr->>IncidentMgr: Avvia workflow
        IncidentMgr-->>Processor: Incidenti gestiti
        deactivate IncidentMgr

        Processor->>Storage: Archivia evento elaborato
        activate Storage
        Storage-->>Processor: Conferma archiviazione
        deactivate Storage
    end

    Processor->>Consumer: Commit offset
    deactivate Processor
```

## Diagramma di Sequenza 3: Archiviazione Multi-Tier

```mermaid
sequenceDiagram
    participant Processor as SIEM Processor
    participant HotStorage as SP40 Hot Storage
    participant ES as Elasticsearch
    participant Redis as Redis Cache
    participant WarmStorage as SP40 Warm Storage
    participant ClickHouse as ClickHouse
    participant S3 as S3 Storage
    participant ColdStorage as SP40 Cold Storage
    participant Glacier as Glacier
    participant RetentionMgr as Retention Manager

    Processor->>HotStorage: Archivia evento (Hot)
    activate HotStorage

    HotStorage->>ES: Index in Elasticsearch
    activate ES
    ES-->>HotStorage: Indexing confirmation
    deactivate ES

    HotStorage->>Redis: Cache in Redis
    activate Redis
    Redis-->>HotStorage: Cache confirmation
    deactivate Redis

    HotStorage-->>Processor: Archiviazione completata
    deactivate HotStorage

    RetentionMgr->>RetentionMgr: Verifica policy retention
    note over RetentionMgr: Dopo 30 giorni

    RetentionMgr->>HotStorage: Esporta dati hot
    activate RetentionMgr

    HotStorage->>WarmStorage: Sposta a warm storage
    activate WarmStorage

    WarmStorage->>ClickHouse: Store in ClickHouse
    activate ClickHouse
    ClickHouse-->>WarmStorage: Storage confirmation
    deactivate ClickHouse

    WarmStorage->>S3: Archive to S3
    activate S3
    S3-->>WarmStorage: Archive confirmation
    deactivate S3

    WarmStorage-->>RetentionMgr: Spostamento completato
    deactivate WarmStorage

    RetentionMgr->>HotStorage: Elimina da hot storage
    deactivate RetentionMgr

    note over RetentionMgr: Dopo 365 giorni
    RetentionMgr->>RetentionMgr: Verifica policy retention

    RetentionMgr->>WarmStorage: Esporta dati warm
    activate RetentionMgr

    WarmStorage->>ColdStorage: Sposta a cold storage
    activate ColdStorage

    ColdStorage->>Glacier: Archive to Glacier
    activate Glacier
    Glacier-->>ColdStorage: Archive confirmation
    deactivate Glacier

    ColdStorage-->>RetentionMgr: Spostamento completato
    deactivate ColdStorage

    RetentionMgr->>WarmStorage: Elimina da warm storage
    deactivate RetentionMgr
```

## Diagramma di Sequenza 4: Analytics e Reporting Real-Time

```mermaid
sequenceDiagram
    participant Events as Security Events
    participant Analytics as SP41 Analytics Engine
    participant Flink as Flink Processor
    participant ML as ML Engine
    participant Reporting as Reporting Engine
    participant Dashboard as Dashboard Engine
    participant Grafana as Grafana
    participant Email as Email Service
    participant User as Security Analyst

    Events->>Analytics: Stream eventi sicurezza
    activate Analytics

    Analytics->>Flink: Elabora real-time
    activate Flink
    Flink->>Flink: Windowed aggregations
    Flink->>Flink: Real-time metrics
    Flink-->>Analytics: Metrics aggiornate
    deactivate Flink

    Analytics->>ML: Threat intelligence
    activate ML
    ML->>ML: Pattern analysis
    ML->>ML: Anomaly detection
    ML->>ML: Behavior analysis
    ML-->>Analytics: Threat insights
    deactivate ML

    Analytics->>Reporting: Genera report compliance
    activate Reporting
    Reporting->>Reporting: Calcola compliance score
    Reporting->>Reporting: Render report
    Reporting->>Reporting: Convert to PDF
    Reporting-->>Analytics: Report generato
    deactivate Reporting

    Analytics->>Dashboard: Aggiorna dashboard
    activate Dashboard
    Dashboard->>Grafana: Update panels
    activate Grafana
    Grafana-->>Dashboard: Update confirmation
    deactivate Grafana

    Dashboard->>Email: Invia alert notifiche
    activate Email
    Email-->>Dashboard: Delivery confirmation
    deactivate Email

    Dashboard-->>Analytics: Dashboard aggiornato
    deactivate Dashboard

    User->>Grafana: Visualizza dashboard
    activate User
    Grafana-->>User: Dashboard data
    User->>Grafana: Drill-down analysis
    Grafana-->>User: Detailed data
    deactivate User

    deactivate Analytics
```

## Diagramma di Sequenza 5: Threat Hunting e Investigation

```mermaid
sequenceDiagram
    participant Analyst as Security Analyst
    participant Kibana as Kibana UI
    participant Search as Unified Search
    participant HotStorage as Hot Storage (ES)
    participant WarmStorage as Warm Storage (ClickHouse)
    participant ColdStorage as Cold Storage (Glacier)
    participant Analytics as Analytics Engine
    participant ML as ML Engine
    participant SOAR as SOAR Platform

    Analyst->>Kibana: Avvia threat hunting
    activate Analyst

    Kibana->>Search: Query ricerca unificata
    activate Search

    Search->>HotStorage: Cerca in hot storage
    activate HotStorage
    HotStorage-->>Search: Risultati hot
    deactivate HotStorage

    Search->>WarmStorage: Cerca in warm storage
    activate WarmStorage
    WarmStorage-->>Search: Risultati warm
    deactivate WarmStorage

    alt Ricerca cold storage necessaria
        Search->>ColdStorage: Inizia retrieval Glacier
        activate ColdStorage
        ColdStorage->>ColdStorage: Initiate retrieval job
        ColdStorage-->>Search: Job ID
        note over ColdStorage: Async retrieval (4-5 hours)
        deactivate ColdStorage
    end

    Search-->>Kibana: Risultati combinati
    deactivate Search

    Kibana-->>Analyst: Visualizza risultati
    Analyst->>Analytics: Richiedi analisi ML
    activate Analytics

    Analytics->>ML: Analizza pattern minaccia
    activate ML
    ML->>ML: Clustering anomalie
    ML->>ML: Pattern recognition
    ML->>ML: Predictive analysis
    ML-->>Analytics: Threat intelligence
    deactivate ML

    Analytics-->>Analyst: Risultati analisi
    deactivate Analytics

    Analyst->>SOAR: Crea playbook investigation
    activate SOAR

    SOAR->>SOAR: Orchestrate investigation
    SOAR->>SOAR: Automate response
    SOAR->>SOAR: Collect evidence
    SOAR-->>Analyst: Investigation results
    deactivate SOAR

    Analyst->>Kibana: Document findings
    deactivate Analyst
```

## Diagramma di Sequenza 6: Compliance Monitoring e Reporting

```mermaid
sequenceDiagram
    participant Scheduler as Report Scheduler
    participant Reporting as SP41 Reporting Engine
    participant DataSource as Analytics Data Source
    participant Calculator as Compliance Calculator
    participant Template as Report Template
    participant PDF as PDF Generator
    participant Distributor as Report Distributor
    participant Recipient as Compliance Officer
    participant Auditor as External Auditor

    Scheduler->>Reporting: Trigger report generation
    activate Scheduler
    note over Scheduler: Scheduled (monthly/quarterly)

    Reporting->>DataSource: Raccogli dati compliance
    activate Reporting
    DataSource-->>Reporting: Compliance data
    deactivate DataSource

    Reporting->>Calculator: Calcola compliance score
    activate Calculator
    Calculator->>Calculator: Analyze controls
    Calculator->>Calculator: Check violations
    Calculator->>Calculator: Calculate metrics
    Calculator-->>Reporting: Compliance score
    deactivate Calculator

    Reporting->>Template: Render report template
    activate Template
    Template->>Template: Populate data
    Template->>Template: Format content
    Template-->>Reporting: HTML report
    deactivate Template

    Reporting->>PDF: Convert to PDF
    activate PDF
    PDF-->>Reporting: PDF report
    deactivate PDF

    Reporting->>Distributor: Distribuisci report
    activate Distributor
    Distributor->>Recipient: Invia email interno
    Distributor->>Auditor: Invia email esterno
    Distributor-->>Reporting: Delivery confirmation
    deactivate Distributor

    deactivate Reporting
    deactivate Scheduler

    Recipient->>Recipient: Review report
    Auditor->>Auditor: Review for audit
```

## Diagramma di Sequenza 7: Predictive Analytics e Risk Assessment

```mermaid
sequenceDiagram
    participant Scheduler as Analytics Scheduler
    participant Predictive as Predictive Engine
    participant TimeSeries as Time Series Model
    participant ML as ML Model
    participant Historical as Historical Data
    participant RiskCalc as Risk Calculator
    participant Dashboard as Dashboard Engine
    participant Alert as Alert System
    participant Analyst as Security Analyst

    Scheduler->>Predictive: Avvia predictive analytics
    activate Scheduler
    note over Scheduler: Daily/Weekly

    Predictive->>Historical: Carica dati storici
    activate Predictive
    Historical-->>Predictive: Historical data

    Predictive->>TimeSeries: Predici volumi eventi
    activate TimeSeries
    TimeSeries->>TimeSeries: Fit ARIMA model
    TimeSeries->>TimeSeries: Forecast future
    TimeSeries-->>Predictive: Volume predictions
    deactivate TimeSeries

    Predictive->>ML: Predici tipi minaccia
    activate ML
    ML->>ML: Analyze patterns
    ML->>ML: Predict threats
    ML-->>Predictive: Threat predictions
    deactivate ML

    Predictive->>RiskCalc: Calcola risk scores
    activate RiskCalc
    RiskCalc->>RiskCalc: Aggregate predictions
    RiskCalc->>RiskCalc: Calculate risk
    RiskCalc-->>Predictive: Risk assessment
    deactivate RiskCalc

    Predictive-->>Dashboard: Aggiorna dashboard predittivo
    deactivate Predictive

    Dashboard->>Alert: Genera alert predittivi
    activate Alert
    alt Risk score alto
        Alert->>Analyst: Invia notifica rischio
    end
    deactivate Alert

    deactivate Scheduler

    Analyst->>Dashboard: Review predictions
    activate Analyst
    Dashboard-->>Analyst: Predictive insights
    Analyst->>Analyst: Plan mitigation
    deactivate Analyst
```

## Diagramma di Sequenza 8: Incident Response Automation

```mermaid
sequenceDiagram
    participant Alert as Alert Engine
    participant SOAR as SOAR Platform
    participant Incident as Incident Manager
    participant Workflow as Workflow Engine
    participant Enricher as Incident Enricher
    participant Responder as Automated Responder
    participant Analyst as Security Analyst
    participant Assets as Asset Management
    participant Network as Network Controls

    Alert->>SOAR: Nuovo alert critico
    activate Alert

    SOAR->>Incident: Crea incidente
    activate SOAR
    Incident-->>SOAR: Incident ID
    deactivate Incident

    SOAR->>Workflow: Avvia workflow response
    activate Workflow
    Workflow->>Enricher: Arricchisci incidente
    activate Enricher
    Enricher->>Assets: Lookup asset info
    Assets-->>Enricher: Asset details
    Enricher->>Enricher: Gather context
    Enricher-->>Workflow: Enriched incident
    deactivate Enricher

    Workflow->>Responder: Esegui automated response
    activate Responder

    alt Tipo minaccia: Malware
        Responder->>Network: Isolate host
        Network-->>Responder: Isolation confirmed
        Responder->>Responder: Quarantine files
    else Tipo minaccia: Brute force
        Responder->>Network: Block source IP
        Network-->>Responder: Block confirmed
        Responder->>Responder: Reset passwords
    end

    Responder-->>Workflow: Response completed
    deactivate Responder

    Workflow->>Analyst: Assegna investigation
    activate Analyst
    Analyst->>Workflow: Investigation in progress
    Analyst->>SOAR: Richiedi additional actions
    SOAR->>Responder: Execute manual actions
    Responder-->>SOAR: Actions completed
    Analyst->>Workflow: Investigation completed
    deactivate Analyst

    Workflow->>Workflow: Update incident status
    Workflow-->>SOAR: Workflow completed
    deactivate Workflow

    deactivate SOAR
    deactivate Alert
```

## Legenda Sequenze

### Attori Principali
- **Agent**: Agenti di raccolta log (Wazuh, Filebeat)
- **Collector**: SP38 SIEM Collector
- **Processor**: SP39 SIEM Processor
- **Storage**: SP40 SIEM Storage
- **Analytics**: SP41 SIEM Analytics & Reporting
- **SOAR**: Security Orchestration, Automation & Response
- **Analyst**: Analista sicurezza

### Flussi Dati
- **Event Flow**: Flusso eventi da raccolta ad archiviazione
- **Processing Flow**: Elaborazione e analisi eventi
- **Storage Flow**: Lifecycle dati multi-tier
- **Analytics Flow**: Generazione insight e report
- **Response Flow**: Risposta automatica e manuale

### Pattern Architetturali
- **Streaming**: Elaborazione real-time con Kafka/Flink
- **Batch**: Elaborazione batch con Spark
- **Multi-tier**: Archiviazione gerarchica hot/warm/cold
- **Event-driven**: Architettura basata su eventi
- **Microservices**: Componenti loosely coupled</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC8 - Integrazione con SIEM (Sicurezza Informatica)/01 Sequence diagrams.md