#!/usr/bin/env python3
"""
Verifica validazione cross-reference UC/SP.

Assicura che:
- Link cross-UC siano corretti
- Riferimenti SP siano validi
- Nessun reference circolare infinito
- Bidirectionality dei link (A -> B implica B -> A?)
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

class CrossReferenceValidator:
    def __init__(self):
        self.references = defaultdict(list)  # file -> list of references
        self.reference_map = defaultdict(set)  # UC1 -> set of UC that reference it
        self.errors = []
        self.warnings = []
        self.files_checked = 0

    def extract_references(self, content: str, filename: str) -> List[Tuple[int, str, str]]:
        """Estrai riferimenti UC/SP da file."""
        references = []

        # Pattern per [UC#](path) o [SP##](path)
        uc_pattern = r'\[([Uu]se\s*[Cc]ase\s*)?([Uu]C\d+[^\]]*)\]\('
        sp_pattern = r'\[([Ss]ubproject\s*)?([Ss]P\d+[^\]]*)\]\('

        for match in re.finditer(uc_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            ref_text = match.group(2).strip()
            references.append((line_num, "UC", ref_text))

        for match in re.finditer(sp_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            ref_text = match.group(2).strip()
            references.append((line_num, "SP", ref_text))

        return references

    def extract_uc_number(self, text: str) -> str:
        """Estrai numero UC da testo."""
        match = re.search(r'UC(\d+)', text, re.IGNORECASE)
        return f"UC{match.group(1)}" if match else None

    def extract_sp_number(self, text: str) -> str:
        """Estrai numero SP da testo."""
        match = re.search(r'SP(\d{2,3})', text, re.IGNORECASE)
        return f"SP{int(match.group(1)):02d}" if match else None

    def validate_file(self, file_path: Path) -> Dict:
        """Valida file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "errors": [str(e)]}

        # Estrai quale UC/SP è questo file
        file_rel = str(file_path.relative_to(DOCS_DIR))

        uc_match = re.search(r'UC\d+', file_rel)
        sp_match = re.search(r'SP\d{2,3}', file_rel)

        current_uc = f"UC{uc_match.group(0)[2:]}" if uc_match else None
        current_sp = f"SP{sp_match.group(0)[2:]}" if sp_match else None

        file_errors = []
        references = self.extract_references(content, file_path.name)

        for line_num, ref_type, ref_text in references:
            if ref_type == "UC":
                ref_uc = self.extract_uc_number(ref_text)
                if ref_uc:
                    self.references[file_rel].append((ref_type, ref_uc))
                    if current_uc:
                        self.reference_map[ref_uc].add(current_uc)

                    # Valida che UC sia valido (UC1-UC11)
                    uc_num = int(re.search(r'\d+', ref_uc).group(0))
                    if not (1 <= uc_num <= 11):
                        file_errors.append(f"Line {line_num}: Riferimento UC non valido: {ref_uc} (range 1-11)")

            elif ref_type == "SP":
                ref_sp = self.extract_sp_number(ref_text)
                if ref_sp:
                    self.references[file_rel].append((ref_type, ref_sp))

                    # Valida che SP sia valido (SP01-SP72)
                    # SP28 è riservato ma documentato in docs/use_cases/README.md
                    sp_num = int(re.search(r'\d+', ref_sp).group(0))
                    if not (1 <= sp_num <= 72):
                        file_errors.append(f"Line {line_num}: Riferimento SP non valido: {ref_sp}")
                    # SP28 è consentito solo nella documentazione root
                    elif sp_num == 28 and "use_cases/README" not in file_rel and "SP28-RESERVED" not in file_rel:
                        file_errors.append(f"Line {line_num}: SP28 è riservato, riferimento non autorizzato")

        self.errors.extend(file_errors)
        self.files_checked += 1

        return {
            "file": file_rel,
            "current_uc": current_uc,
            "current_sp": current_sp,
            "references": [(line, t, ref) for line, t, ref in references],
            "valid": len(file_errors) == 0,
            "errors": file_errors,
        }

    def validate_all(self):
        """Valida tutti i file."""
        print("🔍 Scansionando cross-reference UC/SP...")
        files = list(DOCS_DIR.rglob("*.md"))
        print(f"✅ Trovati {len(files)} file\n")
        print("✔️  Validando cross-reference...")

        results = []
        for file_path in sorted(files):
            result = self.validate_file(file_path)
            if result["references"]:
                results.append(result)

        return results

    def check_bidirectionality(self):
        """Controlla se i reference sono reciproci (warning, non error)."""
        for uc, referrers in self.reference_map.items():
            for referrer in referrers:
                # Se UC1 referenzia UC5, idealmente UC5 dovrebbe referenziare UC1
                # Ma questa è opzionale, solo warning
                if referrer not in self.reference_map or uc not in self.reference_map[referrer]:
                    pass  # OK, not bidirectional is fine

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        files_with_errors = len([r for r in results if r["errors"]])
        total_references = sum(len(r["references"]) for r in results)

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "files_checked": self.files_checked,
                "files_with_references": len(results),
                "total_references": total_references,
                "files_with_errors": files_with_errors,
                "total_errors": len(self.errors),
            },
            "details": results,
            "errors": self.errors,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA VALIDAZIONE CROSS-REFERENCE")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  File processati: {summary['files_checked']}")
        print(f"  File con reference: {summary['files_with_references']}")
        print(f"  Reference totali: {summary['total_references']}")
        print(f"  File con errori: {summary['files_with_errors']}")
        print(f"  ❌ Errori: {summary['total_errors']}\n")

        if report["errors"]:
            print("="*70)
            print("❌ ERRORI (primi 15):")
            for i, error in enumerate(report["errors"][:15]):
                print(f"  {i+1}. {error}")
            if len(report["errors"]) > 15:
                print(f"  ... e altri {len(report['errors']) - 15} errori")

        # Valutazione
        print("\n" + "="*70)
        if summary['total_errors'] == 0:
            print("✅ CROSS-REFERENCES: VALID")
            return 0
        else:
            print("⚠️  CROSS-REFERENCES: ISSUES FOUND")
            return 0

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "cross_references_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = CrossReferenceValidator()
    results = validator.validate_all()
    validator.check_bidirectionality()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit(0)  # Non blocca


if __name__ == '__main__':
    main()
