# 🏗️ ZenShareUp - Architettura Completa

## Indice

1. [Overview Architettura](#overview-architettura)
2. [Componenti Core](#componenti-core)
3. [Microservizi](#microservizi)
4. [Servizi di Supporto](#servizi-di-supporto)
5. [DTO e Data Model](#dto-e-data-model)
6. [Flussi Applicativi](#flussi-applicativi)
7. [Integrazione tra Servizi](#integrazione-tra-servizi)
8. [Sicurezza e Multi-tenancy](#sicurezza-e-multi-tenancy)

---

## Overview Architettura

ZenShareUp è una **piattaforma enterprise per la gestione documentale integrata** basata su un'architettura a **microservizi distribuiti**. Il sistema è progettato per supportare:

- **Gestione documentale completa** (creazione, versionamento, archiviazione)
- **Protocollazione informatica** (registrazione, tracciamento, repertori)
- **Automazione flussi** (workflow amministrativi e procedurali)
- **Comunicazioni email** (invio/ricezione con integrazione documentale)
- **Conformità normativa** (audit trail, legal archive, GDPR)
- **Multi-tenancy** (supporto per molteplici organizzazioni)
- **Integrazione SUAP** (Sportelli Unici delle Attività Produttive)

### Principi Architetturali

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT APPLICATIONS                         │
│                  (Web, Mobile, Desktop)                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                ┌──────────▼──────────┐
                │  API GATEWAY        │
                │  (Authentication)   │
                └──────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ┌───▼────┐      ┌──────▼──────┐    ┌────▼────┐
    │ZenAdmin│      │ZenDocuments │    │ZenProtoll
o│
    │        │      │             │    │         │
    └────────┘      └─────────────┘    └─────────┘
        │                  │                  │
    ┌───▼────┐      ┌──────▼──────┐    ┌────▼────┐
    │ZenMaster│     │ZenMailroom  │    │ZenProcess│
    │        │      │             │    │         │
    └────────┘      └─────────────┘    └─────────┘
        │                  │                  │
    ┌───▼────┐      ┌──────▼──────┐    ┌────▼────┐
    │ZenSuap │      │ZenScheduler │    │ZenArchiv
e│
    │        │      │             │    │         │
    └────────┘      └─────────────┘    └─────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ┌───▼────┐      ┌──────▼──────┐    ┌────▼────┐
    │PostgreSQL      │Redis        │    │RabbitMQ │
    │(Primary DB)    │(Cache)      │    │(Events) │
    └────────┘      └─────────────┘    └─────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │ SFTPGo      │
                    │(File Share) │
                    └─────────────┘
```

---

## Componenti Core

### 1. API Gateway & Authentication

**Scopo**: Punto di ingresso unico per tutti i client, gestione autenticazione e autorizzazione

**Tecnologie**:
- OAuth 2.0 / OpenID Connect
- Keycloak (server di identità)
- JWT (JSON Web Tokens)

**Responsabilità**:
- Routing verso microservizi appropriati
- Validazione autenticazione
- Rate limiting
- CORS management
- API versioning

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ (Username/Password)
       ▼
┌──────────────────────┐
│   Keycloak           │ ◄─── (Validate Credentials)
│   (Identity Provider)│
└──────┬───────────────┘
       │ JWT Token
       ▼
┌──────────────────────┐
│   API Gateway        │ ◄─── (Validate Token)
│   (msacloudgateway)  │
└──────┬───────────────┘
       │
       ├─────► ZenAdmin (Manage Users, Roles)
       ├─────► ZenDocuments (Manage Docs)
       ├─────► ZenProtocollo (Register Protocol)
       ├─────► ZenProcess (Execute Workflow)
       ├─────► ZenMailroom (Send Email)
       ├─────► ZenSuap (SUAP Integration)
       └─────► ZenScheduler (Execute Tasks)
```

### 2. Database Centrale - PostgreSQL

**Scopo**: Persistenza dati per tutti i microservizi

**Caratteristiche**:
- Database relazionale centralizzato
- Schema multi-tenancy (per ogni tenant un database logico)
- Supporto per JSON fields (metadata dinamici)
- Full-text search per documenti
- Audit trails integrati

**Principali Tabelle**:
```
┌─────────────────────────────────────────────┐
│              ZENSHAREUP DATABASE             │
├─────────────────────────────────────────────┤
│ ADMIN SCHEMA                                │
│  ├─ users                                   │
│  ├─ groups                                  │
│  ├─ companies                               │
│  ├─ roles & permissions                     │
│  └─ notification_settings                   │
├─────────────────────────────────────────────┤
│ DOCUMENTS SCHEMA                            │
│  ├─ documents                               │
│  ├─ folders                                 │
│  ├─ document_versions                       │
│  ├─ metadata_definitions                    │
│  ├─ metadata_values                         │
│  ├─ models (templates)                      │
│  └─ assignments (smistamento)               │
├─────────────────────────────────────────────┤
│ PROTOCOL SCHEMA                             │
│  ├─ protocols                               │
│  ├─ correspondents                          │
│  ├─ classifications                         │
│  ├─ special_registers                       │
│  └─ protocol_templates                      │
├─────────────────────────────────────────────┤
│ PROCESS SCHEMA                              │
│  ├─ administrative_procedures               │
│  ├─ technical_procedures                    │
│  ├─ process_instances (Flowable)            │
│  ├─ workflow_tasks                          │
│  └─ form_definitions                        │
├─────────────────────────────────────────────┤
│ MAILROOM SCHEMA                             │
│  ├─ email_parameters                        │
│  ├─ email_signatures                        │
│  ├─ receiving_logs                          │
│  └─ sending_logs                            │
├─────────────────────────────────────────────┤
│ MASTER SCHEMA                               │
│  ├─ tenants                                 │
│  ├─ licenses (attive)                       │
│  └─ events                                  │
├─────────────────────────────────────────────┤
│ ARCHIVE SCHEMA                              │
│  ├─ legal_archive (archiviazione legale)    │
│  ├─ historical_data                         │
│  └─ retention_policies                      │
└─────────────────────────────────────────────┘
```

### 3. Cache - Redis

**Scopo**: Miglioramento performance con caching distribuito

**Utilizzi**:
- Cache lookup tables (utenti, gruppi, aziende)
- Session management
- Temporary data storage
- Rate limiting counters
- Distributed locks per operazioni critiche

### 4. Message Broker - RabbitMQ

**Scopo**: Comunicazione asincrona tra microservizi

**Topic Principali**:
- `documents.events` - Creazione, modifica, eliminazione documenti
- `protocol.events` - Registrazione, cancellazione protocolli
- `workflow.events` - Avanzamento processi
- `email.events` - Invio/ricezione email
- `archive.events` - Archiviazione documenti
- `audit.events` - Audit trail

**Pattern di Utilizzo**:
```
Microservice A (Publisher)
        │
        ├─── Document Created Event
        └───────────────────────┬───────────────────────┐
                                │                       │
                          RabbitMQ Exchange             │
                                │                       │
                    ┌───────────┴───────────┐           │
                    │                       │           │
                 Queue A                 Queue B       Queue C
                    │                       │           │
                    ▼                       ▼           ▼
            Microservice B          Microservice C  Indexer
          (Process Workflow)      (Send Notification) (Full-text)
```

### 5. File Storage - SFTPGo

**Scopo**: Archiviazione file documenti in modo sicuro

**Caratteristiche**:
- SFTP access per client
- WebDAV support
- Backup automated
- Virus scanning
- Encryption at rest

**Organizzazione**:
```
/sftp
├── /tenant-001
│   ├── /documents
│   │   ├── /year-2024
│   │   ├── /year-2025
│   │   └── ...
│   ├── /archives
│   └── /temp
├── /tenant-002
│   └── ...
└── /shared-resources
```

---

## Microservizi

### 1. ZenAdmin (msazenadmin)

**Responsabilità**: Gestione amministrativa della Suite

```
┌─────────────────────────────────────────────┐
│         ZenAdmin Microservice               │
├─────────────────────────────────────────────┤
│ Core Entities:                              │
│  ├─ Users (id, username, email, roles)      │
│  ├─ Groups (organizational units)           │
│  ├─ Companies/Organizations                 │
│  ├─ Roles & Permissions                     │
│  ├─ Protocol AOO (organizational areas)     │
│  └─ Correspondents                          │
│                                             │
│ API Endpoints:                              │
│  ├─ POST /users                             │
│  ├─ GET /users/{id}                         │
│  ├─ PUT /users/{id}                         │
│  ├─ DELETE /users/{id}                      │
│  ├─ GET /groups                             │
│  ├─ GET /companies                          │
│  └─ GET /roles                              │
│                                             │
│ DTOs (25 files):                            │
│  ├─ UserDTO                                 │
│  ├─ CompanyDTO                              │
│  ├─ GroupDTO                                │
│  ├─ ProtAOODTO                              │
│  ├─ AdminLookupDTO                          │
│  └─ NotificationDTO                         │
│                                             │
│ Events Published:                           │
│  ├─ user.created                            │
│  ├─ user.updated                            │
│  ├─ user.deleted                            │
│  ├─ group.updated                           │
│  └─ company.updated                         │
└─────────────────────────────────────────────┘
```

**Flusso di Creazione Utente**:
```
1. Client Request (POST /users)
   {
     "username": "mario.rossi",
     "email": "mario@example.com",
     "roles": ["DocumentManger"]
   }

2. ZenAdmin Service
   ├─ Validate input
   ├─ Check uniqueness (email, username)
   ├─ Generate password (or ask client)
   ├─ Hash password
   ├─ Create user in DB
   ├─ Add to cache
   └─ Publish event

3. Keycloak Integration
   ├─ Create user in Keycloak
   ├─ Assign roles
   └─ Enable/disable

4. Event Published
   ├─ ZenDocuments (update permissions)
   ├─ ZenProtocollo (update responsibility)
   └─ ZenMailroom (notify)

5. Response
   {
     "id": 123,
     "username": "mario.rossi",
     "email": "mario@example.com",
     "status": "ACTIVE"
   }
```

### 2. ZenDocuments (msazendocuments)

**Responsabilità**: Gestione completa del ciclo di vita documentale

```
┌──────────────────────────────────────────────────┐
│         ZenDocuments Microservice                │
├──────────────────────────────────────────────────┤
│ Core Entities:                                   │
│  ├─ Documents                                    │
│  │  ├─ Metadata (custom fields)                  │
│  │  ├─ Versions                                  │
│  │  ├─ Assignments (smistamento)                 │
│  │  └─ Permissions                               │
│  ├─ Folders (dossiers)                           │
│  │  ├─ Hierarchical structure                    │
│  │  ├─ Classification schemas                    │
│  │  └─ Dossier management                        │
│  ├─ Models (document templates)                  │
│  │  ├─ Metadata definitions                      │
│  │  ├─ Configuration                             │
│  │  └─ Validation rules                          │
│  └─ Archive                                      │
│     ├─ Legal archive (GDPR)                      │
│     ├─ Historical archive                        │
│     └─ Retention policies                        │
│                                                  │
│ Document Lifecycle:                              │
│  DRAFT ──► CURRENT ──► DEPOSIT ──► HISTORICAL   │
│                             │                    │
│                             └──► LEGAL ARCHIVE   │
│                                                  │
│ DTOs (65 files):                                 │
│  ├─ DocumentDTO (full entity)                    │
│  ├─ DocumentBaseDTO (base properties)            │
│  ├─ FolderDTO                                    │
│  ├─ ModelDTO (templates)                         │
│  ├─ MetadataDefinitionDTO                       │
│  ├─ AssignmentDetailsOutDTO (smistamento)        │
│  └─ Various specialized DTOs                     │
│                                                  │
│ Key API Endpoints:                               │
│  ├─ POST /documents (create)                     │
│  ├─ GET /documents/{id}                          │
│  ├─ PUT /documents/{id}                          │
│  ├─ DELETE /documents/{id}                       │
│  ├─ POST /documents/{id}/assign (smistamento)    │
│  ├─ POST /documents/{id}/version (new version)   │
│  ├─ GET /documents/search                        │
│  ├─ POST /documents/archive (to legal archive)   │
│  ├─ GET /folders (hierarchy)                     │
│  └─ POST /models (create templates)              │
│                                                  │
│ Events Published:                                │
│  ├─ document.created                             │
│  ├─ document.updated                             │
│  ├─ document.versioned                           │
│  ├─ document.assigned                            │
│  ├─ document.archived                            │
│  └─ document.deleted                             │
└──────────────────────────────────────────────────┘
```

**Document Metadata System**:
```
┌────────────────────────────────────────────┐
│        Model (Template)                     │
├────────────────────────────────────────────┤
│ Name: Fattura                               │
│ Code: INVOICE_2024                          │
│                                             │
│ Metadata Definitions:                       │
│  ├─ numero_fattura (String, Required)       │
│  ├─ data_fattura (Date, Required)           │
│  ├─ importo (Decimal, Required)             │
│  ├─ cliente (String, Required)              │
│  ├─ note (Text, Optional)                   │
│  └─ categoria (Enum, Optional)              │
└────────────────────────────────────────────┘
           │
           │ (Used to create)
           ▼
┌────────────────────────────────────────────┐
│      Document Instance                      │
├────────────────────────────────────────────┤
│ FileName: fattura_001_2024.pdf              │
│                                             │
│ Metadata Values:                            │
│  ├─ numero_fattura: "001/2024"              │
│  ├─ data_fattura: "2024-11-20"              │
│  ├─ importo: 1500.00                        │
│  ├─ cliente: "Acme Corp"                    │
│  ├─ note: "Pagamento a 30 giorni"           │
│  └─ categoria: "SALES"                      │
│                                             │
│ Document Info:                              │
│  ├─ ID: doc_12345                           │
│  ├─ Status: CURRENT                         │
│  ├─ Created: 2024-11-20 10:30               │
│  ├─ CreatedBy: mario.rossi                  │
│  ├─ Version: 1.0                            │
│  └─ FolderId: folder_001                    │
└────────────────────────────────────────────┘
```

**Smistamento (Assignment) Process**:
```
┌─────────────────────────────┐
│ Document Created/Updated    │
└──────────────┬──────────────┘
               │
               ▼
   ┌───────────────────────┐
   │ Need Assignment?      │
   │ (Smistamento)         │
   └───────────┬───────────┘
               │
        ┌──────┴──────┐
        │             │
       YES            NO
        │             │
        ▼             ▼
  ┌──────────┐   ┌─────────┐
  │ Assign   │   │ Stored  │
  │ To:      │   │ in      │
  │ - User   │   │ Folder  │
  │ - Group  │   └─────────┘
  │ - Role   │
  └─────┬────┘
        │
        ▼
  ┌──────────────────────────┐
  │ Send Notification        │
  │ ├─ Assigned To: User     │
  │ ├─ Document: Name        │
  │ ├─ Action: Review/Sign   │
  │ └─ Deadline: 5 days      │
  └──────────────────────────┘
        │
        ▼
  ┌──────────────────────────┐
  │ Assignee Actions:        │
  │ ├─ View                  │
  │ ├─ Comment               │
  │ ├─ Sign/Approve          │
  │ ├─ Reject                │
  │ └─ Forward to Another    │
  └──────────────────────────┘
```

### 3. ZenProtocollo (msazenprotocollo)

**Responsabilità**: Protocollazione informatica conforme a normative italiane

```
┌──────────────────────────────────────────────────┐
│         ZenProtocollo Microservice               │
├──────────────────────────────────────────────────┤
│ Core Entities:                                   │
│  ├─ Protocols (Registration)                     │
│  │  ├─ Protocol Number (sequential/by AOO)       │
│  │  ├─ Registration Date/Time                    │
│  │  ├─ Subject                                   │
│  │  ├─ Main Document (Link to ZenDocuments)      │
│  │  ├─ Confidentiality Level                     │
│  │  └─ Status (DRAFT, CLOSED, CANCELED)          │
│  ├─ Correspondents                               │
│  │  ├─ Sender (Input protocols)                  │
│  │  ├─ Recipient (Output protocols)              │
│  │  ├─ Type (Person, Organization, Public Admin)│
│  │  └─ Reference (Email, PEC, Physical)          │
│  ├─ Classifications (Document Classification)    │
│  │  ├─ Classification Schema                     │
│  │  ├─ Category Path                             │
│  │  └─ Hierarchical Structure                    │
│  ├─ Special Registers                            │
│  │  ├─ Special handling types                    │
│  │  └─ Tracking separate from main register      │
│  └─ Emergency Protocols                          │
│     ├─ Temporary protocol numbers                │
│     └─ Validation within timeframe               │
│                                                  │
│ Protocol Types:                                  │
│  ├─ Input (from external)                        │
│  ├─ Output (to external)                         │
│  ├─ Internal                                     │
│  └─ Return (protocol di ritorno)                 │
│                                                  │
│ DTOs (29 files):                                 │
│  ├─ ProtocolDTO (full protocol)                  │
│  ├─ ProtocolRegistrationDTO (input for creation)│
│  ├─ ClassificationOutDTO                         │
│  ├─ CorrespondentOutDTO                          │
│  └─ ProtocolRegistrationManagerDTO               │
│                                                  │
│ Key API Endpoints:                               │
│  ├─ POST /protocols/register (register)          │
│  ├─ GET /protocols/{protocolNumber}              │
│  ├─ PUT /protocols/{id} (update metadata)        │
│  ├─ DELETE /protocols/{id} (cancel)              │
│  ├─ GET /protocols/search                        │
│  ├─ GET /special-registers                       │
│  ├─ POST /protocols/{id}/urgent (emergency)      │
│  └─ GET /correspondents                          │
│                                                  │
│ Events Published:                                │
│  ├─ protocol.registered                          │
│  ├─ protocol.updated                             │
│  ├─ protocol.canceled                            │
│  └─ protocol.correspondent.added                 │
└──────────────────────────────────────────────────┘
```

**Protocol Registration Flow**:
```
1. Client Prepares Document
   ├─ Create/Upload in ZenDocuments
   ├─ Get Document ID
   └─ Prepare metadata (subject, confidentiality)

2. Client Requests Protocol Registration
   POST /protocols/register
   {
     "mainDocumentId": "doc_12345",
     "protocolType": "INPUT",
     "subject": "Richiesta autorizzazione...",
     "documentDate": "2024-11-20",
     "confidentiality": "PUBLIC",
     "correspondents": [
       {
         "type": "PERSON",
         "name": "Giovanni Rossi",
         "email": "giovanni@example.com"
       }
     ],
     "classificationId": "classification_path_001"
   }

3. ZenProtocollo Service
   ├─ Validate document exists (call ZenDocuments)
   ├─ Validate correspondents
   ├─ Check business rules
   ├─ Generate protocol number (sequential by AOO)
   │  Example: 2024/001234 (year/progressive)
   ├─ Create protocol record with status=CLOSED
   ├─ Link to document
   ├─ Store correspondents
   ├─ Update document status to REGISTERED
   └─ Publish protocol.registered event

4. Response to Client
   {
     "id": "prot_12345",
     "protocolNumber": "2024/001234",
     "registrationDate": "2024-11-20T10:35:00Z",
     "subject": "Richiesta autorizzazione...",
     "mainDocumentId": "doc_12345",
     "status": "CLOSED"
   }

5. Other Services React to Event
   ├─ ZenDocuments (update status, add protocol link)
   ├─ ZenMailroom (send email with protocol number)
   ├─ ZenScheduler (schedule archive if retention expires)
   └─ Indexer (full-text indexing for search)

6. Client Can Now
   ├─ View protocol details
   ├─ Print protocol report
   ├─ Send protocol via email/PEC
   ├─ Export as XML for external systems
   └─ Track status
```

### 4. ZenProcess (msazenprocess)

**Responsabilità**: Automazione di workflow e procedure amministrative

```
┌──────────────────────────────────────────────────┐
│         ZenProcess Microservice                  │
├──────────────────────────────────────────────────┤
│ Core Components:                                 │
│  ├─ Workflow Engine (Flowable)                   │
│  │  ├─ BPMN 2.0 process definitions              │
│  │  ├─ Process instances execution               │
│  │  └─ Task management                           │
│  ├─ Administrative Procedures                    │
│  │  ├─ Name, description, legislation            │
│  │  ├─ Deadline (days)                           │
│  │  ├─ Silence expiration rules                  │
│  │  └─ Required documents                        │
│  ├─ Technical Procedures                         │
│  │  ├─ System-level procedures                   │
│  │  └─ Automated workflows                       │
│  ├─ Web Forms (Form Builder)                     │
│  │  ├─ Dynamic form creation                     │
│  │  ├─ Field types, validation                   │
│  │  └─ Conditional visibility                    │
│  ├─ Tasks                                        │
│  │  ├─ User tasks (manual steps)                 │
│  │  ├─ Service tasks (automated)                 │
│  │  ├─ Message tasks (async operations)          │
│  │  └─ Gateway (parallel/exclusive)              │
│  └─ Process History                              │
│     ├─ Historic instances                        │
│     └─ Audit trail                               │
│                                                  │
│ Flowable Integration:                            │
│  ├─ PostgreSQL backend for persistence           │
│  ├─ Async job execution                          │
│  └─ Event listener integration                   │
│                                                  │
│ DTOs (24 files):                                 │
│  ├─ TaskDTO (workflow task)                      │
│  ├─ AdministrativeProcedureDTO                   │
│  ├─ TechnicalProcedureDTO                        │
│  ├─ FormBuilderFormDTO                           │
│  └─ VariableDTO (process variables)              │
│                                                  │
│ Key API Endpoints:                               │
│  ├─ POST /processes/start                        │
│  ├─ GET /tasks (user tasks)                      │
│  ├─ POST /tasks/{id}/complete                    │
│  ├─ GET /tasks/{id}/form (get form data)         │
│  ├─ POST /tasks/{id}/submit (submit form)        │
│  ├─ GET /process/{id}/history                    │
│  ├─ GET /procedures (list administrative)        │
│  └─ POST /forms (create form)                    │
│                                                  │
│ Events Published:                                │
│  ├─ task.created                                 │
│  ├─ task.assigned                                │
│  ├─ task.completed                               │
│  ├─ process.started                              │
│  ├─ process.completed                            │
│  └─ process.cancelled                            │
└──────────────────────────────────────────────────┘
```

**Workflow Example - Autorizzazione (Authorization Process)**:
```
┌─────────────────────────────────────────────────────┐
│     Procedura: Autorizzazione Commerciale           │
│     Deadline: 30 giorni                             │
│     Silence: Positive (assenso tacito)              │
└──────────────────┬──────────────────────────────────┘
                   │
         Start Process (Client)
                   │
                   ▼
         ┌─────────────────────┐
         │ Receive Application │ (Service Task: Auto)
         │ Store in DB         │
         │ Generate Number     │
         └────────┬────────────┘
                  │
                  ▼
         ┌─────────────────────────────────┐
         │ Create Form for Officer Review  │ (User Task)
         │ - Form: Review Application      │
         │ - Assignee: Officer (Role)      │
         │ - Deadline: 5 days              │
         │ - Status: PENDING REVIEW        │
         └────────┬────────────────────────┘
                  │
      ┌───────────┴───────────┐
      │                       │
   APPROVE                  REJECT
      │                       │
      ▼                       ▼
  ┌────────────┐         ┌──────────────┐
  │ Send Email │         │ Send Rejection
  │ (RabbitMQ) │         │ (RabbitMQ)    │
  │ To: Client │         │ To: Client    │
  └────────┬───┘         └────────┬──────┘
           │                      │
           ▼                      ▼
    ┌────────────────┐      ┌─────────────┐
    │ Close Process  │      │ Close Process
    │ Status: GRANTED      │ Status: DENIED
    └────────────────┘      └─────────────┘
           │                      │
           └──────────┬───────────┘
                      │
              Publish Event
              process.completed
                      │
                      ▼
           ┌──────────────────────┐
           │ ZenDocuments         │
           │ Update document      │
           │ Add metadata:        │
           │ - status: GRANTED    │
           │ - protocol_ref:...   │
           └──────────────────────┘
```

### 5. ZenMailroom (msazenmailroom)

**Responsabilità**: Gestione comunicazioni via email con integrazione documentale

```
┌──────────────────────────────────────────────────┐
│         ZenMailroom Microservice                 │
├──────────────────────────────────────────────────┤
│ Core Responsibilities:                           │
│  ├─ Email Reception                              │
│  │  ├─ IMAP/POP3 polling                         │
│  │  ├─ Attachment download                       │
│  │  ├─ Email parsing                             │
│  │  └─ Automatic document creation               │
│  ├─ Email Sending                                │
│  │  ├─ SMTP with authentication                  │
│  │  ├─ PEC (Posta Elettronica Certificata)       │
│  │  ├─ Template support                          │
│  │  └─ Batch sending                             │
│  ├─ Email Signatures                             │
│  │  ├─ HTML signatures                           │
│  │  └─ Company branding                          │
│  ├─ Automatic Protocol Registration              │
│  │  ├─ Detect incoming mail                      │
│  │  └─ Register automatically as INPUT protocol  │
│  └─ Email Parameter Management                   │
│     ├─ IMAP/SMTP credentials                     │
│     ├─ OAuth for Gmail/Office365                 │
│     └─ Tenant-specific configurations            │
│                                                  │
│ DTOs (13 files):                                 │
│  ├─ EmailDTO (send/receive)                      │
│  ├─ EmailParameterDTO (configuration)            │
│  ├─ OauthEmailParameterDTO                       │
│  ├─ EmailSignatureDTO                            │
│  ├─ ReceivingLogDTO (history)                    │
│  └─ SendingLogDTO (history)                      │
│                                                  │
│ Key API Endpoints:                               │
│  ├─ POST /emails/send                            │
│  ├─ GET /emails/received                         │
│  ├─ GET /email-parameters                        │
│  ├─ POST /email-parameters                       │
│  ├─ PUT /email-signatures/{id}                   │
│  ├─ GET /receiving-logs                          │
│  └─ GET /sending-logs                            │
│                                                  │
│ Events Published:                                │
│  ├─ email.received                               │
│  ├─ email.sent                                   │
│  ├─ email.failed                                 │
│  ├─ document.auto_created (from email)           │
│  └─ protocol.auto_registered (from email)        │
└──────────────────────────────────────────────────┘
```

**Email to Document Flow**:
```
┌────────────────────┐
│ External Sender    │
│ sender@external.com
└─────────┬──────────┘
          │ (Email + Attachments)
          ▼
   ┌──────────────────────────┐
   │ ZenMailroom              │
   │ ├─ Connect to IMAP       │
   │ ├─ Retrieve email        │
   │ ├─ Parse content         │
   │ └─ Download attachments  │
   └──────┬───────────────────┘
          │
          ▼
   ┌────────────────────────────────┐
   │ Automatic Processing           │
   ├────────────────────────────────┤
   │ 1. Create Document             │
   │    - Store in SFTPGo           │
   │    - Add metadata              │
   │    └─ Subject: Email subject   │
   │    └─ Sender: Email from       │
   │                                 │
   │ 2. Register Protocol (if       │
   │    configured)                  │
   │    - Type: INPUT               │
   │    - Correspondent: Sender     │
   │    - Document: Created above   │
   │                                 │
   │ 3. Route Document              │
   │    - Via smistamento if rules  │
   │    - Or store in folder        │
   │                                 │
   │ 4. Send Notification           │
   │    - To: Configured recipient  │
   │    - Content: Email received   │
   └──────┬──────────────────────────┘
          │
          ▼
   ┌──────────────────┐
   │ Inbox Updated    │
   │ User can:        │
   │ ├─ View document │
   │ ├─ Download      │
   │ ├─ Comment       │
   │ └─ Forward       │
   └──────────────────┘
```

### 6. ZenMaster (msazenmaster)

**Responsabilità**: Gestione tenants e licenze

```
┌──────────────────────────────────┐
│    ZenMaster Microservice        │
├──────────────────────────────────┤
│ Core Entities:                   │
│  ├─ Tenants                      │
│  │  ├─ ID, Name                  │
│  │  ├─ Database connection       │
│  │  │  ├─ Host, Port             │
│  │  │  ├─ Database name          │
│  │  │  └─ Credentials            │
│  │  ├─ OAuth/JWT settings        │
│  │  ├─ Storage account (Azure)   │
│  │  └─ License                   │
│  ├─ Licenses                     │
│  │  ├─ License type              │
│  │  ├─ Expiration                │
│  │  ├─ User seats                │
│  │  └─ Features enabled          │
│  └─ Events                       │
│     ├─ Audit trail               │
│     └─ System events             │
│                                  │
│ DTOs (5 files):                  │
│  ├─ TenantDTO                    │
│  ├─ AddTenantRequestDTO          │
│  ├─ LicenzaAttivaFiltrataDTO     │
│  └─ EventDTO                     │
│                                  │
│ Key API Endpoints:               │
│  ├─ POST /tenants (create)       │
│  ├─ GET /tenants/{id}            │
│  ├─ PUT /tenants/{id}            │
│  ├─ GET /licenses                │
│  └─ POST /maintenance            │
│                                  │
│ Multi-tenant Architecture:       │
│ ┌────────────────────────────┐   │
│ │ Per-Tenant Database        │   │
│ │ ├─ postgres1 (Tenant-A)    │   │
│ │ ├─ postgres2 (Tenant-B)    │   │
│ │ └─ postgres3 (Tenant-C)    │   │
│ └────────────────────────────┘   │
│                                  │
│ API Gateway uses Tenant ID       │
│ from JWT token to route to       │
│ correct database                 │
└──────────────────────────────────┘
```

### 7. ZenSuap (msazensuap)

**Responsabilità**: Integrazione con Sportelli Unici delle Attività Produttive

```
┌─────────────────────────────────────┐
│      ZenSuap Microservice           │
├─────────────────────────────────────┤
│ Purpose:                            │
│ Bridge between ZenShareUp and SUAP  │
│ Backoffice systems                  │
│                                     │
│ Core Responsibilities:              │
│  ├─ Receive integration requests    │
│  ├─ Transform data formats          │
│  ├─ Send to SUAP Backoffice         │
│  ├─ Receive responses               │
│  └─ Update documents/protocols      │
│                                     │
│ DTOs (7 files):                     │
│  ├─ IntegrationRequestDTO           │
│  ├─ RequestCdssDTO                  │
│  ├─ SendConclusionsRequestDTO       │
│  └─ SuapJournalDTO                  │
│                                     │
│ Key API Endpoints:                  │
│  ├─ POST /integration/send          │
│  ├─ GET /integration/status         │
│  ├─ POST /conclusions/send          │
│  └─ GET /journal                    │
│                                     │
│ Events Published:                   │
│  ├─ suap.request.sent               │
│  ├─ suap.response.received          │
│  └─ suap.error                      │
└─────────────────────────────────────┘
```

### 8. ZenScheduler (zenscheduler)

**Responsabilità**: Pianificazione e esecuzione di task ricorrenti

```
┌──────────────────────────────────────┐
│      ZenScheduler Microservice       │
├──────────────────────────────────────┤
│ Purpose:                             │
│ Execute scheduled operations across  │
│ all microservices                    │
│                                      │
│ Typical Scheduled Tasks:             │
│  ├─ Document Archival                │
│  │  ├─ Move to legal archive         │
│  │  ├─ Apply retention policies      │
│  │  └─ Cleanup old versions          │
│  ├─ Email Polling                    │
│  │  ├─ Check IMAP every 5 min        │
│  │  ├─ Process new emails            │
│  │  └─ Retry failed sends            │
│  ├─ Workflow Cleanup                 │
│  │  ├─ Complete stale tasks          │
│  │  ├─ Send escalation emails        │
│  │  └─ Archive closed instances      │
│  ├─ Protocol Management              │
│  │  ├─ Process deadline expirations  │
│  │  ├─ Apply silence rules           │
│  │  └─ Auto-close procedures         │
│  ├─ Cache Invalidation               │
│  │  ├─ Refresh lookup tables         │
│  │  └─ Clear expired entries         │
│  ├─ Backup & Maintenance             │
│  │  ├─ Database backup               │
│  │  ├─ Log rotation                  │
│  │  └─ Performance optimization      │
│  ├─ Report Generation                │
│  │  ├─ Daily/weekly reports          │
│  │  └─ Compliance reports            │
│  └─ Notification Sending             │
│     ├─ Digest emails                 │
│     └─ Alert notifications           │
│                                      │
│ Implementation:                      │
│  ├─ Quartz Scheduler                 │
│  ├─ Spring Task Scheduler             │
│  └─ Message-driven (RabbitMQ)        │
│                                      │
│ Configuration:                       │
│  ├─ Cron expressions                 │
│  ├─ Fixed delays                     │
│  └─ One-time tasks                   │
└──────────────────────────────────────┘
```

---

## Servizi di Supporto

### 1. Keycloak - Identity & Access Management

```
┌──────────────────────────────────────────┐
│           Keycloak                       │
├──────────────────────────────────────────┤
│ Capabilities:                            │
│  ├─ User Authentication                  │
│  │  ├─ Username/Password                 │
│  │  ├─ LDAP/Active Directory              │
│  │  ├─ Social login (Google, GitHub)      │
│  │  └─ Multi-factor authentication        │
│  ├─ Role-Based Access Control (RBAC)     │
│  │  ├─ Assign roles to users              │
│  │  ├─ Map roles to permissions           │
│  │  └─ Hierarchical roles                 │
│  ├─ OAuth 2.0 / OpenID Connect           │
│  │  ├─ Token generation                   │
│  │  ├─ Token validation                   │
│  │  └─ Refresh tokens                     │
│  ├─ User Management                      │
│  │  ├─ Create/update/delete users         │
│  │  ├─ Manage passwords                   │
│  │  └─ User sessions                      │
│  └─ Audit Logs                           │
│     ├─ Login attempts                     │
│     ├─ Role changes                       │
│     └─ Permission updates                 │
│                                          │
│ JWT Token Flow:                          │
│                                          │
│ 1. Login Request                         │
│    POST /auth/realms/zenshareup/protocol/openid-connect/token
│    {                                     │
│      "client_id": "zenshareup-api"       │
│      "username": "mario.rossi"           │
│      "password": "secret123"             │
│    }                                     │
│                                          │
│ 2. Token Response                        │
│    {                                     │
│      "access_token": "eyJ0...",           │
│      "expires_in": 3600,                  │
│      "refresh_token": "eyJ0...",          │
│      "token_type": "Bearer"               │
│    }                                     │
│                                          │
│ 3. Use Token in Requests                 │
│    GET /documents                        │
│    Authorization: Bearer eyJ0...        │
│                                          │
│ 4. API Gateway Validates                 │
│    ├─ Check signature                    │
│    ├─ Verify not expired                 │
│    ├─ Extract user info                  │
│    └─ Extract roles/permissions          │
└──────────────────────────────────────────┘
```

### 2. PostgreSQL - Primary Database

- Multi-schema architecture per tenant
- JSONB columns per metadata flessibile
- Full-text search indexes
- Audit trigger logging
- Replication per HA

### 3. Redis - Distributed Cache

- Session store
- User/group/company lookup cache
- Distributed locks
- Rate limiting data
- Temporary operation tracking

### 4. RabbitMQ - Message Broker

- Reliable message delivery
- Topic exchanges per service
- Dead letter queues per failed messages
- Message TTL e durability
- Consumer groups per processing

### 5. SFTPGo - Secure File Storage

- SFTP/WebDAV access
- Multi-tenant file segregation
- Automatic backups
- Virus scanning integration
- Encryption at rest

---

## DTO e Data Model

### DTO Hierarchy Completa

```
┌─────────────────────────────────────────┐
│        BaseDTO<T> (unused)              │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│     TrackBasicChangesDTO                │
│  (createdBy, modifiedBy, dates)         │
│                                         │
│  └─ TrackBasicChangesDTOHasID<PK>       │
│      ├─ TrackBasicChangesDTOHasLongID   │
│      │   └─ [Most Entity DTOs]          │
│      │       ├─ UserDTO                 │
│      │       ├─ CompanyDTO              │
│      │       ├─ GroupDTO                │
│      │       ├─ ProtocolDTO             │
│      │       ├─ DocumentDTO             │
│      │       ├─ FolderDTO               │
│      │       ├─ ModelDTO                │
│      │       ├─ AdministrativeProcedureDTO
│      │       └─ [65+ more entity DTOs]  │
│      │                                  │
│      └─ AdminLookupDTO                  │
│          (admin lookup tables)          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│    LookupElementDTOBase<T, PK>          │
│  (id, code, description, name)          │
│                                         │
│  ├─ LookupElementDTOLong<T>             │
│  │   ├─ UtenteTrackBasicChangesDTO      │
│  │   ├─ GroupTrackBasicChangesDTO       │
│  │   ├─ CompanyTrackBasicChangesDTO     │
│  │   └─ ProtAOOTrackBasicChangesDTO     │
│  │                                      │
│  └─ LookupElementDTOString<T>           │
│      (for string PKs)                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  TableLookupEntityDTOGBase<T, PK>       │
│  (extends TrackBasicChangesDTO +        │
│   code/description for lookup tables)   │
│                                         │
│  └─ TableLookupEntityDTOGLongPK<T>      │
│      ├─ CompanyDTO                      │
│      ├─ GroupDTO                        │
│      └─ [Other lookup table DTOs]       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│      Utility DTOs                       │
├─────────────────────────────────────────┤
│  ├─ PagedResponseDTO<T>                 │
│  │  (paginated list results)            │
│  ├─ FilterDTO                           │
│  │  (dynamic filtering criteria)        │
│  └─ MapperConfigurationBase             │
│     (DTO ↔ Entity mapping)              │
└─────────────────────────────────────────┘
```

### DTO Naming Conventions

| Pattern | Usage | Example |
|---------|-------|---------|
| `[Entity]DTO` | Full entity | `UserDTO`, `DocumentDTO` |
| `[Entity]CreateDTO` | Input for creation | `DocumentCreateDTO` |
| `[Entity]RegistrationDTO` | Specialized create | `ProtocolRegistrationDTO` |
| `[Entity]OutDTO` | Output/read | `ClassificationOutDTO` |
| `[Entity]PatchDTO` | Partial update | `DocumentPatchDTO` |
| `[Entity]SearchDTO` | Search criteria | `DocumentSearchDTO` |
| `[Entity]LookupDTO` | Reference only | `AdminLookupDTO` |
| `[Entity]BaseDTO` | Shared base props | `DocumentBaseDTO` |
| `PagedResponseDTO<T>` | Paginated results | `PagedResponseDTO<DocumentDTO>` |

---

## Flussi Applicativi

### Flusso 1: Creazione e Protocollazione di Documento

```
CLIENTE FINAL
    │
    ├─► 1. Upload Document (ZenDocuments)
    │       POST /documents
    │       ├─ File upload
    │       ├─ Metadata (subject, model)
    │       └─ Response: DocumentDTO
    │
    ├─► 2. Assign to Colleague (Smistamento)
    │       POST /documents/{id}/assign
    │       ├─ Assignee: User/Group/Role
    │       ├─ Action: Review/Sign/Approve
    │       └─ Deadline: 5 days
    │
    ├─► 3. Assignee Reviews & Approves
    │       PUT /documents/{id}/comment
    │       POST /documents/{id}/approve
    │
    ├─► 4. Create New Version (if edits)
    │       POST /documents/{id}/version
    │       ├─ Updated file
    │       └─ Response: New version
    │
    └─► 5. Register Protocol
            POST /protocols/register
            ├─ Main Document ID
            ├─ Confidentiality Level
            ├─ Correspondents
            └─ Classification Path
            │
            ▼ (ZenProtocollo)
            ├─ Validate all inputs
            ├─ Generate Protocol Number
            ├─ Create Protocol Record
            └─ Link to Document
            │
            ▼ (Event: protocol.registered)
            ├─ ZenDocuments updates doc status
            ├─ ZenMailroom sends email
            └─ ZenScheduler schedules archive
            │
            Response: ProtocolDTO with number
            {
              "protocolNumber": "2024/001234",
              "registrationDate": "2024-11-20T10:35:00Z"
            }
```

### Flusso 2: Ricezione Email e Auto-registrazione Protocollo

```
EXTERNAL SENDER
    │
    ├─► Email sent to: ricevute@company.it
    │
    ▼ (ZenMailroom - Scheduled every 5 min)
    ├─ Connect to IMAP mailbox
    ├─ Retrieve new emails
    ├─ Download attachments
    ├─ Parse sender info
    │
    ▼ For each email:
    ├─► 1. Create Document (ZenDocuments)
    │       ├─ Store email body as file
    │       ├─ Store attachments
    │       ├─ Add metadata:
    │       │  ├─ Subject: from email subject
    │       │  ├─ Sender: from email
    │       │  └─ ReceivedDate: email date
    │       └─ Response: DocumentDTO
    │
    ├─► 2. Register Protocol (ZenProtocollo)
    │       ├─ Type: INPUT
    │       ├─ Main Document: from step 1
    │       ├─ Correspondent: email sender
    │       └─ Auto protocol registration
    │
    ├─► 3. Route Document (Smistamento)
    │       ├─ Check routing rules
    │       ├─ Assign to officer if rule matches
    │       └─ Or store in inbox
    │
    ├─► 4. Send Notification
    │       ├─ To: assigned user or inbox owner
    │       ├─ Subject: "New email received"
    │       └─ Link to document
    │
    ▼ RESULT in Dashboard:
    User sees:
    ├─ New document
    ├─ From: sender email
    ├─ Protocol#: 2024/001235
    ├─ Subject: email subject
    ├─ Attachments: list
    └─ Action: Review/Comment/Forward
```

### Flusso 3: Workflow Amministrativo (Autorizzazione)

```
CITIZEN / COMPANY
    │
    ├─► 1. Start Process (ZenProcess)
    │       POST /processes/start
    │       ├─ Process: "Authorization"
    │       └─ Input variables: company_data
    │
    ▼ (Process Instance Created)
    ├─► 2. User Task: Submit Application
    │       ├─ Form: Autorizzazione form
    │       ├─ Fields: azienda, address, activity
    │       └─ Submit: POST /tasks/{id}/submit
    │
    ├─► 3. Automatic Task: Validate
    │       (Service Task)
    │       ├─ Business rules validation
    │       ├─ Document checks
    │       └─ If invalid: notify applicant
    │
    ├─► 4. User Task: Officer Review
    │       ├─ Form: Review & Decision
    │       ├─ Assignee: Officer (role-based)
    │       ├─ Actions:
    │       │  ├─ APPROVE
    │       │  ├─ REQUEST_INFO
    │       │  └─ REJECT
    │       └─ Deadline: 30 days (process deadline)
    │
    ├─► 5a. If APPROVED:
    │       ├─ Document status: GRANTED
    │       ├─ Send authorization letter
    │       ├─ Register as OUTPUT protocol
    │       └─ Close process
    │
    ├─► 5b. If REJECTED:
    │       ├─ Document status: DENIED
    │       ├─ Send rejection notice
    │       ├─ Allow appeal process
    │       └─ Close process
    │
    ├─► 5c. If REQUEST_INFO:
    │       ├─ Send request to applicant
    │       ├─ Wait for response (deadline: 10 days)
    │       └─ If response: return to Officer Review
    │       └─ If no response: auto-REJECT
    │
    ▼ (Process Complete)
    ├─ Citizen receives decision
    ├─ Authority archives decision
    └─ Scheduler records metrics
```

---

## Integrazione tra Servizi

### Service-to-Service Communication

```
┌─────────────────────────────────────────────────────────┐
│                 REST API Direct Calls                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ ZenProtocollo needs document info:                      │
│                                                         │
│   ZenProtocollo ─────────────────────────────►          │
│                  GET /documents/{doc_id}                │
│                                                         │
│                  ◄─────────────────────────── ZenDocuments
│                  DocumentDTO with metadata              │
│                                                         │
│ Authentication: Service JWT token (server-to-server)   │
│ Timeout: 5 seconds                                      │
│ Retry: 2x with exponential backoff                      │
│ Circuit breaker: If 3 failures in 60s, fail fast       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│             Event-Based Async Communication            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Document Registered Event:                              │
│                                                         │
│ ZenDocuments Publisher:                                 │
│     document.created ─────┐                            │
│                           │                            │
│                    RabbitMQ Exchange                     │
│                   (documents.topic)                      │
│                           │                            │
│                    ┌──────┴──────┬──────────────┐        │
│                    │             │              │        │
│              Queue-A       Queue-B         Queue-C        │
│                    │             │              │        │
│                    ▼             ▼              ▼        │
│             ZenProtocollo  ZenMailroom    ZenScheduler   │
│             (register as   (send notify)   (schedule      │
│              protocol)                      archive)      │
│                                                         │
│ Advantages:                                             │
│ ├─ Decoupled services                                   │
│ ├─ Retry on failure (dead letter queue)                │
│ ├─ Audit trail of all events                           │
│ └─ Horizontal scaling of consumers                     │
└─────────────────────────────────────────────────────────┘
```

### Event Publish/Subscribe Pattern

```
┌──────────────────────────────────────────────────┐
│         Documents Topic Exchange                 │
│  zenshareup.documents (fanout or topic)          │
├──────────────────────────────────────────────────┤
│                                                  │
│ Events:                                          │
│  ├─ document.created                             │
│  ├─ document.updated                             │
│  ├─ document.versioned                           │
│  ├─ document.assigned (smistamento)              │
│  ├─ document.archived                            │
│  └─ document.deleted                             │
│                                                  │
│ Subscribers (Queues):                            │
│  ├─ zenshareup.documents.search                  │
│  │  └─ Indexer (full-text search)                │
│  ├─ zenshareup.documents.audit                   │
│  │  └─ Audit Service (compliance)                │
│  ├─ zenshareup.documents.archive                 │
│  │  └─ ZenScheduler (auto-archive)               │
│  ├─ zenshareup.documents.notification            │
│  │  └─ Notification Service (email alerts)       │
│  └─ zenshareup.documents.protocol                │
│     └─ ZenProtocollo (link to protocol)          │
│                                                  │
│ Message Format (RabbitMQ):                       │
│ {                                                │
│   "eventId": "evt_12345",                        │
│   "eventType": "document.created",               │
│   "timestamp": "2024-11-20T10:30:00Z",           │
│   "tenantId": "tenant_001",                      │
│   "userId": "user_123",                          │
│   "sourceService": "ZenDocuments",               │
│   "payload": {                                   │
│     "documentId": "doc_12345",                   │
│     "fileName": "invoice.pdf",                   │
│     "folderId": "folder_001",                    │
│     "modelId": "invoice_template"                │
│   }                                              │
│ }                                                │
└──────────────────────────────────────────────────┘
```

---

## Sicurezza e Multi-tenancy

### Multi-Tenancy Architecture

```
┌────────────────────────────────────────────────┐
│         ZenMaster Service                      │
│     (Tenant Management)                        │
├────────────────────────────────────────────────┤
│ Configured Tenants:                            │
│  ├─ Tenant A (Comune di Roma)                  │
│  │  ├─ Database: postgres_roma                 │
│  │  ├─ Storage: sftp/tenant-roma               │
│  │  └─ License: Enterprise (unlimited users)   │
│  ├─ Tenant B (Comune di Milano)                │
│  │  ├─ Database: postgres_milano               │
│  │  ├─ Storage: sftp/tenant-milano             │
│  │  └─ License: Professional (50 users)        │
│  └─ Tenant C (Private Company)                 │
│     ├─ Database: postgres_company              │
│     ├─ Storage: sftp/tenant-company            │
│     └─ License: Starter (10 users)             │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│     API Gateway (msacloudgateway)              │
│  Tenant Routing                                │
├────────────────────────────────────────────────┤
│                                                │
│ Client Request with JWT:                       │
│ {                                              │
│   "iss": "https://keycloak/realms/...",        │
│   "sub": "user_id",                            │
│   "aud": "zenshareup-api",                     │
│   "tenant_id": "tenant_A",  ◄── KEY            │
│   "roles": ["USER", "DOC_MANAGER"],            │
│   "exp": 1734769800                            │
│ }                                              │
│                                                │
│ Gateway extracts tenant_id and routes to:      │
│ ├─ PostgreSQL connection pool (tenant_A DB)   │
│ ├─ Redis cache key prefix (tenant_A:...)      │
│ ├─ SFTP folder (sftp/tenant-a/...)            │
│ └─ RabbitMQ queue (tenant_A.events)           │
│                                                │
│ Result:                                        │
│ User A sees only Tenant A data                 │
│ User B sees only Tenant B data                 │
│ Complete data isolation                        │
└────────────────────────────────────────────────┘
```

### Security Layers

```
┌───────────────────────────────────────────────────┐
│          ZENSHAREUP SECURITY MODEL                │
├───────────────────────────────────────────────────┤
│                                                   │
│ 1. PERIMETER SECURITY (API Gateway)              │
│    ├─ TLS/HTTPS only (no HTTP)                   │
│    ├─ CORS policy enforcement                    │
│    ├─ Rate limiting (per user/IP)                │
│    ├─ DDoS protection                            │
│    └─ WAF rules                                  │
│                                                   │
│ 2. AUTHENTICATION & AUTHORIZATION                │
│    ├─ OAuth 2.0 / OpenID Connect                 │
│    ├─ JWT token validation                       │
│    ├─ Multi-factor authentication (optional)     │
│    ├─ Role-Based Access Control (RBAC)           │
│    │  ├─ User roles (Admin, Manager, User)       │
│    │  ├─ Document permissions                    │
│    │  ├─ Protocol responsibility                 │
│    │  └─ Workflow task assignment                │
│    └─ Tenant isolation via tenant_id in JWT      │
│                                                   │
│ 3. DATA SECURITY                                 │
│    ├─ Database encryption at rest (PostgreSQL)   │
│    ├─ Field-level encryption for sensitive data  │
│    ├─ File encryption in SFTPGo                  │
│    ├─ Encrypted connections (TLS)                │
│    └─ Secure password hashing (bcrypt)           │
│                                                   │
│ 4. AUDIT & COMPLIANCE                            │
│    ├─ All data changes logged                    │
│    ├─ createdBy/modifiedBy tracking              │
│    ├─ Timestamp audit trails                     │
│    ├─ Event audit log (RabbitMQ)                 │
│    ├─ Legal archive (GDPR compliance)            │
│    └─ Retention policies enforcement             │
│                                                   │
│ 5. API SECURITY                                  │
│    ├─ Input validation & sanitization            │
│    ├─ SQL injection prevention (Parameterized)   │
│    ├─ XSS prevention (output encoding)           │
│    ├─ CSRF protection (token validation)         │
│    └─ Secure headers (HSTS, CSP, etc.)           │
│                                                   │
│ 6. INFRASTRUCTURE SECURITY                       │
│    ├─ Network segmentation (microservices)       │
│    ├─ Database firewall rules                    │
│    ├─ Service-to-service auth (JWT)              │
│    ├─ Secrets management (vault)                 │
│    └─ Regular security updates                   │
└───────────────────────────────────────────────────┘
```

### Permission Model

```
┌─────────────────────────────────────────────────┐
│         Permission Hierarchy                    │
├─────────────────────────────────────────────────┤
│                                                 │
│ ROLES:                                          │
│  ├─ ADMIN                                       │
│  │  └─ Full system access, tenant management    │
│  ├─ DOCUMENT_MANAGER                            │
│  │  └─ Create, edit, delete, assign documents   │
│  ├─ PROTOCOL_MANAGER                            │
│  │  └─ Register, manage, close protocols        │
│  ├─ WORKFLOW_MANAGER                            │
│  │  └─ Create procedures, assign tasks          │
│  └─ USER                                        │
│     └─ View assigned documents, complete tasks  │
│                                                 │
│ DOCUMENT PERMISSIONS (per document):            │
│  ├─ VIEW: Can see document                      │
│  ├─ EDIT: Can modify metadata/content           │
│  ├─ DELETE: Can delete                          │
│  ├─ ASSIGN: Can assign to others                │
│  ├─ VERSION: Can create new versions            │
│  └─ ARCHIVE: Can archive                        │
│                                                 │
│ PROTOCOL PERMISSIONS (per protocol):            │
│  ├─ VIEW: Can see protocol details              │
│  ├─ MANAGE: Can edit metadata                   │
│  ├─ CLOSE: Can close protocol                   │
│  ├─ CANCEL: Can cancel protocol                 │
│  └─ EXPORT: Can export data                     │
│                                                 │
│ WORKFLOW PERMISSIONS:                           │
│  ├─ VIEW_TASKS: Can see assigned tasks          │
│  ├─ CLAIM_TASK: Can claim unassigned tasks      │
│  ├─ COMPLETE_TASK: Can complete/submit          │
│  ├─ DELEGATE_TASK: Can delegate to others       │
│  └─ REASSIGN_TASK: Can reassign                 │
└─────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│            Docker/Kubernetes Deployment                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Load Balancer                                          │
│  ├─ nginx / HAProxy                                     │
│  └─ TLS termination                                     │
│       │                                                 │
│       ├─────► Pod: API Gateway (msacloudgateway)        │
│       ├─────► Pod: Keycloak                             │
│       │                                                 │
│       └─────► Service Mesh (Istio)                      │
│              ├─ Pod: ZenAdmin                           │
│              ├─ Pod: ZenDocuments (replicas: 3)        │
│              ├─ Pod: ZenProtocollo (replicas: 2)       │
│              ├─ Pod: ZenMailroom (replicas: 2)         │
│              ├─ Pod: ZenProcess                         │
│              ├─ Pod: ZenScheduler                       │
│              ├─ Pod: ZenSuap                            │
│              └─ Pod: ZenMaster                          │
│                                                         │
│  StatefulSet:                                           │
│  ├─ PostgreSQL (Primary + Standby)                      │
│  ├─ Redis (Master + Replicas)                           │
│  ├─ RabbitMQ (Cluster)                                  │
│  └─ SFTPGo (Replicated Storage)                         │
│                                                         │
│  ConfigMaps/Secrets:                                    │
│  ├─ Database credentials                               │
│  ├─ JWT signing keys                                   │
│  ├─ Email SMTP settings                                │
│  ├─ OAuth client credentials                           │
│  └─ Feature flags                                       │
│                                                         │
│  Storage:                                               │
│  ├─ PersistentVolume: PostgreSQL data                   │
│  ├─ PersistentVolume: Redis data                        │
│  ├─ PersistentVolume: RabbitMQ messages                │
│  └─ S3/Azure Blob: Document backup                      │
└─────────────────────────────────────────────────────────┘
```

---

## Metriche di Monitoraggio

```
┌──────────────────────────────────────────────┐
│      Key Performance Indicators (KPI)        │
├──────────────────────────────────────────────┤
│                                              │
│ PERFORMANCE:                                 │
│  ├─ API response time: < 500ms (p99)         │
│  ├─ Document upload: < 2s for 10MB          │
│  ├─ Search results: < 1s (1000 docs)         │
│  ├─ Protocol registration: < 3s              │
│  └─ Email processing: < 5s per message       │
│                                              │
│ AVAILABILITY:                                │
│  ├─ System uptime: 99.9%                     │
│  ├─ API availability: 99.95%                 │
│  ├─ Database availability: 99.95%            │
│  └─ RTO (Recovery Time): < 15 min            │
│                                              │
│ CAPACITY:                                    │
│  ├─ Concurrent users: 1000+                  │
│  ├─ Documents per day: 10,000+               │
│  ├─ Protocols per day: 5,000+                │
│  ├─ Workflows per day: 2,000+                │
│  └─ Storage growth: 100GB+/month             │
│                                              │
│ RELIABILITY:                                 │
│  ├─ Error rate: < 0.1%                       │
│  ├─ Failed document uploads: < 0.01%         │
│  ├─ Failed protocol registrations: < 0.01%   │
│  └─ Message loss: 0%                         │
└──────────────────────────────────────────────┘
```

---

## Conclusione

ZenShareUp è una piattaforma enterprise **moderna, scalabile e sicura** per la gestione documentale integrata.

**Punti di Forza**:
- ✅ Architettura a microservizi decoupled
- ✅ Comunicazione asincrona via eventi
- ✅ Multi-tenancy nativa
- ✅ Compliance normativo (audit trail, legal archive)
- ✅ Scalabilità orizzontale
- ✅ Alta disponibilità e disaster recovery
- ✅ Security by design

**Componenti Chiave**:
1. **API Gateway** - Autenticazione e routing
2. **8 Microservizi** - Funzionalità specifiche
3. **PostgreSQL** - Persistenza dati
4. **Redis** - Cache distribuito
5. **RabbitMQ** - Event bus asincrono
6. **SFTPGo** - Storage documentale
7. **Keycloak** - Identity management

Questa architettura supporta la gestione di **centinaia di migliaia di documenti** con **conformità normativa italiana** e **protezione dati GDPR**.
