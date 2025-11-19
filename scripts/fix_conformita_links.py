#!/usr/bin/env python3
"""
Script per correggere i link nella sezione Conformità Normativa.
Cambia da ./templates e ./COMPLIANCE-MATRIX.md a ../../templates e ../../COMPLIANCE-MATRIX.md
"""

import os
import re
import sys
from pathlib import Path

def fix_conformita_links(filepath: Path, dry_run: bool = False) -> tuple[bool, str]:
    """Corregge i link nella sezione Conformità Normativa"""

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verifica se il file ha la sezione Conformità Normativa
        if "## 🏛️ Conformità Normativa" not in content:
            return True, f"⏭️  {filepath.name}: Nessuna sezione conformità"

        # Conta quanti link errati ci sono
        old_count = content.count("./templates/conformita-normativa-standard.md")
        old_count += content.count("./COMPLIANCE-MATRIX.md")

        if old_count == 0:
            return True, f"✓ {filepath.name}: Link già corretti"

        # Correggi i link
        new_content = content.replace(
            "./templates/conformita-normativa-standard.md",
            "../../templates/conformita-normativa-standard.md"
        )
        new_content = new_content.replace(
            "./COMPLIANCE-MATRIX.md",
            "../../COMPLIANCE-MATRIX.md"
        )

        if dry_run:
            return True, f"(DRY-RUN) {filepath.name}: {old_count} link corrigibili"
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"✅ {filepath.name}: {old_count} link corretti"

    except Exception as e:
        return False, f"❌ {filepath.name}: {str(e)}"

def main():
    dry_run = '--dry-run' in sys.argv

    base_path = Path(__file__).parent.parent / 'docs' / 'use_cases'

    if not base_path.exists():
        print(f"❌ Cartella non trovata: {base_path}")
        sys.exit(1)

    # Trova tutti i file SP
    sp_files = []
    for uc_folder in sorted(base_path.glob('UC*')):
        if uc_folder.is_dir():
            for sp_file in sorted(uc_folder.glob('01 SP*.md')):
                sp_files.append(sp_file)

    if not sp_files:
        print("❌ Nessun file SP trovato")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"Correzione link Conformità Normativa in {len(sp_files)} file")
    print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"{'='*70}\n")

    fixed_count = 0
    skip_count = 0
    error_count = 0

    for i, sp_file in enumerate(sp_files, 1):
        success, message = fix_conformita_links(sp_file, dry_run=dry_run)

        if "DRY-RUN" in message or "già corretti" in message or "Nessuna sezione" in message:
            skip_count += 1
        elif success:
            fixed_count += 1
        else:
            error_count += 1

        if i % 10 == 0 or error_count > 0:
            print(f"[{i:2}/{len(sp_files)}] {message}")

    print(f"\n{'='*70}")
    print(f"RIEPILOGO:")
    print(f"  ✅ Corretti: {fixed_count}")
    print(f"  ⏭️  Saltati: {skip_count}")
    print(f"  ❌ Errori: {error_count}")
    print(f"{'='*70}\n")

    if dry_run:
        print("Modalità DRY-RUN: nessun file modificato.")

    sys.exit(0 if error_count == 0 else 1)

if __name__ == '__main__':
    main()
