#!/usr/bin/env python3
"""
Verifica completamento sezioni obbligatorie SP.

Assicura che ogni file SP abbia:
- Overview / Descrizione
- Technical Details / Dettagli Tecnici
- Use Cases / Casi d'Uso
- Error Handling / Gestione Errori
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Sezioni obbligatorie per SP (case-insensitive pattern matching)
REQUIRED_SECTIONS = {
    "overview": [r"overview", r"overview.*?\(", r"panoramica", r"descrizione", r"summary"],
    "technical_details": [r"technical details", r"dettagli tecnici", r"architettura", r"architettura tecnica", r"implementazione", r"responsabilità"],
    "use_cases": [r"use cases", r"casi d'uso", r"scenari", r"examples?", r"esempi"],
    "error_handling": [r"error handling", r"gestione errori", r"error.*handling", r"exception", r"errori"],
}

class SectionValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.sp_files_checked = 0
        self.sp_files_complete = 0

    def extract_headings(self, content: str) -> List[str]:
        """Estrai tutti gli heading dal content."""
        pattern = r'^#+\s+(.+)$'
        headings = []
        for match in re.finditer(pattern, content, re.MULTILINE):
            headings.append(match.group(1).lower().strip())
        return headings

    def check_section_presence(self, headings: List[str], section_name: str, patterns: List[str]) -> bool:
        """Controlla se sezione è presente."""
        for heading in headings:
            for pattern in patterns:
                if re.search(pattern, heading, re.IGNORECASE):
                    return True
        return False

    def validate_sp_file(self, file_path: Path) -> Dict:
        """Valida SP file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "missing_sections": list(REQUIRED_SECTIONS.keys())}

        headings = self.extract_headings(content)
        missing_sections = []
        found_sections = []

        for section_name, patterns in REQUIRED_SECTIONS.items():
            if self.check_section_presence(headings, section_name, patterns):
                found_sections.append(section_name)
            else:
                missing_sections.append(section_name)
                self.errors.append(f"{file_path.name}: Sezione mancante - {section_name}")

        self.sp_files_checked += 1
        if not missing_sections:
            self.sp_files_complete += 1

        return {
            "file": str(file_path.relative_to(DOCS_DIR)),
            "valid": len(missing_sections) == 0,
            "found_sections": found_sections,
            "missing_sections": missing_sections,
            "all_headings": headings[:20],  # Store primi 20 heading per debug
        }

    def validate_all(self):
        """Valida tutti i file SP."""
        print("🔍 Scoprendo file SP...")

        sp_files = []
        # Solo SP file in use_cases/UC* directories
        use_cases_dir = DOCS_DIR / "use_cases"
        if use_cases_dir.exists():
            for uc_folder in use_cases_dir.iterdir():
                if uc_folder.is_dir() and uc_folder.name.startswith("UC"):
                    for file_path in uc_folder.glob("SP*.md"):
                        # Escludi file speciali
                        if "RESERVED" not in file_path.name:
                            sp_files.append(file_path)

        print(f"✅ Trovati {len(sp_files)} file SP\n")
        print("✔️  Validando sezioni obbligatorie...")

        results = []
        for file_path in sorted(sp_files):
            result = self.validate_sp_file(file_path)
            results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        files_with_issues = len([r for r in results if r["missing_sections"]])

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "sp_files_checked": self.sp_files_checked,
                "sp_files_complete": self.sp_files_complete,
                "files_with_missing_sections": files_with_issues,
                "completeness_rate": round((self.sp_files_complete / self.sp_files_checked * 100), 1) if self.sp_files_checked > 0 else 0,
                "total_errors": len(self.errors),
            },
            "details": results,
            "errors": self.errors,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA COMPLETAMENTO SEZIONI SP")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  File SP controllati: {summary['sp_files_checked']}")
        print(f"  File completi: {summary['sp_files_complete']}")
        print(f"  File incompleti: {summary['files_with_missing_sections']}")
        print(f"  Completeness rate: {summary['completeness_rate']}%")
        print(f"  ❌ Errori: {summary['total_errors']}\n")

        # Mostra file incompleti
        incomplete = [r for r in report["details"] if r["missing_sections"]]
        if incomplete:
            print(f"❌ FILE INCOMPLETI ({len(incomplete)}):")
            for result in incomplete[:10]:
                print(f"  • {result['file']}")
                print(f"    Mancanti: {', '.join(result['missing_sections'])}")
            if len(incomplete) > 10:
                print(f"  ... e altri {len(incomplete) - 10} file")

        # Valutazione
        print("\n" + "="*70)
        if summary['completeness_rate'] >= 95:
            print("✅ SECTION COMPLETENESS: EXCELLENT")
            return 0
        elif summary['completeness_rate'] >= 50:
            print("⚠️  SECTION COMPLETENESS: IN PROGRESS (can improve)")
            return 0
        else:
            print("⚠️  SECTION COMPLETENESS: DEVELOPMENT PHASE")
            return 0

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "section_completeness_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = SectionValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    # Non-blocking warning (TIER 2)
    exit(0)


if __name__ == '__main__':
    main()
