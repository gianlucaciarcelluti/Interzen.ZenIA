#!/usr/bin/env python3
"""
Script per sostituire il registro docker da zendata/ a zenia/.

Sostituisce:
- zendata/ms01-classifier → zenia/ms01-classifier
- zendata/ms02-analyzer → zenia/ms02-analyzer
- zendata/* → zenia/*

Uso:
    python3 replace_docker_registry.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class DockerRegistryRenamingTool:
    def __init__(self):
        self.docs_path = Path(__file__).parent.parent / 'docs'
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0
        self.changes_log = []

    def find_all_docs_files(self) -> List[Path]:
        """Trova tutti i file docs che potrebbero contenere zendata/"""
        files = []

        # File types to check
        extensions = ['.md', '.yml', '.yaml', '.json']

        for ext in extensions:
            files.extend(self.docs_path.glob(f'**/*{ext}'))

        return sorted(files)

    def process_file(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """
        Elabora un file sostituendo zendata/ con zenia/.
        Restituisce (numero_replacements, lista_righe_cambiate)
        """
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            # Pattern per docker registry
            pattern = r'zendata/'
            replacement = 'zenia/'

            matches = list(re.finditer(pattern, content))
            for match in matches:
                # Calcola numero di riga
                line_num = content[:match.start()].count('\n') + 1
                old_text = match.group(0)
                changes.append(f"  Line {line_num}: Docker registry - '{old_text}' → '{replacement}'")

            # Applica sostituzione
            content = re.sub(pattern, replacement, content)

            # Se ci sono stati cambiamenti
            if content != original_content:
                if not dry_run:
                    filepath.write_text(content, encoding='utf-8')

                return len(changes), changes

            return 0, []

        except Exception as e:
            self.changes_log.append(f"  ❌ Errore processing {filepath.name}: {e}")
            return 0, []

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui tutte le sostituzioni"""

        print("\n" + "="*70)
        print("DOCKER REGISTRY ZENDATA → ZENIA REPLACEMENT TOOL")
        print("="*70)
        print(f"\nDocs path: {self.docs_path}")
        print(f"Dry run: {dry_run}")

        files = self.find_all_docs_files()
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
                        print(change)
                else:
                    print(f"   {count} replacement(s)")

        # Print summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Files processed: {self.files_processed}")
        print(f"Files changed: {self.files_changed}")
        print(f"Total replacements: {self.replacements}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
            print("   Run without --dry-run to apply changes")
        else:
            print("\n✅ All changes applied successfully")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = DockerRegistryRenamingTool()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
