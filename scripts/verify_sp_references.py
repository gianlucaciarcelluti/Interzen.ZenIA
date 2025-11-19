#!/usr/bin/env python3
"""
Verifica riferimenti SP/MS nella documentazione ZenIA.

Funzionalità:
- Scansiona tutti file MD per riferimenti SP## e MS##
- Verifica esistenza file SP/MS referenziati
- Identifica SP/MS orfani (non referenziati)
- Identifica riferimenti non validi
- Output: report JSON con errori e warnings
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Patterns per trovare riferimenti
SP_PATTERN = re.compile(r'\bSP(\d{2,3})\b')  # SP02, SP072
MS_PATTERN = re.compile(r'\bMS(\d{2})\b')   # MS01, MS16
UC_PATTERN = re.compile(r'\bUC(\d{1,2})\b')  # UC1, UC11

# SP/MS attesi
EXPECTED_SP = set(range(1, 73)) - {28}  # SP01-SP72 escluso SP28
EXPECTED_MS = set(range(1, 17))         # MS01-MS16
EXPECTED_UC = set(range(1, 12))         # UC1-UC11

# SP speciali (accettati in contesti specifici)
LEGACY_SP = {0}  # SP00: Historical/deprecated, solo in file DEPRECATED
RESERVED_SP = {28}  # SP28: Reserved, accettato solo in SP28-RESERVED.md

# File di documentazione che possono referenziare SP speciali
DOCUMENTATION_FILES = {
    'PIANO-REFACTORING-DOCUMENTAZIONE.md',  # Documenta uso futuro SP28
    'VALIDATION-CHECKLIST.md',  # Documenta gap SP00 risolto
    'GAP-RESOLUTION.md',  # Documenta gap storage
    'QUICK-REFERENCE-ARCHITECTURE.md',  # Panoramica architettura
    'SP-MS-MAPPING-MASTER.md',  # Master mapping per SP28 reserved
    'ARCHITECTURE-OVERVIEW.md',  # Overview architettura
    'GLOSSARIO.md',  # Glossario terminologico con riferimenti storici SP00
    'CANONICAL',  # Canonical docs che referenziano file deprecated
    '01 CANONICAL',  # Canonical diagrams che referenziano deprecated
    'SUPPLEMENTARY',  # Supplementary docs che referenziano deprecated
    '00 SP28-RESERVED.md',  # File che documenta SP28 reserved
    'SP28-RESERVED',  # File che documenta SP28 reserved
}


class ReferenceValidator:
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.found_sp = defaultdict(list)  # SP -> lista file che lo referenziano
        self.found_ms = defaultdict(list)  # MS -> lista file che lo referenziano
        self.found_uc = defaultdict(list)  # UC -> lista file che lo referenziano
        self.sp_files = {}                 # SP -> path file
        self.ms_files = {}                 # MS -> path file
        self.errors = []
        self.warnings = []

    def discover_files(self):
        """Scopri file SP e MS sul disco."""
        print("🔍 Scoprendo file SP/MS...")

        # Trova file SP
        for file_path in self.docs_dir.rglob("01 SP*.md"):
            match = re.search(r'SP(\d{2,3})', file_path.name)
            if match:
                sp_num = int(match.group(1))
                self.sp_files[sp_num] = file_path

        # Trova file MS
        for file_path in self.docs_dir.rglob("MS*/SPECIFICATION.md"):
            match = re.search(r'MS(\d{2})', file_path.parent.name)
            if match:
                ms_num = int(match.group(1))
                self.ms_files[ms_num] = file_path

        print(f"✅ Trovati {len(self.sp_files)} SP e {len(self.ms_files)} MS")

    def scan_references(self):
        """Scansiona tutti file MD per riferimenti."""
        print("🔎 Scansionando riferimenti...")

        for file_path in self.docs_dir.rglob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8')
                relative_path = file_path.relative_to(self.docs_dir)

                # Trova SP
                for match in SP_PATTERN.finditer(content):
                    sp_num = int(match.group(1))
                    self.found_sp[sp_num].append(str(relative_path))

                # Trova MS
                for match in MS_PATTERN.finditer(content):
                    ms_num = int(match.group(1))
                    self.found_ms[ms_num].append(str(relative_path))

                # Trova UC
                for match in UC_PATTERN.finditer(content):
                    uc_num = int(match.group(1))
                    self.found_uc[uc_num].append(str(relative_path))

            except Exception as e:
                self.errors.append(f"Errore lettura {relative_path}: {e}")

    def validate(self):
        """Valida riferimenti."""
        print("✔️  Validando riferimenti...")

        # Valida SP
        for sp_num in self.found_sp:
            # SP00: Legacy/deprecated
            if sp_num in LEGACY_SP:
                allowed_files = [f for f in self.found_sp[sp_num] if 'DEPRECATED' in f or any(doc in f for doc in DOCUMENTATION_FILES)]
                if len(allowed_files) == len(self.found_sp[sp_num]):
                    # OK: tutti i riferimenti sono in file autorizzati
                    pass
                else:
                    non_allowed = [f for f in self.found_sp[sp_num] if 'DEPRECATED' not in f and not any(doc in f for doc in DOCUMENTATION_FILES)]
                    if non_allowed:
                        self.warnings.append(f"SP00 (legacy): Trovato in file non-autorizzato: {non_allowed[0]}")

            # SP28: Reserved
            elif sp_num in RESERVED_SP:
                allowed_files = [f for f in self.found_sp[sp_num] if 'SP28-RESERVED' in f or any(doc in f for doc in DOCUMENTATION_FILES)]
                if len(allowed_files) == len(self.found_sp[sp_num]):
                    # OK: tutti i riferimenti sono in file autorizzati
                    pass
                else:
                    non_allowed = [f for f in self.found_sp[sp_num] if 'SP28-RESERVED' not in f and not any(doc in f for doc in DOCUMENTATION_FILES)]
                    if non_allowed:
                        self.warnings.append(f"SP28 (reserved): Trovato in file non-autorizzato: {non_allowed[0]}")

            # SP normali
            elif sp_num not in EXPECTED_SP:
                self.errors.append(f"SP{sp_num:02d}: Non è un SP valido (range 01-72, escluso 28)")

        # Valida MS
        for ms_num in self.found_ms:
            if ms_num not in EXPECTED_MS:
                self.errors.append(f"MS{ms_num:02d}: Non è un MS valido (range 01-16)")

        # Valida UC
        for uc_num in self.found_uc:
            if uc_num not in EXPECTED_UC:
                self.errors.append(f"UC{uc_num}: Non è un UC valido (range 1-11)")

        # Identifica SP non referenziati (orfani)
        unreferenced_sp = EXPECTED_SP - set(self.found_sp.keys())
        if unreferenced_sp:
            sp_list = ", ".join([f"SP{n:02d}" for n in sorted(unreferenced_sp)])
            self.warnings.append(f"SP non referenziati (orfani): {sp_list}")

        # Identifica MS non referenziati
        unreferenced_ms = EXPECTED_MS - set(self.found_ms.keys())
        if unreferenced_ms:
            ms_list = ", ".join([f"MS{n:02d}" for n in sorted(unreferenced_ms)])
            self.warnings.append(f"MS non referenziati (orfani): {ms_list}")

    def generate_report(self) -> Dict:
        """Genera report."""
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "total_sp_found": len(set(self.found_sp.keys())),
                "expected_sp": len(EXPECTED_SP),
                "total_ms_found": len(set(self.found_ms.keys())),
                "expected_ms": len(EXPECTED_MS),
                "total_uc_found": len(set(self.found_uc.keys())),
                "expected_uc": len(EXPECTED_UC),
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
            "sp_references": {
                f"SP{k:02d}": list(set(v))  # Deduplica file
                for k, v in sorted(self.found_sp.items())
            },
            "ms_references": {
                f"MS{k:02d}": list(set(v))
                for k, v in sorted(self.found_ms.items())
            },
            "uc_references": {
                f"UC{k}": list(set(v))
                for k, v in sorted(self.found_uc.items())
            },
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report in formato leggibile."""
        print("\n" + "="*70)
        print("REPORT VERIFICA SP/MS REFERENCES")
        print("="*70)

        summary = report['summary']
        print(f"\n📊 RIEPILOGO:")
        print(f"  SP trovati: {summary['total_sp_found']}/{summary['expected_sp']}")
        print(f"  MS trovati: {summary['total_ms_found']}/{summary['expected_ms']}")
        print(f"  UC trovati: {summary['total_uc_found']}/{summary['expected_uc']}")
        print(f"  ❌ Errori: {summary['errors']}")
        print(f"  ⚠️  Warnings: {summary['warnings']}")

        if report['errors']:
            print(f"\n❌ ERRORI ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"  • {error}")

        if report['warnings']:
            print(f"\n⚠️  WARNINGS ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"  • {warning}")

        if not report['errors'] and not report['warnings']:
            print("\n✅ NESSUN PROBLEMA TROVATO!")

        print("\n" + "="*70)

    def save_report(self, report: Dict):
        """Salva report in JSON."""
        report_file = REPORTS_DIR / "sp_ms_references.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📁 Report salvato: {report_file}")


def main():
    validator = ReferenceValidator(DOCS_DIR)
    validator.discover_files()
    validator.scan_references()
    validator.validate()

    report = validator.generate_report()
    validator.print_report(report)
    validator.save_report(report)

    # Exit code: 0 se OK, 1 se errori
    return 0 if not report['errors'] else 1


if __name__ == "__main__":
    exit(main())
