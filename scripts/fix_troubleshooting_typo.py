#!/usr/bin/env python3
"""
Script to fix TROUBLESHOUTING typo → TROUBLESHOOTING.

Sostituisce tutte le occorrenze del typo:
- TROUBLESHOUTING → TROUBLESHOOTING

Uso:
    python3 fix_troubleshooting_typo.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class TroubleshootingTypoFixerTool:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.docs_path = self.root_path / 'docs'
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0
        self.changes_log = []

    def find_files_with_typo(self) -> List[Path]:
        """Trova tutti i file che contengono TROUBLESHOUTING typo"""
        files = []

        # Cerca in tutti i file markdown e yaml
        for filepath in list(self.docs_path.rglob('*.md')) + list(self.root_path.glob('*.md')):
            try:
                content = filepath.read_text(encoding='utf-8')
                if 'TROUBLESHOUTING' in content:
                    files.append(filepath)
            except:
                pass

        return sorted(files)

    def process_file(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """Correggi il typo nel file"""
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            # Sostituisci TROUBLESHOUTING con TROUBLESHOOTING
            count = content.count('TROUBLESHOUTING')
            if count > 0:
                content = content.replace('TROUBLESHOUTING', 'TROUBLESHOOTING')
                changes.append(f"Fixed {count} TROUBLESHOUTING → TROUBLESHOOTING")

            # Se ci sono stati cambiamenti
            if content != original_content:
                if not dry_run:
                    filepath.write_text(content, encoding='utf-8')
                return count, changes

            return 0, []

        except Exception as e:
            return 0, [f"Error: {e}"]

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui la correzione"""

        print("\n" + "="*70)
        print("TROUBLESHOUTING TYPO FIXER TOOL")
        print("="*70)
        print(f"Dry run: {dry_run}\n")

        files = self.find_files_with_typo()
        print(f"Files found with TROUBLESHOUTING typo: {len(files)}\n")

        for filepath in files:
            self.files_processed += 1
            count, changes = self.process_file(filepath, dry_run)

            if count > 0:
                self.files_changed += 1
                self.replacements += count

                # Determine relative path
                try:
                    rel_path = filepath.relative_to(self.docs_path)
                except ValueError:
                    rel_path = filepath.relative_to(self.root_path)

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
        print(f"Total fixes: {self.replacements}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("   Run without --dry-run to apply changes")
        else:
            print("\n✅ All fixes applied successfully")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = TroubleshootingTypoFixerTool()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
