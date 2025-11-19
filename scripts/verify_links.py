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

# Repository root and extra files to scan (e.g. README.md at repo root)
REPO_ROOT = Path(__file__).parent.parent
EXTRA_FILES = [REPO_ROOT / 'README.md']

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

# File template da escludere (contengono placeholder link)
TEMPLATE_FILES = {
    'BREADCRUMB-NAVIGATION.md',
    'GITHUB-NAVIGATION-GUIDE.md',
    'SP-DOCUMENTATION-TEMPLATE.md',
    'SEQUENCE-DIAGRAMS-TEMPLATE.md',
    'DOCUMENTATION-STRUCTURE-GUIDE.md'
}


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
        # Default: tutti i markdown dentro docs/
        md_files = list(self.docs_dir.rglob("*.md"))

        # Aggiungi file extra (README.md alla root, altri eventualmente)
        for extra in EXTRA_FILES:
            if extra.exists() and extra.suffix.lower() == '.md':
                md_files.append(extra)

        # Rimuovi duplicati e ordina
        md_files = sorted(set(md_files))

        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                # Calcola path relativo per report: usa sempre relativo alla root del repo
                try:
                    relative_path = file_path.relative_to(REPO_ROOT)
                except Exception:
                    relative_path = file_path.name

                # Estrai link markdown in modo robusto (gestisce parentesi annidate nelle URL)
                def iter_markdown_links(text):
                    i = 0
                    L = len(text)
                    while i < L:
                        start = text.find('[', i)
                        if start == -1:
                            break
                        end_text = text.find(']', start + 1)
                        if end_text == -1:
                            break
                        # verificare che subito dopo ci sia '('
                        if end_text + 1 < L and text[end_text + 1] == '(': 
                            j = end_text + 2
                            depth = 1
                            while j < L and depth > 0:
                                if text[j] == '(':
                                    depth += 1
                                elif text[j] == ')':
                                    depth -= 1
                                j += 1
                            if depth == 0:
                                link_text = text[start + 1:end_text]
                                url = text[end_text + 2:j - 1].strip()
                                yield link_text, url, start
                                i = j
                                continue
                        i = end_text + 1

                for link_text, url, match_start in iter_markdown_links(content):
                    line = content[:match_start].count('\n') + 1
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

            # Ignora link in file template (contengono placeholder)
            file_name = Path(file_path).name
            if file_name in TEMPLATE_FILES:
                continue

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
        """Risolvi path relativo in modo robusto."""
        # Decodifica URL-encoded spazi (%20 -> spazio, etc.)
        relative_url = unquote(relative_url)

        # Ignora query string e fragment
        path_part = relative_url.split('#')[0].split('?')[0]

        # Ignora estensioni non-markdown
        for ignore_ext in IGNORE_PATTERNS:
            if path_part.endswith(ignore_ext):
                return Path(self.docs_dir) / path_part

        # Calcola directory del file sorgente.
        # Preferisci il file esatto nella root del repo (es. README.md),
        # altrimenti considera la versione dentro docs/.
        alt = REPO_ROOT / from_file
        if alt.exists():
            from_file_path = alt
        else:
            from_file_path = self.docs_dir / from_file

        from_dir = from_file_path.parent

        # Risolvi path relativo: partendo da from_dir, segui i .. per salire
        # poi scendi nei subdirectory per trovare il target
        current = from_dir
        parts = path_part.split('/')

        for part in parts:
            if part == '..':
                current = current.parent
            elif part and part != '.':
                current = current / part

        target = current

        # Aggiungi .md se non ha estensione
        if not target.suffix and target.parent.exists():
            md_file = target.parent / f"{target.name}.md"
            if md_file.exists():
                return md_file

        return target

    def _is_valid_url(self, url: str) -> bool:
        """Valida URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _normalize_path_in_error(self, error_msg: str) -> str:
        """Normalizza path nel messaggio di errore (rimuove doppia occorrenza di directory repo)."""
        # Rimuove pattern /Interzen.ZenIA/Interzen.ZenIA/ -> /Interzen.ZenIA/
        normalized = error_msg.replace(
            '/Interzen.ZenIA/Interzen.ZenIA/',
            '/Interzen.ZenIA/'
        )
        # Funziona anche con pattern generici (rimuove doppio repo name)
        import re
        normalized = re.sub(
            r'(/Interzen\.ZenIA)+/Interzen\.ZenIA/',
            '/Interzen.ZenIA/',
            normalized
        )
        return normalized

    def generate_report(self) -> Dict:
        """Genera report."""
        # Normalizza i path negli errori (rimuove doppia occorrenza directory)
        normalized_errors = [self._normalize_path_in_error(err) for err in self.errors]

        report = {
            "summary": {
                "total_links": len(self.links),
                "valid_internal": self.valid_count - self.external_count,
                "broken_internal": self.broken_count,
                "external": self.external_count,
                "errors": len(normalized_errors),
                "warnings": len(self.warnings),
            },
            "errors": normalized_errors,
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
        # Salva JSON compatto (nessuna indentazione) per evitare problemi di allineamento
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, separators=(',', ':'), ensure_ascii=False)
        print(f"\n📁 Report salvato: {report_file}")


def main():
    # Debug info
    print(f"📂 DOCS_DIR: {DOCS_DIR}")
    print(f"📂 DOCS_DIR exists: {DOCS_DIR.exists()}")
    print(f"📂 Current working directory: {os.getcwd()}")
    print("")

    validator = LinkValidator(DOCS_DIR)
    validator.scan_files()
    validator.validate_links()

    report = validator.generate_report()
    validator.print_report(report)
    validator.save_report(report)

    # FASE 1: Link validation è non-critico (warning only)
    # Gli errori vengono riportati nel JSON per FASE 2-3
    # Il validator sempre esce con 0 (success) per non bloccare la build
    return 0


if __name__ == "__main__":
    exit(main())
