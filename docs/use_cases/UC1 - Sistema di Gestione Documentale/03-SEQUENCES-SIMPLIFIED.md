# Sequence Diagram - Overview Semplificato (UC1)

## Panoramica Semplificata del Flusso Documentale

Questo diagramma mostra il flusso principale di processamento documenti in versione semplificata, focalizzandosi sui passaggi essenziali.

```mermaid
sequenceDiagram
    autonumber
    participant User
    participant SP15 as SP15 Orchestrator
    participant SP02 as SP02 Extractor
    participant SP07 as SP07 Classifier
    participant SP13 as SP13 Summarizer
    participant SP14 as SP14 Indexer
    participant SP12 as SP12 Search
    participant SP10 as SP10 Dashboard

    Note over User,SP10: Document Processing Overview

    User->>SP15: Upload Document
    SP15->>SP02: Extract Content
    SP02-->>SP15: Text & Metadata
    SP15->>SP07: Classify Document
    SP07-->>SP15: Type & Category
    SP15->>SP13: Generate Summary
    SP13-->>SP15: Summary & Key Points
    SP15->>SP14: Index Document
    SP14-->>SP15: Indexed
    SP15->>SP12: Enable Search
    SP12-->>SP15: Search Ready
    SP15->>SP10: Update Dashboard
    SP10-->>User: Document Processed

    rect rgb(200, 255, 200)
        Note over SP02,SP12: Pipeline Core<br/>Estrazione → Classificazione → Riassunto → Indicizzazione → Ricerca
    end
```

## Spiegazione dei Passaggi

### 1. Upload Documento
- Utente carica documento via interfaccia
- SP15 Orchestrator riceve e valida richiesta

### 2. Estrazione Contenuto
- SP02 estrae testo da PDF/immagini
- Identifica metadati base (autore, data, etc.)

### 3. Classificazione
- SP07 determina tipo documento (delibera, contratto, etc.)
- Assegna categoria e sottocategoria

### 4. Generazione Riassunto
- SP13 crea riassunto automatico
- Estrae punti chiave e informazioni rilevanti

### 5. Indicizzazione
- SP14 rende documento ricercabile
- Crea indici full-text e semantici

### 6. Abilitazione Ricerca
- SP12 prepara motore di ricerca
- Documento diventa interrogabile

### 7. Aggiornamento Dashboard
- SP10 mostra stato e risultati
- Utente riceve notifica completamento

## Tempi Tipici

- **Totale**: 15-45 secondi
- **Estrazione**: 3-8 secondi
- **Classificazione**: <1 secondo
- **Riassunto**: 2-5 secondi
- **Indicizzazione**: 1-3 secondi

## Punti di Decisione

### Classificazione Alta Confidenza
- Procede automaticamente
- Documento pronto per ricerca

### Classificazione Bassa Confidenza
- Flag per revisione umana
- Possibilità correzione manuale

### Errori di Processamento
- Retry automatico
- Alert per intervento operatore</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC1 - Sistema di Gestione Documentale/01 Sequence - Overview Semplificato.md
