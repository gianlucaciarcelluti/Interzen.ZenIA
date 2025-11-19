#!/usr/bin/env python3
"""
Script per sostituire TUTTI i riferimenti a zendata con zenia.

Sostituisce:
- zendata.local → zenia.local (domini)
- zendata-network → zenia-network (network docker-compose)
- @zendata.local → @zenia.local (email)
- #zendata- → #zenia- (slack channels)
- -n zendata → -n zenia (kubernetes namespace)
- Namespace: zendata → Namespace: zenia

Preserva:
- zendata/ (docker image registry)

Uso:
    python3 replace_all_zendata.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class CompleteZeniaRenamingTool:
    def __init__(self):
        self.docs_path = Path(__file__).parent.parent / 'docs'
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0
        self.changes_log = []

        # Pattern di sostituzione (in ordine specifico per evitare conflitti)
        self.patterns = [
            # Domini email
            (r'@zendata\.local', '@zenia.local', 'Email domain'),
            # Domini locali
            (r'zendata\.local', 'zenia.local', 'Local domain'),
            # Network docker-compose
            (r'zendata-network', 'zenia-network', 'Docker network'),
            # Slack channels
            (r'#zendata-', '#zenia-', 'Slack channel'),
            # Kubernetes namespace in comandi
            (r'-n zendata(?=\s|$)', '-n zenia', 'K8s namespace flag'),
            # Namespace: zendata in YAML/markdown
            (r'Namespace: zendata(?=\n|\s|$)', 'Namespace: zenia', 'K8s Namespace value'),
        ]

    def find_all_docs_files(self) -> List[Path]:
        """Trova tutti i file docs che potrebbero contenere zendata"""
        files = []

        # File types to check
        extensions = ['.md', '.yml', '.yaml', '.sql', '.json']

        for ext in extensions:
            files.extend(self.docs_path.glob(f'**/*{ext}'))

        return sorted(files)

    def process_file(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """
        Elabora un file sostituendo tutti i pattern zendata con zenia.
        Restituisce (numero_replacements, lista_righe_cambiate)
        """
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            # Applica tutti i pattern
            for pattern, replacement, description in self.patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    # Calcola numero di riga
                    line_num = content[:match.start()].count('\n') + 1
                    old_text = match.group(0)
                    changes.append(f"  Line {line_num}: {description} - '{old_text}' → '{replacement}'")

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
        print("COMPLETE ZENDATA → ZENIA REPLACEMENT TOOL")
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

    tool = CompleteZeniaRenamingTool()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
