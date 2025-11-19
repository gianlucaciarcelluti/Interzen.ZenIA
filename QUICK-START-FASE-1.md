# 🚀 Quick Start - FASE 1 Completata

**Come usare gli strumenti creati nella FASE 1**

---

## 1️⃣ Eseguire Tutte le Verifiche

```bash
cd /path/to/ZenIA
./scripts/run_all_checks.sh
```

**Output Atteso**:
```
📋 ZenIA Documentation Validation Suite
========================================

1️⃣  Verifica SP/MS References...
2️⃣  Verifica JSON Examples...
3️⃣  Verifica Link Markdown...

📊 RIEPILOGO VERIFICHE
✅ SP/MS References: OK
✅ JSON Examples: OK
✅ Link Markdown: OK

📁 Report completi in: scripts/reports/
  • sp_ms_references.json
  • json_validation.json
  • links_validation.json
```

---

## 2️⃣ Eseguire Singole Verifiche

### Verifica SP/MS References
```bash
python3 scripts/verify_sp_references.py
```

**Cosa controlla**:
- Tutti riferimenti SP01-SP72 (escluso SP28)
- Tutti riferimenti MS01-MS16
- Validità numerazione
- SP/MS orfani

---

### Verifica JSON Examples
```bash
python3 scripts/verify_json_examples.py
```

**Cosa controlla**:
- 502 blocchi JSON nei file MD
- Validità sintassi
- Campi obbligatori

---

### Verifica Link Markdown
```bash
python3 scripts/verify_links.py
```

**Cosa controlla**:
- 1.148 link markdown
- Link interni validi
- Link esterni
- Link rotti

---

## 3️⃣ Visualizzare Report

### Report JSON Completo
```bash
cat scripts/reports/sp_ms_references.json | python3 -m json.tool | less
```

### Solo Summary
```bash
python3 << 'EOF'
import json

# SP/MS References
with open('scripts/reports/sp_ms_references.json') as f:
    data = json.load(f)
    print(f"SP/MS References: {data['summary']['errors']} errors, {data['summary']['warnings']} warnings")

# JSON Validation
with open('scripts/reports/json_validation.json') as f:
    data = json.load(f)
    print(f"JSON: {data['summary']['valid']}/{data['summary']['total_blocks']} valid")

# Links Validation
with open('scripts/reports/links_validation.json') as f:
    data = json.load(f)
    print(f"Links: {data['summary']['broken_internal']} broken")
EOF
```

---

## 4️⃣ File Importanti Creati

### Scripts (Automazione)
```
scripts/
├── verify_sp_references.py    # Valida SP/MS references
├── verify_json_examples.py    # Valida JSON (502 blocchi)
├── verify_links.py            # Verifica link (1.148 link)
├── run_all_checks.sh          # Esegui tutto
└── reports/
    ├── sp_ms_references.json
    ├── json_validation.json
    └── links_validation.json
```

### CI/CD
```
.github/workflows/
└── docs-validation.yml        # GitHub Actions workflow
```

### Documentazione
```
docs/use_cases/UC4 - BPM e Automazione Processi/
└── 00 SP28-RESERVED.md        # Gap SP28 documentato

FASE-1-COMPLETAMENTO.md        # Riepilogo completo FASE 1
QUICK-START-FASE-1.md          # Questo file
```

---

## 5️⃣ Problemi Noti da Risolvere

### ❌ SP00 Trovato (FASE 2)
```
Errore: SP00: Non è un SP valido
File: docs/use_cases/UC5/04 DEPRECATED - Sequence Con SP00.md
Soluzione: Riferimenti storici OK, file tagged DEPRECATED
```

### ❌ SP28 in 9 File (FASE 2)
```
Warning: SP28: Trovato in 9 file (dovrebbe essere reserved)
Soluzione: Normale, SP28 è reserved. Documenteremo meglio in FASE 2
```

### ❌ 45 JSON Invalidi (FASE 2)
```
Errore: 45 blocchi JSON con sintassi errata
Esempio: Expecting property name enclosed in double quotes
Soluzione: Fix in FASE 2 (Settimana 3-4)
```

### ❌ 90 Link Rotti (FASE 3)
```
Errore: 90 link interni non risolvono
Esempio: path/to/SP02.md, ../use_cases/UC1/...
Soluzione: Fix in FASE 3 (Settimana 5-6)
```

---

## 6️⃣ Workflow Giornaliero

### Prima di Committare Cambiamenti Docs
```bash
# 1. Esegui verifiche
./scripts/run_all_checks.sh

# 2. Controlla errori
cat scripts/reports/sp_ms_references.json | python3 -m json.tool | grep -A2 '"errors"'

# 3. Se OK, committa
git add docs/
git commit -m "Update documentation"
git push
```

### Dopo Push su PR
La GitHub Actions workflow eseguirà automaticamente:
- ✅ Verifica SP/MS references
- ✅ Valida JSON examples
- ✅ Verifica link
- ✅ Commenta PR con risultati

---

## 7️⃣ Comandi Git per Merge

### Crea Branch (se non esiste)
```bash
git checkout -b docs/refactoring
git add .
git commit -m "FASE 1 Complete: Documentation Validation Automation"
git push -u origin docs/refactoring
```

### Crea PR
```bash
gh pr create --title "FASE 1 Complete: Documentation Validation" \
  --body "FASE 1 of documentation refactoring complete:

✅ 3 validation scripts (SP/MS, JSON, links)
✅ CI/CD GitHub Actions pipeline
✅ Fixed 11 TROUBLESHOUTING→TROUBLESHOOTING files
✅ Documented SP28 reserved gap

Ready for Phase 2: Content quality improvements
"
```

### Merge (dopo approval)
```bash
gh pr merge 123 --squash
git checkout main
git pull
git tag v1.0-phase-1-complete
git push origin v1.0-phase-1-complete
```

---

## 8️⃣ Troubleshooting

### Errore: "Python3 not found"
```bash
# Installa Python 3.11+
brew install python3  # macOS
sudo apt-get install python3  # Linux
```

### Errore: "Permission denied" su script
```bash
chmod +x scripts/*.py scripts/*.sh
```

### Errore: "Module not found"
```bash
# Gli script usano solo librerie standard (json, re, pathlib)
# Non servono dipendenze esterne
```

### Report vuoto
```bash
# Assicurati di essere nella cartella giusta
cd /path/to/ZenIA
ls -la scripts/run_all_checks.sh  # Deve esistere
```

---

## 9️⃣ Prossimo Step: FASE 2

Quando sei pronto per FASE 2 (Qualità Contenuti):

1. **Fix 45 JSON invalidi**
   - Identificati in `scripts/reports/json_validation.json`
   - Correggi sintassi nei file MD

2. **Rimuovi 3 pseudo-codice**
   - UC5/01 SP11 - Security & Audit.md
   - UC5/02 Sottoprogetti con Pipeline Operative.md
   - UC11/00 Architettura UC11.md
   - Sostituisci con flowchart mermaid

3. **Crea glossario**
   - Decidi terminologia italiano/inglese
   - Crea `docs/GLOSSARIO.md` con 50+ termini

---

## 📞 Supporto

**Problemi?**
- Controlla `FASE-1-COMPLETAMENTO.md` per dettagli
- Vedi `PIANO-REFACTORING-DOCUMENTAZIONE.md` per timeline
- Slack: `#zenia-docs-refactoring`

---

**Versione**: 1.0
**Data**: 2025-11-19
**Status**: ✅ FASE 1 COMPLETATA
