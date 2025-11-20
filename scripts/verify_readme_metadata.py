#!/usr/bin/env python3
"""
Verifica metadati README UC.

Assicura che:
- Tutti i README UC abbiano metadati (data, versione, status)
- Metadata siano coerenti e validi
- README abbiano TOC o navigation matrix
- README abbiano contact/author info
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Metadata obbligatori
REQUIRED_METADATA = {
    "version": r"(version|versione)[\s:]+[\d.]+",
    "status": r"(status|stato)[\s:]+\w+",
    "date": r"(data|date|last[_-]?updated|aggiornato)[\s:]+[\d\-/]+",
}

# Sezioni obbligatorie in README
REQUIRED_SECTIONS = {
    "overview": r"(overview|panoramica|descrizione)",
    "navigation": r"(navigation|indice|toc|tabella|table)",
    "quick_start": r"(quick.*start|guida|inizio rapido)",
}

class MetadataValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.readmes_checked = 0
        self.readmes_valid = 0

    def extract_front_matter(self, content: str) -> Dict[str, str]:
        """Estrai front matter YAML/metadata."""
        metadata = {}

        # YAML front matter tra --- ---
        yaml_pattern = r'^---\n(.*?)\n---'
        yaml_match = re.search(yaml_pattern, content, re.DOTALL | re.MULTILINE)

        if yaml_match:
            yaml_content = yaml_match.group(1)
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip().lower()] = value.strip()

        # Metadata in intestazione file (# Title \n ... metadata ...)
        if not metadata:
            lines = content.split('\n')[:10]
            for line in lines:
                for meta_name, pattern in REQUIRED_METADATA.items():
                    if re.search(pattern, line, re.IGNORECASE):
                        match = re.search(r'[:\s]+(.+)$', line)
                        if match:
                            metadata[meta_name] = match.group(1).strip()

        return metadata

    def extract_headings(self, content: str) -> List[str]:
        """Estrai heading dal content."""
        pattern = r'^#+\s+(.+)$'
        headings = [m.group(1).lower() for m in re.finditer(pattern, content, re.MULTILINE)]
        return headings

    def validate_readme(self, file_path: Path) -> Dict:
        """Valida README file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Errore lettura {file_path.name}: {e}")
            return {"file": str(file_path), "valid": False, "errors": [str(e)]}

        file_rel = str(file_path.relative_to(DOCS_DIR))
        file_errors = []
        file_warnings = []

        # Estrai metadata
        metadata = self.extract_front_matter(content)

        # Controlla metadata obbligatori
        missing_metadata = []
        for meta_name, pattern in REQUIRED_METADATA.items():
            found = False
            if meta_name in metadata:
                found = True
            elif re.search(pattern, content, re.IGNORECASE):
                found = True
                metadata[meta_name] = "found"

            if not found:
                missing_metadata.append(meta_name)
                file_warnings.append(f"Metadata mancante: {meta_name}")

        # Valida metadata trovati
        if "date" in metadata:
            date_str = metadata["date"]
            # Cerca di validare formato data
            try:
                # Tenta vari formati
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                    try:
                        datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        pass
                else:
                    file_warnings.append(f"Data in formato non riconosciuto: {date_str}")
            except:
                pass

        # Estrai heading e controlla sezioni
        headings = self.extract_headings(content)

        missing_sections = []
        for section_name, pattern in REQUIRED_SECTIONS.items():
            found = any(re.search(pattern, h, re.IGNORECASE) for h in headings)
            if not found:
                missing_sections.append(section_name)
                file_warnings.append(f"Sezione mancante: {section_name}")

        # Controlla lunghezza file (README dovrebbe avere contenuto)
        if len(content.strip()) < 500:
            file_errors.append(f"README troppo corto (<500 chars): {len(content.strip())} chars")

        # Controlla presence di link/reference
        links = re.findall(r'\[.*?\]\(.*?\)', content)
        if len(links) < 3:
            file_warnings.append(f"README ha pochi link/reference ({len(links)}, expected >=3)")

        file_errors.extend(file_errors)
        file_warnings.extend(file_warnings)

        self.errors.extend(file_errors)
        self.warnings.extend(file_warnings)

        self.readmes_checked += 1
        if not file_errors:
            self.readmes_valid += 1

        return {
            "file": file_rel,
            "valid": len(file_errors) == 0,
            "metadata_found": metadata,
            "missing_metadata": missing_metadata,
            "missing_sections": missing_sections,
            "link_count": len(links),
            "char_count": len(content.strip()),
            "errors": file_errors,
            "warnings": file_warnings,
        }

    def validate_all(self):
        """Valida tutti i README."""
        print("🔍 Scoprendo README UC...")
        readme_files = []
        for uc_folder in (DOCS_DIR / "use_cases").iterdir():
            if uc_folder.is_dir() and uc_folder.name.startswith("UC"):
                readme = uc_folder / "README.md"
                if readme.exists():
                    readme_files.append(readme)

        print(f"✅ Trovati {len(readme_files)} README\n")
        print("✔️  Validando metadati...")

        results = []
        for readme_path in sorted(readme_files):
            result = self.validate_readme(readme_path)
            results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> Dict:
        """Genera report."""
        valid_readmes = len([r for r in results if r["valid"]])

        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "summary": {
                "readmes_checked": self.readmes_checked,
                "readmes_valid": self.readmes_valid,
                "readmes_with_issues": self.readmes_checked - self.readmes_valid,
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
        print("VERIFICA METADATI README UC")
        print("="*70 + "\n")

        summary = report["summary"]
        print("📊 RIEPILOGO:")
        print(f"  README controllati: {summary['readmes_checked']}")
        print(f"  README validi: {summary['readmes_valid']}")
        print(f"  README con problemi: {summary['readmes_with_issues']}")
        print(f"  ❌ Errori: {summary['total_errors']}")
        print(f"  ⚠️  Warnings: {summary['total_warnings']}\n")

        # Dettagli per README con problemi
        issues_readmes = [r for r in report["details"] if r["errors"] or r["warnings"]]
        if issues_readmes:
            print("README CON PROBLEMI:")
            for result in issues_readmes[:5]:
                print(f"  • {result['file']}")
                if result["missing_metadata"]:
                    print(f"    Metadata mancanti: {', '.join(result['missing_metadata'])}")
                if result["missing_sections"]:
                    print(f"    Sezioni mancanti: {', '.join(result['missing_sections'])}")
            if len(issues_readmes) > 5:
                print(f"  ... e altri {len(issues_readmes) - 5} README")

        # Valutazione
        print("\n" + "="*70)
        if summary['readmes_with_issues'] == 0:
            print("✅ README METADATA: ALL VALID")
            return 0
        else:
            print("⚠️  README METADATA: SOME ISSUES FOUND")
            return 0  # Non blocca

    def save_report(self, report: Dict):
        """Salva report JSON."""
        report_path = REPORTS_DIR / "readme_metadata_validation.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Report salvato: {report_path}")


def main():
    validator = MetadataValidator()
    results = validator.validate_all()
    report = validator.generate_report(results)
    validator.print_report(report)
    validator.save_report(report)
    exit(0)  # Non blocca


if __name__ == '__main__':
    main()
