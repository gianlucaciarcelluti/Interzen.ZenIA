# Gap Resolution - Numerazione SP e Coerenza Architetturale

## Stato Complessivo - AGGIORNATO

- **SP Totali (con SP25 + SP33 aggiunti)**: 70
- **SP Documentati**: 68 (SP01-SP70, esclusi i 2 aggiunti)
- **SP Infrastrutturali**: 8 (UC11 SP63-SP70)
- **SP Gap RISOLTI**:
  - ✅ SP25 "Forecasting & Predictive Scheduling Engine" (UC4) - CREATO
  - ✅ SP33 "Timestamp Authority & Temporal Marking" (UC6) - CREATO
- **SP Gap FALSI**: SP57 non esiste (era errore numerazione UC10-UC11)

---

## Gap Identificati

### Gap 1: SP25 (UC4 - BPM & Process Automation)

**Posizione attesa**: Tra SP24 (Process Mining Engine) e SP26 (Intelligent Workflow Designer)

**Situazione attuale**: Non documentato

**Probabile scopo**:
- Forecasting Engine (predizione colli di bottiglia, workload prediction)
- Scheduler/Planner (pianificazione intelligente task assignment)
- Risk Predictor (predizione rischi processo)

**Impatto**: UC4 matrice dipendenze completa senza esplicito SP25 → probabilmente non intenzionale ma non critico

**Azione consigliata**:
- **Opzione A (Consigliata)**: Documentare SP25 "Forecasting & Predictive Scheduling Engine" in UC4
  - Input: Process execution data, historical patterns, current load
  - Output: Predictions on bottlenecks, recommended optimizations, workload forecasts
  - MS: MS02 (Analyzer) primario, MS10 (Analytics) supporto
  - Posizionamento: Dopo SP24 Process Mining, supporta SP27 Process Analytics

- **Opzione B**: Se non necessario, confermare intenzionale e documentare "SP25 skipped intentionally"

**Documentazione necessaria**:
- Crea: `UC4 - BPM/01 SP25 - Forecasting & Predictive Scheduling Engine.md`

---

### Gap 2: SP33 (UC6 - Firma Digitale Integrata)

**Posizione attesa**: Tra SP31 (Pre-Signature Validator) e SP33 (Post-Signature Auditor)

**Situazione attuale**: Non documentato

**Probabile scopo**:
- **Timestamp Authority (TSA) Manager** / Marcatura Temporale
- Gestione Trusted Time Stamp, validazione temporale, integrazione con servizi TSA
- Completa il flow: Pre-firma (SP31) → Firma (SP30) → **Marcatura temporale (SP33)** → Post-firma audit (SP33)

**Impatto**: Componente critico per compliance normativa (CAD, leggi firma digitale, marcatura temporale obbligatoria)

**Azione consigliata**:
- **Documentare SP33 "Timestamp Authority & Temporal Marking Manager"**
  - Input: Signed documents, signature timestamps
  - Output: Timestamped documents with TSA proof, validity confirmation
  - MS: MS13 (Security) primario, MS04 (Validator) supporto, MS14 (Audit) supporto
  - Dipendenze: SP30 (firma) → SP33 (marcatura) → SP33 (audit)

**Documentazione necessaria**:
- Crea: `UC6 - Firma Digitale/01 SP33 - Timestamp Authority & Temporal Marking.md`

---

### Gap 3: SP57 (UC10 vs UC11)

**Situazione attuale**:
- Documentato come "SP57 - User Feedback Management" in UC10 folder
- Anche riferito in UC11 lista SP51-SP57

**Problema**: Appartenenza duplice non chiara

**Analisi**:
- **Nome e funzione**: "User Feedback Management" è genuinamente UC10 (User Support)
- **Logica**: UC10 = Help Desk + Support Portal; UC11 = Analytics + Reporting
- **Feedback** potrebbe essere:
  - UC10-specific: Feedback diretto da utenti su supporto/helpdesk
  - UC11-specific: Feedback analytics aggregato per reporting/insights

**Azione consigliata**:
- **Mantenere SP57 in UC10** come primario (User Support)
- **Referenziare da UC11** come dipendenza input: "UC11 analytics consuma SP57 feedback data"
- **Documentare esplicitamente** nel SP57:
  - Feedback raccolto in UC10
  - Aggregato/analizzato in UC11
  - Input per SP56 (Support Analytics) e SP64 (Predictive Analytics)

**Documentazione necessaria**:
- Chiarire nei doc UC10 e UC11 il flusso SP57

---

## UC11 Infrastrutture: Riclassificazione Proposta

### Analisi Componenti SP65-SP72

| SP | Nome | Natura | UC-Specific? | Cross-Cutting? |
|---|---|---|---|---|
| SP65 | Data Security & Compliance | Security | ⚠️ Mostly cross-cutting, UC11 specific config | Quasi |
| SP66 | API Gateway & Integration Layer | Infrastructure | ❌ No, serve TUTTI gli UC | **SI** |
| SP67 | DevOps & CI/CD Pipeline | Infrastructure | ❌ No, serve TUTTI gli UC | **SI** |
| SP68 | Disaster Recovery & Business Continuity | Infrastructure | ❌ No, serve TUTTI gli UC | **SI** |
| SP69 | Compliance & Audit Management | Cross-cutting | ⚠️ Audit è cross-cutting ma configurato per analytics | Quasi |
| SP70 | Performance Optimization & Scaling | Infrastructure | ❌ No, serve TUTTI gli UC | **SI** |
| SP71 | Performance Monitoring & Alerting | Cross-cutting | Quasi, ma usage-pattern is cross-cutting | **SI** |
| SP72 | Incident Management & Escalation | Infrastructure | ❌ No, serve TUTTI gli UC | **SI** |

### Riclassificazione Consigliata

**Opzione 1: Mantenere in UC11 (status quo)**
- Pro: Packaging implementativo completo (analytics + ops)
- Con: Semanticamente confuse, non sono analytics

**Opzione 2 (CONSIGLIATA): Creare sezione "Infrastructure & Operations"**
- UC11 diventa "Analytics & Reporting" puro (SP58-SP64)
- Nuova sezione "Cross-Cutting Infrastructure" (SP65-SP72)
- Ogni UC referenzia le infrastrutture di cui ha bisogno
- Più chiaro concettualmente

**Opzione 3: Mantieni in UC11 ma con sezione esplicita**
- UC11 ha 2 sottosezioni: "Core Analytics" e "Operational Infrastructure"
- Chiarire che SP65-SP72 sono "enablers", non feature analytics

**Azione consigliata**:
- Implementare **Opzione 2**: Creare nuovo documento `docs/CROSS-CUTTING-INFRASTRUCTURE.md`
- Spostare SP65-SP72 concettualmente
- Documentare dipendenze da/verso tutti UC

---

## Matrici Dipendenze Incomplete

### UC completate
- ✓ UC1: `02 Matrice Dipendenze Sottoprogetti UC1.md` - COMPLETA
- ✓ UC2: `02 Matrice Dipendenze.md` - COMPLETA
- ✓ UC4: `02 Matrice Dipendenze.md` - COMPLETA

### UC incomplete
- ⚠️ UC3: No explicit matrix doc found (esiste `Guida` ma no matrice)
- ⚠️ UC5: Matrice parziale in `02 Sottoprogetti con Pipeline Operative.pdf`
- ⚠️ UC6-11: No dependency matrices found

### Azione necessaria
Completare matrici per UC3, UC6, UC7, UC8, UC9, UC10, UC11

---

## Architetture UC: Inconsistenze

### UC1
- ✓ 1 architettura: `00 Architettura Generale UC1.md` - OK
- Riferimenti: SP02, SP07, SP13, SP14, SP12, SP15, SP10, SP11
- Stato: COERENTE

### UC5
- ⚠️ 2 architetture:
  1. `00 REFACTORING - Nuova Architettura con EML.md` (legacy/refactoring in progress?)
  2. `00 Architettura Generale Microservizi.md` (canonical)
- Azione: Decidere quale è canonical, deprecare l'altra

### UC6
- ✓ Architettura esplicita presente
- Referimenti: SP30, SP31, SP33 (manca SP33)
- Stato: INCOMPLETE (missing SP33)

### UC7-UC11
- ✓ Architetture presenti
- Stato: COERENTE

---

## Template Standardizzato SP

Ogni SP deve seguire questo template per coerenza:

```markdown
# SPXX - [Nome Componente]

## Overview
- **Caso d'uso**: UC#
- **Categoria**: [Core AI | Platform | Infrastructure | Cross-Cutting]
- **MS Primario**: MS##
- **MS Supporto**: MS##, MS##

## Responsabilità Principali
- Responsabilità 1
- Responsabilità 2
- Responsabilità 3

## Input/Output
**Input**:
- Tipo 1: [descrizione]
- Tipo 2: [descrizione]

**Output**:
- Tipo 1: [descrizione]
- Tipo 2: [descrizione]

## Dipendenze
**Upstream** (richiede):
- SP## [descrizione]
- SP## [descrizione]

**Downstream** (fornisce a):
- SP## [descrizione]

## Architettura Tecnica
- Modelli/componenti
- Storage layer
- API endpoint

## Tecnologie
- Framework/libreria 1
- Framework/libreria 2

## KPI e Monitoraggio
- Metrica 1: target
- Metrica 2: target
```

---

## Piano Azioni Risoluzione

### Phase 1: Documentare Gap (COMPLETATO)
1. ✅ Identificare gap (completato in questo documento)
2. ✅ Creare SP25 "Forecasting Engine" doc UC4 (CREATO)
3. ✅ Creare SP33 "Timestamp Authority" doc UC6 (CREATO)
4. ✅ Chiarire SP57: RISOLTO - SP57 non esiste, era errore conteggio UC10-UC11

### Phase 2: Normalizzare Architetture (NEXT WEEK)
1. Decidere canonical architecture UC5 (deprecare uno dei 2)
2. Creare matrici dipendenze UC3, UC6, UC7, UC8, UC9, UC10, UC11
3. Creare documento `CROSS-CUTTING-INFRASTRUCTURE.md` se adottato Opzione 2

### Phase 3: Standardizzare Template (NEXT WEEK)
1. Applicare template standard a tutti gli SP
2. Validare coerenza terminologia
3. Controllare sp→ms mapping in ogni doc

### Phase 4: Validazione Finale (END OF MONTH)
1. Audit completo matrice UC-SP-MS
2. Verifica dipendenze circolari
3. Documentazione finale sign-off

---

## Summary - AGGIORNATO

| Elemento | Stato | Azione |
|---|---|---|
| **SP25 (UC4)** | ✅ RESOLVED | Documento "SP25 - Forecasting & Predictive Scheduling Engine" creato |
| **SP33 (UC6)** | ✅ RESOLVED | Documento "SP33 - Timestamp Authority & Temporal Marking" creato |
| **SP57** | ✅ RESOLVED | Non esiste - era errore conteggio. UC10 termina a SP54, UC11 inizia a SP55 |
| **SP-MS Mapping** | ✅ UPDATED | SP-MS-MAPPING-MASTER.md aggiornato con SP25, SP33, corrette numerazioni |
| **UC5 Architettura** | ⚠️ TODO | Decidere canonical, deprecare la versione "REFACTORING" |
| **Matrici UC3,6,7,8,9,10,11** | ⚠️ TODO | Completare matrici dipendenze SP-SP per questi UC |
| **Template SP Standardizzazione** | ⚠️ TODO | Applicare SP-DOCUMENTATION-TEMPLATE.md a tutti gli SP |

