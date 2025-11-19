#!/usr/bin/env python3
"""
Verifica validità e completezza payload JSON nella documentazione ZenIA.

Funzionalità:
- Estrae blocchi ```json dai file MD
- Valida sintassi JSON
- Verifica campi obbligatori (quando documentati)
- Identifica payload incompleti o malformati
- Output: report JSON con errori
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Pattern per trovare blocchi JSON in markdown
JSON_BLOCK_PATTERN = re.compile(
    r'```json\n(.*?)\n```',
    re.DOTALL
)

# Campi standard attesi nei payload (per diversi tipi)
REQUIRED_FIELDS = {
    'request': ['request_id', 'timestamp'],  # Opzionali ma consigliati
    'response': ['status', 'data'],           # Opzionali ma consigliati
}

# File da escludere dalla validazione JSON (template, esempi didattici, etc.)
EXCLUDE_FILES = {
    'templates/json-payload-standard.md',  # Template con placeholder comments
    'PIANO-REFACTORING-DOCUMENTAZIONE.md',  # Piano con frammenti esempi
    'VALUTAZIONE-QUALITA-DOCUMENTAZIONE.md',  # Rapporto con esempi frammenti
    'PIANO-AZIONE-AGGIORNATO-NOVEMBRE-2025.md',  # Piano con frammenti
}


class JSONValidator:
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.json_blocks = []
        self.valid_count = 0
        self.invalid_count = 0
        self.warnings = []
        self.errors = []

    def scan_files(self):
        """Scansiona tutti file MD per blocchi JSON."""
        print("🔍 Scansionando file JSON...")

        for file_path in self.docs_dir.rglob("*.md"):
            try:
                relative_path = file_path.relative_to(self.docs_dir)

                # Salta file esclusi
                if str(relative_path) in EXCLUDE_FILES:
                    continue

                content = file_path.read_text(encoding='utf-8')

                # Trova blocchi JSON
                for match in JSON_BLOCK_PATTERN.finditer(content):
                    json_str = match.group(1).strip()
                    self.json_blocks.append({
                        'file': str(relative_path),
                        'content': json_str,
                        'line': content[:match.start()].count('\n') + 1
                    })

            except Exception as e:
                self.errors.append(f"Errore lettura {relative_path}: {e}")

        print(f"✅ Trovati {len(self.json_blocks)} blocchi JSON")

    def validate_blocks(self):
        """Valida ogni blocco JSON."""
        print("✔️  Validando JSON...")

        for block in self.json_blocks:
            file_path = block['file']
            json_str = block['content']
            line = block['line']

            try:
                # Valida sintassi JSON
                data = json.loads(json_str)
                self.valid_count += 1

                # Controlla completezza (warnings, non errori)
                if isinstance(data, dict):
                    if not data:  # JSON vuoto
                        self.warnings.append(
                            f"{file_path}:{line} - JSON vuoto: {{}}"
                        )
                    elif 'request' in file_path.lower() and not any(k in data for k in ['data', 'payload', 'content']):
                        self.warnings.append(
                            f"{file_path}:{line} - Request senza payload data"
                        )

            except json.JSONDecodeError as e:
                self.invalid_count += 1
                error_msg = str(e).split('\n')[0]  # Prima riga solo
                self.errors.append(
                    f"{file_path}:{line} - Errore JSON: {error_msg}"
                )
            except Exception as e:
                self.invalid_count += 1
                self.errors.append(
                    f"{file_path}:{line} - Errore: {e}"
                )

    def generate_report(self) -> Dict:
        """Genera report."""
        report = {
            "summary": {
                "total_blocks": len(self.json_blocks),
                "valid": self.valid_count,
                "invalid": self.invalid_count,
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("REPORT VERIFICA JSON")
        print("="*70)

        summary = report['summary']
        print(f"\n📊 RIEPILOGO:")
        print(f"  Blocchi JSON trovati: {summary['total_blocks']}")
        print(f"  ✅ Validi: {summary['valid']}")
        print(f"  ❌ Invalidi: {summary['invalid']}")
        print(f"  ⚠️  Warnings: {summary['warnings']}")

        if report['errors']:
            print(f"\n❌ ERRORI JSON ({len(report['errors'])}):")
            for error in report['errors'][:10]:  # Mostra primi 10
                print(f"  • {error}")
            if len(report['errors']) > 10:
                print(f"  ... e {len(report['errors']) - 10} altri errori")

        if report['warnings']:
            print(f"\n⚠️  WARNINGS ({len(report['warnings'])}):")
            for warning in report['warnings'][:10]:
                print(f"  • {warning}")
            if len(report['warnings']) > 10:
                print(f"  ... e {len(report['warnings']) - 10} altri warnings")

        if not report['errors']:
            print("\n✅ TUTTI I JSON SONO VALIDI!")

        print("\n" + "="*70)

    def save_report(self, report: Dict):
        """Salva report."""
        report_file = REPORTS_DIR / "json_validation.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📁 Report salvato: {report_file}")


def main():
    validator = JSONValidator(DOCS_DIR)
    validator.scan_files()
    validator.validate_blocks()

    report = validator.generate_report()
    validator.print_report(report)
    validator.save_report(report)

    return 0 if not report['errors'] else 1


if __name__ == "__main__":
    exit(main())
