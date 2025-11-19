#!/usr/bin/env python3
"""
Script per standardizzare la terminologia nella sezione Conformità Normativa.

Sostituisce termini in inglese con versioni italiane coerenti con GLOSSARIO-TERMINOLOGICO.md
"""

import sys
import re
from pathlib import Path

class ConformitaTerminologyFixer:
    def __init__(self):
        self.root_path = Path(__file__).parent.parent
        self.docs_path = self.root_path / 'docs'

        # Mapping terminologia da inglese a italiano per sezione Conformità
        self.terminology_fixes = {
            # Framework/standards - context: Conformità section
            'Framework applicabili': 'Framework applicabili',  # Keep (acronyms accepted per GLOSSARIO)
            'Applicability': 'Applicabilità',
            'Personal Data': 'Dati personali',
            'Personal data': 'dati personali',
            'Data Subject': 'Interessato',
            'Data subject': 'interessato',
            'Security Measures': 'Misure di Sicurezza',
            'Technical measures': 'Misure tecniche',
            'Organizational measures': 'Misure organizzative',
            'Data Processing': 'Elaborazione Dati',
            'Data processing': 'elaborazione dati',
            'Data Protection Officer': 'Responsabile della Protezione dei Dati (DPO)',
            'DPO': 'DPO',  # Keep acronym
            'Competent Authority': 'Autorità Competente',
            'RACI Matrix': 'Matrice RACI',
            'Key Performance Indicator': 'Indicatore Prestazioni Chiave',
            'Performance Monitoring': 'Monitoraggio Prestazioni',
            'Compliance Review': 'Revisione Conformità',
            'Audit Trail': 'Registro di Audit',
            'Data Retention': 'Conservazione Dati',
            'Data Minimization': 'Minimizzazione Dati',
            'Privacy by Design': 'Privacy by Design',  # Accept per standard internazionale
            'HITL Checkpoint': 'Checkpoint HITL',
            'Trusted Service Provider': 'Provider di Servizi Fiduciari',
            'Certificate Chain': 'Catena di Certificati',
            'Timestamp Authority': 'Autorità di Marca Temporale',
            'Revocation Status': 'Stato Revoca',
            'Access Control': 'Controllo Accesso',
            'Encryption': 'Crittografia',
            'Legal Basis': 'Base Legale',
            'Lawfulness': 'Liceità',
            'Accountability': 'Responsabilità',
            'Transparency': 'Trasparenza',
            'Next Review': 'Prossima Review',
            'Review Period': 'Periodo di Revisione',
            'Escalation Path': 'Percorso di Escalation',
            'Responsible': 'Responsabile',
            'Accountable': 'Responsabile (Accountable)',
            'Consulted': 'Consultato',
            'Informed': 'Informato',
        }

        self.files_processed = 0
        self.files_updated = 0

    def fix_file(self, filepath: Path, dry_run: bool = False) -> bool:
        """Applica correzioni terminologiche a un file."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ❌ Error reading {filepath.name}: {e}")
            return False

        original_content = content

        # Apply terminology replacements
        for english_term, italian_term in self.terminology_fixes.items():
            # Case-sensitive replacement
            content = content.replace(english_term, italian_term)

        # Check if changes were made
        if content == original_content:
            return False

        # Write file if not dry-run
        if not dry_run:
            filepath.write_text(content, encoding='utf-8')

        return True

    def run(self, dry_run: bool = False, verbose: bool = False) -> bool:
        """Esegui correzioni terminologiche su tutti gli SP file."""

        print("\n" + "="*80)
        print("CONFORMITÀ TERMINOLOGIA FIXER")
        print("="*80)
        print(f"Dry run: {dry_run}\n")

        # Find all SP files with Conformità sections
        files = list(self.docs_path.rglob('01 SP*.md'))
        print(f"Found {len(files)} SP files\n")

        for filepath in sorted(files):
            self.files_processed += 1
            if self.fix_file(filepath, dry_run):
                self.files_updated += 1
                if verbose or not dry_run:
                    print(f"✅ Fixed: {filepath.parent.name}/")
                    print(f"   {filepath.name}")

        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Files processed: {self.files_processed}")
        print(f"Files updated: {self.files_updated}")

        if dry_run:
            print(f"\n⚠️  DRY RUN MODE - No files were modified")
            print(f"   Run without --dry-run to apply changes")
        else:
            print(f"\n✅ Terminology standardized in {self.files_updated} files")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = ConformitaTerminologyFixer()
    tool.run(dry_run=dry_run, verbose=verbose)


if __name__ == '__main__':
    main()
