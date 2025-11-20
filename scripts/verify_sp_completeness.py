#!/usr/bin/env python3
"""
Verifica completamento e mappatura SP.

Assicura che:
- Tutti i 71 SP (escluso 28) siano presenti
- Nessun SP sia duplicato (presente in più UC)
- Mapping SP -> UC sia corretto
- File SP abbiano formato standardizzato
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# SP attesi: SP01-SP72 escluso SP28
EXPECTED_SP = set(range(1, 73)) - {28}

# Mappatura attesa SP -> UC (basata su numerazione)
UC_RANGES = {
    (1, 11): "UC5",      # SP01-SP11: UC5
    (12, 15): "UC1",     # SP12-SP15: UC1
    (16, 19): "UC2",     # SP16-SP19: UC2
    (20, 23): "UC3",     # SP20-SP23: UC3
    (24, 27): "UC4",     # SP24-SP27: UC4
    (29, 37): "UC6",     # SP29-SP37: UC6
    (38, 41): "UC8",     # SP38-SP41: UC8
    (42, 50): "UC9",     # SP42-SP50: UC9
    (51, 57): "UC10",    # SP51-SP57: UC10
    (58, 72): "UC11",    # SP58-SP72: UC11 (escluso 28 che è in (24,27) but reserved)
}

class SPValidator:
    def __init__(self):
        self.sp_files = {}       # SP -> list di file path
        self.sp_uc_mapping = {}  # SP -> UC atteso
        self.errors = []
        self.warnings = []
        self.sp_found = set()

    def get_expected_uc(self, sp_num: int) -> str:
        """Ottieni UC atteso per SP."""
        for (start, end), uc in UC_RANGES.items():
            if start <= sp_num <= end and sp_num != 28:
                return uc
        return "UNKNOWN"

    def discover_sp_files(self):
        """Scopri tutti i file SP."""
        print("🔍 Scoprendo file SP...")

        for uc_folder in (DOCS_DIR / "use_cases").iterdir():
            if not uc_folder.is_dir() or not uc_folder.name.startswith("UC"):
                continue

            uc_name = uc_folder.name.split(" - ")[0]  # Estrai "UC#"

            for file_path in uc_folder.rglob("SP*.md"):
                # Estrai numero SP dal nome file
                match = re.search(r'SP(\d{2,3})', file_path.name)
                if match:
                    sp_num = int(match.group(1))
                    self.sp_found.add(sp_num)

                    if sp_num not in self.sp_files:
                        self.sp_files[sp_num] = []

                    self.sp_files[sp_num].append({
                        "path": str(file_path.relative_to(DOCS_DIR)),
                        "uc": uc_name,
                        "filename": file_path.name
                    })

        print(f"✅ Trovati {len(self.sp_found)} SP\n")

    def validate(self):
        """Valida completamento e mappatura SP."""
        print("✔️  Validando completamento e mappatura SP...")

        # 1. Controlla SP mancanti
        missing_sp = EXPECTED_SP - self.sp_found
        if missing_sp:
            sp_list = ", ".join([f"SP{n:02d}" for n in sorted(missing_sp)])
            self.errors.append(f"SP mancanti: {sp_list}")

        # 2. Controlla SP extra (non attesi)
        extra_sp = self.sp_found - EXPECTED_SP
        if extra_sp:
            sp_list = ", ".join([f"SP{n:02d}" for n in sorted(extra_sp)])
            self.warnings.append(f"SP non attesi: {sp_list}")

        # 3. Valida mappatura SP -> UC
        for sp_num, files in self.sp_files.items():
            expected_uc = self.get_expected_uc(sp_num)

            # SP28 è riservato, non deve avere file operativi
            if sp_num == 28:
                self.warnings.append(f"SP28: Trovato file (dovrebbe essere riservato)")
                continue

            # Controlla se il file è nel UC corretto
            for file_info in files:
                actual_uc = file_info["uc"]
                if actual_uc != expected_uc:
                    self.errors.append(
                        f"{file_info['filename']}: In UC {actual_uc}, atteso in {expected_uc}"
                    )

            # Controlla duplicati (stesso SP in più UC)
            if len(files) > 1:
                ucs = [f["uc"] for f in files]
                self.warnings.append(f"SP{sp_num:02d}: Duplicato in {len(files)} UC: {', '.join(ucs)}")

        # 4. Valida formato nome file
        for sp_num, files in self.sp_files.items():
            for file_info in files:
                filename = file_info["filename"]
                # Pattern atteso: SP## - Descrizione.md
                if not re.match(r'SP\d{2,3}\s*[-–]\s*.+\.md$', filename):
                    self.warnings.append(
                        f"SP{sp_num:02d}: Nome file non standard: {filename} (atteso: SP## - Descrizione.md)"
                    )

    def generate_report(self) -> Dict:
        """Genera report."""
        # Ordina SP per numero
        sorted_sp = {}
        for sp_num in sorted(self.sp_files.keys()):
            sorted_sp[f"SP{sp_num:02d}"] = {
                "number": sp_num,
                "expected_uc": self.get_expected_uc(sp_num),
                "actual_locations": self.sp_files[sp_num],
                "duplicated": len(self.sp_files[sp_num]) > 1
            }

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "expected_sp_count": len(EXPECTED_SP),
                "found_sp_count": len(self.sp_found),
                "missing_sp": list(sorted(EXPECTED_SP - self.sp_found)),
                "extra_sp": list(sorted(self.sp_found - EXPECTED_SP)),
                "duplicated_sp": len([s for s in self.sp_files.values() if len(s) > 1]),
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
            "sp_mapping": sorted_sp,
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA COMPLETAMENTO E MAPPATURA SP")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  SP attesi: {summary['expected_sp_count']}")
        print(f"  SP trovati: {summary['found_sp_count']}")
        print(f"  ❌ SP mancanti: {len(summary['missing_sp'])}")
        print(f"  ⚠️  SP extra: {len(summary['extra_sp'])}")
        print(f"  ⚠️  SP duplicati: {summary['duplicated_sp']}")
        print(f"  ❌ Errori: {summary['errors']}")
        print(f"  ⚠️  Warnings: {summary['warnings']}\n")

        if summary['missing_sp']:
            print(f"❌ MANCANTI ({len(summary['missing_sp'])}):")
            sp_list = ", ".join([f"SP{n:02d}" for n in summary['missing_sp']])
            print(f"   {sp_list}\n")

        if summary['extra_sp']:
            print(f"⚠️  EXTRA ({len(summary['extra_sp'])}):")
            sp_list = ", ".join([f"SP{n:02d}" for n in summary['extra_sp']])
            print(f"   {sp_list}\n")

        if report["errors"]:
            print("="*70)
            print("❌ ERRORI:")
            for error in report["errors"][:10]:
                print(f"  • {error}")
            if len(report["errors"]) > 10:
                print(f"  ... e altri {len(report['errors']) - 10} errori")

        if report["warnings"]:
            print("\n" + "="*70)
            print("⚠️  WARNINGS:")
            for warning in report["warnings"][:10]:
                print(f"  • {warning}")
            if len(report["warnings"]) > 10:
                print(f"  ... e altri {len(report['warnings']) - 10} warnings")

        # Score finale
        print("\n" + "="*70)
        completeness = (summary['found_sp_count'] / summary['expected_sp_count'] * 100) if summary['expected_sp_count'] > 0 else 0
        print(f"Completeness: {completeness:.1f}% ({summary['found_sp_count']}/{summary['expected_sp_count']})")

        if summary['errors'] == 0 and summary['extra_sp'] == 0 and summary['duplicated_sp'] == 0:
            print("✅ SP COMPLETENESS: PERFECT")
            return 0
        elif summary['missing_sp'] == 0 and summary['errors'] == 0:
            print("⚠️  SP COMPLETENESS: GOOD (some duplicates/extra)")
            return 0
        else:
            print("❌ SP COMPLETENESS: NEEDS WORK")
            return 1

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "sp_completeness_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = SPValidator()
    validator.discover_sp_files()
    validator.validate()
    report = validator.generate_report()
    validator.print_report(report)
    validator.save_report(report)
    exit_code = 0 if not validator.errors else 1
    exit(exit_code)


if __name__ == '__main__':
    main()
