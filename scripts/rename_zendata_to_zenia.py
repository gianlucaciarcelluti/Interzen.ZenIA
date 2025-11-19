#!/usr/bin/env python3
"""
Script per rinominare tutti gli schemi database da zendata_ a zenia_.

Funzionamento:
1. Trova tutti i file DATABASE-SCHEMA.md e init-schema.sql
2. Sostituisce zendata_ con zenia_ in tutti i file
3. Crea un report dei cambimenti

Uso:
    python3 rename_zendata_to_zenia.py [--dry-run] [--verbose]
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

class ZeniaRenamingTool:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent / 'docs' / 'microservices'
        self.files_processed = 0
        self.files_changed = 0
        self.replacements = 0
        self.changes_log = []

    def find_schema_files(self) -> List[Path]:
        """Trova tutti i file che contengono zendata_"""
        files = []

        # Glob patterns per trovare file che potrebbero contenere zendata_
        patterns = [
            '*/DATABASE-SCHEMA.md',
            '*/init-schema.sql',
            '*/TROUBLESHOOTING.md',
            '*/docker-compose.yml',
            '*/kubernetes/*.yaml',
            '*/kubernetes/*.yml',
            'DEVELOPMENT-GUIDE.md',
            'DEPLOYMENT-GUIDE.md',
        ]

        for pattern in patterns:
            if pattern.startswith('*/'):
                # Pattern per microservices
                files.extend(self.base_path.glob(pattern))
            else:
                # Pattern per docs root
                root_files = (self.base_path.parent / pattern).glob('*') if '/' not in pattern else (self.base_path.parent).glob(pattern)
                files.extend(root_files)

        # Filtra solo file che contengono effettivamente zendata_
        result = []
        for f in files:
            if f.is_file():
                try:
                    content = f.read_text()
                    if 'zendata_' in content:
                        result.append(f)
                except:
                    pass

        return sorted(list(set(result)))  # Rimuovi duplicati

    def process_file(self, filepath: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
        """
        Elabora un file sostituendo zendata_ con zenia_.
        Restituisce (numero_replacements, lista_righe_cambiate)
        """
        changes = []

        try:
            # Leggi il file
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Conta e registra i cambimenti
            new_lines = []
            replacements_in_file = 0

            for line_no, line in enumerate(lines, 1):
                if 'zendata_' in line:
                    # Sostituisci zendata_ con zenia_
                    new_line = line.replace('zendata_', 'zenia_')

                    # Registra il cambimento
                    old_schema = re.findall(r'zendata_\w+', line)
                    new_schema = re.findall(r'zenia_\w+', new_line)

                    if old_schema and new_schema:
                        change_desc = f"Line {line_no}: {old_schema[0]} → {new_schema[0]}"
                        changes.append(change_desc)
                        replacements_in_file += 1

                    new_lines.append(new_line)
                else:
                    new_lines.append(line)

            # Se ci sono cambimenti e non è dry-run, scrivi il file
            if replacements_in_file > 0:
                if not dry_run:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    self.files_changed += 1

                self.replacements += replacements_in_file
                return replacements_in_file, changes
            else:
                return 0, []

        except Exception as e:
            print(f"❌ Errore elaborando {filepath.name}: {str(e)}")
            return 0, []

    def run(self, dry_run: bool = False, verbose: bool = False):
        """Esegue il processo di rinomina"""

        print("\n" + "="*70)
        print("🔄 RINOMINA DATABASE SCHEMA: zendata_ → zenia_")
        print("="*70)
        print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'}\n")

        # Trova i file
        files = self.find_schema_files()
        schema_files_with_zendata = [f for f in files if 'zendata_' in f.read_text()]

        if not schema_files_with_zendata:
            print("✅ Nessun file con 'zendata_' trovato!")
            return True

        print(f"File da processare: {len(schema_files_with_zendata)}\n")

        # Processa ogni file
        for filepath in schema_files_with_zendata:
            replacements, changes = self.process_file(filepath, dry_run=dry_run)

            self.files_processed += 1

            if replacements > 0:
                status = "✓ (DRY-RUN)" if dry_run else "✅"
                ms_name = filepath.parent.name
                file_name = filepath.name

                print(f"{status} {ms_name}/{file_name}")
                print(f"   └─ {replacements} replacements")

                if verbose and changes:
                    for change in changes[:3]:  # Mostra prime 3 righe
                        print(f"      • {change}")
                    if len(changes) > 3:
                        print(f"      • ... e {len(changes) - 3} altri")

                self.changes_log.extend(changes)

        # Summary
        print("\n" + "="*70)
        print("📊 RIEPILOGO")
        print("="*70)
        print(f"File processati: {self.files_processed}")
        print(f"File modificati: {self.files_changed if not dry_run else 'N/A (dry-run)'}")
        print(f"Replacements totali: {self.replacements}")

        if dry_run:
            print("\n⚠️  Modalità DRY-RUN: nessun file modificato.")
            print("Esegui senza --dry-run per applicare i cambimenti.")

        return True


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    tool = ZeniaRenamingTool()
    success = tool.run(dry_run=dry_run, verbose=verbose)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
