#!/usr/bin/env python3
"""
Verifica coerenza heading Markdown.

Assicura che:
- Heading siano ben formati (# ## ### ecc.)
- Gerarchia heading sia corretta (no salti: # -> ### senza ##)
- Nessun heading duplicato nello stesso file
- Heading siano maiuscoli/minuscoli coerenti
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

class HeadingValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.files_checked = 0
        self.issues_found = defaultdict(list)

    def validate_file(self, file_path: Path) -> Dict:
        """Valida heading in un file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "errors": [str(e)]}

        file_errors = []
        file_warnings = []
        heading_pattern = re.compile(r'^(#+)\s+(.+)$', re.MULTILINE)

        # Estrai tutti gli heading, escludendo quelli dentro code blocks
        headings = []
        in_code_block = False
        lines = content.split('\n')
        line_num = 0

        for line_idx, line in enumerate(lines, 1):
            # Traccia code block markers (triple backticks)
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            # Salta linee dentro code blocks
            if in_code_block:
                continue

            # Estrai heading solo fuori code blocks
            match = heading_pattern.match(line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    "level": level,
                    "text": text,
                    "line": line_idx,
                })

        # Valida gerarchia
        if headings:
            # Primo heading dovrebbe essere level 1
            if headings[0]["level"] != 1:
                file_warnings.append(f"Line {headings[0]['line']}: Primo heading non è H1 (è H{headings[0]['level']})")

            # Controlla salti di livello
            for i in range(1, len(headings)):
                prev_level = headings[i-1]["level"]
                curr_level = headings[i]["level"]

                if curr_level > prev_level + 1:
                    file_errors.append(
                        f"Line {headings[i]['line']}: Salto heading: H{prev_level} -> H{curr_level} "
                        f"(dovrebbe essere H{prev_level + 1})"
                    )

            # Controlla duplicati heading nello stesso livello (stesso UC/sezione)
            heading_texts = defaultdict(list)
            for h in headings:
                key = (h["level"], h["text"].lower())
                heading_texts[key].append(h["line"])

            for (level, text), lines in heading_texts.items():
                if len(lines) > 1:
                    file_warnings.append(
                        f"Heading duplicato (H{level}): '{text}' appears at lines {lines}"
                    )

        # Valida formato heading
        for h in headings:
            # Heading vuoto
            if not h["text"]:
                file_errors.append(f"Line {h['line']}: Heading vuoto (H{h['level']})")

            # Heading con caratteri speciali problematici
            if re.search(r'[\{\}<>|\\]', h["text"]):
                file_warnings.append(
                    f"Line {h['line']}: Heading contiene caratteri speciali: '{h['text']}'"
                )

        # Valida coerenza capitalizzazione (Title Case vs lowercase)
        title_case_headings = [h for h in headings if h["level"] <= 2 and h["text"][0].isupper()]
        lowercase_headings = [h for h in headings if h["level"] <= 2 and h["text"][0].islower()]

        if title_case_headings and lowercase_headings:
            file_warnings.append(
                f"Capitalizzazione incoerente: mix Title Case e lowercase in H1-H2"
            )

        self.files_checked += 1
        self.errors.extend(file_errors)
        self.warnings.extend(file_warnings)

        return {
            "file": str(file_path.relative_to(DOCS_DIR)),
            "valid": len(file_errors) == 0,
            "heading_count": len(headings),
            "errors": file_errors,
            "warnings": file_warnings,
        }

    def validate_all(self):
        """Valida tutti i file MD."""
        print("🔍 Scansionando file Markdown...")
        files = list(DOCS_DIR.rglob("*.md"))
        print(f"✅ Trovati {len(files)} file\n")
        print("✔️  Validando heading...")

        results = []
        for file_path in sorted(files):
            result = self.validate_file(file_path)
            if result["errors"] or result["warnings"]:
                results.append(result)
                if result["errors"]:
                    self.issues_found[str(result["file"])] = result["errors"]

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        files_with_errors = len([r for r in results if r["errors"]])
        files_with_warnings = len([r for r in results if r["warnings"] and not r["errors"]])

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "files_checked": self.files_checked,
                "files_with_errors": files_with_errors,
                "files_with_warnings": files_with_warnings,
                "total_errors": len(self.errors),
                "total_warnings": len(self.warnings),
            },
            "details": results,
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return report

    def print_report(self, report: Dict):
        """Stampa report."""
        print("\n" + "="*70)
        print("VERIFICA COERENZA HEADING MARKDOWN")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  File processati: {summary['files_checked']}")
        print(f"  File con errori: {summary['files_with_errors']}")
        print(f"  File con warnings: {summary['files_with_warnings']}")
        print(f"  ❌ Errori totali: {summary['total_errors']}")
        print(f"  ⚠️  Warnings totali: {summary['total_warnings']}\n")

        # Mostra errori
        if report["errors"]:
            print("="*70)
            print("❌ ERRORI (primi 15):")
            for i, error in enumerate(report["errors"][:15]):
                print(f"  {i+1}. {error}")
            if len(report["errors"]) > 15:
                print(f"  ... e altri {len(report['errors']) - 15} errori")

        # Mostra warnings
        if report["warnings"]:
            print("\n" + "="*70)
            print("⚠️  WARNINGS (primi 15):")
            for i, warning in enumerate(report["warnings"][:15]):
                print(f"  {i+1}. {warning}")
            if len(report["warnings"]) > 15:
                print(f"  ... e altri {len(report['warnings']) - 15} warnings")

        # Valutazione
        print("\n" + "="*70)
        if summary['total_errors'] == 0:
            print("✅ MARKDOWN HEADINGS: VALID")
            return 0
        else:
            print("❌ MARKDOWN HEADINGS: NEEDS FIXING")
            return 1

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "markdown_headings_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = HeadingValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit_code = 0 if not validator.errors else 1
    exit(exit_code)


if __name__ == '__main__':
    main()
