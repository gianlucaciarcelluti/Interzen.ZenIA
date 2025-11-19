# SP28 - Reserved (Gap nella Numerazione)

**Status**: INTENTIONALLY RESERVED
**Data Creazione**: 2025-11-19
**Categoria**: Architetturale

---

## Motivo Della Riserva

SP28 è **intenzionalmente riservato** e non è documentato come sottoprogetto attivo.

### Contesto Storico

Durante la pianificazione iniziale dell'architettura ZenIA, la numerazione dei Sottoprogetti (SP) è stata strutturata per permettere futuri ampliamenti in categorie specifiche:

- **SP01-SP11**: UC5 - Produzione Documentale Integrata
- **SP12-SP15**: UC1 - Sistema di Gestione Documentale
- **SP16-SP19**: UC2 - Protocollo Informatico
- **SP20-SP23**: UC3 - Governance
- **SP24-SP27**: UC4 - BPM e Automazione
- **SP28**: ⚠️ **RESERVED** per futuro ampliamento UC4 o nuovi UC
- **SP29+**: Ulteriori use cases

### Decisione Architetturale

La riserva di SP28 è documentata in:
- [QUICK-REFERENCE-ARCHITECTURE.md](QUICK-REFERENCE-ARCHITECTURE.md#sp-distribution) - Sezione SP Distribution
- [riepilogo_casi_uso.md](riepilogo_casi_uso.md#sp28-reserved) - Nota su SP28
- [GAP-RESOLUTION.md](GAP-RESOLUTION.md#sp28-intenzionalmente-skipped) - Documentazione gap

---

## Quando Usare SP28

SP28 dovrebbe essere assegnato quando:

1. **Nuovo sottoprogetto UC4**: Se si identifica un nuovo componente per UC4 (BPM e Automazione Processi)
   - Esempio: SP28 - Advanced Process Optimization Engine

2. **Nuovo Use Case**: Se si crea un nuovo UC tra UC4 e UC5
   - Esempio: UC4.5 - Process Innovation → SP28-...

3. **Espansione UC4**: Se la categoria UC4 necessita di un sottoprogetto aggiuntivo
   - SP24-SP27 + SP28 = 5 SP totali per UC4

---

## Come Assegnare SP28

Quando deciderai di utilizzare SP28, segui questi step:

### 1. Creare File SP28
```bash
# Copia template
cp docs/use_cases/UC4\ -\ BPM\ e\ Automazione\ Processi/01\ SP27\ -\ Process\ Analytics.md \
   docs/use_cases/UC4\ -\ BPM\ e\ Automazione\ Processi/01\ SP28\ -\ [NOME_SOTTOPROGETTO].md
```

### 2. Aggiornare Documentazione Master

Aggiorna i seguenti file con riferimento a SP28:

- **SP-MS-MAPPING-MASTER.md**: Aggiungi entry per SP28 con MS primario e supporto
- **riepilogo_casi_uso.md**: Aggiorna tabella SP per UC4 con SP28
- **QUICK-REFERENCE-ARCHITECTURE.md**: Aggiorna matrice SP
- **UC4 Matrice Dipendenze**: Aggiungi SP28 al grafo dipendenze

### 3. Mappare a Microservizio

Determina quale Microservizio (MS) sarà primario:
- MS02 (Analyzer): Per decisioni e classificazione
- MS03 (Orchestrator): Per orchestrazione processi
- MS08 (Workflow): Per automazione

### 4. Eseguire Verifiche

Dopo l'assegnazione, esegui:
```bash
python3 scripts/verify_sp_references.py
# SP28 dovrebbe comparire negli errori come "SP28 trovato ma non referenziato in file SP28.md"
```

---

## Riferimenti Attuali

### File che Referenziano SP28

Attualmente SP28 è referenziato in pochi file in contesti storici:

- **03 DEPRECATED - Analisi Refactoring EML.md**: Contesto legacy (contiene SP00)
- **04 DEPRECATED - Sequence Con SP00.md**: Contesto legacy

Questi riferimenti rimarranno per tracciabilità storica, ma SP28 non è implementato.

---

## Timeline Prevista

| Data | Azione |
|------|--------|
| 2025-11-19 | SP28 Riservato |
| TBD | Valutazione necessità SP28 |
| TBD | Implementazione SP28 (se richiesto) |

---

## Contatti

Per domande sulla riserva di SP28 o per proporre suo utilizzo, contattare:
- **Architecture Team**: [slack #zenia-architecture](https://zenia-workspace.slack.com)
- **Tech Lead**: [TBD]

---

**Documento**: SP28-RESERVED.md
**Versione**: 1.0
**Ultimo Aggiornamento**: 2025-11-19
**Maintainer**: ZenIA Architecture Team
