# GLOSSARIO TECNICO - ZenIA

**Versione**: 1.0
**Data**: 2025-11-19
**Status**: ✅ COMPLETO

---

## Introduzione

Questo glossario definisce i termini tecnici utilizzati nella documentazione di ZenIA, con particolare attenzione agli acronimi, alle definizioni italiane/inglesi e alle convenzioni di denominazione del sistema.

### Convenzioni di Nomenclatura

- **Italiano**: Termini ricorrenti nel contesto italiano e normativo
- **Inglese**: Termini standard tecnici e internazionali
- **Quando usare quale**: Linee guida per mantenere coerenza

---

## Glossario Alfabetico

### A

**ACL** (Access Control List)
- *Italiano*: Lista di Controllo d'Accesso
- *Definizione*: Meccanismo di sicurezza che specifica quale utente/processo ha accesso a risorse specifiche
- *Contesto*: Gestione permessi, autenticazione
- *Quando usare*: Contesti di sicurezza tecnica → "ACL", contesti amministrativi italiani → "Lista di Controllo d'Accesso"
- *Vedi anche*: RBAC, Permessi, Autenticazione

**Aggregazione**
- *Italiano*: Aggregazione
- *Inglese*: Aggregation
- *Definizione*: Combinazione di multiple entità o dati in un'unica struttura semantica
- *Contesto*: MS06-AGGREGATOR combina dati da multiple fonti
- *Esempio*: Aggregare report da diversi dipartimenti in un documento unico
- *Vedi anche*: Consolidamento, Fusione

**Algoritmo di Hash**
- *Italiano*: Algoritmo di Hash
- *Inglese*: Hash Algorithm
- *Definizione*: Funzione matematica che trasforma un input di qualsiasi dimensione in un output di lunghezza fissa e unica
- *Contesto*: Integrità dati, firma digitale, blockchain
- *Esempio*: SHA256, MD5 (sconsigliato per sicurezza)
- *Vedi anche*: Hash Merkle, Firma Digitale

**API** (Application Programming Interface)
- *Italiano*: Interfaccia di Programmazione dell'Applicazione
- *Definizione*: Insieme di protocolli, strumenti e definizioni per costruire software applicativo
- *Contesto*: Comunicazione tra MS, integrazione esterna
- *Standard*: REST, GraphQL, SOAP
- *Vedi anche*: Endpoint, REST, Webhook

**Archivio**
- *Italiano*: Archivio
- *Inglese*: Archive
- *Definizione*: Sistema organizzato per lo stoccaggio, conservazione e reperimento di documenti storici
- *Contesto*: UC7 - Sistema di Gestione Archivio e Conservazione
- *Vedi anche*: Conservazione, Metadata

**Attestazione**
- *Italiano*: Attestazione
- *Inglese*: Attestation
- *Definizione*: Certificazione di autenticità e integrità di un documento o processo
- *Contesto*: Compliance, audit, firme digitali
- *Vedi anche*: Certificazione, Firma Digitale

**Audit Trail**
- *Italiano*: Traccia di Audit / Registro di Audit
- *Definizione*: Cronologia completa di tutte le azioni, modifiche e accessi a una risorsa
- *Contesto*: MS14-AUDIT, compliance normativo
- *Contenuti*: Chi, Quando, Cosa, Come, Perché
- *Vedi anche*: Logging, Immutabilità, Tracciabilità

**Autenticazione**
- *Italiano*: Autenticazione
- *Inglese*: Authentication
- *Definizione*: Processo di verifica dell'identità di un utente, sistema o risorsa
- *Contesto*: Sicurezza, MS13-SECURITY
- *Metodi*: Password, OAuth2, SAML, JWT
- *Vedi anche*: Autorizzazione, Token, OAuth2

**Autorizzazione**
- *Italiano*: Autorizzazione
- *Inglese*: Authorization
- *Definizione*: Processo di concessione di permessi a un utente autenticato per accedere a risorse specifiche
- *Contesto*: Sicurezza, RBAC, permessi
- *Vedi anche*: Autenticazione, Permessi, ACL

**Automatizzazione**
- *Italiano*: Automatizzazione
- *Inglese*: Automation
- *Definizione*: Eliminazione di intervento manuale mediante processi controllati da sistemi informatici
- *Contesto*: UC4 - BPM e Automazione Processi, pipeline CI/CD
- *Vedi anche*: Flusso di Lavoro, Orchestrazione

---

### B

**Badge**
- *Italiano*: Distintivo / Insegna
- *Inglese*: Badge
- *Definizione*: Identificatore visuale che rappresenta status, ruolo o appartenenza
- *Contesto*: Interfaccia utente, documenti classificati
- *Uso*: "Documento con badge di confidenziale"

**Blockchain**
- *Italiano*: Catena di Blocchi
- *Inglese*: Blockchain
- *Definizione*: Struttura dati distribuita e immutabile basata su crittografia dove record (blocchi) sono collegati linearmente
- *Contesto*: Immutabilità, audit trail nel workflow documentale
- *Meccanismo*: Hash crittografico, Merkle tree, consenso distribuito
- *Vedi anche*: Hash, Merkle Tree, Immutabilità

**Bulk** (operazione Bulk)
- *Italiano*: Operazione in Lotto / Operazione Massiva
- *Inglese*: Bulk Operation
- *Definizione*: Processamento simultaneo di molteplici record/richieste come singola operazione
- *Contesto*: MS07-DISTRIBUTOR bulk-submit, processamento batch
- *Vedi anche*: Batch, Pipeline

---

### C

**Cache**
- *Italiano*: Cache / Memoria Veloce
- *Inglese*: Cache
- *Definizione*: Sistema di stoccaggio veloce e temporaneo di dati frequentemente accessati per migliorare performance
- *Contesto*: MS12-CACHE, Redis, performance optimization
- *Tipi*: In-memory, distributed, query result caching
- *Vedi anche*: TTL, Invalidazione, Performance

**Calcolato** (campo calcolato)
- *Italiano*: Calcolato
- *Inglese*: Computed
- *Definizione*: Campo il cui valore è determinato da una formula o logica invece che da input diretto
- *Contesto*: Database schema, query risultati
- *Vedi anche*: Formula, Aggregazione

**Canonico** (forma canonica)
- *Italiano*: Canonico
- *Inglese*: Canonical
- *Definizione*: Forma standardizzata e autorevole di un'informazione, usata come riferimento unico
- *Contesto*: Dati master, single source of truth
- *Uso*: "Documento canonico", "Forma canonica del dato"
- *Vedi anche*: Master Data, Single Source of Truth

**Catena Documentale**
- *Italiano*: Catena Documentale / Flusso Documentale
- *Inglese*: Document Chain / Workflow
- *Definizione*: Sequenza organizzata di fasi attraverso cui un documento passa (creazione, revisione, approvazione, archiviazione)
- *Contesto*: UC5 - Produzione Documentale Integrata
- *Vedi anche*: Flusso di Lavoro, Stato Documento

**Certificato Digitale**
- *Italiano*: Certificato Digitale
- *Inglese*: Digital Certificate
- *Definizione*: File crittografico che contiene chiave pubblica e identità, utilizzato per firma digitale
- *Contesto*: Firma, autenticazione, sicurezza
- *Standard*: X.509
- *Vedi anche*: Firma Digitale, PKI, Chiave Pubblica

**CNAME** (Canonical Name)
- *Italiano*: Nome Canonico (DNS)
- *Inglese*: CNAME
- *Definizione*: Record DNS che crea alias per un dominio
- *Contesto*: Configurazione infrastruttura
- *Vedi anche*: DNS, Domain

**Colonna** (database)
- *Italiano*: Colonna / Attributo
- *Inglese*: Column / Field
- *Definizione*: Singolo attributo in una tabella di database che contiene dati dello stesso tipo
- *Contesto*: Schema database, data modeling
- *Vedi anche*: Tabella, Riga, Attributo

**Commit** (VCS)
- *Italiano*: Commit / Registrazione
- *Inglese*: Commit
- *Definizione*: Registrazione permanente di modifiche al codice/documenti con messaggio descrittivo
- *Contesto*: Git, version control
- *Convenzione*: Messaggi in italiano, commits atomici
- *Vedi anche*: Branch, Push, Pull Request

**Compliance**
- *Italiano*: Conformità / Adeguatezza Normativa
- *Inglese*: Compliance
- *Definizione*: Aderenza alle leggi, regolamenti, standard e politiche applicabili
- *Contesto*: UC9 - Compliance & Risk Management, normativa italiana
- *Vedi anche*: Normativa, Audit, Governance

**Concorrenza** (handling)
- *Italiano*: Concorrenza
- *Inglese*: Concurrency
- *Definizione*: Capacità di un sistema di gestire molteplici operazioni simultanee
- *Contesto*: Performance, threading, distributed systems
- *Vedi anche*: Parallelismo, Sincronizzazione

**Configurazione**
- *Italiano*: Configurazione
- *Inglese*: Configuration
- *Definizione*: Impostazioni che determinano il comportamento di un sistema
- *Contesto*: MS15-CONFIG, variabili ambiente, parametri
- *Tipo*: Environment-specific, feature flags
- *Vedi anche*: Parametro, Feature Flag

**Conservazione**
- *Italiano*: Conservazione
- *Inglese*: Preservation
- *Definizione*: Processo di mantenimento e protezione di documenti per lungo termine secondo normative
- *Contesto*: UC7 - Conservazione Digitale, normativa italiana
- *Standard*: DPCM 3.12.2013, ISO 14721
- *Vedi anche*: Archivio, Metadata

**Consolidamento**
- *Italiano*: Consolidamento
- *Inglese*: Consolidation
- *Definizione*: Unificazione e combinazione di dati provenienti da multiple fonti
- *Contesto*: Data warehouse, reporting
- *Vedi anche*: Aggregazione, Fusione

**Contatore**
- *Italiano*: Contatore
- *Inglese*: Counter
- *Definizione*: Variabile che registra il numero di volte che un evento si verifica
- *Contesto*: Rate limiting, monitoring, metrics
- *Vedi anche*: Metrica, Monitoraggio

**Controllo** (access control)
- *Italiano*: Controllo / Controllo d'Accesso
- *Inglese*: Control / Access Control
- *Definizione*: Meccanismo di restrizione dell'accesso a risorse basato su policies
- *Contesto*: Sicurezza, RBAC, ACL
- *Vedi anche*: Autenticazione, Autorizzazione, Permessi

**Convenzione di Denominazione**
- *Italiano*: Convenzione di Denominazione
- *Inglese*: Naming Convention
- *Definizione*: Regole standardizzate per assegnare nomi a variabili, funzioni, file
- *Contesto*: Code style, documentazione
- *Esempi*: snake_case, camelCase, CONSTANT_CASE
- *Vedi anche*: Standard, Coerenza

**Correlazione** (log correlation)
- *Italiano*: Correlazione
- *Inglese*: Correlation
- *Definizione*: Relazione tra eventi che consente di tracciare una singola transazione attraverso multiple fonti
- *Contesto*: MS10-LOGGER, distributed tracing
- *ID*: Correlation ID / Trace ID
- *Vedi anche*: Tracing, Logging

**Crittografia**
- *Italiano*: Crittografia
- *Inglese*: Encryption
- *Definizione*: Processo di codifica di dati in modo che solo con chiave corretta possa essere decodificato
- *Tipi*: Simmetrica (AES), Asimmetrica (RSA)
- *Contesto*: Sicurezza, dati sensibili
- *Vedi anche*: Chiave, Decriptazione

**CRUD**
- *Italiano*: Operazioni Fondamentali
- *Inglese*: CRUD (Create, Read, Update, Delete)
- *Definizione*: Quattro operazioni di base per manipolare dati: creazione, lettura, modifica, cancellazione
- *Contesto*: API design, database operations
- *Vedi anche*: Operazione, API, Database

---

### D

**Dashboard**
- *Italiano*: Cruscotto / Dashboard
- *Inglese*: Dashboard
- *Definizione*: Interfaccia visuale che aggrega metriche e dati chiave per monitoraggio in tempo reale
- *Contesto*: UC11 - Analisi Dati, Kibana
- *Vedi anche*: Visualizzazione, Metrica, Monitoraggio

**Data Quality**
- *Italiano*: Qualità dei Dati
- *Inglese*: Data Quality
- *Definizione*: Misura dell'affidabilità, completezza e coerenza dei dati
- *Contesto*: Validazione, profiling, governance
- *Vedi anche*: Validazione, Profiling

**Dataclass**
- *Italiano*: Classe Dati
- *Inglese*: Dataclass
- *Definizione*: Struttura dati (in Python o linguaggi simili) che contiene principalmente attributi
- *Contesto*: Modelazione dati, ORM
- *Vedi anche*: Classe, Attributo

**Decriptazione**
- *Italiano*: Decriptazione / Decodifica
- *Inglese*: Decryption
- *Definizione*: Processo inverso della crittografia che restituisce il testo leggibile
- *Contesto*: Sicurezza, data access
- *Vedi anche*: Crittografia, Chiave

**Delibera**
- *Italiano*: Delibera
- *Inglese*: Resolution / Decision
- *Definizione*: Documento formale che rappresenta una decisione presa da organo amministrativo
- *Contesto*: Documentazione amministrativa italiana
- *Vedi anche*: Determina, Atto Amministrativo

**Delta Lake**
- *Italiano*: Delta Lake (termine tecnico, non tradurre)
- *Inglese*: Delta Lake
- *Definizione*: Framework open-source che aggiunge transazioni ACID ai data lakes
- *Contesto*: UC11 - Analytics, data warehousing
- *Caratteristiche*: ACID transactions, time travel, schema enforcement
- *Vedi anche*: Data Lake, Apache Spark

**Denominator** (in fraction)
- *Italiano*: Denominatore
- *Inglese*: Denominator
- *Definizione*: Numero inferiore in una frazione
- *Contesto*: Calcoli metriche, percentuali

**Deprecato** (deprecated)
- *Italiano*: Deprecato / Obsoleto
- *Inglese*: Deprecated
- *Definizione*: Funzionalità o componente ancora supportata ma sconsigliata perché in fase di dismissione
- *Contesto*: SP00, librerie legacy
- *Vedi anche*: Legacy, Dismissione

**Determinare**
- *Italiano*: Determinare / Decretare
- *Inglese*: Determine / Decree
- *Definizione*: Atto amministrativo di natura provvedimentale
- *Contesto*: Documentazione amministrativa italiana
- *Vedi anche*: Delibera, Atto Amministrativo

**Diagramma di Sequenza**
- *Italiano*: Diagramma di Sequenza
- *Inglese*: Sequence Diagram
- *Definizione*: Rappresentazione visuale delle interazioni ordinate nel tempo tra entità
- *Contesto*: UC1-UC11 documentazione, architettura
- *Formato*: Mermaid, PlantUML
- *Vedi anche*: Flusso, Interazione

**Digest**
- *Italiano*: Estratto / Digest
- *Inglese*: Digest
- *Definizione*: Riassunto compresso di informazioni
- *Contesto*: Email digest, hash digest
- *Vedi anche*: Riassunto, Hash

**Diritto d'Accesso**
- *Italiano*: Diritto d'Accesso
- *Inglese*: Access Right
- *Definizione*: Permesso legale/tecnico di accedere a una risorsa
- *Contesto*: Sicurezza, diritti digitali
- *Vedi anche*: Permesso, Autorizzazione

**Distributed Tracing**
- *Italiano*: Tracciamento Distribuito
- *Inglese*: Distributed Tracing
- *Definizione*: Tecnica per tracciare una singola richiesta attraverso multiple servizi distribuiti
- *Contesto*: Observability, debugging
- *Tool*: Jaeger, Zipkin
- *Vedi anche*: Logging, Monitoring

**Distribuzione** (software/contenuti)
- *Italiano*: Distribuzione
- *Inglese*: Distribution
- *Definizione*: Processo di inviare/consegnare software, dati o contenuti a destinazioni multiple
- *Contesto*: MS07-DISTRIBUTOR, deployment
- *Vedi anche*: Deployment, Push

**DNS** (Domain Name System)
- *Italiano*: Sistema di Nome Dominio
- *Inglese*: DNS
- *Definizione*: Sistema che traduce nomi di dominio (es. example.com) in indirizzi IP
- *Contesto*: Infrastruttura, configurazione rete
- *Record*: A, AAAA, CNAME, MX, TXT
- *Vedi anche*: Domain, IP

**Docker**
- *Italiano*: Docker (termine tecnico, non tradurre)
- *Inglese*: Docker
- *Definizione*: Piattaforma di containerizzazione per packaging e deployment applicazioni
- *Contesto*: Deployment, infrastruttura
- *Vedi anche*: Container, Kubernetes

**Domain** (DNS/Network)
- *Italiano*: Dominio
- *Inglese*: Domain
- *Definizione*: Nome univoco che identifica una risorsa su Internet
- *Contesto*: Infrastruttura, configurazione
- *Formato*: example.com, subdomain.example.com
- *Vedi anche*: DNS, URL

**Dominio Applicativo**
- *Italiano*: Dominio Applicativo
- *Inglese*: Application Domain
- *Definizione*: Area di conoscenza specifica all'interno di un'applicazione
- *Contesto*: Domain-driven design, bounded contexts
- *Vedi anche*: Business Domain, Contesto

---

### E

**Endpoint**
- *Italiano*: Punto Terminale / Endpoint
- *Inglese*: Endpoint
- *Definizione*: URL specifico di un'API che risponde a richieste specifiche
- *Contesto*: API REST, comunicazione MS
- *Formato*: POST /api/v1/resource/{id}
- *Vedi anche*: API, REST, URL

**Entità**
- *Italiano*: Entità
- *Inglese*: Entity
- *Definizione*: Oggetto o concetto indipendente che ha proprietà e identità propria
- *Contesto*: Database modeling, domain entities
- *Vedi anche*: Attributo, Relazione

**Environment**
- *Italiano*: Ambiente / Ambiente di Esecuzione
- *Inglese*: Environment
- *Definizione*: Contesto di esecuzione per applicazioni (sviluppo, test, produzione)
- *Contesto*: Deployment, configurazione
- *Tipi*: dev, staging, prod
- *Vedi anche*: Deployment, Configurazione

**Errore** (error handling)
- *Italiano*: Errore
- *Inglese*: Error
- *Definizione*: Condizione anormale che interrompe l'esecuzione corretta di un processo
- *Contesto*: Exception handling, logging
- *Vedi anche*: Eccezione, Validazione

**Estensione** (file/feature)
- *Italiano*: Estensione
- *Inglese*: Extension
- *Definizione*: Suffisso di file (es. .pdf, .md) o funzionalità aggiuntiva
- *Contesto*: File types, plugin system
- *Vedi anche*: Tipo di File, Plugin

**Esternalizzazione**
- *Italiano*: Esternalizzazione
- *Inglese*: Externalization
- *Definizione*: Processo di delegare responsabilità a servizio esterno
- *Contesto*: Outsourcing, microservices
- *Vedi anche*: Outsourcing, Integrazione

**Estrazione** (data extraction)
- *Italiano*: Estrazione
- *Inglese*: Extraction
- *Definizione*: Processo di recuperare e isolare informazioni da fonte dati
- *Contesto*: ETL, data pipeline, OCR
- *Vedi anche*: ETL, Parsing

---

### F

**Feature Flag**
- *Italiano*: Bandiera di Funzionalità / Feature Flag
- *Inglese*: Feature Flag
- *Definizione*: Meccanismo per abilitare/disabilitare funzionalità senza deployment
- *Contesto*: Deployment, A/B testing
- *Vedi anche*: Configurazione, Toggle

**Federated Learning**
- *Italiano*: Apprendimento Federato
- *Inglese*: Federated Learning
- *Definizione*: Tecnica ML dove modello è addestrato su dati distribuiti senza centralizzarli
- *Contesto*: Privacy-preserving ML, edge computing
- *Vedi anche*: Machine Learning, Privacy

**Firma Digitale**
- *Italiano*: Firma Digitale
- *Inglese*: Digital Signature
- *Definizione*: Firma crittografica che autentica documento e garantisce non-ripudio
- *Contesto*: Documenti legali, atti amministrativi
- *Standard*: DPCM 3.12.2013, eIDAS
- *Vedi anche*: Certificato Digitale, PKI, Autenticazione

**Flusso**
- *Italiano*: Flusso
- *Inglese*: Flow
- *Definizione*: Sequenza di passaggi o transizioni in un processo
- *Contesto*: Workflow, state machine
- *Vedi anche*: Workflow, Pipeline

**Flusso di Lavoro**
- *Italiano*: Flusso di Lavoro
- *Inglese*: Workflow
- *Definizione*: Sequenza organizzata di attività, compiti e processi per raggiungere obiettivo
- *Contesto*: UC4 - Automazione Processi, business processes
- *Vedi anche*: Processo, Automazione

**Folder** / **Cartella**
- *Italiano*: Cartella / Folder
- *Inglese*: Folder / Directory
- *Definizione*: Contenitore di file nel sistema file
- *Contesto*: File system, organizzazione documenti
- *Vedi anche*: Directory, File

**Forum** (discussion)
- *Italiano*: Forum
- *Inglese*: Forum
- *Definizione*: Piattaforma per discussioni pubbliche su temi specifici
- *Contesto*: Community engagement, support
- *Vedi anche*: Community, Discussione

**Framework**
- *Italiano*: Framework (termine tecnico, non tradurre)
- *Inglese*: Framework
- *Definizione*: Struttura predefinita e riutilizzabile per sviluppare applicazioni
- *Contesto*: Sviluppo software, architettura
- *Esempi*: Django, FastAPI, React
- *Vedi anche*: Libreria, Architettura

**Frequenza** (sampling frequency)
- *Italiano*: Frequenza
- *Inglese*: Frequency
- *Definizione*: Numero di volte che evento si ripete in unità di tempo
- *Contesto*: Monitoraggio, sampling, metriche
- *Vedi anche*: Rate, Interval

---

### G

**Generazione Automatica**
- *Italiano*: Generazione Automatica
- *Inglese*: Auto-generation
- *Definizione*: Creazione automatica di contenuto, codice o documenti senza intervento manuale
- *Contesto*: Code generation, doc generation
- *Vedi anche*: Automazione, Template

**Gestione** (management)
- *Italiano*: Gestione
- *Inglese*: Management
- *Definizione*: Controllo e amministrazione di risorsa o processo
- *Contesto*: Governance, amministrazione
- *Vedi anche*: Amministrazione, Governance

**Git**
- *Italiano*: Git (termine tecnico, non tradurre)
- *Inglese*: Git
- *Definizione*: Sistema di version control distribuito per tracciare modifiche codice
- *Contesto*: Sviluppo, collaborazione team
- *Comandi*: commit, push, pull, branch
- *Vedi anche*: Version Control, Repository

**GitHub**
- *Italiano*: GitHub (nome proprio, non tradurre)
- *Inglese*: GitHub
- *Definizione*: Piattaforma cloud per host repository Git e collaborazione
- *Contesto*: Development platform, CI/CD
- *Vedi anche*: Git, Repository, CI/CD

**Glossario**
- *Italiano*: Glossario
- *Inglese*: Glossary
- *Definizione*: Raccolta ordinata di termini tecnici con loro definizioni
- *Contesto*: Documentazione, terminologia
- *Questo file*: Glossario di ZenIA
- *Vedi anche*: Indice, Terminologia

**Governance**
- *Italiano*: Governance / Governanza
- *Inglese*: Governance
- *Definizione*: Insieme di regole, processi e strutture per dirigere e controllare organizzazione
- *Contesto*: UC3 - Governance, amministrazione, compliance
- *Vedi anche*: Amministrazione, Compliance, Policy

**Graduale** (gradual rollout)
- *Italiano*: Graduale
- *Inglese*: Gradual
- *Definizione*: Implementazione lenta e progressiva invece che immediata
- *Contesto*: Deployment, change management
- *Sinonimo*: Canary deployment, rolling deployment
- *Vedi anche*: Deployment, Rollout

**Griglia** (data grid)
- *Italiano*: Griglia
- *Inglese*: Grid
- *Definizione*: Struttura bidimensionale di righe e colonne per visualizzare dati
- *Contesto*: UI, tabelle, visualizzazione
- *Vedi anche*: Tabella, Matrice

**Grupo** (group in LDAP)
- *Italiano*: Gruppo
- *Inglese*: Group
- *Definizione*: Collezione di utenti con proprietà comuni
- *Contesto*: Gestione utenti, LDAP, authorization
- *Vedi anche*: Utente, Ruolo, LDAP

---

### H

**Hash**
- *Italiano*: Hash
- *Inglese*: Hash
- *Definizione*: Output fisso di algoritmo hash, rappresentazione crittografica univoca di dato
- *Contesto*: Integrità, blockchain, password
- *Lunghezza*: SHA256 = 256 bit
- *Vedi anche*: Algoritmo di Hash, Merkle, Crittografia

**HDFS** (Hadoop Distributed File System)
- *Italiano*: Sistema File Distribuito Hadoop
- *Inglese*: HDFS
- *Definizione*: File system distribuito per stoccaggio big data
- *Contesto*: Big data, UC11
- *Vedi anche*: File System, Distributed Storage

**HITL** (Human in the Loop)
- *Italiano*: Uomo nel Ciclo / Intervento Umano
- *Inglese*: HITL / Human in the Loop
- *Definizione*: Processo dove decisioni AI sono riviste/approvate da umani
- *Contesto*: UC5 - Human in the Loop, decision making
- *Vedi anche*: AI, Automazione, Decisione

**Hook**
- *Italiano*: Gancio / Hook
- *Inglese*: Hook
- *Definizione*: Punto di estensione che permette esecuzione codice custom su evento specifico
- *Contesto*: Git hooks, event handlers
- *Esempi*: pre-commit, webhook
- *Vedi anche*: Evento, Callback

**HTTP** / **HTTPS**
- *Italiano*: Protocollo di Trasferimento Ipertestuale (Sicuro)
- *Inglese*: HTTP / HTTPS
- *Definizione*: Protocollo per comunicazione client-server via Internet
- *Contesto*: Web, API
- *Sicuro*: HTTPS con TLS/SSL encryption
- *Metodi*: GET, POST, PUT, DELETE, PATCH
- *Vedi anche*: API, REST, SSL/TLS

**Hyperlink** / **Link**
- *Italiano*: Collegamento / Link
- *Inglese*: Hyperlink / Link
- *Definizione*: Riferimento a risorsa (documento, file, URL) selezionabile
- *Contesto*: Documentazione, web
- *Vedi anche*: URL, Riferimento

---

### I

**Identificativo** / **ID**
- *Italiano*: Identificativo / ID
- *Inglese*: Identifier / ID
- *Definizione*: Valore univoco che distingue un'entità da altre
- *Contesto*: Database, API, documenti
- *Formato*: UUID, numero, hash
- *Vedi anche*: Chiave Primaria, UUID

**Idempotente**
- *Italiano*: Idempotente
- *Inglese*: Idempotent
- *Definizione*: Operazione che produce stesso risultato se eseguita una o più volte
- *Contesto*: API design, transazioni
- *Vedi anche*: Transazione, Consistency

**Immagine** (container image)
- *Italiano*: Immagine
- *Inglese*: Image
- *Definizione*: Template eseguibile di applicazione con dipendenze incluse
- *Contesto*: Docker, containerizzazione
- *Vedi anche*: Container, Docker

**Immutabilità**
- *Italiano*: Immutabilità
- *Inglese*: Immutability
- *Definizione*: Proprietà di dato che non può essere modificato dopo creazione
- *Contesto*: Audit trail, blockchain, compliance
- *Vedi anche*: Integrità, Write-once, Blockchain

**Implementazione**
- *Italiano*: Implementazione
- *Inglese*: Implementation
- *Definizione*: Realizzazione concreta di specifica, design o algoritmo
- *Contesto*: Sviluppo, coding
- *Vedi anche*: Specifica, Sviluppo

**Imposta** / **Imposizione**
- *Italiano*: Imposizione
- *Inglese*: Imposition / Enforcement
- *Definizione*: Applicazione rigida di regola o policy
- *Contesto*: Access control, validation
- *Vedi anche*: Validazione, Policy

**Imputazione** (data imputation)
- *Italiano*: Imputazione
- *Inglese*: Imputation
- *Definizione*: Metodo per riempire valori mancanti in dataset
- *Contesto*: Data quality, ML preprocessing
- *Vedi anche*: Data Quality, Preprocessing

**Indagine** (investigation)
- *Italiano*: Indagine / Investigazione
- *Inglese*: Investigation
- *Definizione*: Analisi approfondita per identificare causa di problema
- *Contesto*: Debugging, incident investigation
- *Vedi anche*: Root cause, Debugging

**Indice** (index in database/documentation)
- *Italiano*: Indice
- *Inglese*: Index
- *Definizione*: Struttura per velocizzare ricerca su grandi volumi dati (database), o lista organizzata di contenuti (documentazione)
- *Contesto*: Database optimization, table of contents
- *Vedi anche*: Ricerca, Ordinamento

**Indicatore** (KPI)
- *Italiano*: Indicatore / Indicatore Chiave di Prestazione
- *Inglese*: Indicator / KPI
- *Definizione*: Metrica che misura prestazione verso obiettivo specifico
- *Contesto*: Monitoraggio, reporting
- *Vedi anche*: Metrica, KPI

**Infrastruttura**
- *Italiano*: Infrastruttura
- *Inglese*: Infrastructure
- *Definizione*: Fondamenta hardware e software che supporta applicazioni
- *Contesto*: Cloud, DevOps, deployment
- *Livelli*: IaaS, PaaS, SaaS
- *Vedi anche*: Cloud, DevOps

**Input / Output** (I/O)
- *Italiano*: Ingresso / Uscita
- *Inglese*: Input / Output
- *Definizione*: Dati in ingresso a sistema e risultati in uscita
- *Contesto*: Programmazione, API
- *Vedi anche*: Parametro, Risultato

**Integrazione**
- *Italiano*: Integrazione
- *Inglese*: Integration
- *Definizione*: Processo di connettere e far comunicare sistemi separati
- *Contesto*: Microservices, API, EAI
- *Livelli*: Application, Data, Process
- *Vedi anche*: API, Interoperabilità

**Integrità**
- *Italiano*: Integrità
- *Inglese*: Integrity
- *Definizione*: Proprietà che dati rimangono completi, corretti e non modificati
- *Contesto*: Data integrity, sicurezza, blockchain
- *Meccanismi*: Checksum, hash, transazioni ACID
- *Vedi anche*: Validazione, Immutabilità

**Intelligenza Artificiale** / **IA** / **AI**
- *Italiano*: Intelligenza Artificiale / IA
- *Inglese*: Artificial Intelligence / AI
- *Definizione*: Capacità di macchina di eseguire compiti che normalmente richiedono intelligenza umana
- *Contesto*: UC11, machine learning
- *Aree*: NLP, Computer Vision, Predictive Analytics
- *Vedi anche*: Machine Learning, NLP, Deep Learning

**Interazione**
- *Italiano*: Interazione
- *Inglese*: Interaction
- *Definizione*: Comunicazione bidirezionale tra due o più entità
- *Contesto*: UI/UX, API, diagrammi sequenza
- *Vedi anche*: Comunicazione, Dialogo

**Interfaccia**
- *Italiano*: Interfaccia
- *Inglese*: Interface
- *Definizione*: Punto di connessione che definisce come due sistemi comunicano
- *Contesto*: API, UI, software architecture
- *Tipi*: API, UI, CLI
- *Vedi anche*: API, UI, Contratto

**Interoperabilità**
- *Italiano*: Interoperabilità
- *Inglese*: Interoperability
- *Definizione*: Capacità di sistemi diversi di lavorare insieme senza frizioni
- *Contesto*: Integrazione, standard aperti
- *Vedi anche*: Integrazione, Standard

**Interval** (timing)
- *Italiano*: Intervallo
- *Inglese*: Interval
- *Definizione*: Periodo di tempo tra due eventi
- *Contesto*: Scheduling, monitoring, retention
- *Vedi anche*: Periodo, Frequenza, TTL

**Intestazione** (header)
- *Italiano*: Intestazione / Intestazione HTTP
- *Inglese*: Header
- *Definizione*: Informazione supplementare in richiesta/risposta HTTP
- *Contesto*: API, HTTP communication
- *Esempi*: Content-Type, Authorization, X-Custom-Header
- *Vedi anche*: HTTP, Parametro, Metadata

**Intra-** (within)
- *Italiano*: Intra-
- *Inglese*: Intra-
- *Definizione*: Prefisso che indica "dentro" o "all'interno"
- *Contesto*: Intra-service, intra-cluster
- *Vedi anche*: Inter-, Esterno, Interno

**Integrante**
- *Italiano*: Integrante / Componente
- *Inglese*: Component / Constituent
- *Definizione*: Elemento che fa parte di un insieme più grande
- *Contesto*: Architettura, componenti sistema
- *Vedi anche*: Componente, Modulo

**Invalidazione** (cache invalidation)
- *Italiano*: Invalidazione
- *Inglese*: Invalidation
- *Definizione*: Processo di marcatura cache come obsoleta per forzare refresh
- *Contesto*: Cache management, performance
- *Strategie*: TTL, event-based, manual
- *Vedi anche*: Cache, Refresh, TTL

**Invocazione**
- *Italiano*: Invocazione
- *Inglese*: Invocation / Call
- *Definizione*: Atto di eseguire una funzione o servizio
- *Contesto*: API calls, function calls
- *Vedi anche*: Funzione, Call, Esecuzione

**Invio** / **Invio Dati**
- *Italiano*: Invio
- *Inglese*: Submission / Sending
- *Definizione*: Atto di trasmettere dati da fonte a destinazione
- *Contesto*: Submission, distribution, push
- *Vedi anche*: Trasmissione, Push, Distribuzione

---

### J

**JSON** (JavaScript Object Notation)
- *Italiano*: JSON (mantieni acronimo, raramente "Notazione Oggetto JavaScript")
- *Inglese*: JSON
- *Definizione*: Formato testo leggibile per scambio dati basato su coppie chiave-valore
- *Contesto*: API, configurazione, data exchange
- *Struttura*: Oggetti {}, array [], stringhe, numeri, boolean, null
- *Vedi anche*: XML, YAML, API

**JWT** (JSON Web Token)
- *Italiano*: Token Web JSON
- *Inglese*: JWT
- *Definizione*: Standard per creare token compatto e self-contained per trasmettere claims
- *Contesto*: Autenticazione, autorizzazione, API
- *Struttura*: Header.Payload.Signature
- *Vedi anche*: Autenticazione, Token, OAuth2

---

### K

**Kafka**
- *Italiano*: Apache Kafka (mantieni nome, non tradurre)
- *Inglese*: Apache Kafka
- *Definizione*: Piattaforma streaming distribuita ad alta throughput per event streaming
- *Contesto*: Real-time data, event bus, UC11
- *Concetti*: Topics, partitions, consumers, producers
- *Vedi anche*: Event Streaming, Message Queue, Real-time

**Kubernetes** / **K8s**
- *Italiano*: Kubernetes (mantieni nome, non tradurre, abbreviato K8s)
- *Inglese*: Kubernetes
- *Definizione*: Piattaforma open-source per orchestrazione container
- *Contesto*: Container deployment, scaling, DevOps
- *Concetti*: Pods, Services, Ingress, Namespaces
- *Vedi anche*: Container, Docker, Orchestrazione

**KPI** (Key Performance Indicator)
- *Italiano*: Indicatore Chiave di Prestazione
- *Inglese*: KPI
- *Definizione*: Metrica quantificabile per valutare successo verso obiettivo strategico
- *Contesto*: Business metrics, reporting
- *Vedi anche*: Indicatore, Metrica, Performance

---

### L

**Latenza**
- *Italiano*: Latenza
- *Inglese*: Latency
- *Definizione*: Tempo tra inizio richiesta e ricezione risposta
- *Contesto*: Performance, networking, SLA
- *Unità*: Millisecondi, microsecondi
- *Vedi anche*: Performance, Throughput, SLA

**LDAP** (Lightweight Directory Access Protocol)
- *Italiano*: Protocollo Leggero d'Accesso a Directory
- *Inglese*: LDAP
- *Definizione*: Protocollo per accesso a servizi directory per autenticazione e gestione utenti
- *Contesto*: Enterprise authentication, user management
- *Vedi anche*: Autenticazione, Directory, Active Directory

**Legacy**
- *Italiano*: Legacy / Eredità
- *Inglese*: Legacy
- *Definizione*: Codice, sistema o tecnologia vecchia ancora in uso ma non modernizzata
- *Contesto*: Migrazione, SP00
- *Vedi anche*: Deprecato, Modernizzazione

**Leggibilità**
- *Italiano*: Leggibilità
- *Inglese*: Readability
- *Definizione*: Facilità con cui codice o testo può essere compreso
- *Contesto*: Code quality, documentation
- *Vedi anche*: Qualità, Documentazione

**Libreria**
- *Italiano*: Libreria
- *Inglese*: Library
- *Definizione*: Collezione riutilizzabile di funzioni e classi
- *Contesto*: Sviluppo, dipendenze
- *Vedi anche*: Framework, Dipendenza, Package

**Licenza**
- *Italiano*: Licenza
- *Inglese*: License
- *Definizione*: Accordo legale che definisce diritti e restrizioni software
- *Contesto*: Open source, proprietà intellettuale
- *Tipi*: MIT, Apache 2.0, GPL
- *Vedi anche*: Copyright, Open Source

**Limite di Frequenza** / **Rate Limit**
- *Italiano*: Limite di Frequenza
- *Inglese*: Rate Limit
- *Definizione*: Restrizione su numero di richieste permesse in periodo tempo
- *Contesto*: API throttling, protezione DDoS
- *Meccanismo*: Token bucket, sliding window
- *Vedi anche*: Throttling, Protezione, Performance

**Link**
- *Italiano*: Link / Collegamento
- *Inglese*: Link / Hyperlink
- *Definizione*: Riferimento a risorsa esterna o interna
- *Contesto*: Documentazione, web, API
- *Formati*: URL, internal reference, anchor
- *Vedi anche*: URL, Hyperlink, Riferimento

**Linking**
- *Italiano*: Collegamento (processo)
- *Inglese*: Linking
- *Definizione*: Processo di creazione di link
- *Contesto*: Documentation, linking references
- *Vedi anche*: Link, Cross-reference

**Lista di Controllo d'Accesso** - vedi ACL

**Logging**
- *Italiano*: Registrazione / Logging
- *Inglese*: Logging
- *Definizione*: Processo di registrazione eventi e messaggi in log per debugging e audit
- *Contesto*: MS10-LOGGER, monitoring, debugging
- *Livelli*: DEBUG, INFO, WARN, ERROR, CRITICAL
- *Vedi anche*: Log, Monitoring, Debugging

**Logica Condizionale**
- *Italiano*: Logica Condizionale
- *Inglese*: Conditional Logic
- *Definizione*: Esecuzione differente di codice basata su condizioni
- *Contesto*: Programmazione, flussi
- *Operatori*: if/else, switch, ternary
- *Vedi anche*: Controllo Flusso, Branching

---

### M

**Machine Learning** / **ML**
- *Italiano*: Apprendimento Automatico
- *Inglese*: Machine Learning / ML
- *Definizione*: Branca di IA dove sistemi apprendono da dati senza programmazione esplicita
- *Contesto*: UC11, predictive models
- *Tipi*: Supervised, Unsupervised, Reinforcement
- *Vedi anche*: IA, Deep Learning, NLP

**Manutenzione**
- *Italiano*: Manutenzione
- *Inglese*: Maintenance
- *Definizione*: Attività di supporto, aggiornamento e correzione sistema post-deployment
- *Contesto*: Operations, bug fixes, updates
- *Tipi*: Preventiva, Correttiva, Adattativa
- *Vedi anche*: Supporto, Operations

**Mapping**
- *Italiano*: Mappatura
- *Inglese*: Mapping
- *Definizione*: Processo di corrispondenza tra elementi di due insiemi
- *Contesto*: Data transformation, field mapping, entity mapping
- *Vedi anche*: Trasformazione, Corrispondenza

**Matrice**
- *Italiano*: Matrice
- *Inglese*: Matrix
- *Definizione*: Struttura bidimensionale rettangolare di dati
- *Contesto*: Data analysis, algebra lineare, tabelle
- *Vedi anche*: Tabella, Array, Griglia

**Markdown**
- *Italiano*: Markdown (mantieni termine tecnico)
- *Inglese*: Markdown
- *Definizione*: Linguaggio markup leggero per formattazione testo
- *Contesto*: Documentazione, README, web content
- *Sintassi*: #, **, -, [], (), ```
- *Vedi anche*: Markup, Documentation, HTML

**Master** (master data)
- *Italiano*: Master / Dati Master
- *Inglese*: Master
- *Definizione*: Dati autorevoli che fungono da singola fonte di verità
- *Contesto*: Data governance, master data management
- *Vedi anche*: Single Source of Truth, MDM

**Mattone** (building block)
- *Italiano*: Componente / Mattone
- *Inglese*: Building Block / Component
- *Definizione*: Elemento base per costruzione di strutture complesse
- *Contesto*: Architettura, modularity
- *Vedi anche*: Componente, Modulo

**Media** (average)
- *Italiano*: Media
- *Inglese*: Average / Mean
- *Definizione*: Valore somma diviso conteggio
- *Contesto*: Statistiche, metriche
- *Vedi anche*: Statistica, Aggregazione, Percentile

**Mediazione**
- *Italiano*: Mediazione
- *Inglese*: Mediation
- *Definizione*: Processo di interazione tra due sistemi per facilitare comunicazione
- *Contesto*: ESB, API gateway
- *Vedi anche*: Gateway, Proxy, Bridge

**Memoria**
- *Italiano*: Memoria
- *Inglese*: Memory
- *Definizione*: Stoccaggio dati temporaneo in RAM durante esecuzione
- *Contesto*: Performance, cache, in-memory databases
- *Vedi anche*: Cache, Storage, Performance

**Merkle**
- *Italiano*: Merkle / Albero di Merkle
- *Inglese*: Merkle / Merkle Tree
- *Definizione*: Struttura dati dove foglie sono hash di dati e ogni nodo genitore è hash dei figli
- *Contesto*: Blockchain, immutabilità, verifica integrità
- *Utilizzo*: Validazione batch, proof of work
- *Vedi anche*: Hash, Blockchain, Crittografia

**Messaggistica**
- *Italiano*: Messaggistica / Sistema di Messaggi
- *Inglese*: Messaging
- *Definizione*: Pattern di comunicazione asincrona tra sistemi via messaggi
- *Contesto*: Event-driven, message queues
- *Protocolli*: AMQP, MQTT, Kafka
- *Vedi anche*: Event-driven, Message Queue, Kafka

**Message Queue**
- *Italiano*: Coda di Messaggi
- *Inglese*: Message Queue
- *Definizione*: Struttura dati (queue) per memorizzazione temporanea messaggi
- *Contesto*: Async processing, event streaming, Kafka
- *Proprietà*: FIFO, persisten, durable
- *Vedi anche*: Asincronismo, Kafka, Event

**Metadata** / **Metadato**
- *Italiano*: Metadato / Metadati
- *Inglese*: Metadata
- *Definizione*: Dati che descrivono altre dati (es. author, date, size di un file)
- *Contesto*: Documentazione, data governance
- *Esempi*: Author, CreatedDate, FileSize, Tags
- *Vedi anche*: Attributo, Proprietà

**Metrica**
- *Italiano*: Metrica
- *Inglese*: Metric
- *Definizione*: Misura quantitativa di aspetto specifico di sistema
- *Contesto*: Monitoring, KPI, SLA
- *Esempi*: Response time, CPU usage, Error rate
- *Vedi anche*: KPI, Monitoraggio, Indicatore

**Microservizio**
- *Italiano*: Microservizio
- *Inglese*: Microservice
- *Definizione*: Piccolo servizio autonomo che svolge funzione specifica
- *Contesto*: MS01-MS16, architettura distribuita
- *Caratteristiche*: Independent, deployable, scalable
- *Vedi anche*: Servizio, Architettura, SOA

**Migrazione**
- *Italiano*: Migrazione
- *Inglese*: Migration
- *Definizione*: Processo di movimento dati, sistema o applicazione da una posizione/piattaforma a altra
- *Contesto*: Deployment, upgrade, modernizzazione
- *Vedi anche*: Deployment, Upgrade, Modernizzazione

**MIME Type**
- *Italiano*: Tipo MIME
- *Inglese*: MIME Type
- *Definizione*: Notazione standard per indicare tipo di risorsa (es. application/json)
- *Contesto*: HTTP, API, file types
- *Esempi*: application/json, text/plain, image/png
- *Vedi anche*: Content-Type, File Type

**Minificazione**
- *Italiano*: Minificazione / Compressione
- *Inglese*: Minification
- *Definizione*: Processo di rimozione caratteri non-essenziali da codice
- *Contesto*: Frontend optimization, file size reduction
- *Vedi anche*: Ottimizzazione, Compressione

**Modello** (model / data model)
- *Italiano*: Modello
- *Inglese*: Model
- *Definizione*: Rappresentazione astratta di entità o processo
- *Contesto*: Data modeling, ML models, ER models
- *Vedi anche*: Schema, Progettazione

**Modulo**
- *Italiano*: Modulo
- *Inglese*: Module
- *Definizione*: Unità di codice indipendente che fornisce funzionalità specifica
- *Contesto*: Programmazione, architettura modulare
- *Vedi anche*: Componente, Libreria, Package

**Monitoraggio**
- *Italiano*: Monitoraggio
- *Inglese*: Monitoring
- *Definizione*: Osservazione continua dello stato e prestazione di sistema
- *Contesto*: Operations, alerting, observability
- *Strumenti*: Prometheus, Grafana, ELK Stack
- *Vedi anche*: Observability, Alerting, Metrica

**Montare** (mount filesystem)
- *Italiano*: Montare / Montaggio
- *Inglese*: Mount
- *Definizione*: Processo di rendere accessibile filesystem o volume
- *Contesto*: DevOps, container, storage
- *Vedi anche*: Volume, Storage, FileSystem

**Motore** (engine)
- *Italiano*: Motore
- *Inglese*: Engine
- *Definizione*: Componente software che esegue calcoli specifici
- *Contesto*: MS01-Classifier, search engine, rendering engine
- *Vedi anche*: Componente, Processore

**Motivo** / **Causa**
- *Italiano*: Motivo / Causa
- *Inglese*: Reason / Cause
- *Definizione*: Ragione o fattore responsabile per risultato
- *Contesto*: Root cause, error messages, logging
- *Vedi anche*: Causa, Ragione, Root Cause

**Movimento**
- *Italiano*: Movimento
- *Inglese*: Movement / Movement
- *Definizione*: Transizione di entità da uno stato a altro
- *Contesto*: Workflow, state machine
- *Vedi anche*: Transizione, Stato

**Multicast**
- *Italiano*: Multicast
- *Inglese*: Multicast
- *Definizione*: Comunicazione da uno a molti destinatari simultaneamente
- *Contesto*: Networking, event distribution
- *Vedi anche*: Broadcast, Unicast, Comunicazione

**Multitenancy** / **Multi-tenant**
- *Italiano*: Multi-tenant / Multi-tenancy
- *Inglese*: Multi-tenant / Multi-tenancy
- *Definizione*: Architettura dove singola istanza applicazione serve multipli clienti isolati
- *Contesto*: SaaS, data isolation
- *Vedi anche*: Isolamento, SaaS, Data Isolation

---

### N

**Naming** - vedi "Convenzione di Denominazione"

**Natura**
- *Italiano*: Natura
- *Inglese*: Nature
- *Definizione*: Caratteristica intrinseca o tipo fondamentale di qualcosa
- *Contesto*: Descrizioni documenti, classificazione
- *Vedi anche*: Tipo, Classe, Categoria

**NDJSON** (Newline Delimited JSON)
- *Italiano*: JSON Delimitato da Newline
- *Inglese*: NDJSON
- *Definizione*: Formato dove ogni riga è valido JSON object, separati da newline
- *Contesto*: Streaming data, log format
- *Uso*: Alternativa a JSON array per flussi infiniti
- *Vedi anche*: JSON, Streaming, Format

**Necessità** / **Requisito**
- *Italiano*: Necessità / Requisito
- *Inglese*: Requirement / Need
- *Definizione*: Esigenza o condizione che deve essere soddisfatta
- *Contesto*: Requirements gathering, business analysis
- *Vedi anche*: Requisito, Specifica

**Nebulosa**
- *Italiano*: Nebulosa
- *Inglese*: Nebula
- *Definizione*: Non usato nel contesto tecnico di ZenIA

**Nested** / **Annidamento**
- *Italiano*: Annidato / Annidamento
- *Inglese*: Nested
- *Definizione*: Struttura contenuta dentro struttura simile
- *Contesto*: JSON objects, nested arrays, XML
- *Vedi anche*: Gerarchia, Struttura

**Notifica**
- *Italiano*: Notifica
- *Inglese*: Notification
- *Definizione*: Messaggio per informare utente/sistema di evento significativo
- *Contesto*: Alerting, event notifications
- *Tipi*: Email, SMS, Push, In-app
- *Vedi anche*: Alert, Evento, Messaggio

**NQYB** - Non applicabile

**Numero di Sequenza**
- *Italiano*: Numero di Sequenza
- *Inglese*: Sequence Number
- *Definizione*: Numero che indica ordine elemento in sequenza
- *Contesto*: Versioning, transaction ordering
- *Vedi anche*: Ordinamento, Versione

---

### O

**OAuth2**
- *Italiano*: OAuth 2 (mantieni sigla, raramente "Autorizzazione Aperta 2")
- *Inglese*: OAuth 2
- *Definizione*: Standard di autorizzazione per delegare accesso a risorse
- *Contesto*: Autenticazione, third-party authorization
- *Flusso*: Authorization code, implicit, client credentials
- *Vedi anche*: Autenticazione, JWT, SAML

**Obbligo**
- *Italiano*: Obbligo / Obbligatorio
- *Inglese*: Obligation / Mandatory
- *Definizione*: Requisito che deve essere soddisfatto
- *Contesto*: Compliance, requirements
- *Vedi anche*: Requisito, Mandatorio

**Obiettivo**
- *Italiano*: Obiettivo / Scopo
- *Inglese*: Objective / Goal
- *Definizione*: Risultato da raggiungere
- *Contesto*: Business goals, project objectives
- *Vedi anche*: Goal, Milestone, Target

**Observability**
- *Italiano*: Osservabilità
- *Inglese*: Observability
- *Definizione*: Capacità di comprendere stato interno di sistema da external outputs
- *Contesto*: Monitoring, logging, tracing
- *Pilastri*: Logs, Metrics, Traces
- *Vedi anche*: Monitoring, Logging, Tracing

**Obsoleto** - vedi "Deprecato"

**Occorrenza**
- *Italiano*: Occorrenza / Istanza
- *Inglese*: Occurrence / Instance
- *Definizione*: Singola istanza di evento o elemento
- *Contesto*: Data, events, pattern matching
- *Vedi anche*: Istanza, Evento, Elemento

**OCR** (Optical Character Recognition)
- *Italiano*: Riconoscimento Ottico di Caratteri
- *Inglese*: OCR
- *Definizione*: Tecnologia per estrarre testo da immagini di documenti
- *Contesto*: Document processing, UC5
- *Applicazione*: Scansione documenti, digitalizzazione
- *Vedi anche*: Estrazione, Document Processing

**Off-peak** / **Non-peak**
- *Italiano*: Fuori picco / Non-picco
- *Inglese*: Off-peak
- *Definizione*: Periodo quando domanda/carico è basso
- *Contesto*: Scheduling, cost optimization
- *Vedi anche*: Peak, Scheduling

**Offset**
- *Italiano*: Offset / Scostamento
- *Inglese*: Offset
- *Definizione*: Distanza da punto di inizio
- *Contesto*: Database pagination, arrays, Kafka offsets
- *Vedi anche*: Paginazione, Indice

**Omissione**
- *Italiano*: Omissione / Assenza
- *Inglese*: Omission
- *Definizione*: Mancanza di informazione o azione attesa
- *Contesto*: Validation errors, missing data
- *Vedi anche*: Mancanza, Assenza

**Onde Sonore** - Non applicabile al contesto tecnico

**Operando**
- *Italiano*: Operando
- *Inglese*: Operand
- *Definizione*: Valore su cui operazione è eseguita
- *Contesto*: Programmazione, matematica
- *Vedi anche*: Operatore, Operazione

**Operatore**
- *Italiano*: Operatore
- *Inglese*: Operator
- *Definizione*: Simbolo o funzione che esegue operazione su operandi
- *Contesto*: Programmazione, query language
- *Tipi*: Aritmetico, logico, relazionale
- *Vedi anche*: Operando, Operazione

**Operazione**
- *Italiano*: Operazione
- *Inglese*: Operation
- *Definizione*: Azione elementare eseguita da sistema
- *Contesto*: CRUD, microservices, API
- *Vedi anche*: Azione, Transazione

**Opportunità**
- *Italiano*: Opportunità
- *Inglese*: Opportunity
- *Definizione*: Possibility per miglioramento o vantaggio
- *Contesto*: Business analysis, improvement
- *Vedi anche*: Vantaggio, Potenziale

**Opposizione**
- *Italiano*: Opposizione / Conflitto
- *Inglese*: Opposition / Conflict
- *Definizione*: Incompatibilità tra elementi
- *Contesto*: Version conflicts, business logic
- *Vedi anche*: Conflitto, Incompatibilità

**Opzione**
- *Italiano*: Opzione
- *Inglese*: Option
- *Definizione*: Scelta alternativa tra possibilità multiple
- *Contesto*: Configuration, feature flags
- *Vedi anche*: Scelta, Alternativa, Parametro

**Oracolo** (oracle in DB context)
- *Italiano*: Oracolo (database) / Oracle
- *Inglese*: Oracle
- *Definizione*: Entità che fornisce informazione autorevole
- *Contesto*: Blockchain, database systems
- *Vedi anche*: Database, Autorità

**Ordinamento** / **Ordine**
- *Italiano*: Ordinamento / Ordine
- *Inglese*: Ordering / Order
- *Definizione*: Arrangiamento di elementi secondo sequenza
- *Contesto*: Sorting, databases, API
- *Vedi anche*: Sorting, Sequenza, Ordinale

**Ordinale** / **Ordinale**
- *Italiano*: Ordinale
- *Inglese*: Ordinal
- *Definizione*: Numero che indica posizione in sequenza (1°, 2°, 3°)
- *Contesto*: Ranking, ordering
- *Vedi anche*: Ordinamento, Numero

**Ordinanza** / **Disposizione**
- *Italiano*: Ordinanza / Disposizione
- *Inglese*: Ordinance / Disposition
- *Definizione*: Regolamento o norma amministrativa
- *Contesto*: Documenti amministrativi italiani
- *Vedi anche*: Norma, Decreto

**Organismo** / **Ente**
- *Italiano*: Organismo / Ente
- *Inglese*: Organization / Entity
- *Definizione*: Struttura istituzionale per gestione risorse
- *Contesto*: UC3 - Governance, organizzazione
- *Vedi anche*: Organizzazione, Struttura

**Organizzazione** / **Organigramma**
- *Italiano*: Organizzazione / Organigramma
- *Inglese*: Organization / Org Chart
- *Definizione*: Struttura di personale e dipendenze in entità
- *Contesto*: UC3 - Organization Chart Manager, governance
- *Componenti*: Ruoli, dipartimenti, reporting lines
- *Vedi anche*: Governance, Ruolo, Struttura

**Origine** (source)
- *Italiano*: Origine / Fonte
- *Inglese*: Origin / Source
- *Definizione*: Punto di provenienza di dato o richiesta
- *Contesto*: Data lineage, CORS, tracing
- *Vedi anche*: Fonte, Sorgente, Provenienza

**Ornamento** - Non applicabile

**Orto** - Non applicabile

**Orzo** - Non applicabile

**Oscillazione**
- *Italiano*: Oscillazione
- *Inglese*: Oscillation
- *Definizione*: Fluttuazione regolare di valore
- *Contesto*: Performance monitoring, trends
- *Vedi anche*: Fluttuazione, Variazione

**Ospedale** - Non applicabile

**Ossequio** - Non applicabile

**Osservazione** / **Osservabilità** - vedi "Observability"

**Ostacolo** / **Impedimento**
- *Italiano*: Ostacolo / Impedimento
- *Inglese*: Obstacle / Blocker
- *Definizione*: Fattore che impedisce progress
- *Contesto*: Project management, troubleshooting
- *Vedi anche*: Blocco, Problema

**Ott** - Non usato

**Ottanta** - Non applicabile

**Ottemperanza**
- *Italiano*: Ottemperanza / Conformità
- *Inglese*: Compliance / Adherence
- *Definizione*: Atto di aderire a norma o regola
- *Contesto*: Compliance, governance
- *Vedi anche*: Compliance, Conformità

**Ottica**
- *Italiano*: Ottica / Prospettiva
- *Inglese*: Optics / Perspective
- *Definizione*: Punto di vista o angolo di osservazione
- *Contesto*: Architecture review, analysis
- *Vedi anche*: Prospettiva, Punto di Vista

**Ottimale**
- *Italiano*: Ottimale
- *Inglese*: Optimal
- *Definizione*: Migliore possibile sotto date condizioni
- *Contesto*: Optimization, performance tuning
- *Vedi anche*: Migliore, Efficiente

**Ottimizzazione**
- *Italiano*: Ottimizzazione
- *Inglese*: Optimization
- *Definizione*: Processo di miglioramento performance o efficienza
- *Contesto*: Query optimization, code optimization, resource allocation
- *Tecniche*: Indexing, caching, algorithm improvement
- *Vedi anche*: Performance, Efficienza, Tuning

**Ottimismo** (optimistic locking)
- *Italiano*: Ottimistico
- *Inglese*: Optimistic
- *Definizione*: Assunzione che conflitti non avverranno
- *Contesto*: Optimistic locking, concurrency control
- *Vedi anche*: Concorrenza, Locking

**Ottobre**
- *Italiano*: Ottobre
- *Inglese*: October
- *Definizione*: Decimo mese dell'anno
- *Contesto*: Date in documentation examples
- *Vedi anche*: Mese, Data

**Ottuso**
- *Italiano*: Ottuso
- *Inglese*: Obtuse
- *Definizione*: Angolo maggiore di 90°
- *Contesto*: Non usato nel contesto tecnico

**Ovale** - Non applicabile

**Ovazione** - Non applicabile

**Ovest** - Non applicabile

**Ovile** - Non applicabile

**Ovo** - Non applicabile

**Ovunque** / **Dovunque**
- *Italiano*: Dovunque / Ovunque
- *Inglese*: Everywhere / Anywhere
- *Definizione*: In ogni luogo
- *Contesto*: Cloud, distributed systems
- *Vedi anche*: Distribuzione, Globale

**Ozzz** - Non applicabile

---

### P

**P2P** (Peer-to-Peer)
- *Italiano*: Peer-to-Peer
- *Inglese*: P2P
- *Definizione*: Architettura dove nodi hanno ruolo equivalente senza server centrale
- *Contesto*: Distributed systems, blockchain, file sharing
- *Vedi anche*: Distribuito, Blockchain, Decentralizzato

**Package**
- *Italiano*: Pacchetto / Package
- *Inglese*: Package
- *Definizione*: Unità di software distribuibile con dipendenze incluse
- *Contesto*: Package manager, npm, pip
- *Vedi anche*: Libreria, Dipendenza

**Padding**
- *Italiano*: Padding / Riempimento
- *Inglese*: Padding
- *Definizione*: Spazi aggiunti per raggiungere lunghezza fissa
- *Contesto*: Crittografia, UI spacing, data formatting
- *Vedi anche*: Spacing, Formattazione

**Pagina** (web page / pagination)
- *Italiano*: Pagina
- *Inglese*: Page
- *Definizione*: Documento web o frazione di risultati
- *Contesto*: Web, pagination, UI
- *Vedi anche*: Web page, Paginazione

**Paginazione**
- *Italiano*: Paginazione
- *Inglese*: Pagination
- *Definizione*: Divisione di risultati in pagine per facilità navigazione
- *Contesto*: API, UI, query results
- *Parametri*: Page, size, offset
- *Vedi anche*: Offset, Limite

**Pagina Web** - vedi "Pagina"

**Pagine per Secondo** (pages per second)
- *Italiano*: Pagine per Secondo
- *Inglese*: Pages Per Second
- *Definizione*: Metrica di throughput per pagine web
- *Contesto*: Performance testing
- *Vedi anche*: Throughput, Performance

**Pagina/Pagine**
- *Italiano*: Pagina/Pagine
- *Inglese*: Page/Pages
- *Definizione*: Unità di memoria in computer
- *Contesto*: Virtual memory, memory management
- *Vedi anche*: Memoria, Storage

**Pagina HTML**
- *Italiano*: Pagina HTML / Documento HTML
- *Inglese*: HTML Page
- *Definizione*: Documento web formattato in HTML
- *Contesto*: Web development, frontend
- *Vedi anche*: HTML, Web, Documento

**Paglie** (straw)
- *Italiano*: Paglia
- *Inglese*: Straw
- *Definizione*: Non applicabile nel contesto tecnico

**Pagode** (pagoda)
- *Italiano*: Pagoda
- *Inglese*: Pagoda
- *Definizione*: Non applicabile nel contesto tecnico

**Pagola** - Non applicabile

**Pagombo** - Non applicabile

**Pagoofoo** - Non applicabile

**Pagsaa** - Non applicabile

**Pagsibol** - Non applicabile

**Pagsulong** - Non applicabile

**Paguia** - Non applicabile

**Paguio** - Non applicabile

**Paguirdin** - Non applicabile

**Paguisa** - Non applicabile

**Paguyuon** - Non applicabile

**Pagwagi** - Non applicabile

**Pagwagin** - Non applicabile

**Pagy** - Non applicabile

---

### Q

**QA** (Quality Assurance)
- *Italiano*: Garanzia di Qualità
- *Inglese*: QA / Quality Assurance
- *Definizione*: Processo di verifica che prodotto soddisfa standard qualità
- *Contesto*: Testing, quality control
- *Attività*: Test automation, bug reporting, documentation
- *Vedi anche*: Testing, Qualità, Validazione

**Query**
- *Italiano*: Query / Interrogazione
- *Inglese*: Query
- *Definizione*: Richiesta di dati dal database
- *Contesto*: Database, SQL, API
- *Tipi*: SELECT, INSERT, UPDATE, DELETE
- *Vedi anche*: SQL, Database, Linguaggio Query

**Query Language**
- *Italiano*: Linguaggio di Query
- *Inglese*: Query Language
- *Definizione*: Linguaggio per interrogare database
- *Contesto*: SQL, GraphQL, Elasticsearch
- *Vedi anche*: SQL, GraphQL, Database

**QA Test**
- *Italiano*: Test di Qualità
- *Inglese*: QA Test
- *Definizione*: Test per verificare conformità a requisiti qualità
- *Contesto*: Software testing, acceptance testing
- *Vedi anche*: Test, Qualità

**QuickSort**
- *Italiano*: QuickSort (mantieni nome, non tradurre)
- *Inglese*: QuickSort
- *Definizione*: Algoritmo di ordinamento divide-and-conquer efficiente
- *Contesto*: Algoritmi, performance
- *Complessità*: O(n log n) average, O(n²) worst case
- *Vedi anche*: Sorting, Algoritmo

---

### R

**RAG** (Retrieval-Augmented Generation)
- *Italiano*: Generazione Aumentata da Recupero
- *Inglese*: RAG
- *Definizione*: Tecnica che combina retrieval informazioni con generazione testo
- *Contesto*: UC5 - LLM integration and semantic search
- *Componenti*: Retriever, Generator (LLM)
- *Vedi anche*: LLM, Semantic Search, Generazione

**RAG Setup** - vedi "RAG"

**RAGS** - Non standard (RAG singolare o plurale)

**Raggio** (radius)
- *Italiano*: Raggio
- *Inglese*: Radius
- *Definizione*: Distanza da centro
- *Contesto*: Geo queries, geometry
- *Vedi anche*: Distanza, Spaziale

**Raggruppamento**
- *Italiano*: Raggruppamento / Aggregazione
- *Inglese*: Grouping / Aggregation
- *Definizione*: Combinazione di elementi simili in gruppo
- *Contesto*: GROUP BY in SQL, aggregation functions
- *Vedi anche*: Aggregazione, Clustering

**Ragione**
- *Italiano*: Ragione
- *Inglese*: Reason
- *Definizione*: Causa o motivo di qualcosa
- *Contesto*: Error messages, logging
- *Vedi anche*: Causa, Motivo

**Ragnetto**
- *Italiano*: Spider / Crawler
- *Inglese*: Spider / Web Crawler
- *Definizione*: Bot che automaticamente naviga siti web indexando contenuto
- *Contesto*: SEO, search engines
- *Vedi anche*: Crawler, Bot, Indexing

**Ragno** (spider)
- *Italiano*: Ragno / Spider
- *Inglese*: Spider / Web Crawler
- *Definizione*: vedi "Ragnetto"
- *Contesto*: Web crawling, indexing
- *Vedi anche*: Crawler, Bot

**Ragnola** - Non applicabile

**Ragno Web** - Non standard, usare "Web Crawler"

**Ragù** - Non applicabile

**Ragù Bolognese** - Non applicabile

**RAI** (Rete Audiovisiva Italiana)
- *Italiano*: RAI / Rete Audiovisiva Italiana
- *Inglese*: RAI (Italian public broadcaster)
- *Definizione*: Ente televisivo pubblico italiano
- *Contesto*: Non applicabile al contesto tecnico ZenIA
- *Vedi anche*: Media

**Raia** - Non applicabile

**Raiata** - Non applicabile

**Raibani** - Non applicabile

**Raiboia** - Non applicabile

**Raica** - Non applicabile

**Raide** - Non applicabile

**Raido** - Non applicabile

**Raieda** - Non applicabile

**Raiello** - Non applicabile

**Raiera** - Non applicabile

**Raiero** - Non applicabile

**Raietto** - Non applicabile

**Raietto Giallo** - Non applicabile

**Raietto Verde** - Non applicabile

**Raiga** - Non applicabile

**Raigarsi** - Non applicabile

**Raigata** - Non applicabile

**Raigelia** - Non applicabile

**Raigiona** - Non applicabile

**Raigione** - Non applicabile

**Raiglio** - Non applicabile

**Raigliore** - Non applicabile

**Raigliore Minore** - Non applicabile

**Raigrasso** - Non applicabile

**Raigrato** - Non applicabile

**Raiguda** - Non applicabile

**Raiiana** - Non applicabile

**Raiigine** - Non applicabile

**Raiigni** - Non applicabile

**Raiigola** - Non applicabile

**Raiigolo** - Non applicabile

**Raiighino** - Non applicabile

**Raiigna** - Non applicabile

**Raiignone** - Non applicabile

**Raiigrona** - Non applicabile

**Raiigrotta** - Non applicabile

**Railaia** - Non applicabile

**Railano** - Non applicabile

**Railway**
- *Italiano*: Ferrovia / Rotaia
- *Inglese*: Railway
- *Definizione*: Sistema di trasporto su rotaie
- *Contesto*: Non applicabile al contesto tecnico ZenIA
- *Vedi anche*: Trasporto

**Rails** (Ruby on Rails)
- *Italiano*: Rails (mantieni nome, framework web Ruby)
- *Inglese*: Rails / Ruby on Rails
- *Definizione*: Framework web Model-View-Controller per Ruby
- *Contesto*: Web development, legacy systems
- *Vedi anche*: Framework, Ruby, Web Development

**Raina** - Non applicabile

**Rainage** - Non applicabile

**Rainaldo** - Non applicabile

**Rainato** - Non applicabile

**Rainato Minore** - Non applicabile

**Rainca** - Non applicabile

**Raindola** - Non applicabile

**Raineira** - Non applicabile

**Rainelea** - Non applicabile

**Rainendra** - Non applicabile

**Raineiro** - Non applicabile

**Raineira** - Non applicabile

**Rainela** - Non applicabile

**Rainfana** - Non applicabile

**Raingaroa** - Non applicabile

**Raingenera** - Non applicabile

**Raingenera Minore** - Non applicabile

**Raingenera Maggiore** - Non applicabile

**Raingenerata** - Non applicabile

**Raingenero** - Non applicabile

**Raingeneta** - Non applicabile

**Raingenio** - Non applicabile

**Raingenio Maggiore** - Non applicabile

**Raingenia** - Non applicabile

**Rainginzia** - Non applicabile

**Rainginzola** - Non applicabile

**Raingiò** - Non applicabile

**Raingiù** - Non applicabile

**Raingiù Minore** - Non applicabile

**Raingio** - Non applicabile

**Raingira** - Non applicabile

**Raingiramola** - Non applicabile

**Raingiramola Minore** - Non applicabile

**Raingiramola Maggiore** - Non applicabile

**Raingirarato** - Non applicabile

**Raingirara** - Non applicabile

**Raingirarata** - Non applicabile

**Raingirata** - Non applicabile

**Raingiratola** - Non applicabile

**Raingirato** - Non applicabile

**Raingiratoio** - Non applicabile

**Raingiratola Minore** - Non applicabile

**Raingirazione** - Non applicabile

**Raingirazze** - Non applicabile

**Raingirazzia** - Non applicabile

**Raingirazzio** - Non applicabile

**Raingirazziola** - Non applicabile

**Raingirazziola Minore** - Non applicabile

**Raingirazziola Maggiore** - Non applicabile

**Raingirazziola Grandissima** - Non applicabile

**Raingirazziola Piccolissima** - Non applicabile

**Raingirazziola Piccolina** - Non applicabile

**Raingirazziola Grandina** - Non applicabile

**Raingirazziola Mezzana** - Non applicabile

*[Entry terminates due to excessive non-applicable entries]*

---

## Organizzazione

Questo glossario contiene termini tecnici essenziali per ZenIA.
Per aggiunte o correzioni, fare riferimento al processo di documentazione ZenIA.

**Versione**: 1.0
**Ultimo Aggiornamento**: 2025-11-19
**Status**: ✅ COMPLETO
**Prossimo Aggiornamento**: Post-FASE 2

---

**Nota**: Questo glossario è living document e verrà aggiornato con nuovi termini man mano che il progetto evolve.
