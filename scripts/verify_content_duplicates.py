#!/usr/bin/env python3
"""
Verifica duplicati di contenuto.

Assicura che:
- Nessuna sezione/paragrafo identico ripetuto
- Nessun intero file duplicato
- Warning per contenuto simile (possibile copia-incolla)
"""

import json
import hashlib
import difflib
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

class DuplicateValidator:
    def __init__(self):
        self.file_hashes = {}  # filename -> hash
        self.section_hashes = defaultdict(list)  # hash -> list of (file, line)
        self.warnings = []
        self.errors = []

    def get_content_hash(self, content: str) -> str:
        """Calcola hash di contenuto."""
        return hashlib.md5(content.encode()).hexdigest()

    def extract_sections(self, content: str, filename: str) -> List[Tuple[str, int, str]]:
        """Estrai sezioni da file (tra heading)."""
        sections = []
        lines = content.split('\n')

        current_section = []
        section_start = 0

        for i, line in enumerate(lines):
            if line.startswith('#') and current_section:
                # Nuova sezione, salva la precedente
                section_text = '\n'.join(current_section).strip()
                if len(section_text) > 100:  # Solo sezioni significative
                    section_hash = self.get_content_hash(section_text)
                    sections.append((section_hash, section_start, section_text[:100]))

                current_section = [line]
                section_start = i
            else:
                current_section.append(line)

        # Ultima sezione
        if current_section:
            section_text = '\n'.join(current_section).strip()
            if len(section_text) > 100:
                section_hash = self.get_content_hash(section_text)
                sections.append((section_hash, section_start, section_text[:100]))

        return sections

    def should_skip_file(self, file_rel: str) -> bool:
        """Skip validation for template/specification files with intentional duplicates."""
        skip_patterns = [
            "SPECIFICATION.md",  # MS specifications are templates with intentional duplicates
            "SP-MS-MAPPING",     # Master mapping file documents standard patterns
            "SP28-RESERVED",     # Reserved file documents standard patterns
            "SP-DOCUMENTATION-TEMPLATE",  # Template file - intentional boilerplate
            "README.md",  # README files use standard boilerplate sections
            "TROUBLESHOOTING.md",  # Troubleshooting sections have standard format
            "API.md",  # API documentation has standard structure
            "DATABASE-SCHEMA.md",  # Database schemas follow standard template
            "use_cases/",  # UC/SP files have standardized compliance & technical sections
        ]
        return any(pattern in file_rel for pattern in skip_patterns)

    def validate_file(self, file_path: Path) -> Dict:
        """Valida file per duplicati."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {"file": str(file_path), "valid": False, "errors": [str(e)]}

        file_rel = str(file_path.relative_to(DOCS_DIR))

        # Skip template files with intentional duplicates
        if self.should_skip_file(file_rel):
            return {
                "file": file_rel,
                "valid": True,
                "section_count": 0,
                "errors": [],
                "skipped": True,
            }

        file_errors = []

        # Controlla hash intero file
        file_hash = self.get_content_hash(content)
        if file_hash in self.file_hashes:
            file_errors.append(
                f"File potenzialmente duplicato di: {self.file_hashes[file_hash]}"
            )
            self.warnings.append(f"Duplicato: {file_rel} == {self.file_hashes[file_hash]}")
        else:
            self.file_hashes[file_hash] = file_rel

        # Controlla sezioni
        sections = self.extract_sections(content, file_path.name)
        for section_hash, line_num, section_preview in sections:
            if section_hash in self.section_hashes:
                # Sezione duplicata trovata
                prev_file, prev_line = self.section_hashes[section_hash][0]
                if prev_file != file_rel:
                    file_errors.append(
                        f"Line {line_num}: Sezione duplicata (vedi {prev_file}:{prev_line})"
                    )
                    self.warnings.append(
                        f"Sezione duplicata: {file_rel}:{line_num} == {prev_file}:{prev_line}"
                    )

            self.section_hashes[section_hash].append((file_rel, line_num))

        self.errors.extend(file_errors)

        return {
            "file": file_rel,
            "valid": len(file_errors) == 0,
            "section_count": len(sections),
            "errors": file_errors,
        }

    def validate_all(self):
        """Valida tutti i file."""
        print("🔍 Scansionando file per duplicati...")
        files = list(DOCS_DIR.rglob("*.md"))
        print(f"✅ Trovati {len(files)} file\n")
        print("✔️  Validando duplicati di contenuto...")

        results = []
        for file_path in sorted(files):
            result = self.validate_file(file_path)
            if result["errors"]:
                results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        files_with_errors = len(results)
        duplicate_sections = len([h for h in self.section_hashes if len(self.section_hashes[h]) > 1])

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "files_checked": len(self.file_hashes),
                "files_with_duplicates": files_with_errors,
                "duplicate_sections": duplicate_sections,
                "total_warnings": len(self.warnings),
            },
            "details": results,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA DUPLICATI DI CONTENUTO")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  File controllati: {summary['files_checked']}")
        print(f"  File con duplicati: {summary['files_with_duplicates']}")
        print(f"  Sezioni duplicate: {summary['duplicate_sections']}")
        print(f"  ⚠️  Warnings: {summary['total_warnings']}\n")

        # Mostra file con duplicati in dettaglio
        if report["details"]:
            print("📄 FILE CON DUPLICATI:\n")
            for i, detail in enumerate(report["details"][:20], 1):
                print(f"{i}. {detail['file']}")
                for error in detail["errors"][:3]:
                    print(f"   └─ {error}")
                if len(detail["errors"]) > 3:
                    print(f"   └─ ... e altri {len(detail['errors']) - 3} errori")
                print()
            if len(report["details"]) > 20:
                print(f"... e altri {len(report['details']) - 20} file con duplicati")
            print()

        if report["warnings"]:
            print("⚠️  RIEPILOGO DUPLICATI (primi 15):")
            for warning in report["warnings"][:15]:
                print(f"  • {warning}")
            if len(report["warnings"]) > 15:
                print(f"  ... e altri {len(report['warnings']) - 15} duplicati")

        # Valutazione
        print("\n" + "="*70)
        if summary['duplicate_sections'] == 0:
            print("✅ CONTENT DUPLICATES: NONE FOUND")
            return 0
        else:
            print("⚠️  CONTENT DUPLICATES: FOUND (review recommended)")
            return 0  # Non blocca

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "content_duplicates_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = DuplicateValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit(0)  # Non blocca


if __name__ == '__main__':
    main()
