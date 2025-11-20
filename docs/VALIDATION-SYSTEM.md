# Documentation Validation System

## Overview

The ZenIA documentation validation system is a **3-TIER quality assurance framework** that ensures documentation quality while allowing iterative improvements. Only **TIER 1 (Critical)** checks block commits/merges. **TIER 2 and TIER 3** are warnings for continuous improvement.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  LOCAL: ./scripts/run_all_checks.sh                     │
│  (Runs all 15 validators, shows real-time feedback)     │
└─────────────────────────────────────────────────────────┘
         ↓
         ↓ (git push)
         ↓
┌─────────────────────────────────────────────────────────┐
│  CI/CD: .github/workflows/docs-validation.yml           │
│  (Runs complete validation suite on each commit/PR)     │
└─────────────────────────────────────────────────────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
  PASS    FAIL (TIER 1 only)
   │        │
   ✅       ❌
  MERGE   MUST FIX
  READY
```

## Validation Tiers

### TIER 1: CRITICAL (Blocking) 🚫

**Status**: MUST PASS before commit/merge

5 critical checks:

1. **SP/MS References** (`verify_sp_references.py`)
   - Validates SP01-SP72 references are correct
   - No invalid UC mappings
   - Only authorized files reference reserved SP28
   - **Failure**: Blocks commit

2. **UC Archetype** (`verify_uc_archetype.py`)
   - All 11 UC have required files: 00-ARCHITECTURE.md, 01-OVERVIEW.md, 02-DEPENDENCIES.md, README.md
   - Minimum 70% structure completeness
   - **Failure**: Blocks commit (when below threshold)

3. **SP Completeness** (`verify_sp_completeness.py`)
   - All 71 SP present (SP01-SP72 excluding SP28)
   - No missing SP
   - No duplicate SP across UC
   - **Failure**: Blocks commit

4. **Markdown Headings** (`verify_markdown_headings.py`)
   - Proper heading hierarchy (no H1→H3 jumps)
   - No duplicate headings
   - **Status**: Currently warnings only (non-blocking)

5. **Mermaid Diagrams** (`verify_mermaid_diagrams.py`)
   - Valid Mermaid diagram syntax
   - Proper node definitions
   - **Failure**: Blocks commit

**Typical errors that block**:
- Missing required SP files
- Broken UC archetype
- Invalid diagram syntax

**View results**:
```bash
./scripts/run_all_checks.sh
# Look for: ✅ TIER 1 PASS
```

### TIER 2: CONTENT QUALITY (Warnings) ⚠️

**Status**: Non-blocking, but important to address

4 content quality checks:

1. **Section Completeness** (`verify_section_completeness.py`)
   - SP files should have: Overview, Technical Details, Use Cases, Error Handling sections
   - **Current**: 0% complete, non-blocking warning
   - **Effort**: High (content creation)

2. **Language Coherence** (`verify_language_coherence.py`)
   - Consistent English/Italian usage
   - No mixing languages in critical sections
   - **Status**: ✅ PASSING

3. **Payload Validation** (`verify_payload_validation.py`)
   - JSON request/response examples are valid
   - **Status**: ✅ PASSING

4. **Cross-References** (`verify_cross_references.py`)
   - Internal UC/SP references are valid
   - Link ranges correct
   - **Status**: Warnings (non-blocking)

**Typical warnings**:
- Missing section headers
- Language inconsistency
- Invalid cross-reference ranges

**View results**:
```bash
cat scripts/reports/section_completeness_validation.json
cat scripts/reports/language_coherence_validation.json
```

### TIER 3: LINT & STYLE (Warnings) 🧹

**Status**: Non-blocking style/formatting issues

6 lint checks:

1. **Whitespace Formatting** (`verify_whitespace_formatting.py`)
   - No trailing spaces
   - No tab/space mixing
   - Lines ≤120 characters
   - **Current**: 1978 style warnings (non-blocking)
   - **Effort**: Very high

2. **Orphaned Images** (`verify_orphaned_images.py`)
   - No unused images
   - All referenced images exist
   - **Status**: Warnings (low priority)

3. **Content Duplicates** (`verify_content_duplicates.py`)
   - No identical duplicate sections
   - Detects copy-paste issues
   - **Status**: Warnings (may be intentional)

4. **README Metadata** (`verify_readme_metadata.py`)
   - README files have version, date, status
   - **Status**: ✅ PASSING

5. **JSON Examples** (`verify_json_examples.py`)
   - JSON payloads are valid
   - **Status**: ✅ PASSING

6. **Links** (`verify_links.py`)
   - No broken internal links
   - All references valid
   - **Status**: ✅ PASSING (14→0 broken links)

**Typical warnings**:
- Lines too long (>120 chars)
- Trailing whitespace
- Unused images
- Duplicate sections

**View results**:
```bash
cat scripts/reports/whitespace_formatting_validation.json
cat scripts/reports/orphaned_images_validation.json
```

## Local Usage

### Run Complete Validation

```bash
# Run all checks (15 total)
./scripts/run_all_checks.sh

# Output shows:
# - TIER 1 (Critical) checks
# - TIER 2 (Content Quality) checks
# - TIER 3 (Lint) checks
# - Color-coded feedback (✅ 🟡 ~)
# - Report hints for failures
```

### Run Specific Validator

```bash
# Run only SP references validation
python3 scripts/verify_sp_references.py

# Run only links validation
python3 scripts/verify_links.py

# Run only section completeness
python3 scripts/verify_section_completeness.py
```

### View Detailed Reports

```bash
# Open validation reports (JSON format)
cat scripts/reports/sp_ms_references.json
cat scripts/reports/uc_archetype_validation.json
cat scripts/reports/sp_completeness_validation.json

# Use jq for pretty printing
cat scripts/reports/sp_ms_references.json | jq
```

### Quick Mode vs Verbose

```bash
# Quick mode (only TIER 1, ~20 lines output)
./scripts/run_all_checks.sh

# Quick with all TIER 2-3 checks
./scripts/run_all_checks.sh

# Verbose mode (detailed output)
./scripts/run_all_checks.sh --verbose
```

## CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/docs-validation.yml`

**Workflow Sequence** (all steps run sequentially):

```
1️⃣ Checkout code
     ↓
2️⃣ Set up Python 3.11
     ↓
3️⃣ Run Complete Validation Suite (./scripts/run_all_checks.sh)
     ↓
4️⃣ Upload validation reports as artifacts (if any failures)
     ↓
5️⃣ Display validation summary to logs
     ↓
6️⃣ Check TIER 1 Results (blocks if FAIL)
     ↓
7️⃣ Post PR Comment with Results (sequential after validation)
     ↓
✅ or ❌ Workflow completes
```

**Triggers**:
- On push to: `main`, `razionalizzazione-sp`, `develop`
- On PR to: `main`, `razionalizzazione-sp`
- When docs or scripts change

**Behavior**:
- All steps run sequentially (not in parallel)
- Validation completes first
- PR comment posted AFTER validation results are available
- Comment includes links to artifacts and debug instructions
- Only blocks merge if TIER 1 validation FAILS

**Checking Results**:
1. Go to Actions tab → Click validation run
2. See real-time validation summary in logs
3. Download "validation-reports" artifact
4. Review JSON files for detailed errors
5. PR comment provides direct links and instructions

## Decision Logic

### When Workflow PASSES ✅

```
Validation Suite Completes
     ↓
✅ TIER 1 PASS
     ↓
📝 PR Comment Posted (with artifacts links)
     ↓
🟢 Merge Enabled
     ├─ All critical checks successful
     ├─ TIER 2 warnings logged (non-blocking)
     └─ TIER 3 warnings logged (non-blocking)
```

### When Workflow FAILS ❌

```
Validation Suite Completes
     ↓
❌ TIER 1 FAIL
     ↓
📝 PR Comment Posted (with error details)
     ↓
🔴 Merge Blocked
     ├─ One or more critical checks failed
     ├─ PR comment shows which checks failed
     └─ Developer must fix and re-push
```

### PR Comment Experience

**Automatic PR Comment Posted After Validation**:
- Shows TIER 1 status (✅ PASS or ❌ FAIL)
- Provides direct link to Actions tab
- Lists artifact download instructions
- Includes `./scripts/run_all_checks.sh` debugging tip
- Timestamps completion for audit trail

## Configuration & Customization

### Adjust TIER Levels

Edit `.github/workflows/docs-validation.yml`:

```yaml
# Current: Only TIER 1 blocks
# To make TIER 2 block too, change:
if grep -q "TIER 2 FAIL" validation_output.txt; then
  exit 1
fi
```

### Adjust Thresholds

Edit individual validator scripts:

```python
# verify_sp_completeness.py, line 208
if summary['errors'] == 0 and len(summary['extra_sp']) == 0:
    print("✅ SP COMPLETENESS: PERFECT")
    return 0
```

### Add New Validators

1. Create `scripts/verify_my_check.py`
2. Add to `scripts/run_all_checks.sh`:
   ```bash
   run_check "🔟" "My Check Name" "verify_my_check.py"
   ```
3. Update workflow triggers in `.github/workflows/docs-validation.yml`

## Troubleshooting

### Validation fails locally but passes in CI?

- Ensure Python 3.11+ installed: `python3 --version`
- Reinstall dependencies: `pip install -r requirements.txt` (if exists)
- Run with `--verbose`: `./scripts/run_all_checks.sh --verbose`

### "TIER 1 FAIL" but don't see the error?

1. Check workflow logs: Actions tab → Select run → Logs
2. Download validation-reports artifact
3. Look in reports/ JSON files for specific error details
4. Run `./scripts/run_all_checks.sh --verbose` locally

### My PR comment didn't appear?

- Check Actions tab for `Documentation Commenter` workflow
- If failed, check permissions in `.github/workflows/docs-comment.yml`
- Ensure `GITHUB_TOKEN` has `issues: write` permission

## Performance

- **Local**: ~5-10 seconds (277 files, 15 validators)
- **CI**: ~20-30 seconds (includes artifact upload)
- **Reports**: 15 JSON files in `scripts/reports/`
- **Artifact retention**: 30 days

## Future Enhancements

### Planned for Next Phase

1. **Markdown Headings**: Make blocking (fix 202 heading errors)
2. **Section Completeness**: Add SP section templates
3. **Whitespace**: Auto-fix script for long lines
4. **Content Duplicates**: Identify copy-paste candidates
5. **Metrics Dashboard**: Weekly validation metrics tracking

### Optional Improvements

- Slack notifications on TIER 1 failures
- Automated fixes for whitespace issues
- Machine learning for duplicate detection
- Historical trend analysis

## Workflow Architecture

### Single Consolidated Workflow Design

The system uses **one unified workflow** (`docs-validation.yml`) that handles both validation and PR commenting sequentially:

**Key Design Decisions**:
- ✅ **Single Source of Truth**: One workflow file manages all validation logic
- ✅ **Sequential Execution**: All steps run in order (no parallel race conditions)
- ✅ **Reliable PR Commenting**: Comment posted after validation completes with accurate data
- ✅ **Artifact Management**: Reports uploaded before comment posting ensures links work
- ✅ **Clear Feedback**: Developers see validation results in PR comments immediately

**Previous vs. Current**:
- ❌ **Before**: Separate workflows (`docs-validation.yml` + `docs-comment.yml`) could race
- ❌ **Before**: Comment might post before validation finished
- ✅ **Now**: Single workflow ensures sequential, reliable execution

## References

- [Validation Scripts](../scripts/)
- [UC Archetype Specification](./DOCUMENTATION-STRUCTURE-GUIDE.md)
- [SP Mapping](./ARCHITECTURE-OVERVIEW.md)
- [GitHub Actions Workflows](../.github/workflows/)

---

**Last Updated**: 2025-11-20
**Status**: Production Ready ✅
**TIER 1 Pass Rate**: 100%
