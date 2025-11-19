# MS03 - Microservizio Orchestratore

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)

---

## Indice

1. [Descrizione del Microservizio](#descrizione-del-microservizio)
2. [Flusso Principale di Orchestrazione](#flusso-principale-di-orchestrazione)
3. [Diagrammi di Sequenza](#diagrammi-di-sequenza)
4. [Payload di Richiesta e Risposta](#payload-di-richiesta-e-risposta)
5. [Stack Tecnologico](#stack-tecnologico)
6. [Documentazione Completa](#documentazione-completa)

---

## Descrizione del Microservizio

### Cos'è MS03?
MS03 è il **motore di orchestrazione intelligente** che coordina l'esecuzione dei workflow documentali nel pipeline integrato. Rappresenta il cervello decisionale della piattaforma, gestendo la logica di business, il routing dinamico e l'orchestrazione dei processi.

### Responsabilità Chiave
MS03 fornisce i seguenti servizi di orchestrazione:

1. **Workflow Orchestration**
   - Gestione dello stato dei workflow
   - Coordinamento tra microservizi
   - Routing basato su regole di business
   - Gestione delle transazioni distribuite

2. **Business Rules Engine**
   - Valutazione delle regole di business
   - Decision making dinamico
   - Configurazione delle policy
   - Versionamento delle regole

3. **Process Monitoring**
   - Tracciamento dell'esecuzione dei processi
   - Metriche di performance
   - Alert e notifiche
   - Report di stato

4. **Integration Hub**
   - Coordinamento con sistemi esterni
   - Gestione delle API gateway
   - Protocolli di comunicazione
   - Sicurezza delle integrazioni

### Contesto di Integrazione
MS03 rappresenta il **coordinatore centrale** che orchestra i workflow tra tutti i microservizi:

```
Sorgenti Workflow
      ↓
[MS03-ORCHESTRATOR] ← Questo microservizio
      ↓
Orchestrazione Workflow
      ↓
┌─────────┬────────────┬─────────┐
↓         ↓            ↓         ↓
MS01     MS02        MS04      MS05
(Class)  (Analy)     (Valid)   (Trans)
```

---

## Flusso Principale di Orchestrazione

Il flusso principale di MS03 descrive il percorso di un workflow dall'avvio all'esecuzione:

```
1. WORKFLOW INITIATION
   Richiesta di workflow ricevuta
   ↓
2. VALIDATION & AUTH
   - Verifica autorizzazioni
   - Validazione parametri
   - Controllo SLA
   ↓
3. BUSINESS RULES EVALUATION
   - Applicazione regole di business
   - Determinazione percorso workflow
   - Assegnazione priorità
   ↓
4. RESOURCE ALLOCATION
   - Allocazione risorse necessarie
   - Verifica disponibilità servizi
   - Setup ambiente esecuzione
   ↓
5. EXECUTION COORDINATION
   - Invocazione microservizi sequenziali
   - Gestione stato transizioni
   - Error handling e retry
   ↓
6. MONITORING & LOGGING
   - Tracciamento esecuzione
   - Metriche collection
   - Audit logging
   ↓
7. COMPLETION HANDLING
   - Consolidamento risultati
   - Notifiche completamento
   - Cleanup risorse
   ↓
8. RESPONSE
   - Ritorno stato finale al caller
```

---

## Diagrammi di Sequenza

### Caso 1: Workflow Orchestration Completo

```mermaid
sequenceDiagram
    participant Client
    participant MS03 as MS03<br/>Orchestrator
    participant MS01 as MS01<br/>Classifier
    participant MS02 as MS02<br/>Analyzer
    participant MS04 as MS04<br/>Validator
    participant DB as PostgreSQL<br/>DB

    Client->>MS03: POST /workflow<br/>(workflow request)
    MS03->>MS03: Validate request<br/>(auth & params)

    MS03->>MS03: Evaluate business<br/>rules
    Note over MS03: Determine workflow<br/>path & priority

    MS03->>MS01: Invoke classification<br/>(document)
    MS01->>MS03: Classification result

    MS03->>MS02: Invoke analysis<br/>(classified doc)
    MS02->>MS03: Analysis result

    MS03->>MS04: Invoke validation<br/>(analyzed doc)
    MS04->>MS03: Validation result

    MS03->>DB: Store workflow<br/>state
    DB-->>MS03: Stored

    MS03-->>Client: Workflow response<br/>(status, results)
```

### Caso 2: Workflow con Error Handling

```mermaid
sequenceDiagram
    participant Client
    participant MS03 as MS03<br/>Orchestrator
    participant MS05 as MS05<br/>Transformer
    participant Queue as Retry<br/>Queue

    Client->>MS03: POST /workflow<br/>(complex workflow)

    MS03->>MS05: Invoke transformation
    MS05-->>MS03: ERROR: Timeout

    MS03->>MS03: Handle error<br/>(retry logic)
    Note over MS03: Retry count: 1/3

    MS03->>Queue: Queue retry<br/>(with backoff)
    Queue-->>MS03: Queued

    MS03->>MS05: Retry transformation
    MS05-->>MS03: SUCCESS

    MS03-->>Client: Workflow completed<br/>(with retry info)
```

---

## Payload di Richiesta e Risposta

### Richiesta: Avvio Workflow (POST /workflow)

Diagramma del payload di richiesta:

```mermaid
graph TD
    A[workflow_id] --> B[string]
    C[workflow_type] --> D[string]
    E[parameters] --> F[object]
    F --> G[input_data: object]
    F --> H[options: object]
    I[priority] --> J[string]
    K[callback_url] --> L[string]
    M[timeout_seconds] --> N[number]
```

### Response: 200 OK (Successo)

Diagramma del payload di risposta:

```mermaid
graph TD
    A[workflow_id] --> B[string]
    C[status] --> D[COMPLETED]
    E[results] --> F[object]
    F --> G[steps_executed: array]
    F --> H[final_output: object]
    I[execution_time_ms] --> J[number]
    K[created_at] --> L[datetime]
    M[completed_at] --> N[datetime]
```

---

## Stack Tecnologico

### Linguaggi e Framework
- **Linguaggio**: Python 3.10+
- **API Framework**: FastAPI (async orchestration)
- **Rules Engine**: Drools / Custom Python rules

### Persistenza e Cache
- **Database**: PostgreSQL (stati workflow, regole business)
- **Cache**: Redis (stati workflow temporanei, sessioni)

### Infrastruttura
- **Container**: Docker
- **Orchestrazione**: Kubernetes
- **Message Queue**: RabbitMQ (comunicazione asincrona)
- **Service Discovery**: MS16-REGISTRY

### Dipendenze Inter-Servizio
- **Input da**: Client esterni, altri MS per workflow
- **Output a**: Tutti gli MS per esecuzione coordinata
- **Condiviso con**: MS08-MONITOR (metriche), MS14-AUDIT (audit)
- **Infrastruttura**: MS15-CONFIG, MS16-REGISTRY

---

## Documentazione Completa

### Guida Veloce per Sviluppatori
1. Vedi [SPECIFICATION.md](SPECIFICATION.md) per **specifiche tecniche dettagliate**
2. Consulta [API.md](API.md) per **riferimento endpoint API completo**
3. Studia [DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) per **schema database e indici**
4. Leggi [TROUBLESHOOTING.md](TROUBLESHOOTING.md) per **risoluzione problemi comuni**

### File di Supporto
- `docker-compose.yml`: Setup locale con PostgreSQL + Redis
- `kubernetes/deployment.yaml`: Deployment Kubernetes per produzione
- `examples/`: Campioni richieste/risposte per testing
- `init-schema.sql`: Script DDL inizializzazione database

---

**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)
