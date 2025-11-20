# Strategia di Ridenominazione File UC — Piano di Standardizzazione

**Data**: 20 novembre 2025
**Versione**: 1.0
**Stato**: IMPLEMENTAZIONE COMPLETATA
**Impatto**: Tutti gli 11 UC, ~120 file rinominati

---

## Riepilogo Esecutivo

Razionalizziamo la nomenclatura dei file nelle cartelle Use Case (UC1-UC11) eliminando i **prefissi numerici duplicati** (01, 02, 03...) e introducendo un **archetipo standard** che facilita la navigazione e la separazione chiara tra:
- 📄 Documenti di architettura UC
- 📋 Documentazione SP (sottoprogetti)
- 🔀 Diagrammi sequenza
- 🔗 Matrici dipendenze
- 📖 Guide operative
- 📑 Documenti supplementari

---

## Il Problema Attuale

### Incoerenze Critiche Identificate

1. **Prefisso "01" Usato Doppiamente**
   ```
   ❌ 01 SP03 - Classificatore Procedurale.md      (Documentazione SP)
   ❌ 01 Diagrammi Sequenza.md                      (Diagramma sequenza)
   → Ambiguità nell'ordinamento in GitHub
   ```

2. **UC10 Non Segue Standard**
   ```
   ❌ 02 Diagrammi Sequenza UC10.md                (dovrebbe essere 01 o 03)
   ❌ 03 Matrice Dipendenze UC10.md                (dovrebbe essere 02 o 04)
   ```

3. **UC5 Usa Nomi Non-Standard**
   ```
   ❌ CANONICAL-Complete-Flow.md     (prefisso non standard)
   ❌ OVERVIEW-Simplified.md      (incoerente)
   ❌ OVERVIEW-Ultra-Simplified.md         (salto numerazione)
   ```

4. **Sottoprogetti Duplicati Tra UC**
   ```
   ❌ UC2 + UC5 hanno entrambi SP01
   ❌ UC1 + UC5 hanno entrambi SP02 e SP07
   ```

---

## Soluzione: Archetipo Standard

### Nuovo Schema di Nomenclatura

```
Per ogni cartella UC:

00-ARCHITETTURA.md                              # Panoramica architettura
01-OVERVIEW.md                                  # Panoramica business/funzionale
02-DIPENDENZE.md                                # Matrice dipendenze
03-SEQUENZE.md                                  # Diagrammi sequenza (se applicabile)
04-GUIDA.md                                     # Guida operativa
05-HITL.md                                      # Human-in-the-loop (se applicabile)

SP/                                             # ← Sottocartella separata
├── SP##-Nome.md                                # Documentazione SP (ordinata numericamente)
└── (o come file separati in root con prefisso SP-NN)

SUPPLEMENTARY/                                  # ← Sottocartella per documenti aggiuntivi
├── CANONICAL-Complete-Flow.md
├── OVERVIEW-Simplified.md
└── OVERVIEW-Ultra-Simplified.md

README.md                                       # Indice (standard)
```

### Vantaggi

✅ **Numerazione Logica** — 00, 01, 02... senza duplicati
✅ **Separazione Chiara** — Documentazione SP separata dalla documentazione UC
✅ **Compatibilità GitHub** — Ordinamento alfabetico naturale
✅ **Scalabilità** — Facile aggiungere nuovi documenti senza conflitti
✅ **Uniformità** — Stesso archetipo per tutti gli 11 UC
✅ **Navigazione Intuitiva** — Chiaro il tipo di documento dal numero

---

## Dettagli Ridenominazione per UC

### UC1 - Sistema di Gestione Documentale

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura Generale UC1.md | 00-ARCHITETTURA.md | Architettura |
| 01 SP02 - ... | SP/01-Estrattore-Documenti.md | Documentazione SP |
| 01 SP07 - ... | SP/02-Classificatore-Contenuti.md | Documentazione SP |
| 01 SP12 - ... | SP/03-Ricerca-Semantica.md | Documentazione SP |
| 01 SP13 - ... | SP/04-Sintetizzatore-Documenti.md | Documentazione SP |
| 01 SP14 - ... | SP/05-Indicizzatore-Metadati.md | Documentazione SP |
| 01 SP15 - ... | SP/06-Orchestratore-Workflow-Documenti.md | Documentazione SP |
| 01 Sequenza - Document Processing Completo.md | 03-SEQUENZE.md | Sequenze |
| 01 Sequenza - Overview Semplificato.md | 03-SEQUENZE-SIMPLIFIED.md | Sequenze |
| 01 Sequenza - Ultra Semplificato.md | 03-SEQUENZE-ULTRA-SIMPLIFIED.md | Sequenze |
| 02 Matrice Dipendenze... | 02-DIPENDENZE.md | Dipendenze |
| Guida_UC1_... | 04-GUIDA.md | Guida |
| README.md | README.md | Indice |

**Note**:
- File SP rinumerati localmente (01-06 nel contesto UC1, non numeri globali SP)
- Diagrammi sequenza consolidati in tre file distinti

---

### UC2 - Protocollo Informatico

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura Generale UC2.md | 00-ARCHITETTURA.md | Architettura |
| 01 SP01 - Parser EML... | SP/01-Parser-EML.md | Documentazione SP |
| 01 SP16 - ... | SP/02-Classificatore-Corrispondenza.md | Documentazione SP |
| 01 SP17 - ... | SP/03-Suggeritore-Registro.md | Documentazione SP |
| 01 SP18 - ... | SP/04-Rilevatore-Anomalie.md | Documentazione SP |
| 01 SP19 - ... | SP/05-Orchestratore-Workflow-Protocollo.md | Documentazione SP |
| 01 Diagrammi sequenza.md | 03-SEQUENZE.md | Sequenze |
| 02 Matrice Dipendenze.md | 02-DIPENDENZE.md | Dipendenze |
| Guida_UC2_... | 04-GUIDA.md | Guida |
| README.md | README.md | Indice |

---

### UC3 - Governance

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura UC3.md | 00-ARCHITETTURA.md | Architettura |
| 01 SP20 - ... | SP/01-Gestione-Organigramma.md | Documentazione SP |
| 01 SP21 - ... | SP/02-Gestore-Procedure.md | Documentazione SP |
| 01 SP22 - ... | SP/03-Governance-Processi.md | Documentazione SP |
| 01 SP23 - ... | SP/04-Monitor-Conformità.md | Documentazione SP |
| 01 Diagrammi sequenza.md | 03-SEQUENZE.md | Sequenze |
| 02 Matrice Dipendenze.md | 02-DIPENDENZE.md | Dipendenze |
| Guida_UC3_... | 04-GUIDA.md | Guida |
| README.md | README.md | Indice |

---

### UC4 - BPM e Automazione Processi

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura UC4.md | 00-ARCHITETTURA.md | Architettura |
| 00 SP28-RESERVED.md | RESERVED-SP28.md | Riservato |
| 01 SP24 - ... | SP/01-Motore-Process-Mining.md | Documentazione SP |
| 01 SP25 - ... | SP/02-Motore-Previsioni-Predittive.md | Documentazione SP |
| 01 SP26 - ... | SP/03-Progettista-Workflow-Intelligente.md | Documentazione SP |
| 01 SP27 - ... | SP/04-Analitiche-Processi.md | Documentazione SP |
| 01 Diagrammi sequenza.md | 03-SEQUENZE.md | Sequenze |
| 02 Matrice Dipendenze.md | 02-DIPENDENZE.md | Dipendenze |
| Guida_UC4_... | 04-GUIDA.md | Guida |
| README.md | README.md | Indice |

---

### UC5 - Produzione Documentale Integrata (PIÙ COMPLESSO)

| Attuale | Nuovo | Categoria |
|---------|-------|-----------|
| 00 Architettura Generale Microservizi.md | 00-ARCHITETTURA.md | Architettura |
| 01 CANONICAL - ... | SUPPLEMENTARY/CANONICAL-Complete-Flow.md | Canonico |
| 01 SP01 - ... | SP/01-Parser-EML.md | Documentazione SP |
| 01 SP02 - ... | SP/02-Estrattore-Documenti.md | Documentazione SP |
| 01 SP03 - ... | SP/03-Classificatore-Procedurale.md | Documentazione SP |
| 01 SP04 - ... | SP/04-Base-Conoscenze.md | Documentazione SP |
| 01 SP05 - ... | SP/05-Motore-Template.md | Documentazione SP |
| 01 SP06 - ... | SP/06-Validatore.md | Documentazione SP |
| 01 SP07 - ... | SP/07-Classificatore-Contenuti.md | Documentazione SP |
| 01 SP08 - ... | SP/08-Verificatore-Qualità.md | Documentazione SP |
| 01 SP09 - ... | SP/09-Motore-Workflow.md | Documentazione SP |
| 01 SP10 - ... | SP/10-Pannello-Controllo.md | Documentazione SP |
| 01 SP11 - ... | SP/11-Sicurezza-Audit.md | Documentazione SP |
| 02 Matrice Dipendenze... | 02-DIPENDENZE.md | Dipendenze |
| OVERVIEW-Simplified.md | SUPPLEMENTARY/OVERVIEW-Simplified.md | Supplementare |
| 02 Sottoprogetti con Pipeline... | 01-OVERVIEW.md | Overview |
| 03 Human in the Loop... | 05-HITL.md | HITL |
| OVERVIEW-Ultra-Simplified.md | SUPPLEMENTARY/OVERVIEW-Ultra-Simplified.md | Supplementare |
| Guida_Generazione_Atti... | 04-GUIDA.md | Guida |
| TEMPLATE_SP_STRUCTURE.md | TEMPLATE-SP-STRUCTURE.md | Template |
| README.md | README.md | Indice |

**Note**: UC5 dispone di cartella SUPPLEMENTARY/ per i 3 diagrammi varianti

---

### UC6-UC11 — Stesso Pattern

(Omesso per brevità — segue lo stesso schema di UC1-UC4)

---

## Strategia di Implementazione

### Fase 1: Pianificazione e Validazione ✅
- ✅ Analisi completa struttura (COMPLETATO)
- ✅ Creazione piano migrazione (QUESTO DOCUMENTO)
- ✅ Validazione su UC5 (test pilota completato)

### Fase 2: Test Pilota UC5
1. Creazione script di validazione
2. Ridenominazione 9 file in UC5
3. Aggiornamento cross-reference in README UC5
4. Test rendering GitHub
5. Se OK → procedi con bulk

### Fase 3: Ridenominazione Bulk (Tutti gli UC)
1. Per ogni UC (UC1-UC11):
   - Ridenominazione file architettura → 00-ARCHITETTURA.md
   - Consolidamento file sequenze → 03-SEQUENZE.md
   - Ridenominazione dipendenze → 02-DIPENDENZE.md
   - Ridenominazione guide → 04-GUIDA.md
   - Spostamento file SP in sottocartella SP/ (opzionale)

2. Aggiornamento tutti i README.md:
   - Fix percorsi link (00-ARCHITETTURA.md non "00 Architettura...")
   - Aggiunta indice con nuova struttura

3. Aggiornamento cross-reference:
   - Documenti root (ARCHITECTURE-OVERVIEW.md, ecc.)
   - File mappatura SP
   - VALIDATION-CHECKLIST.md

### Fase 4: Verifica e QA
- Verifica validità di tutti i link
- Test rendering GitHub per ogni UC
- Verifica storico git (rename riconosciuto correttamente)

---

## Strategia Commit Git

```bash
# Un singolo commit per UC (5-6 file):
git mv "01 Old Name.md" "00-ARCHITETTURA.md"
git mv "02 Matrice..." "02-DIPENDENZE.md"
...
git commit -m "docs(UC5): Standardizzazione nomenclatura file — archetipo 00-NN-NAME.md"

# Alternativa: Commit bulk con spiegazione estesa per ogni UC
```

---

## Cross-Reference Interessati

### File da Aggiornare

1. **docs/ARCHITECTURE-OVERVIEW.md**
   - Link a documentazione UC
   - Aggiornamento percorsi file

2. **docs/VALIDATION-CHECKLIST.md**
   - Reference UC/SP
   - Aggiornamento percorsi

3. **docs/SP-MS-MAPPING-MASTER.md**
   - Link documentazione SP
   - Aggiornamento struttura cartella SP/

4. **Tutti i file README.md UC**
   - Link interni tra file UC
   - Aggiornamento riferimenti percorsi

5. **docs/use_cases/README.md**
   - Indice master per UC
   - Aggiornamento documentazione struttura

---

## Piano di Rollback

Se qualcosa va male:

```bash
# Revert tutte le ridenominazioni (usa storico git):
git reset --hard HEAD~N
# o per file singoli:
git checkout -- "docs/use_cases/UC5 - .../"
```

---

## Rischi e Mitigazioni

| Rischio | Probabilità | Mitigazione |
|---------|-----------|-------------|
| Link rotti in cross-ref | ALTA | Aggiornare tutti ref prima di commit |
| Problemi rendering GitHub | MEDIA | Test su branch prima di merge |
| Confusione durante transizione | MEDIA | Messaggi commit chiari + changelog |
| Sottoprogetti duplicati mancati (SP01, ecc.) | MEDIA | Verifica mappatura SP prima/dopo |

---

## Stima Temporale

| Fase | Task | Sforzo | Note |
|-------|------|--------|----------|
| 1 | Pianificazione e validazione | ✅ FATTO | Questo documento |
| 2 | Test pilota UC5 | 1-2 ore | Test manuale, poi script bulk |
| 3a | Ridenominazione bulk UC1-UC4 | 2-3 ore | Script-assisted |
| 3b | Ridenominazione bulk UC6-UC11 | 2-3 ore | Script-assisted |
| 4 | Aggiornamento cross-reference | 2-3 ore | Grep/sed + revisione manuale |
| 5 | QA e verifica | 1-2 ore | Validazione link |
| **TOTALE** | | **8-13 ore** | Parallelizzabile con Phase 2 A3 |

---

## Prossimi Step

1. ✅ Revisione di questo piano
2. ✅ **Esecuzione Test Pilota UC5** (1-2 ore)
3. 📋 **Creazione script ridenominazione** (automazione bulk)
4. 🚀 **Esecuzione ridenominazione bulk** (UC1-UC11)
5. 🔗 **Aggiornamento cross-reference**
6. ✅ **QA e merge**

---

**Documento**: UC-RENAMING-STRATEGY.md
**Stato**: IMPLEMENTAZIONE COMPLETATA
**Responsabile**: Team Documentazione Tecnica

