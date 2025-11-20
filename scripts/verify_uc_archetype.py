#!/usr/bin/env python3
"""
Verifica completamento archetipo UC.

Assicura che ogni UC abbia la struttura standardizzata:
- 00-ARCHITECTURE.md (opzionale per alcuni UC)
- 01-OVERVIEW.md
- 02-DEPENDENCIES.md
- 03-SEQUENCES.md (oppure varianti -SIMPLIFIED, -ULTRA-SIMPLIFIED)
- 04-GUIDE.md (opzionale)
- 05-HITL.md (solo UC5)
- README.md
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Standard archetype per ogni UC
REQUIRED_FILES = {
    "README.md",           # Obbligatorio per tutti
    "01-OVERVIEW.md",      # Obbligatorio
    "02-DEPENDENCIES.md",  # Obbligatorio
}

OPTIONAL_FILES = {
    "00-ARCHITECTURE.md",           # Molto comune
    "03-SEQUENCES.md",              # Sequence diagram canonical
    "03-SEQUENCES-SIMPLIFIED.md",   # Sequence diagram simplified
    "03-SEQUENCES-ULTRA-SIMPLIFIED.md",  # Sequence diagram ultra-simplified
    "04-GUIDE.md",                  # Guide operativa
    "05-HITL.md",                   # Human-in-the-loop (UC5 only)
}

# UC5 ha speciale struttura SUPPLEMENTARY
UC5_SUPPLEMENTARY_FILES = {
    "SUPPLEMENTARY/CANONICAL-Complete-Flow.md",
    "SUPPLEMENTARY/OVERVIEW-Simplified.md",
    "SUPPLEMENTARY/OVERVIEW-Ultra-Simplified.md",
}

class ArchetypeValidator:
    def __init__(self):
        self.uc_folders = []
        self.results = {}
        self.errors = []
        self.warnings = []
        self.completeness_score = 0.0

    def discover_uc_folders(self) -> List[Path]:
        """Scopri cartelle UC."""
        uc_folders = []
        for item in sorted((DOCS_DIR / "use_cases").iterdir()):
            if item.is_dir() and item.name.startswith("UC"):
                uc_folders.append(item)
        return uc_folders

    def check_uc_structure(self, uc_path: Path) -> Dict:
        """Controlla struttura UC."""
        uc_name = uc_path.name
        result = {
            "name": uc_name,
            "path": str(uc_path.relative_to(DOCS_DIR)),
            "required_found": [],
            "required_missing": [],
            "optional_found": [],
            "optional_missing": [],
            "supplementary_found": [],
            "extra_files": [],
            "completeness": 0.0
        }

        # Trova file presenti
        present_files = set(f.name for f in uc_path.glob("*.md") if f.is_file())
        present_files_supplementary = set()

        # Check SUPPLEMENTARY folder (UC5)
        supplementary_path = uc_path / "SUPPLEMENTARY"
        if supplementary_path.exists():
            for f in supplementary_path.glob("*.md"):
                relative = f"SUPPLEMENTARY/{f.name}"
                present_files_supplementary.add(relative)

        # Valida file obbligatori
        for required in REQUIRED_FILES:
            if required in present_files:
                result["required_found"].append(required)
            else:
                result["required_missing"].append(required)
                self.errors.append(f"{uc_name}: File obbligatorio mancante: {required}")

        # Valida file opzionali
        for optional in OPTIONAL_FILES:
            if optional in present_files:
                result["optional_found"].append(optional)
            else:
                result["optional_missing"].append(optional)

        # Valida SUPPLEMENTARY (solo UC5)
        if "UC5" in uc_name:
            for supp_file in UC5_SUPPLEMENTARY_FILES:
                if supp_file in present_files_supplementary:
                    result["supplementary_found"].append(supp_file)
                else:
                    result["optional_missing"].append(supp_file)

        # File extra (non riconosciuti)
        all_expected = REQUIRED_FILES | OPTIONAL_FILES
        for f in present_files:
            if f not in all_expected and not f.startswith("SP"):
                result["extra_files"].append(f)

        # Calcola completezza
        total_required = len(REQUIRED_FILES)
        found_required = len(result["required_found"])
        total_optional = len(OPTIONAL_FILES) + (len(UC5_SUPPLEMENTARY_FILES) if "UC5" in uc_name else 0)
        found_optional = len(result["optional_found"]) + len(result["supplementary_found"])

        required_score = (found_required / total_required * 100) if total_required > 0 else 0
        optional_score = (found_optional / total_optional * 100) if total_optional > 0 else 0

        result["completeness"] = (required_score * 0.7) + (optional_score * 0.3)

        return result

    def validate(self):
        """Valida tutti gli UC."""
        print("🔍 Scoprendo cartelle UC...")
        uc_folders = self.discover_uc_folders()
        print(f"✅ Trovati {len(uc_folders)} UC\n")
        print("✔️  Validando struttura UC...")

        for uc_path in uc_folders:
            result = self.check_uc_structure(uc_path)
            self.results[result["name"]] = result

        # Calcola score totale
        if self.results:
            avg_completeness = sum(r["completeness"] for r in self.results.values()) / len(self.results)
            self.completeness_score = avg_completeness

    def generate_report(self) -> Dict:
        """Genera report."""
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "total_uc": len(self.results),
                "completeness_score": round(self.completeness_score, 1),
                "errors": len(self.errors),
                "warnings": len(self.warnings),
            },
            "uc_details": self.results,
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA COMPLETAMENTO ARCHETIPO UC")
        print("="*70 + "\n")

        print("📊 RIEPILOGO:")
        print(f"  UC totali: {report['summary']['total_uc']}")
        print(f"  Completeness score: {report['summary']['completeness_score']:.1f}%")
        print(f"  ❌ Errori: {report['summary']['errors']}")
        print(f"  ⚠️  Warnings: {report['summary']['warnings']}\n")

        # Dettagli per UC
        print("📂 DETTAGLI UC:")
        for uc_name, details in report["uc_details"].items():
            status = "✅" if not details["required_missing"] else "❌"
            print(f"\n{status} {uc_name}")
            print(f"   Completeness: {details['completeness']:.1f}%")
            if details["required_found"]:
                print(f"   ✅ Obbligatori: {', '.join(details['required_found'][:3])}" +
                      (f" (+{len(details['required_found'])-3})" if len(details['required_found']) > 3 else ""))
            if details["required_missing"]:
                print(f"   ❌ Mancanti: {', '.join(details['required_missing'])}")
            if details["optional_found"]:
                print(f"   ℹ️  Opzionali trovati: {len(details['optional_found'])}")

        if report["errors"]:
            print("\n" + "="*70)
            print("❌ ERRORI:")
            for error in report["errors"]:
                print(f"  • {error}")

        if report["warnings"]:
            print("\n" + "="*70)
            print("⚠️  WARNINGS:")
            for warning in report["warnings"]:
                print(f"  • {warning}")

        # Score finale
        print("\n" + "="*70)
        if self.completeness_score >= 95:
            print("✅ ARCHETYPE COMPLETENESS: EXCELLENT")
            return 0
        elif self.completeness_score >= 80:
            print("⚠️  ARCHETYPE COMPLETENESS: GOOD (can improve)")
            return 0
        else:
            print("❌ ARCHETYPE COMPLETENESS: NEEDS WORK")
            return 1

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "uc_archetype_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = ArchetypeValidator()
    validator.validate()
    report = validator.generate_report()
    validator.print_report(report)
    validator.save_report(report)
    exit_code = 0 if not validator.errors else 1
    exit(exit_code)


if __name__ == '__main__':
    main()
