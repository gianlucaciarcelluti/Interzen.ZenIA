#!/usr/bin/env python3
"""
Script per rimuovere i riferimenti ai file eliminati.

Rimuove link a file che non esistono più:
- Architettura UC (non documentate)
- Deprecated files (UC5)
- File incompleti (UC2)
- Template paths errati

Uso:
    python3 clean_deleted_references.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class DeletedReferencesCleanerTool:
    def __init__(self):
        self.docs_path = Path('docs')
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0

    def get_files_to_clean(self) -> List[Tuple[Path, List[str]]]:
        """Restituisce file e pattern di link da rimuovere"""
        return [
            # UC1 - Architettura non documentata
            (
                self.docs_path / 'use_cases' / 'UC1 - Sistema di Gestione Documentale' / 'README.md',
                [r'^\|\s*Architettura Generale.*\n.*\[Vai\]\(./00 Architettura UC1.md\).*\n']
            ),
            # UC2 - Architettura non documentata + SP incompleto
            (
                self.docs_path / 'use_cases' / 'UC2 - Protocollo Informatico' / 'README.md',
                [
                    r'^\|\s*Architettura Generale.*\n.*\[Vai\]\(./00 Architettura UC2.md\).*\n',
                    r'^\|\s*SP01 - EML Parser.*UC2 Protocol.*\n.*\[Vai\]\(.*SP01.*UC2 Protocol.*\n'
                ]
            ),
            # UC5 - Architettura non documentata + Deprecated file
            (
                self.docs_path / 'use_cases' / 'UC5 - Produzione Documentale Integrata' / 'README.md',
                [r'^\|\s*Architettura Generale.*\n.*\[Vai\]\(./00 Architettura UC5.md\).*\n']
            ),
            # UC5 - Canonical: Riferimento a file deprecated rimosso
            (
                self.docs_path / 'use_cases' / 'UC5 - Produzione Documentale Integrata' / '01 CANONICAL - Generazione Atto Completo.md',
                [r'\[04 DEPRECATED.*\]\(04 DEPRECATED - Sequence Con SP00.md\)']
            ),
        ]

    def process_file(self, filepath: Path, patterns: List[str], dry_run: bool = False) -> Tuple[int, List[str]]:
        """Rimuove i pattern di link dal file"""
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            count = 0
            for pattern in patterns:
                matches = list(re.finditer(pattern, content, re.MULTILINE))
                if matches:
                    count += len(matches)
                    content = re.sub(pattern, '', content, flags=re.MULTILINE)
                    changes.append(f"Removed {len(matches)} reference(s) matching pattern")

            # Se ci sono stati cambiamenti
            if content != original_content:
                if not dry_run:
                    filepath.write_text(content, encoding='utf-8')
                return count, changes

            return 0, []

        except Exception as e:
            return 0, [f"Error: {e}"]

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui la pulizia"""

        print("\n" + "="*70)
        print("DELETED REFERENCES CLEANER TOOL")
        print("="*70)
        print(f"Dry run: {dry_run}\n")

        files_to_clean = self.get_files_to_clean()
        print(f"Files to check: {len(files_to_clean)}\n")

        for filepath, patterns in files_to_clean:
            if not filepath.exists():
                print(f"⚠️  {filepath.relative_to(self.docs_path)} - FILE NOT FOUND")
                continue

            self.files_processed += 1
            count, changes = self.process_file(filepath, patterns, dry_run)

            if count > 0:
                self.files_changed += 1
                self.replacements += count

                rel_path = filepath.relative_to(self.docs_path)
                print(f"✅ {rel_path}")

                if verbose:
                    for change in changes:
                        print(f"   • {change}")
                else:
                    print(f"   {count} removal(s)")

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Files processed: {self.files_processed}")
        print(f"Files changed: {self.files_changed}")
        print(f"Total removals: {self.replacements}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("   Run without --dry-run to apply changes")
        else:
            print("\n✅ All cleanups applied successfully")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = DeletedReferencesCleanerTool()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
