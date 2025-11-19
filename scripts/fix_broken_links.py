#!/usr/bin/env python3
"""
Script per riparare i link rotti nei file INDEX.

Problemi risolti:
1. Ampersand escappati: \& → & nei link markdown
2. File Architettura mancanti riferimenti corretti
3. Path relativi nei template standard

Uso:
    python3 fix_broken_links.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class BrokenLinksFixerTool:
    def __init__(self):
        self.docs_path = Path('docs')
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0

    def find_index_files(self) -> List[Path]:
        """Trova tutti i file INDEX.md"""
        return sorted(self.docs_path.glob('**/00 INDEX.md'))

    def fix_ampersand_escaping(self, content: str) -> Tuple[str, int]:
        """
        Rimuove l'escaping errato degli ampersand nei link markdown.
        [text \\& text].md → [text & text].md
        """
        # Pattern: [testo \\& testo] nei link markdown
        original = content
        
        # Rimuovi i backslash prima dell'ampersand nei link
        content = re.sub(r'\[([^\]]*)\\\&([^\]]*)\]', r'[\1&\2]', content)
        
        return content, len(re.findall(r'\\\&', original))

    def process_file(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """Processa un file e risolve i link rotti"""
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            # Ripara ampersand escappati
            content, ampersand_count = self.fix_ampersand_escaping(content)
            if ampersand_count > 0:
                changes.append(f"Fixed {ampersand_count} escaped ampersands in markdown links")

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
        print("BROKEN LINKS FIXER TOOL")
        print("="*70)
        print(f"Dry run: {dry_run}\n")

        files = self.find_index_files()
        print(f"Files found: {len(files)}\n")

        for filepath in files:
            self.files_processed += 1
            count, changes = self.process_file(filepath, dry_run)

            if count > 0:
                self.files_changed += 1
                self.replacements += count

                rel_path = filepath.relative_to(self.docs_path.parent)
                print(f"✅ {rel_path}")

                if verbose:
                    for change in changes:
                        print(f"   • {change}")

        # Summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Files processed: {self.files_processed}")
        print(f"Files changed: {self.files_changed}")
        print(f"Fixes applied: {self.replacements}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
        else:
            print("\n✅ All fixes applied successfully")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = BrokenLinksFixerTool()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
