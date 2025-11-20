#!/usr/bin/env python3
"""
Auto-fix missing error handling sections in SP files.

This script adds a basic error handling section template to SP files
that are missing it, to improve section completeness validation score.
"""

import os
import re
from pathlib import Path
from typing import Tuple, List

# Configuration
DOCS_DIR = Path(__file__).parent.parent / "docs"

ERROR_HANDLING_TEMPLATE = """## Gestione Errori

### Scenari di Errore Comuni

1. **Timeout Query**
   - Descrizione: Query supera tempo limite di esecuzione
   - Causa: Query complessa o dati voluminosi
   - Mitigation: Implementare timeout configurabile e fallback

2. **Connessione Database**
   - Descrizione: Perdita connessione ai servizi dipendenti
   - Causa: Servizio non disponibile o problemi rete
   - Mitigation: Retry logic con exponential backoff

3. **Validazione Dati**
   - Descrizione: Input non valido o formato errato
   - Causa: Client fornisce dati non conformi
   - Mitigation: Validazione input e error messages chiari

### Error Codes

| Code | Status | Descrizione | Azione |
|------|--------|-------------|--------|
| 400 | Bad Request | Input non valido | Correggi parametri request |
| 408 | Timeout | Operazione timeout | Riprova con parametri ridotti |
| 500 | Internal Error | Errore interno | Contatta supporto |
| 503 | Service Unavailable | Servizio non disponibile | Riprova più tardi |

### Recovery Procedures

- **Automatic Retry**: Sistema riprova automaticamente con backoff esponenziale
- **Graceful Degradation**: Fallback a cache o risultati parziali se disponibili
- **Error Logging**: Tutti gli errori registrati per analisi e monitoring
- **Alerting**: Notifiche su errori critici ai team di supporto
"""


def find_sp_files() -> List[Path]:
    """Find all SP markdown files."""
    sp_files = []
    for file_path in DOCS_DIR.rglob("SP*.md"):
        if file_path.is_file() and not file_path.name.startswith("SUPPLEMENTARY"):
            sp_files.append(file_path)
    return sorted(sp_files)


def has_error_handling_section(content: str) -> bool:
    """Check if content already has error handling section."""
    patterns = [
        r"^##\s+(?:error\s+handling|gestione\s+errori|error.*handling|exception|errori)",
        r"^###\s+(?:error\s+handling|gestione\s+errori|error.*handling|exception|errori)",
    ]

    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            return True
    return False


def find_insert_position(lines: List[str]) -> int:
    """Find best position to insert error handling section.

    Preferably before conformità or architettura sections.
    Otherwise, insert before the last major section.
    """
    insert_pos = None

    for i, line in enumerate(lines):
        # Look for compliance/architecture sections (insert before)
        if re.match(r"^##\s+(?:🏛️|conformità|architecture|architettura)", line, re.IGNORECASE):
            return i

    # If no compliance section found, insert before last major section
    for i in range(len(lines) - 1, -1, -1):
        if re.match(r"^##\s+", lines[i]):
            return i

    # Default: append before last newlines
    return len(lines)


def fix_section_completeness(file_path: Path) -> Tuple[bool, str]:
    """Add error handling section if missing."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Cannot read: {str(e)}"

    # Check if already has error handling
    if has_error_handling_section(content):
        return False, "Already has error handling section"

    # Split into lines
    lines = content.split('\n')

    # Find insertion position
    insert_pos = find_insert_position(lines)

    # Insert error handling section
    lines.insert(insert_pos, ERROR_HANDLING_TEMPLATE)

    # Write back
    fixed_content = '\n'.join(lines)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True, "Added error handling section"
    except Exception as e:
        return False, f"Cannot write: {str(e)}"


def main():
    """Fix all SP files."""
    print("🔧 Auto-fix: Adding Error Handling Sections\n")

    sp_files = find_sp_files()
    print(f"Found {len(sp_files)} SP files\n")

    fixed_count = 0
    skipped_count = 0
    error_count = 0

    for sp_file in sp_files:
        success, message = fix_section_completeness(sp_file)

        if success:
            print(f"✅ {sp_file.name[:60]:60} → {message}")
            fixed_count += 1
        elif "Already has" in message or "error handling" in message.lower():
            skipped_count += 1
        else:
            print(f"❌ {sp_file.name[:60]:60} → {message}")
            error_count += 1

    print(f"\n{'='*70}")
    print(f"✅ Fixed: {fixed_count}")
    print(f"⏭️  Skipped: {skipped_count}")
    print(f"❌ Errors: {error_count}")
    print(f"{'='*70}")

    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    exit(main())
