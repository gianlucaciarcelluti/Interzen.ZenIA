# Sistema di Validazione della Documentazione

## Panoramica

Il sistema di validazione della documentazione ZenIA è un framework di assicurazione qualità a **3 LIVELLI (TIER)** che garantisce la qualità della documentazione pur permettendo miglioramenti iterativi. Solo i controlli di **TIER 1 (Critici)** bloccano commit/merge. **TIER 2 e TIER 3** generano avvisi per il miglioramento continuo.

## Architettura

```
┌─────────────────────────────────────────────────────────┐
│  LOCALE: ./../../scriptsrun_all_checks.sh                    │
│  (Esegue i 15 validator, mostra feedback in tempo reale)│
└─────────────────────────────────────────────────────────┘
         ↓
         ↓ (git push)
         ↓
┌─────────────────────────────────────────────────────────┐
│  CI/CD: ../../.github/workflowsdocs-validation.yml           │
│  (Esegue la suite di validazione completa per ogni commit/PR)
└─────────────────────────────────────────────────────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
  PASS    FAIL (solo TIER 1)
   │        │
   ✅       ❌
  MERGE   DEVE ESSERE CORRETTO
  PRONTO
```

## Livelli di Validazione

### TIER 1: CRITICO (Bloccante) 🚫

**Stato**: DEVE PASSARE prima di commit/merge

5 controlli critici:

1. **Riferimenti SP/MS** (`verify_sp_references.py`)
   - Verifica che i riferimenti SP01-SP72 siano corretti
   - Nessuna mappatura UC non valida
   - Solo i file autorizzati possono riferirsi allo SP28 riservato
   - **Fallimento**: Blocca il commit

2. **Archetipo UC** (`verify_uc_archetype.py`)
   - Tutti gli 11 UC hanno i file richiesti: `00-ARCHITECTURE.md`, `01-OVERVIEW.md`, `02-DEPENDENCIES.md`, `README.md`
   - Completezza struttura minima 70%
   - **Fallimento**: Blocca il commit (se sotto soglia)

3. **Completezza SP** (`verify_sp_completeness.py`)
   - Tutti i 71 SP presenti (SP01-SP72 escl. SP28)
   - Nessuno SP mancante
   - Nessun SP duplicato tra UC
   - **Fallimento**: Blocca il commit

4. **Intestazioni Markdown** (`verify_markdown_headings.py`)
   - Gerarchia intestazioni corretta (no salti H1→H3)
   - Nessuna intestazione duplicata
   - **Stato**: Attualmente solo avvisi (non bloccante)

5. **Diagrammi Mermaid** (`verify_mermaid_diagrams.py`)
   - Sintassi Mermaid valida
   - Definizioni nodi corrette
   - **Fallimento**: Blocca il commit

**Errori tipici che bloccano**:
- File SP richiesti mancanti
- Archetipo UC rotto
- Sintassi diagramma non valida

**Visualizza risultati**:
```bash
./scripts/run_all_checks.sh
# Cerca: ✅ TIER 1 PASS
```

## [Intestazione generata automaticamente livello 2]
### TIER 2: QUALITÀ CONTENUTI (Avvisi) ⚠️

**Stato**: Non bloccante, ma importante da risolvere

4 controlli di qualità dei contenuti:

1. **Completezza Sezioni** (`verify_section_completeness.py`)
   - I file SP dovrebbero avere: Panoramica, Dettagli Tecnici, Casi d'Uso, Gestione Errori
   - **Attuale**: 0% completo, avviso non bloccante
   - **Sforzo**: Alto (creazione contenuti)

2. **Coerenza Linguistica** (`verify_language_coherence.py`)
   - Uso coerente di Italiano/Inglese
   - Nessun mix di lingue in sezioni critiche
   - **Stato**: ✅ PASSATO

3. **Validazione Payload** (`verify_payload_validation.py`)
   - Esempi JSON request/response validi
   - **Stato**: ✅ PASSATO

4. **Cross-References** (`verify_cross_references.py`)
   - I riferimenti interni UC/SP sono validi
   - Intervalli link corretti
   - **Stato**: Avvisi (non bloccante)

**Avvisi tipici**:
- Intestazioni di sezione mancanti
- Incoerenza linguistica
- Intervalli di riferimenti non validi

**Visualizza risultati**:
```bash
cat scripts/reports/section_completeness_validation.json
cat scripts/reports/language_coherence_validation.json
```

### TIER 3: LINT & STYLE (Avvisi) 🧹

**Stato**: Problemi di stile/formattazione non bloccanti

6 controlli lint:

1. **Formattazione Spaziatura** (`verify_whitespace_formatting.py`)
   - Nessuno spazio finale
   - Nessuna mescolanza tab/spazi
   - Linee ≤120 caratteri
   - **Attuale**: 1978 avvisi di stile (non bloccante)
   - **Sforzo**: Molto alto

2. **Immagini Orfane** (`verify_orphaned_images.py`)
   - Nessuna immagine non usata
   - Tutte le immagini referenziate esistono
   - **Stato**: Avvisi (bassa priorità)

3. **Duplicati Contenuto** (`verify_content_duplicates.py`)
   - Nessuna sezione identica duplicata
   - Individua possibili copy-paste
   - **Stato**: Avvisi (potrebbe essere intenzionale)

4. **Metadati README** (`verify_readme_metadata.py`)
   - I README includono versione, data, stato
   - **Stato**: ✅ PASSATO

5. **Esempi JSON** (`verify_json_examples.py`)
   - Payload JSON validi
   - **Stato**: ✅ PASSATO

6. **Link** (`verify_links.py`)
   - Nessun link interno rotto
   - Tutti i riferimenti validi
   - **Stato**: ✅ PASSATO (14→0 link rotti)

**Avvisi tipici**:
- Linee troppo lunghe (>120 char)
- Spaziature finali
- Immagini non usate
- Sezioni duplicate

**Visualizza risultati**:
```bash
cat scripts/reports/whitespace_formatting_validation.json
cat scripts/reports/orphaned_images_validation.json
```

## Utilizzo Locale

### Eseguire la Validazione Completa

```bash
# Esegui tutti i controlli (15 totali)
./scripts/run_all_checks.sh

# L'output mostra:
# - Controlli TIER 1 (Critici)
# - Controlli TIER 2 (Qualità Contenuti)
# - Controlli TIER 3 (Lint)
# - Feedback colorato (✅ 🟡 ~)
# - Suggerimenti nei report per i fallimenti
```

## [Intestazione generata automaticamente livello 2]
### Eseguire un Validator Specifico

```bash
# Esegui solo la validazione riferimenti SP
python3 scripts/verify_sp_references.py

# Esegui solo la validazione link
python3 scripts/verify_links.py

# Esegui solo la verifica completezza sezioni
python3 scripts/verify_section_completeness.py
```

## [Intestazione generata automaticamente livello 2]
### Visualizzare i Report Dettagliati

```bash
# Apri i report di validazione (formato JSON)
cat scripts/reports/sp_ms_references.json
cat scripts/reports/uc_archetype_validation.json
cat scripts/reports/sp_completeness_validation.json

# Usa jq per una stampa leggibile
cat scripts/reports/sp_ms_references.json | jq
```

## [Intestazione generata automaticamente livello 2]
### Modalità Rapida vs Verbose

```bash
# Modalità rapida (solo TIER 1, ~20 righe output)
./scripts/run_all_checks.sh

# Rapida con tutti i controlli TIER 2-3
./scripts/run_all_checks.sh

# Modalità verbose (output dettagliato)
./scripts/run_all_checks.sh --verbose
```

## Integrazione CI/CD

### Workflow GitHub Actions

**File**: `.github/workflows/docs-validation.yml`

**Sequenza Workflow** (tutti i passi eseguiti sequenzialmente):

```
1️⃣ Checkout codice
     ↓
2️⃣ Setup Python 3.11
     ↓
3️⃣ Esegui la suite completa di validazione (./scripts/run_all_checks.sh)
     ↓
4️⃣ Carica i report di validazione come artifacts (se ci sono fallimenti)
     ↓
5️⃣ Mostra il riepilogo di validazione nei log
     ↓
6️⃣ Controlla risultati TIER 1 (blocca se FAIL)
     ↓
7️⃣ Pubblica commento PR con i risultati (sequenziale dopo la validazione)
     ↓
✅ o ❌ Workflow completo
```

**Trigger**:
- On push su: `main`, `razionalizzazione-sp`, `develop`
- On PR verso: `main`, `razionalizzazione-sp`
- Quando cambiano docs o scripts

**Comportamento**:
- Tutti i passi vengono eseguiti in sequenza (non in parallelo)
- La validazione completa prima dell'azione successiva
- Il commento PR viene postato DOPO che i risultati di validazione sono disponibili
- Il commento include link agli artifacts e istruzioni di debug
- Blocca il merge solo se la validazione TIER 1 FALLISCE

**Come controllare i risultati**:
1. Vai alla tab Actions → Clicca sulla run di validazione
2. Visualizza il riepilogo di validazione in tempo reale nei log
3. Scarica l'artifact "validation-reports"
4. Rivedi i file JSON per errori dettagliati
5. Il commento PR fornisce link diretti e istruzioni

## Logica di Decisione

### Quando il Workflow PASSA ✅

```
Suite di validazione completata
     ↓
✅ TIER 1 PASS
     ↓
📝 Commento PR pubblicato (con link agli artifacts)
     ↓
🟢 Merge abilitato
     ├─ Tutti i controlli critici superati
     ├─ Avvisi TIER 2 registrati (non bloccanti)
     └─ Avvisi TIER 3 registrati (non bloccanti)
```

### Quando il Workflow FALLISCE ❌

```
Suite di validazione completata
     ↓
❌ TIER 1 FAIL
     ↓
📝 Commento PR pubblicato (con dettagli degli errori)
     ↓
🔴 Merge bloccato
     ├─ Uno o più controlli critici non superati
     ├─ Il commento PR mostra quali controlli sono falliti
     └─ Lo sviluppatore deve correggere e rifare il push
```

### Esperienza Commento PR

**Commento PR automatico pubblicato dopo la validazione**:
- Mostra stato TIER 1 (✅ PASS o ❌ FAIL)
- Fornisce link diretto alla tab Actions
- Elenca istruzioni per scaricare gli artifacts
- Include il suggerimento di debug `./scripts/run_all_checks.sh`
- Timestamp di completamento per tracciare audit

## Configurazione & Personalizzazione

### Regolare i Livelli TIER

Modifica `.github/workflows/docs-validation.yml`:

```yaml
# Attuale: Solo TIER 1 blocca
# Per rendere TIER 2 bloccante, cambiare:
if grep -q "TIER 2 FAIL" validation_output.txt; then
  exit 1
fi
```

## [Intestazione generata automaticamente livello 2]
### Regolare le Soglie

Modifica gli script validator individuali:

```python
# verify_sp_completeness.py, line 208
if summary['errors'] == 0 and len(summary['extra_sp']) == 0:
    print("✅ SP COMPLETENESS: PERFECT")
    return 0
```

## [Intestazione generata automaticamente livello 2]
### Aggiungere Nuovi Validator

1. Crea `scripts/verify_my_check.py`
2. Aggiungi a `scripts/run_all_checks.sh`:
   ```bash
   run_check "🔟" "My Check Name" "verify_my_check.py"
   ```
3. Aggiorna i trigger del workflow in `.github/workflows/docs-validation.yml`

## Risoluzione dei Problemi

### La validazione fallisce localmente ma passa in CI?

- Assicurati di avere Python 3.11+: `python3 --version`
- Reinstalla le dipendenze: `pip install -r requirements.txt` (se presente)
- Esegui con `--verbose`: `./scripts/run_all_checks.sh --verbose`

### "TIER 1 FAIL" ma non vedo l'errore?

1. Controlla i log del workflow: Actions tab → Seleziona la run → Logs
2. Scarica l'artifact validation-reports
3. Cerca nei file JSON dei report i dettagli degli errori
4. Esegui `./scripts/run_all_checks.sh --verbose` localmente

### Il mio commento PR non è apparso?

- Controlla la tab Actions per il workflow `Documentation Commenter`
- Se fallito, verifica i permessi in `.github/workflows/docs-comment.yml`
- Assicurati che `GITHUB_TOKEN` abbia permessi `issues: write`

## Performance

- **Locale**: ~5-10 secondi (277 file, 15 validator)
- **CI**: ~20-30 secondi (include upload artifacts)
- **Report**: 15 file JSON in `scripts/reports/`
- **Ritenzione artifacts**: 30 giorni

## Miglioramenti Futuri

### Pianificato per la Fase Successiva

1. **Intestazioni Markdown**: Renderle bloccanti (correggere 202 errori heading)
2. **Completezza Sezioni**: Aggiungere template sezioni SP
3. **Spaziatura**: Script di auto-fix per righe lunghe
4. **Duplicati Contenuto**: Identificare candidati copy-paste
5. **Dashboard Metriche**: Tracking settimanale metriche di validazione

### Miglioramenti Opzionali

- Notifiche Slack su fallimenti TIER 1
- Fix automatici per problemi di spaziatura
- ML per rilevamento duplicati
- Analisi trend storici

## Architettura del Workflow

### Design Workflow Unificato

Il sistema utilizza **un unico workflow** (`docs-validation.yml`) che gestisce sia la validazione che il commento PR in modo sequenziale:

**Decisioni di Progetto Chiave**:
- ✅ **Single Source of Truth**: Un file workflow gestisce tutta la logica di validazione
- ✅ **Esecuzione Sequenziale**: Tutti i passi eseguiti in ordine (nessuna race condition)
- ✅ **Commento PR Affidabile**: Commento pubblicato dopo la validazione con dati accurati
- ✅ **Gestione Artifacts**: I report sono caricati prima del posting del commento per assicurare link funzionanti
- ✅ **Feedback Chiaro**: Gli sviluppatori vedono i risultati di validazione direttamente nel commento PR

**Prima vs Ora**:
- ❌ **Prima**: Workflow separati (`docs-validation.yml` + `docs-comment.yml`) potevano creare race
- ❌ **Prima**: Il commento poteva essere postato prima che la validazione fosse completa
- ✅ **Ora**: Workflow unificato garantisce esecuzione sequenziale e affidabile

## Riferimenti

- Script di Validazione: `scripts/` (root directory)
- [Spec Archetipo UC](./DOCUMENTATION-STRUCTURE-GUIDE.md)
- [Mappatura SP](./ARCHITECTURE-OVERVIEW.md)
- Workflows GitHub Actions: `.github/workflows/` (root directory)

---

**Ultimo Aggiornamento**: 2025-11-20
**Stato**: Production Ready ✅
**TIER 1 Pass Rate**: 100%
