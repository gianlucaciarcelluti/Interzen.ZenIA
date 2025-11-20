#!/usr/bin/env python3
"""
Script per riparare i link rotti creati dalle ridenominazioni dei file UC.

Problemi risolti:
1. Link a "01 SP##" rinominati a "SP##"
2. Link a "00 Architettura UC#" rinominati a "00-ARCHITETTURA.md"
3. Link a file SUPPLEMENTARY rinominati
4. Link a "01 Sequence..." rinominati a "03-SEQUENCES.md"

Uso:
    python3 fix_broken_links_post_rename.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class BrokenLinksFixer:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.docs_path = self.repo_root / 'docs'
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0

    def find_all_md_files(self) -> List[Path]:
        """Trova tutti i file markdown."""
        return sorted(self.docs_path.rglob("*.md")) + [self.repo_root / "README.md"]

    def fix_sp_links(self, content: str, file_path: Path) -> Tuple[str, int]:
        """
        Ripara link a file SP rinominati da "01 SP##" a "SP##".
        Esempio: ./01 SP05 - Motore Template.md → ./SP05 - Motore Template.md
        """
        original = content

        # Pattern per link locali: ./01 SP## - ...
        content = re.sub(
            r'(\[.+?\]\(\./)01 (SP\d+\s*[-–].+?\.md)',
            r'\1\2',
            content
        )

        # Pattern per link relativi: ../UC# - .../01 SP##
        content = re.sub(
            r'((\.\./)+[^/\]]+/?)01 (SP\d+\s*[-–].+?\.md)',
            r'\1\3',
            content
        )

        # Link senza ./ prefix: 01 SP##
        content = re.sub(
            r'\(01 (SP\d+\s*[-–].+?\.md)\)',
            r'(\1)',
            content
        )

        return content, len(re.findall(r'01 SP\d+', original))

    def fix_architecture_links(self, content: str) -> Tuple[str, int]:
        """
        Ripara link a file architettura rinominati da "00 Architettura UC#" a "00-ARCHITETTURA.md".
        """
        original = content

        # Pattern: ./00 Architettura UC#.md → ./00-ARCHITETTURA.md
        content = re.sub(
            r'(\[.+?\]\(\./)00 Architettura UC(\d+)\.md',
            r'\100-ARCHITETTURA.md',
            content
        )

        return content, len(re.findall(r'00 Architettura UC\d+', original))

    def fix_sequence_links(self, content: str) -> Tuple[str, int]:
        """
        Ripara link a file sequenza rinominati da "01 Sequence..." a "03-SEQUENCES...".
        """
        original = content

        # Pattern 1: ./01 Sequence - Document Processing Completo.md → ./03-SEQUENCES.md
        content = re.sub(
            r'(\[.+?\]\(\./)01 Sequence\s*[-–]\s*Document Processing Completo\.md',
            r'\103-SEQUENCES.md',
            content
        )

        # Pattern 2: ./01 Sequence - Overview Semplificato.md → ./03-SEQUENCES-SIMPLIFIED.md
        content = re.sub(
            r'(\[.+?\]\(\./)01 Sequence\s*[-–]\s*Overview Semplificato\.md',
            r'\103-SEQUENCES-SIMPLIFIED.md',
            content
        )

        # Pattern 3: ./01 Sequence - Ultra Semplificato.md → ./03-SEQUENCES-ULTRA-SIMPLIFIED.md
        content = re.sub(
            r'(\[.+?\]\(\./)01 Sequence\s*[-–]\s*Ultra Semplificato\.md',
            r'\103-SEQUENCES-ULTRA-SIMPLIFIED.md',
            content
        )

        # Pattern 4: ./01 Sequence diagrams.md → ./03-SEQUENCES.md
        content = re.sub(
            r'(\[.+?\]\(\./)01 Sequence\s+diagrams\.md',
            r'\103-SEQUENCES.md',
            content
        )

        return content, len(re.findall(r'01 Sequence', original))

    def fix_supplementary_links(self, content: str) -> Tuple[str, int]:
        """
        Ripara link a file SUPPLEMENTARY rinominati da "01 CANONICAL..." a "CANONICAL-Complete-Flow.md" ecc.
        """
        original = content

        # Pattern 1: 01 CANONICAL - Generazione Atto Completo.md → CANONICAL-Complete-Flow.md
        content = re.sub(
            r'01 CANONICAL\s*[-–]\s*Generazione Atto Completo\.md',
            r'CANONICAL-Complete-Flow.md',
            content
        )

        # Pattern 2: 02 SUPPLEMENTARY - Overview Semplificato.md → OVERVIEW-Simplified.md
        content = re.sub(
            r'02 SUPPLEMENTARY\s*[-–]\s*Overview Semplificato\.md',
            r'OVERVIEW-Simplified.md',
            content
        )

        # Pattern 3: 03 SUPPLEMENTARY - Ultra Semplificato.md → OVERVIEW-Ultra-Simplified.md
        content = re.sub(
            r'03 SUPPLEMENTARY\s*[-–]\s*Ultra Semplificato\.md',
            r'OVERVIEW-Ultra-Simplified.md',
            content
        )

        return content, len(re.findall(r'(01 CANONICAL|02 SUPPLEMENTARY|03 SUPPLEMENTARY)', original))

    def fix_dependencies_links(self, content: str) -> Tuple[str, int]:
        """
        Ripara link a file dipendenze rinominati da "02 Matrice Dipendenze" a "02-DIPENDENZE.md".
        """
        original = content

        # Pattern: ./00 Architettura UC#.md → ./00-ARCHITETTURA.md
        content = re.sub(
            r'(\[.+?\]\(\./)02 Matrice Dipendenze[^.]*\.md',
            r'\102-DIPENDENZE.md',
            content
        )

        # Pattern con path relativi
        content = re.sub(
            r'(\./)02 Matrice Dipendenze[^.]*\.md',
            r'\102-DIPENDENZE.md',
            content
        )

        return content, len(re.findall(r'02 Matrice Dipendenze', original))

    def process_file(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """Processa un file e risolve i link rotti."""
        changes = []

        try:
            content = filepath.read_text(encoding='utf-8')
            original_content = content

            # Applica tutte le correzioni
            content, count1 = self.fix_sp_links(content, filepath)
            if count1 > 0:
                changes.append(f"Fixed {count1} SP file references")

            content, count2 = self.fix_architecture_links(content)
            if count2 > 0:
                changes.append(f"Fixed {count2} Architecture file references")

            content, count3 = self.fix_sequence_links(content)
            if count3 > 0:
                changes.append(f"Fixed {count3} Sequence file references")

            content, count4 = self.fix_supplementary_links(content)
            if count4 > 0:
                changes.append(f"Fixed {count4} Supplementary file references")

            content, count5 = self.fix_dependencies_links(content)
            if count5 > 0:
                changes.append(f"Fixed {count5} Dependencies file references")

            # Se ci sono stati cambiamenti
            if content != original_content:
                if not dry_run:
                    filepath.write_text(content, encoding='utf-8')
                return len(changes), changes

            return 0, []

        except Exception as e:
            return 0, [f"Error: {e}"]

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui la riparazione."""

        print("\n" + "="*70)
        print("BROKEN LINKS FIXER (Post-Rename)")
        print("="*70)
        print(f"Dry run: {dry_run}\n")

        files = self.find_all_md_files()
        print(f"Processing {len(files)} markdown files...\n")

        for filepath in files:
            self.files_processed += 1
            count, changes = self.process_file(filepath, dry_run)

            if count > 0:
                self.files_changed += 1
                self.replacements += count

                try:
                    rel_path = filepath.relative_to(self.repo_root)
                except:
                    rel_path = filepath.name

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
        print(f"Link fixes applied: {self.replacements}")

        if dry_run:
            print("\n⚠️  DRY RUN MODE - No files were modified")
        else:
            print("\n✅ All link fixes applied successfully")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    fixer = BrokenLinksFixer()
    fixer.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
