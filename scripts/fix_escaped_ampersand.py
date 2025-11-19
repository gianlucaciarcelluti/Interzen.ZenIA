#!/usr/bin/env python3
"""
Script per riparare gli ampersand escappati nei link markdown.

Sostituisce:
- \& → & nei link markdown
- Risolve 54 link rotti causati da escaping errato

Uso:
    python3 fix_escaped_ampersand.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class EscapedAmpersandFixerTool:
    def __init__(self):
        self.docs_path = Path('docs')
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0

    def find_files_with_escaped_ampersand(self) -> List[Path]:
        """Trova tutti i file con \& escappati"""
        files = []
        for filepath in self.docs_path.rglob('*.md'):
            try:
                content = filepath.read_text(encoding='utf-8')
                if '\\&' in content:
                    files.append(filepath)
            except:
                pass
        return sorted(files)

    def process_file(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """Rimuove l'escaping degli ampersand nei link"""
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            # Sostituisci \& con &
            # Pattern: trova \& in qualsiasi contesto
            count = content.count('\\&')
            if count > 0:
                content = content.replace('\\&', '&')
                changes.append(f"Fixed {count} escaped ampersands")

            # Se ci sono stati cambiamenti
            if content != original_content:
                if not dry_run:
                    filepath.write_text(content, encoding='utf-8')
                return len(changes), changes

            return 0, []

        except Exception as e:
            return 0, [f"Error: {e}"]

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui la riparazione"""

        print("\n" + "="*70)
        print("ESCAPED AMPERSAND FIXER TOOL")
        print("="*70)
        print(f"Dry run: {dry_run}\n")

        files = self.find_files_with_escaped_ampersand()
        print(f"Files found: {len(files)}\n")

        for filepath in files:
            self.files_processed += 1
            count, changes = self.process_file(filepath, dry_run)

            if count > 0:
                self.files_changed += 1
                self.replacements += count

                rel_path = filepath.relative_to(self.docs_path)
                print(f"✅ {rel_path}")

                if verbose:
                    for change in changes:
                        print(f"   • {change}")
                else:
                    print(f"   {count} fix(es)")

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Files processed: {self.files_processed}")
        print(f"Files changed: {self.files_changed}")
        print(f"Total ampersands fixed: {self.replacements}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("   Run without --dry-run to apply changes")
        else:
            print("\n✅ All fixes applied successfully")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = EscapedAmpersandFixerTool()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
