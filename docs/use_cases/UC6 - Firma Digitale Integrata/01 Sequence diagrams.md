# Sequence Diagrams - UC6 Firma Digitale Integrata

## Diagramma Completo del Processo Firma

```mermaid
sequenceDiagram
    participant U as Utente
    participant SP31 as SP31 Workflow
    participant SP31 as SP31 Certificate Manager
    participant SP31 as SP31 Signature Engine
    participant SP32 as SP32 Validation
    participant PROVIDER as Signature Provider
    participant DB as Database
    participant AUDIT as Audit Log

    U->>SP31: Richiesta firma documento
    SP31->>SP30: Verifica certificato utente
    SP31->>SP30: Controlla validità certificato
    SP31-->>SP31: Certificato valido

    SP31->>SP31: Crea workflow firma
    SP31->>DB: Salva workflow
    DB-->>SP31: Workflow creato
    SP31->>AUDIT: Log creazione workflow

    SP31->>SP29: Richiedi firma
    SP31->>SP30: Ottieni certificato
    SP31-->>SP29: Certificato + chiave
    SP31->>PROVIDER: Esegui firma digitale
    PROVIDER->>PROVIDER: Firma crittografica
    PROVIDER-->>SP29: Firma completata

    SP31->>SP29: Applica timestamp
    SP31->>DB: Salva firma
    DB-->>SP29: Firma salvata
    SP31-->>SP31: Firma completata

    SP31->>SP32: Valida firma
    SP32->>SP32: Verifica crittografica
    SP32->>SP32: Controlla compliance
    SP32-->>SP31: Validazione positiva
    SP31->>AUDIT: Log completamento

    SP31-->>U: Documento firmato disponibile
```

## Diagramma di Gestione Certificati

```mermaid
sequenceDiagram
    participant USER as Utente
    participant SP31 as Certificate Manager
    participant CA as Certificate Authority
    participant HSM as Hardware Security Module
    participant VAULT as HashiCorp Vault
    participant MONITOR as Monitoring System

    USER->>SP30: Richiesta nuovo certificato
    SP31->>SP30: Valida richiesta
    SP31->>HSM: Genera chiave privata
    HSM-->>SP30: Chiave generata
    SP31->>VAULT: Store chiave sicura
    VAULT-->>SP30: Chiave stored

    SP31->>SP30: Crea CSR
    SP31->>CA: Invia richiesta certificato
    CA->>CA: Valida identità
    CA-->>SP30: Certificato emesso
    SP31->>VAULT: Store certificato
    VAULT-->>SP30: Certificato stored

    SP31->>MONITOR: Schedule monitoraggio scadenza
    MONITOR-->>SP30: Monitoring attivo
    SP31-->>USER: Certificato pronto

    MONITOR->>MONITOR: Controlla scadenza
    MONITOR->>SP30: Alert scadenza imminente
    SP31->>SP30: Avvia rinnovo automatico
    SP31->>CA: Richiesta rinnovo
    CA-->>SP30: Certificato rinnovato
```

## Diagramma di Workflow Firma Multi-Firmatari

```mermaid
sequenceDiagram
    participant INITIATOR as Iniziatore
    participant SP31 as Signature Workflow
    participant SIGNER1 as Firmatario 1
    participant SIGNER2 as Firmatario 2
    participant SP31 as Signature Engine
    participant NOTIFICATION as Notification Service

    INITIATOR->>SP31: Crea workflow sequenziale
    SP31->>SP31: Configura sequenza firma
    SP31->>NOTIFICATION: Notifica primo firmatario
    NOTIFICATION-->>SIGNER1: Richiesta firma

    SIGNER1->>SP31: Firma documento
    SP31->>SP29: Esegui firma
    SP31->>SP29: Applica firma digitale
    SP31-->>SP31: Firma completata
    SP31->>NOTIFICATION: Notifica secondo firmatario
    NOTIFICATION-->>SIGNER2: Richiesta firma

    SIGNER2->>SP31: Firma documento
    SP31->>SP29: Esegui firma
    SP31->>SP29: Applica firma digitale
    SP31-->>SP31: Firma completata
    SP31->>SP31: Verifica completamento workflow
    SP31-->>INITIATOR: Workflow completato
```

## Diagramma di Validazione Firma

```mermaid
sequenceDiagram
    participant REQUESTER as Richiedente
    participant SP32 as Signature Validation
    participant DSS as DSS Framework
    participant OCSP as OCSP Responder
    participant TSA as Timestamp Authority
    participant BLOCKCHAIN as Blockchain Notary

    REQUESTER->>SP32: Richiesta validazione
    SP32->>DSS: Inizia validazione
    DSS->>DSS: Estrai firma documento
    DSS->>OCSP: Verifica revoca certificato
    OCSP-->>DSS: Status certificato
    DSS->>DSS: Verifica firma crittografica
    DSS-->>SP32: Risultato validazione base

    SP32->>TSA: Valida timestamp
    TSA-->>SP32: Timestamp valido
    SP32->>SP32: Raccogli evidence LTV
    SP32->>BLOCKCHAIN: Notarizza evidence (optional)
    BLOCKCHAIN-->>SP32: Notarization receipt

    SP32->>SP32: Assessment compliance
    SP32->>DSS: Genera report dettagliato
    DSS-->>SP32: Validation report
    SP32-->>REQUESTER: Risultato validazione completo
```

## Diagramma di Escalation e Reminder

```mermaid
sequenceDiagram
    participant SP31 as Signature Workflow
    participant SCHEDULER as Task Scheduler
    participant SIGNER as Firmatario
    participant NOTIFICATION as Notification Service
    participant ESCALATION as Escalation Manager

    SP31->>SCHEDULER: Schedule reminder
    SCHEDULER->>SCHEDULER: Attendi deadline reminder
    SCHEDULER->>NOTIFICATION: Invia reminder
    NOTIFICATION-->>SIGNER: Reminder firma

    SCHEDULER->>SCHEDULER: Attendi deadline escalation
    SCHEDULER->>ESCALATION: Trigger escalation
    ESCALATION->>ESCALATION: Valuta escalation rules
    ESCALATION->>NOTIFICATION: Invia escalation
    NOTIFICATION-->>SIGNER: Escalation urgente

    alt Firmatario risponde
        SIGNER->>SP31: Firma documento
        SP31->>SCHEDULER: Cancella escalation
    else Timeout finale
        ESCALATION->>SP31: Auto-reject workflow
        SP31->>SP31: Chiudi workflow
    end
```

## Diagramma Ultra-Semplificato

```mermaid
sequenceDiagram
    participant User as Utente
    participant System as Sistema Firma

    User->>System: Carica documento
    System->>System: Verifica certificato
    System-->>User: Certificato OK

    User->>System: Avvia firma
    System->>System: Firma digitale
    System-->>User: Documento firmato

    User->>System: Valida firma
    System->>System: Verifica integrità
    System-->>User: Firma valida
```</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC6 - Firma Digitale Integrata/01 Sequence diagrams.md