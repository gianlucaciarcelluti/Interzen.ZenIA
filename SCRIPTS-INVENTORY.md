# Scripts Inventory & Organization

## Overview

The `scripts/` directory contains the **unified validation system** for the ZenIA documentation. All scripts are actively used and maintained.

**Total Active Scripts: 16**

---

## Core Orchestration

### `run_all_checks.sh`
**Purpose**: Main orchestrator that runs all 15 validators in sequence

**Tiers**:
- TIER 1: Critical checks (blocks on failure)
- TIER 2: Content quality checks (non-blocking warnings)
- TIER 3: Lint & style checks (non-blocking warnings)

**Usage**:
```bash
./scripts/run_all_checks.sh          # Run all checks
./scripts/run_all_checks.sh --quick  # TIER 1 only
./scripts/run_all_checks.sh --verbose # Detailed output
```

---

## TIER 1: Critical Validators (Blocking)

These validators **block commits/merges** if they fail. All must pass for TIER 1 PASS.

### `verify_sp_references.py`
**Validates**: SP/MS references and UC mappings

**Checks**:
- All SP01-SP72 references are correct (SP28 excluded)
- Valid UC mappings for each SP
- Only authorized files reference SP28
- No invalid reference patterns

**Exit Code**: 0 (pass) or 1 (fail - blocks)

### `verify_uc_archetype.py`
**Validates**: UC structure completeness

**Checks**:
- All 11 UC have required files:
  - `00-ARCHITECTURE.md`
  - `01-OVERVIEW.md`
  - `02-DEPENDENCIES.md`
  - `README.md`
- Minimum 70% structure completeness

**Exit Code**: 0 (pass) or 1 (fail - blocks)

### `verify_sp_completeness.py`
**Validates**: SP file organization

**Checks**:
- All 71 SP present (SP01-SP72 excluding SP28)
- No missing SP
- No duplicate SP across UC
- Correct SP to UC mapping

**Exit Code**: 0 (pass/perfect) or 1 (fail - blocks)

### `verify_markdown_headings.py`
**Validates**: Markdown heading hierarchy

**Checks**:
- No H1→H3 jumps (proper hierarchy)
- No duplicate headings
- Proper nesting structure

**Status**: Currently warnings only (non-blocking)

### `verify_mermaid_diagrams.py`
**Validates**: Mermaid diagram syntax

**Checks**:
- Valid Mermaid diagram syntax
- Proper node definitions
- Valid connections
- No syntax errors

**Exit Code**: 0 (pass) or 1 (fail - blocks)

---

## TIER 2: Content Quality Validators (Non-Blocking)

These validators check content quality and provide warnings. They do **not block merges**.

### `verify_section_completeness.py`
**Validates**: Required content sections in SP files

**Checks**:
- Overview / Panoramica
- Technical Details / Dettagli Tecnici
- Use Cases / Casi d'Uso
- Error Handling / Gestione Errori

**Status**: 0% complete (non-blocking, content creation needed)

### `verify_language_coherence.py`
**Validates**: Consistent English/Italian usage

**Checks**:
- No language mixing in critical sections
- Consistent terminology
- Proper language declaration

**Status**: ✅ PASSING

### `verify_payload_validation.py`
**Validates**: JSON request/response examples

**Checks**:
- Valid JSON structure
- Proper schema compliance
- No syntax errors

**Status**: ✅ PASSING

### `verify_cross_references.py`
**Validates**: Internal UC/SP references

**Checks**:
- Valid cross-reference links
- Correct reference ranges
- No broken internal references

**Status**: Non-blocking warnings

---

## TIER 3: Lint & Style Validators (Non-Blocking)

These validators check formatting and style. They do **not block merges**.

### `verify_whitespace_formatting.py`
**Validates**: Code style and formatting

**Checks**:
- No trailing spaces
- No tab/space mixing
- Lines ≤120 characters

**Status**: ~1978 style warnings (non-blocking)

### `verify_orphaned_images.py`
**Validates**: Image asset usage

**Checks**:
- No unused images
- All referenced images exist
- Proper image paths

**Status**: Non-blocking warnings

### `verify_content_duplicates.py`
**Validates**: Content duplication

**Checks**:
- No identical duplicate sections
- Detects copy-paste issues
- May be intentional

**Status**: Non-blocking warnings

### `verify_readme_metadata.py`
**Validates**: README file structure

**Checks**:
- Version information present
- Date metadata present
- Status field present

**Status**: ✅ PASSING

### `verify_json_examples.py`
**Validates**: JSON payload validity

**Checks**:
- Valid JSON structure
- Proper formatting
- No syntax errors

**Status**: ✅ PASSING

### `verify_links.py`
**Validates**: Internal link validity

**Checks**:
- No broken internal links
- Valid relative paths
- Proper link formatting

**Status**: ✅ PASSING (0 broken links)

---

## Report Output

All validators generate JSON reports in `scripts/reports/`:

```
scripts/reports/
├── sp_ms_references.json              (TIER 1)
├── uc_archetype_validation.json       (TIER 1)
├── sp_completeness_validation.json    (TIER 1)
├── markdown_headings_validation.json  (TIER 1)
├── mermaid_diagrams_validation.json   (TIER 1)
├── section_completeness_validation.json (TIER 2)
├── language_coherence_validation.json (TIER 2)
├── payload_validation.json            (TIER 2)
├── cross_references_validation.json   (TIER 2)
├── whitespace_formatting_validation.json (TIER 3)
├── orphaned_images_validation.json    (TIER 3)
├── content_duplicates_validation.json (TIER 3)
├── readme_metadata_validation.json    (TIER 3)
├── json_validation.json               (TIER 3)
└── links_validation.json              (TIER 3)
```

---

## Deleted Scripts

**50 obsolete scripts removed**:
- UC rename scripts (25 files): Historical UC refactoring
- General migration scripts (5 files): One-time migrations
- Fixup scripts (15 files): One-time corrections
- Old verifiers (3 files): Superseded by current system
- Empty directories (1): Accidentally created

These were migration and one-time fixup scripts from earlier phases. They are no longer needed.

---

## Integration with CI/CD

### GitHub Actions
- **Workflow**: `.github/workflows/docs-validation.yml`
- **Trigger**: Push to `main`/`razionalizzazione-sp`/`develop` or PR to `main`/`razionalizzazione-sp`
- **Behavior**:
  - Runs `./scripts/run_all_checks.sh`
  - Uploads all reports as artifacts
  - Posts PR comment with results
  - Blocks merge only on TIER 1 FAIL

### PR Comments
- Automatic comment posted after validation
- Shows TIER 1 status (PASS/FAIL)
- Links to artifacts and debugging instructions
- Provides commands for local testing

---

## Usage Examples

### Run all validators
```bash
./scripts/run_all_checks.sh
```

### Run TIER 1 only (fast mode)
```bash
./scripts/run_all_checks.sh --quick
```

### Run with detailed output
```bash
./scripts/run_all_checks.sh --verbose
```

### Run single validator
```bash
python3 scripts/verify_sp_completeness.py
python3 scripts/verify_links.py
```

### View detailed reports
```bash
cat scripts/reports/sp_completeness_validation.json | jq
cat scripts/reports/links_validation.json | jq
```

---

## Validation Results Summary

| Validator | TIER | Status | Type |
|-----------|------|--------|------|
| SP/MS References | 1 | ✅ PASS | Blocking |
| UC Archetype | 1 | ✅ PASS | Blocking |
| SP Completeness | 1 | ✅ PASS | Blocking |
| Markdown Headings | 1 | ⚠️ WARNING | Blocking (warnings only) |
| Mermaid Diagrams | 1 | ✅ PASS | Blocking |
| Section Completeness | 2 | ⚠️ 0% | Non-blocking |
| Language Coherence | 2 | ✅ PASS | Non-blocking |
| Payload Validation | 2 | ✅ PASS | Non-blocking |
| Cross-References | 2 | ⚠️ WARNING | Non-blocking |
| Whitespace | 3 | ⚠️ 1978 | Non-blocking |
| Orphaned Images | 3 | ⚠️ WARNING | Non-blocking |
| Content Duplicates | 3 | ⚠️ WARNING | Non-blocking |
| README Metadata | 3 | ✅ PASS | Non-blocking |
| JSON Examples | 3 | ✅ PASS | Non-blocking |
| Links | 3 | ✅ PASS | Non-blocking |

---

## Future Enhancements

- Auto-fix script for whitespace issues
- Metrics dashboard for tracking over time
- Slack notifications on TIER 1 failures
- Machine learning for duplicate detection
- Historical validation trend analysis

---

**Last Updated**: 2025-11-20  
**Status**: Production Ready ✅  
**Active Scripts**: 16  
**Total Validators**: 15
