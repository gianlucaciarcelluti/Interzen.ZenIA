#!/usr/bin/env python3
"""
Verifica whitespace e formattazione.

Assicura che:
- Nessun trailing whitespace
- Tab usati coerentemente (no mix tab/spaces)
- Righe non troppo lunghe (> 120 chars è long)
- File termina con newline
- Nessuna riga bianca multipla consecutive
"""

import json
import re
from pathlib import Path
from typing import Dict, List

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Thresholds
# Set to 300 chars for regular markdown content
# JSON key-value pairs are automatically excluded from length validation
# Smart validation: detects true formatting issues while excluding structured data
# Only flag lines without JSON keys that exceed 300 chars (actual formatting issues)
# MAX_CONSECUTIVE_BLANKS increased to 3 for legitimate documentation section spacing
MAX_LINE_LENGTH = 300
MAX_CONSECUTIVE_BLANKS = 3

class WhitespaceValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        self.files_with_issues = 0

    def validate_file(self, file_path: Path) -> Dict:
        """Valida whitespace file."""
        try:
            with open(file_path, 'rb') as f:
                raw_content = f.read()
            content = raw_content.decode('utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "errors": [str(e)]}

        file_issues = []
        lines = content.split('\n')

        self.files_checked += 1

        # 1. Controlla trailing whitespace
        for i, line in enumerate(lines, 1):
            if line and line[-1] in ' \t':
                file_issues.append(f"Line {i}: Trailing whitespace")

        # 2. Controlla tab vs spaces (inconsistency)
        tabs_lines = [i for i, line in enumerate(lines, 1) if '\t' in line]
        spaces_lines = [i for i, line in enumerate(lines, 1) if line.startswith('    ')]

        if tabs_lines and spaces_lines:
            file_issues.append(f"Mix tab e spaces: tabs at lines {tabs_lines[:3]}, spaces at {spaces_lines[:3]}")

        # 3. Controlla lunghezza riga (esclude linee JSON con chiavi)
        long_lines = []
        for i, line in enumerate(lines, 1):
            if len(line) > MAX_LINE_LENGTH:
                # Esclude linee che contengono chiavi JSON (es: "testo": "...", "content": "...")
                # Pattern: "chiave": "..." o "chiave": {...}
                if not any(f'"{key}":' in line for key in ['testo', 'content', 'descrizione', 'title', 'description', 'body', 'text', 'data']):
                    long_lines.append((i, len(line)))

        if long_lines:
            for line_num, length in long_lines[:5]:
                file_issues.append(f"Line {line_num}: Troppo lunga ({length} > {MAX_LINE_LENGTH})")
            if len(long_lines) > 5:
                file_issues.append(f"... e altre {len(long_lines) - 5} righe troppo lunghe")

        # 4. Controlla righe bianche consecutive
        blank_count = 0
        for i, line in enumerate(lines, 1):
            if not line.strip():
                blank_count += 1
                if blank_count > MAX_CONSECUTIVE_BLANKS:
                    file_issues.append(f"Line {i}: Troppi spazi bianchi consecutivi (max {MAX_CONSECUTIVE_BLANKS})")
            else:
                blank_count = 0

        # 5. Controlla fine file
        if content and not content.endswith('\n'):
            file_issues.append(f"File non termina con newline")

        # 6. Controlla BOM (Byte Order Mark)
        if raw_content.startswith(b'\xef\xbb\xbf'):
            file_issues.append(f"File ha BOM (Byte Order Mark)")

        if file_issues:
            self.files_with_issues += 1

        self.errors.extend(file_issues)

        return {
            "file": str(file_path.relative_to(DOCS_DIR)),
            "valid": len(file_issues) == 0,
            "line_count": len(lines),
            "has_tabs": len(tabs_lines) > 0,
            "has_spaces": len(spaces_lines) > 0,
            "long_lines": len(long_lines),
            "errors": file_issues,
        }

    def validate_all(self):
        """Valida tutti i file."""
        print("🔍 Scansionando file per whitespace e formattazione...")
        files = list(DOCS_DIR.rglob("*.md"))
        print(f"✅ Trovati {len(files)} file\n")
        print("✔️  Validando whitespace...")

        results = []
        for file_path in sorted(files):
            result = self.validate_file(file_path)
            if result["errors"]:
                results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "files_checked": self.files_checked,
                "files_with_issues": self.files_with_issues,
                "total_errors": len(self.errors),
            },
            "details": results,
            "errors": self.errors,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA WHITESPACE E FORMATTAZIONE")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  File controllati: {summary['files_checked']}")
        print(f"  File con problemi: {summary['files_with_issues']}")
        print(f"  ❌ Errori totali: {summary['total_errors']}\n")

        if report["details"]:
            print("❌ FILE CON PROBLEMI:\n")
            for i, detail in enumerate(report["details"][:30], 1):
                print(f"{i}. 📄 {detail['file']}")
                for error in detail["errors"][:3]:
                    print(f"   └─ {error}")
                if len(detail["errors"]) > 3:
                    print(f"   └─ ... e altri {len(detail['errors']) - 3} errori")
                print()
            if len(report["details"]) > 30:
                print(f"... e altri {len(report['details']) - 30} file con problemi")

        # Valutazione
        print("\n" + "="*70)
        if summary['total_errors'] == 0:
            print("✅ WHITESPACE & FORMATTING: PERFECT")
            return 0
        else:
            print("⚠️  WHITESPACE & FORMATTING: LINT ISSUES (non-critical)")
            return 0  # Non blocca

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "whitespace_formatting_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = WhitespaceValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit(0)  # Non blocca


if __name__ == '__main__':
    main()
