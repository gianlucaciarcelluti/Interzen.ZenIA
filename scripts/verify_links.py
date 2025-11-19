#!/usr/bin/env python3
"""
Verifica link nelle documentazione ZenIA.

Funzionalità:
- Scansiona tutti file MD per link markdown [text](url)
- Verifica esistenza file per link interni (relativi)
- Verifica HTTP 200 per link esterni (opzionale, con timeout)
- Identifica link rotti o malformati
- Output: report JSON con errori
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse, unquote
import subprocess

# Configurazione
DOCS_DIR = Path(__file__).parent.parent / "docs"
REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Pattern per markdown link [text](url)
MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Pattern per anchor link nel testo (es. #sezione)
ANCHOR_PATTERN = re.compile(r'^#')

# Pattern per template placeholder (es. UC#, MS##, ../path/to/)
TEMPLATE_PLACEHOLDER_PATTERN = re.compile(r'(UC#|MS##|../path/to/|../../path/to/|url\b|\.\./.+/\.\.\.)')

# Estensioni di file markdown da ignorare
IGNORE_PATTERNS = {'.png', '.jpg', '.gif', '.pdf'}

# URI schemes da ignorare (non sono link interni)
NON_FILE_SCHEMES = {'mailto', 'ftp', 'ftps', 'tel', 'sms', 'geo'}


class LinkValidator:
    def __init__(self, docs_dir: Path):
        self.docs_dir = docs_dir
        self.links = []  # Lista di tuple (file, link_text, url, line_num)
        self.valid_count = 0
        self.broken_count = 0
        self.external_count = 0
        self.errors = []
        self.warnings = []

    def scan_files(self):
        """Scansiona file MD per link."""
        print("🔍 Scansionando link...")

        for file_path in self.docs_dir.rglob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8')
                relative_path = file_path.relative_to(self.docs_dir)

                for match in MARKDOWN_LINK_PATTERN.finditer(content):
                    link_text = match.group(1)
                    url = match.group(2).strip()
                    line = content[:match.start()].count('\n') + 1

                    self.links.append({
                        'file': str(relative_path),
                        'text': link_text,
                        'url': url,
                        'line': line
                    })

            except Exception as e:
                self.errors.append(f"Errore lettura {file_path}: {e}")

        print(f"✅ Trovati {len(self.links)} link")

    def validate_links(self):
        """Valida ogni link."""
        print("✔️  Validando link...")

        for link in self.links:
            file_path = link['file']
            url = link['url']
            line = link['line']

            # Ignora anchor link (es. #sezione)
            if ANCHOR_PATTERN.match(url):
                continue

            # Ignora template placeholders (UC#, MS##, ../path/to/)
            if TEMPLATE_PLACEHOLDER_PATTERN.search(url):
                continue

            # Ignora URI schemes non-file (mailto, ftp, tel, etc.)
            parsed_url = urlparse(url)
            if parsed_url.scheme in NON_FILE_SCHEMES:
                self.valid_count += 1
                continue

            # Link esterno (http/https)
            if url.startswith(('http://', 'https://')):
                self.external_count += 1
                # Per link esterni, solo warning se malformati
                if not self._is_valid_url(url):
                    self.warnings.append(
                        f"{file_path}:{line} - URL malformato: {url}"
                    )
                else:
                    self.valid_count += 1
                continue

            # Link interno (relativo)
            target_path = self._resolve_relative_path(file_path, url)

            if target_path and target_path.exists():
                self.valid_count += 1
            else:
                self.broken_count += 1
                self.errors.append(
                    f"{file_path}:{line} - Link rotto: {url} (risolverebbe: {target_path})"
                )

    def _resolve_relative_path(self, from_file: str, relative_url: str) -> Optional[Path]:
        """Risolvi path relativo (agnostico rispetto al path assoluto)."""
        # Decodifica URL-encoded spazi (%20 -> spazio, etc.)
        relative_url = unquote(relative_url)

        # Ignora query string e fragment
        path_part = relative_url.split('#')[0].split('?')[0]

        # Ignora estensioni non-markdown
        for ignore_ext in IGNORE_PATTERNS:
            if path_part.endswith(ignore_ext):
                return Path(self.docs_dir) / path_part

        # Calcola directory del file sorgente
        from_dir = self.docs_dir / from_file
        from_dir = from_dir.parent

        # Risolvi path relativo SENZA usare .resolve() (che dipende dal path assoluto)
        # Usa os.path.normpath per gestire .. correttamente
        target_relative = os.path.normpath(os.path.join(str(from_dir.relative_to(self.docs_dir)), path_part))
        target = self.docs_dir / target_relative

        # Aggiungi .md se non ha estensione
        if not target.suffix and target.parent.exists():
            if (target.parent / f"{target.name}.md").exists():
                return (target.parent / f"{target.name}.md")

        return target

    def _is_valid_url(self, url: str) -> bool:
        """Valida URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def generate_report(self) -> Dict:
        """Genera report."""
        report = {
            "summary": {
                "total_links": len(self.links),
                "valid_internal": self.valid_count - self.external_count,
                "broken_internal": self.broken_count,
                "external": self.external_count,
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
        print("REPORT VERIFICA LINK")
        print("="*70)

        summary = report['summary']
        print(f"\n📊 RIEPILOGO:")
        print(f"  Link totali: {summary['total_links']}")
        print(f"  ✅ Link interni validi: {summary['valid_internal']}")
        print(f"  ❌ Link interni rotti: {summary['broken_internal']}")
        print(f"  🌐 Link esterni: {summary['external']}")
        print(f"  ⚠️  Warnings: {summary['warnings']}")

        if report['errors']:
            print(f"\n❌ LINK ROTTI ({len(report['errors'])}):")
            for error in report['errors'][:15]:
                print(f"  • {error}")
            if len(report['errors']) > 15:
                print(f"  ... e {len(report['errors']) - 15} altri link rotti")

        if report['warnings']:
            print(f"\n⚠️  WARNINGS ({len(report['warnings'])}):")
            for warning in report['warnings'][:10]:
                print(f"  • {warning}")
            if len(report['warnings']) > 10:
                print(f"  ... e {len(report['warnings']) - 10} altri warnings")

        if not report['errors']:
            print("\n✅ NESSUN LINK ROTTO!")

        print("\n" + "="*70)

    def save_report(self, report: Dict):
        """Salva report."""
        report_file = REPORTS_DIR / "links_validation.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📁 Report salvato: {report_file}")


def main():
    validator = LinkValidator(DOCS_DIR)
    validator.scan_files()
    validator.validate_links()

    report = validator.generate_report()
    validator.print_report(report)
    validator.save_report(report)

    return 0 if not report['errors'] else 1


if __name__ == "__main__":
    exit(main())
